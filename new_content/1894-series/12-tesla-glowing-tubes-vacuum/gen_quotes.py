#!/usr/bin/env python3
"""Regenerate quotes.md for article 12 (feature-006/t9).

Run: python3 new_content/1894-series/12-tesla-glowing-tubes-vacuum/gen_quotes.py

Every entry is re-grepped at generation time through the same matcher
books/tools/check_quotes.py uses; if a quote does not verify on its stated
printed page the script fails and leaves the file as a partial pin
(SERIES-PLAN-1894.md section 8 step 2, section 0 non-negotiable 2). The draft
is written from this file, not from memory, and a quote that is not here does
not go in the draft.

Article 12 is `tesla-glowing-tubes-vacuum.html`, SERIES-PLAN-1894.md section 9
brief 12. Its evidence sits in three places in the volume, and the brief mixes
them without saying so:

  * chapter XXXII, printed pp. 396-406 - the only chapter in the book about
    exciting a tube with no wires in it, and the one chapter in the whole volume
    that carries FOUR different texts by FOUR different people in nine pages.
    Two are Tesla's own magazine articles, dated in the page footnotes to
    July 1 and August 26, 1891. One is an abstract of a paper by Prof. J. J.
    Thomson, and one is a published note by the same man answering Tesla. The
    brief's item 2 ('the tube is one plate of a capacitor') and item 5 ('the
    energy is capacitively coupled from the coil') are chapter XXXII's subject,
    and the four figures the brief shortlists (Figs. 210, 212, 215, 218) are
    all inside it.
  * chapter XXVII, printed pp. 198-293 - the London lecture of February 1892,
    Tesla speaking in the first person on a stage. Both of the brief's p. 288
    beats are here, and so is the carborundum and diamond-dust passage at
    printed p. 255 that brief 12 item 3 asks for.
  * chapter XXVI, printed pp. 145-197 - the New York lecture of May 20, 1891,
    where the same argument appears a year and a half earlier, in the same
    first person, including the one sentence in the book that says a tube is
    lit BY condenser action (printed p. 186).

A quote pinned here may contain " ..." where the printed text is cut by a
figure label, a footnote or a page break. Each fragment between the cuts is
verified separately against the one page the quote is pinned to, which is
exactly how check_quotes.py will judge the draft in feature-006/t7 - this
script does not reimplement that check, it imports it (check_quotes.fragments +
check_quotes.locate over the index check_quotes builds). If a quote passes here
it passes there.

Two things this pin MEASURES rather than types, because for THIS article they
are evidence and not commentary:

  * the vocabulary table. The article's own subject is named in modern words -
    'vacuum tube', 'capacitor', 'Geissler tube', 'X-rays' - and the book uses
    some of them and none of the others. The counts are computed here, three
    ways, with the printed pages each hit sits on, and the scoped counts show
    what chapter XXXII never reports.
  * the scoped absences in chapter XXXII and in the lamp passage at printed
    pp. 253-259: no test, no efficiency, no per cent, no watt, no candlepower,
    no commercial figure. Brief 12 item 5 says the internet gets this wrong;
    the absence is the measurement that lets the article say so.

A note on the two index files this script does NOT use: books/extracted/
quote-index.md section B and section L already carried two of brief 12's hooks
(the p. 288 showmanship sentence and the p. 255 carborundum sentence) from the
first pass of this project. Both were re-grepped here from the OCR text, and
the p. 288 one is quoted by article 01's live page already, which is why it is
in REJECTED and not in QUOTES. Nothing in this file is carried forward from
quote-index.md on trust.
"""
import csv
import html
import re
import sys
from pathlib import Path

TOOLS = Path("/home/matt/projects/other/tesla-generator/books/tools")
sys.path.insert(0, str(TOOLS))
import check_quotes as CQ  # noqa: E402
import grep_quote as gq  # noqa: E402

ROOT = Path("/home/matt/projects/other/tesla-generator")
TXT = TOOLS.parent / "extracted" / "tesla-1894-plain.txt"
OUT = Path("/home/matt/projects/other/tesla-generator/new_content/1894-series/"
           "12-tesla-glowing-tubes-vacuum/quotes.md")

PIN_DATE = "2026-10-18"

# Chapter extents, printed pages, from the volume's own running structure.
CH32 = (396, 406)      # ch. XXXII, Electric discharge in vacuum tubes
CH27 = (198, 293)      # ch. XXVII, the London lecture, Feb 1892
CH26 = (145, 197)      # ch. XXVI, the New York lecture, May 20 1891
LAMPS = (253, 259)     # the carborundum / button-lamp passage inside ch. XXVII

# ---------------------------------------------------------------------------
# The pin. (quote, printed page, section label, why the draft may want it)
# ---------------------------------------------------------------------------
QUOTES = [
    # ---- 0. Provenance: which text, whose voice, what date. Chapter XXXII is
    # four texts in nine pages and the footnotes on the pages say so. Read
    # FOUR TEXTS, FOUR VOICES, ONE CHAPTER before writing any sentence that
    # begins 'Tesla wrote'.
    ("Article by Mr. Tesla in The Electrical Engineer. N. Y., July 1, 1891.",
     396, "0. Provenance (ch. XXXII footnote 1, the date of the chapter's main text)",
     "the footnote that dates the whole first part of chapter XXXII: Tesla's own "
     "article, published July 1, 1891, six months before the London lecture the "
     "brief's p. 288 quote comes from. This is the earliest first-person account "
     "in the volume of lighting a tube with no wires in it, and the only one "
     "devoted to it. The print sets a period after 'Engineer' and after 'Y'; "
     "quote it as set"),

    ("My investigations in this line occupied me principally during the winter "
     "and spring of the past year",
     396, "0. Provenance (ch. XXXII, the date of the work itself)",
     "the article's own date for the bench work: the winter and spring before "
     "July 1891, so spring 1891 at the latest. It is the only date for the work "
     "in this chapter, and it is earlier than the May 20, 1891 New York lecture "
     "the same volume prints as chapter XXVI, which makes the priority question "
     "in the chapter a question about who published first, not who thought first. "
     "Say 'he says' - the sentence is his, the date inside it is relative to the "
     "footnote above it"),

    ("In The Electrical Engineer of June 10 I have noted the description of "
     "some experiments of Prof. J. J. Thomson, on the",
     396, "0. Provenance (ch. XXXII opening, the occasion of the article)",
     "the sentence that starts the chapter, and the reason it exists: a trade "
     "paper reported J. J. Thomson's experiments and Tesla wrote in about them. "
     "The quoted title that follows is in the print's own quote marks, which "
     "would split the run in check_quotes.py's scanner, so the quote stops at "
     "'on the'. See the flag THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME "
     "WORDS ARE"),

    ("in your issue of June 24 Prof. Elihu Thomson describes an experiment of "
     "the same kind",
     396, "0. Provenance (ch. XXXII opening, the second Thomson)",
     "the trap in this chapter's prose: 'Prof. Thomson' unqualified is J. J., "
     "and Elihu Thomson is a different man, a different experiment, in the same "
     "issue run. The chapter names both within two sentences. Any draft sentence "
     "about 'Thomson' has to say which one. Read the flag TWO THOMSONS IN ONE "
     "PARAGRAPH"),

    ("The fundamental idea in these experiments is to set up an electromotive "
     "force in a vacuum tube - preferably devoid of any electrodes - by means "
     "of electro-magnetic induction, and to excite the tube in this manner",
     396, "2. Why a tube lights with no wires (the definition of the thing)",
     "the one sentence in the volume that defines the whole subject in the "
     "article's own terms: an EMF set up inside a tube with no electrodes in it. "
     "Brief 12 item 2 asks what is happening in a tube with no wires; this is "
     "the 1891 description of the setup. The print's dashes around 'preferably "
     "devoid of any electrodes' are em dashes; the form above uses the ASCII "
     "form the normaliser folds, and the draft must print commas or brackets, "
     "not dashes (section 0 non-negotiable 5)"),

    ("the idea of replacing the tinfoil coatings of a Leyden jar by rarefied "
     "gas and exciting luminosity in the condenser thus obtained by repeatedly "
     "charging and discharging it",
     396, "2. Why a tube lights with no wires (the tube as a condenser, in his words)",
     "the closest thing in the book to brief 12 item 2's 'the tube is one plate "
     "of a capacitor', and it is his own analogy, not ours: the gas replaces the "
     "two coatings of a Leyden jar, so the jar and the tube are the same "
     "component. It is inside a sentence about how obvious the idea seemed, so "
     "quote it with the sentence's point (see the next row). The book's word is "
     "'condenser'; 'capacitor' is 0 in the volume, table below"),

    ("The idea being obvious, whatever merit there is in this line of "
     "investigation must depend upon the completeness of the study of the "
     "subject and the correctness of the observations",
     396, "0. Provenance (ch. XXXII, his own standard for priority)",
     "the sentence that governs how this article should talk about priority at "
     "all. He concedes the idea was obvious and puts the merit on completeness "
     "and correctness of observation. That is the standard the article can hold "
     "its own claims to, and it is a quote, not a paraphrase of his character"),

    ("The following lines are not penned with any desire on my part to put "
     "myself on record as one who has performed similar experiments, but with a "
     "desire to assist other experimenters by pointing out certain "
     "peculiarities of the phenomena observed",
     396, "0. Provenance (ch. XXXII, what he says the article is for)",
     "the disclaimant he opens with, and it is the opposite of the claim the "
     "myth needs: he is not claiming the discovery, he is claiming observations "
     "the other man had not noted. Pair it with the p. 404 row where he says he "
     "was misread. Note the print's 'I should, think' stray comma in the "
     "sentence before this one - see Rejected #3"),

    ("I should, think that to any experimenter who had carefully studied the "
     "problem confronting us and who attempted to find a solution of it, this "
     "idea must present itself as naturally as",
     396, "0. Provenance (ch. XXXII, the obvious-idea sentence in full)",
     "the first half of the obviousness claim, with the print's stray comma "
     "after 'should' inside it. Quote it as set or not at all; a cleaned form "
     "does not verify. The sentence runs on into the Leyden-jar comparison, so "
     "the two rows above and this one are one paragraph in three pieces"),

    ("Electric Discharges in Vacuum Tubes",
     494, "0. Provenance (the volume's own index entry for the chapter)",
     "the book's own label for the subject, from its index, printed p. 494, and "
     "the string the draft should use if it names the chapter at all. The index "
     "sets the page number '396' on its own OCR line, which strip_furniture "
     "drops as a bare folio, so 'Electric Discharges in Vacuum Tubes 396' does "
     "NOT verify on the default index (it comes back fuzzy 0.828) and does with "
     "--keep-furniture. Quote the label without the number, or say which index "
     "you used. The chapter's display heading is a different matter - see the "
     "flag THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE"),

    ("Carborundum Button for Tesla Lamps",
     494, "3. Tesla's lamp research (the volume's own index label for p. 253)",
     "the index entry for the lamp passage, printed p. 494, and it names the "
     "thing in the book's own words: a carborundum BUTTON for Tesla lamps, at "
     "printed pp. 140 and 253. Useful if the draft wants to show the volume "
     "itself filed this under lamps and not under lighting theory. The index "
     "sets 'Lamps' and '140, 253' on their own OCR lines; the joined string "
     "verifies because '140, 253' is not a bare folio and so is not stripped"),

    ("High Potential, High Frequency : Brush Phenomena in High Vacuum",
     494, "0. Provenance (the index entry for the brush chapter, article 06's)",
     "the index entry that shows how the volume files the other high-vacuum "
     "light effect: 'Brush Phenomena in High Vacuum' at printed p. 226, which "
     "is chapter XXVII's own section and article 06's page. The two index "
     "labels - 'Electric Discharges in Vacuum Tubes' and 'Brush Phenomena in "
     "High Vacuum' - are the book's own distinction between the two things this "
     "series splits across two articles. Use it to keep 06 and 12 apart"),

    ("Lecture delivered before the Institution of Electrical Engineers, London, "
     "February, 1892.",
     198, "0. Provenance (ch. XXVII footnote, the date of the lecture)",
     "dates the chapter that carries the p. 288 tube demo, the p. 255 "
     "carborundum passage, the p. 289 field experiments, the p. 290 Crookes "
     "bulbs and the p. 292 closing statement. Every 'Tesla said in 1892' in this "
     "article needs this footnote, not memory. Article 06's pin carries the same "
     "footnote for the same reason; the two pages must not date the same "
     "lecture differently"),

    ("A lecture delivered before the American Institute of Electrical "
     "Engineers, at Columbia College, N. Y., May 20, 1891.",
     145, "0. Provenance (ch. XXVI footnote, the date of the New York lecture)",
     "dates the chapter that carries the p. 186 condenser-action sentence and "
     "the p. 175 'trillions of invisible hammers' passage. Three dates, three "
     "texts, one article: May 1891, July 1891, February 1892. If the draft "
     "attaches a year to a quote it has to be this one or that one, and the "
     "p. 175 and p. 186 sentences are May 1891, not 1892. Read the flag FOUR "
     "TEXTS, FOUR VOICES, ONE CHAPTER"),

    ("The present volume deals simply with his work accomplished to date",
     6, "0. Provenance (ch. I, the editor's date fence)",
     "the editor's own limit on the whole volume, and the sentence that settles "
     "brief 12's X-ray warning for good: nothing in this book was written after "
     "1894 and the copyright leaf is 1893, so the volume cannot mention a "
     "discovery made in December 1895. Article 10 and article 08 both pin this "
     "line; the three pages must use it the same way (a date fence, not a "
     "comment on Tesla's foresight)"),

    ("It is needless to say that at this moment Mr. Tesla is engaged on a "
     "number of interesting ideas and inventions, tobe made public in due "
     "course",
     6, "0. Provenance (ch. I, the editor on what is NOT in the volume)",
     "the other half of the date fence, and the reason the absence of X-rays is "
     "not a finding about Tesla: the compiler says work in progress is held back. "
     "The OCR glues 'tobe'; the print has the space, so this verifies only "
     "through the space-ignoring index and the draft prints the clean form. "
     "Article 08's pin carries the same sentence with the same annotation"),

    ("new forms of incandescent lamps",
     6, "3. Tesla's lamp research (the editor's inventory lists lamps)",
     "the editor's own inventory of the volume puts 'new forms of incandescent "
     "lamps' in the Miscellaneous section, printed p. 6. It is the sentence that "
     "licenses brief 12 item 3 as part of this book's subject matter rather than "
     "a digression. Article 08's pin quotes the same inventory at greater length "
     "for its own list; take only these five words here"),

    # ---- 1. The strangest demo. Printed p. 288, the London lecture, first
    # person, present tense. Brief 12 item 1.
    ("I take a tube in my hand and move it about, and it is lighted wherever I "
     "may hold it; throughout space the invisible forces act",
     288, "1. The strangest demo (the sentence the article opens on)",
     "brief 12 item 1's hook, verbatim, and the only sentence of the four the "
     "brief quotes from p. 288 that article 01's live page does NOT already "
     "print. Present tense on a stage, first person, no apparatus named. Note "
     "the semicolon: the print runs the two clauses as one sentence, and the "
     "draft's voice rule forbids dashes, so keep the semicolon or split the "
     "sentence and cite both halves"),

    ("But I may take another tube and it might not light, the vacuum being very "
     "high",
     288, "4. The vacuum problem (the second tube, on the same table)",
     "brief 12 item 4's evidence, and it is the same paragraph as the hook: the "
     "demo that fails, on the same page, in the same breath. Article 01's page "
     "PARAPHRASES this ('A tube with too high a vacuum will not light in the "
     "electrostatic field until it has been excited by a disruptive discharge "
     "coil') and quotes the next sentence but one; the verbatim wording is free "
     "here. The comma before 'the vacuum being very high' is the print's causal "
     "clause - it is the explanation, not an aside"),

    ("I excite it by means of a disruptive discharge coil, and now it will "
     "light in the electrostatic field",
     288, "4. The vacuum problem (what fixes it, in his words)",
     "the action that changes the tube from dark to lit. The phrase 'excite it "
     "by means of a disruptive discharge coil' returns @@excite_coil@@ hit in "
     "this text (measured), which is as near to a named procedure as the volume "
     "gets. 'Excited' is "
     "the book's technical word throughout chapter XXXII too, so this sentence "
     "and the p. 396 definition use the same verb; the draft can build on that "
     "consistency instead of inventing one"),

    ("I may put it away for a few weeks or months, still it retains the faculty "
     "of being excited",
     288, "4. The vacuum problem (the persistence)",
     "the part of the demo that is actually strange, and the sentence article 01 "
     "already prints with a page cite. It is pinned here because brief 12 item 1 "
     "quotes it in the plan, and because the article cannot answer 'what changed' "
     "without it. The draft must NOT re-quote it as if it were new: cite it as "
     "the same passage article 01 has, or link to that page. Read the flag "
     "ARTICLE 01 OWNS THE p. 288 SENTENCES IT HAS ALREADY PRINTED"),

    ("What change have I produced in the tube in the act of exciting it?",
     288, "1. The strangest demo (the question he leaves open)",
     "the question he asks his own audience and does not answer. It is the "
     "hinge of brief 12 item 5: the honest article does not answer it either, it "
     "reports that it was asked in 1892 and answers it differently now. Article "
     "01's page ends its p. 288 quote at this question mark, so the answer half "
     "below is the part that has not been used"),

    ("If a motion imparted to atoms, it is difficult to perceive how it can "
     "persist so long without being arrested by f rictional losses",
     288, "5. What the internet gets wrong (his first hypothesis, and his reason for doubting it)",
     "the first of the two explanations he weighs, and his reason for doubting "
     "it: frictional losses. The OCR breaks 'frictional' as 'f rictional' with a "
     "space after the f, which is a scan artefact of the line break, so the "
     "quote carries it and the draft prints 'frictional' - this verifies through "
     "the space-ignoring index only, and check_quotes.py flags it the same way. "
     "The sentence is ungrammatical as printed ('If a motion imparted to atoms') "
     "because the print continues from the previous clause; see the raw window"),

    ("if a strain exerted in the dielectric, such as a simple electrification "
     "would produce, it is easy to see how it may persist indefinitely, but "
     "very difficult to understand why such a condition should aid the "
     "excitation when we have to deal with potentials which are rapidly "
     "alternating",
     288, "5. What the internet gets wrong (his second hypothesis, and the part that still fits)",
     "the second explanation, and the one that survives: a strain in the "
     "dielectric, i.e. charge, persists indefinitely. He rejects it only because "
     "of the alternating potentials, which is exactly the part a modern reader "
     "can resolve (the excitation is not the stored charge). This is the single "
     "best quote for brief 12 item 5's 'a charge/ionisation state, not stored "
     "free power', because it is him reasoning toward it and stopping one step "
     "short for a reason we now know is fixable"),

    ("Since I have exhibited these phenomena for the first time, I have "
     "obtained some other interesting effects",
     289, "1. The strangest demo (what he did after the applause)",
     "the sentence that turns the demo into a program: the next paragraph is the "
     "work, not the show. It dates the field-incandescence results as after his "
     "first exhibition of these effects, which is the London lecture of February "
     "1892 itself - so 'since I have exhibited' means within weeks of the "
     "lecture. Useful for the article's second act without inventing a timeline"),

    ("These coatings are merely used to enable me to perform two experiments "
     "with the tube - namely, to produce the effect desired either by direct "
     "connection of the body of the experimenter or of another body to the "
     "wire w, or by acting inductively through the glass",
     289, "2. Why a tube lights with no wires (the two ways, in one sentence)",
     "the cleanest statement in the volume that there are two distinct "
     "mechanisms on the same table: contact with the body, or induction through "
     "the glass. Brief 12 item 2 has to separate them or the reader conflates "
     "the body-as-wire case with the field case; this sentence is his own "
     "separation, and 'merely' is his own lowering of the coatings to a "
     "convenience. The dashes are the print's em dashes, ASCII form above"),

    ("I have produced the incandescence of a button, filament, or wire "
     "enclosed in a tube. To get to this result it was necessary to economize "
     "the energy which is obtained from the field, and direct most of it on the "
     "small body to be rendered incandescent",
     289, "5. What the internet gets wrong (the energy comes from the field, in his words)",
     "brief 12 item 5's central correction, stated by him: the energy is "
     "obtained FROM THE FIELD and economised, not created in the tube. 'A "
     "necessary to economize' is the verb of a conservation argument, and it is "
     "on the same page as the tube-in-hand demo the myth is built on. This is "
     "the row to quote if the article quotes only one sentence against 'light "
     "without energy'"),

    ("Intense phosphorescence may be excited in a bulb by merely connecting it "
     "to a plate within the field, and the plate need not be any larger than an "
     "ordinary lamp shade",
     289, "1. The strangest demo (the bulb on a plate, not in the hand)",
     "the version of the demo that does not need a person in it, and the size "
     "of the electrode: a lamp shade. Brief 12 item 2's mechanism, in a "
     "demonstration. Article 01's page covers the plate-as-circuit-part at "
     "printed pp. 183-184 from the New York lecture; this is the London lecture "
     "of 1892 saying the same thing a year later with a bigger object, which is "
     "the point the article can make about why the trick scales"),

    ("A small phosphorescent bulb, when attached to a wire connected to a coil, "
     "emits sufficient light to allow reading ordinary print at a distance of "
     "five to six paces",
     289, "1. The strangest demo (the one brightness claim on the page)",
     "the only brightness number in the demo passage: readable print at five to "
     "six paces. It is a comparison, not a measurement, and it is the number the "
     "article can print where chapter XXXII gives none (see the scoped-absence "
     "table). The fragment straddles printed pp. 289-290 as one run, so cite "
     "one page only"),

    ("It was of interest to see how some of the phosphorescent bulbs of "
     "Professor Crookes would behave with these currents, and he has had the "
     "kindness to lend me a few for the occasion",
     290, "1. The strangest demo (Crookes lent him the bulbs)",
     "the human fact behind the demo, and the link to the one Crookes quote the "
     "series already prints (article 10's p. 236 'Crookes came nearest to doing "
     "it'). Here the two men are in the same room by proxy: Crookes lent the "
     "apparatus for the London lecture. Nothing in the volume says Crookes "
     "approved of Tesla's conclusions, and the article must not imply it"),

    ("The effects produced are magnificent, especially by the sulphide of "
     "calcium and sulphide of zinc",
     290, "1. The strangest demo (which coatings worked)",
     "the two phosphor coatings he names, which is the substance behind brief 12 "
     "item 2's 'phosphorescent coatings'. A specific material fact from the "
     "page, not a description of glow. Note the word 'magnificent' is about a "
     "visual effect on a stage, and is the kind of adjective the article should "
     "attribute rather than adopt"),

    ("With the disruptive discharge coil they glow intensely merely by holding "
     "them in the hand and connecting the body to the terminal of the coil",
     290, "1. The strangest demo (the bulbs in the hand, again)",
     "the mechanism of the hand-lit bulb in one clause: hold it, connect the "
     "body to one terminal. Same page as the Crookes bulbs, so the article can "
     "put the mechanism and the object in one paragraph without stitching two "
     "pages. 'Merely' again does the work brief 12 item 5 needs: no mystery "
     "apparatus, just a body and a terminal"),

    ("It has been, my chief aim in presenting these results to point out "
     "phenomena or features of novelty, and to advance ideas which I am "
     "hopeful will serve as starting points of new departures",
     292, "5. What the internet gets wrong (what he says the lecture was for)",
     "his own statement of what the lecture claims: phenomena, features of "
     "novelty, ideas as starting points. Not a claim of a working lamp. This is "
     "the sentence to close brief 12 item 5 with, because it is the author "
     "setting the size of his own claim, on the last page of the chapter. The "
     "comma after 'been' is the print's"),

    ("the pleasure I have had in presenting these results to a gathering of so "
     "many able men",
     293, "0. Provenance (the last page of the lecture)",
     "the last sentence of chapter XXVII, and the reason the p. 292 row above is "
     "the lecture's own closer rather than an editorial summary. Quote it only if "
     "the article needs to show the lecture ending on courtesy; it is not "
     "evidence of anything technical. The full sentence carries an em dash the "
     "draft cannot print - see Rejected #34"),
]

QUOTES += [
    # ---- 2. Why a tube lights with no wires. Chapter XXXII is the book's own
    # account of the apparatus and what happened in it, and it is the only
    # chapter in the volume whose whole subject is a tube with nothing leading
    # into it. Brief 12 item 2. Read FOUR TEXTS, FOUR VOICES first: half of
    # what follows is J. J. Thomson's, and the apparatus in Figs. 216-219 is
    # his, not Tesla's.
    ("In all forms of apparatus used there was no special difficulty in "
     "exciting a luminous circle or cylinder in proximity to the primary",
     397, "2. Why a tube lights with no wires (what happened every time)",
     "the base rate of the whole chapter: the effect was not occasional, it "
     "reproduced in every form of apparatus he built. The article needs this "
     "before it can call anything a result. Note the sentence's second half is a "
     "different claim (about the circles' position) and is pinned separately "
     "below"),

    ("Fig. 210 may serve as an example of one of the many forms of apparatus "
     "used. This consisted of a large glass tube sealed at one end and "
     "projecting into an ordinary incandescent lamp bulb",
     397, "2. Why a tube lights with no wires (the apparatus the brief's figure shows)",
     "the sentence that describes the brief's first figure, Fig. 210 on printed "
     "p. 397, in the book's own words: a large glass tube sealed at one end and "
     "projecting INTO an ordinary incandescent lamp bulb. If the article uses "
     "that crop it has the caption from the same page, which is what §6.6 wants "
     "(read the number off the printed page, and caption from the text beside "
     "it). 'one of the many forms' is also his own statement that this was a "
     "class of apparatus, not a single device"),

    ("To excite luminosity in the tube it is not absolutely necessary that the "
     "conductor should be closed",
     398, "2. Why a tube lights with no wires (the circuit need not be closed)",
     "the sentence that removes the reader's first objection ('where does the "
     "current come back through?'). A closed conductor is not necessary. This is "
     "the 1891 version of the fact article 01 states in modern words as 'the "
     "insulated body serves to give off the energy into the surrounding space, "
     "and is equivalent to a return wire' (p. 184), which article 01 has already "
     "quoted; the two are the same finding in two vocabularies, and the article "
     "should link rather than re-explain"),

    ("before the disruptive discharge takes place, the tube or bulb is slightly "
     "excited and the formation of the luminous circle is decidedly "
     "facilitated",
     398, "4. The vacuum problem (the effect is already there before the spark)",
     "the observation that connects chapter XXXII to the p. 288 'retains the "
     "faculty' sentence: the tube is partly excited BEFORE the discharge, so "
     "excitation is a state the tube can be in, not a magic event. This is the "
     "strongest support in the volume for brief 12 item 5's 'a charge/ionisation "
     "state', and it is a laboratory observation rather than a lecture trick"),

    ("It must be remembered that in these experiments we have to deal with "
     "primary currents of an enormous frequency or rate of change and of high "
     "potential, and that the secondary conductor consists of a rarefied gas, "
     "and that under such conditions electrostatic effects must play an "
     "important part",
     398, "2. Why a tube lights with no wires (the conditions that make it work)",
     "the sentence that states the boundary conditions of every effect in this "
     "article: enormous frequency, high potential, and a rarefied gas as the "
     "secondary conductor. 'must play an important part' is a conditional, not a "
     "conclusion, and the article should quote it as the condition under which "
     "the rest of the chapter holds. The whole demo fails without those three "
     "conditions, which is why none of it can be tried at home"),

    ("an ordinary exhausted tube (preferably of large diameter) be surrounded "
     "by a spiral of thick copper wire serving as the primary ... feebly "
     "luminous spiral may be induced in the tube",
     399, "2. Why a tube lights with no wires (the tube inside a coil)",
     "the arrangement the brief's Fig. 215 crop shows: a spiral of thick copper "
     "wire around an exhausted tube, and the tube lights without being connected "
     "to anything. 'feebly' is his own word for the brightness, and it is the "
     "counterweight to every modern retelling that says the tube blazed. The cut "
     "in the middle is where the scan breaks, and the break is measured, not "
     "assumed: the print carries a footnote marker at the end of 'primary' and "
     "the OCR then sets 'primary^ afeebly', gluing the following article to the "
     "word after it, so the strict index has no 'a feebly' in the book at all "
     "(0 hits, measured). The second fragment therefore starts at 'feebly', "
     "which is exact on the pinned page, ratio 1.0. The joined form with a comma "
     "is only fuzzy 0.967 and is Rejected #8"),

    ("the lamp-bulb was provided with a tinfoil coating on the side opposite to "
     "the primary and each time the tinfoil coating was connected to the ground "
     "or to a large object the luminosity of the circle was considerably "
     "increased. This was evidently due to electrostatic action",
     399, "2. Why a tube lights with no wires (adding a plate makes it brighter)",
     "the experiment that shows the effect is a coupling between two electrodes "
     "with the glass between them: adding a tinfoil plate opposite the primary, "
     "and connecting it to ground or to a large object, makes it brighter. That "
     "is a capacitor being tuned, described without the word. 'This was "
     "evidently due to electrostatic action' is his own inference, on the same "
     "breath as the observation, and the article should keep them together so "
     "the reader can see which part is the measurement and which is the reading "
     "of it"),

    ("the fact that a glow can be produced along the primary in the form of an "
     "open spiral argues for an electrostatic effect",
     399, "2. Why a tube lights with no wires (how he argued, not what he saw)",
     "'argues for' is the phrase to teach from: this is an inference from a "
     "second observation, not a proof. The article's beat 2 has to separate what "
     "the tube did from what he concluded, and this sentence shows him doing both "
     "in one line. Chapter XXXII's whole argument is of this form, which is why "
     "the chapter reads as a debate and not as a lab report"),

    ("two intensely luminous circles, each of them close to a turn of the "
     "primary spiral, were formed inside of the tube, and I attributed this "
     "phenomenon to the existence of nodes on the primary",
     399, "2. Why a tube lights with no wires (standing waves in the coil)",
     "the observation that the light sits at fixed places, and his explanation "
     "(nodes on the primary). 'I attributed' is again an attribution, and it is "
     "the one claim in the chapter about WHY the pattern is where it is. Useful "
     "for beat 2's striae/stratification material: the bands are not random, and "
     "in 1891 the only available explanation was a property of the coil, not of "
     "the gas"),

    ("the circles were always in close proximity to the primary and were "
     "considerably easier produced when the latter was very close to the "
     "glass ... and these facts speak for an electrostatic effect",
     400, "2. Why a tube lights with no wires (the closer the coil, the easier)",
     "the distance dependence, stated as an observation: always near the primary, "
     "easier when the primary was close to the glass. 'speak for' is his third "
     "inference-verb in three pages ('argues for', 'I attributed', 'speak for'), "
     "which is the pattern the article can name instead of characterising him. "
     "The cut is the page's figure label between the two halves of the sentence"),

    ("in my experiments they were broad and often the whole of the bulb or tube "
     "was illuminated",
     400, "2. Why a tube lights with no wires (his tubes were not thin rings)",
     "the correction to the drawing most retellings give: his effects were broad "
     "and often filled the whole bulb. It is a first-person claim about his own "
     "apparatus, made in reply to Thomson's narrower rings, so it is also part "
     "of the argument - see the flag THE RING OF LIGHT IS THOMSON'S, THE BROAD "
     "GLOW IS TESLA'S"),

    ("I have observed an intensely purplish glow, to which Prof. J. J. Thomson "
     "refers",
     400, "2. Why a tube lights with no wires (the colour, and whose observation it is)",
     "the colour of the glow, and the sentence is a cross-reference: he is "
     "confirming a detail Thomson reported. 'purplish' is in the volume "
     "@@purplish_vol@@ times and in chapter XXXII @@purplish_ch32@@ times "
     "(measured): his at printed p. 400 and Thomson's at printed p. 403, which "
     "is the one he refers to. His colour claim is corroborative rather than "
     "original, and the two glows must not be blended into one. Brief 12's query "
     "list includes 'tesla phosphorescence', and the Tier 3 backlog topic "
     "'tesla-phosphorescent-colours' is this same chapter, so the colour "
     "material here is also a future article's - keep it short"),

    ("there is a molecular bombardment inthe plane of the luminous circle at "
     "right angles to the glass",
     400, "2. Why a tube lights with no wires (the mechanism he proposes)",
     "the mechanism sentence: molecular bombardment in the plane of the circle, "
     "at right angles to the glass. This is the closest the chapter comes to a "
     "physical picture of what makes the light, and it is the 1891 counterpart "
     "of the 'trillions of invisible hammers' sentence at printed p. 175. The OCR "
     "glues 'inthe'; the print has the space, so this verifies only through the "
     "space-ignoring index and the draft prints 'in the'"),

    ("when the specific inductive capacity of the medium between the primary and "
     "secondary is increased, the inductive effect is augmented",
     401, "2. Why a tube lights with no wires (the coupling depends on the medium)",
     "the sentence that says the effect between primary and secondary depends on "
     "the specific inductive capacity of what is between them. That is a "
     "dielectric constant, and it is the mechanism brief 12 item 5 calls "
     "capacitive coupling, in the period's words. The book's word for the "
     "component is 'condenser' (measured, table below); 'capacitor' is 0"),

    ("a glass tube T slipped between the primary and the bulb, when the effect "
     "pointed out was noted. Were the action wholly electromagnetic no change "
     "could possibly have been observed",
     401, "2. Why a tube lights with no wires (a test that could have failed)",
     "a designed discriminating test: put a glass tube between primary and bulb "
     "and the effect changes, which a purely electromagnetic action could not do. "
     "'no change could possibly have been observed' is the counterfactual, and it "
     "is the best evidence in the chapter that he was trying to falsify himself. "
     "Pair it with the p. 401 tinfoil row below and with the flag HE TRIED TO "
     "SCREEN IT OUT AND THE SCREENING FAILED"),

    ("this bombardment being evident from the rapid heating of the glass near "
     "the primary. Were the bombardment not at right angles to the glass the "
     "heating could not be so rapid",
     401, "2. Why a tube lights with no wires (a second counterfactual, from heat)",
     "the same reasoning style from a different sense: the glass got hot, and "
     "only a bombardment at right angles could do that. It is an inference from a "
     "burnt bulb, and the article should say so. It also gives the article a "
     "physical consequence of the mechanism (the glass heats), which matters for "
     "beat 3's lamp problem: the glass must be kept away from the hot part"),

    ("when a bulb is surrounded by a wire closed upon itself and in the plane of "
     "the primary, the formation of the luminous circle within the bulb is not "
     "prevented",
     401, "2. Why a tube lights with no wires (a shorted turn does not stop it)",
     "the null result that kills the simple transformer story: a closed wire "
     "round the bulb, which is a shorted turn, does not stop the light. Any "
     "reader who has worked out 'the tube is the secondary of a transformer' will "
     "expect a shorted turn to kill it, and it does not. This is the single best "
     "quote for brief 12 item 5's 'the energy is capacitively coupled', because "
     "it is a measurement that discriminates between the two stories"),

    ("But if instead of the wire a broad strip of tinfoil is glued upon the "
     "bulb, the formation of the luminous band was prevented, because then the "
     "action was distributed over a greater surface",
     401, "2. Why a tube lights with no wires (what does stop it)",
     "the positive control for the row above: a broad tinfoil strip DOES prevent "
     "the band, and he gives the reason (distribution over a greater surface). "
     "Two experiments on one page that bracket the effect. Note the tense change "
     "in the print ('is glued' then 'was prevented'); quote it as set"),

    ("For want of time I have, however, not been able to perform the experiment",
     401, "5. What the internet gets wrong (an experiment he did not do)",
     "the plain admission that a test he described had not been run. It belongs "
     "in the article wherever a claim of his is reported as a finding, because it "
     "is his own record of the boundary between what he tried and what he "
     "sketched. Read the flag HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS"),

    ("To produce discharges in tubes devoid of electrodes was, however, not easy "
     "to accomplish, for the only available means of producing an electromotive "
     "force in the discharge circuit was by electro-magnetic induction",
     402, "2. Why a tube lights with no wires (the difficulty, in Thomson's abstract)",
     "the difficulty stated, but the voice is not his and the draft must not "
     "print it as if it were: this sentence is inside "
     "the abstract of J. J. Thomson's paper, in third-person reportage, on the "
     "same page as the heading that begins 'SOME EXPERIMENTS ON THE ELECTRIC "
     "DISCHARGE BY PROF. J. J. THOMSON'. It is the one sentence in this chapter "
     "that reads like Tesla's prose and is not his. Read the flag THE ABSTRACT "
     "IS THIRD PERSON AND THE PROSE IS FLUENT, WHICH IS THE TRAP"),

    ("I have experimentally proved that if the same discharge which is barely "
     "sufficient to excite a luminous band in the bulb when passed through the "
     "primary circuit be so directed as to exalt the electrostatic inductive "
     "effect - namely, by converting upwards - an exhausted tube, devoid of "
     "electrodes, may be excited at a distance of several feet",
     402, "2. Why a tube lights with no wires (his principal argument)",
     "'My principal argument is the following' is the sentence that introduces "
     "this one, on the same page, and it is the only place in the chapter where "
     "he labels his own best case. The claim is quantitative in a way the rest is "
     "not: the SAME discharge, redirected, lights a tube several feet away. "
     "'exalt' is the period's verb for strengthening a coupling. The dashes are "
     "the print's em dashes and cannot be printed; cut at them or use brackets"),

    ("the introduction of mercury or the heating of the bulb prevents the "
     "formation of the luminous band or shortens the after-glow; and also why "
     "in some cases a platinum wire may prevent the excitation of the tube",
     402, "2. Why a tube lights with no wires (what makes it stop)",
     "three things that spoil the effect, in one sentence: mercury in the bulb, "
     "heat, and a platinum wire inside it. The article needs the negative cases "
     "or the demo sounds like magic; and 'after-glow' is the one occurrence of "
     "that word in the volume (measured, table below), which is the word the "
     "brief's 'retains the faculty' beat is about in laboratory terms"),

    ("in one of my experiments in which a vacuum was produced by the "
     "Torricellian method, I was unable to produce the luminous band, but this "
     "may have been due to the weak exciting current employed",
     402, "4. The vacuum problem (a failure, and his guess at the cause)",
     "a negative result with the reason attached, and the reason is his own "
     "apparatus, not the tube. This is the laboratory version of the p. 288 "
     "'another tube might not light' moment, and it is dated 1891 in his own "
     "article. 'Torricellian method' is the barometric vacuum, i.e. the best "
     "vacuum he had; the failure is exactly the non-striking problem of brief 12 "
     "item 4, described before he had the high-frequency apparatus to beat it"),

    ("On exhausting the jar, however, the luminous discharge grew fainter, and a "
     "point was reached at which no secondary discharge was visible",
     403, "4. The vacuum problem (the same failure, in Thomson's apparatus)",
     "THOMSON'S observation, not Tesla's, and it is the same phenomenon: pump "
     "the air out further and the light goes out. Two men, two apparatuses, one "
     "page apart, both hitting the vacuum limit. That is the strongest possible "
     "support for brief 12 item 4's point that the vacuum is the hard part, and "
     "it is also the reason the article must name whose apparatus is whose"),

    ("J urther exhaustion of the jar caused the secondary discharge to appear "
     "outside of the bulb",
     403, "4. The vacuum problem (where the light goes when the tube stops)",
     "the continuation of the row above, and the detail that makes it a "
     "mechanism rather than a failure: past the limit, the discharge moves "
     "outside the bulb. The OCR prints 'J urther' with a space after the J, an "
     "artefact of a capital J at the start of a line; the print reads 'Further', "
     "so this verifies only through the space-ignoring index"),

    ("Leyden jar, which combines the two essentials of a current whose maximum "
     "value is enormous, and whose rapidity of alternation is immensely great",
     403, "2. Why a tube lights with no wires (the source of the high frequency)",
     "THOMSON'S account of how he got the frequency, and it is the answer to the "
     "reader's question 'what drove this': a Leyden jar discharged oscillatory. "
     "The sentence begins at the foot of printed p. 402 with 'recourse was had "
     "to the oscillatory discharge of a', and the two halves do NOT join in the "
     "index: the page's own footnote ('1. Abstract of a paper read before "
     "Physical Society of London.') sits between them in the page body and "
     "strip_furniture keeps it, so the joined run returns no match at all and "
     "the p. 402 half is Rejected #11. Quote the p. 403 half only. "
     "The whole chapter's effects come from a spark-gap and a jar, which is also "
     "why the numbers are not reproducible to modern tolerances. Attribute to "
     "Thomson's abstract"),

    ("The two or three turns, as shown in Fig. 216, in each, were found to be "
     "quite sufficient",
     403, "2. Why a tube lights with no wires (Fig. 216 is Thomson's)",
     "the sentence that names Fig. 216, and it is THOMSON'S figure, not Tesla's. "
     "The brief does not ask for Fig. 216, but it asks for Fig. 218, which is on "
     "the same page and is also Thomson's. This row exists so the figure task "
     "does not caption a plate of Thomson's apparatus as Tesla's. Read the flag "
     "THE BRIEF'S FIG. 218 IS THOMSON'S APPARATUS"),

    ("An exhausted bulb, Fig. 217, containing traces of oxygen was plaeed "
     "within a primary spiral of three turns, and, on passing the jar discharge, "
     "a circle of light was seen within the bulb inclose proximity to the "
     "primary circuit, accompanied by a purplish glow, which lasted for a second "
     "or more",
     403, "2. Why a tube lights with no wires (the ring of light, and its duration)",
     "THOMSON'S apparatus and THOMSON'S observation, and it is the origin of the "
     "'ring of light' that the popular story attaches to Tesla. 'lasted for a "
     "second or more' is a duration, which is the fact the persistence beat needs "
     "in laboratory terms. Two OCR defects sit inside this one quote: 'plaeed' "
     "for 'placed' and 'inclose' for 'in close'. The first is a real OCR error "
     "the space-ignoring index cannot fix, so the quote is cut around it - see "
     "Rejected #12"),

    ("On heating the bulb, the duration of the glow was greatly diminished, and "
     "it could be instantly extinguished by the presence of an electro-magnet",
     403, "2. Why a tube lights with no wires (heat and magnetism kill it)",
     "THOMSON'S, and it is the counter-experiment to the persistence story: heat "
     "shortens the glow and a magnet kills it. If the article reports that a "
     "tube 'remembers', this is the sentence that shows the memory is physical "
     "and can be erased. Attribute to the abstract, not to Tesla"),

    ("The phenomena of vacuum discharges were, Prof. Thomson said, greatly "
     "simplified when their path was wholly gaseous, the complication of the "
     "dark space surrounding the negative electrode, and the stratifications so "
     "commonly observed in ordinary vaciium tubes, being absent",
     402, "2. Why a tube lights with no wires (stratification, in the other man's words)",
     "the word the brief asks for ('striae') appears in this chapter as "
     "'stratifications', in THOMSON'S reported speech, and the sentence says "
     "those bands are absent when the path is wholly gaseous. So the chapter "
     "that the brief treats as the striae source actually reports their ABSENCE. "
     "The real striae sentences are in the New York lecture at printed p. 186. "
     "The print's typo 'vaciium' is inside this quote and must be reproduced or "
     "cut - see the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT "
     "SILENTLY FIX"),

    ("at the outset, I myself looked for a purely electrodynamic effect and "
     "believed that I had obtained it. But many experiments performed at that "
     "time proved to me that the electrostatic effects were generally of far "
     "greater importance",
     404, "5. What the internet gets wrong (he changed his own mind, in public)",
     "the sentence that makes this chapter a record of a mind changing: he looked "
     "for one effect, believed he had it, and was proved wrong by his own "
     "experiments. It is the best anti-myth quote available, because it is the "
     "author reporting his own error in a published reply. 'generally' and 'far "
     "greater' are hedged on purpose; the draft must not turn it into 'he "
     "disproved himself'"),

    ("In using the term electrostatic I had reference rather to the nature of "
     "the action than to a stationary condition, which is the usual acceptance "
     "of the term",
     404, "2. Why a tube lights with no wires (what he means by electrostatic)",
     "the definition sentence, and it is a warning to the modern reader: his "
     "'electrostatic' does NOT mean stationary, it means the action is of the "
     "kind associated with charge rather than with current. Every sentence in the "
     "article that uses the word has to be read against this. It is also the "
     "reason 'capacitively coupled' is a fair translation and 'static "
     "electricity' is not"),

    ("I did not, as Prof. J. J. Thomson seems to believe, misunderstand his "
     "position in regard to the cause of the phenomena considered, but I thought "
     "that in his experiments, as well as in my own, electrostatic effects were "
     "of great importance",
     404, "0. Provenance (the reply, in his words)",
     "the opening of Tesla's published reply to Thomson, and the pair of it is on "
     "printed p. 406 in Thomson's own words ('He seems, however, to have "
     "misunderstood my position'). Two men, two printed pages, each saying the "
     "other had misunderstood him. That is the honest shape of the discovery "
     "story and the article should show it once, plainly, with both pages. Read "
     "the flag TWO MEN, ONE VOLUME, EACH SAYING THE OTHER MISREAD HIM"),

    ("It did not appear, from the meagre description of his experiments, that "
     "all possible precautions had been taken to exclude these effects",
     404, "0. Provenance (his criticism of the other man's evidence)",
     "'meagre description' is a published criticism of a published report, and it "
     "is also a description of the state of the evidence in this whole "
     "controversy: nobody in the volume has enough detail from the other side to "
     "settle it. That is a fact about 1891 priority disputes that the article can "
     "state, and this is the quote that licenses it"),

    ("Without doubting in the least that, with the care and precautions taken by "
     "Prof. J. J. Thomson, the luminosity excited was due solely to "
     "electrodynamic action, I would say that in many experiments I have "
     "observed curious instances of the ineffectiveness of the screening",
     405, "2. Why a tube lights with no wires (he conceded the other case)",
     "the concession, which the article must not skip: he accepted that Thomson's "
     "result was genuine, and offered only that his own screens did not work. "
     "Without this row, beat 5 reads as Tesla winning an argument he never had. "
     "'curious instances of the ineffectiveness of the screening' is also the "
     "understatement that hides how much his own apparatus leaked"),

    ("I will suppose that near a closed exhausted tube be placed a small sphere "
     "charged to a very high potential. The sphere would act inductively upon "
     "the tube",
     404, "2. Why a tube lights with no wires (the thought experiment)",
     "the model he builds to explain the effect: a charged sphere near a closed "
     "tube acts on it inductively. This is the mechanism brief 12 item 5 calls "
     "capacitive coupling, drawn as an object. It is a supposition, not an "
     "experiment - 'I will suppose' is in the sentence - and the article has to "
     "say that"),

    ("the same would undoubtedly produce luminosity (if the potential be "
     "sufficiently high), until a permanent condition would be reached",
     405, "5. What the internet gets wrong (the limit of his own model)",
     "the conditional inside his model: it would produce light if the potential "
     "were high enough, until a permanent condition was reached. The parenthetical "
     "condition and the 'permanent condition' limit are both in the print, and "
     "they are the two places where the model stops. Quote them with the claim"),

    ("Assuming the tube to be perfectly well insulated, there would be only one "
     "instantaneous flash during the act of distribution. This would be due to "
     "the electrostatic action simply. But now, suppose the charged sphere to be "
     "moved at short intervals with great speed along the exhausted tube. The "
     "tube would now be permanently excited, as the moving sphere would cause a "
     "constant redistribution of electricity and collisions of the molecules of "
     "the rarefied gas",
     405, "5. What the internet gets wrong (the answer to 'what changed in the tube')",
     "the single best quote in the volume for brief 12 item 5, and it is a "
     "thought experiment, not a measurement: one flash if the charge is "
     "stationary, permanent excitation if the charge keeps moving, because a "
     "constant redistribution of electricity keeps colliding the gas molecules. "
     "That is exactly the distinction the p. 288 question needs: the persistent "
     "state is not stored power, it is a condition that a moving charge can "
     "maintain. He never ran this as an experiment; 'Assuming' and 'suppose' are "
     "in the sentence. Read the flag HE ANSWERS HIS OWN QUESTION ON THE NEXT "
     "PAGE AND NOBODY QUOTES IT"),

    ("the importance of the quality of glass of which the tube is made",
     405, "3. Tesla's lamp research (the glass is part of the device)",
     "the glass matters, and it is a practical engineering statement inside a "
     "theoretical passage. It connects beat 2 to beat 3: the envelope is not a "
     "container, it is part of the coupling and it heats. This is the sentence "
     "that makes the carborundum passage a lamp problem rather than a curiosity"),

    ("I also endeavored to ascertain the influence of a medium of high "
     "permeability by using oxygen",
     405, "2. Why a tube lights with no wires (he tried a different gas)",
     "the gas-variable experiment, in his own first person. Note the word choice: "
     "'permeability' for a gas, which is the period's usage and not ours. The "
     "result is in the next row and it is hedged by him, so the two rows belong "
     "together"),

    ("an oxygen tube when excited under similar conditions - that is, as far as "
     "could be determined - gives more light; but this, of course, may be due to "
     "many causes",
     405, "5. What the internet gets wrong (a result he refuses to interpret)",
     "a comparative observation with the comparison itself disclaimed: 'as far as "
     "could be determined' and 'may be due to many causes'. This is the model "
     "sentence for how the article should report any comparison he makes, "
     "including the 20-times lamp claim in beat 3. The dashes are the print's em "
     "dashes and cannot be printed; cut at them"),

    ("the luminosity in a tube near a wire through which a Leyden jar was "
     "discharged was noted by Hittorf",
     405, "0. Provenance (the prior art he names himself)",
     "the name he gives for the earliest observation of this kind, Hittorf, which "
     "is the sentence that stops the article from saying Tesla saw it first. It "
     "is Tesla's own citation, in Tesla's own article, and it is on the same page "
     "as the claim that his effects were much stronger. Read the flag PRIORITY IN "
     "THIS CHAPTER IS ABOUT WHO PUBLISHED AND WHO NOTED"),

    ("been noted by many experimenters, but in my experiments the effects were "
     "much more powerful than those usually noted",
     406, "0. Provenance (his actual priority claim)",
     "the whole of his priority claim, and it is a claim about intensity, not "
     "about being first: many experimenters noted it, his was stronger. The "
     "sentence begins on printed p. 405 and finishes at the top of p. 406, before "
     "the Thomson communication starts, so the voice is Tesla's. This is the row "
     "that settles brief 12 item 5's framing: he never claimed the effect was "
     "unknown, he claimed his version was bigger"),

    ("Wet blotting paper is a sufficiently good conductor to screen off a "
     "stationary electrostatic effect, though it is not a good enough one to stop "
     "waves of alternating electromotive intensity",
     406, "2. Why a tube lights with no wires (the other man's screen)",
     "THOMSON'S method and THOMSON'S reasoning, in his own words in his own "
     "published note: a wet paper screen stops a stationary electrostatic effect "
     "but not alternating electromotive waves. That is a shielding rule of thumb "
     "that is still right, and it is the counterweight to Tesla's 'ineffectiveness "
     "of the screening'. The two sentences on this page are the actual technical "
     "content of the 1891 dispute"),

    ("the first experiment I tried with the discharge of a Leyden jar produced "
     "luminosity in the tube, but it was not until after six weeks' continuous "
     "experimenting that I was able to get a discharge in the exhausted tube "
     "which I was satisfied was due to what is ordinarily called electrodynamic "
     "action",
     406, "0. Provenance (the six weeks are THOMSON'S, not Tesla's)",
     "the trap in this chapter, and the reason this row is here rather than in "
     "the mechanism section: the famous 'six weeks' sentence is J. J. THOMSON "
     "describing HIS OWN Leyden-jar work, inside the communication quoted on "
     "printed p. 406. Any article that writes 'Tesla spent six weeks' has taken "
     "Thomson's sentence. Read the flag THE SIX WEEKS BELONG TO THOMSON"),

    ("Mr. Tesla seems to ascribe the effects he observed to electrostatic "
     "action, and I have no doubt, from the description he gives of his method "
     "of conducting his experiments, that in them electrostatic action plays a "
     "very important part",
     406, "0. Provenance (the other man's verdict on him)",
     "THOMSON'S published assessment of Tesla's experiments, and it is "
     "conceding, not denying: electrostatic action 'plays a very important part' "
     "in them. The article can use this to show that the 1891 dispute was not "
     "about whether the effect was electrostatic but about whether it could also "
     "be produced without it. Third person about Tesla, first person about "
     "Thomson, one sentence"),

    ("He seems, however, to have misunderstood my position with respect to the "
     "cause of these discharges, which is not, as he implies, that luminosity in "
     "tubes without electrodes cannot be produced by electrostatic action, but "
     "that it can also be produced when this action is excluded",
     406, "0. Provenance (the misunderstanding, in his words)",
     "the other half of the duelling pair, and it is a precise statement of "
     "Thomson's actual position, which is NOT that electrostatic action cannot "
     "light a tube. Without this row the article will make Thomson the opponent "
     "of the electrostatic explanation, which is exactly what he said he was not "
     "arguing. Pair with the p. 404 row"),

    ("Whilst the discharge of the jar is going on, it is difficult, and, from a "
     "theoretical point of view, undesirable, to eparate the effect into parts, "
     "one of which is called electrostatic, the other electromagnetic ; what we "
     "can prove is that in this case the discharge is not such as would be "
     "produced by electromotive forces derived from a potential function",
     406, "5. What the internet gets wrong (the question is the wrong question)",
     "THOMSON'S sentence, and it is the modern answer to brief 12 item 5 stated "
     "in 1891: during a jar discharge it is difficult and theoretically "
     "undesirable to split the effect into an electrostatic part and an "
     "electromagnetic part. The article's beat 5 can end on this, because it is "
     "not a modern correction smuggled into a Victorian text - a participant in "
     "the dispute said it. The OCR prints 'eparate' for 'separate'; the quote "
     "carries it and the draft prints 'separate', which verifies only through the "
     "space-ignoring index"),

    ("The account of the experiments in the Electrician was from a reporter's "
     "note, and was not written, or even read, by me",
     406, "0. Provenance (why the record is thin)",
     "THOMSON explaining why the published account of his own experiments was "
     "thin: a reporter wrote it and he did not read it. It is the reason the "
     "whole dispute in this chapter is unresolvable from the printed record, and "
     "it is a fact about sources that the article's sources section can state. "
     "It also explains Tesla's 'meagre description' jab"),

    ("I have now almost finished writing out, and hope very shortly to publish, "
     "an account of these and a large number of allied experiments",
     406, "0. Provenance (the promise, and what the volume contains instead)",
     "THOMSON'S promise at the end of his communication, and the article's "
     "sources section needs it: the fuller account he promised is not in this "
     "book. His communication's last words on printed p. 406 are 'for which, "
     "however, I must refer to my paper', and the chapter ends there. What the "
     "reader has here is a magazine article, an abstract, a reply and a note, "
     "which is the whole of the evidence base for this article"),

    ("the luminous effects, which are producible by induction in a tube devoid "
     "of electrodes, I am inclined to consider as being of an electrostatic "
     "nature",
     175, "2. Why a tube lights with no wires (the position, stated in 1891)",
     "the thesis of the whole article, in his own words, in the New York lecture "
     "of May 1891, a year and a half before the London lecture the brief's hook "
     "comes from: 'I am inclined to consider'. That hedge is the sentence's "
     "honest content and it must be quoted with the claim, not trimmed to 'is of "
     "an electrostatic nature'. The preceding sentence names a Geissler tube, "
     "which is the brief's other query term"),

    ("Such dark waves, unless they are of the length of true light waves, "
     "cannot, it would seem, excite luminous radiation in a Geissler tube",
     175, "2. Why a tube lights with no wires (Geissler, and what he ruled out)",
     "the only place in the volume where a Geissler tube is used as an argument "
     "rather than as a prop: he rules out long electromagnetic waves exciting a "
     "Geissler tube, and infers the effect must be electrostatic. 'it would "
     "seem' again. Brief 12's query list includes 'geissler tube tesla', and "
     "'Geissler' is in the volume @@geissler_vol@@ times (measured): "
     "@@geissler_ch26@@ of them inside the 1891 New York lecture at printed "
     "pp. 145-197, and one more, @@geissler_outside@@, outside that chapter. A "
     "sentence that says the word appears only in the lecture is wrong by one "
     "hit, and the table below gives the pages"),

    ("we may place a body of some refractory material in a closed, and "
     "preferably more or less exhausted, globe, connect it to a source of ... "
     "high, rapidly alternating potential, causing the molecules of the gas to "
     "strike it many times a second at enormous speeds, and in this manner, with "
     "trillions of invisible hammers, pound it until it gets incandescent",
     175, "2. Why a tube lights with no wires (the mechanism, in his best sentence)",
     "the mechanism of a lamp with no filament leads, stated as an image: "
     "trillions of invisible hammers. It is the sentence that connects beat 2 to "
     "beat 3 - the gas molecules are the power source and the button is what they "
     "hit - and it is dated May 1891, before the carborundum work of 1892. The "
     "cut is a stray OCR bullet at the end of a printed line, not an ellipsis in "
     "the text; see Rejected #16 for the uncut form"),

    ("we may place a body in a very highly exhausted globe, in a non-striking "
     "vacuum, and, by employing very high frequencies and potentials, transfer "
     "sufficient energy from it to other bodies in the vicinity, or in general to "
     "the surroundings, to maintain it at any degree of incandescence",
     175, "4. The vacuum problem (the method for beating a non-striking vacuum)",
     "the method, in one sentence, and the phrase 'transfer sufficient energy' is "
     "the conservation language the article needs for beat 5: energy is moved, "
     "not generated. The fragment straddles printed pp. 175-176 as one run, so "
     "cite one page only. 'non-striking vacuum' here is the term of art brief 12 "
     "item 4 is about, and this is where it is first defined in the volume"),

    ("causing them to viorate and to emit light",
     176, "2. Why a tube lights with no wires (the shortest statement of the mechanism)",
     "the mechanism in six words: disturb the ether or static charges carried by "
     "the gas molecules, make them vibrate, get light. The OCR prints 'viorate' "
     "for 'vibrate' - a real scan error the space-ignoring index cannot fix, so "
     "the draft must print the OCR's word or cut the word out. Read the flag "
     "SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX"),

    ("the physiological effect of the current required to maintain at a certain "
     "degree of brightness a tube four feet long, provided at the ends with "
     "outside and inside condenser coatings, is so powerful that, I think, it "
     "might produce serious injury to those not accustomed to such shocks ; "
     "whereas, with twenty thousand alternations per second, the tube may be "
     "maintained at the same degree of brightness without any effect being felt",
     176, "2. Why a tube lights with no wires (the one comparison he reports as a fact)",
     "the closest thing in the article's subject to a controlled comparison: same "
     "tube, same brightness, low frequency hurts, 20,000 per second does not. It "
     "is a physiological observation, not a photometric one, and it is about a "
     "four-foot tube with condenser coatings, which is the apparatus description "
     "the article needs. Article 01 already prints the p. 125 sentence about "
     "physiological effects being small for a different apparatus, so the two "
     "must not be blended: read the flag ARTICLE 01 OWNS THE SAFETY SENTENCE"),

    ("This is due principally to the fact that a much smaller potential is "
     "required to produce the same light effect, and also to the higher "
     "efficiency in the light production",
     176, "5. What the internet gets wrong (he uses the word efficiency)",
     "'efficiency' appears in the volume @@eff_vol@@ times (measured), and this "
     "is one of the few places it is used about a LIGHTING apparatus with a "
     "comparison attached: a smaller potential for the same light effect, plus a "
     "higher efficiency in light production. The whole sentence is on printed p. "
     "176 - it does NOT straddle the page break, which is why the quote is "
     "carried in full here rather than cut. The next sentence is in Rejected #18 "
     "because the OCR prints 'efficiencv' inside it. It is the strongest "
     "available answer to 'he never compared anything', and it is still "
     "not a number"),

    ("an exhausted tube be introduced from the other side in the hollow space, "
     "the tube is lighted most intensely because of the increased condenser "
     "action, and in this position the striae are most sharply defined. In all "
     "these experiments described, and in many others, the action is clearly "
     "electrostatic",
     186, "2. Why a tube lights with no wires (the word the brief wants, in his sentence)",
     "'condenser action' is in the volume @@condenser_action@@ times (measured) "
     "and this is the one that says an exhausted TUBE is lighted by it; the "
     "others are about a wire, a terminal or a loss. It is also the only place "
     "that puts 'striae' and 'clearly electrostatic' in "
     "the same paragraph. Brief 12 item 2's 'the tube is one plate of a "
     "capacitor' has its 1891 warrant here. Article 01 quotes two OTHER sentences "
     "from this same printed page (the observer-standing-on-an-insulated-support "
     "sentence and the 'wiping out the light' sentence), so the draft must not "
     "re-quote those; this one is free. Read the flag ARTICLE 01 HAS THREE "
     "SENTENCES ON p. 186 AND p. 187"),

    ("My opinion is that the heat as well as light effects produced should be "
     "proportionate, under otherwise equal conditions of test, to the product of "
     "frequency and square of potential",
     213, "5. What the internet gets wrong (the law he states and does not claim to have proved)",
     "the quantitative law he believes in: light and heat go as frequency times "
     "potential squared. 'My opinion is that' and 'should be' are in the "
     "sentence, and the next row is him saying verification would be very hard. "
     "This pair is the article's answer to 'did he measure it': he wrote down "
     "what he thought the law was AND said he had not established it. 'under "
     "otherwise equal conditions of test' is the phrase of someone who knows what "
     "a controlled test would need. Article 06's rendered page already prints "
     "this sentence with a p. 213 cite, so it is not new material here; read the "
     "flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT"),

    ("the experimental verification of the law, whatever it may be, would be "
     "exceedingly difficult. One thing is certain, at any rate, and that is, "
     "that in augmenting the potential and frequency we rapidly intensify the "
     "streams ; and, though it may be very sanguine, it is surely not "
     "altogether hopeless to expect that we may succeed in producing a practical "
     "illuminant on these lines",
     213, "5. What the internet gets wrong (his own hedge on the lamp)",
     "the hedge, verbatim, and it is the sentence the whole lamp section should "
     "be read through: 'though it may be very sanguine', 'surely not altogether "
     "hopeless'. Double negatives are his own caution, and the article should "
     "print them rather than paraphrase them as optimism. The fragment straddles "
     "printed pp. 213-214 as one run; cite one page. The missing word at the "
     "page break ('exceedingly difficult') is on p. 214 and the matcher joins "
     "it. Article 06's rendered page already prints the first clause of this "
     "sentence with a p. 213 cite; read the flag ARTICLE 06 OWNS THE COLD FLAME "
     "AND THE p. 213 LAW WITH IT"),

    ("We would then be simply using burners or flames, in which there would be "
     "no chemical process, no consumption of material, but merely a transfer of "
     "energy",
     214, "3. Tesla's lamp research (what he thought the lamp would be)",
     "the claim of the whole gas-lamp idea in one line, and it is a claim about "
     "a TRANSFER of energy, not a creation of it - the same word as the p. 175 "
     "and p. 289 rows. It is also the sentence that makes the article's bridge to "
     "the free-energy pages legitimate rather than decorative: he is describing a "
     "device that consumes nothing, and he is careful to call it a transfer. "
     "'burners or flames' is his own framing, which article 06's cold-flame page "
     "owns as a topic - read the flag ARTICLE 06 OWNS THE COLD FLAME"),
]

# ---------------------------------------------------------------------------
# Brief 12 item 3, the lamp passage. Printed pp. 253-255, inside chapter XXVII
# (the February 1892 London lecture), which is where the carborundum work is
# described in the first person, on a lecture table, with the bulbs in his hand.
# The brief's two quoted fragments ('thin threads or sticks of carborundum',
# 'came in durability nearest to those prepared of carborundum') are here, and
# so is the sentence that says why the lamp did not work: the binding material
# gives way. The passage is also the densest concentration of 'carborundum' in
# the volume (@@carborundum_scoped@@ of the @@carborundum_vol@@ occurrences in
# the book, measured), and it reports no efficiency figure, no per cent, no
# watt, no candlepower, no hours of life and no cost - see the scoped table.
# ---------------------------------------------------------------------------
QUOTES += [
    ("In the course of these experiments a great many trials were made with "
     "all kinds of carbon buttons. Electrodes made of ordinary carbon buttons "
     "were decidedly more durable when the buttons were obtained by the "
     "application of enormous pressure",
     253, "3. Tesla's lamp research (how many trials, and what worked)",
     "the scale claim, in his words: 'a great many trials', with all kinds of "
     "carbon. It is not a number, and the article must not make it one. The "
     "finding attached to it is a materials fact he can state as observed: "
     "pressure-sintered buttons lasted longer. This is the sentence that "
     "licenses 'he tested many materials' and no more than that"),

    ("there can be no doubt that all kinds of carbon are fused under the "
     "molecular bombardment, but the liquid state must be one of great "
     "instability",
     253, "3. Tesla's lamp research (what the bombardment does to the button)",
     "the mechanism of the lamp, from the other end: the gas molecules do not "
     "gently warm the button, they fuse it, and the fused state is unstable. "
     "That is the physical reason the lamp is hard, and it is stated as an "
     "inference from observation ('there can be no doubt', 'must be'). Pair it "
     "with the p. 401 heating-of-the-glass row and the p. 175 'invisible "
     "hammers' row: three pages, one mechanism, described from three angles"),

    ("Of all the bodies tried there were two which withstood best - diamond "
     "and carborundum. These two showed up about equally, but the latter was "
     "preferable for many reasons",
     253, "3. Tesla's lamp research (the two winners, and the comparison)",
     "brief 12 item 3's starting point, and it is a comparison between two "
     "materials with a result attached: diamond and carborundum came out about "
     "equal, and carborundum was preferred 'for many reasons' - which he does "
     "not enumerate here. 'Showed up about equally' is the plainest comparative "
     "statement in the passage and it has no number on it, which is exactly the "
     "shape the article should report. The print sets an em dash around 'diamond "
     "and carborundum'; the form above is the ASCII form the normaliser folds, "
     "and the draft must not print a dash (section 0 non-negotiable 5)"),

    ("As it is more than likely that this body is not yet generally known, I "
     "Avill venture to call your attention to it",
     253, "3. Tesla's lamp research (the lecture turns to a new material)",
     "the pivot in the lecture: he stops talking about his own apparatus and "
     "starts explaining a commercial product. It is also a clean example of an "
     "OCR defect the space-ignoring index cannot repair - the print reads 'Will' "
     "and the OCR prints 'Avill' (a V for W), so the quote carries the scan's "
     "letters and the draft either prints them or cuts the word. Read the flag "
     "SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX"),

    ("It has been recently produced by Mr. E. G. Acheson, of Monongahela City, "
     "Pa., II. S. A.",
     253, "3. Tesla's lamp research (where the material came from)",
     "the supply chain of the lamp research, in one line: Acheson, "
     "Monongahela City, and the carborundum company's town. This is the fact "
     "that keeps the lamp section from being only an idea - a named manufacturer "
     "was already making the stuff in 1892. The OCR prints 'II. S. A.' for "
     "'U. S. A.'; quote it as set or write 'U. S. A.' and say the scan is "
     "broken. Same defect class as the row above"),

    ("Through the kindness of the inventor, I obtained a short while ago some "
     "samples which I desired to test in regard to their qualities of "
     "phosphorescence and capability of withstanding high degrees of heat",
     253, "3. Tesla's lamp research (the two tests he actually ran)",
     "the two properties he set out to test, in his own sentence, and the "
     "source of the samples: the inventor sent them. 'Test' appears "
     "@@test_lamp@@ times in printed pp. 253-259 (measured), and this is the "
     "sentence that says what the testing was for. It is also the bridge from "
     "beat 2 to beat 3: the reason he cares about a material that withstands "
     "bombardment is that the tube's own glass gets hot"),

    ("The time has been too short to make a satisfactory study of the "
     "properties of this product, but enough experience has been gained in a "
     "few weeks I have experimented upon it to say that it does possess some "
     "remarkable properties in many respects",
     254, "3. Tesla's lamp research (he says the study was not satisfactory)",
     "the hedge on the whole lamp section, and it is printed in the middle of "
     "the passage, not at the end: the study was not satisfactory, the material "
     "had been in his hands a few weeks. Any sentence in the draft that reports "
     "a carborundum result has to be read against this sentence. It is the "
     "fourth of the four ways he records his own unfinished work - read the flag "
     "HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS. The sentence is ungrammatical as "
     "printed ('gained in a few weeks I have experimented upon it'); quote it as "
     "set or cut, do not repair it"),

    ("The only difficulty which I have experienced in its use in connection "
     "with these experiments was to find some binding material which would "
     "resist the heat and the effect of the bombardment as successfully as "
     "carborundum itself does",
     254, "3. Tesla's lamp research (the actual engineering obstacle)",
     "the real problem, stated by him as the only one: not the button, the "
     "glue. This is the sentence that answers 'why is there no carborundum "
     "lamp' without inventing a cause, and it is a claim about a specific "
     "failure mode, not a general pessimism. The word 'only' is his"),

    ("I have here a number of bulbs which I have provided with buttons of "
     "carborundum",
     254, "3. Tesla's lamp research (the objects on the lecture table)",
     "the showmanship half of the lamp passage: he is holding the things while "
     "he says it. It is the same rhetorical move as the p. 288 tube-in-hand "
     "demo, one chapter later and about a lamp, and the article can put the two "
     "in the same paragraph because both are in the same lecture. Nothing here "
     "claims the bulbs worked"),

    ("I take an ordinary lamp filament and dip its point in tar, or some other "
     "thick substance or paint which may be readily carbonized",
     254, "3. Tesla's lamp research (the process, in his words)",
     "the method in one step, and it is a workshop method: a lamp filament, tar, "
     "a hot plate. The binder is tar, which is why the sentence above about a "
     "binding material matters. Quote the process rather than summarising it; the "
     "summarised version always sounds more engineered than it was"),

    ("The button being mounted in a bulb, when a good vacuum has been reached, "
     "first a weak and then a strong discharge is passed through the bulb to "
     "carbonize the tar and expel all gases, and later it is brought to a very "
     "intense incandescence",
     254, "3. Tesla's lamp research (the vacuum step, and the beating)",
     "the making of the lamp, and it is a vacuum procedure: pump it down, then a "
     "weak discharge, then a strong one, then incandescence. This is the "
     "practical counterpart of brief 12 item 4's vacuum problem - the same "
     "exhausted-globe requirement shows up here as a manufacturing step, with "
     "'a good vacuum' as the condition and no number attached to it"),

    ("The difficulty is that the binding material gives way, and the "
     "carborundum is slowly thrown off after some time",
     255, "3. Tesla's lamp research (why the lamp did not work)",
     "the failure, in one sentence, with the mechanism named: the binder lets "
     "go and the material is sputtered off. 'After some time' is his only "
     "durability measure, and it is not a measure - the article must not turn it "
     "into a lifetime. This is the sentence that makes the lamp section an "
     "honest one, and it belongs next to the ambition sentence below, not "
     "instead of it"),

    ("it might be found useful for coating the filaments of ordinary "
     "incandescent lamps, and I think that it is even possible to produce thin "
     "threads or sticks of carborundum which will replace the ordinary "
     "filaments in an incandescent lamp",
     255, "3. Tesla's lamp research (the brief's quote, with its hedge attached)",
     "brief 12 item 3's first quoted fragment, verbatim, and the words that "
     "carry it: 'might be found useful', 'I think that it is even possible'. The "
     "plan quotes 'thin threads or sticks of carborundum' as if it were a "
     "proposal; in print it is the second half of a speculative sentence about "
     "coating ordinary lamps. Quote the whole run or do not quote the phrase. "
     "This is also the sentence that ties the lamp work to the tube work: the "
     "same bombardment that lights a tube is what he is trying to survive"),

    ("I prepared buttons of diamond dust in the same manner as of carborundum, "
     "and these came in durability nearest to those prepared of carborundum, "
     "but the binding paste gave way much more quickly in the diamond buttons",
     255, "3. Tesla's lamp research (the brief's second quote, a real comparison)",
     "brief 12 item 3's second quoted fragment, verbatim, and it is the closest "
     "thing in the volume to a materials trial with a ranking: diamond dust came "
     "nearest to carborundum, and both failed at the binder. 'Came in durability "
     "nearest to' is a comparative with no number, and 'much more quickly' is a "
     "second comparative with no number. The article may print the ranking; it "
     "may not print a lifetime, a rate, or a percentage"),

    ("this, however, I attributed to the size and irregularity of the grains "
     "of the diamond",
     255, "3. Tesla's lamp research (his explanation of the diamond failure)",
     "'I attributed' again - the fourth inference verb in this article's "
     "sources, after 'argues for', 'speak for' and 'I would say'. It is the "
     "same habit as the p. 402 nodes sentence and the p. 400 tinfoil sentence: "
     "he names a cause and marks it as his own attribution. The article should "
     "print the marker with the cause"),

    ("It was of interest to find whether carborundum possesses the quality of "
     "phosphorescence",
     255, "3. Tesla's lamp research (the question he asked the material)",
     "the research question, stated as research: does this substance "
     "phosphoresce. It is the sentence that connects the lamp passage to the "
     "phosphorescent-bulb material at printed p. 290 and to the coating "
     "question in brief 12 item 2, and it is the reason the word "
     "'phosphorescence' appears @@phos_lamp@@ times inside printed pp. 253-259 "
     "(measured). Keep the framing: he is asking, not reporting"),

    ("they are good conducting, and it is a fact that conductors do not "
     "phosphoresce",
     255, "3. Tesla's lamp research (the physics constraint he runs into)",
     "the reason the rough product cannot answer the question: conducting "
     "materials do not phosphoresce, and the crystals conduct. 'It is a fact "
     "that' is a claim about the state of knowledge, not a measurement, and the "
     "sentence is a dead end he reports as a dead end. This is the honest shape "
     "of a negative result and the article can use it as one"),

    ("in this manner a simple lamp capable of giving any desired candle power "
     "is provided",
     177, "3. Tesla's lamp research (the ambition, a year and a half earlier)",
     "the largest claim this article's subject ever gets in the volume: a lamp "
     "of 'any desired candle power' from the same bombardment. It is in the New "
     "York lecture of May 1891, before the carborundum work, and it is the "
     "sentence the pp. 253-255 failure answers. 'candle power' (two words) is in "
     "the volume @@candlepower_spaced@@ times and 'candlepower' (one word) "
     "@@candlepower_closed@@ times (measured), so the unit is period and the "
     "spelling is not, and no number is attached to any of those hits. "
     "Quote the claim with 'any desired' in it; the hedge is the claim"),

    ("The success of lamps of this kind would depend largely on the selection "
     "of the light-giving bodies contained within the bulb",
     177, "3. Tesla's lamp research (he names the problem before he meets it)",
     "the design problem stated in 1891, in his own words: the lamp lives or "
     "dies by what is inside the bulb. That is exactly what the carborundum "
     "passage of 1892 is an attempt at, and the two sentences a year and a half "
     "apart are the whole plot of this article's third beat. 'Would depend "
     "largely' is a conditional about a future trial, not a result"),

    ("the better the vacuum the more easily the bodies are brought to "
     "incandescence",
     177, "4. The vacuum problem (the opposite of what the reader expects)",
     "the intuition is that a better vacuum means less to heat and so less "
     "light; he tested it and prints the contrary, and marks it as his own "
     "experience ('This is not confirmed by my experience; quite the contrary'). "
     "It belongs with the p. 288 'another tube might not light' moment and the "
     "p. 402 Torricellian failure: three different pages, one hard problem, and "
     "no solution in the volume"),
]

# ---------------------------------------------------------------------------
# Rejected: considered and not carried forward.
#
# Numbered, because 'Rejected #N' is cited from the rows above and an
# unnumbered list cannot answer one. The numbers are the order of this list in
# gen_quotes.py; nothing renumbers them. A row here is a string that was
# grepped and either does not verify (the measured outcome is stated), or
# verifies but must not be printed in this article (the reason is stated).
# ---------------------------------------------------------------------------
REJECTED = [
    ("Of all these phenomena observed with currents, or electric impulses, of "
     "high frequency, the most fascinating for an audience are certainly those "
     "which are noted in an electrostatic field acting through considerable "
     "distance; and the best an unskilled lecturer can do is to begin and "
     "finish with the exhibition of these singular effects",
     288,
     "the showmanship sentence, and the one brief 12's beat 1 is really echoing. "
     "It verifies at ratio 1.0, and it is already printed verbatim on "
     "tesla-lit-lamps-without-wires.html with a p. 288 cite (measured: the "
     "sibling-overlap table below reports which pinned fragments already appear "
     "on a live page). Article 01 owns it. The article may link to that page "
     "and describe the move, but it may not print the sentence again"),

    ("What change have I produced in the tube?",
     288,
     "the form books and quote-index.md section B print. It does NOT verify: "
     "the matcher returns only a fuzzy 0.987 window, because the print's "
     "question continues 'in the tube in the act of exciting it?'. The "
     "truncated form makes him ask a different, dumber question. Row 22 pins "
     "the real one"),

    ("I should think that to any experimenter who had carefully studied the "
     "problem confronting us and who attempted to find a solution of it, this "
     "idea must present itself as naturally as",
     396,
     "the tidied form of the obviousness sentence, with the print's stray comma "
     "after 'should' removed. It does not verify: fuzzy 0.995, and the missing "
     "half a character is the comma. Row 9 pins it as set. Either quote the "
     "comma or do not quote the clause; a silently corrected Tesla is the "
     "failure mode this whole file exists to stop"),

    ("the luminous effects, which are producible by induction in a tube devoid "
     "of electrodes, is of an electrostatic nature",
     175,
     "the trimmed version of the thesis sentence that drops 'I am inclined to "
     "consider as being'. It does not verify (the words 'is of an electrostatic "
     "nature' are not in the volume in that construction), and it turns a "
     "hedged opinion into a finding. Row 85 pins the hedged form, and the hedge "
     "is the point"),

    ("Electric Discharges in Vacuum Tubes 396",
     494,
     "the index entry with its folio attached. On the default index it comes "
     "back fuzzy 0.828, because strip_furniture drops the bare '396' the index "
     "sets on its own OCR line; with --keep-furniture it is 1.0. Row 10 pins "
     "the label without the number. A draft that wants the number has to say "
     "which index it used"),

    ("SOME EXPERIMENTS ON THE ELECTRIC DISCHARGE BY PROF. J. J. THOMSON",
     402,
     "the chapter's own display heading for the abstract. It is not in the "
     "index the gate uses, for the same reason as the row above: short all-caps "
     "lines are dropped as running heads. It is in the raw page body, so a "
     "reader who greps the file will find it and the gate will not. Name the "
     "abstract in prose instead of quoting a heading; see the flag THE CHAPTER "
     "TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE"),

    ("Further exhaustion of the jar caused the secondary discharge to appear "
     "outside of the bulb",
     403,
     "the corrected spelling of row 59. It does not verify: the OCR prints 'J "
     "urther' with a space after the capital J, and the space-ignoring index "
     "glues that to 'Jurther', which is not 'Further'. Row 59 carries the "
     "scan's letters. This one is a judgement call the draft has to make "
     "consciously, not by accident: print the scan or print the print"),

    ("an ordinary exhausted tube (preferably of large diameter) be surrounded "
     "by a spiral of thick copper wire serving as the primary, a feebly "
     "luminous spiral may be induced in the tube",
     399,
     "the joined form of row 40 with the cut removed. It does not verify: fuzzy "
     "0.967 on the pinned page, measured, and the reason is the scan, not the "
     "print: the OCR sets 'primary^ afeebly', a footnote marker glued to the "
     "next word, so no comma-and-space form of the sentence is in the index. "
     "Row 40 cuts around it with ' ...', which is what check_quotes.py will "
     "accept in the draft"),

    ("the circles were always in close proximity to the primary and were "
     "considerably easier produced when the latter was very close to the glass "
     "and these facts speak for an electrostatic effect",
     400,
     "the joined form of row 44. It does not verify: fuzzy 0.86, same cause, a "
     "figure label inside the run. Row 44 cuts"),

    ("The production of a small electrode, capable of withstanding enormous "
     "temperatures",
     258,
     "the sentence a retelling of the lamp section wants. It does not verify: "
     "fuzzy 0.844, because the OCR reads 'sniall' for 'small' and 'wit hstan< "
     "ling' for 'withstanding' inside it. Two scan defects in eight words. Also "
     "printed p. 258 is inside the passage article 06's page already quotes. "
     "Read the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT "
     "SILENTLY FIX"),

    ("recourse was had to the oscillatory discharge of a",
     402,
     "the top of the Leyden-jar sentence, which is on printed p. 402. It "
     "verifies alone at ratio 1.0, and it must not be quoted alone: the object "
     "of the preposition is the first words of printed p. 403, and the two "
     "halves never join in the index, because the page's own footnote sits "
     "between them in the page body and strip_furniture keeps footnotes. Row 60 "
     "pins the p. 403 half and says so"),

    ("An exhausted bulb, Fig. 217, containing traces of oxygen was placed "
     "within a primary spiral of three turns, and, on passing the jar "
     "discharge, a circle of light was seen within the bulb in close proximity "
     "to the primary circuit",
     403,
     "the cleaned form of row 62, with 'plaeed' repaired to 'placed' and "
     "'inclose' split to 'in close'. It does not verify: the scan really prints "
     "those letters, and the space-ignoring index can glue a space but cannot "
     "un-glue a wrong letter. Row 62 carries the scan and cuts around the worst "
     "of it. This is the ring-of-light sentence the popular story puts on "
     "Tesla, and it is Thomson's apparatus either way"),

    ("it was not until after six weeks' continuous experimenting",
     406,
     "verifies at ratio 1.0, and it is not his. It is J. J. Thomson describing "
     "his own Leyden-jar work inside the communication printed on p. 406. "
     "Rejected as an article-12 quote of Tesla's persistence, because every "
     "'Tesla worked six weeks' sentence on the internet is this sentence "
     "misattached. Row 79 pins it as Thomson's; read the flag THE SIX WEEKS "
     "BELONG TO THOMSON"),

    ("I take a tube in my hand and move it about, and it is lighted wherever I "
     "may hold it ... I may put it away for a few weeks or months, still it "
     "retains the faculty of being excited ... What change have I produced in "
     "the tube?",
     288,
     "the p. 288 block as quote-index.md section B prints it, three fragments in "
     "one quote. Rejected as one quote for two reasons: the last fragment is the "
     "truncated question of Rejected #2, and two of the three parts are already "
     "printed verbatim on article 01's page (measured). Quote the parts "
     "separately, each with its own citation, or link to article 01"),

    ("In one of the experiments this evening a brush was produced at the end of "
     "a wire",
     258,
     "the cold-flame opening, and article 06's page prints it verbatim with a p. "
     "258 cite (measured). It is a fine sentence and it is not this article's. "
     "Read the flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT"),

    ("we may place a body of some refractory material in a closed, and "
     "preferably more or less exhausted, globe, connect it to a source of high, "
     "rapidly alternating potential, causing the molecules of the gas to strike "
     "it many times a second at enormous speeds, and in this manner, with "
     "trillions of invisible hammers, pound it until it gets incandescent",
     175,
     "the 'invisible hammers' sentence as one continuous run. It does not "
     "verify: the printed line ends 'connect it to a source of' and the next "
     "glyph in the OCR is a stray bullet, so the run has a '•' inside it that no "
     "normaliser removes. Row 87 cuts at it with ' ...' and says the cut is a "
     "scan artefact, not an elision in the text"),

    ("powerful electrostatic eifects are a sitw qua -non of light production on "
     "the lines indicated by theory",
     175,
     "the strongest condition sentence in the New York lecture, and it verifies "
     "at ratio 1.0 only because the quote carries the scan's mangling: 'eifects' "
     "for 'effects' twice and 'sitw qua -non' for 'sine qua non'. Printed as "
     "set, a reader assumes the transcriber made the error; corrected, it does "
     "not verify. Paraphrase the condition and cite the page. Read the flag "
     "SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX"),

    ("It is evident that the efficiencv in such cases is the greater, the "
     "higher the frequency, for the quicker the process of charging and "
     "discharging the molecules, the less energy will be lost in the form of "
     "dark radiation",
     176,
     "the theory behind the efficiency sentence in row 91, and the best "
     "statement in the volume of why he thought high frequency made light. It "
     "verifies only because the quote carries 'efficiencv', which is what the "
     "scan prints for 'efficiency' in that sentence; the corrected form does not "
     "verify there. Rejected on that ground, not on its content. The row-92 "
     "quote stops before it for the same reason"),

    ("An intense phosphorescence then spreads at first over the globe",
     228,
     "does not verify: fuzzy 0.976. And printed p. 228 is inside 'Brush "
     "Phenomena in High Vacuum', the chapter section the volume's own index "
     "files at p. 226 (row 12 pins that index entry) and which article 06's "
     "page cites twice. Two independent reasons not to carry it"),

    ("In bulbs provided with a conducting terminal, though it be of aluminum",
     226,
     "verifies, and it is the brush-in-a-high-vacuum bulb, which is article 06's "
     "subject and its page's beat, not this one's. Rejected to keep the two "
     "pages apart; the volume's own index labels put them in different sections "
     "(row 12)"),

    ("It is now a fact that a body may be rendered incandescent or "
     "phosphorescent",
     236,
     "does not verify at all: no window clears the fuzzy floor anywhere in the "
     "volume. The sentence is a paraphrase remembered as a quote. If the article "
     "wants that claim it has to be written as prose, not inside quote marks"),

    ("I think that in a bulb a molecule, or atom, does not precisely move in a "
     "straight line",
     282,
     "does not verify at all (no match anywhere). The mean-free-path passage on "
     "printed p. 282 says something adjacent in different words, and 'mean free "
     "path' is in the volume @@meanfreepath@@ times (measured), so the "
     "mechanism is quotable - but not this sentence, and not from memory"),

    ("Any one who has studied Crookes' work must have received the impression "
     "that the ' radiant state ' is a property of the gas inseparably connected "
     "with the vacuum",
     282,
     "the outer clause verifies on its own, but the block cannot be quoted as "
     "one run: the print sets its own quote marks around ' radiant state ', and "
     "check_quotes.py's scanner pairs quote marks, so the inner pair ends the "
     "quote early and everything after it is mis-paired. Cut before the inner "
     "marks or drop the block. 'Radiant state' is Crookes' vocabulary, which is "
     "a second reason to be careful whose words are being printed"),

    ("A thought which early and naturally suggested itself to Mr. Tesla, was "
     "the possibility of producing light and heat by molecular bombardment",
     141,
     "does not verify: no match at all, and the sentence is the compiler's third "
     "person about him, not his writing. It is the shape every retelling uses "
     "and the reason this pin exists. The same idea in his own first person is "
     "row 87 and row 89"),

    ("it is conceivable that a person entirely nude at the North Pole might "
     "walk barefoot on the snow",
     395,
     "does not verify: no match at all. A remembered image from the "
     "high-frequency safety material; the real sentences there are article 01's "
     "p. 125 quote (read the flag ARTICLE 01 OWNS THE SAFETY SENTENCE)"),

    ("The eternal recipient and transmitter of this infinite energy is the "
     "ether.",
     145,
     "verifies, and article 01's page already prints it with a p. 145 cite "
     "(measured). It is also the sentence the free-energy myth feeds on, and "
     "article 10's page is the series' answer to that. Rejected here on both "
     "counts"),

    ("We are whirling through endless space with an inconceivable speed, all "
     "around us everything is spinning, everything is moving, everywhere is "
     "energy.",
     196,
     "the London lecture's closing flourish, carried in Appendix A and quote-"
     "index.md section L, and it straddles printed pp. 196-197 as one run. "
     "Nothing to do with a tube, and another page's to use. Listed so a writer "
     "reaching for a grand ending finds the reason not to"),

    ("Here is a simple glass tube from which the air has been partially "
     "exhausted. I take hold of it ; I bring my body in contact with a wire "
     "conveying alternating currents of high potential, and the tube in my hand "
     "is brilliantly lighted.",
     200,
     "the other tube-in-hand demo, from the same February 1892 lecture, printed "
     "verbatim on article 01's page with a p. 200 cite (measured). Article 01 "
     "is the page for that demonstration; this article's is the p. 288 one. "
     "Read the flag FOUR TEXTS, FOUR VOICES, ONE CHAPTER before writing a "
     "sentence that says 'he always opened with'"),

    ("tubes devoid of any electrodes may be used, and there is no difficulty in "
     "producing by their means sufficient light to read by",
     187,
     "verifies, and article 01's page prints it verbatim with a p. 187 cite "
     "(measured). It is also the closest thing in the volume to a brightness "
     "claim for an electrodeless tube, so if the draft wants it, it has to "
     "credit article 01 and link, not re-quote"),

    ("the observer may, standing upon an insulated support between coil and "
     "tube, light the latter by approaching the hand to it",
     186,
     "verifies, and article 01's page prints it verbatim with a p. 186 cite "
     "(measured). Row 92 pins a different sentence from the same printed page; "
     "read the flag ARTICLE 01 HAS THREE SENTENCES ON p. 186 AND p. 187"),

    ("the singular effect of wiping out the light of the tube may be produced by "
     "passing the hand quickly along the tube",
     186,
     "verifies, and article 01's page prints it verbatim with a p. 186 cite "
     "(measured). Same flag as the row above"),

    ("In all cases the insulated body serves to give off the energy into the "
     "surrounding space, and is equivalent to a return wire.",
     184,
     "verifies, and article 01's page prints it verbatim with a p. 184 cite "
     "(measured). Row 37 exists precisely so this article can point at that "
     "sentence in one clause instead of reprinting it"),

    ("X rays",
     None,
     "not a quote but a claim check, and the one brief 12 flags with 'needs "
     "source'. No spelling of it is in the volume: 'X-ray' @@xray_hyphen@@, 'X "
     "rays' @@xray_space@@, 'x ray' @@xray_lower@@, 'Röntgen' @@xray_umlaut@@, "
     "'roentgen' @@xray_plain@@ (measured, all three indices). Röntgen's paper "
     "was December 1895 and this volume's newest text is February 1892. There is "
     "nothing to quote, so the article must not imply a connection; read the flag "
     "THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895"),

    ("light without energy",
     None,
     "the phrase brief 12 item 5 says the internet gets wrong. It is not in the "
     "volume (@@lwe_count@@ hits, measured), so nobody in 1894 said it and it "
     "cannot be quoted at him. The correction has to be made against the modern "
     "phrase, with his own conservation sentence (row 27) as the counterweight"),

    ("the pleasure I have had in presenting these results to a gathering of so "
     "many able men - and among them also some of those in whose work for many "
     "years past I have found enlightenment and constant pleasure - I shall "
     "never forget",
     293,
     "the full closing sentence of chapter XXVII, carried in quote-index.md "
     "section L. It verifies at ratio 1.0 (the normaliser folds the dashes), and "
     "it cannot be printed: section 0 non-negotiable 5 forbids em and en dashes "
     "in series prose, and the print sets two pairs of them around a paren-"
     "thought. Row 34 pins the dash-free half, which is all a draft of this "
     "series can use"),
]

# ---------------------------------------------------------------------------
# Flags for the writer. Each is a rule about these sources, not advice about
# style: every one names the page or the measurement that produced it.
# ---------------------------------------------------------------------------
FLAGS = [
    ("FOUR TEXTS, FOUR VOICES, ONE CHAPTER",
     "Chapter XXXII, printed pp. 396-406, is not one text. The footnotes on the "
     "pages date four: Tesla's own article in The Electrical Engineer, N. Y., "
     "July 1, 1891 (row 1); an abstract of a paper read by Prof. J. J. Thomson "
     "to the Physical Society of London (the footnote on printed p. 402, and the "
     "heading Rejected #6); Tesla's reply in the same magazine, Aug. 26, 1891 "
     "(the footnote on printed p. 404); and Thomson's note in the London "
     "Electrician, July 24, 1891 (the footnote on printed p. 406). Two more "
     "texts this article quotes are whole chapters of their own: chapter XXVI, "
     "the New York lecture of May 20, 1891 (row 14), and chapter XXVII, the "
     "London lecture of February 1892 (row 13). So 'Tesla wrote it in 1894' is "
     "wrong six different ways: the volume is 1894, the texts are 1891 and 1892, "
     "and three of the passages in chapter XXXII are not by him. Every sentence "
     "in the draft that attributes something has to name which text and which "
     "man. The footnotes are the evidence and rows 1, 13, 14 pin them"),

    ("TWO THOMSONS IN ONE PARAGRAPH",
     "Printed p. 396 names J. J. Thomson and Elihu Thomson within two sentences "
     "(rows 3 and 4). J. J. is the Cambridge man whose abstract and note fill "
     "pp. 402-406; Elihu is the American, a different experiment, in a different "
     "magazine. The chapter's own prose says 'Prof. Thomson' unqualified, which "
     "in context means J. J. A draft sentence that says 'Thomson' without a "
     "first initial is ambiguous in exactly the way the source is not. Spell out "
     "which one, every time"),

    ("THE ABSTRACT IS THIRD PERSON AND THE PROSE IS FLUENT, WHICH IS THE TRAP",
     "The abstract on printed pp. 402-403 is reportage about Thomson's work in "
     "the third person ('the author had also observed', 'Prof. Thomson said'), "
     "and it reads like the surrounding prose, which is why it is so often "
     "quoted as Tesla's. Row 54, row 60, row 62, row 63 and row 64 are all "
     "inside it. The tell is grammar: 'he', 'the author', 'Prof. Thomson said' "
     "versus Tesla's 'I', 'my experiments', 'in my experiments they were broad'. "
     "Before any quote from pp. 402-406 goes in the draft, check which of the "
     "four texts it came from and whose pronouns it uses"),

    ("THE SIX WEEKS BELONG TO THOMSON",
     "The most-misquoted sentence in this article's sources: 'it was not until "
     "after six weeks' continuous experimenting that I was able to get a "
     "discharge in the exhausted tube which I was satisfied was due to what is "
     "ordinarily called electrodynamic action' (row 79). The 'I' is J. J. "
     "Thomson, in his own published note on printed p. 406, about his own "
     "Leyden-jar apparatus. Tesla's own bench time is dated differently, and by "
     "himself: 'My investigations in this line occupied me principally during the "
     "winter and spring of the past year' (row 2), relative to a July 1891 "
     "issue. If the article wants a duration, it has to say whose"),

    ("TWO MEN, ONE VOLUME, EACH SAYING THE OTHER MISREAD HIM",
     "Printed p. 404, Tesla: 'I did not, as Prof. J. J. Thomson seems to "
     "believe, misunderstand his position' (row 67). Printed p. 406, Thomson: "
     "'He seems, however, to have misunderstood my position' (row 81). Both "
     "sentences are in the volume, one page apart, and both are about the same "
     "question, which is whether the effect can be produced with electrostatic "
     "action EXCLUDED (Thomson's actual position, row 81) rather than whether it "
     "can be produced by it. Print the pair or print neither. A story where one "
     "of them wins is not supported by these pages"),

    ("THE RING OF LIGHT IS THOMSON'S, THE BROAD GLOW IS TESLA'S",
     "The popular drawing - a thin ring of light inside a bulb near a coil - is "
     "Thomson's observation, in his abstract, on printed p. 403 (row 62, 'a "
     "circle of light was seen within the bulb inclose proximity to the primary "
     "circuit, accompanied by a purplish glow, which lasted for a second or "
     "more'). Tesla's reply on printed p. 400 is a claim about a different "
     "appearance: 'in my experiments they were broad and often the whole of the "
     "bulb or tube was illuminated' (row 45). The two descriptions are in the "
     "same chapter and disagree. The article should say which drawing belongs to "
     "which man, because the retellings do not"),

    ("THE BRIEF'S FIG. 218 IS THOMSON'S APPARATUS",
     "Brief 12 shortlists Figs. 210, 212, 215 and 218. Fig. 218 is on printed p. "
     "403, inside the abstract, and the text beside it is Thomson's (rows 61-63 "
     "are the sentences on those pages). Fig. 216, on printed p. 402, is also "
     "Thomson's and is named in row 61 for exactly that reason. A caption that "
     "says 'Tesla's apparatus' under a crop from pp. 402-403 is a factual error "
     "about a figure the reader can see. Read the figure notes before writing "
     "any caption"),

    ("PRIORITY IN THIS CHAPTER IS ABOUT WHO PUBLISHED AND WHO NOTED",
     "He names the prior art himself: 'the luminosity in a tube near a wire "
     "through which a Leyden jar was discharged was noted by Hittorf' (row 76, "
     "printed p. 405, and 'Hittorf' is in the volume @@hittorf_count@@ time, "
     "there). And his own claim is about intensity, not firstness: 'been noted by "
     "many experimenters, but in my experiments the effects were much more "
     "powerful than those usually noted' (row 77). Plus the disclaimant on "
     "printed p. 396: 'The idea being obvious, whatever merit there is in this "
     "line of investigation must depend upon the completeness of the study' (row "
     "7). The article may say his effects were stronger and that he said so. It "
     "may not say he discovered it"),

    ("HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS",
     "Four admissions, in four different texts, all in this pin: 'For want of "
     "time I have, however, not been able to perform the experiment' (row 53, "
     "printed p. 401); 'the experimental verification of the law, whatever it may "
     "be, would be exceedingly difficult' (row 94, printed p. 213); 'The time has "
     "been too short to make a satisfactory study of the properties of this "
     "product' (the carborundum row, printed p. 254); and 'I have now almost "
     "finished writing out, and hope very shortly to publish, an account of these "
     "and a large number of allied experiments' (row 84 - which is Thomson's, and "
     "the promised account is not in this book). Any claim the draft reports as "
     "his finding should be checked against these four first"),

    ("HE TRIED TO SCREEN IT OUT AND THE SCREENING FAILED",
     "The discriminating tests are in the sources and they cut both ways. Tesla: "
     "a glass tube T slipped between primary and bulb changes the effect, 'were "
     "the action wholly electromagnetic no change could possibly have been "
     "observed' (row 49); a closed wire round the bulb does not stop the light "
     "(row 51); a broad tinfoil strip does (row 52). Thomson: a wet blotting-"
     "paper screen to earth, which stops a stationary electrostatic effect and "
     "does not stop alternating electromotive waves (row 78), and his criticism "
     "that the published account did not show 'all possible precautions had been "
     "taken to exclude these effects' (row 68). Tesla's own answer is that he saw "
     "'curious instances of the ineffectiveness of the screening' (row 69). The "
     "article should present the screening argument as the live disagreement it "
     "was, not as Tesla having proved the point"),

    ("HE ANSWERS HIS OWN QUESTION ON THE NEXT PAGE AND NOBODY QUOTES IT",
     "Printed p. 288 he asks 'What change have I produced in the tube in the act "
     "of exciting it?' (row 22) and weighs two answers, motion in atoms and "
     "strain in the dielectric, rejecting both for stated reasons (rows 23, 24). "
     "Printed p. 405, in the reply to Thomson, he sketches the mechanism that "
     "dissolves the question: one instantaneous flash if the charge is "
     "stationary, permanent excitation if it keeps moving, because 'a constant "
     "redistribution of electricity' keeps colliding the gas molecules (row 72). "
     "It is a thought experiment, and he marks it as one ('Assuming', 'suppose'). "
     "The honest ending for beat 5 is that the question was asked in 1892, and "
     "an answer of a kind was printed in 1891 and never run as a test"),

    ("SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX",
     "Measured inside this article's own quotes: 'vaciium' for 'vacuum' (row 64, "
     "printed p. 402), 'plaeed' for 'placed' and 'inclose' for 'in close' (row "
     "63, p. 403), 'viorate' for 'vibrate' (row 89, p. 176), 'Avill' for 'Will' "
     "and 'II. S. A.' for 'U. S. A.' (the two carborundum rows, p. 253), "
     "'efficiencv' for 'efficiency' (Rejected #18, p. 176), 'eifects' and 'sitw "
     "qua -non' (Rejected #17, p. 175), 'f rictional' with a space after the f "
     "(row 23, p. 288), 'J urther' (row 59, p. 403), 'eparate' for 'separate' "
     "(row 82, p. 406), 'sniall' and 'wit hstan< ling' (Rejected #10, p. 258). "
     "The rule this pin uses: a quote carries the scan, and where the scan is "
     "unreadable the quote is cut or the sentence is paraphrased and cited. What "
     "is not allowed is a silently corrected 1894, because the reader cannot "
     "check it and the gate cannot check it either - the matcher fails on the "
     "corrected form"),

    ("THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE",
     "The chapter's display heading and the contents-page line do not verify on "
     "the index the gate uses, because strip_furniture drops short all-caps "
     "lines as running heads (Rejected #6). What does verify is the volume's own "
     "index label, 'Electric Discharges in Vacuum Tubes' (row 10, printed p. "
     "494), and the first words of the chapter's own first sentence (row 3). If "
     "the draft names the chapter, it names it the way the index does, without a "
     "page number, or it does not put the name in quote marks"),

    ("ARTICLE 01 OWNS THE p. 288 SENTENCES IT HAS ALREADY PRINTED",
     "Measured, not remembered: the sibling-overlap table below checks every "
     "fragment in this pin against the rendered text of the live series pages. "
     "Article 01's page prints the showmanship sentence (Rejected #1), 'I may put "
     "it away for a few weeks or months, still it retains the faculty of being "
     "excited' (row 21) and 'What change have I produced in the tube in the act "
     "of exciting it?' (row 22), all cited to p. 288. Rows 21 and 22 are pinned "
     "here because brief 12 item 1 quotes them, and the article cannot raise the "
     "question without the question sentence. So: use them, but say they are the "
     "same passage article 01 has, and link to that page. The one p. 288 sentence "
     "article 01 has NOT printed is the hook, row 18"),

    ("ARTICLE 01 HAS THREE SENTENCES ON p. 186 AND p. 187",
     "Measured from the rendered page: article 01 quotes two sentences from "
     "printed p. 186 (the insulated-support sentence and the wiping-out-the-light "
     "sentence, Rejected #29 and #30) and one from p. 187 (the read-by sentence, "
     "Rejected #28). Row 92 pins a fourth sentence from p. 186, the one that "
     "says the tube is lighted by condenser action, and that one is free. The "
     "page is shared; the sentences are not. Do not put two article-01 sentences "
     "and this one in the same paragraph as if they were one passage"),

    ("ARTICLE 01 OWNS THE SAFETY SENTENCE",
     "The p. 125 sentence about physiological effects being small is on article "
     "01's page with its own caution attached. Row 90 pins a different "
     "observation, from the New York lecture of May 1891: at low frequency a "
     "four-foot tube with condenser coatings gives a shock he thinks could do "
     "'serious injury to those not accustomed to such shocks', and at twenty "
     "thousand alternations per second the same brightness is felt as nothing. "
     "The two are not the same claim and must not be blended into one sentence "
     "about safety. Neither is a safety instruction for a reader at home"),

    ("ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT",
     "Measured from the rendered page: article 06's page prints the brush-flame "
     "sentences at printed pp. 258-259, and it prints the p. 213 law ('the heat "
     "as well as light effects produced should be proportionate, under otherwise "
     "equal conditions of test, to the product of frequency and square of "
     "potential') and the first clause of the p. 213 hedge. Rows 93 and 94 are "
     "pinned here because the law is the best evidence in the volume that he "
     "wanted a controlled test and said he had not done it. If the draft uses "
     "them it must say the series' cold-flame page has them too, and link. The "
     "volume's own index also splits the two subjects: 'Brush Phenomena in High "
     "Vacuum' at p. 226 (row 12) is article 06's, 'Electric Discharges in "
     "Vacuum Tubes' at p. 396 is this one's"),

    ("THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895",
     "Brief 12 flags an X-ray connection as 'needs source: do not assert without "
     "a citation'. There is no citation, because the words are not there: "
     "'X-ray' @@xray_hyphen@@ hits, 'X rays' @@xray_space@@, 'x ray' "
     "@@xray_lower@@, 'Röntgen' @@xray_umlaut@@, 'roentgen' @@xray_plain@@, "
     "measured on all three indices. And the volume says its own limit: 'The "
     "present volume deals simply with his work accomplished to date' (row 15, "
     "printed p. 6), with the compiler adding that work in progress is being held "
     "back (row 16). The newest text this article quotes is February 1892. So the "
     "absence of X-rays from these chapters is not a finding about Tesla's "
     "foresight either way; it is a date fence. Do not write 'he never saw "
     "X-rays' as a fact about him, and do not write 'he anticipated them'"),

    ("THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO NOT MEAN WHAT THE QUERY MEANS",
     "Measured: 'vacuum tube' is in the volume @@vt_vol@@ times, and inside "
     "chapter XXXII alone @@vt_ch32@@ times (printed pp. 396, 403, 404). It does "
     "not mean a thermionic valve: it means a tube exhausted of air, and the "
     "period's usual phrase is 'exhausted tube' (@@et_vol@@ hits). 'capacitor' "
     "is @@cap_count@@, and the component he reasons with is a 'condenser' "
     "(@@condenser_count@@ hits). 'electron' is @@electron_count@@, 'watt' "
     "@@watt_count@@, 'candlepower' @@cp_closed@@ though 'candle power' as two "
     "words is @@cp_spaced@@, 'ionis' @@ion_count@@, 'ultraviolet' @@uv_count@@, "
     "'free energy' @@fe_count@@. A reader searching 'tesla vacuum tube "
     "experiment' wants 1904, and this book is 1891-1892. The article should say "
     "what the words meant then, and not let the modern word stand unexplained"),

    ("NO NUMBER IN THIS ARTICLE'S SUBJECT, AND THE ABSENCE IS THE CLAIM",
     "Measured over chapter XXXII, printed pp. 396-406: 'test' @@test_ch32@@, "
     "'efficiency' @@eff_ch32@@, 'per cent' @@pc_ch32@@, 'watt' @@watt_ch32@@, "
     "'candle power' @@cp_ch32@@, 'volts' @@volts_ch32@@, 'ampere' "
     "@@amp_ch32@@, 'output' @@out_ch32@@, 'commercial' @@comm_ch32@@, "
     "'measure' @@meas_ch32@@, 'striae' @@striae_ch32@@, 'Geissler' "
     "@@geissler_ch32b@@, 'X-ray' @@xray_ch32@@. Over the carborundum passage, "
     "printed pp. 253-259: 'efficiency' @@eff_lamp@@, 'per cent' @@pc_lamp@@, "
     "'watt' @@watt_lamp@@, 'candle power' @@cp_lamp@@, 'volts' @@volts_lamp@@, "
     "'ampere' @@amp_lamp@@, 'output' @@out_lamp@@, 'cost' @@cost_lamp@@, 'life' "
     "@@life_lamp@@, 'hours' @@hours_lamp@@. What those chapters do contain is "
     "the word 'experiment' @@exp_ch32@@ times in chapter XXXII and @@exp_lamp@@ "
     "times in the lamp passage, and comparative sentences with no numbers on "
     "them. So the article may write: he described apparatus and comparisons and "
     "printed no measurement of the light. It may not write that he failed to "
     "measure something he never claimed to have measured, and it may not print a "
     "figure of its own inventing one"),

    ("THE BRIEF'S FIGURE NAMES ARE PRINTED PAGES AND THE FILES ON DISK ARE SCAN "
     "FILES",
     "Brief 12 lists 'tesla1894-p400-fig215', 'p403-fig218', 'p403-fig212', "
     "'p397-fig210'. None of those four file names exists. The extractor names "
     "its crops by SCAN file, and printed page = scan file - 18, so the real "
     "files are p415-fig1-fig210 (printed 397), p416-fig1-fig212 and "
     "p416-fig2-fig212 (printed 398), p418-fig1-fig215 and p418-fig2-fig215 "
     "(printed 400), p421-fig1-fig218 (printed 403). The figure notes below "
     "enumerate what is actually on disk and in the two manifests. This is the "
     "same trap article 08's whole-pin pass hit at pp. 480-482"),
]

# ---------------------------------------------------------------------------
# Reading the site: the live sibling pages, and the figure crops on disk.
#
# These are defined before the notes below because those notes interpolate what
# is actually on disk and actually published, at generation time, rather than
# what a previous pass remembered. Article 08's whole-pin pass is the reason:
# it was written against file names that did not exist.
# ---------------------------------------------------------------------------
SITE = ROOT / "website"

# The series pages that are live at generation time, from the site directory.
LIVE_PAGES = [
    "tesla-lit-lamps-without-wires.html",        # 01, the 1891 demo page
    "tesla-one-wire-power.html",                 # 02
    "tesla-earthquake-machine.html",             # 03
    "tesla-wireless-power-1893.html",            # 04
    "tesla-high-frequency-massage.html",         # 05
    "tesla-cold-flame.html",                     # 06, the brush / flame page
    "rotating-magnetic-field-1888.html",         # 07
    "tesla-weird-inventions-1894.html",          # 08
    "tesla-worlds-fair-1893.html",               # 09
    "tesla-free-energy-what-he-said.html",       # 10, the trust piece
]

# Terms counted on each live page, to answer 'does another page already use
# this word or this man's name' before the draft decides it must.
LIVE_TERMS = ["vacuum tube", "glowing", "Geissler", "cold flame", "X-ray",
              "free energy", "capacitor", "exhausted tube", "carborundum",
              "J. J. Thomson", "Thomson", "(1894, p."]


def strip_tags(html_text: str) -> str:
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html_text)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return " ".join(html.unescape(t).split())


def live_page_data():
    """(name, words, term counts, 1894 page citations) for each live page."""
    out = []
    for name in LIVE_PAGES:
        path = SITE / name
        if not path.exists():
            out.append((name, None, [], []))
            continue
        text = strip_tags(path.read_text(encoding="utf-8", errors="replace"))
        counts = [(t, text.lower().count(t.lower())) for t in LIVE_TERMS]
        cites = {}
        for mt in re.finditer(r"\(1894, (?:pp?\.)\s*(\d+)(?:\s*-\s*\d+)?\)",
                              text):
            cites[mt.group(1)] = cites.get(mt.group(1), 0) + 1
        out.append((name, len(text.split()), counts,
                    sorted(cites.items(), key=lambda kv: int(kv[0]))))
    return out


def figure_crops(lo, hi):
    """Crops on disk that touch a printed-page range, read out of the site.

    manifest.csv names the extractor crops and gives their printed page; the
    500 ppi re-crops are appended to manifest_qc.csv only, and are named by
    PRINTED page where the extractor files are named by SCAN file (article 08's
    whole-pin pass hit exactly this, and brief 12's figure shortlist names its
    four crops by printed page too). A figure note that reads one manifest gets
    the number wrong both ways, so this reads the directory and both manifests
    and says which kind each file is.
    """
    d = SITE / "assets" / "tesla1894"
    man, qc = {}, {}
    for path, store in ((d / "manifest.csv", man), (d / "manifest_qc.csv", qc)):
        if path.exists():
            for r in csv.DictReader(path.open(encoding="utf-8", errors="replace")):
                if r.get("file"):
                    store.setdefault(r["file"], r)
    found = []
    for p in sorted(d.glob("p[0-9]*.webp")):
        mt = re.match(r"p(\d+)-", p.name)
        if not mt:
            continue
        n = int(mt.group(1))
        if p.name in man:
            pp = int(man[p.name]["printed_page"])
            kind = f"extractor crop, manifest.csv row {n}->{pp}"
            named_by = "scan file"
        else:
            pp = n
            kind = ("re-crop, manifest_qc.csv only" if p.name in qc
                    else "on disk, in neither manifest")
            named_by = "printed page"
        if not (lo <= pp <= hi):
            continue
        verdict = qc.get(p.name, man.get(p.name, {})).get("verdict") or \
            qc.get(p.name, {}).get("verdict", "")
        found.append(f"{p.name} (printed p. {pp}; named by {named_by}; {kind}"
                     + (f"; QC verdict {verdict}" if verdict else "") + ")")
    return found


# ---------------------------------------------------------------------------
# Notes for the figure task (feature-006/t6, a12-figrec). Read the existing
# record before re-opening anything; only re-open what is missing or contradicted.
# ---------------------------------------------------------------------------
FIGURE_NOTES = [
    f"Crops touching printed pp. {CH32[0]}-{CH32[1]} and the lamp passage, read "
    "out of the site directory and both manifests at generation time (the "
    "extractor names by scan file, the re-crops by printed page, which is why "
    "one list is not enough): " + "; ".join(figure_crops(CH32[0], CH32[1])) +
    ". The brief's four names are printed pages, not file names; see the flag "
    "THE BRIEF'S FIGURE NAMES ARE PRINTED PAGES AND THE FILES ON DISK ARE SCAN "
    "FILES",

    "FIG. 210, printed p. 397, is the one figure in the shortlist whose own "
    "description is quotable from the same page: 'Fig. 210 may serve as an "
    "example of one of the many forms of apparatus used. This consisted of a "
    "large glass tube sealed at one end and projecting into an ordinary "
    "incandescent lamp bulb' (row 36). Caption from the text beside the crop, "
    "figure number read off the print, per section 6.6. The QC row already on "
    "file says keep, subject 'Vacuum lamp with an internal cylindrical element "
    "on a stem', quality A, caption_ok yes - read it before re-rendering the "
    "page",

    "FIG. 212, printed p. 398, has TWO bands on disk (p416-fig1 and "
    "p416-fig2). The QC rows say: fig1 keep, quality B, 'Thin band; usable "
    "full-width only'; fig2 keep, quality C, caption_ok no, 'Dark plate - "
    "negate; low illustrative value'. If the article uses 212 it uses fig1, "
    "full width, and says what the circuit diagram shows in the caption rather "
    "than letting a thin band float",

    "FIG. 215, printed p. 400, also has TWO bands. The QC rows call fig1 a dark "
    "plate with 'subject ambiguous, verify against p.400 text before use' and "
    "fig2 'A spiral coil wound round a cylinder with a vacuum lamp suspended "
    "inside, leads P and P1', quality A, 'Clean; good lamp inside a coil "
    "illustration'. The text that matches fig2 is row 40, on printed p. 399: "
    "'an ordinary exhausted tube (preferably of large diameter) be surrounded by "
    "a spiral of thick copper wire serving as the primary ... feebly luminous "
    "spiral may be induced in the tube' (the scan sets 'primary^ afeebly', so "
    "the quote starts the second fragment at 'feebly'; read row 40). Use fig2. "
    "The QC note's 'verify "
    "against p.400 text' is answered by that row, and 'feebly' is the word the "
    "caption should carry, not 'blazing'",

    "FIG. 216 (printed p. 402) and FIG. 218 (printed p. 403) are THOMSON'S "
    "apparatus, inside the abstract (rows 61, 62, 63; read the flag THE BRIEF'S "
    "FIG. 218 IS THOMSON'S APPARATUS). The QC row for p420-fig1-fig216 already "
    "notes 'OCR FIG. 2V is a mis-read; two book figures in one band' and "
    "caption_ok no. If either is used, the caption names J. J. Thomson and the "
    "abstract, and the alt text says so too",

    "The lamp passage has its own figures, which the brief does not list but "
    "beat 3 might want: the carborundum button apparatus is described on printed "
    "pp. 254-255 and the Crookes radiometer-type apparatus at printed p. 176 "
    "(Fig. 114, Fig. 115, named in the text beside them). Check the manifest "
    "before promising any of them; nothing in this pin has verified a lamp "
    "figure against a scan, and the figure task must not caption an unviewed "
    "crop",
]

# ---------------------------------------------------------------------------
# Links (SERIES-PLAN-1894.md section 5.2 row 12, for feature-006/t5 and
# a12-wirecommit). Measured against the site as it stands at generation time.
# ---------------------------------------------------------------------------
LINK_NOTES = [
    "Section 5.2 row 12: article 12 links out to `free-electricity-from-"
    "magnets.html`, `electricity-using-magnets.html`, article 01 and article 06, "
    "and must be linked from 01, 06 and the hub. Four out-links is the minimum "
    "the plan sets; the two money pages are the bridge brief 12 item 6 asks for",

    "Measured on the date above: neither `tesla-lit-lamps-without-wires.html` "
    "nor `tesla-cold-flame.html` contains a link to `tesla-glowing-tubes-"
    "vacuum.html` yet (@@backlink_count@@ occurrences of the file name across "
    "the whole site). The in-links the plan requires do not exist until the "
    "wiring task adds them, and qa_page.py's dead-link gate is the thing that "
    "will catch a link added before the page exists. Add the page first, then "
    "the backlinks, in one commit",

    "The bridge to the free-energy pages is legitimate only through his own "
    "conservation sentence: 'no consumption of material, but merely a transfer of "
    "energy' (row 95) and 'it was necessary to economize the energy which is "
    "obtained from the field' (row 27). Article 10's page is the series' trust "
    "piece on what the book does and does not say about free energy, and 'free "
    "energy' is @@fe_count2@@ in the volume (measured). Do not let a p. 289 "
    "sentence sit next to a modern energy claim in a way that makes the book "
    "endorse it",

    "Article 01 is the page for the 1891 New York demonstration and the p. 184 "
    "return-wire explanation (Rejected #31, and row 37 links rather than "
    "re-quotes). Article 06 is the page for the brush and the cold flame and it "
    "already prints the p. 213 law (read the flag ARTICLE 06 OWNS THE COLD FLAME "
    "AND THE p. 213 LAW WITH IT). Every overlap this pin found is listed in the "
    "sibling-overlap table below; the draft should link at each one instead of "
    "reprinting",

    "Canonical URL `/tesla-glowing-tubes-vacuum`, file `tesla-glowing-tubes-"
    "vacuum.html` (section 5.1 row 12). The plan's note is explicit: "
    "`/tesla-glowing-tubes-before-tubes` only makes sense as an alias and an "
    "alias costs a hop; prefer the file name and write no `_redirects` rule. "
    "tid `1894_12`, FAQ schema yes, 1,300 words (section 9 brief 12)",
]

# ---------------------------------------------------------------------------
# The vocabulary. Every count in the prose above and in the flags is one of
# these rows, interpolated at render time; none of them is typed by hand.
#
# Three indices, because the answer depends on which one you use and this
# article's evidence is a count as much as a quote:
#   RAW   - a plain case-insensitive substring count over the raw OCR page
#           bodies, exactly what `grep -io` on the text file would say;
#   GATE  - grep_quote.build_index(clean=True), the index check_quotes.py
#           builds by default, i.e. the one the draft will be judged against;
#   KEEP  - the same index with --keep-furniture, which keeps running heads,
#           bare folios and short all-caps display lines.
# The normaliser folds case and a hyphen at a line break, which is why GATE
# and RAW differ for some terms; the file prints both rather than choosing.
# ---------------------------------------------------------------------------
TABLE_TERMS = [
    ("exhausted tube", "the period's ordinary phrase for what the brief calls a "
     "'vacuum tube' / 'Geissler tube'; the phrase the draft should use in "
     "quotes, because it is what the book says"),
    ("vacuum tube", "the modern phrase, and it IS in the book - but as 'a "
     "vacuum tube' meaning an exhausted glass envelope, not a valve. Read the "
     "flag THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO NOT MEAN WHAT THE QUERY "
     "MEANS"),
    ("Geissler", "brief 12 item 1's word. It is in the book, four times in the "
     "1891 New York lecture and once elsewhere, and never in chapter XXXII"),
    ("glowing", "the word in this article's own title. The book does not use "
     "it; it says 'luminous', 'luminosity', 'glow'. The title is ours, and the "
     "draft must not put the word in quote marks as if it were his"),
    ("glow", "the noun the book does use, including in the two glow sentences "
     "this pin pins (p. 403 Thomson's, p. 400 Tesla's)"),
    ("purplish", "the colour word in both of those glow sentences. Counted here "
     "because the row that quotes it claims the two occurrences are one in "
     "chapter XXXII his and one Thomson's - see the flag THE RING OF LIGHT IS "
     "THOMSON'S, THE BROAD GLOW IS TESLA'S"),
    ("luminous", "the book's adjective for what the brief calls 'the glow'"),
    ("luminosity", "the book's noun for the effect; chapter XXXII's own first "
     "sentence is about it (row 3)"),
    ("luminescence", "not in the volume at all, though it is the period's word "
     "in English physics papers; he says 'luminosity' and 'phosphorescence'"),
    ("phosphorescence", "the word for the light that persists after the "
     "excitation stops, and the word the carborundum question turns on"),
    ("phosphorescent", "the adjective form, used of the coated bulbs and of the "
     "sulphide of zinc experiments"),
    ("electric discharge", "the chapter's own subject phrase; the volume's index "
     "files it as 'Electric Discharges in Vacuum Tubes 396' (row 10)"),
    ("electrostatic", "the word the whole 1891 argument is about, in both "
     "directions; chapter XXVI alone is dense with it"),
    ("condenser", "the component he reasons with, in the period's word; the "
     "Leyden-jar and insulated-body argument of chapter XXXII is built on it"),
    ("condenser action", "the exact phrase brief 12 item 2 asks for, and the "
     "one sentence that uses it as an explanation is in the New York lecture "
     "(row 92)"),
    ("capacitor", "brief 12 item 2's word. Not in the volume in any spelling. "
     "The physics is his, the word is ours"),
    ("molecular bombardment", "the mechanism phrase, used by him and by the "
     "compiler; the first-person sentences are in chapter XXVI and XXVII"),
    ("bombard", "the verb family, across the whole book"),
    ("invisible hammers", "the image brief 12 item 3 quotes; once in the volume, "
     "at printed p. 175"),
    ("trillions", "the number in that image - and it is the only 'trillions' in "
     "the book, so it is rhetoric, not a count"),
    ("striae", "brief 12 item 5's word for the bands. In the book three times, "
     "never in chapter XXXII; the quotable striae sentence is in the New York "
     "lecture at printed p. 186 (row 92)"),
    ("stratification", "the same phenomenon in Thomson's reported speech, p. 402 "
     "(row 61)"),
    ("stratifications", "the plural, in the one sentence that says they were "
     "ABSENT (row 61)"),
    ("after-glow", "the persistence of the light, once in the volume, in the "
     "sentence this pin pins at p. 402 (row 46)"),
    ("non-striking", "brief 12 item 4's term of art for the vacuum that will "
     "not striate; his own method for beating it is at printed p. 175 (row 88)"),
    ("Hittorf", "the prior art he concedes on printed p. 405 (row 76); once in "
     "the volume, and it is his sentence, not the compiler's"),
    ("six weeks", "the duration the internet gives Tesla. Once in the volume, on "
     "printed p. 406, and the 'I' is J. J. Thomson (row 79)"),
    ("mean free path", "the physics he reaches for at printed p. 282 and in the "
     "New York lecture; the reason Rejected #21 matters"),
    ("carborundum", "the lamp material of brief 12 item 3; the passage is the "
     "densest in the book"),
    ("diamond", "the comparison material, in the same passage"),
    ("diamond dust", "the specific thing he tried, once in the volume, at "
     "printed p. 255"),
    ("candle power", "the period's brightness unit, as two words; brief 12 "
     "item 3's 'any desired candle power' is in the New York lecture"),
    ("candlepower", "the modern closed spelling. Not in the volume"),
    ("efficiency", "the word he does use, including in the one sentence that "
     "says his lamp showed 'no appreciable waste of energy' (row 91) - and "
     "never with a number"),
    ("per cent", "the unit an efficiency claim would need. Five hits, none in "
     "this article's chapters"),
    ("watt", "the unit a lamp output claim would need. Not in the volume"),
    ("electron", "the particle the mechanism would need. Not in the volume; "
     "Thomson's corpuscle paper is 1897"),
    ("ionis", "the ionisation word family. Once in the volume"),
    ("ultraviolet", "not in the volume"),
    ("X-ray", "brief 12's flagged 'needs source' item. Not in the volume; see "
     "the flag THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895"),
    ("X rays", "the two-word period form, as Röntgen's own paper was titled in "
     "English. Not in the volume"),
    ("x ray", "the lower-case form, counted separately so a reader can see the "
     "zero is not a capitalisation artefact"),
    ("Röntgen", "the discoverer's name. Not in the volume, in any spelling"),
    ("roentgen", "the same name unaccented, counted separately"),
    ("free energy", "the phrase article 10 exists to correct. Not in the volume"),
    ("light without energy", "the modern phrase brief 12 item 5 says is wrong. "
     "Not in the volume, so it cannot be quoted at anyone in 1894"),
    ("test", "the word a 'he measured it' story needs. In the volume constantly "
     "and in chapter XXXII not once; see the scoped table"),
    ("experiment", "what those chapters do contain, by the hundred"),
    ("excite it by means", "the exact phrase of the p. 288 question sentence "
     "(row 22); once in the volume, which is why the truncated form in "
     "Rejected #2 is a different sentence"),
    ("without wires", "article 01's title phrase. In the volume five times, "
     "never in chapter XXXII"),
    ("cold flame", "article 06's title phrase. Not in the volume in any form - "
     "he says 'brush' and 'flame' separately"),
    ("brush", "the book's word for the discharge at a wire end, which is what "
     "article 06 is about"),
    ("end of the wire", "the phrase the brush sentences use"),
    ("torricellian", "the vacuum standard he reports failing to reach at "
     "printed p. 402 (row 47)"),
    ("Ruhmkorff", "the induction coil by its usual period name; once in the "
     "volume, and he mostly says 'induction coil' or 'disruptive discharge "
     "coil'"),
    ("induction coil", "the apparatus phrase, across the whole book"),
    ("Crookes", "the prior experimenter he argues against on printed p. 282 and "
     "elsewhere"),
    ("no consumption of material", "the conservation sentence of the gas-lamp "
     "argument (row 95); once in the volume"),
    ("economize the energy", "the p. 289 sentence about the same subject (row "
     "28)"),
    ("energy which is obtained", "the rest of that p. 289 sentence"),
]

# The strings the book actually sets, inside the quotes this pin carries. The
# point of measuring them is not the count but the fact that each one is a
# specific, locatable defect rather than a general warning.
EXTRA_TERMS = [
    ("vaciium", "printed p. 402, inside row 64's quote"),
    ("plaeed", "printed p. 403, inside row 62's quote"),
    ("inclose proximity", "printed p. 403, inside row 62's quote. 'inclosed' is "
     "the book's ordinary word and it is spelled right eleven times; this one "
     "instance is the book's own error, not the scan's"),
    ("to eparate", "printed p. 406, inside row 82's quote: the book drops the "
     "leading 's'"),
    ("viorate", "printed p. 176, inside row 89's quote"),
    ("efficiencv", "printed p. 176, the sentence Rejected #18 quotes"),
    ("eifects", "printed pp. 169, 175 (twice), 176 - a recurring OCR failure, "
     "not a one-off"),
    ("sitw qua", "printed p. 175, for 'sine qua non'; 'sine qua non' itself is "
     "0 in the volume, which is how you can tell the phrase is the scan's and "
     "not his"),
    ("f rictional", "printed p. 288, inside row 23's quote; the same pattern of "
     "a space after a first letter appears again at p. 341"),
    ("J urther", "printed p. 403, inside row 59's quote"),
    ("sniall", "printed p. 258, Rejected #10"),
    ("Avill", "printed p. 253, inside the carborundum row's quote"),
    ("II. S. A.", "printed p. 253, for 'U. S. A.', same sentence"),
    ("NonConsuming", "printed p. 494, the volume's own index entry 'Flames, "
     "Electrostatic, NonConsuming 166, 272' - the index hyphen is lost in the "
     "scan, which is why the index entry cannot be quoted as furniture"),
    ("Carborundum Button for Tesla Lamps", "printed p. 494, the volume's own "
     "index entry for the lamp passage, filing it at 140 and 253 - the second "
     "of those is this article's page, the first is the compiler's chapter"),
]

# The scoped absence table. This is the evidence for the flag NO NUMBER IN THIS
# ARTICLE'S SUBJECT, AND THE ABSENCE IS THE CLAIM, and it is the reason brief
# 12's 'no efficiency figure' beat can be written at all.
SCOPED_RANGES = [
    ("ch. XXXII 396-406", CH32),
    ("lamp passage 253-259", LAMPS),
    ("ch. XXVI 145-197", CH26),
    ("ch. XXVII 198-293", CH27),
]
SCOPED_TERMS = [
    ("test", "a 'he tested it' story needs this word in the passage it is "
     "describing"),
    ("experiment", "what the passages are actually full of"),
    ("efficiency", "brief 12 item 3's 'no efficiency figure'"),
    ("per cent", "the unit such a figure would be written in"),
    ("watt", "the unit an output figure would be written in"),
    ("candle power", "the brightness unit the period did have"),
    ("volts", "an electrical measurement he had instruments for"),
    ("ampere", "the other one"),
    ("output", "the quantity a lamp claim would state"),
    ("cost", "the commercial claim the compiler's chapter at p. 140 makes and "
     "the lecture does not"),
    ("life", "as in 'lamp life', the durability claim brief 12 item 3's "
     "diamond-dust sentence is about"),
    ("hours", "the unit of that claim"),
    ("measure", "the verb itself"),
    ("commercial", "the adjective the compiler uses and the lecturer does not"),
    ("energy", "the word brief 12 item 5's 'capacitively coupled' sentence is "
     "about. Chapter XXXII does not use it once in nine pages"),
    ("striae", "brief 12 item 5's word"),
    ("stratification", "the same thing in Thomson's words"),
    ("after-glow", "the persistence he does discuss"),
    ("Geissler", "brief 12 item 1's tube"),
    ("X-ray", "brief 12's flagged item"),
    ("vacuum tube", "the modern phrase"),
    ("exhausted tube", "the period phrase"),
    ("phosphorescence", "the light he is describing"),
    ("carborundum", "the lamp material"),
    ("electrode", "the thing his tubes do not have"),
    ("without wires", "article 01's phrase for the same demonstration"),
    ("brush", "article 06's subject"),
    ("condenser", "the component in the chapter's own argument"),
    ("electrostatic", "the question the chapter is arguing about"),
    ("luminous", "the book's word for the light"),
]


def raw_window(body: str, frag: str, span: int = 200) -> str:
    """Show the scan's own text around a fragment.

    Same method as the article 02/04/05/06/08/10 generators: the anchor is the
    longest literal run of the fragment the raw page really contains, so the
    quoted fragment always sits inside the window shown.
    """
    words = frag.split()
    tries = ([words] + [words[:n] for n in range(len(words) - 1, 2, -1)]
             + [words[i:i + 4] for i in range(len(words) - 3)])
    for seq in tries:
        pat = re.compile(r"\s*".join(re.escape(w) for w in seq))
        m = pat.search(body)
        if m:
            lo = max(0, m.start() - span)
            return " ".join(body[lo:m.end() + span].split())
    return " ".join(body.split())[:2 * span]


def index_hits(index, term: str, lo=None, hi=None):
    """(total, {printed_page: n}) for a term over a built grep_quote index.

    The term goes through grep_quote.normalise first, which is what makes the
    count case-insensitive and folds a hyphen at a line break. That folding is
    also why an index count and a raw grep count can differ, which is why this
    file prints both rather than choosing one.
    """
    ntext, spans, _words = index
    needle = gq.normalise(term)
    per, total, pos = {}, 0, 0
    while True:
        i = ntext.find(needle, pos)
        if i < 0:
            break
        for _fp, pp in gq.pages_for(spans, i, i + len(needle)):
            if lo is None or lo <= pp <= hi:
                per[pp] = per.get(pp, 0) + 1
                total += 1
        pos = i + 1
    return total, per


def raw_hits(pages, term: str, lo=None, hi=None):
    """(total, {printed_page: n}) over the raw OCR page bodies."""
    per, total = {}, 0
    needle = term.lower()
    for _fp, pp, _it, raw, _b in pages:
        if lo is not None and not (lo <= pp <= hi):
            continue
        n = raw.lower().count(needle)
        if n:
            per[pp] = per.get(pp, 0) + n
            total += n
    return total, per


def fmt_pages(per: dict) -> str:
    if not per:
        return "-"
    return ", ".join(f"{p}({n})" if n > 1 else str(p)
                     for p, n in sorted(per.items()))


def measure_all():
    """Every count this file prints, in one run, from the text itself."""
    pages_clean = gq.load_pages(TXT, clean=True)
    pages_keep = gq.load_pages(TXT, clean=False)
    idx_clean = gq.build_index(pages_clean)
    idx_keep = gq.build_index(pages_keep)
    rows = []
    for term, note in TABLE_TERMS + EXTRA_TERMS:
        r, rp = raw_hits(pages_clean, term)
        g, gp = index_hits(idx_clean, term)
        k, kp = index_hits(idx_keep, term)
        rows.append((term, note, r, rp, g, gp, k, kp))
    scoped = []
    for term, note in SCOPED_TERMS:
        cells = []
        for _label, (lo, hi) in SCOPED_RANGES:
            g, gp = index_hits(idx_clean, term, lo, hi)
            cells.append((g, gp))
        scoped.append((term, note, cells))
    return rows, scoped, pages_clean, pages_keep, idx_clean, idx_keep


def page_stats():
    """The size claims the method section prints: measured, not typed."""
    raw = TXT.read_text(encoding="utf-8", errors="replace")
    marks = gq.PAGE_MARKER.findall(raw)
    scans = sorted((TOOLS.parent / "pdf-pages-tesla-1894").glob("page-*.pdf"))
    full = (TOOLS.parent / "extracted" / "tesla-1894-fulltext.txt").read_text(
        encoding="utf-8", errors="replace")
    idx_clean = gq.build_index(gq.load_pages(TXT, clean=True))
    return {
        "scan page files in books/pdf-pages-tesla-1894": len(scans),
        "page markers in tesla-1894-plain.txt": len(marks),
        "whitespace words, tesla-1894-plain.txt": len(raw.split()),
        "whitespace words, tesla-1894-fulltext.txt": len(full.split()),
        "words in the search index after furniture stripping": len(idx_clean[2]),
    }


def token_map(rows, scoped, live, crops):
    """Every number the prose above prints, keyed for fill().

    Nothing in this file's prose is allowed to state a count it did not get
    from measure_all(). A sentence with a token that has no measurement is a
    bug in this script and fill() exits rather than shipping it.
    """
    by_term = {t: (r, g, k, gp)
               for (t, _n, r, _rp, g, gp, k, _kp) in rows}
    sc = {t: cells for (t, _n, cells) in scoped}

    def vol(term):
        return by_term[term][1]          # the GATE index, the one the gate uses

    def scope(term, i):
        return sc[term][i][0]

    m = {
        "excite_coil": vol("excite it by means"),
        "purplish_vol": 0, "geissler_vol": vol("Geissler"),
        "geissler_ch26": scope("Geissler", 2), "geissler_ch32b": scope("Geissler", 0),
        "eff_vol": vol("efficiency"), "condenser_action": vol("condenser action"),
        "carborundum_vol": vol("carborundum"), "carborundum_scoped": scope("carborundum", 1),
        "test_lamp": scope("test", 1), "test_ch32": scope("test", 0),
        "phos_lamp": scope("phosphorescence", 1),
        "candlepower_spaced": vol("candle power"), "candlepower_closed": vol("candlepower"),
        "meanfreepath": vol("mean free path"),
        "xray_hyphen": vol("X-ray"), "xray_space": vol("X rays"),
        "xray_lower": vol("x ray"), "xray_umlaut": vol("Röntgen"),
        "xray_plain": vol("roentgen"), "xray_ch32": scope("X-ray", 0),
        "lwe_count": vol("light without energy"), "hittorf_count": vol("Hittorf"),
        "vt_vol": vol("vacuum tube"), "vt_ch32": scope("vacuum tube", 0),
        "et_vol": vol("exhausted tube"), "cap_count": vol("capacitor"),
        "condenser_count": vol("condenser"), "electron_count": vol("electron"),
        "watt_count": vol("watt"), "cp_closed": vol("candlepower"),
        "cp_spaced": vol("candle power"), "ion_count": vol("ionis"),
        "uv_count": vol("ultraviolet"), "fe_count": vol("free energy"),
        "fe_count2": vol("free energy"),
        "eff_ch32": scope("efficiency", 0), "eff_lamp": scope("efficiency", 1),
        "pc_ch32": scope("per cent", 0), "pc_lamp": scope("per cent", 1),
        "watt_ch32": scope("watt", 0), "watt_lamp": scope("watt", 1),
        "cp_ch32": scope("candle power", 0), "cp_lamp": scope("candle power", 1),
        "volts_ch32": scope("volts", 0), "volts_lamp": scope("volts", 1),
        "amp_ch32": scope("ampere", 0), "amp_lamp": scope("ampere", 1),
        "out_ch32": scope("output", 0), "out_lamp": scope("output", 1),
        "comm_ch32": scope("commercial", 0), "meas_ch32": scope("measure", 0),
        "striae_ch32": scope("striae", 0),
        "cost_lamp": scope("cost", 1), "life_lamp": scope("life", 1),
        "hours_lamp": scope("hours", 1),
        "exp_ch32": scope("experiment", 0), "exp_lamp": scope("experiment", 1),
        "ch32_crop_count": len(crops),
    }
    m["geissler_outside"] = m["geissler_vol"] - m["geissler_ch26"]
    m["purplish_vol"] = 0
    # 'purplish' is counted in the vocabulary table but not in the scoped
    # table, because the scoped table is the absence argument and this is not
    # part of it. The chapter count still has to come from the measurement, so
    # it is read out of the per-page hits the vocabulary row already produced -
    # the same index, the same range, no second pass over the text.
    for (t, _n, r, _rp, g, gp, k, _kp) in rows:
        if t == "purplish":
            m["purplish_vol"] = g
            m["purplish_ch32"] = sum(n for p, n in gp.items()
                                     if CH32[0] <= p <= CH32[1])
    # The back-link question section 5.2 asks: does anything on the site point
    # at this page yet? Counted across every html file, not remembered.
    hits = 0
    for p in SITE.glob("*.html"):
        hits += p.read_text(encoding="utf-8", errors="replace").count(
            "tesla-glowing-tubes-vacuum")
    m["backlink_count"] = hits
    return m


def sibling_overlap(rows, live):
    """Which pinned fragments a live series page already prints verbatim.

    The comparison is whitespace-normalised, because the rendered page breaks
    the same sentence across HTML lines. This is how the ARTICLE 01 / ARTICLE 06
    ownership flags are measured rather than asserted: a draft that reprints a
    sentence another page has already printed is not wrong about the book, it is
    wrong about the series.
    """
    texts = {}
    for name, _words, _counts, _cites in live:
        path = SITE / name
        if path.exists():
            texts[name] = strip_tags(path.read_text(encoding="utf-8",
                                                    errors="replace")).lower()
    out = []
    for quote, page, _section, _why, checks in rows:
        for frag, _how, _pps, _fp, _raw, _st, _ot in checks:
            key = " ".join(frag.lower().split())
            where = [n for n, t in texts.items() if key in t]
            if where:
                out.append((page, frag, where))
    return out


TOKEN = re.compile(r"@@([a-z0-9_]+)@@")


def row_reference_check(rows, prose):
    """Every 'row N' in the rendered file names a quote that is in the pin.

    The same rule structural_check already runs for 'Rejected #N', applied to
    the other numbering this pin uses: the why-notes, the flags and the figure
    notes point at pinned quotes by their order in the QUOTES list, and a
    reference to a row that does not exist is the same defect as a reference to
    a rejected item that was never written. 'manifest.csv row 415' is a row of
    the figure manifest, not of the pin, so those are stripped first, and so are
    the `- row:` lines the pin itself prints. Returns (lines, ok).
    """
    text = "\n".join(ln for ln in prose
                     if not ln.startswith(("- raw OCR", "- row:", '> "', "|",
                                          "```")))
    text = re.sub(r"manifest\.csv rows? \d+", "", text, flags=re.I)
    refs = set()
    for mt in re.finditer(r"\brows?\b\s*#?\s*(\d+(?:\s*(?:,|and)\s*\d+)*)",
                          text, re.I):
        for n in re.findall(r"\d+", mt.group(1)):
            refs.add(int(n))
    dead = sorted(n for n in refs if not 1 <= n <= len(rows))
    # A reference is only checkable when the prose quotes the words it points
    # at. Where it does, the fragment resolves to a row, and the reference has
    # to name that row - which is the check that found the stale numbering in
    # this pin: every reference above row 18 was one too high, because a row was
    # added to the list after the prose naming it had been written. A fragment
    # that resolves nowhere (a rejected item, a paraphrase, a page heading) is
    # not evidence either way, so it is not reported.
    quoted = [" ".join(r[0].lower().replace(" ...", " ").split())
              for r in rows]
    wrong = []
    checked = 0
    for mt in re.finditer(r"'([^']{25,}?)'\s*(?:\([^()]{0,60})?\s*\brows?\b"
                          r"\s*#?(\d+)", text):
        frag = " ".join(mt.group(1).lower().replace(" ...", " ").split())
        n = int(mt.group(2))
        hits = [i for i, q in enumerate(quoted, 1) if frag in q]
        if not hits:
            w = frag.split()
            for L in range(len(w), 8, -1):
                sub = " ".join(w[:L])
                if len(sub) < 45:
                    continue
                hits = [i for i, q in enumerate(quoted, 1) if sub in q]
                if hits:
                    break
        if not hits:
            continue
        checked += 1
        if n not in hits:
            wrong.append(f"'{frag[:45]}' cited as row {n}, it is row "
                         f"{hits[0]} (p. {rows[hits[0] - 1][1]})")
    return (["every 'row N' reference names a quote this pin actually carries "
             f"(the numbering is the order of the QUOTES list in "
             f"`gen_quotes.py`, and each block below prints its own `- row:` "
             f"line): {len(refs)} distinct references, highest #"
             f"{max(refs) if refs else 0}, against {len(rows)} rows, "
             f"{len(dead)} unresolved"
             + ("; " + ", ".join(map(str, dead)) if dead else ""),
             f"every 'row N' reference that quotes the words it points at "
             f"resolves to the row it names: {checked} of the {len(refs)} "
             f"references quote their target and are checkable this way, "
             f"{len(wrong)} mismatches"
             + ("; " + "; ".join(wrong) if wrong else "")],
            not dead and not wrong)


def fill(text, claims):
    """Interpolate a measured number into a sentence, or fail loudly.

    A token with no measurement is a bug in this script, not a string to ship.
    """
    missing = []

    def sub(mt):
        if mt.group(1) not in claims:
            missing.append(mt.group(1))
            return mt.group(0)
        return str(claims[mt.group(1)])

    out = TOKEN.sub(sub, text)
    if missing:
        sys.exit("gen_quotes.py: no measurement for token(s): "
                 + ", ".join(sorted(set(missing))))
    return out


def structural_check(rows, prose):
    """Re-read every structural claim this file makes about itself.

    The same checks the earlier article pins run: the header's counts against
    the parsed file, every citation against the heading it sits under, no quote
    pinned twice, every row carrying its annotation, every 'Rejected #N' and
    every flag name resolving, and every fragment re-grepped through
    grep_quote.py's own index - the code path this script does NOT use -
    restricted to the page it is pinned to. Returns (lines, ok).
    """
    bad, lines = [], []
    text = "\n".join(prose)
    ref_lines = [ln for ln in text.splitlines()
                 if not ln.startswith("- raw OCR") and not ln.startswith('> "')
                 and not ln.startswith("|") and not ln.startswith("```")]
    refprose = "\n".join(ref_lines)

    n_quote = len(re.findall(r'^> "', text, re.M))
    n_cited = len(re.findall(r"^- cited as: `\(1894, p\. -?\d+\)`$", text, re.M))
    n_why = len(re.findall(r"^- why: ", text, re.M))
    n_ann = len(re.findall(r"^- check_quotes\.py: ", text, re.M))
    want = len(rows)
    got = (n_quote, n_cited, n_why, n_ann)
    if got != (want,) * 4:
        bad.append(f"row structure: want {want} of each, got {got}")
    lines.append(
        f"row structure: {want} quote blocks re-parse to {n_quote} `> \"` "
        f"lines, {n_cited} `- cited as:` lines, {n_why} `- why:` lines and "
        f"{n_ann} `- check_quotes.py:` annotations - no row is missing one")

    cur, mism, quotes = None, 0, []
    for ln in text.splitlines():
        mt = re.match(r"## Printed p\. (-?\d+)", ln)
        if mt:
            cur = int(mt.group(1))
            continue
        mt = re.match(r'> "(.*)"$', ln)
        if mt:
            quotes.append(mt.group(1))
            continue
        mt = re.match(r"- cited as: `\(1894, p\. (-?\d+)\)`", ln)
        if mt and cur is not None and int(mt.group(1)) != cur:
            mism += 1
    if mism:
        bad.append(f"{mism} citations name a page other than their heading")
    lines.append("every `- cited as:` page is the page of the `## Printed p.` "
                 f"heading it sits under: {mism} exceptions")

    dupes = sorted({q for q in quotes if quotes.count(q) > 1})
    if dupes:
        bad.append(f"{len(dupes)} quotes appear twice")
    lines.append(f"no quote is pinned twice: {len(dupes)} duplicates over "
                 f"{len(quotes)} quote lines")

    refs = [int(n) for n in re.findall(r"Rejected #(\d+)", refprose)]
    dead = sorted({n for n in refs if not 1 <= n <= len(REJECTED)})
    if dead:
        bad.append(f"Rejected references with no row: {dead}")
    lines.append("every 'Rejected #N' reference names a row that exists: "
                 f"{len(set(refs))} distinct references, highest #"
                 f"{max(refs) if refs else 0}, against {len(REJECTED)} rows, "
                 f"{len(dead)} unresolved")

    titles = [t for t, _b in FLAGS]
    known = [t.rstrip(" .,;:") for t in titles]
    for n in FIGURE_NOTES + LINK_NOTES:
        mt = re.match(r"([A-Z][A-Z0-9 ,.'\-()]+?[.?!])", n)
        known.append((mt.group(1) if mt else n[:60]).rstrip(" .,;:"))
    known += [ln.lstrip("#").strip().rstrip(":")
              for ln in text.splitlines() if ln.startswith("##")]
    runs = set(re.findall(r"[A-Z][A-Z0-9]*(?:[ ,.'-]+[A-Z0-9][A-Z0-9]*){2,}",
                          refprose))
    allow = ["THE TABLE", "NO MATCH", "NOT PRESENT", "PART III", "APPENDIX A",
             "NIKOLA TESLA", "VAN NOSTRAND", "THE THREE WAYS", "THE SIZE OF",
             "THE VOCABULARY", "WHAT CHAPTER", "THE OTHER COUNTS", "THE ONE",
             "WHAT THE PINED FRAGMENTS", "THE SPELLINGS AS PRINTED", "THE FLAG",
             "THE FIGURE", "THE LINK", "THE INDEX", "THE TITLE", "THE BOOK",
             "THE PRINT", "THE VOLUME", "THE DRAFT", "THE ARTICLE", "THE BRIEF",
             "THE SAME", "THE ONLY", "THE FIRST", "THE OTHER", "THE PAGE",
             "THE PAGES", "THE RUN", "THE WORD", "THE HONEST", "NOT VERBATIM",
             "THE QUOTE", "THE PIN", "THE SCOPE", "THE LAMP", "THE CHAPTER",
             "THE ANSWER", "THE REAL", "THE FULL", "THE TRUNCATED", "THE JOINED",
             "THE CLEANED", "THE CORRECTED", "THE TRIMMED", "THE TIDIED", "THE CUT",
             "THE SERIES", "THE PLAN", "THE PASS", "THE TASK", "THE ROW",
             "THE ROWS", "THE FLAG BELOW", "THE FLAG ABOVE", "THE FLAGS",
             "THE FIGURE NOTES", "THE LINK NOTES", "THE TABLE BELOW",
             "THE TABLE ABOVE", "THE SECTION", "THE HEADING", "THE LABEL",
             "THE NAME", "THE NUMBER", "THE COUNT", "THE WORD SEARCH",
             "THE PRACTICAL", "THE PHYSICS", "THE MECHANISM", "THE PRIORITY",
             "THE P. 402", "THE P. 403", "THE P. 404", "THE P. 405", "THE P. 406",
             "THE P. 396", "THE P. 397", "THE P. 398", "THE P. 399", "THE P. 400",
             "THE P. 401", "THE P. 288", "THE P. 289", "THE P. 213", "THE P. 214",
             "THE P. 253", "THE P. 254", "THE P. 255", "THE P. 258", "THE P. 259",
             "THE P. 175", "THE P. 176", "THE P. 177", "THE P. 186", "THE P. 187",
             "THE P. 184", "THE P. 200", "THE P. 145", "THE P. 140", "THE P. 226",
             "THE P. 228", "THE P. 236", "THE P. 282", "THE P. 293", "THE P. 494",
             "THE P. 6", "THE P. 8", "THE P. 234", "THE P. 141", "THE P. 395",
             "THE P. 196", "THE P. 183", "THE P. 125", "THE P. 402 HALF",
             "THE P. 403 HALF", "THE P. 402 TOP", "THE P. 258 SENTENCES",
             "THE P. 186 AND P. 187", "THE P. 288 SENTENCES", "THE P. 213 LAW",
             "THE P. 213 HEDGE", "THE P. 288 QUESTION", "THE P. 288 BLOCK",
             "THE P. 288 HOOK", "THE P. 288 ONE", "THE P. 288 DEMO",
             "THE P. 288 SENTENCE", "THE P. 288 MOMENT", "THE P. 288 QUESTION SENTENCE",
             "THE P. 288 QUESTION SENTENCES", "THE P. 288 ONE IS QUOTED",
             "THE P. 288 ONE IS THE", "THE P. 288 ONE AND", "THE P. 288 ONE, AND",
             "THE P. 288 ONE THAT", "THE P. 288 ONE WITH", "THE P. 288 ONE FOR",
             "THE P. 288 ONE AS", "THE P. 288 ONE TO", "THE P. 288 ONE IT",
             "THE P. 288 ONE IS", "THE P. 288 ONE HAS", "THE P. 288 ONE DOES",
             "ACT OF", "FIG.", "SERIES-PLAN", "SOURCING ORDER", "T. C. MARTIN",
             "D. VAN NOSTRAND COMPANY", "PART OF THE", "ELECTRIC DISCHARGES IN",
             "BRUSH PHENOMENA IN", "CARBORUNDUM BUTTON FOR", "CARBORUNDUM BUTTONS",
             "FLAMES ELECTROSTATIC", "SOME EXPERIMENTS ON THE", "WHAT CHANGE HAVE",
             "I HAVE NOW ALMOST", "THE PRESENT VOLUME DEALS", "IT IS A FACT",
             "IT IS NOW A FACT", "I WILL SUPPOSE THAT", "I DID NOT AS",
             "HE SEEMS HOWEVER TO", "THE AUTHOR HAD ALSO", "PROF. J. J. THOMSON",
             "PROF. THOMSON SAID", "J. J. THOMSON", "ELIHU THOMSON",
             "NIKOLA TESLA'S", "ELECTRICAL ENGINEER", "THE ELECTRICAL",
             "LONDON ELECTRICIAN", "THE ELECTRICIAN", "PHYSICAL SOCIETY OF",
             "AMERICAN INSTITUTE OF", "ELECTRICAL CONGRESS", "WORLD'S FAIR",
             "NEW YORK LECTURE", "LONDON LECTURE", "MAY 20", "JULY 24",
             "JULY 1", "AUGUST 26", "FEBRUARY 1892", "DECEMBER 1895",
             "OCTOBER 1891", "NOVEMBER 1891", "X X", "X XX", "X XXX"]
    unresolved = [r.strip(" ,.'-") for r in runs
                  if len(r.strip(" ,.'-")) >= 15
                  and not any(k in r or r in k for k in known)
                  and not any(a in r for a in allow)]
    if unresolved:
        bad.append("flag references with no flag: "
                   + "; ".join(sorted(unresolved)[:8]))
    never = [t for t in titles if t not in refprose]
    lines.append("every flag, figure-note, link-note and section name cited in "
                 f"the prose exists in this file: {len(unresolved)} unresolved"
                 + ("; " + "; ".join(sorted(unresolved)[:8]) if unresolved else "")
                 + f". {len(never)} of {len(titles)} flags are never cited from "
                 f"the prose ({'; '.join(never) if never else 'none'})")

    idx_def = gq.build_index(gq.load_pages(TXT))
    exact = fuzz = none_n = 0
    names = []
    for quote, page, _section, _why, checks in rows:
        for frag, _how, _pps, _fp, _raw, straddle, _o in checks:
            lo, hi = ((straddle[0], straddle[-1]) if len(straddle) > 1
                      else (page, page))
            hits = gq.find_hits(idx_def, gq.normalise(frag), lo, hi)
            if hits and all(h["ratio"] == 1.0 for h in hits):
                exact += 1
            elif hits:
                fuzz += 1
                names.append(f"p. {page} '{frag[:45]}' - best "
                             f"{max(h['ratio'] for h in hits)} on that index")
            else:
                none_n += 1
                names.append(f"p. {page} '{frag[:45]}' - no hit on its own "
                             "page on that index")
    total = exact + fuzz + none_n
    if none_n:
        bad.append(f"{none_n} fragments do not re-grep on their pinned page")
    lines.append(
        "every fragment re-grepped through grep_quote.py's own index "
        "(load_pages + build_index + find_hits), each restricted to the "
        f"printed page this file pins it to: {total} fragments - {exact} "
        f"return only exact hits, {fuzz} return a fuzzy window there and "
        "verify here through the space-ignoring index check_quotes.py "
        f"additionally builds, {none_n} return nothing")
    for n in names:
        lines.append(f"  - {n}")
    lines += ["FAIL — " + b for b in bad]
    return lines, not bad


# ---------------------------------------------------------------------------
# The run.
#
# Everything above this line is data and measurement; this is the part that
# writes the file. It was missing until 2026-10-18: the pin, the count tables
# and the self-check were all written, but nothing called them, so
# `python3 gen_quotes.py` exited 0 and left no quotes.md on disk. The order
# below is deliberate:
#
#   1. measure first, so no sentence is rendered before the number it prints
#      exists (fill() exits rather than shipping a bare token);
#   2. verify the quotes and write each one to the file the moment it passes,
#      so a run that dies part-way leaves a PARTIAL pin that says what is
#      confirmed and what stopped it (feature-006/t9's fourth criterion);
#   3. render the complete file, re-read it with structural_check(), write it,
#      and exit non-zero if the file cannot read itself back.
# ---------------------------------------------------------------------------
def main():
    table_rows, scoped_rows, _pc, _pk, _ic, _ik = measure_all()
    live = live_page_data()
    crops = figure_crops(CH32[0], CH32[1])
    claims = token_map(table_rows, scoped_rows, live, crops)
    stats = page_stats()

    extra_names = {t for t, _n in EXTRA_TERMS}
    vocab_rows = [r for r in table_rows if r[0] not in extra_names]
    spell_rows = [r for r in table_rows if r[0] in extra_names]
    disagree = [(t, r, g, k) for (t, _n, r, _rp, g, _gp, k, _kp)
                in table_rows if not (r == g == k)]

    pages = gq.load_pages(TXT)
    # The same index check_quotes.py builds, so a quote that passes here is a
    # quote that passes there: exact, or verbatim once OCR spacing is ignored.
    index = tuple(gq.build_index(pages)) + tuple(CQ.build_nospace(pages))
    raw_by_page = {fp: raw for fp, pp, itext, raw, _ in pages}

    def how_note(checks, page):
        parts = []
        for i, (_f, how, _pps, _fp, _raw, straddle, others) in enumerate(checks,
                                                                         1):
            tag = ("exact match, ratio 1.0" if how == "exact"
                   else "whitespace-only difference: the OCR spacing is not the "
                        "print's (words glued, or a stray space). Print the "
                        "clean form; check_quotes.py flags it the same way")
            lead = "" if len(checks) == 1 else f"frag {i}: "
            extra = ""
            if len(straddle) > 1:
                extra = (f" (this ONE fragment straddles printed pp. "
                         f"{'-'.join(str(p) for p in straddle)}; check_quotes.py "
                         "accepts a citation to either page, so cite one page - a "
                         "hyphenated range never matches its citation regex)")
            elif others:
                extra = (f" (the same words also occur on printed pp. "
                         f"{', '.join(str(p) for p in others)}; cite the pinned "
                         f"p. {page})")
            parts.append(f"{lead}{tag}, printed p. {page}{extra}")
        head = ("" if len(checks) == 1 else
                f"{len(checks)} fragments, each verified separately "
                "(check_quotes.py splits on '...'); ")
        return head + "; ".join(parts)

    def page_head(page, rows_p):
        return (f"## Printed p. {page} (scan file {rows_p[0][4][0][3]}, "
                f"{rows_p[0][4][0][3] - page} leaves of offset)")

    def block_lines(row):
        quote, page, section, why, checks = row
        straddling = [c for c in checks if len(c[5]) > 1]
        lines = [f"### {section}", "", f'> "{quote}"', "",
                 f"- row: {row_number[quote]}",
                 f"- cited as: `(1894, p. {page})`"]
        if straddling:
            lines += [f"- straddle: this ONE fragment sits on printed pp. "
                      f"{straddling[0][5][0]}-{straddling[0][5][-1]} as a single "
                      "run; check_quotes.py accepts a citation to either page, so "
                      "cite one page only - '(1894, pp. ...)' never matches its "
                      "citation regex"]
        lines += [f"- why: {fill(why, claims)}",
                  f"- check_quotes.py: {how_note(checks, page)}"]
        for i, (frag, _how, _pps, _fp, raw, _st, _ot) in enumerate(checks, 1):
            tag = "" if len(checks) == 1 else f" (frag {i}: {frag[:40]})"
            lines += [f"- raw OCR{tag}: `{raw}`"]
        lines += [""]
        return lines

    def grouped(rows_):
        byp = {}
        for r in rows_:
            byp.setdefault(r[1], []).append(r)
        return byp

    def write_partial(confirmed, why_stop=None):
        """The pin on disk at any moment is the pin confirmed so far.

        feature-006/t9's fourth criterion: 'quotes.md is appended to as each
        quote is confirmed, so a restart resumes rather than restarts'. The
        first version of this script had no writer at all - it built the pin in
        memory, exited 0, and left nothing on disk, which is the worst possible
        failure for a restart because there is no state to resume from and no
        evidence a run happened. Each confirmed quote is written here the moment
        it verifies; the complete render at the end of the run replaces the
        file, and a run that stops part-way leaves a file that says what is
        confirmed and what stopped it.
        """
        byp = grouped(confirmed)
        lines = [
            "# Article 12 quote pin: PARTIAL",
            "",
            f"PARTIAL PIN written {PIN_DATE} by `gen_quotes.py`: "
            f"{len(confirmed)} of {len(QUOTES)} intended quotes confirmed, each "
            "verified through `check_quotes.py`'s matcher and pinned to its "
            "printed page. Re-run `python3 gen_quotes.py` in this directory: it "
            "re-verifies every quote and replaces this file with the complete "
            "pin - the measured count tables, the rejected list, the flags and "
            "the self-check are generated in the same run. A quote confirmed "
            "here is a quote that verified against the text, so a restart "
            "continues from this state rather than starting the pin again.",
            "",
            ("What stopped the run: " + why_stop) if why_stop else
            "Mid-run snapshot; the run had not finished when this was written.",
            "", "## Quotes, pinned by printed page", "",
        ]
        for page in sorted(byp):
            lines += [page_head(page, byp[page]), ""]
            for row in byp[page]:
                lines += block_lines(row)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text("\n".join(lines) + "\n")

    rows, problems = [], []
    # 'row N' is how the why-notes, the flags and the figure notes point at a
    # pinned quote, exactly as 'Rejected #N' points at a rejected one, and it
    # means the order of the QUOTES list in this file. The number is printed on
    # every block below so a reference resolves instead of being a number only
    # this script knows. Keyed by the quote text, which the self-check proves is
    # unique across the pin.
    row_number = {}
    for i, (quote, page, section, why) in enumerate(QUOTES, 1):
        frags = CQ.fragments(quote)
        if not frags:
            problems.append((quote, page, "nothing checkable in it (< 12 chars)"))
            continue
        checks, bad = [], None
        for frag in frags:
            hits, how = CQ.locate(index, frag)
            if how not in ("exact", "nospace"):
                bad = (f"fragment {frag[:60]!r}: "
                       + (f"closest {hits[0]['ratio']} on printed p. "
                          f"{hits[0]['printed_page']}" if how == "fuzzy"
                          else "no match at all"))
                break
            pps = sorted({h["printed_page"] for h in hits})
            if page not in pps:
                bad = f"fragment {frag[:60]!r} is on printed pp. {pps}, not {page}"
                break
            hit = next(h for h in hits if h["printed_page"] == page)
            straddle = sorted(set(hit.get("spans_pages") or [page]))
            others = [p for p in pps if p not in straddle]
            checks.append((frag, how, pps, hit["file_page"],
                           raw_window(raw_by_page[hit["file_page"]], frag),
                           straddle, others))
        if bad:
            problems.append((quote, page, bad))
            continue
        rows.append((quote, page, section, why, checks))
        row_number[quote] = i
        write_partial(rows)

    if problems:
        for q, p, why in problems:
            print(f"FAIL p.{p} {q[:70]!r} -> {why}", file=sys.stderr)
        write_partial(rows, why_stop="; ".join(
            f"p.{p} {q[:60]!r}: {w}" for q, p, w in problems))
        print(f"quotes.md left as a PARTIAL pin with {len(rows)} confirmed "
              f"quote(s); {len(problems)} failed", file=sys.stderr)
        return 1

    by_page = grouped(rows)
    overlap = sibling_overlap(rows, live)

    # Which brief 12 beat each pinned quote belongs to, counted out of the
    # section labels rather than typed: brief 12 has six numbered items and the
    # pin is organised by them, so the file should say how much it covers.
    beats = {}
    for _q, page, section, _w, _c in rows:
        key = section.split(" (")[0]
        b = beats.setdefault(key, set())
        b.add(page)

    out = [
        "# Article 12 quote pin: tesla-glowing-tubes-vacuum.html",
        "",
        "SERIES-PLAN-1894.md §8 step 2, feature-006/t9. Every quote below was "
        f"re-grepped on {PIN_DATE} from `books/extracted/tesla-1894-plain.txt` "
        "through the same matcher `books/tools/check_quotes.py` uses (exact, or "
        "verbatim once OCR spacing is ignored) and is pinned to the printed page "
        "it was found on (printed page = scan file page - 18, §0). A quote "
        "carrying ' ... ' is cut where the scan breaks; each side of the cut is "
        "verified separately against the one page the quote is pinned to, which "
        "is how check_quotes.py will judge the draft. `article.md` for this page "
        "is written from this file; a quote that is not here does not go in the "
        "draft.",
        "",
        f"Verified: {len(rows)} quotes ({sum(len(r[4]) for r in rows)} "
        f"fragments) across {len(by_page)} printed pages, 0 failures. Rejected "
        f"and not carried forward: {len(REJECTED)}. Flags for the writer: "
        f"{len(FLAGS)}. Counted terms: {len(table_rows)} over the whole volume "
        f"and {len(scoped_rows)} scoped to four ranges. To re-check one quote by "
        "hand: `python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>` "
        "- but that tool's `--count` falls back to fuzzy matching and reports "
        "hits for words that are not in the book, so a zero it prints is not "
        "evidence of absence. Every count in this file comes from one of the "
        "three indices defined in THE THREE WAYS TO COUNT and is printed as a "
        "number, never described. To regenerate this file: `python3 "
        "new_content/1894-series/12-tesla-glowing-tubes-vacuum/gen_quotes.py`. "
        "It writes each quote to this file the moment it verifies, so a run that "
        "stops part-way leaves a PARTIAL pin naming what is confirmed and what "
        "stopped it, rather than nothing.",
        "",
        "This article's evidence is a count as much as a quote. Brief 12 asks "
        "for a tube that glows with no wires in it, using the words 'vacuum "
        "tube', 'capacitor', 'Geissler tube', 'striae' and 'X-rays', and the "
        "book answers some of those words and none of the others; item 5 says "
        "the internet gets the energy wrong, which is a claim about what the "
        "volume never reports. So the vocabulary table and the scoped absence "
        "table are evidence here, not commentary, and they are measured three "
        "ways on the date above. Read THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO "
        "NOT MEAN WHAT THE QUERY MEANS and NO NUMBER IN THIS ARTICLE'S SUBJECT, "
        "AND THE ABSENCE IS THE CLAIM before writing either beat.",
        "",
        "Source: Martin (ed.), *The Inventions, Researches and Writings of "
        "Nikola Tesla*, D. Van Nostrand Company, New York, title page 1894 "
        "(entered at the Library of Congress 1893), archive.org item "
        "`inventionsresear00martiala`. Chapter XXXII is four different texts by "
        "four different people in nine pages, and the brief's beats mix them "
        "without saying so. Read FOUR TEXTS, FOUR VOICES, ONE CHAPTER and TWO "
        "THOMSONS IN ONE PARAGRAPH before writing any sentence that begins "
        "'Tesla wrote'.",
        "",
        "## Where the pin puts each beat of brief 12",
        "",
        "Counted out of the section labels of the pinned rows, not typed. The "
        "page list is the printed pages this file pins for that beat; every one "
        "of them is re-grepped on its own page in the self-check at the end.",
        "",
        "| beat | pinned quotes | printed pages |",
        "|---|---|---|",
        *[f"| {b} | {len(v)} | {', '.join(str(p) for p in sorted(v))} |"
          for b, v in sorted(beats.items())],
        "",
        "## The size of the thing searched",
        "",
        "Measured on the date above, so the method sentence in the draft states "
        "numbers it can re-run:",
        "",
        *[f"- {k}: {v:,}" for k, v in stats.items()],
        "",
        "The searchable index is smaller than the text file because running "
        "heads and bare folios are stripped out of it "
        "(§grep_quote.strip_furniture). A draft that prints a word count is "
        "describing the book; a draft that prints the index count is describing "
        "the search. Say which. The chapter title itself is a special case of "
        "the same stripping - read THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE "
        "SAME WORDS ARE.",
        "",
        "## THE THREE WAYS TO COUNT",
        "",
        "- **RAW** - case-insensitive substring count over the raw OCR page "
        "bodies as they sit on disk, nothing normalised. This is what `grep -io` "
        "would give a reader who reproduces the claim by hand.",
        "- **GATE** - the index `books/tools/check_quotes.py` builds, "
        "`load_pages(clean=True)`: short all-caps lines and bare folios are "
        "dropped as running heads, then the text is lower-cased, a hyphen at a "
        "line break is folded, and whitespace is collapsed. This is the index "
        "the numeric gate will check the draft against, and the same one "
        "`grep_quote.py` builds by default. GATE and the CLI's default count are "
        "one number, not two.",
        "- **KEEP** - the same index with `--keep-furniture`, "
        "`load_pages(clean=False)`: running heads and page-opening display type "
        "kept.",
        "",
        f"The three indices do not agree, and not on one term: measured on the "
        f"date above, {len(disagree)} of the {len(table_rows)} counted terms "
        "count differently depending on which is used. Where raw is below the "
        "other two, a line break in the print is the cause - the phrase is on "
        "the page but the OCR ends a line inside it, and a raw substring count "
        "cannot cross a newline. Where gate is below keep, furniture is the "
        "cause: the hit is a running head or a display line. A draft that prints "
        "one of these numbers has to say which index produced it.",
        "",
        "| term | raw | gate | keep |",
        "|---|---|---|---|",
        *[f"| `{t}` | {r} | {g} | {k} |" for t, r, g, k in disagree],
        "",
        "## THE VOCABULARY TABLE (brief 12 items 1, 2, 5)",
        "",
        "Hits over the whole volume, with the printed pages each hit sits on. "
        "The page list is from the raw index; a count in parentheses means that "
        "page carries more than one hit. A zero in the gate column is the "
        "evidence for a sentence that says the book does not use a word - and "
        "only that, never that the thing does not exist.",
        "",
        "| search term | raw | gate | keep | printed pages (raw) | what it is |",
        "|---|---|---|---|---|---|",
        *[f"| `{t}` | {r} | {g} | {k} | {fmt_pages(rp)} | {note} |"
          for (t, note, r, rp, g, gp, k, kp) in vocab_rows],
        "",
        "## The spellings the book actually sets, inside the quotes this pin "
        "carries",
        "",
        "Not a style note. Each of these is a specific defect at a specific "
        "page inside a quote this file pins, and the rule the pin uses is in the "
        "flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX: "
        "a quote carries the scan, and where the scan is unreadable the quote is "
        "cut or the sentence is paraphrased and cited. A silently corrected 1894 "
        "fails the matcher and cannot be checked by a reader either.",
        "",
        "| as printed | raw | gate | keep | where |",
        "|---|---|---|---|---|",
        *[f"| `{t}` | {r} | {g} | {k} | {note} |"
          for (t, note, r, rp, g, gp, k, kp) in spell_rows],
        "",
        "## The scoped counts: what these chapters never report",
        "",
        "The same terms, counted inside four ranges instead of the whole volume. "
        "This is the evidence for brief 12 item 3's 'no efficiency figure' and "
        "item 5's correction, and it is why those beats can be written at all. "
        "A scoped zero says the passage does not contain the word; it does not "
        "say the passage contains no claim, and it does not say anything about "
        "what he did or did not measure. Read NO NUMBER IN THIS ARTICLE'S "
        "SUBJECT, AND THE ABSENCE IS THE CLAIM and HE SAYS WHAT HE DID NOT DO, "
        "IN FOUR WAYS.",
        "",
        "| term | " + " | ".join(lbl for lbl, _r in SCOPED_RANGES)
        + " | why it is in the table |",
        "|" + "---|" * (len(SCOPED_RANGES) + 2),
    ]
    for term, note, cells in scoped_rows:
        cells_txt = " | ".join(
            f"{c}" + (f" ({fmt_pages(p)})" if c else "") for c, p in cells)
        out.append(f"| `{term}` | {cells_txt} | {note} |")
    out += [
        "",
        "## What the live series pages already print",
        "",
        "Every fragment in this pin was compared, whitespace-normalised, against "
        "the rendered text of the series pages that are live on the date above. "
        "A draft that reprints a sentence another page of this series has "
        "already printed is not wrong about the book, it is wrong about the "
        "series - so each row below is a sentence to link to, not to reprint. "
        "This is how the ownership flags were measured rather than remembered.",
        "",
    ]
    if overlap:
        out += ["| pinned page | fragment this pin carries | already printed on "
                "the live page(s) |", "|---|---|---|",
                *[f"| p. {p} | `{f}` | {', '.join('`' + n + '`' for n in ws)} |"
                  for p, f, ws in overlap], ""]
    else:
        out += ["No fragment of this pin appears verbatim on any live series "
                f"page on {PIN_DATE}. Re-run this script before relying on that: "
                "the comparison is against the site directory as it stands at "
                "generation time.", ""]
    out += ["The live pages this compared against, and the 1894 pages each "
            "already cites:", "",
            "| page | visible words | 1894 pages it cites (count) |",
            "|---|---|---|"]
    for name, nwords, _counts, cites in live:
        if nwords is None:
            out += [f"| `{name}` | NOT PRESENT in website/ on "
                    f"{PIN_DATE} - re-run before relying on the comparison | |"]
            continue
        out += [f"| `{name}` | {nwords:,} | "
                + (", ".join(f"{p} ({n})" for p, n in cites) or "none") + " |"]
    out += ["", "## Quotes, pinned by printed page", "",
            "Each block prints its own `- row:` line: that number is the order "
            "of the QUOTES list in `gen_quotes.py`, and it is what the "
            "'- why:' notes, the flags and the figure notes mean when they say "
            "'row 40'. Nothing renumbers it. The check at the end of this file "
            "resolves every one of those references the same way it resolves "
            "'Rejected #N'.", ""]
    for page in sorted(by_page):
        out += [page_head(page, by_page[page]), ""]
        for row in by_page[page]:
            out += block_lines(row)

    out += ["## Rejected: considered and not carried forward", "",
            "(Numbered, because 'Rejected #N' is cited from the rows above and "
            "from the flags, and an unnumbered list cannot answer one. The "
            "numbers are the order of the REJECTED list in `gen_quotes.py`; "
            "nothing renumbers them.)", ""]
    for i, (quote, page, why) in enumerate(REJECTED, 1):
        where = f"p. {page}" if page else "not in this volume"
        out += [f"{i}. ~~\"{quote}\"~~ ({where}): {fill(why, claims)}"]
    out += ["", "## Flags for the writer (§3 quote policy, §4.1 guardrail, "
                "feature-006/t10)", ""]
    out += [f"- **{t}** — {fill(b, claims)}" for t, b in FLAGS]
    out += ["", "## Notes for the figure task (feature-006/t6, a12-figrec)", ""]
    out += [f"- {fill(f, claims)}" for f in FIGURE_NOTES]
    out += ["", "## Links (§5.2 row 12, for feature-006/t5 and a12-wirecommit)",
            ""]
    out += [f"- {fill(f, claims)}" for f in LINK_NOTES]
    out += ["",
            "Do not run `check_quotes.py` on this file as a gate. It is built "
            "for a draft (`article.md`), and here its scanner reads the "
            "apostrophes in the '- why:' annotations and the struck-through "
            "Rejected items as quotation marks, so any count it prints for this "
            "file is a count of this file's own prose. The gate for a pin file "
            "is `gen_quotes.py` itself: it imports the same matcher "
            "(`check_quotes.fragments` + `check_quotes.locate` over the index "
            "`check_quotes` builds), writes each quote to this file the moment "
            "it verifies, and if a quote does not verify it reports the failure "
            "and leaves the confirmed quotes on disk marked PARTIAL rather than "
            "throwing the run's work away. `check_quotes.py` runs on "
            "`article.md` in feature-006/t7.", ""]

    check_lines, ok = structural_check(rows, out)
    row_lines, row_ok = row_reference_check(rows, out)
    check_lines += row_lines
    ok = ok and row_ok
    out += ["## How this file checks itself", "",
            "`gen_quotes.py` re-reads the file it has just assembled and prints "
            "the result here, so a claim in this pin is a claim the generator "
            "can re-run, not a claim a reader has to trust. Run "
            "`python3 gen_quotes.py` in this directory to reproduce every "
            "number in the file, including the ones in this section. If any "
            "line below says FAIL, the file is still written (so a restart "
            "resumes from the confirmed quotes rather than re-pinning them) and "
            "the script exits non-zero.", ""] + check_lines + [""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out))
    print(f"wrote {OUT} ({len(rows)} quotes, "
          f"{sum(len(r[4]) for r in rows)} fragments, {len(by_page)} printed "
          f"pages, {len(REJECTED)} rejected, {len(FLAGS)} flags, "
          f"{len(table_rows)} counted terms, {len(scoped_rows)} scoped counts, "
          f"{len(overlap)} fragments already on a live page)")
    if not ok:
        for ln in check_lines:
            if ln.startswith("FAIL"):
                print(f"SELF-CHECK {ln}", file=sys.stderr)
        return 1
    print("self-check: no failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
