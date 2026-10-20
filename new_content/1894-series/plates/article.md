---
title: "Tesla 1894 Plates: 72 Engravings, Cited Page by Page"
slug: tesla-1894-plates.html
pretty_slug: /tesla-1894-plates
description: "72 engravings from the 1894 first edition of Tesla's book, each cited to the printed page it sits on and numbered as the book numbers it."
keywords: [nikola tesla 1894 engravings, tesla 1894 book illustrations, tesla patents diagrams 1894, public domain tesla engravings, tesla book plates download, martin inventions researches writings 1894 figures]
# PUBLISH DATE. Not one of the twelve article dates: the asset pages are not in the
# articles.html grid, so the one-page-per-date cadence settled at
# feature-006/a08-wirecommit does not bind them. It is still the next free date
# after the last wired article (12 takes 2026-10-26), which keeps every page on this
# series on a distinct date and keeps the sequence readable.
date_published: "2026-10-27"
date_modified: "2026-10-27"
primary_query: nikola tesla 1894 engravings
# tid: the asset pages belong to the hub's family, not to a numbered article, so the
# clickbank tag is the hub's. qa_page.py accepts 1894_NN or 1894_hub and nothing else.
tid: "1894_hub"
og_image: assets/og/tesla-1894-plates.webp
standfirst: "Seventy-two engravings and photographs from the 1894 first edition, each one cited to the printed page the book puts it on, with the figure number the book prints under it. Free to reuse, and the page rule is stated on the page."
cta:
  text: "The 1894 book draws machines it never measures and never costs. If you are sizing a real supply for a shed, a workshop or a small off-grid structure, the plans we recommend come with a parts list and a straight answer about output."
  href_suffix: "1894_hub"
pages_used: [14, 378, 379, 392, 393, 478, 482, 483]
sources:
  - text: "The selection record: new_content/1894-series/plates/selection.json. It carries every plate on this page with its printed page, its printed figure numbers, its chapter, its quality grade, the manifest row it came from, and how its caption was read, plus every row the rules rejected and the reason. books/tools/plates_gallery.py --select writes it, and re-running that command reproduces this page"
  - text: "The QC pass those rows come from: manifest_qc.csv, in the website/assets/tesla1894/ folder, 223 catalogued crops, each with a verdict, a subject line written while looking at the crop, an A/B/C quality grade, and whether the aspect and the printed figure number were checked. That file is the §6.2 pass, not this task's work, and this page only reads it"
  - text: "The chapter map: books/extracted/chapters-1894.json, read off the book's own printed contents pages (the scans the running heads are not), which is what lets a plate be named by chapter as well as by page"
  - text: "The caption reading: books/tools/extract_figures.py re-derives the extractor's own ink band at 300 ppi, and the caption is taken from the strip of print between that band and the next figure on the page, which is the only positional way to read a caption when the text layer of the same page also mentions figures inside body paragraphs"
  - text: "The three plates shown in this article's own text, at printed pp. 378, 392 and 478, are three of the 72 on the grid below and carry the same captions here as there, so nothing is said twice in two different ways"
  - text: "The word 'accompanying', which the scan prints as 'aecompaning' on printed p. 375 and as 'accompanying' elsewhere: the quotes on this page are taken from the pages where the scan is clean, and every one of them was re-grepped from books/extracted/tesla-1894-plain.txt and pinned to its printed page before it was written here"
---

This page carries 72 engravings and photographs from the 1894 first edition of
*The Inventions, Researches and Writings of Nikola Tesla*, edited by Thomas
Commerford Martin. Every plate on it is cited three ways: the figure number the
book sets under the plate, the page number the book prints in its own corner, and
the chapter the book puts it in. None of them is captioned from a file name.

> Public domain (1894 imprint). Reuse freely; a credit line is appreciated.

The grid is grouped by the four parts of the volume and, inside each part, by
chapter and printed page, so it reads as the book rather than as a pile of
pictures. Each plate links to the full file, and the whole set comes as one ZIP.

## Citing a Plate From This Page

The credit line we would like, and the one the ZIP's README prints:

> Plate, Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla
> (1894), p. 378.

The number in that line is the number the book prints, not the number of the page
of the scan we worked from. Our scan runs eighteen leaves ahead of the printed
folios, so the printed page is the scan file number minus 18. That rule is worth
stating because it is the most common way a citation like this goes wrong: a file
called p396 in a folder of page scans is the plate the book prints on page 378,
and a citation that says 396 sends a reader to a page of the volume that carries
different writing altogether.

Every caption on this page states the printed page. The file names behind the
files are a different matter, and they are kept in the selection record rather
than in front of the reader, because a file name records where a crop was cut
from, which is not the same fact as what a plate is.

## The Book Names Its Own Plates

The volume points at its own engravings in its own prose, which is where the
figure numbers on this page come from. On printed p. 378, in the chapter on high
frequency and high potential currents, the text says: "Figs. 204 and 205
illustrate a machine in which the armature conductor and field coils are
stationary, while the field magnet core revolves" (1894, p. 378). The next
sentence separates the next plate from it: "Fig. 206 shows a machine embodying the
same plan of construction, but having a stationary field magnet and rotary
armature" (1894, p. 378).

![A 1894 engraving, Fig. 205, printed p. 378: plan view of a machine with two square coil groups on a frame, a shaft and a flywheel](/assets/tesla1894/p396-fig1-fig205.webp) "Fig. 205 - printed p. 378 - Ch. XXIX - Plan view of a machine: two square coil groups on a frame with a shaft and a flywheel"

Chapter XXX does the same thing about the two plates that open it. Tesla writes
that he "devised various forms" of apparatus "of which two are illustrated in the
accompanying engravings" (1894, p. 392), and then, one printed page later, names
the second one: "Another form of apparatus is illustrated in Fig. 209" (1894, p. 393).
The footnote on that first page says where the chapter came from: "Article by Mr.
Tesla in The Electrical Engineer, N. Y., May 6, 1891" (1894, p. 392). That is also
why the plates do not look like one set. They came in with the articles they were
drawn for, from several magazines and several years, and the volume reprinted
them.

![A 1894 engraving, Fig. 208, printed p. 392: a ring lined inside with two sets of tin-foil coatings, and inside it a cylinder carrying the matching coatings, both led out to two ring terminals](/assets/tesla1894/p392-fig208.webp) "Fig. 208 - printed p. 392 - Ch. XXX - A ring marked A lined on the inside with two sets of tin-foil coatings marked a and b, and inside it a cylinder marked B carrying coatings marked a1 and b1, the two sets led out to two ring terminals marked T with + and - signs; dashed field lines drawn through both"

The volume is also the source for the plainest caution about using these plates as
evidence. The Appendix chapter that reprints the World's Fair exhibit says of the
models on its own table: "All these models shown represent early work, and the
enlarged engravings are made from photographs taken early in 1888" (1894, p. 483).
It then says the plate fails some of them: "There is a great number of other
models which were exhibited, but which are not brought out sharply in the
engraving, Fig. 297" (1894, p. 483). A plate is a plate. The book says so, on the
page that discusses the very engraving reproduced below, and a caption that
promises more than the print gives is not a citation, it is a claim.

![A 1894 halftone, Fig. 297, printed p. 478: a long table of motors, rings and coils at the World's Fair personal exhibit, with a railing in front](/assets/tesla1894/plate-p478-fig297.webp) "Fig. 297 - printed p. 478 - Ch. XLII - Long table of motors, rings and coils at the World's Fair exhibit, railing in front, 'Electrical Engineer' credit lower right"

The extractor that cut our crops named each one for the figure string nearest the
crop in the scan's text layer, and a page that mentions figures in its body
paragraphs confuses that. Printed p. 14 is the clearest case: the plate the
extractor cut from that scan page is captioned FIG. 7. and FIG. 7a. by the book,
while the same page's text layer contains a body sentence that mentions Fig. 9,
and the file came out called fig9. A caption read from the strip of print under
the plate gets it right; a caption read from the file name does not.

## How These 72 Were Chosen

The plates were catalogued before they were chosen. The file called manifest_qc.csv,
in the website/assets/tesla1894/ folder of this site, holds 223 crops, each with a
verdict, a subject line written while looking at the crop, an A/B/C quality grade,
and a note of whether the aspect and the printed figure number had been checked.
This page reads that file and applies five rules, and the rules are printed here
because they are what makes the page citable rather than merely pretty.

- The row must be a keeper and the plate must be A or B quality. C-grade crops are
  out: they are the ones the QC pass found badly scanned, badly cropped or badly
  exposed.
- The printed figure number must be settled. A row that flags its own number as
  mis-read, contradicted or unsettled cannot carry a number in a caption, so it
  carries no plate here.
- The file must be one of the book's own figures. Page-scan crops and downloaded
  patent sheets live in the same folder and are not book engravings, so they are
  out.
- One plate per printed figure. Where an automatic crop and a later hand crop cover
  the same printed figure, the hand crop wins, because it was cut after the page
  was opened at 400 to 500 ppi and its notes name the scan it was read from.
- A per-chapter cap. Without it the gallery would be chapter III, which is dense
  with diagrams, and the rest of the volume would be a footnote.

Then the captions. For each surviving plate the tool re-derives the ink band the
extractor cut, at the same 300 ppi and in the same order, and reads the text lines
in the strip of print between that band and the next figure on the page. A line
counts as a caption only if it is nothing but a caption: a body sentence that
happens to begin with a figure word is not one. The book sets its captions in small caps and the scan's text layer mangles them,
so the line the print sets as FIG. 1. arrives as Fie. l., and the line the print
sets as FIGS. 45, 46 and 47. arrives as Fms. 45, 46 and 47.; the reader
normalizes only the letter-for-digit confusions this scan actually makes, and the
selection record keeps each line exactly as the layer gave it, so every
normalization can be checked against the print it came from. Where the strip under
a plate holds no caption line at all, the plate is left out rather than guessed
at.

What that produced, stated as counts so it can be re-run and argued with: of the
223 catalogued crops, 4 are not book figures at all, 129 fail the rules above
(72 because their printed figure number was never read correctly, 29 because they
are C-grade, 15 because no caption line sits under them, 7 because their own QC
note leaves the number unsettled, 5 because the QC pass marked them keep-tight or
drop, 1 because the caption line is there with its number unreadable), 90 pass,
5 of those are second crops of a figure already in the pool, and the 85 unique
printed figures are capped to the 72 on this page. They cover 30 chapters across
all four parts of the volume: 24 in Part I, 23 in Part II, 21 in Part III, 4 in
the Appendix. 66 are graded A and 6 are graded B. 19 are hand crops cut against
the print at 400 to 500 ppi. 17 carry a figure number different from the one their
file name claims, because the caption under the plate said something else. 21
captions name more than one figure, because the extractor's band runs across two
or three figures the page captions separately, and a caption that quietly drops
the other two is not describing the plate it is under.

The full record, plate by plate and rejection by rejection, is
new_content/1894-series/plates/selection.json, and books/tools/plates_gallery.py
writes it. Re-run the command and you get this page or you do not, which is the
whole point of writing it down.

{{GALLERY}}

## The Download

The ZIP is the same 72 plates at up to 1200 pixels on the long edge, as PNG, with
a README that lists each file against its figure number, printed page and chapter
and repeats the page rule and the licence:
[tesla-1894-plates.zip](/assets/tesla1894/tesla-1894-plates.zip), about 10 MB.

If you want to link to something rather than download it, this page is the thing
to link to: it is the set, the method and the citations in one place, and the
credit line above is the one we would like back. The pages this series writes
about the same volume are on [the articles index](/articles.html), including
[the World's Fair exhibit this gallery's Appendix plates came from](/tesla-worlds-fair-1893),
[the 1891 lecture that explains the diagrams in Part II](/rotating-magnetic-field-1888),
[the glowing tubes chapter, which reads the four different texts inside one chapter](/tesla-glowing-tubes-vacuum),
and [what Tesla actually wrote about free energy](/tesla-free-energy-what-he-said).
The hub of this series is being written last, so its twelve cards can be real.

{{CTA}}

{{SOURCES}}
