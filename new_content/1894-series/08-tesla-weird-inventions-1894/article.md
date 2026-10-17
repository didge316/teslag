---
title: "9 Tesla Inventions From 1894 That Never Caught On"
slug: tesla-weird-inventions-1894.html
# §5.1 leaves this choice open and the plan of record (feature-006/a08-wirecommit) settles it:
# keep the file name tesla-weird-inventions-1894.html and carry /tesla-weird-inventions as the
# alias. redirect_rules() emits the pair of 301s from this pair of values, so pretty_slug is the
# alias here and never a restatement of the file name.
pretty_slug: /tesla-weird-inventions
description: "Nine devices from the 1894 book, each cited to its printed page. The volume reports no failure for any of them. It records what each one still needed."
keywords: [tesla lesser known inventions, weird tesla inventions, tesla facts list, tesla failed inventions, tesla 1894 book inventions]
# PUBLISH DATE, settled at feature-006/a08-wirecommit (2026-10-17). The draft carried 2026-10-17,
# the day its first batch was written, which is the day article 11 is already dated on the site. The
# nine wired pages in this series each carry their own date, ascending in the order they were wired:
# 03 10-14, 09 10-16, 11 10-17, 07 10-18, 01 10-19, 02 10-20, 04 10-21, 05 10-22, 06 10-23. That is
# section 11's cadence rule ('2 per week, never more than 2 in a day') applied as one page per date,
# and articles.html is in that same order. This page is the tenth wired, so it takes the next date in
# the sequence and its card goes after the article 06 card, which is where feature-005/a06-wirecommit
# put that one. The alternative was measured before it was rejected: keep 10-17 and insert this card
# between the 11 and 07 cards. It is inside the cadence rule and it keeps the grid monotonic, but it
# puts two pages on one date and breaks the second invariant the grid already has, that card order is
# wiring order. Nothing here is a claim that anything is published: no page in this series has been
# pushed (D6), and six of the nine already carry dates in the future for the same reason.
# CHECKED BEFORE THE CHANGE, NOT ASSUMED: make_article.py run on this draft exactly as it stands puts
# out a page byte-identical to the committed one (books/tmp/f06wire/tesla-weird-inventions-1894.html,
# cmp clean against website/tesla-weird-inventions-1894.html at 45,641 bytes), so the render is
# reproducible and the only bytes this edit moves are the five date strings in the head, the JSON-LD
# and the visible date line. The feature-006/t4 visual record therefore still describes this page.
date_published: "2026-10-24"
date_modified: "2026-10-24"
series_no: 8
primary_query: tesla lesser known inventions
tid: "1894_08"
# og_image is the path every page in this series carries and no page in this series has the file
# yet: feature-010/t2 generates all thirteen with the script feature-010/t1 writes. Setting the path
# here is the series convention, not a claim that the file exists.
# card_image is figure 1 of the page, as on every other article in the series, so it is set at
# feature-006/t2 with the figure record below, once the number had been read off the printed caption
# at 500 ppi. It is the same file as figure 1, not a second crop of the same plate.
og_image: assets/og/tesla-weird-inventions-1894.webp
card_image: assets/tesla1894/p410-fig220.webp
card_alt: "1894 circuit diagram, Fig. 220, printed p. 410: an alternating current generator feeding a line that divides at one point and rejoins at another, with a direct current source in each of the two branches"
standfirst: "Nine devices, each cited to the printed page of the 1894 book that collected them. The volume never says any of them failed, and for most of the nine it says nothing at all about what became of them. What it does record, entry by entry, is the thing each machine needed and had not got: a rotating armature turning in step with the line, a dielectric with no gas in it, a current that had to be reversed after every reading."
# FIGURES, feature-006/t2 (2026-10-17). Three figures, placed one per entry, in entries 1, 2 and 4.
# Not nine, and the reason is §6.6 and §12 rather than a shortage of engravings: §6.6 'Every article
# ships with 2-3 images placed in the body, each adjacent to the paragraph it illustrates', and nine
# cannot be squared with that or with the 400 KB figure gate. §9 brief 08's 'one engraving per entry'
# is the same kind of brief line as the nine H2s that decision 15 had to give up for the 5-9 H2 gate,
# and it goes the same way: the gate is the boundary and the count is not. Article 06 shipped three
# under the identical brief line. Six entries carry no figure on this page; which ones, and what it
# would take to add one, is under 'NOT RE-OPENED' at the end of this block.
#
# READ BEFORE ANYTHING WAS RE-OPENED (criterion 1). App. C's row for this page names six candidates
# by scan file: p440-fig230 p.422, p452-fig247 p.434, p478-fig283 p.460, p484-fig290 p.466,
# p464-fig266 p.446, p475-fig281 p.457. §9 brief 08 prints the same six in printed-page form
# (p422-fig230, p434-fig247, p446-fig266, p457-fig281, p460-fig283, p466-fig290), which is a
# shorthand and not a filename: printed page = scan file - 18 (§0), so p422-fig230 is the file
# p440-fig1-fig230.webp. Then website/assets/tesla1894/manifest.csv and manifest_qc.csv rows 149 to
# 192 - every row either file has anywhere in the page range of all nine entries, scans 428 to 491,
# since neither file has a row for scan 427 or 492 - and the crops themselves,
# opened as images: p428-fig1-fig220.webp, p440-fig1-fig230.webp and p448-fig1-fig243.webp. Also
# read: the feature-006/t0 lesson in books/harness/lessons-decisions.md, which named entry 2 as the
# gap, and feature-005/a06-figrec's two lessons, which are why every box below is written down.
# Three claims in this page's own earlier record are wrong, and they are corrected here instead of
# being carried into the figure task:
#   1. 'entries 4 to 6 have no crop on disk either'. They have crops. manifest.csv has rows, and the
#      files exist, for printed pp. 425, 426, 427 and 430 (entry 4), 433, 434, 435 and 436 (entry 5)
#      and 439, 440, 441, 442, 444, 445 and 446 (entry 6). Entry 2 is the only one of the nine with
#      no crop anywhere, and it is the only one of the nine with no row in manifest.csv either.
#   2. 'entry 5's figure is App. C's p434-fig247, which is in the candidate list below'. The file is
#      website/assets/tesla1894/p452-fig1-fig247.webp, it is on disk, and manifest_qc row 163 calls
#      it keep/A. It is not used here; the reason is under 'NOT RE-OPENED'.
#   3. 'Two manifest_qc subject lines describe those meters wrongly'. Two subject lines, yes, but only
#      one of the two figures is a meter. Measured against the print the two are row 149 (Fig. 220,
#      which is not a meter and has no battery in the sense the note means) and row 156 (Fig. 229, a
#      meter figure, called 'good coherer/retcoherer illustration'). Row 157 (Fig. 230) is not wrong
#      so much as incomplete: it omits the galvanometer and both resistance coils, which are most of
#      the drawing. All three notes are corrected in manifest_qc.csv at this task, in the site repo,
#      with the read that corrects them named in the note, and so are two more that turned up while
#      checking them: row 158's 'Figure number 281 is genuine for p.425', which that page's own three
#      printed captions contradict without anything settling it (the note now says NOT SETTLED and says
#      why the page was not re-opened), and row 161's description of the p.430 two-figure band, which
#      is the crop this task replaced. That is the standing reason every caption
#      below is written from the prose of the printed page and every figure number from the printed
#      caption, never from an extractor filename or a QC note (§6.6).
#
# RE-OPENED AT 500 ppi, and only these four pages (criterion 2). Each was chosen because its evidence
# is missing or contradicted, not because it was next to hand. pdftoppm -r 500 of
# books/pdf-pages-tesla-1894/page-NNN.pdf, 1856 x 3227 px a page, the native resolution of the image
# embedded in the page PDF, the same size feature-005/a06-figrec measured. The renders themselves are
# in gitignored books/tmp/f06t2/; every crop that carries a read is committed under figures/ beside
# this file, with the exact box it was cut at and its sha256 in figures/README.md, so the read can be
# re-made without re-rendering anything.
#   printed p. 410, scan 428 (entry 1). A crop exists and is keep/A (row 149), but its subject line
#     is contradicted by the print, and the crop carries no printed caption, which §6.6 requires.
#   printed p. 418, scan 436 (entry 2). No crop, no manifest row, nothing. Re-opened, and the reason
#     the row was never written is now known: extract_figures.py run over scan 436 at both 300 and
#     500 dpi returns 0 figures for this page, because it masks every row the text layer claims and
#     these two plates sit inside the claimed text block. The plates are there. In the 500 ppi render
#     their ink runs y 1474 to 1941, x 230 to 1143 for the left plate and x 1233 to 1730 for the
#     right, and both printed captions are set under them at y 1945 to 2024.
#   printed p. 422, scan 440 (entry 3). A crop exists and is keep/A (row 157), but the number was
#     contradicted: the text layer of this page sets the printed caption as 'FIG. 280.' while the body
#     of the same page reads 'In Fig. 230 the conductors c c' are connected in parallel'. Re-opened to
#     settle which the print says.
#   printed p. 430, scan 448 (entry 4). A crop exists and is keep/A (row 161 of both manifest files;
#     this block first said row 176, which is p464-fig1-fig266 on printed p. 446 and untouched here),
#     but it is a two-figure band at 300 ppi holding Fig. 242 and Fig. 243 side by side with neither
#     printed caption, its subject line ('A long solenoid with a sliding armature rod and a detail block at right')
#     describes neither plate correctly, and the file is named for the smaller of the two. Re-opened,
#     because this is the machine the closing beat names.
#
# WHAT THE PRINT SAYS, read off those renders. The crops named below are the evidence and they are in
# git, not in tmp/.
#   printed p. 410: the printed caption under the single plate is 'FIG. 220.'
#     (figures/p410-printed-caption-fig220.png), and the body line on the same page begins 'In Fig.
#     220, A designates a generator of alternating currents,'
#     (figures/p410-bodyref-fig220-line.png). The plate is one diagram: a box marked A low in the
#     centre, two conductors marked B leading out of it and turning up at the sides of the plate,
#     dividing at a point marked Y at the left and rejoining at a point marked X at the right, two
#     branch conductors between those points marked C above and D below, a round cell symbol with one
#     long and one short bar inside it in each branch, marked E above and F below, and three small
#     dark diamond shaped symbols set at intervals along each branch. The prose on the same page says
#     the same thing in other words: 'A designates a generator of alternating currents, and B B the
#     main or line circuit therefrom', the circuit 'is divided into two paths or branches', and 'the
#     generators E F are connected up in series therein, one generator in each part or half of the
#     circuit' (printed p. 410); the page before it says, of the devices put in the branches, 'Assume,
#     for example, that these devices are batteries, primary or secondary, or continuous current dynamo
#     machines' (printed p. 409). So row 149's 'two lamps in opposite arms of a loop with a battery and
#     switches' gets the loop right and the parts wrong: A is the alternating current generator, the two
#     devices in the arms are the direct current sources the chapter calls generators and then current
#     sources, and no word for a lamp, a meter, an indicator or a switch appears anywhere in the four
#     printed pages of this chapter (scans 427 to 430 searched). The three dark symbols are not
#     described either, so the alt text gives their shapes and the caption says plainly that they are
#     not named.
#   printed p. 418: two plates side by side, 'FIG. 227.' under the left and 'FIG. 228.' under the
#     right (figures/p418-printed-caption-band-fig227-fig228.png). Fig. 227 is a rectangular can in
#     section, walls hatched, with a plate stack near each end drawn as a set of horizontal lines,
#     three dark vertical strips between them, the interior filled with a stippled space, a terminal
#     led out through the middle of each short wall, and letters on the plate. Fig. 228 is a taller
#     can in section with two plates whose outer edges are curved, a threaded rod with nuts and a
#     stuffing box through each side wall, and the same filled interior. The page after this one names
#     both plates and their letters, in the volume's own text layer and clean: 'Fig. 227 is a section
#     of a condenser constructed in accordance with this principle and having stationary plates; and
#     Fig. 228 is a similar view of a condenser with adjustable plates', then box or receptacle A,
#     plates B and c, terminals D and E through the sides of the case, strips of porous insulating
#     material F 'used merely for the purpose of maintaining them in position', and 'The space within
#     the can is filled with oil G' (printed p. 419). Every one of those letters is legible in the
#     500 ppi crop and points where the prose says it points. That sentence on p. 419 is already
#     quoted in entry 2, so the caption adds no quote the register has not pinned.
#   printed p. 422: the printed caption under the plate is 'FIG. 230.' (figures/p422-printed-caption-
#     fig230.png), and the body line on the same page reads 'In Fig. 230 the conductors c c' are
#     connected in parallel, the' (figures/p422-bodyref-fig230-line.png). The print says 230; the
#     text layer's 'FIG. 280.' is the mis-read, and it is the same 3-for-8 confusion this scan makes
#     twice nearby - 'Fig. 281' on printed p. 425, whose three printed captions read 231, 232 and 233,
#     and 'FIG. 287.' on p. 427, where the sequence reads 237, 238, 239. Both of those two are text-
#     layer reads and neither was re-opened, so they are flagged and not settled; see 'NOT RE-OPENED'.
#     Settled against the print, so the figure this page would have published for entry 3 carries the
#     number the print gives it. The plate is the meter: a long tube in section with hatched end plugs, two conductors
#     running its whole length, one labelled above the tube and one below it (the text on the same page
#     calls them c and c'), both led out to coiled resistances marked R' and R'', a round instrument
#     marked G in the line conductors L L, and a vertical ladder of seven contact points marked T. The
#     printed caption 'FIG. 230.' is inside the plate crop as well as in the caption crop. The prose on
#     pp. 421 and 422 describes exactly that, and says
#     'Figs. 229 and 230 illustrate two forms of such a meter' (printed p. 421). Entry 3 is not
#     illustrated on this page, and the reason is under 'NOT RE-OPENED'.
#   printed p. 430: 'FIG. 242.' under the left plate and 'FIG. 243.' under the right
#     (figures/p430-printed-caption-band-fig242-fig243.png), and the two body lines on the same page
#     say which is which: 'Fig. 242 is a central vertical longitudinal section of the com-'
#     (figures/p430-bodyref-fig242-line.png) and 'plete apparatus and Fig. 243 is a cross-section of
#     the magnetic' (figures/p430-bodyref-fig243-line.png). Fig. 242 is the pyromagnetic generator:
#     a long horizontal bundle of parallel tubes in section spanning the plate, wound at two places
#     with coils, those two coils led up to two small round instruments, the middle of the bundle
#     passing up through a column that stands in a rectangular firebox with a fire drawn under it and
#     a door with a handle at its foot, two vessels partly filled with liquid and a wide flue above
#     them, and pipes from the ends of the bundle to those vessels. Fig. 243 is a small rectangle of
#     circles inside a casing, which is the armature core in cross-section. The prose on the same page
#     matches the drawing part for part: a casing or shell enclosing hollow iron tubes, conductors
#     wound around the core to form the coils in which the currents are developed, current consuming
#     devices in the circuits of those coils, a furnace or closed firebox through which the middle of
#     the core extends, a boiler above the fire, and a steam exhaust pipe that communicates with all
#     the tubes (printed p. 430). Note that the letters on this plate do not all match the letters in
#     that prose, which is normal for a reprinted patent drawing: the firebox the text calls n is
#     marked D on the plate. The caption therefore names the parts in words and not by letter, per the
#     feature-005/t4 rule that a figure whose point is a labelled part must have the part named in the
#     caption text.
#
# WHAT IS PUBLISHED, and where it sits. Three crops, cut at 500 ppi, each the whole plate with its
# printed caption inside the crop, named by printed page as §6.2.5 asks and as article 06's three are
# named. They are in the site repo, committed at this task, and manifest_qc.csv gains a row for each
# of them - rows 217, 218 and 219 of that file, each with the box it was cut at, its sha256, the
# evidence crop that carries the read, and the row it supersedes named:
#   figure 1, website/assets/tesla1894/p410-fig220.webp, 1115 x 629, 21,236 bytes, sha256
#     30a0d64a1841cf4357ae59381ea502fa2cd46e73e65c4a1c38f01e4b8db1a419. Cut from scan 428 at box x
#     396 to 1511, y 1291 to 1920 of the 500 ppi render. It supersedes p428-fig1-fig220.webp, which
#     is the same plate at 300 ppi with no printed caption and a subject line the print contradicts.
#     Placed at the end of entry 1, inside the first entries H2, which is where §6.6 puts figure 1.
#   figure 2, website/assets/tesla1894/p418-fig227.webp, 933 x 496, 40,390 bytes, sha256
#     adf89bbad4ce82ea53aef1b845cb7562d0e87c485c1585c247c802862546c65d. Cut from scan 436 at box x
#     220 to 1153, y 1538 to 2034. There is no earlier crop of this plate to supersede: it is the
#     first crop of printed p. 418 in five years of extraction. Placed at the end of entry 2.
#   figure 3, website/assets/tesla1894/p430-fig242.webp, 1169 x 768, 73,692 bytes, sha256
#     40e6a706c34dfaa4384dd5bf3c789a1dcfabe6b1ea64189d5d73d08d02a04072. Cut from scan 448 at box x
#     196 to 1365, y 1189 to 1957. It supersedes the two-figure band p448-fig1-fig243.webp. Placed
#     inside the closing beat, after the paragraph that names this machine, which is where §6.6 puts
#     figure 3 and is the pairing the page's own argument asks for.
#   Total figure weight as published: 135,318 bytes, inside the 400 KB gate. The three alt texts and
#   captions are the figures: block below and are the only copy: the body image lines carry no alt
#   and no title, so make_article.py takes both from here (img_tag and the figmap lookup). Article 06
#   keeps a second copy of both in its body image lines and the two copies of its Fig. 110 alt already
#   disagree with each other ('black ground' against 'dark ground'), which is the defect this avoids.
#   The captions cite their page in §6.6's form, '(1894), p. 410', not in the '(1894, p. 410)' form,
#   so they do not enter the citation regex and pages_used below is unchanged by the figures. The four
#   pages the plates are on are inside the chapter ranges the sources: block already lists.
#   One deviation from §6.6, stated rather than left to be noticed: figure 2 sits in the same H2 block
#   as figure 1, because entries 1, 2 and 3 are one H2 and the only figures with verified evidence are
#   in entries 1 to 4. Figure 3 is where §6.6 wants it. If the owner wants figure 2 out of that block,
#   the candidate is Fig. 247 on printed p. 434, and it has to be read off the print first.
#
# NOT RE-OPENED, and what that leaves open. Six entries have no figure here, and for none of them is
# the printed caption number known, because no task has read one. App. C's six candidates are crops
# that exist and are keep/A, and their QC notes are not contradicted by anything I read, but a QC note
# is not a printed-caption read, and §6.6 is explicit that the extractor filename and the QC note are
# hints. So they are recorded as available and unverified, which is the honest state, and none of them
# is published here:
#   entry 3, Fig. 230, printed p. 422: read at this task and settled above, and not published. The
#     reason is placement, not evidence: entry 3 is in the same H2 block as entries 1 and 2, and a
#     fourth figure in that block would be three in one section of a five-section page and would put
#     this page outside §6.6. If the owner wants the meter on the page, it replaces figure 2, not adds
#     to it. The crop for it is cuttable at the box in the record above whenever wanted.
#   entry 5, Fig. 247, printed p. 434 (App. C's p452-fig247): the file p452-fig1-fig247.webp exists
#     and row 163 calls it keep/A. The text layer of printed p. 434 sets two captions on that page,
#     'FIG. 246.' and 'FIG. 247.', and the body line says Fig. 246 is a section of the end of a shaft
#     with the commutator on it and Fig. 247 is the inner or bearing face of the collector. The crop is
#     971 x 616 and covers both, so it is a two-figure band like the one this task replaced at p. 430.
#     Not re-opened: nothing about it is contradicted, and this page has no room for a fourth figure.
#   entries 6, 7, 8 and 9: App. C's p464-fig266, p475-fig281, p478-fig283 and p484-fig290, and the
#     crops for printed pp. 439 to 446, 449, 452 to 462 and 466 to 473. Several of those rows already
#     flag their own numbers as uncertain ('number unreliable', 'Caption spans Figs.293-294'), which is
#     a reason not to publish them, not a reason to re-open them at this task: the page is at three
#     figures. Anyone adding one reads the printed caption at 500 ppi first, which is the whole of
#     §6.6's verification step.
#   printed p. 425 (entry 4's chapter, first figure page): manifest_qc row 158 says 'Figure number 281
#     is genuine for p.425'. The text layer of that page sets three captions, 'FIG. 231.', 'FIG. 232.'
#     and 'FIG. 233.', and the body line on the same page that the extractor took the number from
#     reads 'In Fig. 281 the permanent magnet N is connected with a frame'. One of those two is wrong,
#     and the 3-for-8 confusion this scan makes twice nearby (pp. 422, 427) says which is likely. Not
#     re-opened, because this page publishes no figure from p. 425 and entry 4's figure is the one on
#     p. 430. Flagged here and in that file, whose row 158 note now reads NOT SETTLED with the reason
#     the page was not re-opened, so no next reader takes it as settled.
#   The two page renders this task did not need: printed p. 419 (scan 437), whose prose names Figs.
#     227 and 228, was read in the text layer and not rendered. That prose is clean, contains no
#     figure number the print contradicts, and is already quoted in entry 2, so a crop of it would
#     prove nothing the register has not pinned. If the caption for figure 2 is ever changed to quote
#     that sentence, re-read it against the render first.
#
# WHAT feature-006/a08-figrec and t3 take from this block: three figures, verified:true, sourced here
# and not re-derived; the index.json figures[] rows point at the three files above; t3 renders the
# page with the three body image lines already in place, and qa_page.py's image gates will find the
# files, their alt, width and height in the block below; t4 reviews these three crops at 375, 768 and
# 1280, where the letters inside the plates are expected to be marginal, as they were on article 05,
# which is why every part the argument needs is named in words in the caption text.
figures:
  # Figure 1. Number read off the printed caption at 500 ppi, not from the extractor filename or the
  # manifest_qc subject line, both of which are wrong about this plate. See the block above.
  - src: /assets/tesla1894/p410-fig220.webp
    alt: "1894 circuit diagram, Fig. 220, printed p. 410: a rectangular box marked A low in the centre, two conductors marked B leading out of it and turning up at the sides of the plate, dividing at a point marked Y at the left and rejoining at a point marked X at the right, two branch conductors running between those points, the upper marked C and the lower marked D, a round cell symbol with one long and one short bar inside it in each branch, marked E in the upper branch and F in the lower, and three small dark diamond shaped symbols set at intervals along each branch"
    width: 1115
    height: 629
    caption: "Fig. 220, printed p. 410, the whole diagram with its printed caption inside the crop. Engraving from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 410. Public domain. The text on that page names the parts: A is a generator of alternating currents, B B is the line, and at the point where direct currents are wanted the line is divided into two paths or branches, with a generator in each, the two connected in series one in each half of the circuit. The drawing is that division, and it is drawn as a division: the line enters at the left, splits at Y, runs along the two branches, and rejoins at X. The three small dark symbols in each branch are not described anywhere in the chapter, so they are named here by shape only and not as lamps or meters. This is the arrangement entry 1 above is about, and the part of it that matters is the split, not the two cells: the chapter's own difficulty, quoted above, is that the devices which do this work in the other figures of the same chapter have to turn in step with the line."
  # Figure 2. The first crop of printed p. 418 that any pass has made: extract_figures.py returns 0
  # figures for scan 436 at both 300 and 500 dpi, which is why there was no row for it. Every letter
  # named in this caption is legible in the crop and is the letter the prose on printed p. 419 uses.
  - src: /assets/tesla1894/p418-fig227.webp
    alt: "1894 engraving, Fig. 227, printed p. 418: a rectangular can shown in section with its walls hatched, a stack of horizontal plates standing inside near each end, three dark vertical strips between the two stacks, the whole interior filled with a stippled space, a terminal led out through the middle of each short wall, and letters marking the case, the two plate stacks, the dark strips, the terminals and the filled interior"
    width: 933
    height: 496
    caption: "Fig. 227, printed p. 418, the whole plate with its printed caption inside the crop; the plate beside it on the same printed page is Fig. 228, the same condenser with adjustable plates. Engraving from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 418. Public domain. The page after this one describes what is drawn, and the letters on the plate are its letters: a box or receptacle containing the plates or armatures, led out to terminals through the sides of the case, the plates separated by strips of porous insulating material used merely for the purpose of maintaining them in position, and the space within the can filled with oil. Nothing in the drawing is a solid dielectric. The insulating thing between the plates is the oil, and the strips are spacers, which is the whole of entry 2 above drawn as the book drew it. The book hedges its own novelty on the same page, saying oil between conductors has been a common practice, and that hedge is why this is the entry on this list that did not lose."
  # Figure 3. Placed with the closing beat, which names this machine. The letters on this plate do not
  # all match the letters in the prose on the same page (the firebox the text calls n is marked D on
  # the plate), so the caption names the parts in words and not by letter.
  - src: /assets/tesla1894/p430-fig242.webp
    alt: "1894 engraving, Fig. 242, printed p. 430: a long horizontal bundle of parallel tubes in section spanning the width of the plate, wound at two places with coils of many turns, those two coils led up to two small round instruments near the top of the drawing; the middle of the bundle passes up through a column standing in a rectangular firebox with a fire drawn under it and a door with a handle at its foot, and above the firebox the column branches into two vertical vessels partly filled with liquid with a wide flue rising between them; pipes run from near the ends of the tube bundle up and over to those vessels, one of them with a valve in it; a spring loaded fitting and a bracket are drawn at the left end of the bundle and the whole machine stands on a flat base"
    width: 1169
    height: 768
    caption: "Fig. 242, printed p. 430, the whole apparatus with its printed caption inside the crop; the small plate beside it on the same printed page, a rectangle of circles inside a casing, is Fig. 243, which the same page calls a cross-section of the magnetic armature-core of the generator. Engraving from Martin (ed.), The Inventions, Researches and Writings of Nikola Tesla (1894), p. 430. Public domain. The text on this page says the armature core is a casing enclosing a number of hollow iron tubes, that conductors wound around it form the coils in which the currents are developed, that current consuming devices are in the circuits of those coils, that a furnace or closed firebox surrounds the middle of the core, that a boiler holding water sits above the fire, and that the steam from the boiler passes through the tubes, which is the artificial cooling the page calls the first of its two features of novelty. The drawing matches that list part for part. What the chapter reports with the drawing is what it reports without it: no output, no efficiency figure and no trial. This is the machine the section above names as the only one in this volume that the phrase 'magnetic generator' is attached to, and it is a heat engine."
#
# PAGES USED, all nine entries. This list is rendered into the published
# Sources block by make_article.py sources_block(), so it is the pages the page actually cites, not
# the pages consulted: printed p. 416 was read but is not cited anywhere in this draft, because the
# 'active (as distinguished from a dead) resistance' quote was left out (see LENGTH below), so 416
# is not in the list and returns only if that quote is added. The same is true of the pages batch 2
# read and did not cite: 425, 428, 430, 431, 433, 439, 443 and 447 are pinned in the register
# and absent from the draft, and each returns only if its quote is added. Batch 3 read printed
# pp. 448 to 450, 451 to 464 and 465 to 474 and cites nine of those pages - 448, 450, 451, 463,
# 464, 465, 467, 468 and 474 - so 449, 452 to 462, 466 and 469 to 473 are read and not cited, and
# the p. 452 fifty-per-cent illustration is among the pages left out (see decision 11 below). The
# closing beat adds two index pages that no entry uses: printed p. 496, the volume's own index line
# 'Pyromagnetic Generators', and printed p. 495, which was read to confirm that 496 is the index
# page carrying it and is not cited. Printed p. 390 IS here,
# because entry 6 quotes the third-brush claim from it; it is ch. XXIX, not Part III, and it is the
# same chapter article 11's page is built on. The list below is not typed by hand: it is the set of
# pages in the '(1894, p. N)' citations in the body, read out with the citation regex
# check_quotes.py uses, so it cannot disagree with the body it sits above.
pages_used: [6, 390, 409, 412, 418, 419, 420, 422, 423, 424, 429, 432, 434, 436, 437, 438, 441, 448, 450, 451, 463, 464, 465, 467, 468, 474, 496]
#
# SOURCES. The two modern ones are not decoration: the register's Rejected #7 requires a modern
# source for any sentence placing entry 1 in a history of rectifiers, and the flag ENTRY 2 IS THE
# ENTRY THAT DID NOT LOSE requires one for the claim that the principle won. Both were fetched at
# drafting time on 2026-10-17 and each is listed below with the sentence it is used for. Modern
# sources are paraphrased in the body and never put inside quotation marks: check_quotes.py matches
# every double-quoted run in the body against the 1894 text, so a modern quotation in quotes is a
# FAIL there by construction, and that is how article 06 handles it too. ONE OF THE TWO URLS
# BREAKS A §12 GATE, AND IT IS NOT A BOOK PDF: the ABB Review row's url ends in '.pdf', and
# qa_page.py's D4 gate is a plain substring test for '.pdf' anywhere in the page, so it fails this
# page on a journal PDF. Measured at the smoke render below (books/tmp/f06t2b/qa_smoke.out).
# Fixing it is an owner call at feature-006/t3, not a silent edit here: either the ABB citation
# loses its url and keeps the bibliographic text, or a non-.pdf location is found for the same
# article. Inventing a URL is the one thing not to do.
# DONE AT feature-006/t3 (2026-10-17): the url is off that row and the bibliographic text stands
# on its own, which is the first of the two options the draft batch left open. The second was
# measured, not assumed. curl on 2026-10-17: the .pdf itself returns 200, and it is kept here so
# the source stays findable even though the page no longer links to it -
# https://library.e.abb.com/public/45d14c404e73a375c125762d00485f4f/66-70%203M998_ENG72dpi.pdf,
# the same address the draft fetched on 2026-10-17. The library path without the file name returns
# 403, and so does a guessed 66-70.html at the end of that path, so there is no non-.pdf location
# for this article to link to. The citation still names the authors, the article title, the journal,
# the issue and the pages, which is enough for a reader to find it. qa_page.py's D4 gate is left
# exactly as it is: a substring test for '.pdf' is what that gate is, and narrowing it is a tool
# change, not a page fix.
sources:
  - text: "Chapter XXXIII, 'METHOD OF OBTAINING DIRECT FROM ALTERNATING CURRENTS', printed pp. 409 to 417 (scan files 427 to 435). Entry 1 and the provenance quote 'Mr. Tesla divides such circuit at any desired point into two branches or paths' are from it. The chapter is the volume's editor writing about Tesla in the third person, not Tesla's writing"
  - text: "Chapter XXXIV, 'CONDENSERS WITH PLATES IN OIL', printed pp. 418 to 419 (scan files 436 to 437). Entry 2, including the editor's own footnote on printed p. 418, which is quoted in the register and not used in this draft"
  - text: "Chapter XXXV, 'ELECTROLYTIC REGISTERING METER', printed pp. 420 to 423 (scan files 438 to 441). Entry 3, including the editor's verdict on electrolytic meters at printed p. 423"
  - text: "Chapter XXXVI, 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS', printed pp. 424 to 431 (scan files 442 to 449). Entry 4. The 400-to-500-a-minute number is in the compiler's footnote on printed p. 424, about a horseshoe-magnet bench experiment he says he learned of in an interview with Tesla, and the same footnote says the chapter's own devices vibrate 'very slow'; the draft prints the number only as that footnote prints it"
  - text: "Chapter XXXVII, 'ANTI-SPARKING BRUSH AND COMMUTATOR', printed pp. 432 to 437 (scan files 450 to 455). Entry 5. The chapter gives no year for either device, only 'some years ago' and 'A few years later', and prints no patent number anywhere in it"
  - text: "Chapter XXXVIII, 'AUXILIARY BRUSH REGULATION OF DIRECT CURRENT DYNAMOS', printed pp. 438 to 447 (scan files 456 to 465). Entry 6, including 'devised by him as far back as 1885' at printed p. 438, which is the compiler's date and not Tesla's"
  - text: "Chapter XXXIX, 'IMPROVEMENT IN THE CONSTRUCTION OF DYNAMOS AND MOTORS', printed pp. 448 to 450 (scan files 466 to 468). Entry 7. The chapter prints no date, no patent number, no trial and no result; its one stated advantage is the bearing placement at printed p. 450, behind the sentence 'This machine possesses several advantages', and it closes by widening the claim to machines of the ordinary type generally used"
  - text: "Chapter XL, 'DIRECT CURRENT ARC LIGHTING SYSTEM', printed pp. 451 to 464 (scan files 469 to 482). Entry 8, including the three sentences at printed p. 451 that make it the only one of the nine with a stated fate: the system 'was confided to a company formed for its exploitation', Tesla then turned to what the compiler calls his 'more celebrated' rotary field system, and the apparatus appeared at a time when many other lamps and machines were in the market. The company is not named anywhere in the chapter. The chapter heading as the scan reads it is 'TKSLA XI,' and 'SYSTKM', which is 'XL' and 'SYSTEM' misread; the chapter number is taken from the chapter order, not from that line"
  - text: "Chapter XLI, 'IMPROVEMENT IN UNIPOLAR GENERATORS' (the printed heading sets UNIPOLAR inside quotation marks), printed pp. 465 to 474 (scan files 483 to 492). Entry 9. Printed pp. 465 to 466 and the top of 467 are the compiler; from the middle of printed p. 467 to the foot of p. 474 the chapter is Tesla's own writing, and the compiler says so in the text and dates it in the footnote ('Article by Mr. Tesla, contributed to The Electrical Engineer, N. Y., Sept. 2, 1891'). Entry 9's 'two years ago' is inside that reprinted article, so the date it points to is derived from the volume's own date-stamp and is not stated by the volume"
  - text: "Chapter XXIX, the author's own account of high-frequency alternating-current generators, printed pp. 374 to 391 (scan files 392 to 409). NOT Part III: it is the author writing about himself in the third person. Entry 6's priority claim at printed p. 390 is his own sentence with his own hedges in it. Article 11 (feature-007) is built on this same chapter and says nothing about the voice, so the two pages do not contradict each other today; if either page ever describes that voice, both must be checked together"
  - text: "Thomas J. Blalock, 'The Rotary Era, Part 2: Early AC-to-DC Power Conversion, Continued', IEEE Power and Energy Magazine, November/December 2013, for the modern half of entry 1: the mercury arc rectifier 'did away with the need to maintain bearings, commutators, and brushes as was necessary with rotary converters', Con Edison shut its last New York rotary converter substations in 1977 and moved those direct-current customers onto solid-state rectifier units, and the last IND 60-Hz rotary was shut down in 2005"
    url: "https://magazine.ieee-pes.org/novemberdecember-2013/history-10"
  - text: "Lars Jonsson and Rutger Johansson, 'High-voltage bushings: 100 years of technical advancement', ABB Review 3/2009, pp. 66 to 70, for the modern half of entry 2: oil-impregnated paper became the predominant condenser bushing technology in the 1960s and the article reports it still holding more than 80 percent of that market, and oil impregnation under vacuum is used because 'oil fills out all parts of the bushing and remains in a liquid phase throughout its entire life', void-free"   # no url: feature-006/t3, see the note above the sources list
  - text: "Every 1894 quote on this page is taken from the register new_content/1894-series/08-tesla-weird-inventions-1894/quotes.md, 126 quotes and 132 fragments across 51 printed pages with 0 failures, regenerated by gen_quotes.py in that directory, which exits non-zero and writes nothing if any quote misses. Re-runnable one at a time with books/tools/grep_quote.py"
# DRAFT STATE, feature-006/a08-draft3 (2026-10-17). The draft is complete: the Part III provenance
# paragraph, entries 1 to 9, and the closing beat on the only 'magnetic generator' in the volume.
# Batch 1 (feature-006/t1) wrote entries 1 to 3, batch 2 (feature-006/a08-draft2) wrote entries 4
# to 6, and this task wrote the provenance paragraph, entries 7 to 9 and the closer from the
# register's batch-3 rows, with no change to entries 1 to 6. The provenance paragraph is the
# register flag PART III IS NOT ALL THE COMPILER'S PROSE honoured in the body: it says, before
# entry 1, that eight of the nine chapters are the compiler's third-person prose about Tesla (see
# decision 14 for why not six), that ch. XLI is Tesla's own reprinted article from the middle of
# printed p. 467, and that entry 6
# borrows from a chapter that is the author writing about himself in the third person. Entries 1
# and 3 are unchanged from the batches that wrote them; entry 1 still carries no voice sentence,
# because that flag asks the intro for it, not the entry. What is not here yet, and which task
# owns it:
#   the cta block   no plan task owns it, and it is a real gap, not a detail: the CTA sentence is
#   frontmatter (article 09's 'cta: text:' is how every page in this series fills {{CTA}}), this file
#   has no cta: key, and make_article.py cta_block() emits an empty paragraph when the key is
#   missing, so the page renders a blank alert box. qa_page.py does not look for a CTA, so
#   feature-006/t3 will not catch it either. Flagged rather than invented here.
#   the FAQ   §9 brief 08 does not ask for FAQ schema - it asks for it in briefs 03, 04, 07, 10, 11
#   and 12 and not in 08 or 09, and article 09 shipped with faq: [] - so faq: [] is the brief as
#   written, and {{FAQ}} renders as nothing. If the owner wants one, that is a new task.
#   The {{FAQ}}, {{CTA}} and {{SOURCES}} placeholders are in the body, in the order every other
#   page in this series has them.
#   the figure record, the three published crops, card_image and card_alt   feature-006/t2, done
#   2026-10-17, and the record is the FIGURES block below rather than a line in this list
#   the index.json figures[] row   feature-006/a08-figrec, which reads this record and does not
#   re-derive it; the og_image FILE   feature-010/t2, which generates all thirteen
#   render and numeric gates   feature-006/t3; visual QA   feature-006/t4
# WHAT A SMOKE RENDER OF THIS DRAFT ALREADY FAILS, measured again at this task (2026-10-17) by
# rendering it to books/tmp/f06t2b/tesla-weird-inventions-1894.html and running qa_page.py on that
# (output at books/tmp/f06t2b/qa_smoke.out; the quote tool's own output for the same bytes is at
# books/tmp/f06t2b/check_quotes.out, 45 fragments, 45 verbatim and page-cited, 0 problems, exit 0):
# 27 of 29 gates, 2 failures, both named with their owner, and both the same two the draft batch
# that wrote this page measured (books/tmp/f06a08d3/qa_smoke.out). The denominator moved between
# those two measurements and it is not a tool change: qa_page.py line 304 adds the '2-3 figures in
# <figure class="mb-4 pt-5">' gate only for a page that references assets/tesla1894/, so the
# figure-less draft was scored against 28 gates and this page is scored against 29. The new gate
# passes. The two that do not: the reciprocal-links gate wants 3 links to pages that link back and
# finds none, because nothing links to this page yet - that is feature-006/a08-wirecommit's in-link
# work, not a defect in the draft. The D4 book-PDF gate is the ABB url noted above, and it was
# fixed at feature-006/t3, which is the task that owns it. Everything else
# passes, including the H2 count (6, inside 5-9), the figure count (3) and the heading-case gate,
# which is why the headings are written to that case in the draft rather than left to be fixed on
# the page (decision 16).
#   in-links per §5.2 (03, 10 and the hub in)   feature-006/a08-wirecommit
#   the fourth out-link §5.2 asks for, the one to article 10   feature-006/a08-wirecommit. The
#   three out-links this draft places all point at pages that exist today - rotating-magnetic-
#   field-1888.html from entry 8, magnet-motor.html and perpetual-motion-generator.html from the
#   closer - and the link to tesla-free-energy-what-he-said.html is not placed because that page is
#   not rendered and qa_page.py fails a dead relative href, which is the rule the earlier batches
#   followed as well
# Decisions these batches took, recorded where the next batch will read them (1 to 3 are
# feature-006/t1's; 4 to 8 are feature-006/a08-draft2's):
#   1. The §9 brief 08 hooks for entries 2 and 3 are contradicted by the print (register Rejected
#      #9 and #10). Entry 3's meter counts no bubbles and its unit is the lamp-hour; entry 2's
#      'the reason your capacitor is not in air' is a claim about a modern object, and this draft
#      makes no such claim. Both entries are written from the pinned sentences. The bubble point is
#      not argued in the body either; if the page wants to correct it, that is a 'what the internet
#      gets wrong' section at assembly, not a line in the entry.
#   2. Entry 2 is written as the entry that did not lose, per the register flag ENTRY 2 IS THE
#      ENTRY THAT DID NOT LOSE, with the ABB source for the modern half. The 1894 form is stated
#      as the part nobody builds. That is in tension with the brief's title claim that all nine
#      'never caught on', and the register says the same for entry 9. The title is the brief's and
#      the h1 mirrors it, so it is unchanged here; the standfirst says plainly that the volume
#      reports no failure. Flagged for the owner at REVIEW rather than fixed silently.
#   3. Entry 1's history sentence carries the IEEE source, which is what Rejected #7 requires.
#      Modern sources are paraphrased, never quoted: check_quotes.py matches every double-quoted
#      run in the body against the 1894 text, so a modern quotation in quotation marks is a FAIL.
#   4. Entry 4's brief hook is used the way the register says it must be (the flag THE 400-500-A-
#      MINUTE NUMBER IS A FOOTNOTE, NOT A SPEC): the number is printed as what the compiler's
#      footnote says about a horseshoe-magnet bench experiment he 'learned of' in an interview, and
#      the footnote's own 'very slow' sentence is printed beside it as the entry's 'why it lost'. It
#      is not printed as a speed, an output or a claim about any machine. The pyromagnetic generator
#      is named because the heading names it and the article's closing beat needs it.
#   5. Entry 4's 600 degrees centigrade is NOT in the draft. The flag THE BOOK'S 600° IS NOT THE
#      CURIE POINT forbids the comparison, and no modern source was fetched for entry 4, so the
#      temperature stays out; it may be added only with a source carried beside it in Sources.
#   6. Entry 5 is written from the chapter's opening sentence, which is about high-EMF direct-current
#      dynamos used for arc lighting, not from the brief's 'the problem every DC motor had' (the flag
#      ENTRY 5'S HOOK IS ABOUT MOTORS; THE PRINT'S FAULT IS A GENERATOR FAULT). No year is given for
#      either device: the chapter's only dates are 'some years ago' and 'A few years later', it
#      prints no patent number anywhere, and §6.3 needs a patent record checked before a year goes in.
#   7. Entry 6's 1885 is the compiler's date, and the sentence says the book gives the device a year,
#      not that Tesla dated his own work. The claim that no other year appears in the six chapters
#      entries 1 to 6 come from was measured, not recalled: books/tmp/f06a08d2/years_scan.out scans
#      the text of scan files 427 to 465 (printed pp. 409 to 447) for four-digit years and finds
#      exactly one, 1885, at printed p. 438. The priority claim is quoted from printed p. 390, in his
#      own chapter, with both hedges inside the marks; the elision in that quote is a cut over the
#      mechanism the entry has just paraphrased, not a cut over a corrupt scan.
#   8. The three 'nothing is reported' sentences in entries 4 to 6 are stated as absences in our own
#      words, never as 1894 verdicts (Rejected #21 and #22), and their scoped counts were re-run at
#      draft time as the register's WORD COUNTS flag requires (books/tmp/f06a08d2/counts_rerun.out,
#      grep_quote.py --count over printed pp. 424-431, 432-437 and 438-447). Two of them changed the
#      wording. 'output' and 'trial' are not 0 in pp. 424-431, one each, both at p. 429: 'meaning
#      larger output' about a design, and 'earlier trials' about somebody else's work. So entry 4
#      says neither machine is reported built, run or measured and no efficiency figure appears in
#      the chapter, which is a claim about what the chapter reports, not about which words occur in
#      it. And 'test' is 1 in pp. 432-437 only because 'greatest' contains it. A substring count is
#      not a word count - the register says so, and re-running it found the same thing again on the
#      first try. The same caveat applies to batch 3's counts: 'test' is 3 in pp. 451 to 464 only
#      because 'greatest' and 'slightest' contain it, and entry 8's absence sentence is written as
#      what the chapter reports, not as which strings occur in it.
#   9. The provenance paragraph goes before entry 1, not at the end, and it carries the two quotes
#      that prove the voice changes - the compiler's hand-over sentence and the footnote dating what
#      he hands over, both at printed p. 467. Both precede every quotation from pp. 467 to 474,
#      which is the order the register requires for entry 9: the reader meets the hand-over before
#      meeting Tesla's own sentences, so entry 9 does not have to stop and explain itself.
#  10. Entry 7 is written as the empty entry the register found (BATCH 3 finding 5): one pattern cast
#      in two halves, one stated advantage, and nothing else. No story is invented for it, and the
#      entry says in its own words that the chapter reports no build, no trial, no date and no
#      patent number. The chapter's closing move, widening the claim to machines 'of the ordinary
#      type generally used' (printed p. 448), is quoted rather than summarised because it is the
#      entry's reason for being on a list of things that did not catch on: nothing in it is specific
#      to Tesla's systems, and the entry says that makes it the least Tesla-shaped of the nine.
#  11. Entry 8 keeps 'rotary field' inside quotation marks with its p. 451 cite, and the link to
#      rotating-magnetic-field-1888.html is the bridge to article 07 the register authorises. The
#      company is named nowhere in the chapter, and the entry says the company is never named rather
#      than guessing at one. The p. 452 fifty-per-cent number is deliberately not used: read in the
#      raw scan it is an illustration of reducing waste currents by subdividing an armature core,
#      not a result for the lighting system, and a number in the entry would imply a tested system
#      the chapter does not report. Entry 8's absence sentence is about installation, load test and
#      result, which is what the chapter does not report; 'test' as a string is 3 in pp. 451 to 464,
#      all of it inside longer words.
#  12. Entry 9 quotes 'two years ago' inside the p. 474 sentence and then derives the date instead
#      of converting it: the entry states that the volume dates the notes to Sept. 2, 1891 and
#      labels the resulting 1889 as our arithmetic, not a date the volume states. The closer quotes
#      'worked satisfactorily' from the same sentence at a shorter length, which is why the two
#      greps of it return different ratios (0.989 in full, 0.963 cut short, per the register flag
#      THE CLI AND THE GATE DO NOT SHARE AN INDEX); the full sentence verifies through the
#      space-ignoring index because the scan glues 'bythe', and that is recorded in QUOTE CHECK
#      below rather than hidden by quoting the sentence only up to 'two years ago'.
#  13. The closing beat re-ran its own count at draft time instead of copying article 07's or batch
#      2's: grep_quote.py --count 'magnetic gener' over the whole volume returns 4 hits on the
#      default furniture-stripped index, on printed pp. 6, 429 twice and 496 (books/tmp/f06a08d3/
#      counts_rerun.out); with --keep-furniture it returns 5, adding the chapter heading at printed
#      p. 424. The body states the four, because the sentence it writes is about running text, and
#      says one page carries two so the count cannot be read as a miscount. The index line at
#      printed p. 496 was read in the raw scan, not inferred: it reads 'Pyromagnetic Generators'
#      followed by '429'. Article 07 already makes the same point in its own words with the same
#      three pages, so the two pages agree; this one adds the count and does not repeat its wording.
#  14. The intro's voice disclosure says eight of the nine chapters are the compiler's prose, not
#      six. The first pass of that paragraph said 'six of the nine chapters, printed pp. 409 to 447',
#      which is true of the six it named and misleading about the other three: the register's own
#      chapter list calls ch. XXXIX 'the compiler's prose again' and ch. XL 'the compiler's prose',
#      and only ch. XLI changes voice, partway down printed p. 467. Entries 7 and 8 are third-person
#      prose about Tesla, so an intro that stops at six leaves the reader to work out the rest. The
#      paragraph is 16 words longer for it; the count below is re-measured, not adjusted.
#  15. The nine entries are H3s under three H2s, not nine H2s. The draft as batch 3 wrote it had
#      eleven H2s (intro, nine entries, closer), and make_article.py adds a twelfth for the Sources
#      block, against the §12 gate 'H2 count 5-9' (qa_page.py line 177, 5 <= h2 <= 9 over the whole
#      rendered page; the shell contributes none, so the draft's own H2s are the whole count). Nine
#      entry H2s cannot fit under that ceiling whatever the intro and closer do, so the brief's nine
#      entries and §12 cannot both be honoured by nine H2s, and §12 is the gate. The three H2s are
#      the volume's own chapter blocks - chs. XXXIII-XXXV, XXXVI-XXXVIII, XXXIX-XLI - so the
#      grouping is the book's, not a thematic invention, and the nine entries keep the book's order
#      and their numbers. Article 09 is the precedent: its §9 brief lists nine structure items and it
#      shipped with six H2s and four H3s. The intro says the grouping follows the chapter blocks, so
#      the structure is explained rather than left for a reader to infer. This is what keeps
#      feature-006/t3 from failing on a structure the draft chose; the entry text itself is unchanged
#      by it, and the per-entry counts below are unchanged by it too.
#  16. The headings are written in the house title case in the draft, not left for the page. books/
#      harness/docs/CONSTRAINTS.md says the rule bites in the draft, because make_article.py renders
#      from it, and feature-006/a08-titlecase exists to check exactly this; the smoke render above
#      reports 0 findings, so that task now only has to confirm it. Two entry headings were reworded
#      to satisfy the tool rather than patched by it: '7. A Dynamo Frame Cast In Two Identical
#      Halves' reads to the tool as a heading whose first real word is an article, which it wants
#      lowercase, so it is now '7. One Frame Pattern, Cast in Two Identical Halves'; the same for
#      '9. The Disc That Makes...' -> '9. Discs That Make Direct Current Without a Commutator'. Both
#      say what the entry says. 'In' in the closing H2 and 'The' in the intro H2 follow the tool's
#      rule for short prepositions and mid-heading articles.
# 16b. CONFIRMED AT feature-006/a08-titlecase (2026-10-17), and not one byte of this draft or of the
#      page was changed to confirm it. Three measurements, all exit 0:
#        python3 books/tools/titlecase_headings.py --check website/tesla-weird-inventions-1894.html
#          -> '1 page(s) scanned, 0 heading(s) not title case', exit 0. That is the same code
#          qa_page.py's heading-case gate calls, so the gate and this number cannot disagree.
#        the draft re-rendered as it stands (make_article.py, feature-006/a08-wirecommit's command
#          without --wire) to books/tmp/f06a08tc/tesla-weird-inventions-1894.html: 45,641 bytes, cmp
#          clean against the committed page, and --check on that fresh render reports 0 as well. That
#          cmp is what makes the page check a check of the draft: the page is what the current tool
#          makes from these bytes today, so the case cannot be living only in the committed file. The
#          render was re-run after this block was written and cmp is still clean at 45,641 bytes
#          (books/tmp/f06a08tc/render_after_register_edit.out), which is the proof that a front-matter
#          comment moves no rendered byte and that the numbers above describe the bytes this file now
#          holds. All three commands and their exit codes are kept at books/tmp/f06a08tc/
#          titlecase_check_final.out. Two more were re-run on these same bytes because a register
#          edit is still an edit: qa_page.py on the page, 29/29 exit 0 with 'h2/h3 and FAQ names are
#          title case' ok, and check_quotes.py on the draft, 45 fragments, 45 verbatim and
#          page-cited, 0 problems, exit 0 - unchanged from the batch-3 count, because check_quotes
#          strips the front matter before it scans and this block is front matter.
#        books/tmp/f06a08tc/draft_titlecase_check.py (output draft_titlecase_check.out, exit 0,
#          0 findings) applies the tool's own titlecase() to this draft's heading lines, because the
#          tool reads <h2>/<h3> tags and cannot be pointed at a markdown draft at all. Result: 14
#          draft headings (5 H2, 9 H3), 14 already title case; the page's 15 h2/h3 strings are those
#          14 verbatim plus the Sources H2 sources_block() adds, so the two records are the same
#          list; 0 FAQPage blocks, so 0 mainEntity names to keep in step (front matter faq: [],
#          which is what §9 brief 08 asks for - §7 emits FAQPage only 'when faq present'); h1 and
#          its title/og:title/twitter:title mirrors all four identical and untouched.
#      WHAT THAT ROW MEASURED BEYOND ITS OWN PAGE, named and not fixed here. The open item
#      feature-001/heading-case-gate left on 2026-10-16 ('the retrofit stopped at the rendered
#      pages') is still open, and it now has a count: books/tmp/f06a08tc/other_drafts_titlecase_
#      scan.out runs that same titlecase() over every draft in new_content/1894-series/ and returns
#      11 drafts, 87 h2/h3 lines, 72 not title case. Article 08 is the only clean draft in the
#      series. Every other series page was retitled on its rendered page only, so re-rendering any
#      of those drafts puts sentence case back and fails the heading-case gate on a page that passed
#      last week. It belongs to feature-009/t2, whose §5.2 out-link work touches the series pages -
#      the 2026-10-16 lesson records that it re-renders 02 and 04, 7 lines each - and to
#      feature-012/t1 for the hub draft (8 of its 9 lines); the other 50 lines sit in drafts no row
#      re-renders today. One command per draft fixes it, and no page needs a hand edit.
# LENGTH. §9 brief 08 asks for nine entries of roughly 130 words in a 1,500-word listicle. All nine
# are counted with the command below, because a count without its method is the failure this
# register has already been corrected for twice. The method changed with decision 15: it now splits
# the body on any H2 or H3 line (kept as books/tmp/f06a08d3/len_check.py, which also strips the
# {{FAQ}}/{{CTA}}/{{SOURCES}} placeholders so page furniture is not counted as prose), and it
# reproduces batch 1's and batch 2's per-entry numbers unchanged, which is the check that the new
# method measures the same thing:
#   python3 books/tmp/f06a08d3/len_check.py   # output kept beside it at len_check.out
#   entry 1: 150, entry 2: 149, entry 3: 148   [feature-006/t1's three, re-measured 2026-10-17 by
#   that method and unchanged]   entry 4: 156, entry 5: 153, entry 6: 156
#   [feature-006/a08-draft2's three, unchanged]   entry 7: 165, entry 8: 162, entry 9: 171
#   [feature-006/a08-draft3's three, measured 2026-10-17 by that same command on the bytes this
#   file now holds, after the length pass recorded below; the same command on the bytes batch 3
#   first handed over gave 173, 180 and 176, and that earlier number is kept here rather than
#   overwritten, because the pass below is the reason the two differ. Re-measure again at assembly,
#   because the counts move with the text and a count taken before the sentence reporting it was
#   written is a stale count]
# The whole body measures 2,003 words by that command, re-run on the bytes this file now holds
# (books/tmp/f06a08d3b/len_check.out, 2026-10-17): standfirst 83, the provenance paragraph 287, the
# three group H2s 0 (they carry no prose of their own, by decision 15), the nine entries 1,410, the
# closing beat 223. Against the brief's 1,500 that is a third over, and
# part of it is structural rather than padding: the provenance paragraph and the closing beat are not
# in the brief's per-entry budget, and they are where the register's required voice disclosure and
# §9 brief 08's required closing beat live. Flagged for the owner at VERIFY in the same shape as the
# article 06 length flag; qa_page.py has no word-count gate to catch it either.
# The first six are 14 to 20 percent over the brief's number, and the overage is the register's rules, not
# padding: entry 1 needs the synchronism sentence to say why it lost, entry 2 needs the finding and
# the book's own hedge on its novelty, entry 3 needs the reversal step and the editor's verdict,
# entry 4 needs the sentence that puts the brief's 400-to-500 number on a bench experiment instead
# of on the machine, entry 5 needs the sentence that says the fault is a generator's and the hedge
# inside the book's own claim, and entry 6 needs both hedges of the p. 390 claim, which is the
# longest quoted run in the draft until batch 3, and is now second behind the p. 474 belt-contact
# sentence at 30 words. Entries 7 to 9 came out of batch 3 at 173, 180 and 176: 11 to 15 percent
# over the top of the band the first six set, which is the comparison this batch's acceptance
# criterion asks for, and 33 to 38 percent over the brief's number. A length pass on this batch's
# own prose brought them to 165, 162 and 171 - 4 to 10 percent over that band, 25 to 32 percent
# over the brief's number. What came out was connective wording of ours, not evidence: 'and closes
# by widening the claim', 'It also says the frame suits', 'the polyphase machinery of' became 'set
# out in' over the same article 07 link, 'and the book prints no measurement' turned into a colon,
# and the p. 464 lamp quote taken as its first clause only - 'the lamp cuts itself out automatically
# when the arc gets too long', where the draft had quoted the whole run including 'and reinserts
# itself automatically in the circuit if the carbons drop together'. The full run stays in quotes.md
# at printed p. 464 for whoever wants it back. No entry lost a page cite and no page left the body:
# check_quotes.py re-run on these bytes still reports 45 fragments, 45 verbatim and page-cited, 0
# problems, and pages_used above still equals the set of pages the body cites, read out by the same
# regex. The p. 474 belt-contact sentence was not cut, and the p. 464 self-reinserting half was the
# only quote shortened: the closer's 'until their inventor ran out of time' rests on the p. 474
# sentence, so cutting it there would have unmoored a claim the closing beat makes. The same shape,
# for the same reasons, at the new lengths. Entry 7 needs the
# sentence reporting that the chapter gives no build, no trial, no date and no patent number, because
# the register says the entry has no story and must not be given one. Entry 8 needs the company
# sentence and the sentence saying the company is never named, which is the only narrative the volume
# supplies for any of the nine, plus the bridge to article 07. Entry 9 needs the date derivation,
# because the register requires 'two years ago' to be shown as arithmetic done on the volume's own
# date-stamp rather than as a date the volume states, and it carries the 30-word p. 474 sentence,
# which is the only report of a machine built and worked anywhere in these nine entries.
# Cutting to 130 would mean dropping a quote, and with it the page cite the entry exists to carry.
# Quotes the register pins that were left out for that reason, available if the owner wants the
# entries longer: 'an active (as distinguished from a dead) resistance' (printed p. 416) for entry 1;
# 'since the gain of one conductor should equal the loss of the other' (printed p. 422) for entry 3;
# the p. 425 induction refinement, the p. 428 fly-wheel sentence and the p. 430 cooling claim for
# entry 4; the p. 433 matched-faces sentence and the p. 437 mercury quote for entry 5; the p. 441
# prior-art pair and the p. 447 lights claim for entry 6. This is a brief-owner call at VERIFY in
# the same shape as the article 06 length flag, and qa_page.py has no word-count gate to catch it
# either.
#
# QUOTE CHECK, the whole draft as it now stands. python3 books/tools/check_quotes.py
# new_content/1894-series/08-tesla-weird-inventions-1894/article.md, run on 2026-10-17 on the bytes
# this file holds: exit 0, 1 file, 45 quote fragments, 45 verbatim and page-cited, 0 problems
# (books/tmp/f06a08d3/cq_final.out). That is batch 1's 13, batch 2's 14 and this batch's 18. The count is stated
# with the command, the date, the exit code and the output file, per the register's rule that a
# count without its method is a claim the next draft copies wrong. The tool counts fragments, not
# quoted runs, and splits a quotation cut by ' ... ' into its two halves, which is why 45 fragments
# come from 43 quoted runs: the p. 412 synchronism quote in batch 1 and the p. 390 claim in batch 2
# are each one run cut in two, which is visible in the tool's own output as two adjacent
# fragments of one sentence; batch 3 adds no cut of its own, so its 18 fragments are 18 runs. Batch 1's own pass recorded 17 fragments for a body the tool reports as
# 13, and 17 does not reproduce on any version of those bytes. Two fragments verify through the
# space-ignoring index rather than the normal one: 'the electrical
# resistance of the conductor is varied in a definite proportion to the strength of the current',
# printed p. 420, because the OCR glues 'isvaried', and 'Several machines with belt contact were
# constructed by the writer two years ago, and worked satisfactorily ; but for want of time the work
# in that direction has been temporarily suspended', printed p. 474, because the OCR glues 'bythe'.
# The register annotates both the same way, and its flag THE CLI AND THE GATE DO NOT SHARE AN INDEX
# names six such fragments in its own batch-3 sweep; the clean forms are the print's, and the p. 474
# sentence is quoted in full on purpose rather than cut at 'two years ago', which is where a shorter
# grep of it returns 0.963 instead of 0.989. The other 43 are exact
# matches. One fragment, 'some years ago' at printed p. 432, is short enough that the tool finds it
# on three pages (233, 388 and 432) and reports the citation as correct against the one it is cited
# to; it is kept because the entry's point is that the chapter gives no year. The phrase is 14
# characters, just over the tool's 12-character fragment floor. The tool strips the frontmatter
# before it scans (check_quotes.check(), the
# '\n---' split), so the numbers in this comment are not part of what it counts and cannot inflate
# themselves the way the self-count in quotes.md does.
# ONE SCANNER FACT THAT CHANGED HOW A SENTENCE HAD TO BE WRITTEN. A short quoted run placed
# immediately before a long one breaks the long one. Entry 6 first read 'he writes of himself as "the
# writer": "as far as records go, ..."'. The scanner took 'the writer' (10 characters, under its
# 12-character fragment floor), moved one quote mark on, and paired the closing mark of that phrase
# with the closing mark of the p. 390 quote, so the fragment it tested began with a quotation mark
# and came back 0.995, a FAIL, on a sentence that greps at ratio 1.0 through the CLI
# (grep_quote.py 'as far as records go, he seems to have been the first who has successfully
# regulated machines' --page 390-390, and the full sentence, both 1.0). The fix was to put the
# third-person point in our own words and keep only the p. 390 sentence inside the marks: a short
# quoted term in front of a long quote has to use single quotes, or none.
# Re-run this at feature-006/t3 on the finished page; the number above describes this draft and
# nothing after it.
faq: []
---
**Standfirst.** Nine devices, each cited to the printed page of the 1894 book that collected them. The volume never says any of them failed, and for most of the nine it says nothing at all about what became of them. What it does record, entry by entry, is the thing each machine needed and had not got: a rotating armature turning in step with the line, a dielectric with no gas in it, a current that had to be reversed after every reading.

## Before the Entries: Whose Words These Are

Nine devices, all from Part III of the 1894 volume, the part its editor titles 'MISCELLANEOUS INVENTIONS AND WRITINGS'. He announces it in his own inventory of the book, printed p. 6: "Mr. Tesla's work ranges far beyond" (1894, p. 6) the polyphase work the rest of the volume is about, and names the section's contents: arc lighting, pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, improvements in dynamos, electrical meters, condensers, unipolar dynamos. That sentence, not any editorial choice of ours, is why this list has nine entries.

Whose words these are changes halfway through. Eight of the nine chapters are the editor writing about his subject in the third person, start to finish, entries 7 and 8 included; on the six that run from printed p. 409 to p. 447 the tells are plain: 'Mr. Tesla divides such circuit' (1894, p. 409), 'attributable to Mr. Tesla' (1894, p. 420). The ninth chapter is the exception, and the book says so. From the middle of printed p. 467 the compiler hands the chapter over - "It is thought appropriate by the compiler to append here some notes on unipolar dynamos, written by Mr. Tesla, on a recent occasion" (1894, p. 467) - and the footnote on that page dates it: "Article by Mr. Tesla, contributed to The Electrical Engineer, N. Y., Sept. 2, 1891" (1894, p. 467). Entry 6 borrows a sentence from a chapter that is his own, where he writes of himself in the third person. Every quotation mark below is the print's; every page number is the printed folio. The three headings that follow keep the book's order - chapters XXXIII to XXXV, XXXVI to XXXVIII, XXXIX to XLI - three chapters at a time.

## Currents, Condensers and Meters

### 1. Direct Current From Alternating Current

Chapter XXXIII splits an alternating circuit "at any desired point into two branches or paths" (1894, p. 409). One branch opposes one sign of the wave, the other the opposite sign, so the two halves go different ways. What comes out is "two or more direct currents without the employment of any commutator" (1894, p. 409). Not needing a commutator is the claim.

The volume never says the scheme failed. What it says three times, of three machines, is that they must turn in step with the supply: "the rotation and action of the commutator must be in synchronism ... with the periods of the alternations" (1894, p. 412). That is the difficulty: a rotating part tied to the line frequency. Conversion later went to static devices, and the last rotary converters feeding New York direct current were shut down in 1977 and replaced by solid-state rectifier units (Blalock, 2013).

![](/assets/tesla1894/p410-fig220.webp)

### 2. Condensers With the Plates in Oil

In high-frequency, high-potential apparatus the expected insulators are wrong: glass and mica, the bodies with the highest specific inductive capacity, are "inferior as insulators" (1894, p. 418). The reason is gas. It is "very desirable to exclude all gaseous matter from the apparatus" (1894, p. 418), because molecular bombardment in it wastes energy and injures the device. The device is a can. Its plates are held apart by porous strips "used merely for the purpose of maintaining them in position" (1894, p. 419): the oil is the dielectric. The book hedges its own novelty: oil between conductors "has been a common practice" (1894, p. 419). That hedge is why this entry did not lose. Vacuum oil impregnation is still how high-voltage paper insulation is made, because oil leaves no voids; oil-impregnated bushings hold more than 80 percent of that market (Jonsson and Johansson, 2009). Nobody builds the 1894 form.

![](/assets/tesla1894/p418-fig227.webp)

### 3. Electrolytic Registering Meter

Chapter XXXV opens with "an ingenious form of electrolytic meter attributable to Mr. Tesla" (1894, p. 420): metal is plated onto one conductor and stripped from the other until "the electrical resistance of the conductor is varied in a definite proportion to the strength of the current" (1894, p. 420). The unit is the lamp-hour: the book measures "the increase of resistance of one conductor or the diminution of the resistance of the other per lamp hour" (1894, p. 422). Then the fatal step, in the same chapter: after every registration the current must be reversed, "so that the deposit will be taken from the conductor which has gained and added to that which has lost" (1894, p. 423). The editor's own verdict on the whole class closes the chapter: such meters "seem to need every auxiliary advantage to make them permanently popular and successful" (1894, p. 423).

## Heat, Brushes and Regulation

### 4. Thermo-Magnetic Motor and Pyromagnetic Generator

Heat destroys magnetism: an iron bar "when heated to redness loses its magnetism" (1894, p. 424). Tesla's thermo-magnetic motor runs on that: a burner heats an armature that a magnet pulls. The pyromagnetic generator puts the same effect to work in a coil (1894, p. 429). The compiler's own hedge on how far the work went: "he has but glanced at them" (1894, p. 424).

The spirit lamp and the L-shaped iron strip are a bench experiment, not the machine: the compiler heard of it in an interview with Tesla, and the strip vibrates against a horseshoe magnet "as rapidly as 400 to 500 times a minute" (1894, p. 424). The same footnote gives the limit - vibration is "very slow owing to the inability of the iron to follow rapid changes in temperature" (1894, p. 424). Neither machine is reported built, run or measured, and no efficiency figure appears in printed pp. 424 to 431.

### 5. Anti-Sparking Brush and Commutator

The fault is a generator's, not a motor's. In "direct current dynamos of great electromotive force - such, for instance, as those used for arc lighting" a spark appears when a commutator bar leaves the brush (1894, p. 432). The book calls the older fixes "expensive or not fully available" (1894, p. 432). Tesla's first device was mica or asbestos behind the brush, dated only as "some years ago" (1894, p. 432). His second was two matched discs, commutator and collector built alike, so the short circuit and the break "occur at the same instant" (1894, p. 434). The claim is hedged: it promises "a reduction which amounts practically to a suppression of the spark" (1894, p. 434). The insulating segments are stone: "glass, marble, or soapstone" (1894, p. 436). The last version has liquid mercury for segments (1894, p. 437). Neither is reported tested or run in printed pp. 432 to 437.

### 6. Auxiliary-Brush Regulation of Direct Current Dynamos

Chapter XXXVIII is the only one of the six chapters entries 1 to 6 come from that gives a device a year: "devised by him as far back as 1885" (1894, p. 438). No other year appears in them. The regulator adds a third brush on the commutator, bridged to a point on the field winding. Move it and "more or less of the current through the field-helices is diverted through the shunt" (1894, p. 438); set it right and, on the book's own rule, the brush carries no current at normal load (1894, p. 441).

The priority claim is his own, in another chapter, on high-frequency alternators, where he writes of himself in the third person: "as far as records go, he seems to have been the first who has successfully regulated machines ... by means of a third brush" (1894, p. 390). Chapter XXXVIII reports no installation, load test or result for the regulator.

## Frames, Lamps and Discs

### 7. One Frame Pattern, Cast in Two Identical Halves

Chapter XXXIX is three printed pages, one device, and no story. "The field magnets and frame are cast in two parts. These parts are identical in size and shape" (1894, p. 448): one pattern, two halves, bearings cast in with the frame. The claim is manufacture, not performance: the machine "requires fewer parts, and which involves less trouble and expense in its manufacture" (1894, p. 448).

The one technical reason is a bearing placement: "The bearings for the shaft are located at the neutral points of the field, so that the armature core is not affected by the magnetic condition of the field" (1894, p. 450). The book prefaces that with "This machine possesses several advantages" (1894, p. 450) and supplies exactly one. Nothing in printed pp. 448 to 450 says the frame was built or tried, and no date or patent number appears in it. The frame suits machines 'of the ordinary type generally used' (1894, p. 448): the least Tesla-shaped of the nine.

### 8. Tesla's Direct Current Arc Lighting System

Chapter XL is the only one that says what became of the device. Tesla's direct current arc lighting system "was confided to a company formed for its exploitation"; he then turned to what the compiler calls his 'more celebrated' "rotary field" system (1894, p. 451), set out in [the paper Tesla scribbled in pencil](rotating-magnetic-field-1888.html). The company is never named. The book's reason it did not win: a crowded market and a compliment. The apparatus "appeared at a time when a great many other lamps and machines were in the market" (1894, p. 451).

The lamp is the clever half: two electro-magnets pull against each other on the carbon-feed lever. The feed is so fine that "the movement of the rod cannot be detected without some actual measurement" (1894, p. 463): the book prints no measurement. Its last claim: "the lamp cuts itself out automatically when the arc gets too long" (1894, p. 464). The chapter reports no installation, load test or result.

### 9. Discs That Make Direct Current Without a Commutator

A unipolar machine is a disc turned between the poles of an even field; its current runs from centre to rim, "of one direction without the employment of commutating devices" (1894, p. 468). A useful voltage needs very high speed or a very large disc, and at either "it becomes difficult to secure and maintain a good electrical connection between the collecting brushes and the conductor, owing to the high peripheral speed" (1894, p. 465).

The rest of the chapter is Tesla's own writing. His answer: "a flexible conducting belt may be employed to advantage" (1894, p. 474). Then the one sentence in this list that reports a machine built and run: "Several machines with belt contact were constructed by the writer two years ago, and worked satisfactorily ; but for want of time the work in that direction has been temporarily suspended" (1894, p. 474). The book dates those notes to Sept. 2, 1891 (1894, p. 467), so 'two years ago' means about 1889 - our arithmetic, not the volume's.

## The Only Magnetic Generator in This Book

Entry 4 is the one that concerns this site. Search the text layer of our copy of the volume for 'magnetic gener': four hits on three printed pages, one page carrying two - the editor's inventory (1894, p. 6), the chapter text at printed p. 429, and the volume's own index entry "Pyromagnetic Generators" (1894, p. 496), which points back to p. 429. Every one is pyro-magnetic. There is no other. The generator this book attaches that phrase to is entry 4's machine: one that works because heat destroys magnetism, with a flame under it, in a chapter that reports no output, no efficiency figure and no trial.

![](/assets/tesla1894/p430-fig242.webp)

The pages here about magnet motors and perpetual motion are [the Tesla magnet motor](magnet-motor.html) and [perpetual motion machines](perpetual-motion-generator.html). Neither cites this book, and nothing on this page is evidence for what they sell. What this page can say is narrower: the only magnetic generator in the 1894 volume is a heat engine, and none of the nine machines here is one either.

The book never says these nine failed. For seven of them it records no trial, no output and no result. For two it records something else: entry 2's principle is still how high-voltage paper insulation is made, and entry 9's machines "worked satisfactorily" until their inventor ran out of time (1894, p. 474).

{{FAQ}}

{{CTA}}

{{SOURCES}}
