import sys
import datetime
import urllib.parse
import urllib.request

from config import TELEGRAM_TOKEN, CHAT_ID, MODE
from content import MARKETING_IDEAS, SALES_TIPS
from formatter import format_marketing, format_sales

TBILISI_OFFSET = 4  # UTC+4


def today_index():
    now_utc = datetime.datetime.utcnow()
    now_tbilisi = now_utc + datetime.timedelta(hours=TBILISI_OFFSET)
    epoch = datetime.date(2024, 1, 1)
    return (now_tbilisi.date() - epoch).days


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        if resp.status != 200:
            body = resp.read().decode("utf-8")
            raise RuntimeError(f"Telegram error: {resp.status} {body}")


def main():
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Missing TELEGRAM_TOKEN or CHAT_ID", file=sys.stderr)
        sys.exit(1)

    idx = today_index()

    if MODE == "morning":
        # Morning: marketing campaign idea
        item = MARKETING_IDEAS[idx % len(MARKETING_IDEAS)]
        day_num = (idx % len(MARKETING_IDEAS)) + 1
        msg = format_marketing(item, day_num)
    else:
        # Evening: sales tip
        item = SALES_TIPS[idx % len(SALES_TIPS)]
        day_num = (idx % len(SALES_TIPS)) + 1
        msg = format_sales(item, day_num)

    send_message(TELEGRAM_TOKEN, CHAT_ID, msg)
    print(f"Sent [{MODE}] message — index {idx}")


if __name__ == "__main__":
    main()
