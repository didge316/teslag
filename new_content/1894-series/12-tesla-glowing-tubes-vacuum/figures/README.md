# Article 12 figure evidence — what was read off the print, and where the proof is

This directory exists so the figure verification for this article survives its working
directory. `books/tmp/` is gitignored and gets cleared; §6.6 requires every figure number to be
read off the printed page in the scan, never off an extractor filename or an OCR caption, and
that read is only worth anything if the crop it was made from can be opened again. All eleven
PNGs here were cut at feature-006/t6 (2026-10-18) out of nine 500 ppi renders, and **every one
of them has its exact `--box` recorded below**. The boxes were written to
`books/tmp/f06t6/crops.json` as the crops were cut and are copied here so the record does not
live in a gitignored file. That file records nine crops and not eleven: the two folio-token crops
below were cut after it was written and were never added to it, which is why the QC rows for the
published figures say eleven and point here rather than at it.

Page mapping used throughout (§0.4): **printed page = scan file page − 18**. So scan file 306 is
printed p. 288, scan 415 is printed p. 397, scan 418 is printed p. 400, scan 420 is printed
p. 402, scan 421 is printed p. 403. The renders are `pdftoppm -r 500` of
`books/pdf-pages-tesla-1894/page-NNN.pdf`, 1856 x 3226 px a page, the native resolution of the
image embedded in that page PDF. They are in
`books/tmp/f06t6/scan-{306,307,415,416,417,418,419,420,421}-500.png`, not committed (regenerable
with `books/tools/fig_crop.py --printed <N> --view --view-ppi 500`). Seven of the nine were opened
against a plate; scans 416 and 417 were rendered only to read their printed captions in the text
layer, which is the weakest read in this file and is marked as such wherever it was used.

## The three figures this page publishes

They live in the `website` repo, not here, because that is where the page loads them from. Each
is the whole plate with its own printed `FIG. N.` line inside the crop, which is the §6.6
requirement; each is named by printed page as §6.2.5 asks. The widths and heights in the
frontmatter are these files' actual pixel sizes.

| published file | px | bytes | sha256 | cut from the 500 ppi render at box |
|---|---|---|---|---|
| `website/assets/tesla1894/p288-figs163-164.webp` | 880x1450 | 84,776 | `5312aff240f8cbf9341a7ba358cf7e4da3b52d0a41d21cee61230e2b68350595` | x 515, y 980 to x 1395, y 2430 of scan 306, levels stretched (`fig_crop.py --autocontrast`) |
| `website/assets/tesla1894/p397-fig210.webp` | 785x939 | 54,204 | `0aaa8e1d9fea89a618b90b8f572e48ffb862ecccfee444229a5883cbe18932c7` | x 608, y 1187 to x 1393, y 2126 of scan 415 |
| `website/assets/tesla1894/p403-fig218.webp` | 530x1110 | 55,856 | `7f411a57a6f4a09c844851d7ad17dc2990ce58b4023eb206be490b4d8cc4f57d` | x 235, y 1120 to x 765, y 2230 of scan 421 |

Total 194,836 bytes, inside the 400 KB figure budget every article in this series works to.

They supersede, and the QC rows say so:

- `p288-figs163-164.webp` supersedes `p306-fig1-fig163.webp`, a 300 ppi band of the same two
  plates with **neither printed caption inside it** (its own `caption_ok` was already `no`).
  Measured by matching that file back onto the render: it covers x503-1398 y969-2392, so both
  plates are inside it whole, and the print sets the two captions at y2369-2417, which means the
  crop ends through the middle of the letters.
- `p397-fig210.webp` supersedes `p415-fig1-fig210.webp`, whose number is right but whose printed
  caption is outside the crop. Measured: that file covers x347-1403 y1174-2072, which is wider than
  the plate (x620-1380) and contains the whole plate including the small detail at its lower right;
  the plate's last ink row is y2047 and the caption's first is y2072, which is exactly where the
  crop ends. An earlier pass of this task wrote that the old crop cut off that lower-right detail.
  It does not, and the claim is replaced here with the measurement instead of being left beside it.
- `p403-fig218.webp` supersedes nothing usable: `p421-fig1-fig218.webp` is a 300 ppi band that
  holds Fig. 218 **and** Fig. 219 side by side and takes its number from body type, not from a
  caption. Measured: it covers x213-1504 y1097-2183, and the print sets the two captions at
  y2173-2226, so its own bottom edge falls inside them.

## The eleven evidence crops committed here

| file | sha256 | box in the 500 ppi render | what it proves |
|---|---|---|---|
| `p288-printed-caption-band-fig163-fig164.png` | `599e70f5610999ea0f1e29c2661c8e52e1fb2bc4fb4597c66261e26e3735db0c` | x 500, y 2345 to x 1400, y 2440 of scan 306 | printed p. 288 sets two plates side by side and captions them `FIG. 163.` (left, x 542-1003) and `FIG. 164.` (right, x 1179-1350). The extractor crop on disk carries neither. |
| `p289-bodyref-fig163-line.png` | `1121f1da9999e6672537c6b40a162376c2ee135cc66b4d7fc1c63573c5f17d1c` | x 39, y 889 to x 1704, y 981 of scan 307 | the body line on the next printed page reads `the occasion. In Fig. 163 a short tube TJ, sealed to another long` — the sentence that says what the two plates draw, and the second read of 163 in the volume. `TJ` is the scan's OCR of `T'`. |
| `p397-bodyref-fig210-line.png` | `5b5f94b4763fe3498b70dd6945c86ab5745898297d83cc41aecdb0a116502655` | x 49, y 384 to x 1698, y 475 of scan 415 | the body line above the plate reads `which were carried out by me in practice. Fig. 210 may serve` — the sentence the plate belongs to, and the second read of 210 on that page. |
| `p400-printed-caption-fig214.png` | `712d321c9696e3597ffb4ff75aaca41be2d39b6783182676b7e5bb4307178485` | x 835, y 1416 to x 1148, y 1500 of scan 418 | the printed caption under the **upper** plate on printed p. 400 is `FIG. 214.`. Both extractor crops on that page are named `fig215`, so one of them is wrong, and this says which. |
| `p400-printed-caption-fig215.png` | `f47f146ea92f1857f3ffcb851b2dd74c3b80d09520bc6e49b7aefad0f69d0370` | x 836, y 2565 to x 1150, y 2649 of scan 418 | the printed caption under the **lower** plate is `FIG. 215.`. That page carries two plates and two captions; the extractor gave both crops the second number. |
| `p401-bodyref-fig215-line.png` | `d45c06d573a5bed935d1908806fdb2e4df42a96aded204ff246326c74087aad9` | x 29, y 1192 to x 1683, y 1283 of scan 419 | the body line on the next printed page reads `is roughly illustrated in Fig. 215. In this case luminosity was` — the sentence that names the parts `B` and `T` drawn on printed p. 400, and the reason the lower plate's letters are not a guess. |
| `p402-printed-caption-band-fig216-fig217.png` | `3fa09ece4535f47e3c6c06260d839119b663398f8060e21f251c531de9d60be3` | x 560, y 2600 to x 1480, y 2705 of scan 420 | printed p. 402 captions two plates in one band: `FIG. 216.` at x 591-785 and, at x 1290-1456, the print's `FIG. 217.`, which the text layer returns as `FIG. 2V,`. The extractor made one crop for both. |
| `p402-folio-token.png` | `8f830417481e931721f2c4f6094d8ddaeaf066b1f0d58a8315701d397cdd7e5a` | x 100, y 80 to x 420, y 190 of scan 420 | the folio on this page is degraded in our scan: the ink is not legible enough to read a last digit from, and the text layer returns `403`. The sequence either side (scan 419 folio `401`, scan 421 folio `403`, scan 422 folio `404`) and the §0.4 rule put this page at printed **402**, which is what every citation on this page uses. Recorded so nobody re-derives a page number from this token. |
| `p403-printed-caption-band-fig218-fig219.png` | `d1a0ef57790a79638bef700931510d33f282327cf7a949d76a39405bc1acf09f` | x 380, y 2145 to x 1310, y 2245 of scan 421 | printed p. 403 captions two plates in one band: `FIG. 218.` at x 403-588 (left) and `FIG. 219.` at x 1103-1287 (right). Figure 3 of this page is the left-hand plate alone. |
| `p403-bodyref-fig218-line.png` | `7af5c8fa4a91260d6d6389365c47527e90670a26609dd4afa1d649d2fb395e67` | x 39, y 2676 to x 1694, y 2779 of scan 421 | the body line under the plates reads `bulb, Fig. 218, surrounded by a primary spiral, was contained in a bell-jar,` — the sentence the plate belongs to, on the same printed page as the plate, and the second read of 218 there. |
| `p403-folio-token.png` | `b4708f3432533658705f7eb58a92a8c3da61db709509c2986fa205f5f2a35c67` | x 1480, y 100 to x 1780, y 210 of scan 421 | the folio on the next page reads `403` cleanly, which is the control that makes the degraded token above legible-by-sequence rather than by guess. |

Each of the eleven was opened and read at feature-006/t6, and each says what the frontmatter
record in `../article.md` claims it says.

## The figure map of the two passages this page is about, as the print sets it

Ten plates in the nine pages of chapter XXXII, and two on the lecture page. Every number below
was read off the printed caption in a 500 ppi render **except** the two rows marked *(text layer)*,
which were read from the text layer at the coordinates given and are not settled visually. The
plate-ink column says *not measured* on those same two rows for the same reason.

| printed page | scan | printed captions on the page | plate ink in the 500 ppi render | whose text it is |
|---|---|---|---|---|
| 288 | 306 | `FIG. 163.` x 542-1003 y 2369-2417; `FIG. 164.` x 1179-1350 y 2369-2417 | left x 530-730 y 997-2359; right x 1160-1380 y 993-2359 | Tesla's own February 1892 lecture |
| 397 | 415 | `FIG. 210.` x 820-1013 y 2061-2117 | x 620-1381 y 1199-2047 | Tesla's July 1891 article |
| 398 | 416 | *(text layer)* `FIG. 211.` x 883-1077 y 916-979; `FIG. 212.` x 876-1069 y 2597-2660 | not measured | Tesla's July 1891 article |
| 399 | 417 | *(text layer)* `FIG. 213.` x 795-981 y 1853-1908 (one caption only) | not measured | Tesla's July 1891 article |
| 400 | 418 | `FIG. 214.` x 895-1089 y 1431-1487; `FIG. 215.` x 896-1090 y 2580-2635 | upper x 56-1754 y 621-1496; lower x 493-1483 y 1898-2645 | Tesla's July 1891 article |
| 402 | 420 | `FIG. 216.` x 591-785 y 2637-2685; `FIG. 217.` x 1290-1456 y 2629-2678 (text layer: `FIG. 2V,`) | left x 460-890 y 2107-2611; right x 1210-1540 y 2012-2610 | the abstract of J. J. Thomson's paper, whose display heading is on this same page at y 1567-1643, above both plates |
| 403 | 421 | `FIG. 218.` x 403-588 y 2173-2222; `FIG. 219.` x 1103-1287 y 2178-2226 | left x 240-760 y 1140-2158; right x 910-1480 y 1560-2135 | the abstract |

Printed pp. 396, 401, 404, 405 and 406 carry no printed caption at all, and printed pp. 285 to
287 and 289 to 293 carry none either: the two plates on printed p. 288 are the only art on the
pages that hold the tube-in-hand passage. Printed pp. 251 to 260, which is where the carborundum
lamp passage sits, name no figure in the text layer and produced no extractor crop; that is a
text-layer measurement, and §6.6's own lesson from feature-006/t2 is that a zero from
`extract_figures.py` is not proof a page has no plate, so the claim this page makes is only that
it publishes no lamp figure and why.

## What the extractor record gets wrong about these pages

Eight crops cover the ten plates of chapter XXXII, and the print contradicts the number in four
of the eight:

1. **printed p. 400.** Both crops are named `fig215`. The page prints `FIG. 214.` under the
   upper plate and `FIG. 215.` under the lower. `p418-fig1-fig215.webp` is Fig. 214.
2. **printed p. 402.** One crop covers two plates, and the second caption reads `FIG. 2V,` in the
   text layer. The print says `FIG. 217.`
3. **printed p. 403.** One crop covers two plates, and its name came from a body-type reference
   (`manifest.csv` caption field: `stantly extinguished by the presence of an electro-magnet.
   Another exhausted bulb, Fig. 218, surrounded by a primary spi`), not from a caption.
4. **printed p. 399.** The crop is named `fig214`. That page's only printed caption is
   `FIG. 213.`; there is no `FIG. 214.` caption on it. Fig. 214's plate is on the next page. This
   case is a text-layer read and the plate was never opened, which is said rather than skipped,
   because the same text layer returns `FIG. 2V,` for the print's `FIG. 217.` two pages later and a
   read that mis-sets a caption that way cannot settle a number by itself.

Printed p. 398 is the fifth case and was **not** re-opened, because this page publishes nothing
from it: both crops there are named `fig212` while the page prints `FIG. 211.` and `FIG. 212.`.
That read is from the text layer with coordinates, and the QC rows for those two files now say
the number is unsettled rather than corrected.

## Re-deriving a crop

Every box used at feature-006/t6 is in the tables above, so any crop here or any published crop
can be re-cut identically without re-reading the page:

Run these from `books/`. `--view-ppi 500` for the preview is not the default (the default is 100),
and `--ppi 500` for the crop is not the default either (the default is 400). Omit `--ppi 500` and
the tool renders the page at 400 ppi and treats the box as 400 ppi coordinates, which silently
cuts a *different, larger* piece of the page at the same pixel size. That was hit at this task,
not written from the docs: the first re-cut came out 880x1450 like the published file and mean
101 levels away from it, because the flag was missing.

    python3 tools/fig_crop.py --printed 402 --view --view-ppi 500              # whole page to look at
    python3 tools/fig_crop.py --printed 402 --box 560,2600,1480,2705 --ppi 500 \
        --out books/tmp/recheck-402-captions.png

To re-make a published crop exactly: same box, `--ppi 500`, and the tool's own webp encoding
(`quality=92`). That reproduces all three files byte for byte. This was tested rather than
asserted: each published file was re-cut from its recorded box and re-encoded, and all three
re-cuts came out identical to the committed files, sha256 included.

One caution for anyone re-cutting the published crops: the boxes above are the plate plus its
printed caption and a margin. The figure ink bboxes alone, without the caption, are in the map
table above. Cutting to those drops the printed caption out of the crop, which is the one thing
§6.6 requires the published figure to carry. For the printed p. 288 pair the plates are dark
halftones: cut them with `--autocontrast`, as this task did, or they read as two black bars.
