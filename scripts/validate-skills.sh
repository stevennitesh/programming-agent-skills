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

frontmatter_yaml_warnings() {
    awk '
        NR == 1 {
            if ($0 != "---") {
                exit
            }
            in_frontmatter = 1
            next
        }
        in_frontmatter && $0 == "---" {
            exit
        }
        in_frontmatter && $0 ~ /^[[:alnum:]_-]+:[[:space:]]*/ {
            key = $0
            sub(/:.*/, "", key)
            value = $0
            sub(/^[^:]+:[[:space:]]*/, "", value)
            if ((key == "name" || key == "description") && value !~ /^["\047]/ && value ~ /:[[:space:]]/) {
                printf "%s:%d: frontmatter %s value contains colon-space and must be quoted for YAML: %s\n", FILENAME, NR, key, $0
            }
        }
    ' "$1"
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
retired_hits="$tmp_dir/retired_hits"
trailing_hits="$tmp_dir/trailing_hits"
renamed_hits="$tmp_dir/renamed_hits"
local_hits="$tmp_dir/local_hits"
object_paths="$tmp_dir/object_paths"
tracked_file="$tmp_dir/tracked"
installed_diff="$tmp_dir/installed_diff"

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
        yaml_warnings=$(frontmatter_yaml_warnings "$skill_file")
        if [ -n "$yaml_warnings" ]; then
            fail "Skill frontmatter is not safe YAML:"
            printf '%s\n' "$yaml_warnings" | sed 's/^/  /'
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
else
    if ! grep -Eq 'unavailable skills should not be simulated|should not simulate it' README.md; then
        fail "README must explain that unavailable skills should not be simulated."
    fi
    if ! grep -Fq 'AGENT_SKILLS_DIR' README.md; then
        fail "README install docs must use AGENT_SKILLS_DIR instead of an agent-specific skills path."
    fi
    if ! grep -Fq '~/.codex/skills' README.md; then
        fail "README install docs must remind Codex users of the common ~/.codex/skills default."
    fi
    if ! grep -Fq '~/.claude/skills' README.md; then
        fail "README install docs must remind Claude Code users of the common ~/.claude/skills default."
    fi
    if ! grep -Fq 'cp -R skills/* "$AGENT_SKILLS_DIR/"' README.md; then
        fail 'README is missing the full router-compatible install command: cp -R skills/* "$AGENT_SKILLS_DIR/"'
    fi
    if ! grep -Eq 'installed[- ]copy|installed copy' README.md; then
        fail "README must explain AGENT_SKILLS_DIR installed-copy validation."
    fi
    if ! grep -Fq 'smaller starter setup with the router' README.md; then
        fail 'README must mark the smaller starter setup as using the router and core local skills.'
    fi

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

    readme_route_skills="$tmp_dir/readme_route_skills"
    awk '
        /^Typical paths:/ {
            in_paths = 1
            next
        }
        in_paths && /^## / {
            in_paths = 0
        }
        in_paths {
            line = $0
            while (match(line, /`[^`]+`/)) {
                token = substr(line, RSTART + 1, RLENGTH - 2)
                if (token ~ /^[a-z0-9][a-z0-9-]*$/) {
                    print token
                }
                line = substr(line, RSTART + RLENGTH)
            }
        }
    ' README.md | sort -u > "$readme_route_skills"
    while IFS= read -r route_skill; do
        [ -n "$route_skill" ] || continue
        if ! has_line "$route_skill" "$skill_names_file"; then
            fail "README Typical paths references missing skill: $route_skill"
        fi
    done < "$readme_route_skills"
fi

if [ -e AGENTS.md ]; then
    fail "Root AGENTS.md should not exist in this repo; use AGENTS_PORTABLE_FALLBACK.md or AGENTS_SKILL_PACK_ROUTER.md."
fi

for required_doc in AGENTS_PORTABLE_FALLBACK.md AGENTS_SKILL_PACK_ROUTER.md; do
    if [ ! -f "$required_doc" ]; then
        fail "Missing required agent instruction document: $required_doc"
    fi
done

if [ -f AGENTS_SKILL_PACK_ROUTER.md ]; then
    if ! grep -Eq 'unavailable.*do not simulate|do not simulate.*unavailable' AGENTS_SKILL_PACK_ROUTER.md; then
        fail "AGENTS_SKILL_PACK_ROUTER.md must say unavailable skills should not be simulated."
    fi

    router_skill_refs="$tmp_dir/router_skill_refs"
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
    ' AGENTS_SKILL_PACK_ROUTER.md | sort -u > "$router_skill_refs"
    while IFS= read -r router_skill; do
        [ -n "$router_skill" ] || continue
        if ! has_line "$router_skill" "$skill_names_file"; then
            fail "AGENTS_SKILL_PACK_ROUTER.md references missing skill: $router_skill"
        fi
    done < "$router_skill_refs"
fi

installed_skills_dir=${AGENT_SKILLS_DIR:-}
if [ -n "$installed_skills_dir" ]; then
    if [ ! -d "$installed_skills_dir" ]; then
        fail "AGENT_SKILLS_DIR does not exist or is not a directory: $installed_skills_dir"
    elif [ -d skills ]; then
        while IFS= read -r skill_name; do
            [ -n "$skill_name" ] || continue
            repo_skill_dir="skills/$skill_name"
            installed_skill_dir="$installed_skills_dir/$skill_name"
            if [ ! -d "$installed_skill_dir" ]; then
                fail "Installed skill missing from AGENT_SKILLS_DIR: $skill_name"
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
[ -f AGENTS_PORTABLE_FALLBACK.md ] && printf '%s\n' "AGENTS_PORTABLE_FALLBACK.md" >> "$published_markdown"
[ -f AGENTS_SKILL_PACK_ROUTER.md ] && printf '%s\n' "AGENTS_SKILL_PACK_ROUTER.md" >> "$published_markdown"
if [ -d skills ]; then
    find skills -type f -name '*.md' | sort >> "$published_markdown"
fi

retired_pattern='public'/'caller|user'/'caller|caller path|caller-visible entry point|Agent-ready|[Nn]eeds decision|pressure examples?|pressure[- ]scenario|failure scenarios?|public entry point|dirty[ -]trees?|dirty state|(^|[^[:alnum:]_])seam([^[:alnum:]_]|$)'

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
