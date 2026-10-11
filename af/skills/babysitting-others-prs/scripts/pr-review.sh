#!/bin/sh
# Post a top-level review. Appends the reviewed-head marker. Refuses a closed PR.
# usage: pr-review.sh OWNER/REPO N approve|comment|request-changes BODYFILE MEASURED_SHA
# Exit 5 if the head moved since MEASURED_SHA: re-measure, do not post.
set -eu
dir=$(dirname "$0")
repo=$1; pr=$2; event=$3; bodyfile=$4; measured=$5
sha=$("$dir/pr-head.sh" "$repo" "$pr")
if [ "$sha" != "$measured" ]; then
  echo "pr-review: head moved, $measured -> $sha; re-measure before posting" >&2
  exit 5
fi
case "$event" in
  approve) ev=APPROVE ;;
  comment) ev=COMMENT ;;
  request-changes) ev=REQUEST_CHANGES ;;
  *) echo "pr-review: event must be approve, comment or request-changes" >&2; exit 2 ;;
esac
tmp=$(mktemp)
{ cat "$bodyfile"; printf '\n\n<!-- reviewed-head: %s -->\n' "$sha"; } > "$tmp"
gh api "repos/$repo/pulls/$pr/reviews" -f commit_id="$sha" -f event="$ev" \
  -F body=@"$tmp" --jq '"\(.state) \(.id) at \(.commit_id[0:12])"'
rm -f "$tmp"
