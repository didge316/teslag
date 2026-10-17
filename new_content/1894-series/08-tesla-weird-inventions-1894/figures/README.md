# Article 08 figure evidence — what was read off the print, and where the proof is

This directory exists so the figure verification for this article survives its working
directory. `books/tmp/` is gitignored and gets cleared; §6.6 requires every figure number to
be read off the printed page in the scan, never off an extractor filename or an OCR caption,
and that read is only worth anything if the crop it was made from can be opened again. All
eight PNGs here were cut at feature-006/t2 (2026-10-17) out of four 500 ppi renders, and
**every one of them has its exact `--box` recorded below**, which is the thing feature-005/t6
could not do for article 06 and what feature-005/a06-figrec had to reconstruct by hand. The
boxes were written to `books/tmp/f06t2/crops.json` as the crops were cut; they are copied here
so the record does not live in a gitignored file, and each crop was re-cut from its box after
the first pass and came out byte-identical (see "Re-deriving a crop").

Page mapping used throughout (§0.4): **printed page = scan file page − 18**. So scan file 428
is printed p. 410, scan file 436 is printed p. 418, scan file 440 is printed p. 422, scan file
448 is printed p. 430. The renders are `pdftoppm -r 500` of
`books/pdf-pages-tesla-1894/page-NNN.pdf`, 1856 x 3227 px a page, the native resolution of the
image embedded in the page PDF — the same size feature-005/a06-figrec measured on four pages of
this same scan. They are in `books/tmp/f06t2/scan-p{428,436,440,448}-500ppi.png`, not
committed (2.2 MB each, regenerable with `books/tools/fig_crop.py --printed <N> --view
--view-ppi 500`).

## The three figures this page publishes

They live in the `website` repo, not here, because that is where the page loads them from.
Each is the whole plate with its own printed `FIG. N.` line inside the crop, which is the §6.6
requirement; each is named by printed page as §6.2.5 asks. The widths and heights in the
frontmatter are these files' actual pixel sizes.

| published file | px | bytes | sha256 | cut from the 500 ppi render at box |
|---|---|---|---|---|
| `website/assets/tesla1894/p410-fig220.webp` | 1115x629 | 21,236 | `30a0d64a1841cf4357ae59381ea502fa2cd46e73e65c4a1c38f01e4b8db1a419` | x 396, y 1291 to x 1511, y 1920 of scan 428 |
| `website/assets/tesla1894/p418-fig227.webp` | 933x496 | 40,390 | `adf89bbad4ce82ea53aef1b845cb7562d0e87c485c1585c247c802862546c65d` | x 220, y 1538 to x 1153, y 2034 of scan 436 |
| `website/assets/tesla1894/p430-fig242.webp` | 1169x768 | 73,692 | `40e6a706c34dfaa4384dd5bf3c789a1dcfabe6b1ea64189d5d73d08d02a04072` | x 196, y 1189 to x 1365, y 1957 of scan 448 |

Total 135,318 bytes, inside the 400 KB per-article figure gate. The three crops supersede
`p428-fig1-fig220.webp` and `p448-fig1-fig243.webp`, which are 300 ppi extractor crops, one of
them without a printed caption and the other a two-figure band named for the smaller of the two
plates it holds; both keep their `manifest_qc.csv` rows, with notes saying what is wrong with
them and which file replaces them. `p418-fig227.webp` supersedes nothing, because there was
never a crop of printed p. 418 — see "Why printed p. 418 has no row in manifest.csv" below.

## The evidence crops committed here

| file | sha256 | box in the 500 ppi render | what it proves |
|---|---|---|---|
| `p410-printed-caption-fig220.png` | `4af95c29d4e08e89cff8f6def235efb7ac6e2e27497300e096d97d207c041fda` | x 845, y 1862 to x 1066, y 1924 of scan 428 | the printed caption under the single plate on printed p. 410 is `FIG. 220.` — the number figure 1 of this page carries. |
| `p410-bodyref-fig220-line.png` | `5d21b039619cc7da352c29483f0ddac21f6e1376e644cf3b84cae27c374ffa4f` | x 199, y 853 to x 1754, y 938 of scan 428 | the body text on the same printed page begins `In Fig. 220, A designates a generator of alternating currents,` — the in-text cross-reference that ties the plate to the parts named in the caption, and the second independent read of the number 220 on that page. |
| `p418-printed-caption-band-fig227-fig228.png` | `791c0854e635685ac52f2b829254c80518f2e0fce5c382e239f3c6286b70c49a` | x 600, y 1930 to x 1580, y 2040 of scan 436 | printed p. 418 sets two engravings side by side and captions them `FIG. 227.` (left) and `FIG. 228.` (right). Figure 2 of this page is the left-hand plate. This band is the first evidence that any plate exists on printed p. 418 at all: no crop and no manifest row for that page existed before this task. |
| `p422-printed-caption-fig230.png` | `96013d9b3e440e2a01af1676baa41e72d38507a87749fcffb12697e5f1fa92f4` | x 865, y 2178 to x 1090, y 2240 of scan 440 | the printed caption under the meter plate on printed p. 422 is `FIG. 230.`, not the `FIG. 280.` the text layer of that page returns. Settles the number for the one figure this page would have used for entry 3. |
| `p422-bodyref-fig230-line.png` | `e16737471511809ff4c7f0b437ddc2b18333fc60e1036916350d7819e286818b` | x 220, y 760 to x 1780, y 838 of scan 440 | the body text on the same printed page reads `In Fig. 230 the conductors c c' are connected in parallel, the` — the second read of 230 on that page, in body type, against the text layer's `FIG. 280.` in the caption slot. |
| `p430-printed-caption-band-fig242-fig243.png` | `0ef3e5f412c480c04620d96a5047e5313caf7b0ad93ef46013891d44ac5293ee` | x 660, y 1880 to x 1660, y 1960 of scan 448 | printed p. 430 captions the left plate `FIG. 242.` and the right one `FIG. 243.`. Figure 3 of this page is the left-hand plate; the extractor crop on disk is named for the right one. |
| `p430-bodyref-fig242-line.png` | `8c697fa3c8c76303a7e2c1297103f43affbd8b098aa9e5519fc1a727b7dc6840` | x 198, y 1054 to x 1752, y 1132 of scan 448 | the line above the plates reads `Fig. 242 is a central vertical longitudinal section of the com-` — the sentence that says which of the two plates is the generator, set above them because the illustration block breaks it. |
| `p430-bodyref-fig243-line.png` | `c7fa298a970123c35c5c6f5fa272192ed941d39865af196ab46217bd0f03604c` | x 135, y 2012 to x 1746, y 2090 of scan 448 | the line below the plates continues it: `plete apparatus and Fig. 243 is a cross-section of the magnetic`. Together with the crop above this is the read that says Fig. 242 is the whole apparatus and Fig. 243 is the armature core in section, which is the opposite of what the file name on disk implies. |

Each of the eight was opened and read at feature-006/t2, and each says what the frontmatter
record in `../article.md` claims it says.

## Why printed p. 418 has no row in manifest.csv, settled at feature-006/t2

The gap named in the feature-006/t0 lesson ("entry 2's Figs. 227 and 228 have no crop and no
manifest row") is not a lost crop. `extract_figures.py` run over scan 436 at both 300 and 500
dpi returns **0 figures for that page**, so no row was ever written and no crop was ever cut.
The reason is the extractor's own masking: it masks every row the text layer claims, and on this
page the two plates sit inside the claimed text block, so the plates were masked away. The ink is
there: in the 500 ppi render the two plates run y 1474 to 1941, x 230 to 1143 for the left and
x 1233 to 1730 for the right, and both printed captions sit under them at y 1945 to 2024. That
is why the caption band crop above is the one that proves the plates exist — the plates
themselves were never extracted, so there is nothing older to compare against.

This is worth recording as a tool limit, not just an article-08 fact: any page where an
engraving sits inside a two-column text block can come back as zero figures from
`extract_figures.py`, and a zero from that tool is not evidence that a page has no plate.

## Three reads that contradict the record on disk, settled against the print

1. **`FIG. 230.` on printed p. 422, not `FIG. 280.`** The text layer puts `FIG. 280.` in the
   caption slot; the print says 230, and the body type on the same page says 230 twice over
   (the two crops above). It is the same 3-for-8 confusion this scan makes on printed p. 425
   (`Fig. 281` in body type where that page's three printed captions are `FIG. 231.`,
   `FIG. 232.`, `FIG. 233.`) and on printed p. 427 (`FIG. 287.` where the sequence is 237, 238,
   239). Those two pages were not re-opened — this page publishes no figure from either — but
   `manifest_qc.csv` row 158's note that "Figure number 281 is genuine for p.425" is now marked
   in that file as not settled, so nobody takes it as one.
2. **`manifest_qc.csv` row 149's subject line for Fig. 220.** It reads "two lamps in opposite
   arms of a loop with a battery and switches". The print contradicts three of those four words:
   `A` is a generator of alternating currents (the body-type line committed above), the two
   devices in the arms are the direct-current sources the chapter calls generators and then
   current sources, and no word for a lamp, a meter, an indicator or a switch appears anywhere
   in the four printed pages of chapter XXXIII (scans 427 to 430 searched). The row's note now
   says so and names the file that replaces the crop.
3. **`manifest_qc.csv` row 156's subject line for Fig. 229.** It reads "good
   coherer/retcoherer illustration". Fig. 229 is a meter: printed p. 421 says `Figs. 229 and 230
   illustrate two forms of such a meter` and then describes `G` as a direct-current generator and
   `L L` as the conductors. Row 157 (Fig. 230) is not wrong so much as incomplete — it omits the
   galvanometer `G` and both resistance coils, which are most of that drawing, and describes the
   contact bank `T` as part of a tube. All three notes are corrected in that file at this task.

What was **not** re-opened, and it is not an oversight: entries 5 to 9's App. C candidates
(Figs. 247, 266, 281, 283, 290) and the meter plate of entry 3. Nothing about them was
contradicted by anything read here, §6.6 limits re-opening to figures whose evidence is missing
or contradicted, and this page is at three figures, which is §6.6's ceiling. Their state — crops
on disk, QC notes that are hints, printed-caption numbers never read — is recorded in the
frontmatter block "NOT RE-OPENED" in `../article.md`.

## Re-deriving a crop

Every box used at feature-006/t2 is in the two tables above, so any crop here or any published
crop can be re-cut identically without re-reading the page:

    python3 books/tools/fig_crop.py --printed 410 --view --view-ppi 500        # whole page to look at
    python3 books/tools/fig_crop.py --printed 410 --box 845,1862,1066,1924 --ppi 500 \
        --out books/tmp/recheck-410-caption.png

To re-make a published crop exactly, cut the box and encode it as PIL writes webp at
`quality=88, method=4`; that reproduces all three files byte for byte.

This was tested rather than asserted: after the first pass, the three published crops and the
eight evidence crops were re-cut from the boxes above out of the same four renders. All eight
PNGs came out **byte-identical** to the committed files. The three published crops are lossy
webp, so a bare re-crop does not reproduce their bytes; re-encoded with the parameters used at
this task, `quality=88, method=4`, all three come out byte-identical too, and their sizes
(21,236 / 40,390 / 73,692 bytes) match the table above. So every figure on this page can be
re-made exactly by anyone, which is more than article 06's record claims — five of its eight
evidence crops have no recorded box. Per §6.6, only a figure whose evidence is missing or
contradicted should be re-opened at all; these boxes exist so that a later pass can look at a
settled read without paying for a re-render, not so that a settled read gets re-litigated.

One caution for anyone re-cutting the published crops: the boxes above are the plate plus its
printed caption and a 10 px margin. The figure ink bboxes alone, without the caption, are Fig.
220 x 406-1501 y 1301-1833; Fig. 227 x 230-1143 y 1548-1888; Fig. 228 x 1233-1730 y 1474-1929;
Fig. 230 x 269-1678 y 1145-2171; Fig. 242 x 206-1355 y 1199-1903; Fig. 243 x 1431-1707
y 1513-1680. Cutting to those instead drops the printed caption out of the crop, which is the
one thing §6.6 requires the published figure to carry.
