import pytest
from app.services.game_service import _evaluate, _calculate_score, COLORS


def test_evaluate_all_correct():
    cp, cc = _evaluate("ABCD", "ABCD")
    assert cp == 4
    assert cc == 0


def test_evaluate_none_correct():
    cp, cc = _evaluate("ABCD", "EFEF")
    # A,B,C,D vs E,F,E,F — no match at all if ABCD has no E or F
    assert cp == 0
    assert cc == 0


def test_evaluate_color_only():
    # ABCD vs DCBA — 0 in position, 4 correct colors
    cp, cc = _evaluate("ABCD", "DCBA")
    assert cp == 0
    assert cc == 4


def test_evaluate_partial():
    cp, cc = _evaluate("AABB", "ABCD")
    # Position: A==A (pos 0), B!=B? pos1: A vs B no, pos2: B vs C no, pos3: B vs D no → cp=1
    assert cp == 1
    # Color: A:min(2,1)=1, B:min(2,1)=1 → total color matches=2, subtract cp=1 → cc=1
    assert cc == 1


def test_evaluate_repeated_colors_no_overcount():
    # Secret has two A's, guess has three A's. Extra A in guess must not overcount.
    cp, cc = _evaluate("AABC", "AAAD")
    # Positions: A==A (0), A==A (1) => 2
    assert cp == 2
    # Only one additional A is available in secret after exact matches: no extra color-only hits here.
    assert cc == 0


def test_evaluate_repeated_colors_all_color_hits():
    # Same multiset of colors, all misplaced
    cp, cc = _evaluate("AABB", "BBAA")
    assert cp == 0
    assert cc == 4


def test_calculate_score_win():
    score = _calculate_score(1, True)
    assert score == 1000


def test_calculate_score_loss():
    score = _calculate_score(10, False)
    assert score == 0


def test_calculate_score_last_attempt():
    score = _calculate_score(10, True)
    assert score == 100
