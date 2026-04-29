"""
Currency Converter - Intermediate Python Project
Features:
  - Live exchange rates via Open Exchange Rates (free tier) OR fallback mock rates
  - Conversion history with timestamps
  - Favorites / bookmarked pairs
  - Reverse conversion
  - CLI menu-driven interface
  - JSON persistence for history & favorites
  - Input validation & error handling
  - Rate caching (1-hour TTL)
"""

import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────────
DATA_FILE = "converter_data.json"
CACHE_TTL = 3600          # seconds before rates are considered stale
API_URL = "https://open.er-api.com/v6/latest/USD"   # free, no key required

FALLBACK_RATES = {        # snapshot rates relative to USD (for offline use)
    "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.50,
    "CAD": 1.36, "AUD": 1.53, "CHF": 0.88, "CNY": 7.24,
    "INR": 83.10, "MXN": 17.15, "BRL": 4.97, "KRW": 1325.0,
    "SGD": 1.34, "HKD": 7.82, "NOK": 10.55, "SEK": 10.42,
    "DKK": 6.89, "NZD": 1.63, "ZAR": 18.63, "AED": 3.67,
}

CURRENCY_NAMES = {
    "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound",
    "JPY": "Japanese Yen", "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
    "CHF": "Swiss Franc", "CNY": "Chinese Yuan", "INR": "Indian Rupee",
    "MXN": "Mexican Peso", "BRL": "Brazilian Real", "KRW": "South Korean Won",
    "SGD": "Singapore Dollar", "HKD": "Hong Kong Dollar", "NOK": "Norwegian Krone",
    "SEK": "Swedish Krona", "DKK": "Danish Krone", "NZD": "New Zealand Dollar",
    "ZAR": "South African Rand", "AED": "UAE Dirham",
}

# ── Data persistence ────────────────────────────────────────────────────────────

def load_data() -> dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"history": [], "favorites": [], "cache": {}}

def save_data(data: dict) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Exchange rate fetching ──────────────────────────────────────────────────────

def fetch_live_rates() -> Optional[dict]:
    """Fetch rates from free API. Returns dict or None on failure."""
    try:
        with urllib.request.urlopen(API_URL, timeout=5) as resp:
            payload = json.loads(resp.read().decode())
            if payload.get("result") == "success":
                return payload["rates"]
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        pass
    return None

def get_rates(data: dict) -> tuple[dict, str]:
    """Return (rates_dict, source_label). Uses cache, live, or fallback."""
    cache = data.get("cache", {})
    cached_rates = cache.get("rates")
    cached_time = cache.get("timestamp", 0)

    if cached_rates and (time.time() - cached_time) < CACHE_TTL:
        return cached_rates, "cached"

    live = fetch_live_rates()
    if live:
        data["cache"] = {"rates": live, "timestamp": time.time()}
        save_data(data)
        return live, "live"

    print("  ⚠  Could not reach exchange rate API — using built-in fallback rates.")
    return FALLBACK_RATES, "fallback"

# ── Conversion logic ────────────────────────────────────────────────────────────

def convert(amount: float, from_cur: str, to_cur: str, rates: dict) -> Optional[float]:
    """Convert amount from_cur → to_cur via USD base."""
    if from_cur not in rates or to_cur not in rates:
        return None
    in_usd = amount / rates[from_cur]
    return in_usd * rates[to_cur]

def format_currency(amount: float, code: str) -> str:
    return f"{amount:,.4f} {code}"

# ── History & Favorites ─────────────────────────────────────────────────────────

def add_to_history(data: dict, entry: dict) -> None:
    data["history"].insert(0, entry)
    data["history"] = data["history"][:50]    # keep last 50 entries
    save_data(data)

def show_history(data: dict) -> None:
    history = data.get("history", [])
    if not history:
        print("\n  No conversion history yet.\n")
        return
    print(f"\n{'─'*60}")
    print(f"  {'CONVERSION HISTORY':^56}")
    print(f"{'─'*60}")
    for i, h in enumerate(history[:10], 1):
        print(f"  {i:2}. {h['timestamp'][:16]}  "
              f"{h['amount']:>12,.2f} {h['from']} → "
              f"{h['result']:>14,.4f} {h['to']}")
    print(f"{'─'*60}\n")

def toggle_favorite(data: dict, pair: str) -> None:
    favs = data.setdefault("favorites", [])
    if pair in favs:
        favs.remove(pair)
        print(f"  ★  Removed {pair} from favorites.")
    else:
        favs.append(pair)
        print(f"  ★  Added {pair} to favorites.")
    save_data(data)

def show_favorites(data: dict, rates: dict) -> None:
    favs = data.get("favorites", [])
    if not favs:
        print("\n  No favorites saved yet. Star a pair during conversion!\n")
        return
    print(f"\n{'─'*60}")
    print(f"  {'FAVORITE PAIRS  (rate per 1 unit)':^56}")
    print(f"{'─'*60}")
    for pair in favs:
        try:
            f, t = pair.split("/")
            rate = convert(1, f, t, rates)
            print(f"  {pair:<10}  1 {f} = {rate:>14,.4f} {t}")
        except Exception:
            print(f"  {pair}  (rate unavailable)")
    print(f"{'─'*60}\n")

# ── Input helpers ───────────────────────────────────────────────────────────────

def get_currency(prompt: str, rates: dict) -> str:
    while True:
        code = input(prompt).strip().upper()
        if code in rates:
            return code
        print(f"  ✗  '{code}' not recognised. Try: {', '.join(list(rates)[:8])} …")

def get_amount(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt).replace(",", ""))
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("  ✗  Please enter a positive number.")

# ── Screens ─────────────────────────────────────────────────────────────────────

def banner() -> None:
    print("\n" + "═"*60)
    print("  💱  CURRENCY CONVERTER  |  Intermediate Python Project")
    print("═"*60)

def menu() -> str:
    print("\n  [1] Convert currency")
    print("  [2] View conversion history")
    print("  [3] View & manage favorites")
    print("  [4] List all supported currencies")
    print("  [5] Quit")
    return input("\n  Choose an option: ").strip()

def do_conversion(data: dict, rates: dict, source: str) -> None:
    print(f"\n  (Rates source: {source})\n")
    amount   = get_amount("  Amount      : ")
    from_cur = get_currency("  From        : ", rates)
    to_cur   = get_currency("  To          : ", rates)

    result = convert(amount, from_cur, to_cur, rates)
    if result is None:
        print("  ✗  Conversion failed.")
        return

    rate = result / amount
    print(f"\n  ┌{'─'*50}┐")
    print(f"  │  {format_currency(amount, from_cur):>22}  →  {format_currency(result, to_cur):<22}│")
    print(f"  │  Rate: 1 {from_cur} = {rate:.6f} {to_cur:<37}│")
    print(f"  └{'─'*50}┘")

    # Reverse conversion
    print(f"  ↔  Reverse: 1 {to_cur} = {1/rate:.6f} {from_cur}")

    # Log to history
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "amount": amount, "from": from_cur,
        "result": result, "to": to_cur,
    }
    add_to_history(data, entry)

    # Offer to favorite
    pair = f"{from_cur}/{to_cur}"
    favs = data.get("favorites", [])
    hint = "remove from" if pair in favs else "add to"
    star = input(f"\n  Press F to {hint} favorites, or Enter to continue: ").strip().upper()
    if star == "F":
        toggle_favorite(data, pair)

def list_currencies(rates: dict) -> None:
    print(f"\n{'─'*60}")
    print(f"  {'CODE':<6} {'NAME':<28} {'1 USD ='}")
    print(f"{'─'*60}")
    for code in sorted(rates):
        name = CURRENCY_NAMES.get(code, "")
        print(f"  {code:<6} {name:<28} {rates[code]:.4f}")
    print(f"{'─'*60}\n")

# ── Main loop ───────────────────────────────────────────────────────────────────

def main() -> None:
    banner()
    data = load_data()
    rates, source = get_rates(data)
    print(f"  ✓  {len(rates)} currencies loaded  ({source} rates)\n")

    while True:
        choice = menu()
        if choice == "1":
            do_conversion(data, rates, source)
        elif choice == "2":
            show_history(data)
        elif choice == "3":
            show_favorites(data, rates)
        elif choice == "4":
            list_currencies(rates)
        elif choice == "5":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  ✗  Invalid option, please try again.")

if __name__ == "__main__":
    main()
