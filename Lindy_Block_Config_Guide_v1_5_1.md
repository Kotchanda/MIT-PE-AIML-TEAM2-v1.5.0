# Lindy block-by-block configuration guide (v1.5.0)

Generated: 2026-02-28T20:56:14Z


This guide is **Lindy-optimized**: each block includes what to configure in the Lindy UI, what variables to store, and the **exact field mappings** between the questionnaire and `plans.json`.


## 1) Data model: `benefit_dictionary.json` fields

These are the fields your bot reads/writes. **NULL means unknown** (never treat as false).


| field                    | type         | required   | enum   | description                                                            |
|:-------------------------|:-------------|:-----------|:-------|:-----------------------------------------------------------------------|
| last_verified            | date         | True       |        |                                                                        |
| source_url               | text         | True       |        |                                                                        |
| cancer_cover             | boolean|null | False      |        |                                                                        |
| cardiac_cover            | boolean|null | False      |        |                                                                        |
| completeness_score       | number       | False      |        | 1 - (null_key_count / number_of_key_fields). Range 0.0–1.0 (computed). |
| day_case                 | boolean|null | False      |        |                                                                        |
| doc_type                 | enum|null    | False      |        | Type of public source_url.                                             |
| effective_from           | date|null    | False      |        | Effective date stated on plan Table of Cover/Benefits (if known).      |
| excess_amount_text       | text|null    | False      |        |                                                                        |
| excess_required          | boolean|null | False      |        |                                                                        |
| gp_visits                | boolean|null | False      |        |                                                                        |
| hospital_cover           | enum|null    | False      |        |                                                                        |
| maternity_cover          | boolean|null | False      |        |                                                                        |
| maternity_waiting_months | integer|null | False      |        |                                                                        |
| mental_health            | boolean|null | False      |        |                                                                        |
| null_key_count           | integer      | False      |        | Number of NULLs across key decision fields (computed).                 |
| outpatient_cover         | boolean|null | False      |        |                                                                        |
| overseas_emergency       | boolean|null | False      |        |                                                                        |
| overseas_planned         | boolean|null | False      |        |                                                                        |
| plan_tier                | enum|null    | False      |        |                                                                        |
| private_room             | boolean|null | False      |        |                                                                        |
| public_open_url          | text|null    | False      |        | Public URL to open plan details/documents. If absent, use source_url.  |
| semi_private_room        | boolean|null | False      |        |                                                                        |



## 2) Question → field mapping (exact)

These are the authoritative mappings from `question_bank.json` (`maps_to_fields`).


| question_id          | type          | maps_to_fields                            | question_text                                                      | options                                                  |
|:---------------------|:--------------|:------------------------------------------|:-------------------------------------------------------------------|:---------------------------------------------------------|
| Q_EXCESS_TOLERANCE   | single_choice | excess_required, excess_amount_text       | Are you comfortable paying an excess/co-payment to reduce premium? | Prefer no excess | Small excess is fine | Excess is fine |
| Q_HOSPITAL_LEVEL     | single_choice | hospital_cover                            | What level of hospital access do you want?                         | Public only | Private | Hi-Tech                          |
| Q_MATERNITY          | boolean       | maternity_cover, maternity_waiting_months | Is maternity cover important in the next 2–3 years?                | True | False                                             |
| Q_MENTAL_HEALTH      | boolean       | mental_health                             | Is mental health cover important to you?                           | True | False                                             |
| Q_OUTPATIENT_USAGE   | single_choice | outpatient_cover, gp_visits               | How often do you expect to use GP and outpatient services?         | Rarely | Sometimes | Often                               |
| Q_OVERSEAS_EMERGENCY | boolean       | overseas_emergency                        | Do you need overseas emergency cover?                              | True | False                                             |
| Q_PRICE_POSTURE      | single_choice | plan_tier                                 | Which best describes your approach?                                | Price-sensitive | Balanced | Benefit-maximizing          |
| Q_ROOM_PREFERENCE    | single_choice | semi_private_room, private_room           | Do you prefer private/semi-private room cover where available?     | Not important | Semi-private is fine | Private preferred |



## 3) Recommended option-to-value normalization

Lindy should store the user’s selection as normalized values. Use the mappings below as defaults.


### Q_EXCESS_TOLERANCE

- `Prefer no excess` → `LOW`

- `Small excess is fine` → `MEDIUM`



### Q_HOSPITAL_LEVEL

- `Public only` → `PUBLIC`

- `Private` → `PRIVATE`

- `Hi-Tech` → `HI_TECH`



### Q_MATERNITY

- `True` → `True`

- `False` → `False`



### Q_MENTAL_HEALTH

- `True` → `True`

- `False` → `False`



### Q_PRICE_POSTURE

- `Price-sensitive` → `BUDGET`

- `Balanced` → `BALANCED`

- `Benefit-maximizing` → `PREMIUM`



## 4) Lindy blocks (exact configuration)

### Block 1 — Consent Gate

- UI: render `compliance_statement.md` (asset)
- Buttons: `I Agree`, `Decline`
- Variables:
  - `consent.accepted` (bool)
  - `session_id` (string)
- Routing:
  - If `Decline`: end session (or switch to read-only info mode)


### Block 2 — Mode Select

- Question: Fast (6 Qs) vs Deep (12 Qs)
- Variables:
  - `mode` = `FAST` or `DEEP`
  - `question_budget` = 6 or 12


### Block 3 — Load Assets

Configure Lindy ‘Load File / Knowledge Asset’ steps:
- `question_bank.json` → `cfg.questions`
- `plans.json` → `data.plans`
- `scoring_spec.json` → `cfg.scoring`
- `benefit_dictionary.json` → `cfg.schema`
- Initialize:
  - `answers = {}`
  - `asked_questions = []`
  - `remaining_plans = data.plans.plans` (array)
  - `verification_flags = {}`


### Block 4 — Dataset validation

- For each plan:
  - Ensure `public_open_url` exists; else fallback to `source_url`
  - Ensure `null_key_count` and `completeness_score` exist; if missing compute using KEY_FIELDS
- KEY_FIELDS (must match compute_completeness):
  - `plan_tier, hospital_cover, outpatient_cover, gp_visits, maternity_cover, mental_health, overseas_emergency, semi_private_room, private_room, excess_required`


### Block 5 — Ask-Next Selector (internal)

- Inputs: `remaining_plans`, `answers`, `asked_questions`, `cfg.questions`, optional `analytics_summary`
- Output: `next_question` JSON with `question_id`, `options`, optional `followup_if_uncertain`
- Stop rules:
  - `len(asked_questions) >= question_budget` OR `len(remaining_plans) <= 15` OR user clicks “Show results now”


### Block 6 — Ask Question (broker style)

- Render `next_question` as:
  - 1 line rationale (“why it matters”)
  - buttons for each option
  - button: `Not sure`
- If `Not sure`: ask exactly **one** follow-up, then accept NULL if still unclear.


### Block 7 — Normalize Answer → Schema Fields (exact)

- Use `maps_to_fields` for that question_id.
- Write normalized values into `answers.fields` (not raw text).
- Recommended stored object:
```json
{
  "answers": {
    "Q_HOSPITAL_LEVEL": {"hospital_cover": "PRIVATE", "confidence": 0.9},
    "Q_MATERNITY": {"maternity_cover": true, "confidence": 0.8}
  }
}
```


### Block 8 — NULL-safe elimination

- For each plan in `remaining_plans`:
  - If plan[field] is NULL: keep plan + set `verification_needed=true`
  - Else apply definitive mismatch rules
- If `remaining_plans` becomes 0: rollback last elimination and mark that question as “soft” for next runs.


### Block 9 — Score + tie-break

- Compute score from `cfg.scoring`
- Tie-break:
  1) higher score
  2) if within 5 points → higher `completeness_score`
  3) fewer verification flags
- Output: `ranked_plans` top 10


### Block 10 — Explainable results UI

- Render Top 3–5 plan cards with:
  - plan name + insurer
  - score
  - top 3 drivers
  - trade-offs
  - verification badge
  - button opens `public_open_url`
- Add “Compare” toggle (stores selected plan_ids)


### Block 11 — Telemetry (anonymous only)

- Write a row/event to Lindy data store with schema:
  - `session_id`, `consent_accepted`, `mode`, `asked_questions` (IDs), `dropoff_question_id`, `presented_plan_ids`, `clicked_plan_id`, `helpful`, `time_to_recommendation_sec`
- Absolutely no free-text transcript storage.


### Block 12 — Stats page (charts)

- Query aggregate counters from Lindy store:
  - top clicked plans
  - top asked questions
  - dropoff questions
- Render bars using:
  - `labels[]`, `values[]`


## 5) Exact mappings (copy/paste)

Use these mappings in your Lindy normalization block:


- `Q_HOSPITAL_LEVEL` → `hospital_cover`

- `Q_PRICE_POSTURE` → `plan_tier`

- `Q_MATERNITY` → `maternity_cover`, `maternity_waiting_months`

- `Q_OUTPATIENT_USAGE` → `outpatient_cover`, `gp_visits`

- `Q_MENTAL_HEALTH` → `mental_health`

- `Q_ROOM_PREFERENCE` → `semi_private_room`, `private_room`

- `Q_OVERSEAS_EMERGENCY` → `overseas_emergency`

- `Q_EXCESS_TOLERANCE` → `excess_required`, `excess_amount_text`




## v1.5.1 Addendum — Broker-style rendering of questions

In the **Ask Question** block, do NOT display `question_text` directly.

Instead:
- Use `broker_openers[]` to phrase the question naturally
- Offer buttons from `broker_button_labels[]`
- If unclear, ask exactly one follow-up from `soft_probes[]`
- Then write only the normalized enum/boolean values into `answers`

This keeps the UI conversational while preserving deterministic field mappings.