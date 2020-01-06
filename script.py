#!/usr/bin/env python3
import sys
from datetime import datetime as dt
from os import system
from signal import SIGINT, signal
from time import sleep

import bs4 as b
import requests as r
from emoji import emojize as e

LINK = "https://www.cnb.cz/cs/menova-politika/br-zapisy-z-jednani/Rozhodnuti-bankovni-rady-CNB-2013-1383828900000/"
LOC = "boarddecision-item"
TEXT = "Zveřejníme v lednu 2020"


def get_page_html():
    return r.get(LINK).text


def wipe_shell():
    system("clear")


def wait(interval):
    sleep(interval)


def display_time():
    print(dt.now().strftime("%H:%M:%S"))


# see https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
def handle_kill(sig, frame):
    print("CTRL+C pressed.")
    sys.exit(0)


def message_with_emoji(string: str, div: object, emoji=":smile:", replicate=0):
    em = ""
    if replicate > 0:
        for _ in range(replicate):
            em += emoji
    else:
        em = emoji

    message = f"{string}\n{em}\n{div.text}"
    print(e(message, use_aliases=True))


def check_if_docs_uploaded():
    soup = b.BeautifulSoup(get_page_html(), "lxml")
    div = soup.find_all("div", LOC)[3]

    if TEXT.lower() in div.text.lower().strip():
        message_with_emoji(
            "2013 FX interventions docs not published yet.",
            div,
            emoji=":disappointed_relieved:",
            replicate=10,
        )

    else:
        message_with_emoji(
            "2013 FX interventions docs are PUBLISHED.",
            div,
            emoji=":joy:",
            replicate=10,
        )


def job(interval):
    signal(SIGINT, handle_kill)
    while True:
        wipe_shell()
        display_time()
        check_if_docs_uploaded()
        wait(interval)


if __name__ == "__main__":
    job(600)
