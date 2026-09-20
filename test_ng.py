import requests

url = "https://publicreporting.cftc.gov/resource/72hh-3qpy.json"
params = {
    "$where": "upper(market_and_exchange_names) like '%HENRY HUB%'",
    "$order": "report_date_as_yyyy_mm_dd DESC",
    "$limit": 10,
}

r = requests.get(url, params=params, timeout=30)
data = r.json()

print(f"Toplam kayit: {len(data)}\n")

for d in data:
    market = d.get("market_and_exchange_names", "?")
    m_money_long = d.get("m_money_positions_long_all", "?")
    report_date = d.get("report_date_as_yyyy_mm_dd", "?")[:10]
    print(f"{report_date} | {market}")
    print(f"           | m_money_long = {m_money_long}")
    print()