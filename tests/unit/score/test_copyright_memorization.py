from pyrit.score.copyright_memorization import build_authorized_probe, measure_verbatim_overlap


def test_overlap_is_case_insensitive_and_contiguous():
    result = measure_verbatim_overlap("The quick brown fox jumps over the hill", "A QUICK brown fox jumps over it", min_tokens=3)
    assert result.matched_tokens == 4
    assert result.reference_fraction == 4 / 8


def test_short_match_is_suppressed():
    result = measure_verbatim_overlap("one two three", "one two", min_tokens=3)
    assert result.matched_tokens == 0
    assert result.reference_fraction == 0


def test_probe_is_bounded():
    probe = build_authorized_probe("abcdefgh", max_chars=3)
    assert probe.endswith("fgh")
    assert "abc" not in probe
