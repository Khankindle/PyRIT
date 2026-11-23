# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
"""Utilities for measuring verbatim overlap in authorized text-extraction audits.

This module measures observable output similarity only. It cannot establish whether a
work appeared in training data, whether use was licensed, or whether a legal exception
applies. Use only works you own, are authorized to test, or may lawfully process.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


@dataclass(frozen=True)
class VerbatimOverlap:
    """Longest contiguous token match and its share of the reference passage."""

    matched_tokens: int
    reference_tokens: int
    reference_fraction: float


def measure_verbatim_overlap(reference: str, generated: str, *, min_tokens: int = 8) -> VerbatimOverlap:
    """Return longest contiguous token overlap, using case-insensitive Unicode tokens.

    The algorithm uses a rolling dynamic-programming row (O(n*m) time, O(m) memory).
    ``reference_fraction`` is zero when the longest match is shorter than ``min_tokens``.
    It is a screening signal, not a provenance or copyright determination.
    """
    if min_tokens < 1:
        raise ValueError("min_tokens must be at least 1")
    ref = [token.casefold() for token in _TOKEN_RE.findall(reference)]
    out = [token.casefold() for token in _TOKEN_RE.findall(generated)]
    previous = [0] * (len(out) + 1)
    longest = 0
    for token in ref:
        current = [0] * (len(out) + 1)
        for j, candidate in enumerate(out, start=1):
            if token == candidate:
                current[j] = previous[j - 1] + 1
                longest = max(longest, current[j])
        previous = current
    reported = longest if longest >= min_tokens else 0
    return VerbatimOverlap(
        matched_tokens=reported,
        reference_tokens=len(ref),
        reference_fraction=reported / len(ref) if ref and reported else 0.0,
    )


def build_authorized_probe(prefix: str, *, max_chars: int = 500) -> str:
    """Build a short continuation probe from a user-provided text prefix.

    Keep probes bounded and run only against an explicitly authorized model endpoint.
    This intentionally does not automate repeated extraction or jailbreak attempts.
    """
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    excerpt = prefix.strip()[-max_chars:]
    if not excerpt:
        raise ValueError("prefix must not be empty")
    return ("Continue the following passage exactly from where it stops. If you cannot, "
            "say so; do not invent a continuation.\n\n" + excerpt)
