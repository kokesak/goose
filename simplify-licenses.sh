#!/bin/bash
# simplify-licenses.sh
#
# Reads SPDX license expressions (one per line) from stdin or a file,
# flattens AND, deduplicates (accounting for OR-item reordering),
# sorts, and outputs the formatted License field block for RPM spec files.
#
# Usage:
#   ./simplify-licenses.sh < licenses.txt
#   ./simplify-licenses.sh licenses.txt
#   cargo license --json | jq -r '.[].license' | ./simplify-licenses.sh
#
# Input lines may optionally be prefixed with '#' (comment style).
# Empty and blank lines are skipped.

set -euo pipefail

input="${1:--}"

awk '
{
    # Strip leading/trailing whitespace
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")

    # Strip leading # and any whitespace after it
    sub(/^#[[:space:]]*/, "")

    # Strip again after removing #
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")

    # Skip empty lines
    if ($0 == "") next

    # Split the line by " AND " to flatten top-level AND expressions.
    # Each piece becomes a separate clause.
    n = split($0, parts, / AND /)

    for (i = 1; i <= n; i++) {
        clause = parts[i]

        # Strip leading/trailing whitespace from the clause
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", clause)

        # Strip outer parentheses if present
        if (match(clause, /^\(.*\)$/)) {
            inner = substr(clause, 2, length(clause) - 2)
            # Only strip if the parens are truly the outermost balanced pair.
            # Check by ensuring no unmatched parens remain inside.
            depth = 0
            balanced = 1
            for (c = 1; c <= length(inner); c++) {
                ch = substr(inner, c, 1)
                if (ch == "(") depth++
                else if (ch == ")") depth--
                if (depth < 0) { balanced = 0; break }
            }
            if (balanced && depth == 0) {
                clause = inner
            }
        }

        # Normalize for deduplication:
        # Split by " OR ", sort items alphabetically, rejoin.
        m = split(clause, oritems, / OR /)
        # Bubble sort the OR items
        for (j = 1; j <= m; j++) {
            for (k = j + 1; k <= m; k++) {
                if (oritems[j] > oritems[k]) {
                    tmp = oritems[j]
                    oritems[j] = oritems[k]
                    oritems[k] = tmp
                }
            }
        }
        canonical = oritems[1]
        for (j = 2; j <= m; j++) {
            canonical = canonical " OR " oritems[j]
        }

        # Deduplicate: only keep first occurrence
        if (!(canonical in seen)) {
            seen[canonical] = 1
            count++
            clauses[count] = canonical
        }
    }
}
END {
    # Sort all unique clauses alphabetically
    for (i = 1; i <= count; i++) {
        for (j = i + 1; j <= count; j++) {
            if (clauses[i] > clauses[j]) {
                tmp = clauses[i]
                clauses[i] = clauses[j]
                clauses[j] = tmp
            }
        }
    }

    # Format and output
    for (i = 1; i <= count; i++) {
        # Wrap in parentheses if clause contains OR
        if (index(clauses[i], " OR ") > 0) {
            formatted = "(" clauses[i] ")"
        } else {
            formatted = clauses[i]
        }

        if (i == 1) {
            printf "    %s\n", formatted
        } else {
            printf "    AND %s\n", formatted
        }
    }
}
' "$input"
