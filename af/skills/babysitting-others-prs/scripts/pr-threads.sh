#!/bin/sh
# List review threads: comment id, resolved state, path, line, author, first line of body.
# usage: pr-threads.sh OWNER/REPO N [LOGIN]
set -eu
repo=$1; pr=$2; who=${3:-}
owner=${repo%%/*}; name=${repo##*/}
gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!){
  repository(owner:$o,name:$r){ pullRequest(number:$n){
    reviewThreads(first:100){ nodes{ id isResolved isOutdated path line
      comments(first:1){ nodes{ databaseId author{ login } body } } } } } }
}' -f o="$owner" -f r="$name" -F n="$pr" \
 --jq '.data.repository.pullRequest.reviewThreads.nodes[]
   | .comments.nodes[0] as $c
   | "\($c.databaseId)\t\(if .isResolved then "resolved" else "open" end)\t\(if .isOutdated then "outdated" else "current" end)\t\(.path):\(.line // "file")\t\($c.author.login)\t\($c.body | split("\n")[0])"' \
 | { if [ -n "$who" ]; then grep -F "	$who	" || true; else cat; fi; }
