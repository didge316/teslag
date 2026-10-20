---
title: "Tesla 1894 Word Search: Free Energy 0, Perpetual 0"
slug: tesla-1894-word-search.html
pretty_slug: /tesla-1894-word-search
description: "The word search behind this series: the exact command, the counts for every term, and why one honest run returns four and another returns five."
keywords: [tesla 1894 free energy, nikola tesla perpetual motion 1894 book, inventions researches writings nikola tesla word search, tesla 1894 text layer, pyromagnetic generator 1894]
# PUBLISH DATE. Not one of the twelve article dates: the asset pages are not in the
# articles.html grid, so the one-page-per-date cadence settled at
# feature-006/a08-wirecommit does not bind them. It is the next free date after the
# plates page (2026-10-27), which keeps every page in this series on a distinct date.
date_published: "2026-10-28"
date_modified: "2026-10-28"
primary_query: tesla 1894 free energy never said
# tid: this page belongs to the hub's family, not to a numbered article, so the
# clickbank tag is the hub's. qa_page.py accepts 1894_NN or 1894_hub and nothing else.
tid: "1894_hub"
og_image: assets/og/tesla-1894-word-search.webp
card_image: assets/tesla1894/scan-p424-chapter-heading.webp
card_alt: "The opening of chapter XXXVI of the 1894 volume: CHAPTER XXXVI. then, in display type, THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS."
kicker: "The 1894 File · a linkable data page. Every count on it comes from a command, and the command is printed on the page."
standfirst: "This series says the 1894 book never uses the phrase 'free energy'. That is a countable claim, so here is the count: the command, the numbers, the printed page of every hit, and the one place where two honest runs of the same command return different totals."
cta:
  text: "The 1894 book reports machines it often never measures and never costs. If you are sizing a real supply for a shed, a workshop or a small off-grid structure, the plans we recommend come with a parts list and a straight answer about output."
  href_suffix: "1894_hub"
pages_used: [6, 424, 429, 496]
sources:
  - text: "The text being searched: books/extracted/tesla-1894-plain.txt, the text layer of our own scan of archive.org item inventionsresear00martiala. 518 page images, 506 page bodies, one file. The page images are numbered page-001 to page-518 and every body in the file carries its scan file number, so any count on this page can be walked back to a page image"
  - text: "The counting script: books/tools/count_terms.py. Its first three output lines print the command it was run with, the file it read, whether running heads were kept or dropped, and the page offset rule. Run twice today, 2026-10-20, once with the default index and once with --keep-furniture; both outputs are transcribed on this page. The raw-text counts quoted in the last section were taken with a plain case-insensitive count over the same file, with no normalisation, and they are labelled as such wherever they appear"
  - text: "The normalisation it borrows: books/tools/grep_quote.py, the same folding the quote checker uses, so a count on this page and a verified quote in an article are matched by one rule and not two"
  - text: "The page images behind the three figures: scans 442, 447 and 514 of the same item, rendered at 500 ppi and cut with books/tools/fig_crop.py, which prints the scan file and the printed page for every crop it cuts"
  - text: "The argument this data supports, on this site: Tesla on Free Energy: What He Actually Said. It prints the same counts, from a script in its own directory, and it is the page that draws the conclusion. This page draws none"
  - text: "A second use of the same method on a different phrase, on this site: the article on the cold flame, which whole-word searches this same text layer for 'cold flame' and 'cold fire' and gets 0 for both"
faq:
  - q: "Does the 1894 Book Contain the Phrase Free Energy?"
    a: "Not in our copy. 'free energy' returns 0 occurrences, whole-word and as a substring, in the text layer of a scan of the 1894 first edition, and so does 'free-energy'. The stem 'free energ' also returns 0, so a line-end hyphenation or a broken word would not hide a hit either. The two words on their own are common in the volume: 'free' appears 97 times on 73 printed pages and 'energy' 243 times on 119. The words are there. The phrase is not."
  - q: "Does a Count of Zero Prove Tesla Never Said It?"
    a: "No, and this page does not claim that. A zero here is a statement about one text: the 1894 first edition, edited by Thomas Commerford Martin, as its text layer reaches our machine. It says nothing about a later printing, a different edition, a lecture transcript, or anything Tesla wrote after 1894. What the zero does carry is a scope: the claim that this book says 'free energy' is refuted by this search, and the claim that Tesla 'believed in free energy' is untouched by it either way."
  - q: "Why Do Two Runs of the Same Command Give Four and Five?"
    a: "Because the default index drops running heads, bare page numbers and short all-capital display lines before it searches, and one of the five occurrences is a chapter title set in display type. Run with --keep-furniture the count is 5, on printed pp. 6, 424, 429 twice and 496. Run with the default index the chapter title on printed p. 424 is gone and the count is 4. Both numbers are true of the text each was taken from, which is why every count on this page names its index."
  - q: "Can I Run This Search Myself?"
    a: "The book is public domain and the scan is on archive.org as item inventionsresear00martiala, so the text is obtainable. Our script lives in a private working repository, so the exact code is not published. The rules it applies are stated in full on this page, including the page-number offset and the hyphen folding, and a search that follows those rules returns the same numbers. If you would rather have the numbers than the rules, the counts table and the printed page of every hit are here."
figures:
  # FIGURES. Three, each one the print of a page that is a row in the occurrence
  # table, so the figure and the row are the same claim in two media.
  #   assets/tesla1894/scan-p424-chapter-heading.webp 1641x240 27,378 bytes sha256
  #     ce1c60607d618edeba56b92179470c38cb9bada6bbbce43e752bb613ba7b286e
  #     cut from the 500 ppi render of scan 442 at box x139,y625 to x1780,y865, published 1:1.
  #     The box was set from the ink profile of the render, not from the text-layer bboxes: the
  #     text layer splits this heading into four fragments and its bboxes clip the glyph ink, so
  #     a box built from them cuts the tops off the next line. Rows with ink: 668-710 and
  #     783-826. The box starts and ends in whitespace, so the crop carries no part of any other
  #     line on the page.
  #   assets/tesla1894/scan-p429-pyromagnetic-line.webp 1639x139 39,690 bytes sha256
  #     ec0bf5b62f561ecd963481356b73fdbf2b484b1155a097bc5d1f9aa86cf5e63d
  #     cut from the 500 ppi render of scan 447 at box x83,y240 to x1722,y379, published 1:1.
  #     Same method: ink bands on that page are 245-307, 314-377, 380-443, 450-512, so the box
  #     ends at 379, in the gap between the second and third lines. Two complete lines, no
  #     partial line. Three earlier boxes (y1 420, 398, 390, 458) each carried a sliver of the
  #     next line and were discarded; the caption says what the crop carries.
  #   assets/tesla1894/scan-p496-index.webp 860x695 59,920 bytes sha256
  #     a6e5df9f695cf4ff5618ad3aa041c0adff35844b0f7776eb99076bc6c8bdebda
  #     already published by feature-008/a10-claims with the caption recorded in
  #     new_content/1894-series/10-*/figures/README.md row 221. Reused here, not recut, and the
  #     caption repeats that row's facts rather than writing a second account of the same image.
  # The word-search page is an asset page in the hub's family, so it carries the hub's tid and
  # no series_no. The kicker is front matter, not the KICKER constant: 'No. None of 12' would be
  # a false thing to print on a page that is not one of the twelve.
  - src: /assets/tesla1894/scan-p424-chapter-heading.webp
    alt: "Two lines of display type from printed page 424 of the 1894 volume: CHAPTER XXXVI. centered, and below it in larger small capitals THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS. with a hyphen inside both compounds"
    width: 1641
    height: 240
    caption: "Page-scan crop of the chapter heading on printed p. 424, cut from the 500 ppi render of scan file 442 at box x139,y625 to x1780,y865 and published at 1:1. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 424. Public domain. This is the fifth occurrence of the string 'magnetic generator' in the volume, and the one the default search index does not contain: the text layer reads the line in four fragments, 'CHAPTEK', 'THERMO-MAGNETIC', 'XXXVI.' and 'MOTORS AND PYRO-MAGNETIC GENERATORS.', and the index drops every one of them as a short all-capital line. The print hyphenates both compounds. The running text on printed p. 429 does not."
  - src: /assets/tesla1894/scan-p429-pyromagnetic-line.webp
    alt: "Two lines of running text from printed page 429 of the 1894 volume: Mr. Tesla has also devoted his attention to the development of, then a pyromagnetic generator of electricity based upon the following, with a superscript one after electricity"
    width: 1639
    height: 139
    caption: "Page-scan crop of the first two lines of the passage on printed p. 429 that names the machine, cut from the 500 ppi render of scan file 447 at box x83,y240 to x1722,y379 and published at 1:1. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 429. Public domain. The crop carries two complete lines and stops in the whitespace above the third; the column runs on below it. The print sets 'pyromagnetic' closed up, with no hyphen, and the footnote marker is the superscript one after 'electricity'. The text layer puts that marker inside the word, as 'electricity1', which is why the quotation on this page stops before it."
  - src: /assets/tesla1894/scan-p496-index.webp
    alt: "Printed page 496 of the 1894 volume: the folio 496 at the upper left and the start of the running head INDEX. cut off at the right edge of the crop, then the top of the left column of the volume's own index in display type, seven entries ending at the foot of the crop: Ozone Production of, Phenomena Produced by Electrostatic Force, Phosphorescence and Sulphide of Zinc, Physiological Effects of High Frequency, Polyphase Systems, Polyphase Transformer, and Pyromagnetic Generators with dotted leaders running to the page number 429"
    width: 860
    height: 695
    caption: "Page-scan crop of the top of the left column of the volume's own index, printed p. 496, from the folio down to the entry Pyromagnetic Generators and the number it gives, 429. The same published crop the article on free energy uses, with the same facts, so two pages describe one image in one way. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 496. Public domain. This entry is the fifth occurrence in the counts table and it is an index entry, not prose. The print sets this one closed up as well. The right column of the same page carries Thermo-Magnetic Motors and 424, and the G column two pages earlier carries Generators, Pyromagnetic and 429."
---

**Standfirst.** This series says the 1894 book never uses the phrase 'free energy'. That is a
countable claim, so it should be checkable without taking this site's word for anything. This page
is the working: the text that was searched, the command that searched it, the counts, the printed
page of every hit, and the one place where two honest runs of the same command return different
totals.

The argument built on these numbers is on
[Tesla on Free Energy: What He Actually Said](tesla-free-energy-what-he-said.html). This page is the
data behind that argument, and it draws no conclusion of its own. It exists so that a number quoted
anywhere in [The 1894 File](tesla-1894.html) can be traced to a command and a page.

## The Text Layer and the Offset Rule

The volume is Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla, with Special
Reference to His Work in Polyphase Currents and High Potential Lighting*, D. Van Nostrand, New York,
1894. Our copy is a scan of the archive.org item `inventionsresear00martiala`: 518 page images,
numbered page-001 to page-518, with a text layer. That text layer is extracted to one file,
`books/extracted/tesla-1894-plain.txt`, split into 506 page bodies, each marked with the scan file
number it came from.

The scan file numbers and the book's own page numbers are not the same thing, and the difference is
measured rather than guessed. **Printed page = scan file number minus 18.** You can check that
without our files: open scan 447 of the item and the page you get is the one the book numbers 429,
with 429 printed in its own corner.

The offset was checked across the volume. 402 body pages carry a bare page number in the text layer,
and 367 of those numbers equal the scan file number minus 18. The other 35 are misreads by the text
layer rather than disagreements about pagination: scan 226 is printed p. 208 and the layer reads its
folio as '308'; scan 446 is printed p. 428 and the layer reads '438'. Chapter opening pages carry no
folio at all, which is exactly what the offset rule is for. Scan 442 is printed p. 424, it opens
chapter XXXVI, and the only number on it is the chapter numeral.

## The Command, Verbatim

Two runs against one file, transcribed as they came out on 2026-10-20:

```
python3 books/tools/count_terms.py \
  'free energy' free-energy 'free energ' perpetual perpetu 'over unity' over-unity \
  unity free energy generator magnetic 'magnetic generator' pyro-magnetic \
  thermo-magnetic magneto dynamo radiometer inexhaustible

python3 books/tools/count_terms.py --keep-furniture 'magnetic generator'
```

The script prints its own conditions in the first three lines of its output: the command it was run
with, the file it read, whether running heads were kept or dropped, and the offset rule. A number
taken from that output carries its provenance with it.

What the script does to the text before counting, which is the part that decides whether a hit is
found at all, is the same folding the quote checker in this repository uses:

- ligatures folded, so the print's 'fi' ligature reads as 'fi'
- the long-s read as 's', and the OCR artefact that sets '8' for 'S' reversed
- curly quotes, dashes and ellipses replaced by their plain forms
- a hyphen at a line end removed along with the line break, so a word broken across two lines reads
  as one word
- a hyphen inside a compound removed between letters, so 'pyro-magnetic' and 'pyromagnetic' are the
  same string to the search. Letters only: a numeric range like 400-500 is left alone
- whitespace collapsed, everything lower case

Two counting rules are reported separately, because they answer different questions:

- **whole word**: the term stands alone, with a non-word character on each side
- **substring**: the term appears anywhere, including inside a longer word or compound

And two indexes, because the same text gives different totals depending on what is searched:

- **prose only**, the default: running heads, bare page numbers and short all-capital display lines
  are dropped before searching, so a chapter title is not in the text being counted
- **everything kept**, with `--keep-furniture`: the page text as it sits in the file

## The Counts

Both totals come from the runs above. 'Prose only' is the default index; 'everything kept' is
`--keep-furniture`. The last column is the printed pages where the substring form appears, taken
from the kept index, which is the wider of the two.

| term | whole word | prose only | everything kept | printed pages the substring appears on |
|---|---:|---:|---:|---|
| 'free energy' | 0 | 0 | 0 | none |
| 'free-energy' | 0 | 0 | 0 | none |
| 'free energ' | 0 | 0 | 0 | none |
| 'perpetual' | 0 | 0 | 0 | none |
| 'perpetu' | 0 | 0 | 0 | none |
| 'over unity' | 0 | 0 | 0 | none |
| 'over-unity' | 0 | 0 | 0 | none |
| 'unity' | 9 | 9 | 9 | 3, 4, 119, 142, 143, 156, 193, 327, 477 |
| 'free' | 49 | 97 | 97 | 73 pages, not listed here |
| 'energy' | 242 | 243 | 243 | 119 pages, not listed here |
| 'generator' | 203 | 231 | 243 | 91 pages, or 98 with display type |
| 'magnetic' | 215 | 273 | 288 | 140 pages, or 144 with display type |
| 'magnetic generator' | 0 | 4 | 5 | 6, 424, 429 twice, 496 |
| 'pyro-magnetic' | 5 | 5 | 7 | contents page (scan 17, no printed folio), 6, 424, 429 twice, 494, 496 |
| 'thermo-magnetic' | 3 | 3 | 5 | contents page (scan 17, no printed folio), 6, 424, 495, 496 |
| 'magneto' | 1 | 1 | 1 | 448 |
| 'dynamo' | 42 | 60 | 66 | 41 pages, or 43 with display type |
| 'radiometer' | 4 | 4 | 4 | 126, 232 twice, 236 |
| 'inexhaustible' | 1 | 1 | 1 | 197 |

Two rows in that table start with a scan file number instead of a page number, and they do it
because there is no page number to give. Scan 17 is the volume's own table of contents: it sets the
chapter titles in display type, and it is where the seventh 'pyro-magnetic' and the fifth
'thermo-magnetic' occurrence sit. Front matter carries no printed folio, so the script reports that
hit at printed page -1, which is its way of saying 'no folio here, cite the scan file'. The default
index drops those display lines, which is exactly why those two rows lose two occurrences each
between the prose-only and everything-kept columns.

The first seven rows are the claim. The rest are controls, and a null result without controls is
worth very little. The same command on the same file finds 9 standalone occurrences of 'unity', 4 of
'radiometer' and 1 of 'inexhaustible'. A zero from this method means the string is not there, not
that the method is blind.

The two rows that matter most for anyone who has read the marketing are 'free' and 'energy', four
rows above 'free energy'. The book uses 'free' 97 times and 'energy' 243 times and never puts them
next to each other.

## The Five Occurrences, Read in Context

A count of five invites one question, which is: five of what. The answer changes what the number
means, so it is in the body rather than in a footnote.

The sequence 'magnetic generator' never stands alone in this volume. Its whole-word count is 0 in
both indexes. Every one of its substring occurrences sits inside a longer word: the print sets
'pyro-magnetic generator' in display type and in the preface, and 'pyromagnetic generator' closed up
in running text and in the index. What the search finds is the machine chapter XXXVI is about.

| printed page | scan file | what the text is | the string as the text layer has it |
|---|---|---|---|
| 6 | 24 | the editors' preface, listing what the volume contains | 'pyro-magnetic generators,' |
| 424 | 442 | the display heading of chapter XXXVI | 'MOTORS AND PYRO-MAGNETIC GENERATORS.' |
| 429 | 447 | running text, first line of the passage that names the machine | 'a pyromagnetic generator of electricity1' |
| 429 | 447 | running text, later in the same passage | 'the pyromagnetic generator, treated in this chapter' |
| 496 | 514 | the volume's own index, an entry and a page number | 'Pyromagnetic Generators' |

Two of the five are prose. One is a chapter title, one is a preface list, one is an index entry.
That is worth saying plainly, because 'the book mentions magnetic generators five times' reads
differently once you know that two of the five are the book filing its own text.

The preface sentence is the volume's editors describing what the volume contains: it includes "a
great many other inventions in arc lighting, transformers, pyro-magnetic generators, thermo-magnetic
motors" (1894, p. 6). That is not Tesla writing.

Neither are the two prose occurrences. They are the compiler's, and the chapter says at its opening
where the information came from: "In an interview with Mr. Tesla on this subject, the compiler
learned of an experiment which will interest students" (1894, p. 424). The two occurrences are his
summary of that subject. The first is "Mr. Tesla has also devoted his attention to the development
of a pyromagnetic generator of electricity" (1894, p. 429), and the second, later in the same
passage, is "the enlargement of these ideas will be found in Mr. Tesla's work on the pyromagnetic
generator, treated in this chapter" (1894, p. 429).

The first of those two stops before a superscript footnote marker. The text layer puts the marker
inside the word, as 'electricity1', so a quotation that ran on would be quoting something the print
separates.

The chapter title is named here rather than quoted as one string, because the text layer does not
hold it as one string. It reads the line in four fragments: 'CHAPTEK', 'THERMO-MAGNETIC', 'XXXVI.'
and 'MOTORS AND PYRO-MAGNETIC GENERATORS.' The heading as the book sets it is on the crop below,
and it is legible there.

![The chapter heading on printed p. 424](/assets/tesla1894/scan-p424-chapter-heading.webp "Page-scan crop of the chapter heading on printed p. 424, cut from the 500 ppi render of scan file 442 at box x139,y625 to x1780,y865 and published at 1:1. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 424. Public domain. This is the fifth occurrence of the string 'magnetic generator' in the volume, and the one the default search index does not contain: the text layer reads the line in four fragments, 'CHAPTEK', 'THERMO-MAGNETIC', 'XXXVI.' and 'MOTORS AND PYRO-MAGNETIC GENERATORS.', and the index drops every one of them as a short all-capital line. The print hyphenates both compounds. The running text on printed p. 429 does not.")

The reading gives one thing the counts table cannot show: **the book is not consistent about the
hyphen.** The preface on printed p. 6 and the chapter title on printed p. 424 set 'pyro-magnetic'
with a hyphen. The running text on printed p. 429, twice, and the index entry on printed p. 496 set
'pyromagnetic' closed up. The two crops below are the print itself rather than the text layer, and
between them they show both forms.

That inconsistency is why the search folds hyphens at all. Counted over the raw text layer with no
normalisation, 'pyro-magnetic' returns 3 hits and 'pyromagnetic' returns 4, seven in all. A reader
typing either spelling into a plain search finds fewer than half of them.

![Two lines of running text on printed p. 429](/assets/tesla1894/scan-p429-pyromagnetic-line.webp "Page-scan crop of the first two lines of the passage on printed p. 429 that names the machine, cut from the 500 ppi render of scan file 447 at box x83,y240 to x1722,y379 and published at 1:1. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 429. Public domain. The crop carries two complete lines and stops in the whitespace above the third; the column runs on below it. The print sets 'pyromagnetic' closed up, with no hyphen, and the footnote marker is the superscript one after 'electricity'. The text layer puts that marker inside the word, as 'electricity1', which is why the quotation on this page stops before it.")

![The volume's own index entry on printed p. 496](/assets/tesla1894/scan-p496-index.webp "Page-scan crop of the top of the left column of the volume's own index, printed p. 496, from the folio down to the entry Pyromagnetic Generators and the number it gives, 429. The same published crop the article on free energy uses, with the same facts, so two pages describe one image in one way. Scan from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 496. Public domain. This entry is the fifth occurrence in the counts table and it is an index entry, not prose. The print sets this one closed up as well. The right column of the same page carries Thermo-Magnetic Motors and 424, and the G column two pages earlier carries Generators, Pyromagnetic and 429.")

## Why One Run Says Four and the Other Says Five

The default index cleans each page before searching it, because in this scan running heads sit in the
middle of sentences. The rule that does it is short enough to print:

```
if re.fullmatch(r"[ivxlcdmIVXLCDM]{1,5}|\d{1,4}", s):
    continue                    # a bare page number
...
if (len(s) < 140 and nwords <= 9 and ratio > 0.7) or \
   (len(s) < 60 and nwords <= 6 and ratio > 0.6):
    continue                    # a running head, or a display line
```

`ratio` is the share of capital letters in the line and `nwords` its word count. Run over scan 442,
printed p. 424, that rule removes four lines:

| line the default index removes | characters | words | capital share |
|---|---:|---:|---:|
| 'CHAPTEK' | 7 | 1 | 1.0 |
| 'THERMO-MAGNETIC' | 15 | 1 | 1.0 |
| 'XXXVI.' | 6 | 1 | 1.0 |
| 'MOTORS AND PYRO-MAGNETIC GENERATORS.' | 36 | 4 | 1.0 |

That is the whole difference between 4 and 5. The default index reports 4 occurrences, on printed
pp. 6, 429 twice and 496. The kept index reports 5, adding the chapter title on printed p. 424.

Neither number is wrong. Each is true of the text it was taken from. What this series does with that
is stated once and followed everywhere: a count names its index, and a claim about the book uses the
wider index, because the claim is about the book and not about a search tool. The free energy
article prints 5 for the same reason and says the same thing in its own method paragraph.

## What a Zero Does and Does Not Prove

A zero from this method has a scope, and the scope is the honest part of it.

It covers one text: the 1894 first edition, as its text layer reaches this machine. It does not
cover a later printing, a different edition, a lecture transcript, or anything Tesla wrote after
this volume. It does not cover an idea the book paraphrases without naming: the volume discusses
energy, storage and loss constantly, and 'energy' and 'generator' are among its common vocabulary,
so the absence of a two-word phrase is not the absence of a subject.

It also does not settle what Tesla meant anywhere else. The claim this site makes is narrow and it
survives the search: a sentence circulated as his promise of free energy is printed in a book that
never uses the phrase, and the one machine the book describes under a name containing 'magnetic
generator' has a fire under it. Both halves of that, with the chapter, the footnotes and the
question of who is writing in each passage, are on
[Tesla on Free Energy: What He Actually Said](tesla-free-energy-what-he-said.html).

What would change these numbers, and by how much:

- **a different text layer.** This one misreads folios on 35 pages and splits a chapter title into
  four fragments. A better layer would not move the zeros for 'free energy', which are absences of a
  two-word sequence, but it could move the substring totals for hyphenated compounds
- **a looser adjacency rule.** Counting 'free' and 'energy' within a few words of each other returns
  non-zero results and answers a different question. This page counts the phrase, and says so
- **a different index.** 4 or 5, as above

The same method on the same file, applied to a different phrase, is worked through in the article on
[the cold flame Tesla held in his hand](tesla-cold-flame.html), which whole-word searches 'cold
flame' and 'cold fire', gets 0 for both, and then reports the words the book does use. The
engravings from this scan are catalogued page by page at
[Tesla 1894 Plates](tesla-1894-plates.html).

{{FAQ}}

{{CTA}}

{{SOURCES}}
