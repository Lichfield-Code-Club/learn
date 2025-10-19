#!/bin/bash

# Set member name
MEMBER="$1"
REPO_DIR="$HOME/workspace/learn"
REPO_URL="https://github.com/Lichfield-Code-Club/learn.git"

mkdir -p £{REPO_DIR}
# Remove existing repo
if [ -d "$REPO_DIR" ]; then
    echo "Removing existing repo at $REPO_DIR"
    rm -rf "$REPO_DIR"
fi

# Clone fresh
echo "Cloning repo..."
git clone "$REPO_URL" "$REPO_DIR"

cd "$REPO_DIR" || exit

# Check if remote branch exists
if git ls-remote --exit-code --heads origin "$MEMBER" > /dev/null; then
    echo "Branch '$MEMBER' exists remotely. Checking out..."
    git checkout "$MEMBER"
else
    echo "Branch '$MEMBER' does not exist. Creating and pushing..."
    git checkout -b "$MEMBER"
    git push -u origin "$MEMBER"
fi

echo "Repo ready on branch: $MEMBER"

