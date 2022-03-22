from sys import argv
import json
import csv
import os
import requests


API_KEY = os.getenv("API_KEY")


def send_bcomp_invitation(school_name, emails):
    """sends bcomp invitation"""
    print("send_bcomp_invitation", school_name, emails, flush=True)
    res = requests.post(
        "https://api.eu.mailgun.net/v3/bcomp.id/messages",
        auth=("api", API_KEY),
        files=[
            ("attachment", open("attachments/poster-bcomp.jpg", "rb")),
            ("attachment", open("attachments/undangan-bcomp.pdf", "rb")),
        ],
        data={
            "from": "Brilliant Competition <announcement@bcomp.id>",
            "to": emails,
            "subject": "Undangan Brilliant Competition XIII",
            "template": "undangan-bcomp-xiii",
            "o:tag": ["invitation", "initial-campaign"],
            "h:X-Mailgun-Variables": json.dumps({"school_name": school_name}),
        },
    )
    print(res, flush=True)


def main(csvfile):
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        school, emails = row["school"], row["email"]
        emails = [e for e in emails.replace(" ", "").split("//") if e]
        print(i, "parsed from csv row", school, emails, flush=True)
        if emails:
            send_bcomp_invitation(school, emails)


if __name__ == "__main__":
    _, fname = argv
    with open(fname, newline="") as f:
        main(f)
