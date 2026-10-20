---
title: "The Flame That Doesn't Burn: Tesla's Cold Fire"
slug: tesla-cold-flame.html
pretty_slug: /tesla-cold-flame
description: "Tesla held a flame up to a lecture hall and dared them to call it not a flame. The 1894 book also says it is hot. Here is what he claimed."
keywords: [tesla cold flame, tesla cold fire, electric flame tesla, brush discharge 1894, tesla flame without combustion]
date_published: "2026-10-23"
date_modified: "2026-10-23"
series_no: 6
primary_query: tesla cold flame
tid: "1894_06"
og_image: assets/og/tesla-cold-flame.webp
# card_image is figure 1 of the page, as on every other article in the series. Repointed at
# feature-005/t6 from the 150 ppi extractor crop p186-fig1.webp to the verified Fig. 110 crop, which
# is the image the p. 166 prose actually argues with.
card_image: assets/tesla1894/p165-fig110.webp
card_alt: "1894 photograph, Fig. 110, printed p. 165: an induction coil with its primary laid sideways across the bottom and an insulated column at either end, a pale brush of discharge rising from the top of each column"
standfirst: "The 1894 book prints a man holding a flame up to a lecture audience and asking whether it is less a flame because it does not scorch his hand. It also prints three sentences in which he insists that flame is hot. The phrase 'cold flame' is in it zero times, and so is the reason he never built the lamp."
figures:
  # VERIFIED AGAINST THE PRINTED PAGES, feature-005/t6, 2026-10-11 and 2026-10-12. Each crop below
  # was opened next to a 500 ppi render of the page it came from and the figure number was read off
  # the printed caption in that render, never off an extractor filename or an OCR caption (§6.6).
  # The zoom crops that carry the reads are committed next to this file, under
  # figures/ (see figures/README.md for what each one proves and its sha256); the 500 ppi
  # page renders they were cut from are in gitignored books/tmp/ and are regenerable with
  # books/tools/fig_crop.py --printed <N> --view --view-ppi 500. scan-p183-500ppi.png = printed p. 165,
  # scan-p186-500ppi.png = printed p. 168, scan-p244-500ppi.png = printed p. 226
  # (printed page = scan file - 18, §0). Each crop is at
  # 500 ppi, the native resolution of the scan image embedded in the page PDFs (1856 x 3227 px a
  # page, measured on the renders of scan files 183, 184, 186 and 244), carries its printed caption inside the crop, and is the whole plate rather than the
  # 150 ppi fragment the extractor cut. Figure weight as used: 56 + 51 + 51 = 158 KB, inside the
  # 400 KB article gate. What was read off the print, and where:
  #   printed p. 165 (scan file 183): two photographs side by side, 'FIG. 109.' under the left and
  #     'FIG. 110.' under the right (figures/p165-caption-band-fig109-fig110.png). Figure 1 below is the
  #     right-hand plate. Fig. 109 is the same coil with a horizontal conductor across the top of
  #     it, a small brush at one end of that conductor and a bright knob at the other; it belongs to
  #     the points-and-capacity discussion on that page and is not used here.
  #   printed p. 168 (scan file 186): printed caption 'FIG. 111.', and the body reference on the
  #     same page reads 'nel, Fig. 111, which widens when the potential is increased'
  #     (figures/p168-printed-caption-fig111.png and figures/p168-bodyref-fig111-line.png). The OCR
  #     renders both as 'FIG. ill.' for 111.
  #   printed p. 226 (scan file 244): printed captions 'FIG. 141.' under this plate and 'FIG. 142.'
  #     under the plate to its right (figures/p226-caption-band-fig141-fig142.png). Figure 3 below is the
  #     left-hand plate. The small italic letters inside this plate, by the tube, at the pool and at the
  #     ring, are smudges even at 500 ppi (figures/p226-fig141-part-letter-zoom.png), so the alt text
  #     names shapes only and the parts are named in the caption from the p. 226 prose, which is the
  #     quote pinned in quotes.md under 'Printed p. 226 (scan file 244)'. The globe label is NOT one of
  #     the illegible ones. It was re-opened at 500 ppi at feature-005/a06-figrec on 2026-10-12 because
  #     the record contradicted itself there, and it is an italic L. Two reads settle it, both against the
  #     print of the same page, and both recorded in figures/README.md with their exact boxes:
  #       (a) the printed line that names the globe. The page's text layer puts the word it renders 'Z,'
  #     at x 245.088-252.351 pt, y 384.330-392.338 pt of a 267.264 x 464.544 pt page, i.e. 6.9444 px
  #     per pt in the 500 ppi render. Cropping that box (x 1381, y 2645 to x 1770, y 2743) shows the
  #     line ending '...lamp globe L,': a serif bar across the top of the letter, one stem slanting
  #     down-left, a foot running right and turning up at its end, then a comma. That is an L; a Z needs
  #     a top bar the full width of the letter and a flat bottom bar, and this glyph has neither
  #     (figures/p226-textline-globe-L.png, sha256 c2d99d772a24d88a4da080d1f087babc6ebbbd0518eaf6fb
  #     d69431f242fd7fe3).
  #       (b) the plate label is the same letterform. Mapped at native pixels, no interpolation, the
  #     glyph at the right edge of the globe (x 795-818, y 1467-1490 of the render) has the same three
  #     strokes in the same arrangement as that printed italic L: short serif bar above the top of the
  #     stem, one stem slanting down-left, foot running right and turning up. It is 23 px tall against
  #     the body text's 33 px, which is why a 4x LANCZOS upscale of it reads as a '7' - the interpolation
  #     smears the serif bar into a top bar and the rising foot into a flat one. The crops are
  #     figures/p226-fig141-globe-label.png (180 x 160 px, box x 740 to 920 and y 1440 to 1600 of
  #     books/tmp/scan-p244-500ppi.png, sha256 f8f427dd67fcebbacb0717808dfc5ad3beaeb9787be459b353dcb9e04619cfa0)
  #     and the same crop at 4x, figures/p226-fig141-globe-label-4x.png, sha256
  #     b8c69c9b293e1a164a0aa6897b71f76e13294886f72f4923490bea083a108e6e; the read was made from the
  #     native pixels, not from the upscale. Both label crops re-derive from those boxes exactly:
  #     re-cut at this task out of books/tmp/scan-p244-500ppi.png, the plate crop reproduces sha256
  #     f8f427dd... byte for byte and the printed-line crop reproduces c2d99d77... byte for byte, so
  #     the boxes are not an approximation and anyone can re-make the read from them.
  #     So the text layer is the wrong one twice over: it prints 'incandescent lamp globe Z' where the
  #     type says L, and it renders the barometer tube's label as '&' in the same sentence. The p. 227
  #     line 'When the globe L (Figs. 141 and 142)' on printed p. 227 is not quoted on the page but is
  #     verbatim in the volume's text layer, and the p. 228 sentence 'it is usually sufficient to grasp
  #     the globe L with the hand', which the page quotes in its FAQ answer, are clean text and agree
  #     with the plate.
  #     The caption and the quoted description keep eliding the letter positions, because check_quotes.py
  #     checks against the OCR text and 'globe L' would not match it there; the label is recorded here
  #     and in figures/README.md, not in the page copy.
  # No other article in this series carries Figs. 109, 110, 111 or 141 (index.json figures[] read
  # 2026-10-11 and again 2026-10-12), so §6.6's no-reuse rule is satisfied.
  # NONE OF THE THREE IS AN ENGRAVING. The art in this part of the volume is photographic: Figs. 109
  # to 111 are halftone photographs of the coil with the discharge running, retouched to a black
  # ground, and Fig. 141 is a drawing printed in reverse, bright lines on a dark ground. The alt text
  # and the captions say which is which, per §6.6, 'alt describes the apparatus as actually seen, not
  # as the OCR caption claims'.
  # FIGURE 1 IS NOT ON THE PAGE THE SENTENCE POINTING AT IT IS ON. The p. 166 sentence quoted in the
  # body ends '(Fig. 110)', but the plate is set in the text of printed p. 165 (scan file 183), the
  # reverse of the same leaf: two photographs side by side on that page, 'FIG. 109.' under the left,
  # 'FIG. 110.' under the right. The extractor cut nothing from scan file 184 because printed p. 166
  # is all text, which is why the draft named a p184-* file; there is no plate on that page to crop.
  # p165-fig110.webp is the right-hand plate of the pair. The left-hand plate, Fig. 109, is the same
  # coil with a horizontal conductor across the top of it, a small brush at one end of that conductor
  # and a bright knob at the other; it belongs to the points-and-capacity discussion on printed p. 165
  # and is not used here. No other article in this series carries Figs. 109, 110 or 111 (index.json
  # figures[] read 2026-10-11).
  - src: /assets/tesla1894/p165-fig110.webp
    alt: "1894 photograph, Fig. 110, printed p. 165: an induction coil photographed against a black ground, its primary wound in many flat turns and laid sideways across the lower part of the plate, an insulated metal column standing at either end of it, and from the top of each column a pale discharge rising straight up, bright at its root just above the metal and widening upward into a tufted plume, the two plumes alike in height and shape"
    width: 761
    height: 681
    caption: "Fig. 110, printed p. 165, with the printed caption inside the crop. The sentence that points at this plate is set in the paragraph on the next printed page. The prose says what is drawn: the primary coil is placed sideways, it is best to replace the usual terminals of the coil with a pair of metal columns insulated with a good thickness of ebonite, and when the fissures are closed with wax 'the brushes cannot form anywhere except at the tops of the columns' (1894, p. 166). Two columns, and a brush at the top of each: that is the arrangement in the photograph. And 'one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure' (1894, p. 166). From the Columbia College lecture of May 20 1891. Public domain."
  # Figure 2, mid-article: the whole plate at 500 ppi, which supersedes p186-fig1.webp (444 x 412, a
  # 150 ppi cut of the middle of the plate with no printed caption). manifest_qc.csv row 74 described
  # that crop as 'a primary coil with a pear-shaped vacuum lamp glowing above it', which is not what
  # the p. 168 prose describes for the plate it numbers Fig. 111. The OCR of this page renders the
  # figure number as 'FIG. ill.' in the printed caption and 'Fig. Ill' in the body reference; the
  # print itself was read off the 500 ppi render at 4x (figures/p168-bodyref-fig111-line.png)
  # and says 'Fig. 111, which widens when the potential is increased'. 'luminous funnel' is 1
  # occurrence in the volume, printed p. 168. No other article carries this plate.
  - src: /assets/tesla1894/p168-fig111.webp
    alt: "1894 photograph, Fig. 111, printed p. 168: the same kind of coil, its primary in many flat turns along the bottom of the plate and an insulated column at either side; standing on the top of the right-hand column is a bright pear-shaped glow, broad and rounded at the top and narrowing to a thin bright stem that runs down to the terminal, with a short ribbed section and a small dark fitting above it; the column at the left is capped by a small bright discharge"
    width: 709
    height: 717
    caption: "Fig. 111, printed p. 168, with the printed caption inside the crop. The text on this page numbers the plate and names the shape: a small button, or preferably a very thin wire or filament, enclosed in an unexhausted globe and connected with the terminal of the coil 'may be rendered incandescent', and the phenomenon is made much more interesting by 'the rapid spinning round in a circle of the top of the filament, thus presenting the appearance of a luminous funnel' (1894, p. 168). The printed line goes on, 'Fig. 111, which widens when the potential is increased'. The bright pear standing on the terminal of the coil is that funnel. This is the step from a brush to a lamp, and it is why the argument of this page ends at a bulb. Public domain."
  # Figure 3, closing section: the left-hand plate of the Fig. 141 / Fig. 142 pair set on printed
  # p. 226. This supersedes p244-fig1-fig141.webp (836 x 624), which is the extractor's two-figure
  # band: both plates cut off top and bottom, no printed caption, and it is the dark un-negated
  # plate manifest_qc.csv row 99 describes. The p. 228 plates (Figs. 144, 145) are already article
  # 02's and the p. 179 plates are article 01's, so §6.6's no-reuse rule points here.
  - src: /assets/tesla1894/p226-fig141.webp
    alt: "1894 drawing printed in reverse, bright lines on a dark ground, Fig. 141, printed p. 226: a large pear-shaped lamp globe, and sealed into its neck a long narrow tube with thick walls shown in section by diagonal hatching, running down through the neck into a bulbous chamber at the lower end that is filled with a hatched pool; the top of that tube is blown out into a small sphere centred inside the large globe, and that small sphere is filled with a stippled mass; a thin rod runs down the bore of the tube, ends in a bright point just above the pool, and continues out of the chamber and down to a small ring"
    width: 515
    height: 943
    caption: "Fig. 141, printed p. 226, the whole plate with its printed caption inside the crop; the plate beside it on the same page is Fig. 142. The book describes this bulb on the same printed page: 'In Fig. 141 the bulb comprises an incandescent lamp globe ... in the neck of which is sealed a barometer tube ... the end of which is blown out to form a small sphere' (1894, p. 226). The drawing matches that description part for part: the small sphere is blown at the end of the long tube and set in the middle of the large globe, as the text on that page requires it to be, and it is filled with a stippled mass of conducting powder, which the following page says is led to the generator. No wire enters through the glass, which is also what that page advises. This is the apparatus behind the passage quoted above, a brush 'formed at, or near, a single terminal in high vacuum' (1894, p. 226), and the ancestor of the desk globe. Public domain."
# §5.2 out-link map for this article: 7-interesting-facts-about-magnets.html (present, below),
# 01 = tesla-lit-lamps-without-wires.html (present, below) and 12 = tesla-glowing-tubes-vacuum.html.
# CLOSED 2026-10-20. That third target was deferred, not skipped: article 12 was feature-006 and was
# not rendered, so website/tesla-glowing-tubes-vacuum.html did not exist and a link to it would have
# failed qa_page.py's dead-link gate. It goes in when 12 is written, and 12's own §5.2 row already
# requires it to link back here; both halves of that are now in. Body out-links as drafted: 4
# (01, 11, 7-interesting-facts, 05), inside §5.2's 4-6 band; with 12 the page is at 6, the top of
# the band, and it carries no more. The link to 11 is required by §9 brief 06
# section 4, 'cross-ref Ch. XXIX, article 11', which is the chapter the alternator numbers quoted
# from printed p. 376 and printed p. 381 come from. The link to 05 is off-map and is here for one
# reason: the same Columbia College lecture of May 20 1891 supplies both pages, and 05 is where this
# site carries that lecture's own caution about high-frequency currents used with condensers. It is a
# safety bridge, not a way of making a number.
# The reciprocal gate is now closed on this page, and it was never a thing this page could do by
# itself: §5.2 requires 06 to be linked from 01, from 12 and from the hub, and none of those could
# link to a page that did not exist when they were written. All three now do: 01's backlink went in
# on 2026-10-20 in the same pass that closed this one, 12 links here from its own body, and the hub
# links here from its twelve-item list. The earlier note that 01's backlink 'goes in at
# feature-009/t1' did not happen; it is recorded here as done at a different task.
# LENGTH, flagged not hidden. The body of this draft is 5,113 words. §9 brief 06 targets 1,200 and §3
# puts flagships at 1,200-1,800 with 'Do not pad' and the thicken*.py habit banned. This is out of
# band by a factor of nearly three, and it is the largest piece in the series; the six already accepted
# run 1,771 to 3,319. qa_page.py has no word-count check, so the t7 numeric gate will not catch this
# and passing t7 will not mean the length is right. It is an owner call at VERIFY, not something to
# fix silently here: cutting to band means removing whole verified quote chains (the scaling argument
# at pp. 166-167 and 213, the alternator numbers at pp. 376 and 381) and would change what the page
# argues, which is a decision for the human, not for the next pass of the generator.
cta:
  text: "Tesla's cold flame failed on one thing only: he could not build the frequency. That is a problem of apparatus, and it is the same problem a real home supply asks you to solve on paper first: what the machine is actually rated to put out, and at what."
  href_suffix: "1894_06"
pages_used: [121, 145, 166, 167, 168, 169, 171, 198, 213, 226, 227, 228, 258, 259, 291, 322, 376, 381]
faq:
  - q: "What is Tesla's cold flame?"
    a: "A brush of discharge at the end of a wire, presented to a lecture audience as a flame. The phrase 'cold flame' does not occur in the 1894 volume, and neither does 'cold fire' (0 occurrences each, whole-word, whole volume). What does occur is a London lecture of February 1892 in which Tesla produces a brush on a wire in front of the Institution of Electrical Engineers and says of it: 'The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light; but is it the less a flame because it does not scorch my hand'? (1894, p. 258). Coolness is his comparison, not his adjective. The same volume says three times that the brush is hot: 'they are veritable flames, for they are hot' (1894, p. 166), 'scorching hot air escapes at the top of the tube' (1894, p. 167), and 'Anything held within the brush is, of course, rapidly heated' (1894, p. 167)."
  - q: "Does a cold flame break the physics of combustion?"
    a: "No, and he never claimed it did. His point is about the source of the light, not about getting energy for nothing: 'a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place' (1894, p. 167). In modern terms a brush is a corona discharge: where the field at a conductor exceeds the dielectric strength of air, about 30 kV per cm at standard temperature and pressure, the air ionises, an electron avalanche follows, and the glow is photon emission from that gas, with audible noise, real power loss and chemically active gas as by-products (Zobaa et al., Scientific Reports, 2025). Nothing comes from nothing, and his own bookkeeping agrees: he writes that such impulses cannot be sent along a wire in air 'for most of the energy would be lost in molecular bombardment and consequent heating' (1894, p. 291)."
  - q: "Why did Tesla never build the cold-flame lamp?"
    a: "He says so, twice, and the reason is a frequency he could not generate. Near a brush 'the enormous potential may be made to alternate or fluctuate perhaps many million times a second' (1894, p. 168), and to get the flame he says 'we only need to perfect methods of producing enormous frequencies and potentials' (1894, p. 167). The 1894 volume's own account of his best alternator gives about 15,000 alternations per second as the practical ceiling of one design (1894, p. 376) and 30,000 per second from another (1894, p. 381). Off-the-shelf apparatus failed as well: 'In employing a commercial coil, the production of very powerful brush effects is attended with considerable difficulties', and 'the best insulation is apt to give way' (1894, p. 169). So he put the terminal inside an evacuated bulb instead, and states plainly why: 'This is done merely to enable the apparatus to perform the work which it is not capable of performing at ordinary air pressure' (1894, p. 259)."
  - q: "Is a plasma globe the same thing as Tesla's brush?"
    a: "It is the same phenomenon in a bulb, and he describes that bulb. 'It may be quite properly ranked among the brush phenomena - in fact, it is a brush, formed at, or near, a single terminal in high vacuum' (1894, p. 226). To run one he gives the modern demonstration exactly: 'it is usually sufficient to grasp the globe L with the hand' (1894, p. 228). He also records the behaviour every plasma globe shows, that 'the approach of the observer at a few paces from the bulb will cause the brush to fly to the opposite side, and if he walks around the bulb it will always keep on the opposite side' (1894, p. 228). A toy globe is low-pressure gas, usually krypton, xenon or neon, with an electrode at the centre driven by a high-voltage high-frequency transformer of a few kilovolts at a frequency around 35 kHz (Arizona State University Physics Instructional Resource Team). It is not a flame and it burns nothing."
sources:
  - text: "Chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY', a lecture delivered before the American Institute of Electrical Engineers at Columbia College, N. Y., May 20, 1891. The chapter's footnote verifies as printed at p. 145 and the chapter runs printed pp. 145 to 197. The brush passages used here are printed pp. 166 to 169 and p. 171"
  - text: "Chapter XXVII, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF HIGH POTENTIAL AND HIGH FREQUENCY', a lecture delivered before the Institution of Electrical Engineers, London, February, 1892. Its footnote verifies as printed at p. 198 and the chapter runs printed pp. 198 to 293. The stage moment is printed p. 258, the frequency-squared opinion p. 213, the vacuum brushes pp. 226 to 228, the energy bookkeeping p. 291"
  - text: "Chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', the Philadelphia and St. Louis lecture of February-March 1892 (printed pp. 294 to 373). The passage on the discharge as a standing energy loss, and the account of what it does to the air of a room, are printed p. 322; the same paragraph credits Professor Crookes on nitrous acid"
  - text: "Chapter XXIX, on the high-frequency alternator, which is the volume editor's text in the third person and not a Tesla paper: it reads 'In one type of machine of this kind constructed by Mr. Tesla'. The 15,000 and 30,000 alternations-per-second figures are quoted from it at printed pp. 376 and 381 and are attributed to the book, not to him. Article 11 in this series is built on the same chapter"
  - text: "The volume's editorial introduction, printed p. 121, which writes about 'Mr. Tesla' in the third person. The phrase 'the true electric flame' quoted here is the editor's, not his"
  - text: "Word search of the text layer of our scan (books/extracted/tesla-1894-plain.txt), whole volume, whole-word matching over the same normalised index books/tools/grep_quote.py builds, re-run at draft time on 2026-10-11: 'cold flame' 0, 'cold fire' 0, 'corona' 0, 'plasma' 0, 'ioniz' 0, 'electron' 0, 'ultraviolet' 0, 'combustion' 0. 'electrode' 131. 'hot brush' 2 (printed pp. 127, 167). 'veritable flame' 3 (printed pp. 120, 166, 167; p. 120 is the editor's introduction). 'true electric flame' 1 (printed p. 121). 'luminous funnel' 1 (printed p. 168). 'ozone' 7 (printed pp. 127, 158, 171, 322, and the index at pp. 495 and 496). 'chemical process' 5 (printed pp. 127, 167, 214, 250, 272). 'cold' 7 (printed pp. 296, 300, 311, 361, 362, 363, 387), and none of those seven is about the brush or the flame: they are the feeling of warmth or cold on skin, air condensed by intense cold, electrodes that may remain quite cold, an outer globe that stays cold while a button inside it is incandescent, a medium that must be dark and cold, and a column of gas between electrodes. 'scorch' 3 (printed pp. 124, 167, 258)"
  - text: "Zobaa A. M., Abdelnabi H. H., Reda R. M. and Mahmoud A. G., 'Quantifying and mitigating electrical and environmental impacts of corona discharge', Scientific Reports 15, 41165 (2025), for the modern account of a corona: the field exceeding the dielectric strength of air at about 30 kV per cm at standard temperature and pressure, ionisation and an electron avalanche, a blue glow with audible noise, power loss and chemically active gas emissions, and corona rings, larger conductors and wider conductor spacing as the standard mitigations"
    url: "https://doi.org/10.1038/s41598-025-24666-1"
  - text: "US Environmental Protection Agency, 'Ozone Generators that are Sold as Air Cleaners', for ozone as a lung irritant (chest pain, coughing, shortness of breath and throat irritation at relatively low concentrations) and for its finding that at concentrations not exceeding public health standards ozone has little potential to remove indoor air contaminants"
    url: "https://www.epa.gov/indoor-air-quality-iaq/ozone-generators-are-sold-air-cleaners"
  - text: "Arizona State University Physics Instructional Resource Team, 'Plasma Globe', for the construction of the modern toy: low-pressure krypton, xenon or neon, an electrode at the centre of the globe, and a high-voltage high-frequency transformer underneath it at a few kilovolts and a frequency in the vicinity of 35 kHz"
    url: "https://physics.asu.edu/plasma-globe"
  - text: "Every quote on this page was re-grepped from the text layer of our scan and pinned to its printed page before drafting. The register is new_content/1894-series/06-tesla-cold-flame/quotes.md, 52 quotes across 18 printed pages with 0 failures, re-runnable with books/tools/grep_quote.py and regenerated by gen_quotes.py in that directory. The draft was re-checked against that register at books/tools/check_quotes.py: 1 file, 0 quote problems"
---

**Standfirst.** Nikola Tesla produced a brush of electric discharge at the end of a wire in front of a lecture audience and asked whether it was any the less a flame because it did not scorch his hand. The 1894 book that reprints that lecture also prints, three separate times, that the same brush is hot. The phrase 'cold flame' is in it zero times, and so is the reason he never built the lamp: he could not make the frequency.

## The stage moment, and the word that is not in the book

Four different texts are quoted on this page and they are not the same paper, so the dates go down first. The stage moment is London. The chapter it comes from carries its own footnote, printed p. 198, which reads "Lecture delivered before the Institution of Electrical Engineers, London, February, 1892." (1894, p. 198) The mechanism passages two sections later are New York, and that chapter's footnote, printed p. 145, reads "A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891." (1894, p. 145) One further text is quoted here, the Philadelphia and St. Louis lecture of February-March 1892, and one is not his writing at all: the chapter on the high-frequency alternator is the volume editor's, about 'Mr. Tesla' in the third person. 1894 is the book. The writing is 1891 and 1892.

Inside the London lecture, the sentence that puts this on a stage is in the present tense about that evening: "In one of the experiments this evening a brush was produced at the end of a wire" (1894, p. 258). Then the move this series' title is built on:

"The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand" (1894, p. 258)

and the same move a second time about light instead of heat: "Is it the less a flame because it does not hurt my eyes by its brilliancy" (1894, p. 258). Both questions are left open here on purpose: this scan prints their question marks as '{' and as ' ?'. The marks sit outside the quotation marks; the words inside them are the print's, including the compositor's space before the semicolon.

Read what he is doing. He is not reporting a measurement and he is not announcing a new substance. He is taking an audience's definition apart in front of them. Cool to the hand and dim to the eye are the two tests by which people decide something is not a flame, so he removes both tests and asks what is left. What is left, he says two sentences later, is a project: "The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful" (1894, p. 258). A lamp. That sentence decides what the rest of this page is about.

Now the word. A whole-word search of the text layer of our scan, whole volume, re-run at draft time on 2026-10-11, returns 0 occurrences of 'cold flame' and 0 of 'cold fire'. So does 'combustion'. The method behind a zero like that one, and the two indexes a count can be taken over, are set out on a standing page of their own: [Tesla 1894 Word Search](tesla-1894-word-search.html), which prints the command it ran and states the rules in full. The book's names for this phenomenon are hotter than ours: 'the hot brush' occurs twice, printed pp. 127 and 167; 'veritable flame' occurs three times, printed pp. 120, 166 and 167; 'luminous funnel' occurs once, printed p. 168; 'scorch' occurs three times, printed pp. 124, 167 and 258, and two of those are in the passages quoted here. The closest the 1894 book comes to naming this a flame is the volume's editorial introduction, which is not his writing, and which classifies the discharge series as "starting from the thread-like discharge and passing through various stages to the true electric flame" (1894, p. 121). That is an editor summarising a colleague's results, and it is not 'cold' either.

'cold' is in the book seven times, at printed pp. 296, 300, 311, 361, 362, 363 and 387: the sensation of warmth or cold on skin, air condensed and solidified by intense cold, electrodes that may remain quite cold, an outer globe that stays cold while a button inside it is incandescent, a medium that must be dark and cold, a column of gas between electrodes. Not one of the seven is about the brush or the flame. The title of this page is ours. The claims are his.
## What a brush actually is

The New York lecture of May 20 1891 is where the phenomenon is described, and it is described as an experiment you have to work at. He replaces the usual terminals of the coil with two metal columns insulated with a good thickness of ebonite, closes the cracks and fissures with wax so the discharge can only form at the tops of the columns, and adjusts the length of the wire until the rise of potential is exactly counteracted by the drop through the coil. Then, in his words:

"one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure" (1894, p. 166)

That sentence ends by pointing at a plate, Fig. 110. The plate is not on that page: it is set on the facing page, printed p. 165, and it is a photograph rather than an engraving, because the art in this part of the volume is photographic, halftone photographs of the coil with the discharge running, retouched to a black ground. The crop below is that plate, cut for this page rather than borrowed from another article, because it is the image the prose argues with.

![1894 photograph, Fig. 110, printed p. 165: an induction coil photographed against a dark ground, the winding shown as a wide stack of many flat turns filling the lower half of the plate, an insulated column standing at either side of it, and from the top of each column a pale discharge rising upward, bright at its root just above the metal and widening into a tufted plume, the two plumes alike in height and shape](/assets/tesla1894/p165-fig110.webp "Fig. 110, printed p. 165, the whole plate with its printed caption inside the crop; the plate to its left on the same page is Fig. 109. The sentence that points at this plate is set on the facing page, printed p. 166. The prose there says what is drawn: the primary coil is placed sideways, the usual terminals of the coil are replaced by a pair of metal columns insulated with a good thickness of ebonite, and when the cracks and fissures are closed with wax 'the brushes cannot form anywhere except at the tops of the columns' (1894, p. 166). Two columns, and a brush at the top of each: that is the arrangement in the photograph. From the Columbia College lecture of May 20 1891. Public domain.")

He will not let the resemblance stand as a simile. The next sentence is a correction: "But they do not only resemble, they are veritable flames, for they are hot" (1894, p. 166). Then the honest scale of what he had: "Certainly they are not as hot as a gas burner, but they would be so if the frequency" (1894, p. 166), and the potential, were high enough. The quote stops where it still verifies; the scan garbles the conjunction in the rest of that clause, and the thought does not need the missing word. He is conceding that his flame is cooler than a gas burner and claiming that the difference is an engineering gap.

His mechanism, in one of his own sentences: "The heat developed is, of course, due to the impact of the air molecules against the terminals and against each other" (1894, p. 166). That is a bombardment theory of a cool flame, and it predicts the very contradiction a reader would trip over. A brush can feel cool and be genuinely hot at the same time, because the heating is local, thin, and carried away fast: "In the positive brush of a static machine the exchange of the molecules is very rapid, the stream is constantly of one direction, and there are fewer collisions ; hence the heating effect must be very small" (1894, p. 167). Then the rule, stated as a rule: "Anything that impairs the facility of exchange tends to increase the local heat produced" (1894, p. 167).

And then the demonstration that ends the word 'cold' as an adjective. He holds a glass tube over the brush so the draught carries the brush up the tube: "If a glass tube be held over the brush so as to allow the draught to carry the brush upwards, scorching hot air escapes at the top of the tube" (1894, p. 167). 'Scorching' is his word, one of three in the volume. So is the sentence that follows it, which is also the practical consequence he draws: "Anything held within the brush is, of course, rapidly heated, and the possibility of using such heating effects for some purpose or other suggests itself" (1894, p. 167). 'Suggests itself' is the hedge, and it is doing the hedging.

In the vocabulary we use now, this is a corona discharge, and none of that vocabulary is in this book: 'corona' 0 occurrences, 'plasma' 0, 'ioniz' 0, 'electron' 0, which returns only fuzzy hits for 'electrode', and 'ultraviolet' 0. The modern account is ours and carries no page cite, and it comes from the 2025 measurement paper in the sources below: where the field at a conductor exceeds the dielectric strength of air, about 30 kV per cm at standard temperature and pressure, the gas ionises, an electron avalanche follows, and the glow is photon emission from that gas, with audible noise, real power loss and chemically active gas as by-products. His word is 'the brush' and his explanation is molecular bombardment. Both descriptions are of the same thing: a thin, cool-to-the-hand, genuinely hot, genuinely lossy glow at the surface of a high-voltage conductor. Neither one of them is a fire that consumes fuel, and that is exactly the distinction he goes on to make.
## The bigger idea: light and heat with no chemical process

This is the part of the argument that gives this page its title, and it is not a claim about free energy. He looks at the hot brush and reasons backwards from it to ordinary fire: "When contemplating this singular phenomenon of the hot brush, we cannot help being convinced that a similar process must take place in the ordinary flame" (1894, p. 167). The phrase inside that sentence, 'the hot brush', is one of the two occurrences in the volume.

The claim proper, in one sentence, in full:

"we have a possible way of producing - by other than chemical means - a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods of producing enormous frequencies and potentials" (1894, p. 167)

The dashes around 'by other than chemical means' are the printer's em dashes set here as ordinary hyphens, because this site's voice rule forbids typographic dashes in an article body. The words and their order are the print's, and the sentence is longer than the one usually quoted from this lecture, which drops 'we have a possible way of producing' and 'and to accomplish this'.

Read the grammar, because that is where the honesty is. 'A possible way of producing'. 'We only need to perfect methods'. He is not announcing a cold flame; he is naming a research program and locating the difficulty in the apparatus. The condition is stated again in the next sentence, and stated as a condition: "I have no doubt that if the potential could be made to alternate with sufficient rapidity and power, the brush formed at the end of a wire would lose its electrical characteristics and would become flamelike" (1894, p. 167). Then the theory in six words: "The flame must be due to electrostatic molecular action" (1894, p. 167).

He draws a consequence at once, and it is a storm accident: "It is well known that objects are often set on fire without the lightning striking them" (1894, p. 167). His explanation is the brush, at scale. On a nail in a roof, or on any more or less conducting projection rendered conducting by damp, a powerful brush may appear, and near it the enormous potential may be made to fluctuate, in his words, "perhaps many million times a second" (1894, p. 168), so that "the air molecules are violently attracted and repelled, and by their impact produce such a powerful heating effect" (1894, p. 168) that a fire starts. Then the sentence he leaves standing, hedged only by its own opening: "It is conceivable that a ship at sea may, in this manner, catch fire at many points at once" (1894, p. 168).

'It is conceivable' is doing the work. It is the same construction this site looked at on [Tesla's high-frequency massage cure of 1891](tesla-high-frequency-massage.html), where he carries a heating apparatus out to a nude man standing comfortably warm at the North Pole and stops there. It is the mark of a writer following an idea to a consequence rather than selling one.

The step from a brush to a lamp is one move, and he takes it on the next printed page. Prevent the air exchanging and the local heating rises: "the local heating effect may be so exalted as to bring a body to incandescence" (1894, p. 168). A small button, or better a very thin filament, sealed in a partly exhausted globe and connected to the terminal of the coil, may be rendered incandescent, and it does more than glow:

![1894 photograph, Fig. 111, printed p. 168: the same kind of coil, its winding a stack of many flat turns along the bottom of the plate and an insulated column at either side; standing on the top of the right-hand column is a bright pear-shaped glow, broad and rounded at the top and narrowing to a thin bright stem that runs down to the terminal, with a short ribbed section and a small dark fitting above it; the column at the left is capped by a small bright discharge](/assets/tesla1894/p168-fig111.webp "Fig. 111, printed p. 168, the whole plate with its printed caption inside the crop. The text on this page numbers the plate and names the shape: a small button, or preferably a very thin wire or filament, enclosed in an unexhausted globe and connected with the terminal of the coil 'may be rendered incandescent', and the phenomenon is made more interesting by 'the rapid spinning round in a circle of the top of the filament, thus presenting the appearance of a luminous funnel' (1894, p. 168). The printed line on that page goes on, 'Fig. 111, which widens when the potential is increased', read off the print at 500 ppi because the OCR gives it as 'Fig. Ill'. The bright pear standing on the terminal of the right-hand column is that funnel. This is the step from a brush to a lamp, and it is why the argument of this page ends at a bulb. Public domain.")

The prose beside that plate describes the top of the filament spinning in a circle and calls the shape a luminous funnel, one occurrence of that phrase in the whole volume, printed p. 168. It is a brush with a lamp inside it, and it is as close as he gets to the thing he says he wants.
## Why he never got it: the frequency was not there

He says why himself, more than once, in plain words, and the reason is a number.

Start with the number he had. In the same paragraph as 'veritable flames, for they are hot': "Produced with, say, twenty thousand alternations per second, the heat is easily perceptible even if the potential is not excessively high" (1894, p. 166). Now the number the explanation needs: "perhaps many million times a second" (1894, p. 168). That is the gap, printed two pages apart in one lecture, and it is a factor of a hundred or more.

He had an argument for why the gap might be crossable, and it is a scaling argument rather than a wish. The molecules near a terminal do not get away from it: "The higher the frequency, the less the molecule is able to get away, and this the more so, as for a given effect the potential required is smaller" (1894, p. 166). The sentence runs across the folio and finishes on the next printed page: "which practically the same molecules would strike the terminal" (1894, p. 167). Strike the same molecules again and again and the heat at and near the terminal is 'excessive'. He then says the heat would begin to fall off again at still higher frequency, for reasons he calls obvious, which is what a working experimenter says about something he has not measured.

In the London lecture he puts the scaling as a law: "the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential" (1894, p. 213). If heat and light go as frequency times the square of the potential, then 'enormous frequencies and potentials' is not a flourish, it is the entire difficulty, quantitatively. And he hedges his own law in the next sentence: "the experimental verification of the law, whatever it may be, would be exceedingly difficult" (1894, p. 213). 'Whatever it may be' is him declining to promise that the law is the one he just wrote.

What he actually had, stated as a premise for an inference rather than as a measurement: "with potentials of no more than one or two hundred thousand volts, the heating effects are considerable" (1894, p. 168), and therefore, in his own phrase, "we may imagine how much more powerful they must be with frequencies and potentials many times greater" (1894, p. 168). 'We may imagine' is his marker for the step he did not take. He stakes a priority claim in the same paragraph, and the sentence is a hedge about evidence rather than a boast: "I am not aware that, up to the present ... the heating effects of a brush produced by a rapidly alternating potential ... have been experimentally demonstrated, at least not to such a remarkable degree" (1894, p. 168). The cuts in the middle of that quote are where the printed page inserts a figure caption between the halves of the sentence; each piece is quoted as it stands.

Then the apparatus, which is where the claim actually dies. Off-the-shelf equipment of 1891 could not do this: "In employing a commercial coil, the production of very powerful brush effects is attended with considerable difficulties" (1894, p. 169), and the failure mode is named: "when these high frequencies and enormous potentials are used, the best insulation is apt to give way" (1894, p. 169). The lamp idea is written up in the same mood it was proposed in: "The possibility of bringing a body to incandescence in an exhausted globe, or even when not at all enclosed, would seem to afford a possible way of obtaining light ... might be rendered available for useful purposes" (1894, p. 169). 'Would seem to afford a possible way'.

The frequency he could actually build is in the same book, in the chapter on his high-frequency alternators, and it is not his writing. That chapter describes his machines in the third person, 'In one type of machine of this kind constructed by Mr. Tesla'. The ceiling it gives for the simpler design is the book's sentence, not his: "Up to about 15,000 alternations per second in an experimental machine, the former plan may be followed, but a more efficient machine is obtained on the second plan" (1894, p. 376). The better machine is the book's description as well: "the field had 480 polar projections on each side, and from this machine it was possible to obtain 30,000 alternations per second" (1894, p. 381). Fifteen thousand, thirty thousand, against the many million the flame needs. Those machines, their pole counts, and why building one was 'a tale of woe' in that chapter's own phrase, are the subject of [Tesla's high-frequency alternator](tesla-high-frequency-alternator.html).

The glass bulb is the part a reader is most likely to mistake for the design. It is not the design, it is a substitute for a machine: "Were there means at hand for producing electric impulses of a sufficiently high frequency, and for transmitting them, the bulb could be done away with" (1894, p. 258). Then the admission, on the next printed page: "But as such means are not at disposal, it becomes necessary to place the terminal in the bulb and rarefy the air in the same" (1894, p. 259). Then the plainest sentence in the whole argument: "This is done merely to enable the apparatus to perform the work which it is not capable of performing at ordinary air pressure" (1894, p. 259). The envelope stands in for the alternator. The same substitution runs through the lamps he held up in 1891, and [Tesla lit lamps by holding them](tesla-lit-lamps-without-wires.html) works through that apparatus story in full, including the part about what the glass and the room each have to do for a circuit that looks incomplete. The other half of that story, the exhausted tube that lights in the hand and keeps the habit of lighting after it is put away, is on its own page at [Glowing Glass in Tesla's Bare Hand](tesla-glowing-tubes-vacuum.html), and it is the same book's material, printed p. 288.

One safety note, and its basis is his rather than ours. The voltages in these experiments are 'one or two hundred thousand volts' (1894, p. 168), the air coming off the brush is 'scorching' (1894, p. 167), and the chemistry of a working coil fills a room (1894, p. 171). The caution about taking such currents directly from a machine or from a secondary of low resistance, especially with condensers, is on the massage page linked above. Nobody should read this article as an invitation to repeat any of it at home.
## What the internet gets wrong

**That the 'cold fire' in a modern video contradicts combustion physics.** It does not contradict anything, because it is not combustion. What is usually filmed is a corona or a low-pressure gas discharge, and a corona is a loss with a glow attached: ionisation and an electron avalanche at the surface of a conductor, a blue glow, audible noise, power leaving the circuit, chemically active gas given off. Tesla's own bookkeeping is identical, and he wrote it as an obstacle rather than a wonder: "It would, of course, be out of question to transmit such impulses through a wire immersed in a gaseous medium, even if the wire were provided with a thick and excellent insulation, for most of the energy would be lost in molecular bombardment and consequent heating" (1894, p. 291). 'Out of question' is the print's phrasing, not a slip of ours; the modern idiom would fail the verbatim check. From the Philadelphia and St. Louis lecture, the same point in six words: "they always exist, consuming energy and modifying the action of the apparatus" (1894, p. 322). A brush is not something for nothing. It is a bill you can see.

**That 'a flame without a chemical process' is a free-energy claim.** It is a lighting claim, and the lecture it comes from says what for: a lamp whose flame is smaller than the one on the stage but incomparably more powerful (1894, p. 258). The sentence quoted above is about the source of the light and heat, not about getting energy out of nowhere: no material consumed, no chemical process, and the stated price is enormous frequencies and enormous potentials (1894, p. 167). He did make a large economy claim about electric lighting in that same London lecture, a multiple of what an incandescent lamp gives for the same expenditure, and this page does not quote it, because a number like that is worth nothing without the argument attached to it and that argument belongs to a different article.

**That the naming is his.** The 1894 volume has names for this phenomenon and every one of them points the other way. The biggest brush in the New York lecture, several inches long, produced by running an iron core up into the secondary, is introduced as "an excessively powerful brush, several inches long, which may be appropriately called" (1894, p. 171) St. Elmo's hot fire. That is the book's name, set off in its own quotation marks on the printed page, and it is the opposite of the word in this article's title. The editor of the 1894 volume, writing about 'Mr. Tesla' in the third person in the introduction, describes the same family of effects as ending in "the true electric flame" (1894, p. 121) - the phrase is the editor's, and it is not 'cold' either. The modern words are absent: 'corona' 0, 'plasma' 0, 'ioniz' 0, 'electron' 0, 'ultraviolet' 0.

**That he got it to work.** He reports no cold-flame lamp and no measured gain from one. What he reports is a set of conditions: 'if the potential could be made to alternate with sufficient rapidity and power' (1894, p. 167), 'we may imagine how much more powerful they must be' (1894, p. 168), 'would seem to afford a possible way' (1894, p. 169), 'But as such means are not at disposal' (1894, p. 259). Those are not four hedges around one result. They are the result: a program, a mechanism, a scaling argument, and an admission that the machinery did not exist.

## Where you see it now

**On the transmission grid.** Corona on conductors is the ordinary, expensive, well-documented descendant of what he was playing with: audible noise, real power loss, chemically active gas given off, and the standard fixes are corona rings on the hardware, larger conductors, and wider spacing between them. The 2025 study cited below quantifies the electrical and environmental effects of that corona and names those same mitigations. Tesla's own version of the mitigation is an electrostatic screen, and he is precise about why the naive version of a screen fails: put a conducting coating on the insulation and earth it, and 'all the energy would pass through the conducting coating to the ground and nothing would get to the end of the wire' (1894, p. 291).

**In an ozone generator.** He says so, and he says why it is a frequency machine: "For the production of ozone, alternating currents of very high frequency are eminently suited" (1894, p. 171), because "the ozonizing action of a discharge is dependent on the frequency as well as on the potential" (1894, p. 171). His own apparatus was an ozone generator whether or not anyone sold it as one: "It is a most powerful ozonizer, so powerful indeed, that only a few minutes are sufficient to fill the whole room with the smell of ozone" (1894, p. 171). The Philadelphia and St. Louis lecture gives the same effect as a working hazard: "if a coil, such as this one, is worked for a very long time it will make the atmosphere of a small room unbearable, for the eyes and throat are attacked" (1894, p. 322). That is the honest half of the modern ozone story. The other half is the regulator's: the US EPA, which is the source for the health point here, records ozone as a lung irritant that can cause chest pain, coughing, shortness of breath and throat irritation at relatively low concentrations, and finds that at concentrations not exceeding public health standards ozone has little potential to remove indoor air contaminants. The device is real. The air-purifier claim usually is not.

**In a plasma globe on a desk.** He describes that globe, and he describes the demonstration exactly as it is still done: "it is a brush, formed at, or near, a single terminal in high vacuum" (1894, p. 226), and to excite one, "it is usually sufficient to grasp the globe L with the hand" (1894, p. 228). He even records the behaviour every owner notices, that the discharge follows the person in the room: "the approach of the observer at a few paces from the bulb will cause the brush to fly to the opposite side, and if he walks around the bulb it will always keep on the opposite side" (1894, p. 228). The same passage describes the sensitive bulb being slowed or sped up by a magnet held some way off, which is the only reason a magnet has any business on a page about a flame.

![1894 drawing printed in reverse, bright lines on a dark ground, Fig. 141, printed p. 226: a large pear-shaped lamp globe, and sealed into its neck a long narrow tube with thick walls shown in section by diagonal hatching, running down through the neck into a bulbous chamber at the lower end that is filled with a hatched pool; the top of that tube is blown out into a small sphere centred inside the large globe, and that small sphere is filled with a stippled mass; a thin rod runs down the bore of the tube, ends in a bright point just above the pool, and continues out of the chamber and down to a small ring](/assets/tesla1894/p226-fig141.webp "Fig. 141, printed p. 226, the whole plate with its printed caption inside the crop; the plate beside it on the same page is Fig. 142. The book describes this bulb on the same printed page: 'In Fig. 141 the bulb comprises an incandescent lamp globe ... in the neck of which is sealed a barometer tube ... the end of which is blown out to form a small sphere' (1894, p. 226). The drawing matches that description part for part: the small sphere is blown at the end of the long tube and set in the middle of the large globe, as the text on that page requires it to be, and it is filled with a stippled mass of conducting powder, which the following page says is led to the generator. No wire enters through the glass, which is also what that page advises. This is the apparatus behind the passage quoted above, a brush 'formed at, or near, a single terminal in high vacuum' (1894, p. 226), and the ancestor of the desk globe. Public domain.")

The bulbs in that chapter are the ancestor of the toy, and the book's own description of its plates is one line long: "Figs. 143, 144 and 145 indicate different forms, or stages, of the brush" (1894, p. 227). The modern toy, per the Arizona State University physics group cited below, is a low-pressure gas globe, usually krypton, xenon or neon, with an electrode at the centre driven from underneath by a high-voltage high-frequency transformer running at a few kilovolts and a frequency in the vicinity of 35 kHz. A few tens of kilohertz, a few kilovolts, and a hand on the glass. He asked for many million alternations a second and one or two hundred thousand volts, and he could not get them, so he put the terminal in a bulb and rarefied the air. A desk toy is what you get when you do that and then forget why: he needed many million alternations a second, and the potentials he was working with, 'one or two hundred thousand volts' (1894, p. 168), gave heating he called considerable and a flame he did not have.

This site's beginner page on magnetic fields and on generating current with magnets is [7 interesting facts about magnets](7-interesting-facts-about-magnets.html); the discharge itself is not on it, and the connection between the two is the one this section just drew, a high-voltage source and a gas that gives way.

The test this series applies to every claim is the one Tesla applied to his own apparatus first: what is the source, what does it actually put out, and where is the sentence in which the writer states the condition under which his claim holds. For the cold flame, that sentence is already on this page, and it is not a flourish. It is 'But as such means are not at disposal' (1894, p. 259). The idea was a physical program with a mechanism, a scaling argument and a route to a lamp. The frequency was not there, so the flame stayed a demonstration, and the phrase that sells it now, 'cold flame', is one nobody in that book ever wrote.

{{FAQ}}

{{CTA}}

{{SOURCES}}
