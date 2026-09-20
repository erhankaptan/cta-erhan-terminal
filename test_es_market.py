import requests

url = "https://publicreporting.cftc.gov/resource/gpe5-46if.json"
params = {
    "$limit": 500,
    "$order": "report_date_as_yyyy_mm_dd DESC",
    "$select": "market_and_exchange_names",
}

r = requests.get(url, params=params, timeout=30)
data = r.json()

# S&P 500, NASDAQ, EURO içeren tüm market adlarını göster
unique = sorted(set(d.get("market_and_exchange_names", "") for d in data))

print("=== ES (S&P) ===")
for name in unique:
    if "S&P" in name.upper() or "SP" in name.upper():
        print(f"  {name}")

print("\n=== NQ (NASDAQ) ===")
for name in unique:
    if "NASDAQ" in name.upper():
        print(f"  {name}")

print("\n=== 6E (EURO) ===")
for name in unique:
    if "EURO" in name.upper():
        print(f"  {name}")

print("\n=== DIGER FINANSAL ===")
for name in unique:
    if any(x in name.upper() for x in ["DOW", "RUSSELL", "YEN", "POUND", "FRANC", "AUSTRALIAN", "CANADIAN", "SWISS"]):
        print(f"  {name}")