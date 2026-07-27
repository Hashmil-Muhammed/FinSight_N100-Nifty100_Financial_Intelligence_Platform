# Sprint 3 Retrospective: Peer Engine & Reporting

**Date:** July 2026  
**Intern Name:** Hashmil Muhammed 
**Sprint Goal:** Build the Peer Engine (Module 4), calculate percentile ranks, and generate Excel reports for peer comparisons.

## 🟢 What Went Well?
* Successfully implemented percentile ranking logic using Pandas `.rank(pct=True)`.
* Handled automated generation of multiple Excel sheets segmented by `peer_group_name` using `openpyxl`.
* Built an automated Data Quality (DQ) test script that verified all ranks fall within the valid 0-100 limits.
* All final DQ tests are passing and fully green.

## 🔴 What Didn't Go Well?
* **Data Mapping Issues:** Faced challenges where the `ROE` and `NPM` columns were initially missing in the Excel output. This happened because the raw data was stored in `financial_ratios`, but the report script was primarily querying `peer_percentiles`.
* **SQL Join Failures:** Direct SQL JOIN operations resulted in empty datasets due to slight formatting mismatches in the `year` column between different tables.

## 💡 Action Items & Learnings
* **Action Item:** Resolved the data mapping issue by fetching both tables separately and using a **Pandas `merge()`** with `.astype(str).str.strip()` to ensure accurate alignment of `company_id` and `year`.
* **Learning:** Relying solely on SQL `JOIN` can be risky if data types or formats (like strings with hidden spaces) do not match perfectly. Using Pandas for memory-merging is more robust for data manipulation.
* **Learning:** Always implement proactive Data Quality checks before exporting final reports to catch empty/null values early.