#!/bin/sh
# Resolve the thread whose first comment has this id. Pass -u to unresolve.
# usage: pr-resolve.sh [-u] OWNER/REPO N COMMENT_ID
set -eu
mutation=resolveReviewThread
if [ "${1:-}" = "-u" ]; then mutation=unresolveReviewThread; shift; fi
repo=$1; pr=$2; cid=$3
owner=${repo%%/*}; name=${repo##*/}
tid=$(gh api graphql -f query='
query($o:String!,$r:String!,$n:Int!){
  repository(owner:$o,name:$r){ pullRequest(number:$n){
    reviewThreads(first:100){ nodes{ id comments(first:1){ nodes{ databaseId } } } } } }
}' -f o="$owner" -f r="$name" -F n="$pr" \
 --jq ".data.repository.pullRequest.reviewThreads.nodes[] | select(.comments.nodes[0].databaseId == $cid) | .id")
[ -n "$tid" ] || { echo "pr-resolve: no thread whose first comment is $cid" >&2; exit 4; }
gh api graphql -f query="mutation(\$id:ID!){ $mutation(input:{threadId:\$id}){ thread{ isResolved } } }" \
  -f id="$tid" --jq '"\(.data | to_entries[0].value.thread.isResolved)"'
