# Article 06 figure evidence — what was read off the print, and where the proof is

This directory exists so the figure verification for this article survives its working
directory. `books/tmp/` is gitignored and gets cleared; §6.6 requires every figure number
to be read off the printed page in the scan, never off an extractor filename or an OCR
caption, and that read is only worth anything if the crop it was made from can be opened
again. The five PNGs here are byte-identical copies of the crops that were actually
opened during feature-005/t6 on 2026-10-12 — sha256 below, so a later pass can prove it
is looking at the same pixels and does not have to re-render a 500 ppi page to check a
figure number that has already been checked.

Page mapping used throughout (§0.4): **printed page = scan file page − 18**. So scan file
183 is printed p. 165, scan file 186 is printed p. 168, scan file 244 is printed p. 226.
The 500 ppi renders these crops came from are `pdftoppm -r 500` of
`books/pdf-pages-tesla-1894/page-NNN.pdf` (1856 x 3226 px a page, the native resolution
of the image embedded in the page PDF). Those renders are not committed — they are 2.2 MB
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
| `p226-fig141-part-letter-zoom.png` | `7cbdc30475362e51a0259156752016b1a33ef57746464bf4c7385d2c9d64294f` | `books/tmp/f05t6c/fig141-labels.png` | the small italic part letters beside the tube and pool in Fig. 141 are too degraded to read at 500 ppi, which is why the alt text names shapes rather than part letters. It does not settle the globe label — see the gap below. |

All five were re-opened against the print at feature-005/a06-wipcommit (2026-10-12) before
being committed, and each says what the frontmatter record in `../article.md` claims it
says — with one exception, recorded below rather than quietly kept.

## One thing the record gets wrong, left here for feature-005/t6

The frontmatter comment on figure 3 says the Fig. 141 part letters are "too degraded to
read even at 500 ppi". That is true of the small italic letters inside the plate — the
committed zoom above shows them as smudges. It is not true of the plate as a whole: at the
right edge of the large globe there is a letter that reads as an italic `L` in the full
crop `p226-fig141.webp`, while the OCR of the sentence describing this very bulb prints
`In Fig. 141 the bulb comprises an incandescent lamp globe Z, in the neck of which is
sealed a barometer tube &, the end of which is blown out to form a small sphere s`. Print
and OCR disagree about the globe's label — `L` against `Z` — and the description of the
companion bulb two pages on says `it is usually sufficient to grasp the globe L with the
hand`, which points at the OCR being the wrong one. That is precisely the failure §6.6 is
written against, and the plate at 500 ppi is the only way to settle it. What does stay
unreadable at 500 ppi is the small letters inside the plate — by the tube, at the pool,
at the ring.

So the frontmatter sentence is right in its effect — the alt text names shapes, which is
what §6.6 wants when parts cannot be named, and the caption quotes the p. 226 description
with the letter labels elided — but the blanket claim is overstated. Before this page goes
to QA it should be narrowed to the letters that actually are illegible, and the globe label
should be settled against the print rather than assumed unreadable. That is t6's call, not
a change to make in a WIP commit.

## Re-deriving a crop

`fig_crop.py` writes to `books/tmp/` when `--out` is under it, so a fresh look costs one
render:

    python3 books/tools/fig_crop.py --printed 165 --view --view-ppi 500   # whole page to look at
    python3 books/tools/fig_crop.py --printed 165 --box x0,y0,x1,y1 --ppi 500 \
        --out books/tmp/recheck-165.png

The exact `--box` values used for the five crops above were not recorded, so re-deriving
one means re-reading the page; that is why the crops themselves are committed. Per §6.6,
only a figure whose evidence is missing or contradicted should be re-opened at all.
