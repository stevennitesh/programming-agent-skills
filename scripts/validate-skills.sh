#!/usr/bin/env sh
set -eu

# Skill frontmatter/schema validation is intentionally delegated to the Codex
# internal skill validator. This script only checks repo-specific integrity.

public_mode=0
verbose=0

for arg in "$@"; do
    case "$arg" in
        --public|--release)
            public_mode=1
            ;;
        -v|--verbose)
            verbose=1
            ;;
        -h|--help)
            printf '%s\n' "Usage: scripts/validate-skills.sh [--public|--release] [-v|--verbose]"
            exit 0
            ;;
        *)
            printf '%s\n' "Unknown argument: $arg" >&2
            printf '%s\n' "Usage: scripts/validate-skills.sh [--public|--release] [-v|--verbose]" >&2
            exit 2
            ;;
    esac
done

failures=0

fail() {
    failures=$((failures + 1))
    printf '%s\n' "- $*"
}

has_line() {
    grep -Fxq "$1" "$2"
}

skill_resource_references() {
    awk '
        {
            line = $0
            while (match(line, /`[^`]+`/)) {
                token = substr(line, RSTART + 1, RLENGTH - 2)
                if (token ~ /^(templates|references|scripts|examples)\/[^`[:space:]]+$/) {
                    print token
                }
                line = substr(line, RSTART + RLENGTH)
            }
        }
    ' "$1"
}

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
    printf '%s\n' "Not inside a Git repository." >&2
    exit 1
}
cd "$repo_root"

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT INT TERM

skill_names_file="$tmp_dir/skill_names"
published_markdown="$tmp_dir/published_markdown"
trailing_hits="$tmp_dir/trailing_hits"
local_hits="$tmp_dir/local_hits"
tracked_file="$tmp_dir/tracked"
ignored_tracked_file="$tmp_dir/ignored_tracked"
installed_diff="$tmp_dir/installed_diff"
engineering_contract_diff="$tmp_dir/engineering_contract_diff"

: > "$skill_names_file"
: > "$published_markdown"
: > "$trailing_hits"

if [ ! -d skills ]; then
    printf '%s\n' "Skill validation failed:"
    fail "Missing skills/ directory."
else
    skill_count=0
    for skill_dir in skills/current/* skills/experimental/* skills/extra/*; do
        [ -d "$skill_dir" ] || continue
        skill_count=$((skill_count + 1))
        skill_file="$skill_dir/SKILL.md"
        folder_name=$(basename "$skill_dir")

        if [ ! -f "$skill_file" ]; then
            fail "Skill folder missing SKILL.md: $folder_name"
            continue
        fi

        printf '%s\n' "$folder_name" >> "$skill_names_file"

        resource_refs="$tmp_dir/resource_refs_$folder_name"
        skill_resource_references "$skill_file" | sort -u > "$resource_refs"
        while IFS= read -r resource_ref; do
            [ -n "$resource_ref" ] || continue
            case "$resource_ref" in
                /*|../*|*/../*|*/..)
                    fail "Skill resource reference must stay inside the skill directory: $skill_file -> $resource_ref"
                    continue
                    ;;
            esac
            if [ ! -e "$skill_dir/$resource_ref" ]; then
                fail "Skill resource reference is missing: $skill_file -> $resource_ref"
            fi
        done < "$resource_refs"
    done

    if [ "$skill_count" -eq 0 ]; then
        fail "No skill directories found under skills/."
    fi
fi

if [ ! -f README.md ]; then
    fail "Missing README.md."
fi

for required_doc in AGENTS_PORTABLE_FALLBACK.md AGENTS_SKILL_PACK_GUIDE.md; do
    if [ ! -f "$required_doc" ]; then
        fail "Missing required agent instruction document: $required_doc"
    fi
done

for required_setup_doc in \
    AGENTS.md \
    docs/agents/issue-tracker.md \
    docs/agents/triage-labels.md \
    docs/agents/domain.md \
    docs/agents/engineering-contract.md \
    skills/current/setup-matt-pocock-skills/engineering-contract.md
do
    if [ ! -f "$required_setup_doc" ]; then
        fail "Missing required setup surface document: $required_setup_doc"
    fi
done

if [ -f docs/agents/engineering-contract.md ] && [ -f skills/current/setup-matt-pocock-skills/engineering-contract.md ]; then
    if ! diff -u skills/current/setup-matt-pocock-skills/engineering-contract.md docs/agents/engineering-contract.md > "$engineering_contract_diff"; then
        fail "docs/agents/engineering-contract.md differs from setup template:"
        sed 's/^/  /' "$engineering_contract_diff"
    fi
fi

if [ -f AGENTS_SKILL_PACK_GUIDE.md ]; then
    guide_skill_refs="$tmp_dir/guide_skill_refs"
    awk '
        {
            line = $0
            while (match(line, /`[^`]+`/)) {
                token = substr(line, RSTART + 1, RLENGTH - 2)
                if (token ~ /^[a-z0-9][a-z0-9-]*$/) {
                    print token
                }
                line = substr(line, RSTART + RLENGTH)
            }
        }
    ' AGENTS_SKILL_PACK_GUIDE.md | sort -u > "$guide_skill_refs"
    while IFS= read -r guide_skill; do
        [ -n "$guide_skill" ] || continue
        if ! has_line "$guide_skill" "$skill_names_file"; then
            fail "AGENTS_SKILL_PACK_GUIDE.md references missing skill: $guide_skill"
        fi
    done < "$guide_skill_refs"
fi

installed_skills_dir=${AGENT_SKILLS_DIR:-}
require_all_installed=${AGENT_SKILLS_REQUIRE_ALL:-0}
if [ -n "$installed_skills_dir" ]; then
    if [ ! -d "$installed_skills_dir" ]; then
        fail "AGENT_SKILLS_DIR does not exist or is not a directory: $installed_skills_dir"
    elif [ -d skills ]; then
        for installed_skill_dir in "$installed_skills_dir"/*; do
            [ -d "$installed_skill_dir" ] || continue
            installed_skill_name=${installed_skill_dir##*/}
            if ! has_line "$installed_skill_name" "$skill_names_file"; then
                fail "Installed AGENT_SKILLS_DIR contains unknown or stale skill: $installed_skill_name"
            fi
        done

        while IFS= read -r skill_name; do
            [ -n "$skill_name" ] || continue
            if [ -d "skills/current/$skill_name" ]; then
                repo_skill_dir="skills/current/$skill_name"
            elif [ -d "skills/experimental/$skill_name" ]; then
                repo_skill_dir="skills/experimental/$skill_name"
            elif [ -d "skills/extra/$skill_name" ]; then
                repo_skill_dir="skills/extra/$skill_name"
            else
                fail "Repo skill path not found for installed skill comparison: $skill_name"
                continue
            fi
            installed_skill_dir="$installed_skills_dir/$skill_name"
            if [ ! -d "$installed_skill_dir" ]; then
                if [ "$require_all_installed" = "1" ]; then
                    fail "Installed skill missing from AGENT_SKILLS_DIR: $skill_name"
                fi
                continue
            fi
            if diff -qr --exclude='*:Zone.Identifier' "$repo_skill_dir" "$installed_skill_dir" > "$installed_diff" 2>"$tmp_dir/installed_diff_err"; then
                :
            else
                diff_status=$?
                if [ "$diff_status" -eq 1 ]; then
                    fail "Installed skill differs from repo: $skill_name"
                    sed 's/^/  /' "$installed_diff"
                else
                    fail "Installed skill comparison failed for $skill_name: $(cat "$tmp_dir/installed_diff_err")"
                fi
            fi
        done < "$skill_names_file"
    fi
fi

[ -f README.md ] && printf '%s\n' "README.md" >> "$published_markdown"
[ -f AGENTS.md ] && printf '%s\n' "AGENTS.md" >> "$published_markdown"
[ -f AGENTS_PORTABLE_FALLBACK.md ] && printf '%s\n' "AGENTS_PORTABLE_FALLBACK.md" >> "$published_markdown"
[ -f AGENTS_SKILL_PACK_GUIDE.md ] && printf '%s\n' "AGENTS_SKILL_PACK_GUIDE.md" >> "$published_markdown"
if [ -d skills ]; then
    find skills -type f -name '*.md' | sort >> "$published_markdown"
fi
if [ -d docs/books ]; then
    find docs/books -type f -name '*.md' | sort >> "$published_markdown"
fi
if [ -d docs/agents ]; then
    find docs/agents -type f -name '*.md' | sort >> "$published_markdown"
fi
if [ -d docs/language ]; then
    find docs/language -type f -name '*.md' | sort >> "$published_markdown"
fi

while IFS= read -r file; do
    [ -n "$file" ] || continue
    if [ -f "$file" ]; then
        grep -nE '[[:blank:]]$' "$file" | sed "s|^|$file:|" >> "$trailing_hits" || true
    fi
done < "$published_markdown"

if [ -s "$trailing_hits" ]; then
    fail "Trailing whitespace found:"
    sed 's/^/  /' "$trailing_hits"
fi

if [ "$public_mode" -eq 1 ]; then
    git ls-files > "$tracked_file"
    if [ ! -s "$tracked_file" ]; then
        fail "No tracked files found."
    fi

    git ls-files -ci --exclude-standard > "$ignored_tracked_file"
    if [ -s "$ignored_tracked_file" ]; then
        fail "Tracked files match ignore rules:"
        sed 's/^/  /' "$ignored_tracked_file"
    fi

    local_identifier_pattern='DESKTOP-|S-1-5-21|[A-Z]:\\|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|api[_-]?key[[:space:]]*[:=]|secret[[:space:]]*[:=]|token[[:space:]]*[:=]|password[[:space:]]*[:=]|BEGIN (RSA|OPENSSH|PRIVATE)'
    if git grep -n -I -E "$local_identifier_pattern" -- . > "$local_hits" 2>"$tmp_dir/local_err"; then
        while IFS= read -r hit; do
            case "$hit" in
                scripts/validate-skills.sh:*)
                    continue
                    ;;
                *example.com*|*EXAMPLE.COM*|*correct-horse-battery-staple*)
                    continue
                    ;;
            esac
            fail "Potential local identifier or secret pattern: $hit"
        done < "$local_hits"
    else
        code=$?
        if [ "$code" -ne 1 ]; then
            fail "git grep local identifier scan failed: $(cat "$tmp_dir/local_err")"
        fi
    fi
fi

diff_check_output="$tmp_dir/diff_check_output"
if git diff --check > "$diff_check_output" 2>&1; then
    diff_check_status=0
else
    diff_check_status=$?
fi
if [ "$diff_check_status" -ne 0 ] || [ -s "$diff_check_output" ]; then
    fail "git diff --check reported whitespace or diff issues:"
    sed 's/^/  /' "$diff_check_output"
fi

if [ "$verbose" -eq 1 ]; then
    if [ -f "$tracked_file" ]; then
        tracked_count=$(wc -l < "$tracked_file" | tr -d '[:space:]')
        printf '%s\n' "Tracked files: $tracked_count"
    fi
    if [ -f "$skill_names_file" ]; then
        skill_count=$(wc -l < "$skill_names_file" | tr -d '[:space:]')
        printf '%s\n' "Skill folders: $skill_count"
    fi
fi

if [ "$failures" -ne 0 ]; then
    if [ "$public_mode" -eq 1 ]; then
        printf '%s\n' "Public readiness check failed."
    else
        printf '%s\n' "Skill validation failed."
    fi
    exit 1
fi

if [ "$public_mode" -eq 1 ]; then
    printf '%s\n' "Public readiness check passed."
else
    printf '%s\n' "Skill validation passed."
fi
