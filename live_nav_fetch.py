from pathlib import Path

import pandas as pd
import requests


# Directory to save raw API data
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


# Scheme codes provided in the assignment
SCHEMES = {
    "125497": "HDFC_Top_100",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip",
}


def fetch_and_save_nav(scheme_code, assigned_name):

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nFetching: {scheme_code} ({assigned_name})")

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:

            data = response.json()

            meta = data.get("meta", {})
            nav_list = data.get("data", [])

            actual_scheme_name = meta.get(
                "scheme_name",
                assigned_name
            )

            fund_house = meta.get(
                "fund_house",
                "Unknown"
            )

            print(f"API Scheme Name: {actual_scheme_name}")
            print(f"Fund House: {fund_house}")

            if not nav_list:
                print(
                    f"No NAV records found for "
                    f"scheme code {scheme_code}."
                )
                return

            # Convert NAV records to DataFrame
            df = pd.DataFrame(nav_list)

            # Add scheme information
            df["amfi_code"] = scheme_code
            df["scheme_name"] = actual_scheme_name

            # Save raw API data
            output_path = (
                RAW_DIR / f"live_nav_{scheme_code}.csv"
            )

            df.to_csv(
                output_path,
                index=False
            )

            print(
                f"Saved: {output_path} "
                f"({len(df)} rows)"
            )

        else:

            print(
                f"Failed to fetch {assigned_name} "
                f"({scheme_code}). "
                f"Status: {response.status_code}"
            )

    except requests.exceptions.RequestException as error:

        print(
            f"Network/API error for "
            f"{scheme_code}: {error}"
        )


# Fetch NAV for all targeted schemes
for code, name in SCHEMES.items():

    fetch_and_save_nav(
        code,
        name
    )