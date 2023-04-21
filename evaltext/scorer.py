import re
from typing import Callable, Optional, List


class S:
    """Scorer for a text."""

    text: str
    _results: List[float]
    _weights: List[float]

    def __init__(self, text):
        self.text = text
        self._weights = []
        self._results = []

    def _add_result(self, w: float, r: float):
        self._weights.append(w)
        self._results.append(r)

    def score(self) -> float:
        return sum(self._results) / sum(self._weights)

    def contains(self, search: str, max_count: Optional[int] = None, ignore_case: bool = False, w: float = 1) -> "S":
        result_w = 0
        t = self.text
        s = search
        if ignore_case:
            t = self.text.lower()
            s = search.lower()
        cnt = t.count(s)
        if cnt > 0:
            if max_count is None or cnt <= max_count:
                result_w = w
        self._add_result(w, result_w)
        return self

    def not_contains(self, search: str, ignore_case: bool = False, greater_than: int = 0, w: float = 1) -> "S":
        result_w = 0
        t = self.text
        s = search
        if ignore_case:
            t = self.text.lower()
            s = search.lower()
        if t.count(s) <= greater_than:
            result_w = w
        self._add_result(w, result_w)
        return self

    def contains_regex(self, s, w: float = 1) -> "S":
        result_w = 0
        if re.search(s, self.text):
            result_w = w
        self._add_result(w, result_w)
        return self

    def not_contains_regex(self, s, w: float = 1) -> "S":
        result_w = 0
        if not re.search(s, self.text):
            result_w = w
        self._add_result(w, result_w)
        return self

    def length_range(self, min_len: int, max_len: int, w: float = 1) -> "S":
        result_w = 0
        if min_len <= len(self.text) <= max_len:
            result_w = w
        self._add_result(w, result_w)
        return self

    def line(self, n, fn: Callable[["S"], None]) -> "S":
        result_w = 0
        lines = self.text.splitlines()
        if n < len(lines):
            s = S(lines[n])
            fn(s)
            w = sum(s._weights)
            result_w = sum(s._results)
        self._add_result(w, result_w)
        return self

    def part(self, s, fn: Callable[["S"], None]) -> "S":
        result_w = 0
        m = re.search(s, self.text)
        if m:
            s = S(m.group(1))
            fn(s)
            w = sum(s._weights)
            result_w = sum(s._results)
        self._add_result(w, result_w)
        return self

    def part_p(self, s, fn: Callable[[str], bool], w: float = 1) -> "S":
        result_w = 0
        m = re.search(s, self.text)
        if m:
            if fn(m.group(1)):
                result_w = w
        self._add_result(w, result_w)
        return self

    def call_p(self, fn: Callable[[str], bool], w: float = 1) -> "S":
        result_w = 0
        if fn(self.text):
            result_w = w
        self._add_result(w, result_w)
        return self

    def one_of(self, array, w: float = 1) -> "S":
        result_w = 0
        for s in array:
            if s == self.text:
                result_w = w
        self._add_result(w, result_w)
        return self


# TESTS ========================================================================

def test_score():
    assert S("a").contains("a", w=1).contains("a", w=1).score() == 1.0
    assert S("a").contains("a", w=3).contains("b", w=1).score() == 0.75


def test_contains():
    assert S("aaa").contains("a").score() == 1
    assert S("aaa").contains("a", w=0.5).score() == 1
    assert S("aaa").contains("A", ignore_case=True).score() == 1
    assert S("aaa").contains("a", max_count=1).score() == 0


def test_not_contains():
    assert S("aaa").not_contains("b").score() == 1
    assert S("aaa").not_contains("A", ignore_case=False).score() == 1
    assert S("aaa").not_contains("A", ignore_case=True).score() == 0


def text_contains_regex():
    assert S("A: \d+").contains_regex("A: 333").score() == 1
    assert S("A: \d+").contains_regex("A: aaa").score() == 0


def test_length_range():
    assert S("aaa").length_range(1, 4).score() == 1
    assert S("aaa").length_range(1, 2).score() == 0


def test_chain():
    assert S("aaa").contains("a").not_contains("b").score() == 1
    assert S("aaa").contains("a").not_contains("a").score() == 0.5


def test_line():
    assert S("aaa\nbbb\nccc").line(0, lambda s: s.contains("aaa")).score() == 1
    assert S("aaa\nbbb\nccc").line(1, lambda s: s.contains("bbb")).score() == 1
    assert S("aaa\nbbb\nccc").line(2, lambda s: s.contains("ccc")).score() == 1
    assert S("aaa\nbbb\nccc").line(2, lambda s: s.contains("aaa")).score() == 0


def test_part():
    assert S("aaa").part("a(.+)", lambda s: s.contains("aa")).score() == 1
    assert S("aaa").part("a(.+)", lambda s: s.contains("bb")).score() == 0


def test_call_p():
    assert S("aaa").call_p(lambda t: t.startswith("a")).score() == 1
    assert S("aaa").call_p(lambda t: t.startswith("b")).score() == 0
