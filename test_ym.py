import requests

url = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
params = {
    "$limit": 500,
    "$order": "report_date_as_yyyy_mm_dd DESC",
    "$select": "market_and_exchange_names",
}

r = requests.get(url, params=params, timeout=30)
data = r.json()

unique = sorted(set(d.get("market_and_exchange_names", "") for d in data))

print("=== DOW / DOW JONES ARAYANLAR ===")
for name in unique:
    if "DOW" in name.upper() or "DJIA" in name.upper() or "INDUSTRIAL" in name.upper():
        print(f"  {name}")

print("\n=== TÜM FİNANSAL MARKETLER (kontrol için) ===")
for name in unique:
    if "CHICAGO" in name.upper() and any(x in name.upper() for x in ["DOW", "S&P", "NASDAQ", "RUSSELL", "EURO", "YEN", "POUND", "DOLLAR", "FRANC"]):
        print(f"  {name}")