# Irish Life Health TOC ingestion (direct PDF URLs)

High-value coverage step: ingest ALL Irish Life Health Tables of Cover PDFs from the official registry:

- https://www.irishlife.ie/health-insurance/help/tables-of-cover/

## What you get
- One plan row per ILH policy with a direct PDF URL (`source_url` / `public_open_url`)
- No quote-engine scraping; no premiums stored

## Run it
1) Install dependencies:
- `pip install requests beautifulsoup4 pandas`

2) Run in the package folder:
- `python ilh_toc_ingest.py --plans_json plans.json --plans_csv plans.csv --out_json plans.json --out_csv plans.csv`

3) Re-host updated `plans.json` and `plans.csv`

## Enrichment after ingestion
Use the direct PDF to fill:
- hospital_cover (PUBLIC/PRIVATE/HI_TECH)
- outpatient/day-to-day flags
- excess/co-pay flags
- maternity and mental health indicators

Then recompute completeness (`compute_completeness.py`) if needed.