# Policy Refresh Runbook (v1.3.0)

Objective: keep `plans.json` current and ensure each plan has a public-open URL.

## Sources to monitor (public)
1) Irish Life Health — Tables of Cover (effective date banners show the current year)
2) Laya Healthcare — Schemes list page (the canonical plan name list)
3) VHI — All health insurance plans (plan description pages) + Downloads (Tables of Benefits)
4) Level Health — Plans page + insurer update notices
5) HIA “Insurance Plan Updates” monthly pages (new/updated plans and effective dates)

## Monthly refresh procedure
1. Check HIA “Insurance Plan Updates” for new plans (add rows immediately).
2. For each insurer:
   - Compare current plan name list against your dataset.
   - Add new plan names as stubs with `source_url` pointing to the plan list page.
3. For any plan selected by users frequently:
   - Replace index `source_url` with a plan-specific PDF or plan description URL.
4. Populate key fields from the plan-specific document.
5. Recompute completeness:
   - run `compute_completeness.py` (or equivalent)
6. Publish updated `plans.json` + bump version.

## URL quality rule
Preferred: plan-specific PDF (Table of Cover/Benefits) or plan description page.
Fallback: insurer plan list page or HIA update notice (temporary only; mark for enrichment).