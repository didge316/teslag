# ClickBank API — teslamagneticgenerator.com hops report

Generated 2026-07-15. Data pulled live from the ClickBank Analytics API.

## Auth

- Endpoint base: `https://api.clickbank.com/rest/1.3`
- Header format: `Authorization: API-...` (NO `Bearer` prefix — using `Bearer` returns 401 "Invalid API key")
- Accept: `application/json`
- Key role: ClickBank API Key with **Analytics** permission (Developer key alone is no longer required as of Aug 2023)
- Account nickname for this site: **`didge2009`** (the `d8eb82m1v0d` in the hoplinks is the affiliate vendor param, not the account nickname)

## Useful endpoints

| Purpose | URL |
|---|---|
| List accounts I can read | `GET /quickstats/accounts` |
| Total sale/refund/cb | `GET /quickstats/count?account=didge2009&startDate=...&endDate=...` |
| Daily sale/refund/cb | `GET /quickstats/list?account=didge2009&startDate=...&endDate=...` |
| Hops per vendor | `GET /analytics/AFFILIATE/VENDOR?account=didge2009&startDate=...&endDate=...` |
| Hops per tracking ID (tid) | `GET /analytics/AFFILIATE/TRACKING_ID?account=didge2009&startDate=...&endDate=...` |
| Hops per product (vendor side) | `GET /analytics/AFFILIATE/VENDOR_PRODUCT_SKU?account=didge2009&...` |

Key `select` fields: `HOP_COUNT`, `SALE_COUNT`, `NET_SALE_AMOUNT`, `ORDER_IMPRESSION`, `EARNINGS_PER_HOP`, `HOPS_PER_SALE`.

Spec: https://support.clickbank.com/en/articles/10535402

## Product swap (from git history)

Repo: `/home/matt/projects/other/tesla-generator/website`

| Commit | Date | Note |
|---|---|---|
| `ff71671` | 2026-07-02 19:18 | **Swap to Ultimate OFF-GRID Generator (enrev) + add nofollow to all affiliate links** |
| `93b26a7` | 2026-07-03 | Rebrand CTAs to "Complete Ultimate OFF-GRID Generator", swap hero video, rename spokesperson |
| `e769f4d` | 2026-07-03 | Site-wide SEO polish and video warm-up copy |
| `bf37fe4` | 2026-07-03 | Swap tower-ad image and remove sidebar ad/news card outlines |

Hoplink change in `ff71671`:
- Before: `https://d061e8q2v47zfya8scml6ucs3p.hop.clickbank.net/?tid=...` (old product)
- After:  `https://d8eb82m1v0d-e34sx8nd2men7t.hop.clickbank.net/?tid=...` (new "Ultimate OFF-GRID Generator")

Switch date: **Jul 2, 2026**. Use Jul 1 vs Jul 3 as the clean cutoff.

## Hops: before vs after

Note: all hops come in as `vendor=Direct` (ClickBank's analytics API collapses vendor for affiliate calls on this account), so per-vendor split is not possible — use `TRACKING_ID` (the `?tid=` param) for placement-level breakdown instead.

### Totals around the switch

| Window | Days | Hops | Hops/day | Sales | Net $ | Order impressions |
|---|---|---|---|---|---|---|
| Before — 2026-06-18 → 2026-07-01 | 14 | **479** | 34.2 | 0 | $0.00 | 0 |
| After  — 2026-07-03 → 2026-07-14 | 12 | **465** | 38.8 | 0 | $0.00 | **6** |
| 2026-07-01 → 2026-07-14 (combined) | 14 | 524 | 37.4 | 0 | $0.00 | 6 |
| Trailing 60d (2026-05-15 → 2026-07-14) | 61 | 1905 | 31.2 | 1 | $26.18 | 15 |

Reading: hop count is roughly flat-to-up. The clear improvement is **order form impressions**: 0 in the 14 days before the swap vs 6 in the 12 days after — meaning the new pitch page is actually getting visitors to the order form, where the old one wasn't. No sales yet in either window (the one $26.18 sale in the trailing-60d view occurred before the switch).

### Hops by tracking ID (`?tid=`)

#### BEFORE — 2026-06-18 → 2026-07-01 (14d) — 479 hops, 0 sales, 0 order impressions

| tid | hops |
|---|---|
| Not Set | 334 |
| index_btm | 16 |
| index_top_txt | 15 |
| index_takeamin | 15 |
| index_pic_txt | 15 |
| comment | 15 |
| index_vid | 14 |
| side_square | 12 |
| side_tower | 12 |
| whole_house_btm | 2 |
| perp_video | 2 |
| scam_btm | 1 |
| ABC11 | 1 |
| solar_btm | 1 |
| MGWP | 1 |
| linktop | 1 |
| from_magnets | 1 |
| sound_proof | 1 |
| oldman | 1 |
| side_ad | 1 |
| perp_real | 1 |
| ABC39 | 1 |
| check2 | 1 |
| oldman_pic | 1 |
| under_solar_vid | 1 |
| index_perp_under | 1 |
| index_this_web | 1 |
| ABC78 | 1 |
| ABC75 | 1 |
| solar_vid | 1 |
| perp_top | 1 |
| check | 1 |
| ABC88 | 1 |
| perp_these_btm | 1 |
| htb_vid_txt | 1 |
| perp_these | 1 |
| build_btm | 1 |
| htm_fe_btm | 1 |
| **TOTAL** | **479** |

#### AFTER — 2026-07-03 → 2026-07-14 (12d) — 465 hops, 0 sales, 6 order impressions

| tid | hops | ord_imp |
|---|---|---|
| Not Set | 132 | 0 |
| index_top_txt | 26 | 0 |
| side_tower | 24 | 0 |
| index_pic_txt | 24 | 1 |
| comment | 22 | 1 |
| index_btm | 22 | 0 |
| index_takeamin | 21 | 1 |
| index_vid | 19 | 1 |
| side_square | 18 | 1 |
| solar_btm | 7 | 0 |
| whole_house_btm | 7 | 1 |
| htb_click_here | 6 | 0 |
| sound_proof | 6 | 0 |
| under_solar_vid | 6 | 0 |
| build_btm | 6 | 0 |
| htb_vid_txt | 6 | 0 |
| oldman_this_project | 6 | 0 |
| htm_fe_btm | 6 | 0 |
| index_perp_under | 5 | 0 |
| solar_vid | 5 | 0 |
| oldman_vid | 5 | 0 |
| perp_top | 5 | 0 |
| oldman_third | 5 | 0 |
| side_square_whole | 5 | 0 |
| side_tower_whole | 5 | 0 |
| perp_btm | 5 | 0 |
| motor | 5 | 0 |
| wplink2 | 4 | 0 |
| wplink3 | 4 | 0 |
| perp_real | 4 | 0 |
| magmo_top | 4 | 0 |
| side_perp | 4 | 0 |
| reviewli | 4 | 0 |
| scam_btm | 4 | 0 |
| perp_these_btm | 4 | 0 |
| perp_video | 3 | 0 |
| perp_these | 3 | 0 |
| side_ad | 3 | 0 |
| wplinkcon | 3 | 0 |
| side_mag2019 | 3 | 0 |
| wplinkcon2 | 3 | 0 |
| wplink4 | 2 | 0 |
| wplink | 2 | 0 |
| ABC29 | 1 | 0 |
| mc_ind | 1 | 0 |
| **TOTAL** | **465** | **6** |

## Conclusion

Is it getting better hops? **Marginal — hops/day nudged up from ~34 to ~39 (+13%).** The real signal is funnel depth: order-form impressions went 0 → 6, so the new pitch page is converting hop traffic further than the old one did. Still 0 sales in the 12 days post-swap, so too early to call it a win — worth re-checking in another 2–3 weeks once the new pitch page has more order-form traffic to convert.

## How to re-run this

```bash
KEY="API-..."  # Clerk/API key with Analytics permission, no Bearer
ACCT="didge2009"

# Totals (per vendor)
curl -sS -H "Authorization: $KEY" -H "Accept: application/json" \
  "https://api.clickbank.com/rest/1.3/analytics/AFFILIATE/VENDOR?account=$ACCT&startDate=2026-07-03&endDate=2026-07-14&select=HOP_COUNT&select=SALE_COUNT&select=NET_SALE_AMOUNT&select=ORDER_IMPRESSION"

# By tracking ID
curl -sS -H "Authorization: $KEY" -H "Accept: application/json" \
  "https://api.clickbank.com/rest/1.3/analytics/AFFILIATE/TRACKING_ID?account=$ACCT&startDate=2026-07-03&endDate=2026-07-14&select=HOP_COUNT&select=SALE_COUNT&select=ORDER_IMPRESSION"
```