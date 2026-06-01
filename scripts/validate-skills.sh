#!/usr/bin/env sh
set -eu

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

frontmatter_value() {
    key=$1
    file=$2
    awk -v key="$key" '
        NR == 1 {
            if ($0 != "---") {
                exit
            }
            in_frontmatter = 1
            next
        }
        in_frontmatter && $0 == "---" {
            found_end = 1
            exit
        }
        in_frontmatter && !found && $0 ~ ("^" key ":[[:space:]]*") {
            sub("^[^:]+:[[:space:]]*", "")
            value = $0
            found = 1
        }
        END {
            if (found_end && found) {
                print value
            }
        }
    ' "$file"
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
retired_hits="$tmp_dir/retired_hits"
trailing_hits="$tmp_dir/trailing_hits"
renamed_hits="$tmp_dir/renamed_hits"
local_hits="$tmp_dir/local_hits"
object_paths="$tmp_dir/object_paths"
tracked_file="$tmp_dir/tracked"

: > "$skill_names_file"
: > "$published_markdown"
: > "$retired_hits"
: > "$trailing_hits"

if [ ! -d skills ]; then
    printf '%s\n' "Skill validation failed:"
    fail "Missing skills/ directory."
else
    skill_count=0
    for skill_dir in skills/*; do
        [ -d "$skill_dir" ] || continue
        skill_count=$((skill_count + 1))
        skill_file="$skill_dir/SKILL.md"
        folder_name=$(basename "$skill_dir")

        if [ ! -f "$skill_file" ]; then
            fail "Skill folder missing SKILL.md: $folder_name"
            continue
        fi

        first_line=$(sed -n '1p' "$skill_file")
        if [ "$first_line" != "---" ]; then
            fail "Skill missing opening frontmatter marker: $skill_file"
        fi
        if ! awk 'NR > 1 && $0 == "---" { found = 1; exit } END { exit found ? 0 : 1 }' "$skill_file"; then
            fail "Skill missing closing frontmatter marker: $skill_file"
        fi

        skill_name=$(frontmatter_value name "$skill_file")
        if [ -z "$skill_name" ]; then
            fail "Skill missing frontmatter name: $skill_file"
        elif [ "$skill_name" != "$folder_name" ]; then
            fail "Skill name mismatch: folder '$folder_name' has name '$skill_name'"
        fi
        printf '%s\n' "$folder_name" >> "$skill_names_file"

        description=$(frontmatter_value description "$skill_file")
        if [ -z "$description" ]; then
            fail "Skill missing frontmatter description: $skill_file"
        fi
    done

    if [ "$skill_count" -eq 0 ]; then
        fail "No skill directories found under skills/."
    fi
fi

if [ ! -f README.md ]; then
    fail "Missing README.md."
else
    while IFS= read -r skill_name; do
        [ -n "$skill_name" ] || continue
        if ! grep -Eq '^\|[[:space:]]*`'"$skill_name"'`[[:space:]]*\|' README.md; then
            fail "README skill map is missing skill: $skill_name"
        fi
    done < "$skill_names_file"

    mapped_skills="$tmp_dir/mapped_skills"
    sed -n 's/^|[[:space:]]*`\([^`][^`]*\)`[[:space:]]*|.*/\1/p' README.md > "$mapped_skills"
    while IFS= read -r mapped_skill; do
        [ -n "$mapped_skill" ] || continue
        if ! has_line "$mapped_skill" "$skill_names_file"; then
            fail "README skill map references missing skill: $mapped_skill"
        fi
    done < "$mapped_skills"
fi

[ -f README.md ] && printf '%s\n' "README.md" >> "$published_markdown"
[ -f AGENTS.md ] && printf '%s\n' "AGENTS.md" >> "$published_markdown"
if [ -d skills ]; then
    find skills -type f -name '*.md' | sort >> "$published_markdown"
fi

retired_pattern='public'/'caller|user'/'caller|caller path|caller-visible entry point|Agent-ready|[Nn]eeds decision|pressure examples?|pressure[- ]scenario|failure scenarios?|public entry point|(^|[^[:alnum:]_])seam([^[:alnum:]_]|$)'

while IFS= read -r file; do
    [ -n "$file" ] || continue
    if [ -f "$file" ]; then
        grep -nE "$retired_pattern" "$file" | sed "s|^|$file:|" >> "$retired_hits" || true
    fi
done < "$published_markdown"

if [ -s "$retired_hits" ]; then
    fail "Retired or conflicting vocabulary found:"
    sed 's/^/  /' "$retired_hits"
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

    blocked_path_names='andrej-karpathy-skills
matt-pocock-skills
codex-correctness
philosophies_discussions
superpowers'

    if [ -e sources ]; then
        fail "Ignored source-corpus directory exists locally: sources/"
    fi

    while IFS= read -r file; do
        [ -n "$file" ] || continue
        case "$file" in
            scripts/validate-skills.sh)
                continue
                ;;
        esac

        for name in $blocked_path_names; do
            case "$file" in
                "$name"|"$name"/*)
                    fail "Tracked source-corpus path remains: $file"
                    ;;
            esac
        done
    done < "$tracked_file"

    renamed_skill_pattern='thin-plan|github-work-tracking|manage-subagents'
    if git grep -n -I -E "$renamed_skill_pattern" -- . > "$renamed_hits" 2>"$tmp_dir/renamed_err"; then
        while IFS= read -r hit; do
            case "$hit" in
                scripts/validate-skills.sh:*)
                    continue
                    ;;
            esac
            fail "Stale renamed skill reference: $hit"
        done < "$renamed_hits"
    else
        code=$?
        if [ "$code" -ne 1 ]; then
            fail "git grep renamed skill scan failed: $(cat "$tmp_dir/renamed_err")"
        fi
    fi

    local_identifier_pattern='DESKTOP-|S-1-5-21|[A-Z]:\\|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|api[_-]?key[[:space:]]*[:=]|secret[[:space:]]*[:=]|token[[:space:]]*[:=]|password[[:space:]]*[:=]|BEGIN (RSA|OPENSSH|PRIVATE)'
    if git grep -n -I -E "$local_identifier_pattern" -- . > "$local_hits" 2>"$tmp_dir/local_err"; then
        while IFS= read -r hit; do
            case "$hit" in
                scripts/validate-skills.sh:*)
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

    history_output=$(git rev-list --all -- $blocked_path_names 2>&1) || {
        fail "Git history path scan failed: $history_output"
        history_output=''
    }
    if [ -n "$(printf '%s' "$history_output" | tr -d '[:space:]')" ]; then
        fail "Git history still references removed source-corpus paths: $(printf '%s' "$history_output" | tr '\n' ' ')"
    fi

    if git rev-list --objects --all > "$object_paths" 2>"$tmp_dir/object_err"; then
        while IFS=' ' read -r object path; do
            [ -n "${path:-}" ] || continue
            for name in $blocked_path_names; do
                case "$path" in
                    "$name"|"$name"/*|*/"$name"|*/"$name"/*)
                        fail "Git object path still references source corpus: $object $path"
                        ;;
                esac
            done
        done < "$object_paths"
    else
        fail "Git object path scan failed: $(cat "$tmp_dir/object_err")"
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
