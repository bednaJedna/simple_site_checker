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
# see https://stackoverflow.com/questions/44078888/clickable-html-links-in-python-3-6-shell/53658415#53658415
SHELL_LINK = f"\u001b]8;;{LINK}\u001b\\CTRL+click HERE to get there.\u001b]8;;\u001b\\"


def get_page_html(link):
    return r.get(link).text


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

    message = f"{string}\n{em}\n{div.text}\n{SHELL_LINK}"
    print(e(message, use_aliases=True))


def get_soup(link):
    return b.BeautifulSoup(get_page_html(link), "lxml")


def get_element(soup: object, element_type: str, element_loc: str, counter: int):
    return soup.find_all(element_type, element_loc)[counter]


def check_if_docs_uploaded(
    link: str, element_type: str, element_loc: str, counter: int
):
    div = get_element(get_soup(link), element_type, element_loc, counter)

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


def job():
    signal(SIGINT, handle_kill)
    while True:
        wipe_shell()
        display_time()
        check_if_docs_uploaded(LINK, "div", LOC, 3)
        wait(600)


if __name__ == "__main__":
    job()
