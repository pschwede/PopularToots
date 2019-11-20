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

python3 top-toot.py \
| tail -1 \
| awk -F$'\t' '{
	match($2, /@[^/]+/);
	print "#Rising! "substr($2, RSTART, RLENGTH)", your toot is currently pretty popular: "$2""
}' \
> "$LAST"

diff -s "$LAST" "$LAST.last" || python3 toot.py <"$LAST"

rm -f "$LAST.last"

deactivate

cd -
