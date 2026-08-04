#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from requests import Session, RequestException
from csv import DictWriter, DictReader
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep

COURTS = ["central", "eastern", "metro_south", "northeast", "southeast", "western"]
DEFAULT_START_DATE = "2020-10-24"
WEEKLY_END_DATE = datetime.strptime("2023-07-01", "%Y-%m-%d")
URL = "https://masslandlords.net/policy/eviction-data"
WEEKLY_URL = "/".join([URL, "filings-week-ending"])
MONTHLY_URL = "/".join([URL, "filings-month"])

def create_date_list(start_date, end_date=False, freq="monthly"):
    """
    Create a list of week starts between a start and end date.
    """
    if freq == "monthly":
        start_date = start_date.replace(day=1)
        delta = relativedelta(months=1)
        adjustment = delta - relativedelta(days=1)
    elif freq == "weekly":
        delta = relativedelta(days=7)
        adjustment = relativedelta(days=0)
    else:
        raise SystemExit(f"Error: {freq} is not a valid frequency.")
    if not end_date:
        end_date = datetime.today()
    date_list = []
    while start_date <= end_date:
        date_adjusted = start_date + adjustment
        date_list.append(date_adjusted.strftime("%Y-%m-%d"))
        start_date += delta
    return date_list


def parse_page(page_request):
    """
    Parses requested page.
    """
    results = dict.fromkeys(COURTS, 0)
    page = page_request.text.split()
    for i in range(len(page) - 1):
        if (page[i - 1][-1] == "%" or page[i - 1] == "Percent") & page[i + 1].isdigit():
            if page[i] in results.keys():
                results[page[i]] = page[i + 1]
            else:
                continue
        else:
            continue
    return results

def scrape_date_list(date_list, base_url, out_csv, append=False):
    results = []

    with Session() as session:
        for d in date_list:
            url = f"{base_url}-{d}"
            print(f"Attempting to download {d}.")
            
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 404:
                    print(f"😞 No data available for {d}. 😞")
                    continue
                response.raise_for_status()
            except RequestException as e:
                print(f"Network error downloading {d}: {e}")
                continue

            try:
                r = parse_page(response)
                r["date"] = d
                results.append(r)
            except Exception as e:
                print(f"Failed to parse data for {d}: {e}")

            sleep(1.5)
    
    if not results:
        print("No data collected. Can't write CSV.")
        return

    mode = "a" if append else "w"
    
    with open(out_csv, mode, newline="", encoding="utf-8") as f:
        writer = DictWriter(f, fieldnames=["date"] + COURTS)
        if not append:
            writer.writeheader()
        writer.writerows(results)
        print(f"Successfully saved {len(results)} rows to {out_csv}.")

def dates_from_csv(file, col_name="date"):
    dates = []
    with open(file, mode="r", encoding="utf-8") as f:
        reader = DictReader(f)  # Use DictReader if your CSV has a header name
        for row in reader:
            dates.append(row[col_name])
    
    return dates

def main():
    from pathlib import Path
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="start date", default="2020-10-24")
    parser.add_argument("-e", "--end", help="end date", default=datetime.today().strftime("%Y-%m-%d"))
    parser.add_argument("-p", "--path", help="path to directory in which results should be stored", default="./")
    args = parser.parse_args()

    try:
        default_start_date = datetime.strptime(DEFAULT_START_DATE, "%Y-%m-%d")
        start_date = datetime.strptime(args.start, "%Y-%m-%d")
    except:
        quit(f"Error: Provided start date '{args.start}' is not a valid date of the format YYYY-MM-DD.")
    
    try:
        end_date = datetime.strptime(args.end, "%Y-%m-%d")
    except:
        quit(f"Error: Provided end date '{args.end}' is not a valid date of the format YYYY-MM-DD.")

    if start_date >= end_date:
        quit(f"Error: Provided end date '{end_date}' is before provided start date '{start_date}.")
    
    if end_date < WEEKLY_END_DATE:
        weekly_end_date = start_date
    else:
        weekly_end_date = WEEKLY_END_DATE

    path = Path(args.path)
    try:
        path.mkdir(parents=False, exist_ok=True)
    except Exception as e:
        print(f"Error: Parent directory for '{path}' is missing. Exiting. {e}")
    
    weekly_file = path/"weekly_filings.csv"
    monthly_file = path/"monthly_filings.csv"

    weekly_dates_extant = []
    week_exists = False
    if weekly_file.exists():
        week_exists = True
        weekly_dates_extant = dates_from_csv(weekly_file)
    
    monthly_dates_extant = []
    month_exists = False
    if monthly_file.exists():
        month_exists = True
        monthly_dates_extant = dates_from_csv(monthly_file)

    week_list = create_date_list(start_date, end_date=weekly_end_date, freq="weekly")
    weeks = list(set(week_list) - set(weekly_dates_extant))
    scrape_date_list(weeks, base_url=WEEKLY_URL, out_csv=weekly_file, append = week_exists)
    month_list = create_date_list(start_date, end_date=end_date, freq="monthly")
    months = list(set(month_list) - set(monthly_dates_extant))
    scrape_date_list(months, base_url=MONTHLY_URL, out_csv=monthly_file, append = month_exists)