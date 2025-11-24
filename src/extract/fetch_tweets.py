"""
ChargeNow Case Study – Robust Tweet Extraction

This script:
- Calls Twitter API v2 for #ChargeNow tweets
- Handles empty results
- Handles API schema changes safely
- Retries on network/429/source availability issues
- Logs useful metadata
- Returns raw JSON suitable for storage in Snowflake VARIANT or object storage
"""

import os
import time
import hashlib
import requests
from typing import Dict, Any, Optional

TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

def hash_user_id(uid: str) -> str:
    """Hash user_id using SHA-256 for anonymization."""
    return hashlib.sha256(uid.encode("utf-8")).hexdigest()


def fetch_tweets(
    start_time: str,
    end_time: str,
    retries: int = 5,
    backoff_seconds: int = 5
) -> Dict[str, Any]:
    """
    Fetch #ChargeNow tweets between start_time and end_time (ISO8601).
    Implements:
        - Retry logic
        - RateLimit handling (429)
        - Empty result handling
        - Logging
    """
    if not TOKEN:
        raise RuntimeError("TWITTER_BEARER_TOKEN not set in environment")

    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    params = {
        "query": "#ChargeNow",
        "start_time": start_time,
        "end_time": end_time,
        "tweet.fields": "created_at,public_metrics,entities,referenced_tweets",
        "expansions": "author_id",
        "user.fields": "location,public_metrics",
        "max_results": 100,
    }

    for attempt in range(1, retries + 1):
        try:
            print(f"[INFO] Calling Twitter API (Attempt {attempt}/{retries})…")
            resp = requests.get(url, headers=headers, params=params, timeout=30)

            # Rate limited
            if resp.status_code == 429:
                print("[WARN] Rate limited by Twitter API. Sleeping 60 seconds…")
                time.sleep(60)
                continue

            resp.raise_for_status()
            data = resp.json()

            # Handle empty result safely
            if "data" not in data or len(data["data"]) == 0:
                print(f"[INFO] No tweets found between {start_time} and {end_time}.")
                return {"data": [], "meta": data.get("meta", {}), "errors": None}

            print(f"[INFO] Extracted {len(data.get('data', []))} tweets.")
            return data

        except Exception as e:
            print(f"[ERROR] Twitter API call failed: {e}")

            if attempt == retries:
                print("[ERROR] Max retries reached. Failing extraction.")
                raise

            sleep_time = attempt * backoff_seconds
            print(f"[INFO] Retrying in {sleep_time} seconds…")
            time.sleep(sleep_time)

    # Should never reach this
    return {"data": [], "meta": {}, "errors": "Unexpected execution path"}


if __name__ == "__main__":
    print("This module is intended to be run via Airflow. Not standalone.")
