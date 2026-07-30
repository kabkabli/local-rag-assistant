#!/usr/bin/env bash

REPORT="project_report.md"

echo "# Local RAG Assistant - Project Report" > "$REPORT"
echo "" >> "$REPORT"
echo "Generated: $(date)" >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Repository Information
##################################################

echo "## Repository Information" >> "$REPORT"
echo "" >> "$REPORT"

echo "Repository: $(basename "$(pwd)")" >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Git Status
##################################################


echo "## Git Status" >> "$REPORT"
echo "" >> "$REPORT"
echo '```' >> "$REPORT"
git status >> "$REPORT" 2>&1
echo '```' >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Recent Commits
##################################################

echo "## Recent Commits" >> "$REPORT"
echo "" >> "$REPORT"
echo '```' >> "$REPORT"
git log --oneline -20 >> "$REPORT" 2>/dev/null
echo '```' >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Branches
##################################################

echo "## Branches" >> "$REPORT"
echo "" >> "$REPORT"
echo '```' >> "$REPORT"
git branch -a >> "$REPORT" 2>/dev/null
echo '```' >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Project Tree
##################################################

echo "## Project Structure" >> "$REPORT"
echo "" >> "$REPORT"
echo '```text' >> "$REPORT"

find . \
    -path "./.git" -prune -o \
    -path "./.venv" -prune -o \
    -path "./venv" -prune -o \
    -path "./__pycache__" -prune -o \
    -path "./chroma_db" -prune -o \
    -path "./.pytest_cache" -prune -o \
    -print >> "$REPORT"

echo '```' >> "$REPORT"
echo "" >> "$REPORT"

##################################################
# Python Files
##################################################

echo "## Python Files" >> "$REPORT"
echo "" >> "$REPORT"

find . -name "*.py" | sort >> "$REPORT"

echo "" >> "$REPORT"

##################################################
# Python Statistics
##################################################

echo "## Statistics" >> "$REPORT"
echo "" >> "$REPORT"

FILES=$(find . -name "*.py" | wc -l)

LINES=$(find . -name "*.py" -exec cat {} \; | wc -l)

echo "- Python Files: $FILES" >> "$REPORT"
echo "- Total Lines: $LINES" >> "$REPORT"

echo "" >> "$REPORT"

##################################################
# TODO / FIXME
##################################################

echo "## TODO / FIXME" >> "$REPORT"
echo "" >> "$REPORT"

grep -RInE "TODO|FIXME|HACK" . \
--include="*.py" \
--exclude-dir=.git \
--exclude-dir=.venv \
--exclude-dir=venv \
>> "$REPORT" 2>/dev/null

echo "" >> "$REPORT"

##################################################
# Requirements
##################################################

echo "## Requirements" >> "$REPORT"
echo "" >> "$REPORT"

for f in requirements.txt pyproject.toml Pipfile; do
    if [ -f "$f" ]; then
        echo "### $f" >> "$REPORT"
        echo '```' >> "$REPORT"
        cat "$f" >> "$REPORT"
        echo '```' >> "$REPORT"
        echo "" >> "$REPORT"
    fi
done

##################################################
# README
##################################################

if [ -f README.md ]; then
echo "## README" >> "$REPORT"
echo "" >> "$REPORT"
echo '```markdown' >> "$REPORT"
cat README.md >> "$REPORT"
echo '```' >> "$REPORT"
echo "" >> "$REPORT"
fi

##################################################
# Module Summary
##################################################

echo "## Python Modules" >> "$REPORT"
echo "" >> "$REPORT"

find . -name "*.py" | while read file
do
    echo "### $file" >> "$REPORT"

    grep -E "^class " "$file" >> "$REPORT"

    grep -E "^def " "$file" >> "$REPORT"

    echo "" >> "$REPORT"
done

##################################################
# Largest Files
##################################################

echo "## Largest Python Files" >> "$REPORT"
echo "" >> "$REPORT"

find . -name "*.py" -exec wc -l {} \; | sort -nr | head -20 >> "$REPORT"

echo "" >> "$REPORT"

##################################################
# Finish
##################################################

echo "---" >> "$REPORT"
echo "" >> "$REPORT"
echo "Report generation complete." >> "$REPORT"

echo ""
echo "==========================================="
echo "Report created:"
echo "$REPORT"
echo "==========================================="
