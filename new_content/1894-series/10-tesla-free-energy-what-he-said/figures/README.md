# Article 10 figure evidence — what was read off the print, and where the proof is

This directory exists so the figure verification for this article survives its working
directory. `books/tmp/` is gitignored and gets cleared; §6.6 requires every figure claim to be
read off the printed page in the scan, never off an extractor filename, a manifest subject line
or an OCR caption, and that read is only worth anything if the crop it was made from can be
opened again. All ten files here were cut at feature-007/t2 (2026-10-18) out of eight 500 ppi
renders, and **every one of them has its exact box recorded below**, which is the thing
feature-005/t6 could not do for article 06 and what feature-005/a06-figrec had to reconstruct
by hand. The boxes were written to `books/tmp/f07t2/crops.json` as the crops were cut by
`books/tmp/f07t2/cut_f07t2.py`; they are copied here so the record does not live in a
gitignored file, and every crop was re-cut from its box at the end of this task and came out
byte-identical (see "Re-deriving a crop"). Ten of the twelve files are in this directory; two
are in the site repo.

Page mapping used throughout (§0.4): **printed page = scan file page − 18**. So scan file 254
is printed p. 236, scan file 442 is printed p. 424, scan file 447 is printed p. 429, scan file
448 is printed p. 430, scan file 512 is printed p. 494 and scan file 514 is printed p. 496.
Scan files 9 and 10 are unnumbered front matter (title page, copyright page) and have no
printed page number; the title page's own date line reads 1894.

The renders are `pdftoppm -r 500` of `books/pdf-pages-tesla-1894/page-NNN.pdf`. **The body
pages are 1856 x 3227 px, and the two front-matter pages are not**: scan 9 is 1792 x 3272 and
scan 10 is 1832 x 3202. Every box below is in pixels of the render named by its scan number,
so a box on a front-matter page is in that page's own pixel grid, not in the 1856 x 3227 grid
the rest of this file assumes. They are in `books/tmp/f07t2/scan-p{009,010,254,442,447,448,449,512,514}-500ppi.png`,
not committed (0.8 to 4.7 MB each, regenerable with
`pdftoppm -r 500 books/pdf-pages-tesla-1894/page-NNN.pdf out`).

## The three figures this page publishes

They live in the `website` repo, not here, because that is where the page loads them from.
Two are page-scan crops, which is §6.6's sourcing order 4, the words being the artefact; the
third is an engraving borrowed from article 08 with a caption written for this page. Each is
named by printed page as §6.2.5 asks, with a suffix saying which part of the page a page-scan
crop is (`-index`), which the older `-detail` suffix on `scan-p346-detail.webp` does not. The
widths and heights in the frontmatter are these files' actual pixel sizes.

| published file | px | bytes | sha256 | cut from the 500 ppi render at box |
|---|---|---|---|---|
| `website/assets/tesla1894/scan-p236.webp` | 820x690 | 115,452 | `982e6b16fb9f5b4b189bbbe71386e33e429a048dc31788cae9b85ef58e8010b0` | x 110, y 110 to x 1750, y 1490 of scan 254, then reduced to 0.5 |
| `website/assets/tesla1894/p430-fig242.webp` | 1169x768 | 73,692 | `40e6a706c34dfaa4384dd5bf3c789a1dcfabe6b1ea64189d5d73d08d02a04072` | not cut here: cut at feature-006/t2 from scan 448 at x 196, y 1189 to x 1365, y 1957 |
| `website/assets/tesla1894/scan-p496-index.webp` | 860x695 | 59,920 | `a6e5df9f695cf4ff5618ad3aa041c0adff35844b0f7776eb99076bc6c8bdebda` | x 100, y 110 to x 960, y 805 of scan 514, at 1.0 |

Total 249,064 bytes, inside the 400 KB article-figure gate that `qa_page.py` measures.

**Why figure 1 is published at half the scale it was cut at.** The read was made at 500 ppi and
the crop was cut at 500 ppi, then reduced to 0.5 before saving. At full scale the same crop is
1640 x 1380 and this page's three figures together would have gone over the 400 KB gate. Half
scale puts the crop at 820 px wide, which is the 1.1x-the-740-px-column sizing that
`manifest_qc.csv` row 213 records for `scan-p346-detail.webp`, the only other page-scan crop of
a text page the site publishes. Figure 3 is published at 1.0 (860 px, 1.16x the column) because
a smaller crop of a two-column index page loses the folio, and the folio is what makes the crop
self-identifying.

**What figure 2 is doing here.** `p430-fig242.webp` is the plate article 08 publishes as its
figure 3. It was cut, verified and hashed at feature-006/t2 (2026-10-17), where the printed
captions `FIG. 242.` and `FIG. 243.` and the body line naming them were read off a 500 ppi
render. Nothing at this task contradicts that read, so the plate was **not re-opened**: it was
re-hashed here (the sha256 above is the one article 08 recorded) and borrowed. §6.6 allows the
same engraving on two articles only when the caption differs, and these two do: article 08's
names the parts and the absence of a trial, this page's is about the fire under the machine and
the boiler above it. The alt texts necessarily resemble each other, because it is the same plate.

## The ten evidence crops committed here

These are not published. They are the proof of the reads in the frontmatter record in
`../article.md`, and each one is a crop of a page that had to be re-opened because its evidence
was missing or contradicted.

| file | sha256 | box in the render named by its scan | what it proves |
|---|---|---|---|
| `p236-line-kinetic-em-dashes.png` | `067c870e288a00eba8c5d54e93c4c3a6a04edd6ba88febd8e741df08256589f3` | x 110, y 725 to x 1760, y 870 of scan 254 | the two lines that set `if kinetic` and `is, for certain` carry the printer's **em dashes**, not the hyphens this site's voice rule forces into the body text. |
| `p236-paragraph-break-after-inefficient.png` | `e156a40e4171fe37394b0f4f0eee35df6805489497fe0f8db9d52d920d7ecaaa` | x 110, y 1330 to x 1760, y 1490 of scan 254 | `ever invented!` ends the wheelwork paragraph and the next paragraph begins, indented, `The preceding experiment is only one of many equally inter-`. This is the layout the article's argument about the sentence depends on. |
| `p424-chapter-heading.png` | `f5fa4ef56563db5883b28daf6bfa4614e5272735fd423772755a5ddd2ae40871` | x 150, y 640 to x 1770, y 840 of scan 442 | chapter XXXVI's display heading as the page sets it: `CHAPTER XXXVI.` then `THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS.` |
| `p424-page-no-plate.webp` | `d7660ef869f14dff5dd39a3b3c199f9dda80be4b877630860695f3c570715c36` | whole of scan 442, reduced to 0.377 | the whole of printed p. 424: heading, two paragraphs, a footnote, and **no engraving and no printed `FIG.` line anywhere on the page**. §9 brief 10 asks this article for a figure at p. 424; the brief's pointer is wrong. |
| `p429-page-no-illustration.webp` | `6d5b390bb9598d067d3aa0f17f29ffd9699cde4362b5bb282af43d965d3383a8` | whole of scan 447, reduced to 0.377 | the whole of printed p. 429: the pyromagnetic generator's two laws, the flame-to-orange-red bench experiment and a footnote, and **no illustration of any kind**. The draft said this page illustrated the generator with a bench setup; it does not, and the sentence is rewritten in the body. |
| `p431-page-no-illustration.webp` | `9d09e1095f0017fcc12e967d6c5353db49d6b893ad2d8ed41c8834476f8153ae` | whole of scan 449, reduced to 0.377 | the whole of printed p. 431, the chapter's last page: running head `THERMO-MAGNETISM AND PYRO-MAGNETISM.`, folio 431, one closing paragraph about the steam-exhaust pipe and the cooling device, and **no illustration**; the lower two thirds of the page is blank. | 
| `p494-generators-pyromagnetic-429.png` | `08462f9e46ee6bfae24770f078f6044419d13bb126becfd1e947f148a1d3eedb` | x 960, y 1900 to x 1770, y 2120 of scan 512 | the right column of the volume's index on printed p. 494 carries `Generators, Pyromagnetic..... 429`, one of the two index entries the article counts. |
| `p496-right-column-thermo-magnetic-motors-424.png` | `a76d57a2e34b774127e287bc2eda8a7a9038cd021ae8885656334af6b6d542ca` | x 960, y 415 to x 1770, y 690 of scan 514 | the right column of printed p. 496 carries `Thermo-Magnetic Motors..... 424`, which is the index entry behind the `magnetic motor` count of 3 that the body reports. |
| `frontmatter-title-page-scan09.webp` | `4e7225235e89ef9eff3922b17f2b50b1b244b9d4acb8066f929e30cbd57936ec` | whole of scan 9, reduced to 0.39 | the title page of our copy: `THE INVENTIONS RESEARCHES AND WRITINGS OF NIKOLA TESLA`, `WITH SPECIAL REFERENCE TO HIS WORK IN POLYPHASE CURRENTS AND HIGH POTENTIAL LIGHTING`, `BY THOMAS COMMERFORD MARTIN`, the line under his name reading `Editor THE ELECTRICAL ENGINEER; Past-President American Institute Electrical Engineers`, then `1894`, then `THE ELECTRICAL ENGINEER / NEW YORK / D. VAN NOSTRAND COMPANY, / NEW YORK.` This is the read that lets the hub's `figures[0]` row (`scan-title-page.webp`, `verified: false` in `new_content/1894-series/index.json`) be set from evidence. |
| `frontmatter-copyright-page-scan10-entry-line.png` | `dc243a17af8a514ca9d392d986c8cc6c5d20d69baba895bdcc41ed1ac92b81e9` | x 400, y 1500 to x 1500, y 1800 of scan 10 | the copyright entry: `Entered according to Act of Congress in the year 1893 by T. C. MARTIN in the office of the Librarian of Congress at Washington`. Entered 1893, title page 1894, which is worth knowing the next time anyone dates this edition from the copyright line. |

Each of the ten was opened and read at feature-007/t2, and each says what the frontmatter
record in `../article.md` claims it says.

## Re-deriving a crop

`python3 books/tmp/f07t2/cut_f07t2.py` re-cuts all twelve files this task touched (two
published, ten evidence) from the boxes above and prints their sizes and sha256s. Re-run at
the end of this task, every file came out **byte-identical** to the one committed here or in
the site repo: 11 files compared on the first re-run and 12 on the second, 0 changed. That is
the test feature-006/t2 recorded as the lesson ("re-run a box and a hash, that is the test"),
and it is the reason the boxes are in this file rather than only in `crops.json`.

The script writes the published crops straight into `website/assets/tesla1894/` and the evidence
crops into this directory, and it re-hashes `p430-fig242.webp` without touching it, so the
record can show that the borrowed plate is unchanged.

## Three claims the earlier draft of this record made, corrected against the print

The record written at the start of this task asserted things it had not checked. They are
corrected here rather than carried, in the same way feature-006/t2 corrected article 08's record.

1. **"The text layer gives hyphens" for the wheelwork sentence. It does not.** The PDF text
   layer of scan 254 carries the same em dashes the print sets: `if kinetic — and this we know
   it` is U+2014 in `page-254.pdf` and in `books/extracted/tesla-1894-plain.txt`. The body
   writes spaced hyphens because `qa_page.py`'s voice gate bans em and en dashes inside the
   article, not because the source differs. The quote still verifies because
   `grep_quote.normalise` maps U+2014, U+2013 and U+2012 to a plain hyphen and then deletes
   hyphen-plus-space, so both spellings normalise to the same string.
2. **"The printer's line at the foot of the copyright page is unreadable at 500 ppi." It is
   readable.** At x 150 to x 700, y 3040 to y 3110 of scan 10 the print gives
   `Press of McIlroy & Emmet, 36 Cortlandt St., N. Y.` in dark roman type, legible at 500 ppi
   without stretching. The text layer of that page has the same line with a lower-case l,
   `Mcllroy`; whether the printed letter is a capital I or a lower-case l is not decidable at
   this resolution, so the rest of the line is recorded off the print and that one letter is
   claimed neither way. What *is* unreadable is the faint line below it, and it is not a printer's
   line at all: mirrored and contrast-stretched it reads `...AN NOSTRAND COMPANY,`, reversed.
   That is the title page's own imprint line showing through the back of the same leaf, which
   says scan 9 and scan 10 are the two faces of one physical leaf.
3. **"Printed pp. 425, 426, 427 and 428 (scans 443 to 446): crops exist, rows 158 to 161 call
   them keep/A." The row numbers and the page numbers do not line up.** Rows 158 to 161 of
   `website/assets/tesla1894/manifest_qc.csv` are `p443-fig1-fig281.webp`,
   `p444-fig1-fig235.webp`, `p445-fig1-fig287.webp` and `p448-fig1-fig243.webp`, which are
   printed pp. **425, 426, 427 and 430** (scan files 443, 444, 445 and 448), all four
   `keep` / quality `A`. **Printed p. 428 (scan 446) has no crop on disk and no row in either
   manifest**, even though its text layer sets the caption lines `FIG. 240.` and `FIG. 241.`;
   the extractor returned nothing for that page. Rows 162 and 163 (`p451-fig1-fig244.webp`,
   `p452-fig1-fig247.webp`, printed pp. 433 and 434) are not chapter XXXVI at all: printed
   p. 433 opens `SPARKING BRUSHES AND COMMUTATORS`, the next chapter. Chapter XXXVI runs
   printed pp. 424 to 431, which is confirmed by the running head on scan 449.

## Three pages that were re-opened and have nothing on them

Printed p. 424 and printed p. 429 are the two pages this article's own pointers cited for an
illustration, and neither page has one. That is the whole of the CONTRADICTION half of this
task, and both halves are proved by a whole-page crop rather than by a crop of something,
because the absence of an engraving is only checkable on the whole page. Printed p. 431 was
re-opened for the same reason and has nothing on it either, which closes the chapter: of its
eight pages, three are now verified empty of art and one is verified to carry two plates.

- printed p. 424 (scan 442): heading, two paragraphs, one footnote. No plate, no printed
  `FIG.` line, and the text layer of that page returns no `FIG.` string either. §9 brief 10's
  figure line points this article at `tesla1894-p424-fig*`; no file in the site repo uses that
  name form, and there is nothing on that page to crop.
- printed p. 429 (scan 447): the two laws, the bench experiment described in words, one
  footnote. No illustration. The chapter's two drawings of the machine are on printed p. 430.
- printed p. 431 (scan 449): one closing paragraph and a blank lower half. No illustration, and
  its text layer returns no `FIG.` string either. This page was rendered at 500 ppi during this
  task and read off that render; the record's first draft said it had not been rendered, which
  is wrong, and the crop above is the proof of what the render shows.

## What was not re-opened, and what that leaves open

- **Printed p. 430 (scan 448)** — settled at feature-006/t2 on 2026-10-17 against a 500 ppi
  render, with the printed captions and the body line naming them read off the print. Re-hashed
  here, unchanged. Borrowed, not re-made.
- **Printed pp. 425, 426, 427 (scans 443, 444, 445)** — crops exist, rows 158 to 160 call them
  `keep` / `A`. This page publishes nothing from them, so they were not re-opened. The
  disagreement row 158 records for printed p. 425 (its note says "Figure number 281 is genuine
  for p.425" while that page's text layer sets `FIG. 231.`, `FIG. 232.` and `FIG. 233.`) is
  still NOT SETTLED, exactly as article 08 left it, and nobody should take it as settled.
- **Printed p. 428 (scan 446)** — no crop, no row, not rendered at this task, and nothing on
  this page cites it. Its text layer sets `FIG. 240.` and `FIG. 241.`, so a plate is claimed by
  the text layer and has never been verified off the print by anyone.
- **Printed p. 431 (scan 449)** — rendered and read (see above), and nothing on this page
  cites it, so no figure was published from it.
- The chapter's plate pages, named from the text layer's caption lines and **not verified**:
  printed pp. 425, 426, 427, 428 and 430. Of those, only 430 has been read off the print.
  What has been read off the print is the other side of the question: printed pp. 424, 429 and
  431 have no art on them at all.

## Two things the text layer does on the pages this task re-opened

Neither is a reason to doubt the reads above, which were made off the print. Both are specimens
of the limit the article's own method section describes, and one of them is the reason the hub's
title-page row could not have been verified from the text layer at any price.

- **The title page's text layer returns its subtitle with the words out of order**:
  `WITH SPECIAL REFERENCE CURRENTS AND TO HIGH HIS WORK POTENTIAL IN POLYPHASE LIGHTING`.
  `with special reference` as a phrase returns **0** hits in `books/extracted/tesla-1894-plain.txt`
  while the page plainly sets it (measured 2026-10-18).
- **The index pages put an entry and its page number on separate lines**, so
  `Pyromagnetic Generators......429` as the page sets it returns **0** while
  `Pyromagnetic Generators` returns **1** and `Generators, Pyromagnetic` returns **1**. That is
  why this article cites the phrase and the page number separately rather than as one string,
  and why the two counts the body prints are the phrase counts, not leader-inclusive counts.
- **The em dashes on printed p. 236 are in the text layer too** (see correction 1 above), which
  is the other direction: there, the text layer is right and the site's own voice rule is what
  changes the characters that get printed.

## manifest_qc.csv rows written at this task

The site repo's `website/assets/tesla1894/manifest_qc.csv` had no row for either page-scan crop
this task cut, so two were added, following the precedent of row 213 (`scan-p346-detail.webp`),
the only comparable row in the file:

- **row 220** `scan-p236.webp` — its box, its 0.5 publishing scale and why, its size and sha256,
  and the reads that figure 1 of article 10 depends on.
- **row 221** `scan-p496-index.webp` — same, for figure 3.
- **row 219** `p430-fig242.webp` — a note appended saying the plate is now also used in article
  10 with a different caption, which is the condition §6.6 puts on reusing an engraving.

Row numbers are file line numbers, header included, which is the convention feature-006/t2
established when it added rows 217 to 219.
