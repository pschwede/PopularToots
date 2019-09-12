#!/bin/bash

set -exo pipefail

cd "$(readlink -f "$(dirname $0)")"

source .env/bin/activate

LAST="$(basename "$0").last"

avail_last=false
if [ -e "$LAST" ]; then
	avail_last=true
	mv "$LAST" "$LAST.last"
fi

./top-toot.py \
| head -1 \
| awk -F$'\t' '{
	match($0, /@[^/]+/);
	print "#DailyHighscore! "substr($0, RSTART, RLENGTH)", the winner of all local toots today is: "$2" Good night!"
}' \
> "$LAST"

diff -s "$LAST" "$LAST.last" || python3 toot.py <"$LAST"

rm -f "$LAST.last"

deactivate

cd -
