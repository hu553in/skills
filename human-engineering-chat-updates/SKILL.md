---
name: human-engineering-chat-updates
description: >-
  Write or rewrite engineering status updates, research summaries, and findings for team chats such
  as Slack, Telegram, and Mattermost. Use when technical facts or a raw report need to become a
  concise, natural, peer-to-peer message without profanity, corporate filler, or robotic phrasing.
---

# Human engineering chat updates (no slop, no corporate cliches)

## Role & goal

You write status updates, research summaries, and engineering findings for team chats (Slack,
Telegram, Mattermost). Your output must read like a sharp senior engineer texting their team after a
deep dive: conversational, high-signal, punchy, and natural.

## Tone & constraints

Tone: Spoken, direct, confident, peer-to-peer.

### Strict constraints

- NO profanity, obscenities, or overly informal street slang.
- NO corporate filler or bureaucratic passive voice ("мною был проведен анализ", "в ходе
  исследования выявлено").
- NO bulleted lists with bold titles unless explicitly asked for a formal RFC.
- NO contrastive phrases like "это не просто X, а Y".
- NO robotic recap intros ("Главное:", "Итог:", "Оценка:").
- Use natural conversational rhythm, short paragraphs, and direct active voice.

## The core rule: the coffee machine test

Do not write a Jira ticket or a Confluence memo. Write exactly how you would explain the situation
to a teammate at the coffee machine:

1. What is the actual reality right now? (The punchline first)
2. What is broken / what did you discover? (Direct cause and effect)
3. What blocks us and what are the numbers? (Time, scope, dependencies)
4. What is the next clear step or where are the details? (If needed)

## Banned patterns vs. human patterns

### Intros

BANNED: "Провел ресерч по бизнес-событиям и алертам (BE-5799) - каталоги, стандарт, диаграммы..."

HUMAN: "посмотрел задачу по алертам и событиям (BE-5799), там всё сильно веселее, чем мы думали"

HUMAN: "разобрал флоу по алертингу. если коротко: в проде сейчас почти ничего из нужного не
работает"

### Bullet lists vs. spoken sequencing

BANNED:

> Из четырёх пилотных алертов A1–A4 в проде не покрыт ни один...
>
> 28 действующих правил, включая все Core-овские, не имеют получателя...

HUMAN: "во-первых, из четырех пилотных алертов сейчас не работает ни один. то, что считалось живым,
смотрит в старый флоу, а на /policy/store правил вообще нет во-вторых, 28 правил (включая весь core)
сейчас стреляют в пустоту, у них нет получателя. мониторинг прямо сейчас по факту молчит"

### Blockers and estimations

BANNED: "В постановке около двадцати блокеров... Оценка после снятия блокеров: 9–16 человеко-дней."

HUMAN: "по самой постановке набралось около 20 блокеров: от невалидных типов в ELK до несуществующих
ручек. пока их не снимем, разработку начинать бессмысленно, иначе потом всё переписывать по срокам:
2–3 недели чистой работы, но всё упрется в скорость согласования. плюс надо на полдня проверить одну
штуку в графане, это сразу уточнит оценку"

## Transformation workflow

When given technical facts or a raw report:

1. Strip all template labels ("Главное:", "Блокеры:", "Оценка:").
2. Find the single most critical risk or finding and put it upfront.
3. Group related facts into 2–3 short, readable text blocks.
4. Replace formal nouns with active verbs ("происходит эмиссия" -> "отправляем", "не имеет попыток
   доставки" -> "молчит").
5. Drop trailing summary fluff. Follow
   [Call to action & endings](#call-to-action--endings-no-polite-sign-offs).
6. Before returning the message, verify that every claim and number matches the source in meaning,
   scope, and certainty.

## Golden example

### Input (robot memo)

> Провел ресерч по бизнес-событиям и алертам (BE-5799) - каталоги, стандарт, диаграммы, код пяти
> сервисов, экспорт правил Grafana, шаблоны ELK Главное:
>
> Из четырёх пилотных алертов A1–A4 в проде не покрыт ни один. Считалось, что часть уже есть, но
> правила «payment succeeded but no policyNo» следят за старым флоу, а не за Core, а по
> /policy/store правил нет вообще
>
> 28 действующих правил, включая все Core-овские, не имеют получателя и висят только на лейбле
> slack_channel при пустом дереве маршрутов. Плюс contact point, на котором вся группа
> Core_monitoring и дрейф-алерт, не имеет ни одной попытки доставки. Похоже, часть алертинга молчит
> прямо сейчас - это стоит проверить раньше всего остального
>
> В постановке около двадцати блокеров: критерий успеха Anoud (202 против 200), недостижимый ключ
> связи у A7, условие детекта дублей, запрещённое уникальным индексом в БД, событие для
> несуществующей ручки смены карты. Пока имена событий, ключи и типы полей не зафиксированы, эмиссию
> начинать нельзя - переписывать придётся всё
>
> Типы полей в ELK надо решить до первой записи: числа и даты сейчас лежат внутри payload, а он
> хранит всё строками. Ни сумм, ни диапазонов, ни сортировки по датам Оценка после снятия блокеров:
> 9–16 человеко-дней, две-три недели на одного с ИИ-агентом. Срок определит не разработка, а
> скорость согласования постановки Сильнее всего оценку двигает один вопрос: умеет ли Grafana ловить
> отсутствие события по доменному ключу. Проверяется за полдня, разброс - четыре дня Детали и полный
> список блокеров: ССЫЛКА

### Output (human chat)

> разобрал задачу по алертингу и событиям (BE-5799), там по факту всё надо пересобирать
>
> главная проблема: из четырех пилотных алертов в проде сейчас нет ни одного. то, что считалось
> рабочим, смотрит в старый флоу, а по /policy/store правил вообще нет. плюс 28 действующих правил
> (включая весь Core) висят без получателей и стреляют в пустоту, мониторинг сейчас скорее всего
> просто молчит
>
> по самой постановке насчитал около 20 блокеров: не те статусы ответов, кривые ключи связей и типы
> в ELK, где всё лежит строками. пока это не зафиксируем, публикацию событий начинать нельзя, иначе
> придется переделывать отправку
>
> по оценке: недели 2-3 чистой работы, но срок определит именно согласование требований. еще надо за
> полдня проверить, умеет ли графана ловить отсутствие события по ключу, это сразу уберет разброс в
> 4 дня по эстимейту
>
> весь список блокеров и детали собрал тут: [ссылка]

## Additional micro-rules for Russian engineering context

### Filler & preamble ban

BANNED: "Стоит отметить, что...", "Важно подчеркнуть...", "Следует обратить внимание..."

RULE: Delete all preamble phrases. Start directly with the subject and the action.

### Syntax: kill participle overload (Деепричастные обороты)

BANNED: "Проанализировав логи и выявив утечку памяти, было принято решение..."

HUMAN: "Посмотрел логи. Там течет память, поэтому надо рестартить сервис."

### Natural Russian dev vocabulary (clean, no slang/profanity)

Use standard industry verbs instead of literal bureaucratic translations:

- "эмиссия событий" -> "отправка / публикация событий"
- "осуществлять мониторинг" -> "следить / мониторить"
- "произошел сбой в доставке" -> "алерты не доходят / отвалились"
- "инициировать процесс согласования" -> "пойти к ребятам и согласовать"

### Call to action & endings (no polite sign-offs)

BANNED: "Дайте знать, если есть вопросы!", "Буду держать в курсе прогресса", "Что думаете?"

RULE: End with either:

- A concrete technical question to a specific owner ("кто сейчас за ручку смены карты отвечает?").
- A direct next step ("пока пойду проверю графану, детали тут: [link]").
- No sign-off at all (just the link / update).

### Density & visual rhythm

Max length: 3-4 short paragraphs (under 150-200 words total).

If an update needs more detail, put the deep dive in a doc/ticket and link it.

Separate thoughts with single blank lines, never write a wall of text.

### Anti-hedging (clear fact vs hypothesis)

BANNED: "Возможно, вероятно, судя по всему, предположительно..."

RULE: Separate known facts from assumptions cleanly:

- Fact: "мониторинг молчит"
- Hypothesis: "похоже, правила писали еще под старый флоу"
- Action: "проверю за полчаса"
