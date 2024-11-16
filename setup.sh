#!/bin/bash

# 1. Remove .git directory if exists
echo "1. Removing .git directory..."
rm -rf .git
echo ".git directory removed"

# 2. Initialize git repository
echo "2. Initializing Git repository..."
git init
echo "Git repository initialized"

# 3. Remove .gitkeep files
echo "3. Removing .gitkeep files..."
rm -f data/raw/.gitkeep data/processed/.gitkeep
echo ".gitkeep files removed"

# 4. Update .gitignore
echo "4. Updating .gitignore file..."
echo "/data" >> .gitignore
echo ".gitignore file updated"

echo "All setup completed successfully!"