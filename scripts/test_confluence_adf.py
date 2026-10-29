import copy
import importlib.util
import json
import os
import ssl
import sys
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from functools import reduce
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from operator import getitem
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch
from urllib.error import URLError
from urllib.parse import parse_qs, urlsplit

SCRIPT = (
    Path(__file__).resolve().parents[1] / "confluence-adf/scripts/confluence_adf.py"
)
SPEC = importlib.util.spec_from_file_location("confluence_adf", SCRIPT)
adf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adf)

DOCUMENT = {
    "type": "doc",
    "version": 1,
    "content": [
        {
            "type": "paragraph",
            "attrs": {"localId": "paragraph-original"},
            "content": [{"type": "text", "text": "Original section"}],
        },
        {
            "type": "paragraph",
            "content": [
                {"type": "mention", "attrs": {"id": "account-17", "text": "@Reader"}},
                {
                    "type": "text",
                    "text": "Anchored comment",
                    "marks": [
                        {"type": "strong"},
                        {
                            "type": "annotation",
                            "attrs": {
                                "id": "comment-23",
                                "annotationType": "inlineComment",
                            },
                        },
                    ],
                },
                {
                    "type": "inlineCard",
                    "attrs": {"url": "https://example.atlassian.net/browse/EXAMPLE-1"},
                },
            ],
        },
        {
            "type": "extension",
            "attrs": {"extensionKey": "sample-macro", "parameters": {"keep": True}},
        },
        {
            "type": "table",
            "attrs": {"layout": "wide", "width": 760},
            "content": [
                {
                    "type": "tableRow",
                    "content": [
                        {
                            "type": "tableCell",
                            "attrs": {"colspan": 2, "colwidth": [380, 380]},
                            "content": [],
                        }
                    ],
                }
            ],
        },
        {"type": "futureEditorNode", "attrs": {"opaque": [1, {"keep": "unchanged"}]}},
    ],
}


class HelperTests(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.state = SimpleNamespace(
            document=copy.deepcopy(DOCUMENT),
            version=17,
            title="Page title",
            appearance="full-width",
            appearance_version=3,
            draft=None,
            draft_title=None,
            requests=[],
            error=None,
            drift=None,
            next_link=None,
            property_pages=None,
            put_reply="normal",
            put_status=200,
            after_write_error=None,
            conflict_on_put=False,
        )
        state = self.state

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def respond(self, value, status=200, raw=None, truncated=False):
                payload = json.dumps(value).encode() if raw is None else raw
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header(
                    "Content-Length", str(len(payload) + (100 if truncated else 0))
                )
                if status == 302:
                    self.send_header("Location", "/credential-target")
                self.end_headers()
                self.wfile.write(payload)

            def do_GET(self):
                state.requests.append(("GET", self.path, None))
                if state.error:
                    self.respond({"secret": "test-secret-do-not-print"}, state.error)
                    return
                if (
                    state.version > 17
                    and state.after_write_error
                    and state.after_write_error != "null-links"
                ):
                    if state.after_write_error == "malformed":
                        self.respond(None, raw=b'{"secret":"test-secret-do-not-print",')
                    elif state.after_write_error == "truncated":
                        self.respond(
                            {"secret": "test-secret-do-not-print"}, truncated=True
                        )
                    elif state.after_write_error in ("null-body", "null-adf"):
                        self.respond(
                            {
                                "id": "123",
                                "status": "current",
                                "body": None
                                if state.after_write_error == "null-body"
                                else {"atlas_doc_format": None},
                            }
                        )
                    else:
                        self.respond(
                            {"secret": "test-secret-do-not-print"},
                            state.after_write_error,
                        )
                    return
                parsed = urlsplit(self.path)
                query = parse_qs(parsed.query)
                if parsed.path.endswith("/properties"):
                    if state.version > 17 and state.after_write_error == "null-links":
                        self.respond({"results": [], "_links": None})
                        return
                    cursor = query.get("cursor", ["start"])[0]
                    next_link = None
                    if state.property_pages is not None:
                        next_link = state.property_pages.get(cursor)
                    elif cursor == "start":
                        next_link = (
                            state.next_link
                            or "/wiki/api/v2/pages/123/properties?cursor=second"
                        )
                    if next_link:
                        self.respond(
                            {
                                "results": [],
                                "_links": {"next": next_link},
                            }
                        )
                    else:
                        self.respond(
                            {
                                "results": [
                                    {
                                        "key": "content-appearance-published",
                                        "value": state.appearance,
                                        "version": {"number": state.appearance_version},
                                    }
                                ],
                                "_links": {},
                            }
                        )
                    return
                if parsed.path.endswith("/pages/123"):
                    is_draft = (
                        query.get("get-draft") == ["true"] and state.draft is not None
                    )
                    self.respond(
                        {
                            "id": "123",
                            "status": "draft" if is_draft else "current",
                            "title": (
                                (state.draft_title or state.title)
                                if is_draft
                                else state.title
                            ),
                            "version": {"number": state.version},
                            "body": {
                                "atlas_doc_format": {
                                    "value": json.dumps(
                                        state.draft if is_draft else state.document
                                    )
                                }
                            },
                        }
                    )
                    return
                self.respond({}, 404)

            def do_PUT(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                state.requests.append(("PUT", self.path, body))
                if state.conflict_on_put:
                    state.version += 1
                    state.document["content"][0]["content"][0]["text"] = (
                        "Concurrent published edit"
                    )
                if body["version"]["number"] != state.version + 1:
                    self.respond({}, 409)
                    return
                state.version += 1
                state.title = body["title"]
                state.document = json.loads(body["body"]["value"])
                if state.drift == "appearance":
                    state.appearance = "fixed-width"
                    state.appearance_version += 1
                elif state.drift == "body":
                    state.document["content"].pop()
                raw = {"empty": b"", "object": b"{}", "malformed": b"{"}.get(
                    state.put_reply
                )
                self.respond(
                    {"id": "123", "version": {"number": state.version}},
                    state.put_status,
                    raw=raw,
                    truncated=state.put_reply == "truncated",
                )

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.client = adf.Client(
            f"http://127.0.0.1:{self.server.server_port}/wiki", "Basic test-only"
        )
        client_patch = patch.object(adf, "load_client", return_value=self.client)
        self.load_client = client_patch.start()
        self.addCleanup(client_patch.stop)
        self.base = self.root / "base.json"
        self.new = self.root / "new.json"
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        self.state.requests.clear()
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["content"][0]["text"] = "Requested change"
        self.new.write_text(json.dumps(sent), encoding="utf-8")

    def run_command(self, *args):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = adf.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def put(self):
        return self.run_command(
            "put", "123", str(self.base), str(self.new), "Update section"
        )

    def writes(self):
        return [request for request in self.state.requests if request[0] == "PUT"]

    def test_publishes_native_adf_and_keeps_unrelated_rich_content(self):
        baseline = json.loads(self.base.read_text())
        self.assertEqual(
            baseline["appearance"],
            {"content-appearance-published": {"value": "full-width", "version": 3}},
        )
        code, output, error = self.put()
        self.assertEqual((code, error), (0, ""))
        self.assertIn("v17 -> v18", output)
        method, path, request = self.writes()[0]
        self.assertEqual((method, path), ("PUT", "/wiki/api/v2/pages/123"))
        self.assertEqual(request["body"]["representation"], "atlas_doc_format")
        self.assertEqual(
            request["version"], {"number": 18, "message": "Update section"}
        )
        self.assertEqual(
            (request["id"], request["title"], request["status"]),
            ("123", "Page title", "current"),
        )
        self.assertEqual(set(request), {"id", "title", "status", "body", "version"})
        self.assertEqual(
            self.state.document["content"][0]["content"][0]["text"], "Requested change"
        )
        self.assertEqual(self.state.document["content"][1:], DOCUMENT["content"][1:])
        self.assertEqual(self.state.appearance, "full-width")

    def test_rejects_published_metadata_body_and_appearance_drift_without_writing(self):
        for field, replacement in (
            ("version", 18),
            ("title", "Changed title"),
            ("appearance", "fixed-width"),
            ("appearance_version", 4),
            ("document", {"type": "doc", "version": 1, "content": []}),
        ):
            original = getattr(self.state, field)
            with self.subTest(field=field):
                setattr(self.state, field, replacement)
                self.assertEqual(self.put()[0], 1)
                self.assertEqual(self.writes(), [])
                setattr(self.state, field, original)

    def test_rejects_wrong_page_and_site_baselines_without_requests(self):
        baseline = json.loads(self.base.read_text())
        for field, replacement in (
            ("id", "456"),
            ("site", "https://another.atlassian.net/wiki"),
        ):
            with self.subTest(field=field):
                self.base.write_text(
                    json.dumps({**baseline, field: replacement}), encoding="utf-8"
                )
                self.assertEqual(self.put()[0], 1)
                self.assertEqual(self.state.requests, [])

    def test_rejects_divergent_draft_without_writing(self):
        self.state.draft = copy.deepcopy(DOCUMENT)
        self.state.draft["content"][0]["content"][0]["text"] = (
            "A collaborator's pending change"
        )
        code, _, error = self.put()
        self.assertEqual(code, 1)
        self.assertIn("Unpublished draft differs at /content/0/content/0/text", error)
        self.assertNotIn("A collaborator's pending change", error)
        self.assertEqual(self.writes(), [])

    def test_rejects_draft_with_another_title_without_printing_it(self):
        self.state.draft = copy.deepcopy(DOCUMENT)
        self.state.draft_title = "Pending collaborator title"
        code, output, error = self.put()
        self.assertEqual(code, 1)
        self.assertIn("Unpublished draft has another title", error)
        self.assertNotIn("Pending collaborator title", output + error)
        self.assertEqual(self.writes(), [])

    def test_publishes_over_a_draft_that_holds_only_editor_metadata(self):
        link = {
            "type": "link",
            "attrs": {"href": "https://example.atlassian.net/wiki/x/1"},
        }
        self.state.document["content"][1]["content"].append(
            {"type": "text", "text": "Linked page", "marks": [link]}
        )
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        sent = copy.deepcopy(self.state.document)
        sent["content"][0]["content"][0]["text"] = "Requested change"
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.state.draft = copy.deepcopy(self.state.document)
        draft_content = self.state.draft["content"]
        # The published macro has no macroParams; the editor adds one holding only the parent ID.
        draft_content[2]["attrs"]["parameters"]["macroParams"] = {
            "_parentId": {"value": "456"}
        }
        draft_content[1]["content"][3]["marks"][0]["attrs"]["__confluenceMetadata"] = {
            "linkType": "page",
            "contentTitle": "Cached title",
        }
        code, _, error = self.put()
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(len(self.writes()), 1)
        self.assertEqual(self.state.document, sent)

    def test_draft_check_treats_an_empty_macro_params_as_absent(self):
        self.state.document["content"][2]["attrs"]["parameters"]["macroParams"] = {}
        current = self.client.page("123")
        self.state.draft = copy.deepcopy(self.state.document)
        del self.state.draft["content"][2]["attrs"]["parameters"]["macroParams"]
        self.client.check_draft("123", current)

    def test_draft_check_accepts_macro_ids_the_editor_adds(self):
        # The published macro has empty parameters, none at all, or parameters of its own.
        own = {"macroParams": {"name": {"value": "Excerpt"}}}
        for published in ({}, None, own):
            for name in ("_parentId", "_referencedContentId"):
                with self.subTest(published=published, name=name):
                    attrs = self.state.document["content"][2]["attrs"]
                    if published is None:
                        attrs.pop("parameters", None)
                    else:
                        attrs["parameters"] = copy.deepcopy(published)
                    current = self.client.page("123")
                    self.state.draft = copy.deepcopy(self.state.document)
                    self.state.draft["content"][2]["attrs"]["parameters"] = {
                        "macroParams": {
                            **(published or {}).get("macroParams", {}),
                            name: {"value": "456"},
                        }
                    }
                    self.client.check_draft("123", current)

    def test_draft_check_ignores_cached_titles_on_cards(self):
        original = copy.deepcopy(self.state.document)
        for card_type in ("inlineCard", "blockCard", "embedCard"):
            with self.subTest(card_type=card_type):
                self.state.document = copy.deepcopy(original)
                card = {
                    "type": card_type,
                    "attrs": {"url": "https://example.atlassian.net/x/1"},
                }
                # An inline card goes into the paragraph, a block card into the document.
                path = (
                    ["content", 1, "content"]
                    if card_type == "inlineCard"
                    else ["content"]
                )
                parent = reduce(getitem, path, self.state.document)
                parent.append(card)
                path.append(len(parent) - 1)
                current = self.client.page("123")
                self.state.draft = copy.deepcopy(self.state.document)
                node = reduce(getitem, path, self.state.draft)
                node["attrs"]["__confluenceMetadata"] = {
                    "linkType": "page",
                    "contentTitle": "Cached title",
                }
                self.client.check_draft("123", current)
                # A changed card target is still a pending edit.
                node["attrs"]["url"] = "https://example.atlassian.net/x/2"
                pointer = "/" + "/".join(map(str, path)) + "/attrs/url"
                with self.assertRaises(adf.ConfluenceError) as raised:
                    self.client.check_draft("123", current)
                self.assertEqual(
                    str(raised.exception),
                    f"Unpublished draft differs at {pointer}; "
                    "resolve pending edits before publishing",
                )

    def test_draft_check_ignores_editor_metadata_on_the_published_side_too(self):
        link = {
            "type": "link",
            "attrs": {
                "href": "https://example.atlassian.net/x/1",
                "__confluenceMetadata": {},
            },
        }
        self.state.document["content"][1]["content"].append(
            {"type": "text", "text": "Linked page", "marks": [link]}
        )
        self.state.document["content"][2]["attrs"]["parameters"]["macroParams"] = {
            "_parentId": {"value": "1"}
        }
        current = self.client.page("123")
        self.state.draft = copy.deepcopy(self.state.document)
        del self.state.draft["content"][2]["attrs"]["parameters"]["macroParams"]
        del self.state.draft["content"][1]["content"][3]["marks"][0]["attrs"][
            "__confluenceMetadata"
        ]
        self.client.check_draft("123", current)

    def test_draft_check_ignores_editor_metadata_only_where_the_editor_adds_it(self):
        self.state.document["content"][2]["attrs"]["parameters"]["macroParams"] = {
            "style": {"value": "published"}
        }
        current = self.client.page("123")
        # The editor adds a parent ID next to existing macro parameters.
        self.state.draft = copy.deepcopy(self.state.document)
        self.state.draft["content"][2]["attrs"]["parameters"]["macroParams"][
            "_parentId"
        ] = {"value": "456"}
        self.client.check_draft("123", current)
        # Cached link metadata on a mark that is not a link is a real difference.
        self.state.draft = copy.deepcopy(self.state.document)
        annotation = self.state.draft["content"][1]["content"][1]["marks"][1]
        annotation["attrs"]["__confluenceMetadata"] = {"linkType": "page"}
        with self.assertRaisesRegex(adf.ConfluenceError, "/content/1/content/1/marks"):
            self.client.check_draft("123", current)
        # A parent ID outside macroParams is not where the editor puts it.
        self.state.draft = copy.deepcopy(self.state.document)
        self.state.draft["content"][2]["attrs"]["parameters"]["_parentId"] = "456"
        with self.assertRaisesRegex(adf.ConfluenceError, "/content/2/attrs/parameters"):
            self.client.check_draft("123", current)

    def test_link_metadata_does_not_hide_a_changed_link_target_in_the_draft(self):
        link = {"type": "link", "attrs": {"href": "https://example.atlassian.net/x/1"}}
        self.state.document["content"][1]["content"].append(
            {"type": "text", "text": "Linked page", "marks": [link]}
        )
        current = self.client.page("123")
        self.state.draft = copy.deepcopy(self.state.document)
        attrs = self.state.draft["content"][1]["content"][3]["marks"][0]["attrs"]
        attrs.update(
            {"href": "https://example.atlassian.net/x/2", "__confluenceMetadata": {}}
        )
        with self.assertRaisesRegex(
            adf.ConfluenceError, "/content/1/content/3/marks/0/attrs/href"
        ):
            self.client.check_draft("123", current)

    @unittest.skipIf(
        sys.version_info < (3, 12),
        "before 3.12, json.dumps in canonical() hits the Python recursion limit first",
    )
    def test_differences_survive_nesting_deeper_than_the_recursion_limit(self):
        def build(leaf):
            nested = [leaf]
            for _ in range(3000):
                nested = [nested]
            return {
                "type": "doc",
                "version": 1,
                "content": [{"attrs": {"blob": nested}}],
            }

        self.assertEqual(adf.differences(build(0), build(0)), [])
        self.assertEqual(
            adf.differences(build(0), build(1)),
            ["(nesting too deep to locate the rest)"],
        )

    def test_editor_metadata_does_not_hide_a_pending_edit_in_the_same_draft(self):
        self.state.document["content"][2]["attrs"]["parameters"]["macroParams"] = {
            "style": {"value": "published"}
        }
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        self.state.draft = copy.deepcopy(self.state.document)
        self.state.draft["content"][2]["attrs"]["parameters"]["macroParams"] = {
            "_parentId": {"value": "456"},
            "pending-collaborator-key": {"value": "pending-collaborator-value"},
            "style": {"value": "published"},
        }
        code, output, error = self.put()
        self.assertEqual(code, 1)
        self.assertIn(
            "Unpublished draft differs at /content/2/attrs/parameters;", error
        )
        # Paths stop at macro parameters: their keys and values can be page data.
        self.assertNotIn("pending-collaborator", output + error)
        self.assertEqual(self.writes(), [])

    def test_verify_accepts_page_links_stored_without_their_title_segment(self):
        page = "https://example.atlassian.net/wiki/spaces/KEY/pages/2878439433"
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["content"].append(
            {
                "type": "text",
                "text": "Page link",
                "marks": [
                    {"type": "link", "attrs": {"href": page + "/Page+title#top"}}
                ],
            }
        )
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        stored = self.state.document["content"][0]["content"][1]["marks"][0]["attrs"]
        command = ("verify", "123", str(self.base), str(self.new))
        sent_mark = sent["content"][0]["content"][1]["marks"][0]["attrs"]
        for sent_href, stored_href in (
            (page + "/Page+title#top", page + "#top"),
            (page + "/Page+title?focusedCommentId=1", page + "?focusedCommentId=1"),
            (
                "https://api.atlassian.com/ex/confluence/cloud-id/wiki/spaces/KEY/pages/9/T",
                "https://api.atlassian.com/ex/confluence/cloud-id/wiki/spaces/KEY/pages/9",
            ),
            # A custom domain may serve the space path at the root.
            (
                "https://docs.example.com/spaces/KEY/pages/9/T",
                "https://docs.example.com/spaces/KEY/pages/9",
            ),
        ):
            with self.subTest(accepted=stored_href):
                sent_mark["href"] = sent_href
                self.new.write_text(json.dumps(sent), encoding="utf-8")
                stored["href"] = stored_href
                code, output, _ = self.run_command(*command)
                self.assertEqual(code, 0)
                self.assertNotIn("Stored ADF differs", output)
        for sent_href, stored_href in (
            (page + "/Page+title#top", page.replace("2878439433", "2878439434")),
            # Only the final segment is a title, so a deeper path keeps its middle.
            (page + "/Page+title/attachments/9", page + "/attachments/9"),
            (page + "/Page+title/attachments/9", page),
            (
                page.replace("/spaces/KEY/", "/spaces/A/B/") + "/Page+title",
                page.replace("/spaces/KEY/", "/spaces/A/B/"),
            ),
            (page + "/Page+title?focusedCommentId=1", page + "?focusedCommentId=2"),
            (page + "/Page+title", page + "/Another+title"),
            (page, page + "/Page+title"),
            (page, page + "/"),
            # Only absolute lowercase https URLs with a space key match.
            (
                "/wiki/spaces/KEY/pages/2878439433/Page+title",
                "/wiki/spaces/KEY/pages/2878439433",
            ),
            (
                page.replace("https://", "HTTPS://") + "/Page+title",
                page.replace("https://", "HTTPS://"),
            ),
            (
                page.replace("/spaces/KEY/", "/spaces//") + "/Page+title",
                page.replace("/spaces/KEY/", "/spaces//"),
            ),
            (page + "/", page),
            (
                page.replace("https://", "http://") + "/Page+title",
                page.replace("https://", "http://"),
            ),
            # A page URL that is not the whole href, a non-numeric ID and another path shape.
            (
                "https://example.net/r?next=" + page + "/Page+title",
                "https://example.net/r?next=" + page,
            ),
            (
                page.replace("2878439433", "١٢") + "/Page+title",
                page.replace("2878439433", "١٢"),
            ),
            (
                page.replace("2878439433", "abc") + "/Page+title",
                page.replace("2878439433", "abc"),
            ),
            (
                page.replace("/spaces/", "/x/") + "/Page+title",
                page.replace("/spaces/", "/x/"),
            ),
        ):
            with self.subTest(rejected=stored_href):
                sent_mark["href"] = sent_href
                self.new.write_text(json.dumps(sent), encoding="utf-8")
                stored["href"] = stored_href
                code, output, _ = self.run_command(*command)
                self.assertEqual(code, 1)
                self.assertIn(
                    "Stored ADF differs at: /content/0/content/1/marks/0/attrs/href",
                    output,
                )

    def test_differences_never_report_equal_when_the_serialized_texts_differ(self):
        left = {"type": "doc", "version": 1, "content": [{"attrs": {"n": 1}}]}
        right = {"type": "doc", "version": 1, "content": [{"attrs": {"n": 2}}]}
        # Simulate a walk that misses the difference the serialized comparison found.
        with patch.object(adf.json, "loads", return_value={}):
            self.assertEqual(adf.differences(left, right), ["(location unknown)"])

    def test_differences_report_only_values_that_differ(self):
        left = {
            "type": "doc",
            "version": 1,
            "content": [{"attrs": {"same": None, "changed": 1}}],
        }
        right = copy.deepcopy(left)
        right["content"][0]["attrs"]["changed"] = 2
        self.assertEqual(adf.differences(left, right), ["/content/0/attrs/changed"])

    def test_normalizations_leave_their_input_unchanged(self):
        document = copy.deepcopy(DOCUMENT)
        document["content"][1]["content"].append(
            {
                "type": "text",
                "text": "Link",
                "marks": [
                    {
                        "type": "link",
                        "attrs": {
                            "href": "https://e.atlassian.net/wiki/spaces/K/pages/1/T",
                            "__confluenceMetadata": {},
                        },
                    }
                ],
            }
        )
        document["content"][2]["attrs"]["parameters"]["macroParams"] = {
            "_parentId": {"value": "1"}
        }
        original = copy.deepcopy(document)
        adf.without_editor_metadata(document)
        adf.without_page_link_titles(document)
        self.assertEqual(document, original)

    def test_verify_distinguishes_an_added_null_attribute_from_an_absent_one(self):
        self.assertEqual(self.put()[0], 0)
        self.state.document["content"][0]["attrs"]["addedByEditor"] = None
        code, output, _ = self.run_command(
            "verify", "123", str(self.base), str(self.new)
        )
        self.assertEqual(code, 1)
        self.assertIn("Stored ADF differs at: /content/0/attrs/addedByEditor", output)

    def test_verify_keeps_json_types_of_ordinary_attributes_distinct(self):
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["attrs"].update({"flag": True, "count": 1, "offset": 0.0})
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        attrs = self.state.document["content"][0]["attrs"]
        command = ("verify", "123", str(self.base), str(self.new))
        for key, stored in (("flag", 1), ("count", 1.0), ("offset", -0.0)):
            with self.subTest(key=key):
                original = attrs[key]
                attrs[key] = stored
                try:
                    code, output, _ = self.run_command(*command)
                    self.assertEqual(code, 1)
                    self.assertIn(
                        f"Stored ADF differs at: /content/0/attrs/{key}", output
                    )
                finally:
                    attrs[key] = original

    def test_difference_paths_escape_keys_that_could_forge_a_path_or_line(self):
        left = {"type": "doc", "version": 1, "content": [{"attrs": {"a/b~c\nd": 1}}]}
        right = {"type": "doc", "version": 1, "content": [{"attrs": {"a/b~c\nd": 2}}]}
        self.assertEqual(adf.differences(left, right), ["/content/0/attrs/a~1b~0c\\nd"])
        # A Unicode line separator would also start a new line in a terminal.
        left["content"][0]["attrs"] = {"k ": 1}
        right["content"][0]["attrs"] = {"k ": 2}
        self.assertEqual(adf.differences(left, right), ["/content/0/attrs/k\\u2028"])

    def test_difference_paths_stop_at_list_shaped_macro_parameters(self):
        left = {
            "type": "doc",
            "version": 1,
            "content": [{"attrs": {"parameters": [{"secret-key": 1}]}}],
        }
        right = copy.deepcopy(left)
        right["content"][0]["attrs"]["parameters"][0]["secret-key"] = 2
        self.assertEqual(adf.differences(left, right), ["/content/0/attrs/parameters"])

    def test_difference_paths_follow_sorted_keys(self):
        # Eight keys make an accidentally sorted set order unlikely.
        keys = "hgfedcba"
        left = {
            "type": "doc",
            "version": 1,
            "content": [{"attrs": dict.fromkeys(keys, 1)}],
        }
        right = {
            "type": "doc",
            "version": 1,
            "content": [{"attrs": dict.fromkeys(keys, 2)}],
        }
        self.assertEqual(
            adf.differences(left, right),
            [f"/content/0/attrs/{key}" for key in "abcdefgh"],
        )

    def test_verify_drops_titles_only_from_link_marks(self):
        page = "https://example.atlassian.net/wiki/spaces/KEY/pages/1"
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["content"][0]["marks"] = [
            {"type": "customMark", "attrs": {"href": page + "/Title"}}
        ]
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        self.state.document["content"][0]["content"][0]["marks"][0]["attrs"]["href"] = (
            page
        )
        code, _, _ = self.run_command("verify", "123", str(self.base), str(self.new))
        self.assertEqual(code, 1)

    def test_difference_report_is_capped_and_names_length_changes(self):
        left = {"type": "doc", "version": 1, "content": [{"n": 1} for _ in range(7)]}
        right = copy.deepcopy(left)
        for node in right["content"][1:]:
            node["n"] = 2
        paths = adf.differences(left, right)
        self.assertEqual(paths, [f"/content/{index}/n" for index in range(1, 7)])
        self.assertEqual(
            adf.summarize(paths),
            "/content/1/n, /content/2/n, /content/3/n, /content/4/n, /content/5/n, ...",
        )
        self.assertEqual(
            adf.summarize(paths[:5]),
            "/content/1/n, /content/2/n, /content/3/n, /content/4/n, /content/5/n",
        )
        self.assertEqual(
            adf.differences(left, {**left, "content": left["content"][:6]}),
            ["/content (length 7 -> 6)"],
        )

    def test_verify_reports_the_comparison_with_fewer_differences_past_the_cap(self):
        page = "https://example.atlassian.net/wiki/spaces/KEY/pages/1"
        sent = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Link",
                            "marks": [{"type": "link", "attrs": {"href": page + "/T"}}],
                        }
                    ],
                }
            ]
            + [
                {"type": "paragraph", "content": [{"type": "text", "text": "Text"}]}
                for _ in range(6)
            ],
        }
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        stored = self.state.document["content"]
        stored[0]["content"][0]["marks"][0]["attrs"]["href"] = page
        for paragraph in stored[1:]:
            paragraph["content"][0]["text"] = "Changed"
        code, output, _ = self.run_command(
            "verify", "123", str(self.base), str(self.new)
        )
        self.assertEqual(code, 1)
        self.assertNotIn("attrs/href", output)
        self.assertIn("/content/1/content/0/text", output)

    def test_verify_reports_the_as_sent_comparison_when_titles_were_kept(self):
        page = "https://example.atlassian.net/wiki/spaces/KEY/pages/"
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["content"] += [
            {
                "type": "text",
                "text": f"Link {number}",
                "marks": [{"type": "link", "attrs": {"href": f"{page}{number}/Title"}}],
            }
            for number in range(6)
        ]
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        self.state.document["content"][0]["content"][0]["text"] = "Changed"
        code, output, _ = self.run_command(
            "verify", "123", str(self.base), str(self.new)
        )
        self.assertEqual(code, 1)
        self.assertIn("Stored ADF differs at: /content/0/content/0/text\n", output)

    def test_verify_rejects_a_save_that_drops_only_some_page_link_titles(self):
        page = "https://example.atlassian.net/wiki/spaces/KEY/pages/"
        sent = copy.deepcopy(DOCUMENT)
        sent["content"][0]["content"] += [
            {
                "type": "text",
                "text": f"Link {number}",
                "marks": [{"type": "link", "attrs": {"href": f"{page}{number}/Title"}}],
            }
            for number in (1, 2)
        ]
        self.new.write_text(json.dumps(sent), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        self.state.document["content"][0]["content"][1]["marks"][0]["attrs"]["href"] = (
            page + "1"
        )
        command = ("verify", "123", str(self.base), str(self.new))
        self.assertEqual(self.run_command(*command)[0], 1)

    def test_does_not_publish_when_adf_is_unchanged_or_only_marks_are_reordered(self):
        document = copy.deepcopy(DOCUMENT)
        document["content"][1]["content"][1]["marks"].reverse()
        self.new.write_text(json.dumps(document), encoding="utf-8")
        code, output, _ = self.put()
        self.assertEqual(code, 0)
        self.assertIn("no write", output)
        self.assertEqual(self.writes(), [])

    def test_failed_post_write_checks_return_nonzero_and_do_not_repair_or_retry(self):
        for drift in ("body", "appearance"):
            with self.subTest(drift=drift):
                self.state.document = copy.deepcopy(DOCUMENT)
                self.state.version = 17
                self.state.appearance = "full-width"
                self.state.appearance_version = 3
                self.state.requests.clear()
                self.state.drift = drift
                code, _, error = self.put()
                self.assertEqual(code, 1)
                self.assertIn("Verification failed", error)
                self.assertEqual(len(self.writes()), 1)

    def test_verify_ignores_mark_order_but_detects_node_removal_and_extra_versions(
        self,
    ):
        self.assertEqual(self.put()[0], 0)
        self.state.document["content"][1]["content"][1]["marks"].reverse()
        command = ("verify", "123", str(self.base), str(self.new))
        self.assertEqual(self.run_command(*command)[0], 0)
        self.state.version += 1
        self.assertEqual(self.run_command(*command)[0], 1)
        self.state.version -= 1
        self.state.document["content"].pop()
        self.assertEqual(self.run_command(*command)[0], 1)

    def test_get_cannot_overwrite_baseline(self):
        original = self.base.read_bytes()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 1)
        self.assertEqual(self.base.read_bytes(), original)

    def test_verify_detects_opaque_parameter_order_and_json_type_changes(self):
        self.state.document["content"][2]["attrs"]["parameters"]["marks"] = [
            "alpha",
            "beta",
        ]
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        document = copy.deepcopy(self.state.document)
        document["content"][0]["content"][0]["text"] = "Requested change"
        self.new.write_text(json.dumps(document), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        parameters = self.state.document["content"][2]["attrs"]["parameters"]
        parameters["marks"].reverse()
        command = ("verify", "123", str(self.base), str(self.new))
        self.assertEqual(self.run_command(*command)[0], 1)
        parameters["marks"].reverse()
        parameters["keep"] = 1
        self.assertEqual(self.run_command(*command)[0], 1)

    def test_opaque_macro_mark_parameter_change_is_published(self):
        self.state.document["content"][2]["attrs"]["parameters"]["marks"] = [
            "alpha",
            "beta",
        ]
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        document = copy.deepcopy(self.state.document)
        document["content"][2]["attrs"]["parameters"]["marks"].reverse()
        self.new.write_text(json.dumps(document), encoding="utf-8")
        self.assertEqual(self.put()[0], 0)
        self.assertEqual(len(self.writes()), 1)
        self.assertEqual(
            self.state.document["content"][2]["attrs"]["parameters"]["marks"],
            ["beta", "alpha"],
        )

    def test_diagnostics_do_not_interpret_opaque_macro_parameters_as_adf(self):
        self.state.document["content"][2]["attrs"]["parameters"]["opaqueData"] = [
            {"type": "tableCell", "attrs": None},
            {"type": "tableCell", "attrs": {"colspan": "opaque-value"}},
            {"type": "mention", "attrs": {"id": "opaque-account"}},
        ]
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        document = copy.deepcopy(self.state.document)
        document["content"][0]["content"][0]["text"] = "Requested change"
        self.new.write_text(json.dumps(document), encoding="utf-8")
        code, _, error = self.put()
        self.assertEqual((code, error), (0, ""))
        self.assertEqual(self.state.document["content"][1:], document["content"][1:])
        self.assertEqual(
            adf.statistics(self.state.document),
            {
                "mention": 1,
                "inlineCard": 1,
                "table": 1,
                "macros": 1,
                "mergedCells": 1,
                "annotation": 1,
            },
        )

    def test_rejects_non_adf_input_before_requests(self):
        for value in (
            [],
            {"type": "doc", "version": True, "content": []},
            {"storage": {"value": "<p>Converted content</p>"}},
        ):
            with self.subTest(value=value):
                self.new.write_text(json.dumps(value), encoding="utf-8")
                self.assertEqual(self.put()[0], 1)
                self.assertEqual(self.state.requests, [])

    def test_errors_and_redirects_do_not_echo_response_secrets_or_follow_redirects(
        self,
    ):
        for status in (401, 409, 302):
            with self.subTest(status=status):
                self.state.requests.clear()
                self.state.error = status
                code, output, error = self.put()
                self.assertEqual(code, 1)
                self.assertNotIn("test-secret-do-not-print", output + error)
                self.assertEqual(len(self.state.requests), 1)
                self.assertEqual(self.writes(), [])

    def test_certificate_failure_names_the_trust_store_fix(self):
        certificate = ssl.SSLCertVerificationError("certificate verify failed")
        # OpenSSL can end the message with a period; the report drops it before ")".
        certificate.verify_message = "unable to get local issuer certificate."
        for failure in (URLError(certificate), certificate):
            with (
                self.subTest(failure=type(failure).__name__),
                patch.object(self.client.opener, "open", side_effect=failure),
            ):
                code, _, error = self.put()
                self.assertEqual(code, 1)
                self.assertIn(
                    "TLS certificate verification failed "
                    "(unable to get local issuer certificate)",
                    error,
                )
                # The per-command fix comes before the global one left to the user.
                self.assertLess(
                    error.index("SSL_CERT_FILE"), error.index("Install Certificates")
                )
        without_reason = ssl.SSLCertVerificationError("certificate verify failed")
        with patch.object(
            self.client.opener, "open", side_effect=URLError(without_reason)
        ):
            code, _, error = self.put()
        self.assertEqual(code, 1)
        self.assertIn("verification failed (certificate rejected)", error)
        for failure in (
            URLError(ConnectionRefusedError("connection refused")),
            ssl.SSLError("wrong version number"),
            URLError(ssl.SSLError("wrong version number")),
        ):
            with (
                self.subTest(failure=type(failure).__name__),
                patch.object(self.client.opener, "open", side_effect=failure),
            ):
                code, _, error = self.put()
                self.assertEqual(code, 1)
                self.assertIn("check connectivity", error)
                self.assertNotIn("TLS", error)

    def test_rejects_foreign_property_pagination_without_following_it(self):
        self.state.next_link = (
            "https://foreign.example/wiki/api/v2/pages/123/properties?cursor=second"
        )
        code, _, error = self.put()
        self.assertEqual(code, 1)
        self.assertIn("Unexpected property pagination target", error)
        self.assertEqual(len(self.state.requests), 2)

    def test_verify_distinguishes_appearance_json_types(self):
        self.state.appearance = {"flags": [True, False]}
        self.base.unlink()
        self.assertEqual(self.run_command("get", "123", str(self.base))[0], 0)
        self.assertEqual(self.put()[0], 0)
        self.state.appearance = {"flags": [1, 0]}
        code, output, _ = self.run_command(
            "verify", "123", str(self.base), str(self.new)
        )
        self.assertEqual(code, 1)
        self.assertIn("appearance unchanged: False", output)

    def test_verifies_successful_write_even_with_unusable_response_body(self):
        for reply in ("empty", "object", "malformed", "truncated"):
            with self.subTest(reply=reply):
                self.state.document = copy.deepcopy(DOCUMENT)
                self.state.version = 17
                self.state.requests.clear()
                self.state.put_reply = reply
                code, output, error = self.put()
                self.assertEqual((code, error), (0, ""))
                self.assertIn("v17 -> v18", output)
                self.assertEqual(len(self.writes()), 1)
                self.assertEqual(
                    self.state.document["content"][0]["content"][0]["text"],
                    "Requested change",
                )
                self.assertEqual(
                    self.state.requests[-2][0:2],
                    ("GET", "/wiki/api/v2/pages/123/properties?limit=100"),
                )

    def test_failed_read_after_write_is_reported_without_secrets_or_another_write(self):
        for failure in (
            502,
            "malformed",
            "truncated",
            "null-body",
            "null-adf",
            "null-links",
        ):
            with self.subTest(failure=failure):
                self.state.document = copy.deepcopy(DOCUMENT)
                self.state.version = 17
                self.state.requests.clear()
                self.state.after_write_error = failure
                code, output, error = self.put()
                self.assertEqual(code, 1)
                self.assertEqual(self.state.version, 18)
                self.assertEqual(len(self.writes()), 1)
                self.assertIn("read the page before retrying", error)
                self.assertNotIn("test-secret-do-not-print", output + error)

    def test_applied_write_with_http_error_is_not_retried(self):
        self.state.put_status = 500
        code, _, error = self.put()
        self.assertEqual(code, 1)
        self.assertEqual(self.state.version, 18)
        self.assertEqual(len(self.writes()), 1)
        self.assertIn("read the page before retrying", error)

    def test_racing_published_edit_is_not_overwritten_or_retried(self):
        self.state.conflict_on_put = True
        code, _, error = self.put()
        self.assertEqual(code, 1)
        self.assertEqual(len(self.writes()), 1)
        self.assertIn("HTTP 409", error)
        self.assertEqual(
            self.state.document["content"][0]["content"][0]["text"],
            "Concurrent published edit",
        )

    def test_follows_query_relative_property_links_beyond_two_pages(self):
        self.state.property_pages = {
            "start": "?cursor=second",
            "second": "?cursor=third",
        }
        path = self.root / "paginated.json"
        self.assertEqual(self.run_command("get", "123", str(path))[0], 0)
        snapshot = json.loads(path.read_text())
        self.assertEqual(
            snapshot["appearance"],
            {"content-appearance-published": {"value": "full-width", "version": 3}},
        )
        self.assertEqual(
            self.state.requests[-1][1], "/wiki/api/v2/pages/123/properties?cursor=third"
        )

    def test_scoped_gateway_keeps_context_when_following_site_relative_properties(self):
        self.client = adf.Client(
            f"http://127.0.0.1:{self.server.server_port}/ex/confluence/cloud-id/wiki",
            "Basic test-only",
        )
        self.load_client.return_value = self.client
        path = self.root / "gateway.json"
        self.assertEqual(self.run_command("get", "123", str(path))[0], 0)
        self.assertEqual(
            self.state.requests[-1][1],
            "/ex/confluence/cloud-id/wiki/api/v2/pages/123/properties?cursor=second",
        )


class ConfigurationTests(unittest.TestCase):
    def test_environment_credentials_and_url_normalization(self):
        values = {
            "CONFLUENCE_URL": "https://example.atlassian.net/",
            "CONFLUENCE_USERNAME": "reader@example.com",
            "CONFLUENCE_API_TOKEN": "test-token",
        }
        with patch.dict(os.environ, values, clear=True):
            client = adf.load_client()
        self.assertEqual(client.site, "https://example.atlassian.net/wiki")
        self.assertEqual(client.auth, "Basic cmVhZGVyQGV4YW1wbGUuY29tOnRlc3QtdG9rZW4=")
        self.assertEqual(
            adf.normalize_site(
                "https://api.atlassian.com/ex/confluence/cloud-id/wiki/"
            ),
            "https://api.atlassian.com/ex/confluence/cloud-id/wiki",
        )

    def test_config_is_explicit_and_partial_environment_does_not_mix_credentials(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(
                json.dumps(
                    {
                        "mcpServers": {
                            "custom": {
                                "env": {
                                    "CONFLUENCE_URL": "https://example.atlassian.net/wiki",
                                    "CONFLUENCE_USERNAME": "reader@example.com",
                                    "CONFLUENCE_API_TOKEN": "test-token",
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(
                    adf.load_client(path, "custom").site,
                    "https://example.atlassian.net/wiki",
                )
                with self.assertRaises(ValueError):
                    adf.load_client()
            with (
                patch.dict(
                    os.environ,
                    {"CONFLUENCE_URL": "https://different.atlassian.net/wiki"},
                    clear=True,
                ),
                self.assertRaises(ValueError),
            ):
                adf.load_client(path, "custom")

    def test_rejects_unsafe_context_urls(self):
        for value in (
            "http://example.atlassian.net/wiki",
            "https://user:secret@example.atlassian.net/wiki",
            "https://example.atlassian.net/wiki?token=secret",
            "https://example.atlassian.net/wiki#fragment",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                adf.normalize_site(value)

    def test_help_needs_no_credentials(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            redirect_stdout(StringIO()),
            self.assertRaises(SystemExit) as result,
        ):
            adf.main(["--help"])
        self.assertEqual(result.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
