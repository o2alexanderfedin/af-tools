#!/bin/sh
# Start a resolvable review thread on the diff. Appends the reviewed-head marker.
# usage: pr-thread.sh OWNER/REPO N PATH LINE BODYFILE [START_LINE]
#        pr-thread.sh OWNER/REPO N PATH file BODYFILE
set -eu
dir=$(dirname "$0")
repo=$1; pr=$2; path=$3; line=$4; bodyfile=$5; start=${6:-}
sha=$("$dir/pr-head.sh" "$repo" "$pr")
tmp=$(mktemp)
{ cat "$bodyfile"; printf '\n\n<!-- reviewed-head: %s -->\n' "$sha"; } > "$tmp"
if [ "$line" = file ]; then
  gh api "repos/$repo/pulls/$pr/comments" -f path="$path" -f commit_id="$sha" \
    -f subject_type=file -F body=@"$tmp" --jq '"thread \(.id) on \(.path)"'
elif [ -n "$start" ]; then
  gh api "repos/$repo/pulls/$pr/comments" -f path="$path" -f commit_id="$sha" \
    -F line="$line" -f side=RIGHT -F start_line="$start" -f start_side=RIGHT \
    -F body=@"$tmp" --jq '"thread \(.id) on \(.path):\(.start_line)-\(.line)"'
else
  gh api "repos/$repo/pulls/$pr/comments" -f path="$path" -f commit_id="$sha" \
    -F line="$line" -f side=RIGHT -F body=@"$tmp" --jq '"thread \(.id) on \(.path):\(.line)"'
fi
rm -f "$tmp"
