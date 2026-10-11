#!/bin/sh
# Print a PR's head SHA. Exit 3 if the PR is not open.
# usage: pr-head.sh OWNER/REPO N
set -eu
repo=$1; pr=$2
state=$(gh api "repos/$repo/pulls/$pr" --jq '.state + " " + (.merged_at // "null")')
case "$state" in
  "open null") ;;
  *) echo "pr-head: $repo#$pr is not open ($state)" >&2; exit 3 ;;
esac
gh api "repos/$repo/pulls/$pr" --jq .head.sha
