#!/bin/sh
# Reply inside an existing thread.
# usage: pr-reply.sh OWNER/REPO N COMMENT_ID BODYFILE
set -eu
repo=$1; pr=$2; cid=$3; bodyfile=$4
gh api "repos/$repo/pulls/$pr/comments/$cid/replies" -F body=@"$bodyfile" --jq '"reply \(.id)"'
