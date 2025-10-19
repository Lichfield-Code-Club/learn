#!/bin/bash

# Set member name
MEMBER="$1"
REPO_DIR="$HOME/workspace/learn"
LOG_DIR="$HOME/workspace/learn/log"

echo "Hello World" > /tmp/push.log
cd "$REPO_DIR" || exit

mkdir -p ${LOG_DIR}

# Confirm current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$MEMBER" ]; then
    echo "Switching to branch: $MEMBER" >> ${LOG_DIR}/push.log
    git checkout "$MEMBER" || {
        echo "Branch $MEMBER not found. Aborting." >> ${LOG_DIR}/push.log
        exit 1
    }
fi

# Stage changes
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit." >> ${LOG_DIR}/push.log
else
    git commit -m "Update by $MEMBER on $(date '+%Y-%m-%d %H:%M')"
fi

# Push with upstream if needed
git push -u origin "$MEMBER"

echo "Changes pushed to branch: $MEMBER" >> ${LOG_DIR}/push.log

