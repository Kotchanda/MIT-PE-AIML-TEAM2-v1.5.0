# Ingestion Runbook (UI-only) — Full Plan Benefit Extraction (v1.6.0)

Generated: 2026-03-01T17:33:22Z

This runbook upgrades the dataset by extracting **full benefit-level records** from public insurer documents
(PDF tables of cover / tables of benefits) for:

- Irish Life Health (TOC registry page)
- VHI (downloads + plan pages)
- Laya (scheme pages + PDFs; HIA PDFs as fallback)
- Level (plan pages + PDFs when available; HIA updates as change log)

## A. Where to run ingestion (no local terminal)

Choose ONE of these browser-only options:
1) **Lindy Hosted Code / VM** (if your Lindy workspace supports it)
2) **Any managed "run code in browser" environment** you control (internal dev portal)

### A1) If using Lindy Hosted Code / VM
1. Create a new Lindy workflow: **Data → Refresh Plan Benefits**
2. Add a “Code” block (Python) and paste the contents of:
   - `ingestion/enrich_plans.py`
   - `ingestion/pdf_parser.py`
   - `ingestion/utils.py`
   - provider adapters (`provider_*.py`)
3. Add Python deps in the Lindy environment (if there is a “Dependencies” UI):
   - `requests`, `beautifulsoup4`, `pdfplumber`
4. Configure storage paths as variables:
   - `PLANS_JSON_PATH` = current `plans.json` asset
   - `OUTPUT_PLANS_JSON_PATH` = `plans_enriched.json` (new asset)
   - `CACHE_DIR` = `/tmp/plan_docs_cache` (or Lindy cache)

5. Run the workflow manually once, then schedule it weekly/monthly.

### A2) If Lindy does NOT support hosted code/VM
Use the same workflow concept but run the script in your managed execution environment and then:
- Upload the generated `plans_enriched.json` back into Lindy assets.

## B. What the ingestion produces
- `benefits[]` per plan: list of extracted benefit records (hundreds per plan possible)
- `benefits_meta`: extraction status, sources, parser version, timestamp
- Updated `public_open_url` pointing to the official PDF when a match is found

## C. How the broker-agent uses this
- The agent uses natural broker-style questions
- Maps answers into structured core fields
- Scores using `scoring_spec.json`
- When a user asks “why?”, the agent can cite specific benefit records:
  - category + benefit_name + limit + source_page + source_url

## D. Important limitations (honest)
- Matching PDFs to plan names is **best-effort**; you will improve matching by adding a `plan_document_url` field
  per plan (recommended).
- Some providers may not publish a complete PDF registry; in those cases extraction coverage may be partial until
  additional sources (HIA plan PDFs) are integrated.
