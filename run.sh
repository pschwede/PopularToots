#!/bin/bash

set -exo pipefail

cd $(readlink -f $(dirname $0))
source bin/activate
./top-post.py | \
	awk -F$'\t' '{print "#DailyHighscore! The winner of all local toots today is a "$1" scored one: "$2" Good night!"}' | \
	./toot.py
deactivate
