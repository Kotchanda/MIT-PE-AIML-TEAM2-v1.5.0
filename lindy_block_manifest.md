# Lindy Block Manifest — Irish Health Insurance Chooser (v1.4.1)

Generated: 2026-02-28T18:34:09Z

This is a **1:1 checklist** you can implement in Lindy. Each block lists: purpose, inputs, outputs, tools, and failure handling.

---

## BLOCK 0 — App Shell / Navigation
**Purpose:** Provide persistent navigation between:
- Chat (broker mode)
- Compare view (selected plans)
- Stats (post-session)
- Gov Dashboard (system manager)

**Inputs:** none  
**Outputs:** UI routes

**Failure handling:** if stats/gov pages can’t load, show “data not available” and continue.

---

## BLOCK 1 — Welcome + Consent Gate (No‑Storage)
**Purpose:** Explicit consent for session-only processing.

**Load:** `compliance_statement.md`  
**UI:** Agree / Decline

**Inputs:** user click  
**Outputs:** `consent.accepted` boolean

**Failure handling:** if user declines → end session or “general info mode” with no personal questions.

---

## BLOCK 2 — Mode Select (Fast‑track vs Deep‑dive)
**Purpose:** Set question budget and style.

**Inputs:** user choice  
**Outputs:**
- `mode = "FAST" | "DEEP"`
- `max_questions = 6 (FAST) / 12 (DEEP)`

**Failure handling:** default to FAST if user doesn’t choose.

---

## BLOCK 3 — Load Config + Dataset
**Purpose:** Load the runtime artifacts.

**Tools (GET):**
- `question_bank.json` → `cfg.questions`
- `scoring_spec.json` → `cfg.scoring`
- `benefit_dictionary.json` → `cfg.schema`
- `plans.json` → `data.plans`

**Outputs:**
- `remaining_plans`
- `answers`, `asked_questions`

**Failure handling:**
- If dataset fetch fails → show error and stop.
- If one config file fails → stop (configuration integrity required).

---

## BLOCK 4 — Validate Dataset + Completeness
**Purpose:** Ensure `public_open_url` exists and compute/validate completeness.

**Checks:**
- Each plan must have `public_open_url` (fallback to `source_url`)
- Compute/validate `null_key_count` and `completeness_score`

**Outputs:**
- `data_quality.avg_completeness`
- plan-level `verification_needed`

**Failure handling:**
- If plan has no open URL → exclude plan and log `DATA_QUALITY_MISSING_URL`.

---

## BLOCK 5 — “What you’ll need” Briefing (Pre‑Questions)
**Purpose:** Tell user what kinds of answers improve quality (budget posture, hospital access level, maternity, outpatient, etc.).

---

## BLOCK 6 — Broker‑Style Ask‑Next Loop
**Purpose:** Ask minimal high-yield questions with broker-like probing.

**Algorithm (each iteration):**
1) Select next question (priority × info‑gain × popularity − friction)
2) Ask with buttons + “other/unsure”
3) Capture answer + optionally 1 free-text clarification
4) Normalize to structured fields (maps_to_fields)

**Failure handling:**
- If user refuses/unsure → store `null` answer and continue.
- If user types sensitive data unexpectedly → warn and offer to proceed without.

---

## BLOCK 7 — NULL‑Safe Elimination
Eliminate only on definitive mismatch; NULL keeps plan + sets `verification_needed=true`.

**Failure handling:** if remaining_plans drops to 0 → relax the last filter and retry.

---

## BLOCK 8 — Score + Tie‑Break
Tie-break: within 5 points → higher `completeness_score` → fewer verification flags.

---

## BLOCK 9 — Explainable Results + Compare
Each plan card must include: score, reasons, trade-offs, verification badge, and `public_open_url`.

---

## BLOCK 10 — Feedback + Anonymous Telemetry
POST `/session_analytics` (no payload).

---

## BLOCK 11 — Post‑Session Stats Panel
GET `/analytics_summary` and render `post_session_stats_panel.md`.

---

## BLOCK 12 — Gov System Manager Dashboard
GET `/gov_health_summary` and render charts for capacity/flow/waiting lists.