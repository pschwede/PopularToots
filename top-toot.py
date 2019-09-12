#!/usr/bin/env python3

from typing import Optional, Tuple, Any
import re
import requests
from collections import Counter
from os import path
from datetime import datetime, timedelta, tzinfo
from math import inf
from mastodon import Mastodon
from sys import stderr
from time import sleep

from config import APIBASE, USERSECRET

TWITTERNAME = re.compile(r'(@[a-zA-Z0-9@-_]+)')
HASHTAG = re.compile(r'(#[a-zA-Z0-9#-_]+)')
HTMLFAVS = re.compile(r'(?<=<i class="fa fa-star"></i><span>)[0-9]+')
REQLIMIT = inf


class GMT1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "Europe/Berlin"


def get_public_hashtags_mastodon(url: str) -> Counter:
    """
    Count the most used hashtags.
    """
    counter = Counter()

    timeline = requests.get("https://%s/api/v1/timelines/public" % url)
    for entry in timeline.json():
        counter.update(HASHTAG.findall(entry.content))

    return counter


def get_local_timeline_favs_mastodon(
        offset_hours: int = 4,
        interval_days: int = 1,
        interval_hours: int = 0
        ) -> Tuple[Tuple[int, Optional[Any]],Tuple[int, Optional[Any]]]:
    """
    Extract the winning toots from the public local timeline.
    """
    if not path.exists(USERSECRET):
        raise Exception("Missing USERSECRET")
    mastodon = Mastodon(
            access_token = USERSECRET,
            api_base_url = APIBASE,
            ratelimit_method="pace"
            )
    MAXAGE = offset_hours + interval_days*24 + interval_hours
    START = datetime.now(tz=GMT1())
    YESTERDAY = START - timedelta(hours=MAXAGE)
    RECENTLY = START - timedelta(hours=offset_hours)

    highscore = (0, None)
    highgain = (0, None)
    req_count = 0
    toot_count = 0
    age = 0.

    max_id = None
    while age <= MAXAGE and req_count < REQLIMIT:
        timeline = mastodon.timeline_local(max_id=max_id, limit=40)
        req_count += 1

        for toot in timeline:
            toot_count += 1
            age = (START - toot.created_at) / timedelta(hours=1)
            max_id = toot.id if max_id is None else min(max_id, toot.id)

            if age < offset_hours:
                continue
            if age > MAXAGE:
                break

            score = toot.reblogs_count * 2
            score += toot.favourites_count
            score += toot.replies_count * 0
            if highscore[0] < score:
                highscore = (score, toot)

            gain = score / age  # pt/hr
            if highgain[0] < gain:
                highgain = (gain, toot)

        dt = (datetime.now(tz=GMT1()) - START).total_seconds()
        print((
            "%.0f%%\tAvg. rate: %.1f "
            "requests (=%.1f toots) per second.") % (
                100 * age / MAXAGE,
                req_count / dt,
                toot_count / dt
                ), file=stderr)

    print("Total number of toots analyzed: %d" % req_count, file=stderr)
    print("Total seconds required: %d" % (
        datetime.now(tz=GMT1()) - START).total_seconds(), file=stderr)
    return (highscore, highgain)


def main():
    """
    Print highest score and highest gain (in pt/hr) and their toots (url and content).
    """
    highscore, highgain = get_local_timeline_favs_mastodon()

    score, toot = highscore
    print("%s\t%s\t%s" % (score, toot.url, toot.content))

    gain, toot = highgain
    print("%.2f\t%s\t%s" % (gain, toot.url, toot.content))


if __name__ == "__main__":
    main()
