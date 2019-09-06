#!/usr/bin/env python3

import re
import requests
from collections import Counter
from os import path
from datetime import datetime, timedelta, tzinfo
from config import APIBASE, USERSECRET
from mastodon import Mastodon


TWITTERNAME = re.compile(r'(@[a-zA-Z0-9@-_]+)')
HASHTAG = re.compile(r'(#[a-zA-Z0-9#-_]+)')
HTMLFAVS = re.compile(r'(?<=<i class="fa fa-star"></i><span>)[0-9]+')


class GMT1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1)
    def dst(self, dt):
        return timedelta(0)
    def tzname(self,dt):
        return "Europe/Berlin"

def get_public_hashtags_mastodon(url):
    counter = Counter()

    timeline = requests.get("https://%s/api/v1/timelines/public" % url)
    for entry in timeline.json():
        counter.update(HASHTAG.findall(entry.content))

    return counter

def get_local_timeline_favs_mastodon():
    if not path.exists(USERSECRET):
        raise Exception("Missing USERSECRET")
    mastodon = Mastodon(
            access_token = USERSECRET,
            api_base_url = APIBASE,
            ratelimit_method="pace"
            )
    yesterday = datetime.now(tz=GMT1()) - timedelta(days=1)
    highscore = (0, None)
    max_id = None
    while True:
        timeline = mastodon.timeline_local(max_id)
        for toot in timeline:
            if yesterday >= toot.created_at:
                return highscore
            if max_id is None:
                max_id = toot.id
            else:
                max_id = min(max_id, toot.id)
            score = toot.reblogs_count * 2 + toot.favourites_count
            if highscore[0] < score:
                highscore = (score, toot)
    return highscore

if __name__ == "__main__":
    score, toot = get_local_timeline_favs_mastodon()
    print("%s\t%s\t%s" % (score, toot.url, toot.content))
