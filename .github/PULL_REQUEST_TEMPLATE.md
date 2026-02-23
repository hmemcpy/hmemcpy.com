# HTTPS Canonical URL Fix

## Problem
Search Console detected canonical URL mismatches:
- **Your site:** `http://hmemcpy.com/...` (HTTP)
- **Google index:** `https://hmemcpy.com/...` (HTTPS)

This causes SEO issues and duplicate content warnings.

## Solution
Config already has `base_url = "https://hmemcpy.com"` ✅

**Action needed:** Trigger a fresh deployment to rebuild with correct canonical URLs.

## After Merge
1. Site will rebuild with HTTPS canonicals
2. Google will re-crawl and update index
3. Search Console errors will resolve

## Verification
Run Search Console URL Inspection on any post after deployment:
- `userCanonical` should show `https://...`
- Should match `googleCanonical`
