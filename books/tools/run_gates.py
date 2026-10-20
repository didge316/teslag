#!/usr/bin/env python3
"""Run every deterministic gate the 1894 series has, in one non-zero-exiting pass.

This exists so the harness gate can actually gate. `harness/config.json` names
this script as `commands.test` and `titlecase_headings.py --check` as
`commands.lint`; before that, the BUILD gate ran no project check at all and a
task "passing" meant only that a worker had marked it complete.

    python3 books/tools/run_gates.py            # every page, every draft
    python3 books/tools/run_gates.py --quick    # skip the quote pass (slowest)

What it runs, in the order that fails cheapest first:

  1. qa_page.py --self-test          the fixture tests for the page gates
  2. check_quotes.py --self-test     the fixture tests for the quote checker:
                                     one case per defect class it once got wrong
  3. make_article.py --self-test     the renderer's own fixture: lists, tables,
                                     code, links, schema. A render is the one step
                                     that can silently change every page at once.
  4. titlecase_headings.py --check   the house rule for series headings
  5. check_quotes.py --all-series    every quote verbatim + page-cited (SERIES-PLAN §8 step 2, §12)
  6. qa_page.py --all-series         the numeric page gates: links, canonicals, figures, schema

Paths are resolved from this file, not from the caller's cwd, because the
harness runs commands with cwd = books/ while the pages live in ../website.

What it cannot check, and no run of this script will: figure subject/caption
truth, 3-viewport layout, OG legibility. Those are §12 visual gates and need
vision — `shot_qa.py <slug>` per page. A green run here is necessary, not
sufficient.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def run(label: str, argv: list[str], timeout: int = 900) -> tuple[int, float, str]:
    t0 = time.time()
    try:
        p = subprocess.run(argv, cwd=str(TOOLS.parent), capture_output=True,
                          text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 124, time.time() - t0, f"TIMEOUT after {timeout}s: {' '.join(argv)}"
    except OSError as e:
        return 127, time.time() - t0, f"could not start {argv[0]}: {e}"
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, time.time() - t0, out


def tail(text: str, n: int = 25) -> str:
    """Last n non-empty lines — the summary is at the end of every gate's output."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    return "\n".join(("    " + ln) for ln in lines[-n:])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true",
                    help="skip check_quotes.py, the slowest pass")
    ap.add_argument("--final", action="store_true",
                    help="a planned page that does not exist yet is a failure, not a warning. "
                         "Use at SHIP; leave off during BUILD.")
    args = ap.parse_args()

    py = sys.executable
    steps = [
        ("gate self-test", [py, str(TOOLS / "qa_page.py"), "--self-test"]),
        ("quote checker self-test",
         [py, str(TOOLS / "check_quotes.py"), "--self-test"]),
        ("renderer self-test",
         [py, str(TOOLS / "make_article.py"), "--self-test"]),
        ("heading title case", [py, str(TOOLS / "titlecase_headings.py"), "--check"]),
    ]
    if not args.quick:
        steps.append(("quote verbatim + cited",
                      [py, str(TOOLS / "check_quotes.py"), "--all-series", "--quiet"]))
    steps.append(("numeric page gates", [py, str(TOOLS / "qa_page.py"), "--all-series"]))

    failed = []
    warned = []
    print(f"running {len(steps)} gate(s) from {TOOLS.parent}\n")
    for label, argv in steps:
        code, secs, out = run(label, argv)
        # A page that has not been built yet is unfinished work, not a defect.
        # Failing the gate for it would make the gate red for every remaining
        # task in the plan, which is indistinguishable from a worker doing
        # nothing — the exact shape that burns a run without progress. At SHIP
        # pass --final and unbuilt pages are failures again.
        if (code != 0 and label == "numeric page gates" and not args.final):
            missing = [ln.split(" ", 1)[1].strip()
                       for ln in out.splitlines() if ln.startswith("MISSING ")]
            broken = [ln for ln in out.splitlines()
                      if " — FAIL " in ln or ln.startswith("FAIL ")]
            if missing and not broken:
                code = 0
                warned.extend(missing)
        flag = "PASS" if code == 0 else f"FAIL(exit {code})"
        print(f"=== {label}: {flag} in {secs:.0f}s ===")
        if code != 0:
            print(tail(out))
            failed.append(label)
        else:
            # Print only the tool's own summary line on success — a green gate
            # should cost the reader two lines, not three hundred.
            summary = [ln for ln in out.splitlines()
                       if "pass" in ln.lower() or "PASS" in ln][-1:]
            print("    " + (summary[0].strip() if summary else "clean"))
            for m in warned:
                print(f"    NOT BUILT YET (not a defect): {m}")
        print()

    if failed:
        print(f"GATE FAIL — {len(failed)}/{len(steps)} gate(s) failed: {', '.join(failed)}")
        print("not covered here (need vision): figure subject/caption truth, "
              "3-viewport layout, OG legibility — §12 visual gates via shot_qa.py")
        return 1
    if warned:
        print(f"GATE PASS with {len(warned)} unbuilt page(s): "
              + ", ".join(Path(m).name for m in warned))
        return 0
    print(f"GATE PASS — {len(steps)}/{len(steps)} gates clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
