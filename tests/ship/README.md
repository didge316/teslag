# tests/ship — the machinery items 5, 6 and 7 were committed with

Nothing in this directory measures the site. It is the part of the work that was
**building the commits**, and it lived in `/tmp` until 04:00-ish on 2026-11-19, when
a reboot took it with it — for the second time in this project's history, which is
what `PLAN-ALT-NAV-OVERFLOW.md` §1 means by "harnesses live in the repo, never /tmp".
The source was only recoverable because the session log records every file write;
the recovery is replayed here, patch for patch, and the paths were moved out of
`/tmp` while doing it.

| file | what it is |
|---|---|
| `stage.py` | Builds each intermediate state from `git show HEAD:<path>` plus this branch's own transformations: `item5/` (whitespace + quote repair, old nav still in place) and `item6/` (that, plus the nav rewrite), and `site-shipped/` — a copy of the tree exactly as the branch tip will contain it, i.e. **without** anybody else's in-flight work. This is the tree the definitive gates were served from on `:8200`. |
| `commit-index.py` | Turns those states into four commits through the **git index** (`hash-object -w` + `update-index --cacheinfo`), never the filesystem, then verifies afterwards that `HEAD` equals the measured tree file-for-file. `--dry` stages nothing. |
| `split.py` | The item-7/item-6 CSS split: the stylesheet with the two navbar rule blocks cut, for the commit that is only the caps. `css7` regenerates `tests/.staging/css-item7.css` from the snapshot and writes nothing else — `stage.py shipped` calls it on every build, because a `css-item7.css` cut from yesterday's snapshot makes every BEFORE-flavour cell and the payload comparison measure a stylesheet nobody is shipping. Its mutating modes (`a-css` without `--dry`, `b-html`, `c-restore`) rewrite the working tree and now refuse to do so without `--write-tree`; `commit-index.py` only ever calls `step_a_css(dry=True)`. |
| `messages/` | The four commit messages, kept in git because the numbers they quote are artefacts in this repo and a message that drifts from them is the quiet failure this whole branch is built to catch. |

## Why the commit split cannot be a `git add`

Two of the three items (the nav rewrite and the whitespace repair) touch the same
52 files, so no whole-file staging separates them. Worse: the working tree also
contains somebody else's unfinished work — `js/scripts.js` (the sticky bar, +322/-1,
and it is **not** in any commit on this branch), `_headers`, `_redirects`, `llms.txt`,
`sitemap.xml`, the untracked `electrical-experimenter.html` with `assets/ee1919/`, and
an uncommitted paragraph inside four pages linking to that page.

`git add -u '*.html'` — the obvious command — puts their paragraph into a commit whose
message says *whitespace only*, and nothing in `git add` or `git commit --stat` says so.
So nothing here edits a file: every state is regenerated from `HEAD`, hashed, and put
in the index. What is left uncommitted afterwards is asserted to be exactly the owner's
work, and `stage.py` stops on any difference between the generated tree and the working
tree that does not mention `electrical-experimenter` / `ee1919` / `email-capture`.

## Order

```bash
python3 tests/ship/stage.py shipped                      # build states, assert the scope
python3 -m http.server 8200 --bind 127.0.0.1             # from tests/.staging/site-shipped
(cd tests/overflow && python3 gate.py http://127.0.0.1:8200 --engine webkit --only "$PAGES")
python3 tests/ship/commit-index.py --dry                 # preflight + what would be staged
python3 tests/ship/commit-index.py                       # four commits, then verify HEAD
```

**`shipped` is not optional.** `stage.py` with no argument runs `build`, which regenerates
the item5/item6 page states and leaves `site-shipped/` exactly as it was — so a gate run
after a CSS edit, invoked that way, measures last week's stylesheet and reports it green.
That is how the EmailOctopus fix of 2026-11-19 nearly went out unmeasured: the tree
rebuild printed "generated 52 pages" and looked like a rebuild. `shipped` is the one that
rebuilds the measured tree (`rm -rf` + streaming tar, then the generated pages over it),
and `tests/validate.sh` step 0/9 calls it for that reason.

`commit-index.py` refuses to commit unless every artefact its messages quote contains
its own verdict line — `tests/overflow/gate-FINAL-*.txt` must each carry a complete
green matrix (a chunked run's verdict lines are summed), `inert-100.txt` and
`tests/nav/verify-final.txt` must carry a verdict, and `css-comment-only.py` must say
the stylesheet on disk still describes the bytes the gates served. A run that was
interrupted leaves a file whose tail is a traceback, and twice on this branch a number
was already in the notes before the artefact was read.

Nothing in here pushes. Pushes to `main`, and preview-branch pushes, are the owner's
call (`HANDOFF.md`).

## After any CSS change: the payload snapshot has to move with it

`gate.py` prints the sha256 prefix of the stylesheet it served, and
`tests/overflow/payload-measured-<prefix>.css` is those exact bytes; `css-comment-only.py`
proves the file on disk still says what those bytes said (comments stripped, whitespace
collapsed, byte-identical). When rule text changes on purpose — as it did with the
`.eo-form input[type="submit"] { overflow: hidden; overflow: clip }` rule — the answer is
never to relax that check. Re-run the gates against the new bytes, save the CSS the new
run served as a new `payload-measured-*.css`, and leave the old snapshot where it is: it
is the evidence for `gate-BEFORE-cssfix-*` and `gate-BEFORE-cssregions`, which are cited
in `KNOWN-WEBKIT-300.md` as the before picture. `css-comment-only.py` with no arguments
picks the newest snapshot and prints all of them, so the pairings stay visible.
