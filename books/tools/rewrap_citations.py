#!/usr/bin/env python3
r"""Re-wrap markdown paragraphs so that citations like '(1894, p. N)' are never split across lines.

check_quotes.py's citation regex is r'\(1894, p\. \d+\)' and it does not span a newline, so a
citation wrapped over two lines reads as no citation at all. This script only re-wraps paragraphs
that currently contain a broken citation; it never changes the text of a line, only where the
lines break. Tokens that must stay whole: page citations, markdown links, {{PLACEHOLDER}}.
"""
import re
import sys

WIDTH = 99
CITE = re.compile(r"\(1894, p\. \d+\)")
BROKEN = re.compile(r"\(1894,\s*\n\s*p\. \d+\)|\(1894, p\.\s*\n\s*\d+\)")
ATOM = re.compile(r"\[.*?\]\(.*?\)|\{\{[A-Z]+\}\}|\(1894, p\. \d+\)")


def wrap(paragraph: str) -> str:
    text = " ".join(paragraph.split())
    # Replace must-not-break spans with space-free placeholders, wrap on words, put them back.
    atoms: list[str] = []

    def stash(m: re.Match) -> str:
        atoms.append(m.group(0))
        return f"\x00{len(atoms) - 1}\x00"

    words = ATOM.sub(stash, text).split()
    lines, cur = [], ""
    for word in words:
        if cur and len(cur) + 1 + len(word) > WIDTH:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    if cur:
        lines.append(cur)
    out = "\n".join(lines)
    out = re.sub(r"\x00(\d+)\x00", lambda m: atoms[int(m.group(1))], out)
    assert " ".join(out.split()) == text, "re-wrapping changed the text"
    return out


def main(path: str) -> int:
    src = open(path, encoding="utf-8").read()
    m = re.match(r"\A---\n.*?\n---\n", src, re.S)
    if not m:
        print("no front matter block found; refusing to touch", path)
        return 2
    head, body = src[: m.end()], "\n" + src[m.end() :]
    out, n = [], 0
    for block in re.split(r"(\n{2,})", body):
        if block.startswith("\n") or not block.strip():
            out.append(block)
            continue
        if block.lstrip().startswith(("#", "|", "-", ">", "!", "{{")):
            out.append(block)
            continue
        if BROKEN.search(block):
            block = wrap(block)
            n += 1
        out.append(block)
    open(path, "w", encoding="utf-8").write(head + "".join(out))
    left = len(BROKEN.findall("".join(out)))
    stray = [m.group(0) for m in re.finditer(r"\(1894, p\.\s*$", "".join(out), re.M)]
    print(f"{path}: re-wrapped {n} paragraph(s); {left} broken citation(s) left; {len(stray)} dangling")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
