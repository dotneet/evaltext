import re
from typing import Callable, Optional


class S:
    """Scorer for a text."""

    text: str
    _score: float

    def __init__(self, text):
        self.text = text
        self._score = 0

    def score(self) -> float:
        return self._score

    def contains(self, search: str, max_count: Optional[int] = None, ignore_case: bool = False, w: float = 1) -> "S":
        t = self.text
        s = search
        if ignore_case:
            t = self.text.lower()
            s = search.lower()
        cnt = t.count(s)
        if cnt > 0:
            if max_count is None or cnt <= max_count:
                self._score += w
        return self

    def not_contains(self, search: str, ignore_case: bool = False, w: float = 1) -> "S":
        t = self.text
        s = search
        if ignore_case:
            t = self.text.lower()
            s = search.lower()
        if t.count(s) == 0:
            self._score += w
        return self

    def contains_regex(self, s, w: float = 1) -> "S":
        if re.search(s, self.text):
            self._score += w
        return self

    def not_contains_regex(self, s, w: float = 1) -> "S":
        if not re.search(s, self.text):
            self._score += w
        return self

    def length_range(self, min_len: int, max_len: int, w: float = 1) -> "S":
        if min_len <= len(self.text) <= max_len:
            self._score += w
        return self

    def line(self, n, fn: Callable[["S"], None]) -> "S":
        lines = self.text.splitlines()
        if len(lines) > n:
            s = S(lines[n])
            fn(s)
            self._score += s.score()
        return self

    def part(self, s, fn: Callable[["S"], None]) -> "S":
        m = re.search(s, self.text)
        if m:
            s = S(m.group(1))
            fn(s)
            self._score += s.score()
        return self

    def part_p(self, s, fn: Callable[[str], bool], w: float = 1) -> "S":
        m = re.search(s, self.text)
        if m:
            if fn(m.group(1)):
                self._score += w
        return self

    def call_p(self, fn: Callable[[str], bool], w: float = 1) -> "S":
        if fn(self.text):
            self._score += w
        return self

    def one_of(self, array, w: float = 1) -> "S":
        for s in array:
            if s == self.text:
                self._score += w
                return self
        return self


def test_contains():
    assert S("aaa").contains("a").score() == 1
    assert S("aaa").contains("a", w=2).score() == 2
    assert S("aaa").contains("A", ignore_case=True).score() == 1
    assert S("aaa").contains("a", max_count=1).score() == 0


def test_chain():
    assert S("aaa").contains("a").not_contains("b").score() == 2

def test_part():
    assert S("aaa").part("a(.+)", lambda s: s.contains("aa")).score() == 1
    assert S("aaa").part("a(.+)", lambda s: s.contains("bb")).score() == 0

def test_call_p():
    assert S("aaa").call_p(lambda t: t.startswith("a")).score() == 1
    assert S("aaa").call_p(lambda t: t.startswith("b")).score() == 0
