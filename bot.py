# bot.py

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

import praw

from generator import generate_post, choose_next_interval_hours


STATE_PATH = Path("state.json")
LOG_PATH = Path("private_log.jsonl")


def now_utc():
    return datetime.now(timezone.utc)


def load_state():
    if not STATE_PATH.exists():
        return {
            "next_run_at": None,
            "last_post_title": None,
            "last_level": None,
        }

    with STATE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state):
    with STATE_PATH.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)


def parse_time(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def should_post(state):
    next_run_at = parse_time(state.get("next_run_at"))

    if next_run_at is None:
        return True

    return now_utc() >= next_run_at


def schedule_next(state):
    hours = choose_next_interval_hours()
    next_time = now_utc() + timedelta(hours=hours)

    state["next_run_at"] = next_time.isoformat()
    state["next_interval_hours"] = hours

    return hours, next_time


def log_private(post, next_interval_hours, next_time):
    entry = {
        "created_at": now_utc().isoformat(),
        "title": post["title"],
        "level": post["level"],
        "hidden_message": post["hidden_message"],
        "next_interval_hours": next_interval_hours,
        "next_run_at": next_time.isoformat(),
    }

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_env(name, required=True, default=None):
    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(f"Missing environment variable: {name}")

    return value


def publish_to_reddit(post):
    reddit = praw.Reddit(
        client_id=get_env("REDDIT_CLIENT_ID"),
        client_secret=get_env("REDDIT_CLIENT_SECRET"),
        username=get_env("REDDIT_USERNAME"),
        password=get_env("REDDIT_PASSWORD"),
        user_agent=get_env("REDDIT_USER_AGENT"),
    )

    subreddit_name = get_env("SUBREDDIT_NAME")
    subreddit = reddit.subreddit(subreddit_name)

    submission = subreddit.submit(
        title=post["title"],
        selftext=post["body"],
    )

    return submission.url


def main():
    state = load_state()

    if not should_post(state):
        print("Not time yet.")
        print("Next run at:", state.get("next_run_at"))
        return

    post = generate_post()
    next_interval_hours, next_time = schedule_next(state)

    live_mode = os.getenv("LIVE_MODE", "false").lower() == "true"

    print("Generated post")
    print("Title:", post["title"])
    print("Level:", post["level"])
    print("Hidden message:", post["hidden_message"])
    print("Next interval hours:", next_interval_hours)
    print("Next run at:", next_time.isoformat())
    print()
    print(post["body"][:1000])
    print()

    if live_mode:
        url = publish_to_reddit(post)
        print("Published:", url)
        state["last_post_url"] = url
    else:
        print("DRY RUN: not published to Reddit.")

    state["last_post_title"] = post["title"]
    state["last_level"] = post["level"]

    save_state(state)
    log_private(post, next_interval_hours, next_time)


if __name__ == "__main__":
    main()
