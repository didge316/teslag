# Article 06 figure evidence — what was read off the print, and where the proof is

This directory exists so the figure verification for this article survives its working
directory. `books/tmp/` is gitignored and gets cleared; §6.6 requires every figure number
to be read off the printed page in the scan, never off an extractor filename or an OCR
caption, and that read is only worth anything if the crop it was made from can be opened
again. Five of the eight PNGs here are byte-identical copies of the crops opened during
feature-005/t6 (2026-10-11/12), copied out of `books/tmp/f05t6*`; the other three were cut
at feature-005/a06-figrec (2026-10-12) out of `books/tmp/f06figrec/` to settle the one
figure whose evidence contradicted itself. sha256 below, so a later pass can prove it is
looking at the same pixels and does not have to re-render a 500 ppi page to check a figure
number that has already been checked. The three label crops from this last pass are the
only ones whose exact `--box` was written down, and the two of them the reads were made
from were re-cut from those boxes at feature-005/a06-figrec and came out byte-identical to
the committed files — see "Re-deriving a crop".

Page mapping used throughout (§0.4): **printed page = scan file page − 18**. So scan file
183 is printed p. 165, scan file 186 is printed p. 168, scan file 244 is printed p. 226.
The 500 ppi renders these crops came from are `pdftoppm -r 500` of
`books/pdf-pages-tesla-1894/page-NNN.pdf` (1856 x 3227 px a page, the native resolution
of the image embedded in the page PDF; measured at feature-005/a06-figrec on the renders of
scan files 183, 184, 186 and 244, all four of which are 1856 x 3227). Those renders are not committed — they are 2.2 MB
each and regenerable with `books/tools/fig_crop.py --printed <N> --view --view-ppi 500`.

## The three figures this page publishes

They live in the `website` repo, not here, because that is where the page loads them from:
`website/assets/tesla1894/p165-fig110.webp` (761x681,
sha256 `ad401cae35f0f61a3d5cd1a20be5aafc606e4f8ee449a983a811438d83da1490`),
`p168-fig111.webp` (709x717,
sha256 `7a865b1cfe5c1ca4ead3b2364b53384587cbea0cd248d3b1d41bc1cad3d64ec5`) and
`p226-fig141.webp` (515x943,
sha256 `cb69b3ed639c80f93584424d8689b520dddc1081650e9bac6ec6a36e262eb937`). Total 157 KB,
inside the 400 KB per-article figure gate. Each published crop carries its own printed
`FIG. N.` line inside the crop, which is the §6.6 requirement; the widths and heights in
the article frontmatter are these files' actual pixel sizes.

## The evidence crops committed here

| file | sha256 | copied from (gitignored) | what it proves |
|---|---|---|---|
| `p165-caption-band-fig109-fig110.png` | `6c54b308dd295c3bec08a48d03e55e864fde7e9d0bd5bf7c0db2c6fa299ebdc2` | `books/tmp/f05t6b/z-165-captions.png` | printed p. 165 sets two photographs side by side and captions them `FIG. 109.` (left) and `FIG. 110.` (right). Figure 1 of the page is the right-hand plate. This is also the proof that the plate is on p. 165 while the sentence pointing at it is set on p. 166. |
| `p168-printed-caption-fig111.png` | `6d3eaa1af8329d9ff341173cd51601ba354a0e231ac0a373eec0fbb005096851` | `books/tmp/f05t6b/z-168-caption.png` | the printed caption under the second plate reads `FIG. 111.`, not the `FIG. ill.` the OCR returns. |
| `p168-bodyref-fig111-line.png` | `8111f86401644b8027293af57a06ef001d333f5d3265f488b62389975a4fc7af` | `books/tmp/f05t6/zoom-168-bodyref-line1.png` | the body text on the same printed page reads `nel, Fig. 111, which widens when the potential is increased` — the in-text cross-reference that ties the plate to the "luminous funnel" prose quoted in the caption. |
| `p226-caption-band-fig141-fig142.png` | `d6fc90e1a48f2fd5af18b3dc37dfbd6868d6c887ed2b3da65fec60dba5818874` | `books/tmp/f05t6b/z-226-captions.png` | printed p. 226 captions the left plate `FIG. 141.` and the right one `FIG. 142.`. Figure 3 of the page is the left-hand plate. |
| `p226-fig141-part-letter-zoom.png` | `7cbdc30475362e51a0259156752016b1a33ef57746464bf4c7385d2c9d64294f` | `books/tmp/f05t6c/fig141-labels.png` | the small italic part letters beside the tube and pool in Fig. 141 are too degraded to read at 500 ppi, which is why the alt text names shapes rather than part letters. It does not settle the globe label — the three crops below do. |
| `p226-fig141-globe-label.png` | `f8f427dd67fcebbacb0717808dfc5ad3beaeb9787be459b353dcb9e04619cfa0` | `books/tmp/f06figrec/z-226-globe-label.png` | the label at the right edge of the large globe in Fig. 141 at the native 500 ppi resolution: 180 x 160 px, box x 740 to 920 and y 1440 to 1600 of `books/tmp/scan-p244-500ppi.png`. One of the two reads the settled record below rests on. |
| `p226-fig141-globe-label-4x.png` | `b8c69c9b293e1a164a0aa6897b71f76e13294886f72f4923490bea083a108e6e` | `books/tmp/f06figrec/z-226-globe-label-4x.png` | the crop above at 4x (LANCZOS). Interpolation is what blurs this glyph: upscaled it reads at a glance like a `7` or a `Z`. The read was made from the native pixels, not from this upscale. |
| `p226-textline-globe-L.png` | `c2d99d772a24d88a4da080d1f087babc6ebbbd0518eaf6fbd69431f242fd7fe3` | `books/tmp/f06figrec/p226-textline-globe-L.png` | printed p. 226, the line that introduces this very plate, ending `…an incandescent lamp globe L,`. The letter is an italic `L` in the print; the PDF text layer of the same page renders that word as `Z,`. Cut at feature-005/a06-figrec — the decisive evidence for the settled read below. |

Each of the eight was opened against the print at the task that made it — the five at
feature-005/t6, re-checked at feature-005/a06-wipcommit, and the three label crops at
feature-005/a06-figrec — and each says what the frontmatter record in `../article.md`
claims it says, including the one place where that record had contradicted itself, now
settled below.

## The Fig. 141 globe label: print against OCR, settled at feature-005/a06-figrec (2026-10-12)

The frontmatter comment on figure 3 used to say the Fig. 141 part letters are "too degraded to
read even at 500 ppi". That is true of the small italic letters inside the plate — the
committed zoom above shows them as smudges — and it is still true of them: by the tube, at
the pool, at the ring. It was not true of the plate as a whole. At the right edge of the
large globe there is a letter, while the text layer of the same page renders the sentence
describing this very bulb as `In Fig. 141 the bulb comprises an incandescent lamp globe Z,
in the neck of which is sealed a barometer tube &, the end of which is blown out to form a
small sphere s`. Print and text layer disagreed about the globe's label — `L` against `Z` —
and the description of the same bulbs two pages on reads `When the globe L (Figs. 141 and
142) is exhausted to a very high degree` and `it is usually sufficient to grasp the globe L
with the hand`, which pointed at the text layer being the wrong one. That is precisely the
failure §6.6 is written against, so the plate was re-opened at 500 ppi and read, which is
what §6.6 permits for a figure whose evidence is contradicted and only for that figure. That
re-open happened in the feature-005/a06-figrec pass, not at t6; the five crops above that
came from `books/tmp/f05t6*` are the t6 reads and were not re-opened here.

It is an italic `L`, and the read is now made against the print of the same page rather than
against the plate alone. Two independent things settle it.

1. **The printed line that names the globe.** The text layer puts the word it renders `Z,` at
   x 245.088–252.351 pt, y 384.330–392.338 pt of a page that is 267.264 × 464.544 pt, so 6.9444
   px per pt in the 500 ppi render. Cropping that box out of the render shows the line ending
   `…lamp globe L,`: a serif bar across the top of the letter, one stem slanting down to the
   left, a foot running right and turning up at its end, then a comma. That is an `L`. A `Z`
   would need a top bar the full width of the letter and a flat bottom bar; there is no bottom
   bar at all, and the bottom stroke rises.
2. **The plate label is the same letterform.** Mapped at native pixels, with no interpolation,
   the glyph at the right edge of the globe in Fig. 141 has the same three strokes in the same
   arrangement as that printed italic `L`: a short serif bar sitting above the top of the stem,
   one stem slanting down-left, a foot running right and turning up. The plate glyph is 23 px
   tall against the body text's 33 px, which is why it looked ambiguous when it was first read
   from a 4x LANCZOS upscale — the interpolation smears the serif bar into a top bar and the
   rising foot into a flat one, and a blurred `L` looks like a `7`. The native-pixel map is what
   the read was made from, and the two plate crops above are that region.

The text layer is the wrong one, and it errs in a way this passage invites: in the same
sentence it renders the barometer tube's label as `&`, and a page later it renders `bulb` as
`bull)`. The p. 227 line `When the globe L (Figs. 141 and 142)` is clean body text and agrees
with the plate.

What did NOT change, and why. The alt text still names shapes rather than part letters,
because the letters that would have to be named inside the plate are the ones that really
are illegible, which is what §6.6 asks for in that case. The caption and the quoted
description still elide the letter positions, because `check_quotes.py` checks quotes
against the OCR text and `globe L` would not match it there: a quote corrected to agree
with the print would fail the tool that guards the quotes, and that is a worse trade than
an elision. The label is recorded here and in the frontmatter, not in the page copy. The
frontmatter sentence is now narrowed to the letters that actually are illegible, which is
what this note asked for.

## Re-deriving a crop

`fig_crop.py` writes to `books/tmp/` when `--out` is under it, so a fresh look costs one
render:

    python3 books/tools/fig_crop.py --printed 165 --view --view-ppi 500   # whole page to look at
    python3 books/tools/fig_crop.py --printed 165 --box x0,y0,x1,y1 --ppi 500 \
        --out books/tmp/recheck-165.png

The exact `--box` values used for the five t6 crops were not recorded, so re-deriving one
means re-reading the page; that is why the crops themselves are committed. Per §6.6,
only a figure whose evidence is missing or contradicted should be re-opened at all.

The globe-label crops are recorded exactly, and the record was tested rather than asserted:
at feature-005/a06-figrec both committed crops were re-cut from the boxes below out of
`books/tmp/scan-p244-500ppi.png` and came out byte-identical — `p226-fig141-globe-label.png`
sha256 `f8f427dd…` from the plate box, and `p226-textline-globe-L.png` sha256
`c2d99d77…` from the text-layer box at 3x LANCZOS. So these can be re-cut identically by
anyone, which the t6 crops cannot.

- the plate label: box x 740, y 1440 to x 920, y 1600. The glyph itself sits at x 795–818,
  y 1467–1490; the letterform map the read was made from covers x 793–825, y 1462–1496.
- the printed line: the text layer's bbox for the word it renders `Z,` is x 245.088–252.351 pt,
  y 384.330–392.338 pt, and the page is 267.264 × 464.544 pt, so multiply by 6.9444 to get
  pixels of the render. The committed crop is x 1381, y 2645 to x 1770, y 2743 at 3x LANCZOS.
- both reads need the native pixels. An 8x LANCZOS upscale of the plate label reads as a `7`
  to the eye; the pixel map is what settled it.
