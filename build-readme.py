import json, os

obs = json.load(open('super-funded-obs.json'))
firm = obs['dealstore']
latest = obs['observations'][0]

is_global = os.environ['IS_GLOBAL'] == 'true'
code = os.environ['STANDING_CODE']
discount = os.environ['DISCOUNT']
month_year = os.environ['MONTH_YEAR']

by_year = {}
for o in obs['observations']:
    year = o['date_published'].split('-')[0]
    if year not in by_year:
        by_year[year] = []
    by_year[year].append(o)
years = sorted(by_year.keys(), reverse=True)

readme = f"""---
license: other
tags:
- discount-codes
- prop-firm
- trading
- {os.environ['FIRM_SLUG']}
size_categories:
- n<1K
---
# {firm['name']} - Deal History

Historical deal observations from [PropFirmDiscount.com](https://propfirmdiscount.com) - The trusted prop firm coupon directory.

**Prop firm page:** {firm['url']}

**Verified exclusive discount code:** {code} (works any time; live rate always on prop firm page)

Use discount code **{code}** to get **{discount} off** on {firm['name']} challenges and accounts in {month_year}. This exclusive discount code is verified by our team at PropFirmDiscount.com and gives you the best pricing on all {firm['name']} evaluation accounts.

---

## Latest Deal

### {firm['name']} - {latest['title']}

<ul>
<li><strong>Published:</strong> {latest['date_published']}</li>
<li><strong>Offer ends:</strong> {latest.get('date_exp') or 'N/A'}</li>
<li><strong>Discount:</strong> {latest['discount_value']}</li>
"""

if latest.get('scope'):
    readme += f"<li><strong>Scope:</strong> {', '.join(latest['scope'])}</li>\n"

if is_global:
    readme += f"<li><strong>Code:</strong> {code}</li>\n"

readme += f"""<li><strong>Deal page:</strong> <a href="{latest['post_url']}">{latest['post_url']}</a></li>
</ul>
"""

if not is_global:
    readme += "\n**Note:** This deal has a limited-time campaign code. Visit the deal page to get the code and full terms.\n"

readme += f"""

---

## Discount Code History

Total deals tracked: **{len(obs['observations'])}**

"""

# Tables by year
for year in years:
    deals = by_year[year]
    readme += f"### {year} ({len(deals)} deals)\n\n"
    readme += "| Deal Date | Title | Discount | Expires | Deal Link |\n"
    readme += "|---|---|---|---|---|\n"

    for deal in deals:
        title = deal['title'].replace('|', '\\|')
        expires = deal.get('date_exp') or 'N/A'
        disc = deal['discount_value']
        if '%' in disc and 'off' not in disc.lower():
            disc = disc + ' off'
        readme += f"| {deal['date_published']} | {title} | {disc} | {expires} | [View Deal]({deal['post_url']}) |\n"

    readme += "\n"

readme += f"""---

## About This Repository

This repository tracks all historical deals for **{firm['name']}** published on PropFirmDiscount.com. Updated hourly via automated sync.

**Data source:** PropFirmDiscount.com
**Prop firm profile:** {firm['url']}

## Freshness

<!-- pfd-last-synced (auto-updated each sync) -->
Last synced: {os.environ['STAMP']} (auto, hourly)

Deals are tracked continuously by the PropFirmDiscount team; this mirror syncs with the live API within an hour. Campaign codes come and go with each promotion; standing codes are re-verified yearly.

## License

Data © PropFirmDiscount. May be referenced with attribution and a link to https://propfirmdiscount.com.
"""

with open('README.md', 'w') as f:
    f.write(readme)

print("✓ README generated successfully")
