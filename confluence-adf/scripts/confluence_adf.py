#!/usr/bin/env python3
"""Read, update, and verify published Confluence Cloud pages using native ADF."""

import argparse
import base64
import http.client
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG_KEYS = ("CONFLUENCE_URL", "CONFLUENCE_USERNAME", "CONFLUENCE_API_TOKEN")


class ConfluenceError(Exception):
    """A failed request or preservation check that needs operator attention."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Authenticated requests must not forward credentials to redirect targets.
        return None


def read_json(path):
    with Path(path).expanduser().open(encoding="utf-8") as file:
        return json.load(file)


def normalize_site(value):
    parsed = urllib.parse.urlsplit(value.rstrip("/"))
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "CONFLUENCE_URL must be an HTTPS context URL without credentials or query"
        )
    path = parsed.path.rstrip("/")
    if not path.endswith("/wiki"):
        path += "/wiki"
    return urllib.parse.urlunsplit(("https", parsed.netloc.lower(), path, "", ""))


def load_client(config_path=None, server="atlassian"):
    values = {key: os.environ.get(key) for key in CONFIG_KEYS}
    if not any(value is not None for value in values.values()) and config_path:
        config = read_json(config_path)
        try:
            values = config["mcpServers"][server]["env"]
        except (KeyError, TypeError) as error:
            raise ValueError(
                "MCP config must contain mcpServers[server].env"
            ) from error
    if not isinstance(values, dict) or any(
        not isinstance(values.get(key), str) or not values[key].strip()
        for key in CONFIG_KEYS
    ):
        raise ValueError(
            "Set CONFLUENCE_URL, CONFLUENCE_USERNAME, and CONFLUENCE_API_TOKEN together, "
            "or pass --mcp-config with a configured server"
        )
    site = normalize_site(values["CONFLUENCE_URL"])
    credentials = f"{values['CONFLUENCE_USERNAME']}:{values['CONFLUENCE_API_TOKEN']}"
    auth = "Basic " + base64.b64encode(credentials.encode()).decode()
    return Client(site, auth)


def validate_adf(value):
    if (
        not isinstance(value, dict)
        or value.get("type") != "doc"
        or type(value.get("version")) is not int
        or value["version"] != 1
        or not isinstance(value.get("content"), list)
    ):
        raise ValueError("Expected a native ADF doc with version 1 and a content array")
    return value


def read_adf(path):
    value = read_json(path)
    if isinstance(value, dict) and "adf" in value:
        value = value["adf"]
    return validate_adf(value)


def page_adf(page):
    body = page.get("body")
    representation = body.get("atlas_doc_format") if isinstance(body, dict) else None
    value = representation.get("value") if isinstance(representation, dict) else None
    if not isinstance(value, str) or not value:
        raise ConfluenceError(
            "Page has no native ADF body; legacy conversion is out of scope"
        )
    return validate_adf(json.loads(value))


def canonical(value):
    """Ignore mark order while keeping node order and all attributes significant."""

    def visit(node):
        if isinstance(node, dict):
            result = {
                key: visit(item) if key in ("content", "adf") else item
                for key, item in node.items()
            }
            if "type" in node and "marks" in node:
                result["marks"] = sorted(
                    node["marks"], key=lambda mark: json.dumps(mark, sort_keys=True)
                )
            return result
        if isinstance(node, list):
            return [visit(item) for item in node]
        return node

    # Serialization also preserves JSON distinctions such as true versus 1.
    return json.dumps(visit(value), ensure_ascii=False, sort_keys=True)


def differences(left, right):
    """Paths of all differing values, without the values, which can hold page data.

    Mark indexes in a path follow the sorted mark order that canonical() compares. Paths stop at
    macro parameters, whose keys can be page data.
    """
    left_text, right_text = canonical(left), canonical(right)
    if left_text == right_text:
        return []
    found = []
    missing = object()  # an absent key differs from an explicit null

    def visit(a, b, path):
        opaque = path.endswith("/attrs/parameters")
        if not opaque and isinstance(a, dict) and isinstance(b, dict):
            for key in sorted(set(a) | set(b)):
                # JSON Pointer escaping plus JSON string escaping: a key cannot add a path level
                # or a line to the report.
                segment = json.dumps(key.replace("~", "~0").replace("/", "~1"))[1:-1]
                visit(a.get(key, missing), b.get(key, missing), f"{path}/{segment}")
        elif not opaque and isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                found.append(f"{path or '/'} (length {len(a)} -> {len(b)})")
            else:
                for index, (x, y) in enumerate(zip(a, b)):
                    visit(x, y, f"{path}/{index}")
        # Serialized comparison keeps true versus 1 and -0.0 versus 0.0 distinct.
        elif (
            a is missing
            or b is missing
            or json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True)
        ):
            found.append(path or "/")

    try:
        visit(json.loads(left_text), json.loads(right_text), "")
    except RecursionError:
        # The serialized comparison above already found a difference; only its location is lost.
        return found + ["(nesting too deep to locate the rest)"]
    # The serialized texts differ, so the result must never be empty.
    return found or ["(location unknown)"]


def summarize(paths, limit=5):
    return ", ".join((paths[:limit] + ["..."]) if len(paths) > limit else paths)


def transform_adf(value, change):
    """Copy an ADF tree, letting change(node) edit each node; opaque attrs stay unwalked."""

    def visit(node):
        if isinstance(node, list):
            return [visit(item) for item in node]
        if not isinstance(node, dict):
            return node
        node = dict(node)
        for key in ("content", "marks"):
            if key in node:
                node[key] = visit(node[key])
        change(node)
        return node

    return visit(value)


# Link marks and smart cards whose page title the Cloud editor caches in __confluenceMetadata.
EDITOR_TITLE_CACHES = frozenset({"link", "inlineCard", "blockCard", "embedCard"})
# Page IDs the Cloud editor adds to a macro's macroParams.
EDITOR_MACRO_PARAMS = frozenset({"_parentId", "_referencedContentId"})


def without_editor_metadata(value):
    """Drop attributes the Cloud editor adds to its collaborative draft on its own.

    Opening a page in the editor can leave a draft with page IDs added to a macro and a cached page
    title added to a link or card. A draft that differs only by these carries no pending edit. The
    IDs can be the only macro parameters, so an empty macroParams or parameters counts as absent.
    """

    def without(mapping, names):
        return {key: item for key, item in mapping.items() if key not in names}

    def change(node):
        attrs = node.get("attrs")
        if not isinstance(attrs, dict):
            return
        if node.get("type") in EDITOR_TITLE_CACHES:
            attrs = node["attrs"] = without(attrs, {"__confluenceMetadata"})
        parameters = attrs.get("parameters")
        if not isinstance(parameters, dict):
            return
        macro = parameters.get("macroParams")
        if isinstance(macro, dict):
            macro = without(macro, EDITOR_MACRO_PARAMS)
            rest = without(parameters, {"macroParams"})
            parameters = {**rest, "macroParams": macro} if macro else rest
        node["attrs"] = (
            {**attrs, "parameters": parameters}
            if parameters
            else without(attrs, {"parameters"})
        )

    return transform_adf(value, change)


# The single last path segment after .../spaces/KEY/pages/ID is the title. Any HTTPS host matches,
# since Confluence sites can use custom domains and the API gateway.
PAGE_LINK = re.compile(
    r"^(https://[^/?#]+(?:/[^/?#]+)*/spaces/[^/?#]+/pages/[0-9]+)/[^/?#]+(?=[?#]|\Z)"
)


def without_page_link_titles(value):
    """Drop the title segment that Confluence removes from a sent page link when it saves.

    Apply it to the sent document only, so a stored link that gains or changes a title still fails.
    """

    def change(node):
        attrs = node.get("attrs")
        if node.get("type") == "link" and isinstance(attrs, dict):
            href = attrs.get("href")
            if isinstance(href, str):
                node["attrs"] = {**attrs, "href": PAGE_LINK.sub(r"\1", href)}

    return transform_adf(value, change)


def read_snapshot(path, client, page_id):
    value = read_json(path)
    if not isinstance(value, dict):
        raise TypeError("Baseline must be a get snapshot")
    if value.get("site") != client.site or value.get("id") != page_id:
        raise ValueError(
            "Baseline belongs to a different site or page; get a fresh snapshot"
        )
    if (
        value.get("status") != "current"
        or not isinstance(value.get("title"), str)
        or not value["title"]
        or type(value.get("version")) is not int
        or value["version"] < 1
        or not isinstance(value.get("appearance"), dict)
    ):
        raise ValueError("Invalid baseline metadata; get a fresh snapshot")
    validate_adf(value.get("adf"))
    return value


class Client:
    def __init__(self, site, auth):
        self.site = site
        self.api = site + "/api/v2/"
        self.auth = auth
        self.opener = urllib.request.build_opener(NoRedirect())

    def call(self, path, method="GET", body=None):
        url = urllib.parse.urljoin(self.api, path)
        if not url.startswith(self.api):
            raise ConfluenceError(
                "Refusing a request outside the configured API context"
            )
        request = urllib.request.Request(
            url,
            method=method,
            data=json.dumps(body, ensure_ascii=False).encode()
            if body is not None
            else None,
            headers={
                "Authorization": self.auth,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with self.opener.open(request, timeout=60) as response:
                if method == "PUT":
                    # The subsequent page read is authoritative even if this body is incomplete.
                    return None
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 409:
                message = "HTTP 409: update conflict; inspect the page version and approval requirements"
            else:
                message = f"HTTP {error.code}: {method} failed; check access and API configuration"
                if method == "PUT":
                    message += "; read the page before retrying"
            # Error bodies can contain page data or credentials. Do not echo them.
            error.close()
            raise ConfluenceError(message) from error
        except (
            urllib.error.URLError,
            TimeoutError,
            OSError,
            http.client.HTTPException,
            json.JSONDecodeError,
            UnicodeDecodeError,
        ) as error:
            reason = (
                error
                if isinstance(error, ssl.SSLCertVerificationError)
                else getattr(error, "reason", None)
            )
            if isinstance(reason, ssl.SSLCertVerificationError):
                # OpenSSL's verify message names the cause and holds no page data.
                detail = (getattr(reason, "verify_message", None) or "").rstrip(".")
                detail = detail or "certificate rejected"
                raise ConfluenceError(
                    f"{method} request failed: TLS certificate verification failed "
                    f"({detail}); "
                    "for an unknown issuer, set SSL_CERT_FILE to a CA bundle for this command "
                    "or have the user install CA certificates for this Python (python.org "
                    "builds on macOS: 'Install Certificates.command'); for a host mismatch, "
                    "check CONFLUENCE_URL"
                ) from error
            raise ConfluenceError(
                f"{method} request failed; check connectivity and read the page before retrying"
            ) from error

    def page(self, page_id):
        page = self.call(f"pages/{page_id}?body-format=atlas_doc_format&status=current")
        if str(page["id"]) != page_id or page["status"] != "current":
            raise ConfluenceError("Expected the requested published page")
        adf = page_adf(page)
        appearance = {}
        path = f"pages/{page_id}/properties?limit=100"
        property_url = self.api + f"pages/{page_id}/properties"
        seen = set()
        while path:
            if path in seen:
                raise ConfluenceError(
                    "Repeated property pagination link; snapshot is incomplete"
                )
            seen.add(path)
            properties = self.call(path)
            for prop in properties["results"]:
                if "appearance" in prop["key"]:
                    appearance[prop["key"]] = {
                        "value": prop["value"],
                        "version": prop["version"]["number"],
                    }
            links = properties.get("_links", {})
            if not isinstance(links, dict):
                raise ConfluenceError(
                    "Invalid property pagination metadata; snapshot is incomplete"
                )
            next_link = links.get("next")
            if next_link:
                current_url = urllib.parse.urljoin(self.api, path)
                next_url = urllib.parse.urljoin(current_url, next_link)
                parsed = urllib.parse.urlsplit(next_url)
                expected = urllib.parse.urlsplit(property_url)
                if (
                    (parsed.scheme, parsed.netloc) != (expected.scheme, expected.netloc)
                    or parsed.path
                    not in (expected.path, f"/wiki/api/v2/pages/{page_id}/properties")
                    or parsed.fragment
                ):
                    raise ConfluenceError("Unexpected property pagination target")
                # Gateway requests can receive site-relative /wiki pagination links.
                path = property_url + "?" + parsed.query
            else:
                path = None
        return {
            "site": self.site,
            "id": page_id,
            "title": page["title"],
            "status": page["status"],
            "version": page["version"]["number"],
            "adf": adf,
            "appearance": appearance,
        }

    def check_draft(self, page_id, current):
        draft = self.call(
            f"pages/{page_id}?body-format=atlas_doc_format&get-draft=true"
        )
        if str(draft["id"]) != page_id or draft["status"] not in ("current", "draft"):
            raise ConfluenceError(
                "Could not establish the page's draft state; nothing written"
            )
        if draft["title"] != current["title"]:
            raise ConfluenceError(
                "Unpublished draft has another title; resolve pending edits before publishing"
            )
        changed = differences(
            without_editor_metadata(current["adf"]),
            without_editor_metadata(page_adf(draft)),
        )
        if changed:
            raise ConfluenceError(
                f"Unpublished draft differs at {summarize(changed)}; "
                "resolve pending edits before publishing"
            )


def statistics(value):
    counts = {
        "mention": 0,
        "inlineCard": 0,
        "table": 0,
        "macros": 0,
        "mergedCells": 0,
        "annotation": 0,
    }

    def visit(node):
        if isinstance(node, dict):
            kind = node.get("type")
            if kind in ("mention", "inlineCard", "table", "annotation"):
                counts[kind] += 1
            if kind in (
                "extension",
                "bodiedExtension",
                "inlineExtension",
                "multiBodiedExtension",
            ):
                counts["macros"] += 1
            if kind in ("tableCell", "tableHeader") and any(
                node.get("attrs", {}).get(span, 1) > 1
                for span in ("rowspan", "colspan")
            ):
                counts["mergedCells"] += 1
            # Macro parameters and other attrs are opaque, not an ADF subtree.
            for key in ("content", "marks"):
                visit(node.get(key))
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return counts


def cmd_get(client, args):
    page = client.page(args.page_id)
    with Path(args.out).open("x", encoding="utf-8") as file:
        json.dump(page, file, ensure_ascii=False, indent=2)
        file.write("\n")
    title = json.dumps(page["title"], ensure_ascii=False)
    print(
        f"Saved {args.out}: page {args.page_id} {title} v{page['version']}, "
        f"{len(page['adf']['content'])} top-level nodes"
    )
    print(json.dumps(statistics(page["adf"]), sort_keys=True))


def verify(client, page_id, base, sent):
    now = client.page(page_id)
    expected_version = base["version"] + (canonical(base["adf"]) != canonical(sent))
    changed = differences(sent, now["adf"])
    # Accept the page as sent or with every page-link title dropped. A save that keeps some titles
    # and drops others fails, which errs on the side of reporting.
    # When both fail, report the comparison with fewer differences: it is less likely to list title
    # drops that the other comparison accepts. An empty list means the untitled form matched.
    if changed:
        untitled = differences(without_page_link_titles(sent), now["adf"])
        changed = min(changed, untitled, key=len)
    checks = {
        "stored ADF matches sent ADF": not changed,
        "appearance unchanged": canonical(now["appearance"])
        == canonical(base["appearance"]),
        "title unchanged": now["title"] == base["title"],
        "expected version": now["version"] == expected_version,
    }
    print(f"Page {page_id}: v{base['version']} -> v{now['version']}")
    for label, passed in checks.items():
        print(f"{label}: {passed}")
    if changed:
        print("Stored ADF differs at:", summarize(changed))
    print("Baseline counts:", json.dumps(statistics(base["adf"]), sort_keys=True))
    print("Stored counts:", json.dumps(statistics(now["adf"]), sort_keys=True))
    if not all(checks.values()):
        raise ConfluenceError(
            "Verification failed; retain the baseline and inspect the page"
        )


def cmd_put(client, args):
    base = read_snapshot(args.base, client, args.page_id)
    sent = read_adf(args.new)
    current = client.page(args.page_id)
    if canonical(current) != canonical(base):
        raise ConfluenceError(
            "Page or appearance changed; get a fresh snapshot and rebuild"
        )
    if canonical(sent) == canonical(base["adf"]):
        print(f"ADF unchanged; no write, page {args.page_id} v{base['version']}")
        return
    client.check_draft(args.page_id, current)
    client.call(
        f"pages/{args.page_id}",
        "PUT",
        {
            "id": args.page_id,
            "status": "current",
            "title": current["title"],
            "version": {"number": current["version"] + 1, "message": args.message},
            "body": {
                "value": json.dumps(sent, ensure_ascii=False),
                "representation": "atlas_doc_format",
            },
        },
    )
    print("Write accepted; verifying stored page")
    try:
        verify(client, args.page_id, base, sent)
    except (ConfluenceError, ValueError, KeyError, TypeError) as error:
        raise ConfluenceError(
            f"Write accepted but verification failed: {error}; read the page before retrying"
        ) from error


def cmd_verify(client, args):
    base = read_snapshot(args.base, client, args.page_id)
    verify(client, args.page_id, base, read_adf(args.new))


def page_id(value):
    if not value.isascii() or not value.isdecimal() or int(value) < 1:
        raise argparse.ArgumentTypeError(
            "PAGE_ID must be a positive decimal content ID"
        )
    return str(int(value))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mcp-config", type=Path, help="Read credentials from a local MCP JSON config"
    )
    parser.add_argument(
        "--mcp-server", default="atlassian", help="MCP server key (default: atlassian)"
    )
    commands = parser.add_subparsers(dest="command", required=True)
    get = commands.add_parser("get", help="Save a baseline snapshot to a new file")
    put = commands.add_parser("put", help="Publish an authorized edit and verify it")
    check = commands.add_parser("verify", help="Verify the stored page without writing")
    for command in (get, put, check):
        command.add_argument("page_id", type=page_id)
    get.add_argument("out", type=Path)
    for command in (put, check):
        command.add_argument("base", type=Path)
        command.add_argument("new", type=Path)
    put.add_argument("message")
    args = parser.parse_args(argv)
    try:
        client = load_client(args.mcp_config, args.mcp_server)
        {"get": cmd_get, "put": cmd_put, "verify": cmd_verify}[args.command](
            client, args
        )
    except (ConfluenceError, ValueError, OSError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
