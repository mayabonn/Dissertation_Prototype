import os
import sys
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timezone

# Paths
BASE_DIR     = os.path.dirname(__file__)
ROOT_DIR     = os.path.join(BASE_DIR, "..")
ACCOUNTS_TXT = os.path.join(ROOT_DIR, "data", "accounts.txt")
OUTPUT_CSV   = os.path.join(ROOT_DIR, "data", "raw_posts.csv")
ERRORS_LOG   = os.path.join(ROOT_DIR, "data", "errors.log")
ENV_PATH     = os.path.join(ROOT_DIR, ".env")

load_dotenv(ENV_PATH)
ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
ACCOUNT_ID   = os.getenv('INSTAGRAM_ACCOUNT_ID')

if not ACCESS_TOKEN or not ACCOUNT_ID:
    raise EnvironmentError("Missing INSTAGRAM_ACCESS_TOKEN or INSTAGRAM_ACCOUNT_ID in .env")

BASE_URL    = "https://graph.facebook.com/v24.0"
CUTOFF_DATE = datetime(2025, 5, 1, tzinfo=timezone.utc)  # fixed window: May 2025 – May 2026


def load_accounts(filepath):
    """
    Loads Instagram usernames from accounts.txt.
    Skips comment lines and blank lines.
    Usernames not printed for ethical reasons.
    """
    with open(filepath, "r") as f:
        return [
            line.strip().lstrip("@")
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]


def get_account_data(username):
    """
    Collects posts from the last 12 months for one account.
    Uses Business Discovery endpoint with pagination.
    """
    url    = f"{BASE_URL}/{ACCOUNT_ID}"
    params = {
        "fields": (
            f"business_discovery.username({username})"
            f"{{username,followers_count,"
            f"media{{caption,like_count,comments_count,timestamp}}}}"
        ),
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        msg = str(e)
        print(f"  [SKIPPED] {msg}")
        with open(ERRORS_LOG, "a") as f:
            f.write(f"{datetime.now(timezone.utc)} | {username} | {msg}\n")
        return []

    if "error" in data:
        msg = data['error'].get('message', 'unknown')
        print(f"  [SKIPPED] {msg}")
        with open(ERRORS_LOG, "a") as f:
            f.write(f"{datetime.now(timezone.utc)} | {username} | {msg}\n")
        return []

    discovery  = data.get("business_discovery", {})
    followers  = discovery.get("followers_count", 0)
    media_data = discovery.get("media", {})
    posts      = []
    stop       = False

    while media_data and not stop:
        for post in media_data.get("data", []):
            ts = post.get("timestamp", "")
            if ts:
                if datetime.fromisoformat(ts.replace("Z", "+00:00")) < CUTOFF_DATE:
                    stop = True
                    break
            posts.append({
                "username":        username,
                "followers_count": followers,
                "caption":         post.get("caption", ""),
                "like_count":      post.get("like_count", 0),
                "comments_count":  post.get("comments_count", 0),
                "timestamp":       ts
            })

        next_page = media_data.get("paging", {}).get("next")
        if next_page and not stop:
            time.sleep(1)
            try:
                response = requests.get(next_page)
                response.raise_for_status()
                media_data = response.json()
            except requests.exceptions.RequestException as e:
                msg = str(e)
                print(f"  [PAGINATION ERROR] {msg}")
                with open(ERRORS_LOG, "a") as f:
                    f.write(f"{datetime.now(timezone.utc)} | {username} | pagination | {msg}\n")
                break
        else:
            break

    print(f"  Collected {len(posts)} posts ({followers:,} followers)")
    return posts


def load_existing_data(filepath):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        return df, set(df["username"].unique())
    return pd.DataFrame(), set()


def save_progress(posts, output_path):
    """Saves collected posts to CSV immediately after each account."""
    if not posts:
        return
    df_new = pd.DataFrame(posts)
    if os.path.exists(output_path):
        df_existing = pd.read_csv(output_path)
        df_merged   = pd.concat([df_existing, df_new], ignore_index=True)
        df_merged.drop_duplicates(subset=["username", "timestamp"], keep="first", inplace=True)
        df_merged.to_csv(output_path, index=False)
    else:
        df_new.to_csv(output_path, index=False)


def run_collection(accounts, already_collected, part_label):
    new_accounts = [a for a in accounts if a not in already_collected]
    successful   = 0
    failed       = 0

    print(f"── {part_label} ({len(new_accounts)} accounts to collect) ──")

    for i, username in enumerate(new_accounts, 1):
        print(f"[{i}/{len(new_accounts)}]", end=" ")
        posts = get_account_data(username)
        if posts:
            save_progress(posts, OUTPUT_CSV)
            successful += 1
        else:
            failed += 1
        time.sleep(2)

    df_final = pd.read_csv(OUTPUT_CSV) if os.path.exists(OUTPUT_CSV) else pd.DataFrame()
    print(f"Successful: {successful} | Failed: {failed}")
    print(f"Total posts: {len(df_final):,} | Total accounts: {df_final['username'].nunique()} | Shape: {df_final.shape}")


def run_part(part):
    print("=" * 50)
    print(f"INSTAGRAM DATA COLLECTION — PART {part}")
    print("=" * 50)
    all_accounts           = load_accounts(ACCOUNTS_TXT)
    mid                    = len(all_accounts) // 2
    accounts               = all_accounts[:mid] if part == 1 else all_accounts[mid:]
    df_existing, collected = load_existing_data(OUTPUT_CSV)
    run_collection(accounts, collected, f"Part {part}")
    print("=" * 50)
    print(f"PART {part} DONE")
    print("=" * 50)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_part(int(sys.argv[1]))
    else:
        run_part(1)
        print("\nWaiting 10 seconds before Part 2...\n")
        time.sleep(10)
        run_part(2)