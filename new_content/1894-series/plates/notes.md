# feature-008/t1 - the plates gallery (tesla-1894-plates)

SERIES-PLAN-1894.md §16.3(1): "60 engravings, page-cited, in a lazy-loaded grid,
each with printed page, book Fig. number and chapter, plus a downloadable ZIP
(1200 px, ~15 MB) and a one-line licence statement".

## What is here

- `article.md` - the draft. `{{GALLERY}}` marks where the grid goes; the grid is
  built from the selection record, not written here.
- `selection.json` - the audit trail, written by `books/tools/plates_gallery.py
  --select`. Every plate with its printed page, printed figure numbers, chapter,
  quality grade, the manifest row it came from, and how its caption was read; plus
  every rejected row and the reason. Re-running the command reproduces the page or
  says why it cannot.

## How to regenerate

    python3 books/tools/plates_gallery.py --all      # select, thumbs, zip, build
    python3 books/tools/qa_page.py website/tesla-1894-plates.html

`--report` prints the caption states; `--sheet` writes a contact sheet of the
plates the text layer cannot settle, for reading against the page render.

## What was measured at this task, not assumed

- The pool: `website/assets/tesla1894/manifest_qc.csv`, 223 rows. 4 are not book
  figures (page scans, a patent sheet, an index card). 129 fail the selection
  rules, 90 pass, 5 are second crops of a figure already in the pool, 85 unique
  printed figures, capped to 72 by the per-chapter rule.
- Captions come from the strip of print under the extractor's own ink band,
  re-derived at 300 ppi. 53 were read from the text layer that way, 19 came from
  hand crops whose QC rows record the printed caption being read at 400-500 ppi,
  and 0 needed this task's eyes. 17 of the 72 carry a figure number different from
  their file name because the caption under the plate said something else; 21 name
  more than one figure because the band runs across figures the page captions
  separately.
- The printed p. 14 example the page cites was checked against the scan's text
  layer at this task: that page sets `FIG. 7.` and `FIG. Ta.` (= 7a.) under the
  plate the extractor cut, and its body text separately mentions Fig. 9, which is
  the number the file carries (`p032-fig1-fig9.webp`). The gallery captions it as
  Figs. 7 and 7a, printed p. 14.
- The three plates shown in the article text (printed pp. 378, 392, 478) are three
  of the 72 on the grid and carry the same captions in both places.
- Every quote on the page was re-grepped and pinned before drafting:
  `python3 books/tools/check_quotes.py new_content/1894-series/plates/article.md`
  reports 8 fragments, 8 verbatim and page-cited.

## Tool changes made at this task

`books/tools/plates_gallery.py` was untracked work from the three attempts before
this one; the selection, caption-reading and page-building logic is theirs. Two
defects in the caption text were fixed here, because the captions are the
deliverable:

1. `LEAD_FIG` had no `re.IGNORECASE`, so a subject line beginning "Fig. 208:" kept
   its own figure prefix inside a caption that already states the figure. It now
   matches case-insensitively and only when a separator follows, so
   "Fig. 163 (left) and Fig. 164 (right), each a tall sealed tube" is left alone.
2. Provenance clauses survived into captions ("re-exported at 400 ppi from scan
   file 496 and rotated to landscape:", "; printed FIG. 208. caption inside the
   crop"). They are about our file, not the plate, and are now taken out. 14 of
   the 72 captions carried one; 0 do now.
3. `fig_label` rendered `p482-figs300-308.webp` as "Figs. 300 and 308" when the
   plate carries nine printed figures. A named range now reads "Figs. 300 to 308".

## Open at handoff, on purpose

- The page is not wired: no sitemap.xml entry, no llms.txt line, no card, no
  inbound link. That is feature-008/t5. Until something links to it,
  `qa_page.py`'s ">= 3 links to pages that link back" gate fails on this page
  alone; every other gate passes.
- `og_image` points at `assets/og/tesla-1894-plates.webp`, which does not exist
  yet. All twelve shipped series pages reference an OG file the OG pass has not
  made; this page is consistent with them rather than quietly different.
- The hub (`tesla-1894.html`) does not exist yet, so the breadcrumb in the
  JSON-LD names a page that is not written. §16.3 wants the hub to link here; the
  hub ships last by design (O3).
