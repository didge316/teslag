#!/usr/bin/env python3
"""Regenerate quotes.md for article 10 (feature-007/t0).

Run: python3 new_content/1894-series/10-tesla-free-energy-what-he-said/gen_quotes.py

Every entry is re-grepped at generation time through the same matcher
books/tools/check_quotes.py uses; if a quote does not verify on its stated printed
page the script fails and writes nothing (SERIES-PLAN-1894.md section 8 step 2,
section 0 non-negotiable 2). The draft is written from this file, not from memory,
and a quote that is not here does not go in the draft.

Two things this pin MEASURES rather than types, because for THIS article they are
the evidence and not the commentary:

  * the word-search table (section 9 brief 10 item 2, Appendix D). The counts are
    computed here, three ways: a raw case-insensitive substring count over the OCR
    file, grep_quote.py's index built with running heads KEPT, and the index
    check_quotes.py actually builds, which drops short all-caps lines as running
    heads. A number the draft prints has to come with the index that produced it.
  * the three live pages section 9 brief 10 item 7 and section 5.2 row 10 link to.
    Their claim wording is read out of website/ at generation time, so "no claim
    carried forward that the live pages cannot support" (feature-007/t0 criterion
    3) is something the file shows rather than asserts.

A pinned quote may contain " ..." where the printed text is cut. Each fragment
between the cuts is verified separately against the one page the quote is pinned
to, which is exactly how check_quotes.py will judge the draft in feature-007/t3 -
this script does not reimplement that check, it imports it (check_quotes.fragments
+ check_quotes.locate over the index check_quotes builds). If a quote passes here
it passes there.
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
SITE = ROOT / "website"
OUT = Path("/home/matt/projects/other/tesla-generator/new_content/1894-series/"
           "10-tesla-free-energy-what-he-said/quotes.md")

PIN_DATE = "2026-10-17"

# The word-search table (brief 10 item 2 / Appendix D). RAW = case-insensitive
# substring count over books/extracted/tesla-1894-plain.txt as it sits on disk.
# KEEP = grep_quote.py's index built with load_pages(clean=False), running heads
# and display type kept. GATE = the index check_quotes.py builds,
# load_pages(clean=True), which drops short all-caps lines as running heads.
TABLE_TERMS = [
    ("free energy", "free energy / free-energy"),
    ("free-energy", "free energy / free-energy"),
    ("perpetual", "perpetual"),
    ("over unity", "over unity / over-unity"),
    ("over-unity", "over unity / over-unity"),
    ("magnetic generator", "magnetic generator"),
]
EXTRA_TERMS = [
    ("magnetic gener", "the stem article 08's closing beat searches"),
    ("magnetic generators", "the plural"),
    ("pyromagnetic", "unhyphenated"),
    ("pyro-magnetic", "hyphenated"),
    ("pyromagnetism", "the noun the chapter title uses"),
    ("thermo-magnetic", "the other half of ch. XXXVI's title"),
    ("magnetic motor", "the phrase the site's product vocabulary invites"),
    ("magnet motor", "the site's other product phrase"),
    ("magnetic engine", "a plausible-sounding 19th-century phrase"),
    ("magnetic dynamo", "ditto"),
    ("free electricity", "the site's phrase, and a live page's title"),
    ("free energ", "any inflected free-energy form"),
    ("perpetu", "any perpetual form"),
    ("unity", "what a reader searching 'over unity' by halves finds"),
    ("free", "the word alone"),
    ("energy", "the word alone"),
    ("wheelwork", "the phrase everyone posts"),
    ("wheelwork of nature", "the phrase as quoted"),
    ("radiometer", "Crookes' instrument"),
    ("Crookes", "the man the passage names"),
    ("efficiency", "the book's own measured quantity"),
    ("commercial usefulness", "the p. 8 phrase"),
    ("inexhaustible", "the p. 197 word"),
    ("bifilar", "the live page's coil word"),
    ("512,340", "the live page's patent number"),
    ("coil for electromagnets", "the live page's patent title"),
    ("test", "does ch. XXXVI report one"),
    ("experiment", "ditto"),
    ("result", "ditto"),
    ("per cent", "ditto"),
    ("output", "ditto"),
]
# Scoped over printed pp. 424-431, the chapter the pyromagnetic beat rests on.
CH36 = (424, 431)
SCOPED_TERMS = [("test", CH36), ("experiment", CH36), ("result", CH36),
                ("per cent", CH36), ("efficiency", CH36), ("output", CH36),
                ("free energy", CH36), ("perpetual", CH36)]

# The live pages brief 10 item 7 / section 5.2 row 10 link to.
LIVE_PAGES = ["magnetic-generator-scam.html",
              "tesla-magnetic-generator-worth-it.html",
              "free-electricity-from-magnets.html"]
LIVE_TERMS = ["free energy", "free-energy", "perpetual", "over unity",
              "over-unity", "magnetic generator", "1894", "512,340", "bifilar",
              "patent", "wheelwork", "efficiency", "Tesla"]
# Sentences on those pages article 10 must not carry forward, matched over the
# tag-stripped text so the pin prints the live wording itself.
LIVE_CLAIMS = [
    ("magnetic-generator-scam.html",
     r"[^.]*roughly 5 times more energy[^.]*\.", "over-unity claim"),
    ("magnetic-generator-scam.html",
     r"[^.]*if you put in 100 watts[^.]*\.", "the worked 5x number"),
    ("magnetic-generator-scam.html",
     r"[^.]*generating energy from perpetual motion[^.]*\.",
     "the page's own framing of the sceptics' case"),
    ("tesla-magnetic-generator-worth-it.html",
     r"[^.]*Patent No\. 512,340[^.]*\.", "patent claim"),
    ("tesla-magnetic-generator-worth-it.html",
     r"[^.]*inspired by Nikola Tesla's 1894 bifilar coil patent[^.]*\.",
     "the 1894 attribution"),
    ("tesla-magnetic-generator-worth-it.html",
     r"[^\"]{0,400}Not truly .{0,3}free energy[^.]*\.",
     "the page's own hedge - the one clause article 10 can agree with"),
    ("free-electricity-from-magnets.html",
     r"[^.]*perpetual motion generator design keeps spinning[^.]*\.",
     "perpetual-motion claim"),
    ("free-electricity-from-magnets.html",
     r"[^.]*reduce your bill by 30 to 50 percent[^.]*\.", "a savings number"),
]

# (quote exactly as the draft may print it, printed page, brief 10 section,
#  why it is in the piece)
QUOTES = [
    # ---- 0. Provenance: which text, whose voice, what the volume covers.
    ("Entered according to Act of Congress in the year 1893 ... in the office "
     "of the Librarian of Congress at Washington",
     -8, "0. Provenance (the copyright leaf)",
     "the method section says it searched 'the 1894 first edition', and this is "
     "the leaf that dates the book: entered 1893, title page 1894. Both halves "
     "verify; the whole line does not, because the OCR of the printer's imprint "
     "breaks the run - Rejected #1. Cite it as an unnumbered front-matter leaf "
     "by its scan file, never as 'p. -8'"),

    ("The present volume deals simply with his work accomplished to date",
     6, "0. Provenance (ch. I, the editor's date fence)",
     "the editor's own limit on the whole volume: everything in it is work "
     "already done by 1894. That is what licenses the article's question - "
     "these are devices described and written up by 1894, so asking what the "
     "book actually says about energy is fair and no 'Tesla predicted the "
     "future' framing is needed (section 4.1). Article 08's pin quotes the same "
     "line; the two articles must use it the same way"),

    ("includes a great many other inventions in arc lighting, transformers, "
     "pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, "
     "improvements in dynamos, new forms of incandescent lamps, electrical "
     "meters, condensers, unipolar dynamos, the conversion of alternating into "
     "direct currents",
     6, "2. The table (the editor's own inventory, ch. I)",
     "the first of the five 'magnetic generator' hits, and the only place in the "
     "volume where the phrase is hyphenated 'pyro-magnetic generators'. It is "
     "also the book's own inventory of the devices the phrase is attached to, and "
     "the only generator word in it is a pyro- one. Start the quote at "
     "'includes': the print sets ' Miscellaneous ' in its own quote marks, which "
     "would split the run in check_quotes.py's scanner"),

    ("Lecture delivered before the Institution of Electrical Engineers, London, "
     "February, 1892.",
     198, "0. Provenance (ch. XXVII footnote)",
     "dates the chapter that carries the p. 236 quote, the pp. 196-197 'energy "
     "from the medium' passage, the p. 232 one-wire sentence and the p. 267 "
     "one-wire prediction. Section 3's quote style prints 'Tesla wrote in 1892', "
     "so the date has to be in the pin, not in memory. Article 06's pin carries "
     "the same footnote for the same reason"),

    ("A lecture delivered before the American Institute of Electrical Engineers, "
     "at Columbia College, N. Y., May 20, 1891.",
     145, "0. Provenance (ch. XXVI footnote)",
     "dates the chapter that carries the p. 167 flame passage. Two dates, two "
     "chapters, and the article quotes from both: if it says '1892' about the "
     "flame or '1891' about the wheelwork sentence it is wrong. Read the flag "
     "FOUR TEXTS, FOUR DATES before writing brief 10 item 4"),

    ("BEFORE proceeding to study the three Tesla lectures here presented, the "
     "reader may find it of some assistance to have his attention directed to "
     "the main points of interest and significance therein",
     119, "0. Provenance (ch. XXV opening - the compiler's voice)",
     "printed pp. 119-144 are chapter XXV, the compiler's introduction to the "
     "lectures, not Tesla writing. The brief's 'earth-potential motors (p. 138)' "
     "sits inside it. This sentence proves it: he is introducing 'the three "
     "Tesla lectures', first person plural, about Tesla in the third"),

    ("We may now proceed to a running review of the lectures themselves",
     119, "0. Provenance (ch. XXV, the compiler labels his own chapter)",
     "the compiler says his chapter is a running review. So the p. 138 "
     "earth-potential passage is a book writer's summary of a demonstration "
     "Tesla gave, not Tesla's own claim. The draft may still use it and must "
     "attribute it. See the flag WHICH PAGES ARE TESLA WRITING"),

    # ---- 2. The table: every 'magnetic generator' hit in the volume.
    ("Mr. Tesla has also devoted his attention to the development of a "
     "pyromagnetic generator of electricity",
     429, "2. The table (the body-text hit, ch. XXXVI)",
     "the volume's prose attaching 'generator' to a magnet word - and the heat "
     "word is in the same sentence, 'pyro'. The trailing footnote digit on "
     "'electricity1' does not break the match, so the phrase is quotable. This "
     "is the machine the table's row 4 is about"),

    ("The enlargement of these ideas will be found in Mr. Tesla's work on the "
     "pyromagnetic generator, treated in this chapter",
     429, "2. The table (the compiler's footnote - the second hit on the same page)",
     "the second of two body hits on printed p. 429, in the compiler's own "
     "footnote on that page. It matters for the count: one page carries two of "
     "the five, which is why '5 hits' and '4 pages' are both true and neither is "
     "an error. It also says the compiler thinks the machine is covered twice in "
     "one chapter"),

    ("Pyromagnetic Generators",
     496, "2. The table (the volume's own index, P entry)",
     "the fifth hit. The volume indexes its own generator under 'Pyromagnetic "
     "Generators', and the page number it gives - 429 - is set on a separate OCR "
     "line, so quote the entry without the number and cite the index leaf; the "
     "joined string comes back fuzzy. Article 08's pin records the same "
     "behaviour for its index lines"),

    ("Generators, Pyromagnetic",
     494, "2. The table (the volume's own index, G entry)",
     "the same entry alphabetised the other way, on a different index leaf. Two "
     "index entries, both pointing at printed p. 429, and nothing anywhere else "
     "in the volume. The strongest single piece of evidence for the article's "
     "claim that the book's only generator-with-magnets is a heat engine: the "
     "book's own indexers filed it that way twice"),

    ("Thermo-Magnetic Motors",
     496, "2. The table (the index entry for the other half of the chapter)",
     "the index line for the 'motors' half of ch. XXXVI's title, pointing at "
     "printed p. 424. Note the annotation this row carries: the same words also "
     "occur on printed p. 6 inside the editor's inventory, so cite p. 496 for "
     "the index and p. 6 for the inventory, never one cite for both"),

    # ---- 3. The quote everyone posts, uncut (ch. XXVII, printed p. 236).
    ("Throughout space there is energy. Is this energy static or kinetic ? If "
     "static our hopes are in vain; if kinetic - and this we know it is, for "
     "certain - then it is a mere question of time when men will succeed in "
     "attaching their machinery to the very wheelwork of nature",
     236, "3. The quote everyone posts (ch. XXVII, the sentence itself)",
     "the sentence the internet prints, in the form the print actually has. Two "
     "things the brief's version gets wrong and the draft must not copy: the "
     "print says 'attaching', not 'attach', and the sentence is not a promise - "
     "it is a conditional about kinetic energy that ends, four sentences later, "
     "in an insult about a machine's efficiency. The print's em dashes are typed "
     "here as ' - ', the form the normaliser folds to. See the flag THE "
     "RUNBOOK'S OWN EXAMPLE COMMAND MISQUOTES THE PRINT"),

    ("Of all, living or dead, Crookes came nearest to doing it",
     236, "3. The quote everyone posts (the sentence the posts cut)",
     "the sentence immediately after the famous one, and the reason the passage "
     "is about a machine at all. Crookes is named, so the next quote has a "
     "subject. No internet version of the quote includes this line"),

    ("His radiometer will turn in the light of day and in the darkness of the "
     "night; it will turn everywhere where there is heat, and heat is everywhere",
     236, "3. The quote everyone posts (the radiometer)",
     "what 'attaching machinery to the wheelwork of nature' looks like in the "
     "book: a radiometer running on heat. This makes the passage about a heat "
     "engine, not about magnets - the same category error as the pyromagnetic "
     "beat, running the other way"),

    ("this beautiful little machine, while it goes down to posterity as the "
     "most interesting, must likewise be put on record as the most inefficient "
     "machine ever invented",
     236, "3. The quote everyone posts (the warning)",
     "the beat brief 10 item 3 asks for and the end of the passage: Tesla's own "
     "verdict on the machine he has just held up as the nearest thing to his own "
     "idea. Stop the quote before the exclamation mark - the print sets a space "
     "before it, 'ever invented !', and the glued form is not in the run. "
     "Rejected #2"),

    ("The preceding experiment is only one of many equally interesting "
     "experiments which may be performed by the use of only one wire with "
     "alternations of high potential and frequency",
     236, "3. The quote everyone posts (what the passage is actually about)",
     "the paragraph break lands here: the wheelwork passage is the preface to "
     "the one-wire demonstrations, and the book says so in its own transition. "
     "This sentence lets the article connect brief 10 item 3 to item 4 without "
     "inventing a link"),

    ("we may pass an inappreciable current over the line, and on any point of "
     "the same we are able to obtain a heavy current, capable of fusing a thick "
     "copper wire",
     236, "3. The quote everyone posts (the demonstration on the same page)",
     "Appendix A's p. 236 row. What he actually demonstrated, on the same "
     "printed page as the famous sentence: a small current in, a heavy current "
     "out at any point of the wire. It is a transformer effect, not an energy "
     "claim, and the article must not let the two readings merge"),

    ("However impracticable this plan of working may appear in many cases, it "
     "certainly seems practicable, and even recommendable, in the production of "
     "light",
     236, "4. What he did claim: one wire (his own hedge, same page)",
     "Tesla hedging his own one-wire plan in the same lecture, four paragraphs "
     "after the famous sentence. 'However impracticable ... it certainly seems "
     "practicable' is the register the article should be quoting when it "
     "separates what he claimed from what he demonstrated"),

    ("A perfected lamp would require but little energy, and if wires were used "
     "at all we ought to be able to supply that energy without a return wire",
     236, "4. What he did claim: one wire (the conditional)",
     "'if wires were used at all' - a conditional, not a plan. Brief 10 item 4 "
     "asks for 'what he said, what he demonstrated, what happened', and this is "
     "the 'what he said' half in the weakest form he himself used"),

    # ---- 4. Energy from the medium (ch. XXVII, printed pp. 196-197).
    ("How far the results here borne out are capable of practical applications "
     "will be decided in the future",
     196, "4. What he did claim: energy from the medium (the hedge first)",
     "the sentence that comes before the passage the free-energy posters quote. "
     "He declines to claim a practical application, in the same lecture, on the "
     "page before. If the article quotes pp. 196-197 without this, it has "
     "reproduced the internet's error with better sources"),

    ("there is a possibility of obtaining energy not only in the form of light, "
     "but motive power, and energy of any other form, in some more direct way "
     "from the medium",
     196, "4. What he did claim: energy from the medium (the claim)",
     "the actual proposition, in his words: energy 'in some more direct way from "
     "the medium'. The closest the 1894 book comes to a free-energy sentence, "
     "and it is a possibility claim about a method, not a device. Brief 10 item "
     "4's first entry"),

    ("the time has come when one may utter such words before an enlightened "
     "audience without being considered a visionary",
     196, "4. What he did claim: energy from the medium (he knows how it sounds)",
     "he flags his own claim as visionary, in the impersonal third person ('one "
     "may utter'), to an institution. The honest pivot needs this: the book's "
     "own author tells the audience how the claim will land"),

    ("whirling through endless space with an inconceivable speed, all around us "
     "everything is spinning, everything is moving, everywhere is energy",
     197, "4. What he did claim: energy from the medium (the sentence that "
     "straddles a page break)",
     "Appendix A's pp. 196-197 row, in the form that verifies. The run starts on "
     "printed p. 196 and ends on 197, and its first words are the ones the OCR "
     "cannot read: the scan sets 'AVe are whirling through' at the foot of "
     "p. 196, so Appendix A's 'We are whirling through endless space' does not "
     "verify at all - Rejected #3. Cite p. 197, where the fragment ends and "
     "where check_quotes.py will accept the citation. Read the flag THE OCR "
     "BREAKS THE ONE SENTENCE APPENDIX A QUOTES"),

    ("There must be some way of availing ourselves of this energy more directly",
     197, "4. What he did claim: energy from the medium (the demand)",
     "'there must be' - an assertion about what ought to exist, right after the "
     "description of space as full of energy. The strongest sentence in the "
     "volume for the free-energy reading, and it names no machine, no output and "
     "no method"),

    ("Then, with the light obtained from the medium, with the power derived "
     "from it, with every form of energy obtained without effort, from the "
     "store forever inexhaustible, humanity will advance with giant strides",
     197, "4. What he did claim: energy from the medium (the hope, uncut)",
     "'without effort', 'forever inexhaustible' - the words a free-energy reader "
     "would want, in a sentence about humanity, not about a generator. "
     "'inexhaustible' is 1 hit in the whole volume and it is here; the article "
     "can say that. It is a wish in a lecture close: the paragraph ends by "
     "saying the contemplation of these possibilities 'fills our hearts with "
     "supreme delight'"),

    # ---- 4b. One-wire transmission (brief 10 item 4 names pp. 232 and 267).
    ("An interesting feature of these high frequency currents is that they "
     "allow of operating all kinds of devices by connecting the device with only "
     "one leading wire to the electric source",
     137, "4. What he did claim: one wire (the compiler's version, ch. XXV)",
     "the earliest one-wire statement in the volume, and it is the compiler's, in "
     "the introduction, describing a demonstration. Not in brief 10, which names "
     "pp. 232 and 267; pinned because the 'what happened' half needs the "
     "sequence - the compiler states the practical case first, Tesla states it "
     "twice later in his own voice. Attribute this one to the book, not to Tesla"),

    ("it may be more economical to supply the electrical energy",
     137, "4. What he did claim: one wire (the half that verifies)",
     "the second half of the compiler's p. 137 sentence, cut short because the "
     "print's next words are 'witli one lead', an OCR l-for-i no index folds. "
     "The full sentence is Rejected #4. The draft may quote this half and "
     "paraphrase the rest, or leave p. 137 out and use pp. 232 and 267, which is "
     "what the brief asks for"),

    ("A most curious feature of alternate currents of high frequencies and "
     "potentials is that they enable us to perform many experiments by the use "
     "of one wire only",
     232, "4. What he did claim: one wire (Tesla's own, ch. XXVII)",
     "brief 10 item 4's second entry, in his own voice, in the chapter that "
     "carries the wheelwork passage. Note what the claim is scoped to: "
     "'experiments', with high frequency and high potential. It is not a "
     "power-transmission claim, and the sentence four pages later (p. 236) says "
     "the plan may be impracticable"),

    ("when transmitted through conductors, it follows that, on the whole, it is "
     "better to employ one wire than two",
     267, "4. What he did claim: one wire (the reasoning)",
     "the reasoning behind the one-wire case, in his own lecture, thirty-five "
     "printed pages after p. 232. 'on the whole' is in the sentence and stays in "
     "the quote"),

    ("if motors, lamps, or devices of any kind are perfected, capable of being "
     "advantageously operated by currents of extremely high frequency, "
     "economical reasons will make it advisable to use only one wire, "
     "especially if the distances are great",
     267, "4. What he did claim: one wire (the prediction, and its condition)",
     "brief 10 item 4's third entry. The prediction is real and it is "
     "conditional: it depends on motors and lamps first being 'perfected'. That "
     "is the 'what he said vs what happened' beat in one sentence, and the "
     "article must print the condition, not only the prediction"),

    # ---- 4c. Earth-potential motor (brief 10 item 4 names p. 138).
    ("An experiment of special interest shown by Mr. Tesla, is the running, by "
     "the use of only one insulated line, of a motor operating on the principle "
     "of the rotating magnetic field enunciated by Mr. Tesla",
     138, "4. What he did claim: an earth-potential motor (the demonstration)",
     "what was actually shown, on one insulated line, with the rotating-field "
     "motor - the machine article 07 is about. The compiler wrote it, in the "
     "third person, naming him twice. This is the 'what he demonstrated' half of "
     "brief 10 item 4 for this entry, and it is the honest one: a disc turned on "
     "a bench"),

    ("Experiments of this kind seem to bring it within possibility to operate a "
     "motor at any point of the earth's surface from a central source, without "
     "any connection to the same except through the earth",
     138, "4. What he did claim: an earth-potential motor (the claim)",
     "brief 10 item 4's fourth entry. Read the hedges: 'seem to bring it within "
     "possibility'. The claim is that a thing is possible in principle, not that "
     "a machine was built. Article 10's whole argument is the difference between "
     "those two, so the hedges stay in the quote"),

    ("a grounded wire reaching up to some height would be traversed by a current",
     138, "4. What he did claim: an earth-potential motor (the proposed apparatus)",
     "the apparatus he proposes, in the conditional: 'If, by means of powerful "
     "machinery, rapid variations of the earth's potential were produced, a "
     "grounded wire ... would be traversed by a current'. Nothing in the volume "
     "says it was built. The longer form is Rejected #5 - the OCR breaks its "
     "middle"),

    ("The current might be converted to low tension and used to operate a motor "
     "or other device",
     138, "4. What he did claim: an earth-potential motor (the second conditional)",
     "'might' - a chain of conditionals: if the variations were produced a wire "
     "would carry a current, which might be converted, which might drive a motor. "
     "Four steps, none of them a build. This is what a 19th-century 'energy from "
     "the earth' claim actually looks like in print"),

    ("The experiment, which would be one of great scientific interest, would "
     "probably best succeed on a ship at sea",
     138, "4. What he did claim: an earth-potential motor (the ship)",
     "Appendix A's p. 138 row. He never claims a machine; he says an experiment "
     "would be interesting and would probably work best on a ship. 'best succeed "
     "on a ship at sea' is 1 hit in the volume, here ('ship at sea' is 2, the "
     "other at p. 168 in the same lecture). The internet prints this as Tesla "
     "predicting wireless power; the sentence is about a scientific experiment"),

    ("In this manner, even if it were not possible to operate machinery, "
     "intelligence might be transmitted quite certainly",
     138, "4. What he did claim: an earth-potential motor (what he actually "
     "claims for it)",
     "the claim he does make is about signalling, and he concedes machinery may "
     "not be possible in the same breath. If the article wants one sentence to "
     "show the gap between the myth and the text, this is it"),

    # ---- 4d. A flame without combustion (brief 10 item 4 names p. 167).
    ("But they do not only resemble, they are veritable flames, for they are hot",
     166, "4. What he did claim: a flame without combustion (the argument)",
     "his argument for calling the brush a flame, in his own lecture (ch. XXVI, "
     "May 1891). Pinned to p. 166, not 167: the sentence is on the page before "
     "the one brief 10 names, and the page break falls inside the passage. See "
     "the flag THE FLAME PASSAGE STRADDLES A PAGE BREAK"),

    ("Produced with, say, twenty thousand alternations per second, the heat is "
     "easily perceptible even if the potential is not excessively high",
     166, "4. What he did claim: a flame without combustion (the number)",
     "a worked number attached to a demonstration, on the same page - the "
     "counterweight to the aspirational passages: here he gives a frequency and a "
     "sensory result. Article 11's chapter is the machine that produced such "
     "frequencies and article 06's page is built on this same brush passage; read "
     "the flag THIS BEAT IS ALREADY ANOTHER ARTICLE'S before writing it up"),

    ("a veritable flame, which would give light and heat without any material "
     "being consumed, without any chemical process taking place",
     167, "4. What he did claim: a flame without combustion (the claim)",
     "brief 10 item 4's fifth entry and Appendix A's p. 167 row, in the form "
     "that verifies. Note the conditional 'would give' and that the sentence "
     "begins 'we have a possible way of producing'. The compiler paraphrased the "
     "same idea two chapters earlier in his own words (p. 120, pinned below), so "
     "the article must be clear which voice says what"),

    ("we have a possible way of producing - by other than chemical means - a "
     "veritable flame, which would give light and heat without any material "
     "being consumed, without any chemical process taking place, and to "
     "accomplish this, we only need to perfect methods of producing enormous "
     "frequencies and potentials",
     167, "4. What he did claim: a flame without combustion (the whole "
     "conditional, with its price)",
     "the full sentence including the condition: 'we only need to perfect methods "
     "of producing enormous frequencies and potentials'. The print's em dashes "
     "are typed as ' - '. Print this if the article wants the claim and its "
     "price in one quote"),

    ("it seems strange that after all these centuries past of familiarity with "
     "the flame, now, in this era of electric lighting and heating, we are "
     "finally led to recognize, that since time immemorial we have, after all, "
     "always had",
     167, "4. What he did claim: a flame without combustion (the rhetorical end)",
     "his own joke on the same page: we have always had 'electric light and "
     "heat' at our disposal. Pinned only up to 'had' because the next words are "
     "set by the print in its own quotation marks, which breaks check_quotes.py's "
     "pairing - Rejected #6. Paraphrase the phrase and cite the page"),

    ("the production of a veritable flame by the agitation of electrostatically "
     "charged molecules",
     120, "4. What he did claim: a flame without combustion (the compiler "
     "paraphrases it first)",
     "chapter XXV, the compiler, two chapters and forty-seven printed pages "
     "before Tesla's own sentence. He calls it 'a veritable flame' too, and adds "
     "that it points to a flame consuming no material. Two voices, one idea, two "
     "pages: an article that quotes the compiler's sentence with a p. 167 cite "
     "has invented a Tesla sentence"),

    ("this result points out a way of obtaining a flame which consumes no "
     "material and in which no chemical action whatever takes place",
     120, "4. What he did claim: a flame without combustion (the compiler's "
     "version)",
     "the compiler's wording, which is closer to brief 10's phrase 'a flame "
     "without combustion' than Tesla's is. Pinned so the draft can see which "
     "sentence it is actually quoting"),

    # ---- 5. The pyromagnetic twist (ch. XXXVI, printed pp. 424-431).
    ("a loadstone or iron bar when heated to redness loses its magnetism",
     424, "5. The pyromagnetic twist (the physics the chapter starts from)",
     "the chapter's opening fact, attributed to William Gilbert 'as far back as "
     "the beginning of the seventeenth century'. The machine works because heat "
     "destroys magnetism - which is why it is a heat engine. Brief 10 item 5's "
     "opening"),

    ("since that time the influence of heat on the magnetic metals has been "
     "investigated frequently, though not with any material or practical result",
     424, "5. The pyromagnetic twist (the compiler's verdict before the machine)",
     "the compiler's own assessment in the chapter's first paragraph: this line "
     "of work had produced nothing practical. A verdict inside the book, in 1894, "
     "about this class of machine, and the strongest sentence article 10 has for "
     "the pyromagnetic beat. It is not a verdict on Tesla's machine - read the "
     "flag THE CHAPTER'S OWN VERDICTS, IN ORDER"),

    ("For a man of Mr. Tesla's inventive ability, the problems in this field "
     "have naturally had no small fascination, and though he has but glanced at "
     "them, it is to be hoped he may find time to pursue the study deeper and "
     "further",
     424, "5. The pyromagnetic twist (he only glanced at it)",
     "'though he has but glanced at them'. The compiler, in the same paragraph, "
     "says Tesla barely touched this field. That clause disposes of any reading "
     "of the pyromagnetic generator as Tesla's great project; print it rather "
     "than paraphrase it"),

    ("Meanwhile he has worked out one or two operative devices worthy of note",
     424, "5. The pyromagnetic twist (what the chapter actually claims)",
     "'one or two' and 'worthy of note' - the extent of the claim. No trial, no "
     "output, no installation anywhere in the chapter (see the scoped counts in "
     "THE TABLE). The article may write that the book reports no test; it may "
     "not write that the machine failed (section 4.1)"),

    ("He obtains mechanical power by a reciprocating action resulting from the "
     "joint operations of heat, magnetism, and a spring or weight or other force",
     424, "5. The pyromagnetic twist (what the thermo-magnetic motor is)",
     "the motor half of the chapter in one sentence: heat, magnetism and a "
     "spring. A reciprocating heat engine with a magnetic valve in it. This is "
     "what the 'motors' in the chapter title are, and it makes the pyromagnetic "
     "point without any word search at all"),

    ("the vibration obtained in this manner is very slow owing to the inability "
     "of the iron to follow rapid changes in temperature",
     424, "5. The pyromagnetic twist (the limitation, in the compiler's footnote)",
     "the compiler's footnote explains why these machines are slow: iron cannot "
     "follow rapid temperature changes. A physical limit stated in the book "
     "itself, in 1894, about this class of machine. The 'why it did not catch "
     "on' half can rest on this sentence instead of on speculation"),

    ("In an interview with Mr. Tesla on this subject, the compiler learned of an "
     "experiment which will interest students",
     424, "5. The pyromagnetic twist (where the famous number comes from)",
     "the provenance of the 400-500 figure: the compiler heard about a "
     "demonstration in an interview with Tesla. So the number the internet quotes "
     "as a machine's operating rate is a hearsay demonstration, and the book says "
     "so on the same page. Cite the footnote as the compiler's, not as Tesla's "
     "claim"),

    ("A spirit lamp is placed under the sheet iron piece and when the iron is "
     "heated to a certain temperature it is easily set in vibration oscillating "
     "as rapidly as 400 to 500 times a minute",
     424, "5. The pyromagnetic twist (the spirit lamp)",
     "the demonstration itself: a horseshoe magnet, an L-shaped strip of sheet "
     "iron, a spirit lamp, and a vibration. '400 to 500' is 1 hit in the whole "
     "volume, here. Article 08's pin carries the same sentence for its entry 4; "
     "the two articles must not both present it as a machine's rating. Read the "
     "flag THE 400-500 SENTENCE IS ONE ARTICLE'S CLOSING BEAT AND THE OTHER'S "
     "OPENING"),

    ("The experiment is very easily performed and is interesting principally on "
     "account of the very rapid rate of vibration",
     424, "5. The pyromagnetic twist (what the demonstration was for)",
     "the compiler's note on the demonstration: it is interesting because of the "
     "vibration rate, not because of any power produced. No watts, no output, no "
     "efficiency in the footnote"),

    ("based upon the following laws",
     429, "5. The pyromagnetic twist (the generator claims to rest on physics)",
     "the sentence introducing the two laws the pyromagnetic generator is said to "
     "rest on. Short, but it is the hinge between the table row and the physics, "
     "and it verifies exactly"),

    ("First, that electricity or electrical energy is developed in any "
     "conducting body by subjecting such body to a varying magnetic influence",
     429, "5. The pyromagnetic twist (law one)",
     "the first law is plain induction. Nothing free about it, and the chapter "
     "says so in the same structure it uses to sell the machine. This is the "
     "sentence that lets the article say the pyromagnetic generator is a heat "
     "engine driving an ordinary induction effect"),

    ("the magnetic properties of iron or other magnetic substance may be "
     "partially or entirely destroyed or caused to disappear by raising it to a "
     "certain temperature",
     429, "5. The pyromagnetic twist (law two)",
     "the second law: heat destroys the magnetism. Verifies only through the "
     "space-ignoring index, because the OCR glues 'destroyedor' at a line end; "
     "the print has the space. Annotated in the entry, and the two indices are "
     "set out in the section 'THE THREE WAYS TO COUNT'"),

    ("This principle of operation may be illustrated by a simple experiment",
     429, "5. The pyromagnetic twist (the demonstration the generator rests on)",
     "what the generator is illustrated by: a bar, a coil and a flame, on a "
     "bench. The chapter never moves from the illustration to a machine that was "
     "run"),

    ("Then apply to the iron between the coil and the steel bar a flame or "
     "other source of heat which will be capable of raising that portion of the "
     "iron to an orange red",
     429, "5. The pyromagnetic twist (the flame again)",
     "the heat source in the book's own words: a flame, to orange red, about "
     "600 degrees centigrade. Every version of this machine has fire in it, which "
     "is the point of brief 10 item 5"),

    ("The chief point to be noted is that Mr. Tesla attacked this problem in a "
     "way which was, from the standpoint of theory, and that of an engineer, far "
     "better than that from which some earlier trials in this direction started",
     429, "5. The pyromagnetic twist (the compiler's praise, and its limits)",
     "the footnote praises the theory, not the machine: 'from the standpoint of "
     "theory, and that of an engineer'. The closest thing to a favourable verdict "
     "in the chapter, and it still says nothing about output. Quotable, with the "
     "qualifier kept"),

    ("The chief effort of the inventor was to economize the heat, which was "
     "accomplished by inclosing the iron in a source of heat well insulated, and "
     "by cooling the iron by means of steam, utilizing the steam over again",
     429, "5. The pyromagnetic twist (a boiler, in the footnote)",
     "the design effort was heat management: an insulated heat source and reused "
     "steam cooling. Read with the p. 430 engraving, which shows a firebox, a "
     "fire and a boiler of water, this settles what the machine is. It is the "
     "compiler's footnote, not Tesla's words, and the article must not present it "
     "as his"),

    ("The construction also permits of more rapid magnetic changes per unit of "
     "time, meaning larger output",
     429, "5. The pyromagnetic twist (the only output sentence in the chapter)",
     "'meaning larger output' - a design property with no number attached. The "
     "scoped counts in THE TABLE show what the chapter does not contain: no "
     "'per cent', no efficiency figure, no test. The article may say the chapter "
     "states a design intention and reports no measurement"),

    ("repeated indefinitely, the effect upon the coil being similar to that "
     "which would follow from moving the magnetized bar to and from the end of "
     "the iron bar or plate",
     430, "5. The pyromagnetic twist (the run that starts on the page before)",
     "the first three words are at the foot of printed p. 429, so the quote is "
     "pinned to p. 430, where the rest of it sits and where the citation will be "
     "accepted. The full run across the break is Rejected #7. It matters because "
     "it is the chapter's own description of the machine as a repeating cycle - a "
     "heat engine in the ordinary sense"),

    ("the features of novelty in the invention being, first, the employment of "
     "an artificial cooling device, and, second, inclosing the source of heat",
     430, "5. The pyromagnetic twist (what is claimed as new)",
     "the two features of novelty: a cooling device and an enclosed heat source. "
     "Not a new physics and not a free source: a boiler arrangement. This is the "
     "claim the chapter actually makes, and it is what the engraving on the same "
     "page illustrates"),

    ("Above the fire is a boiler K, containing water",
     430, "5. The pyromagnetic twist (the boiler, in the body text)",
     "the plainest sentence in the chapter, and the one the pyromagnetic beat "
     "should print: there is a fire and there is a boiler of water. A steam "
     "engine's furniture, in a chapter whose title says magnetic"),

    ("There are special advantages in the employment of a cooling device, in "
     "that the metal of the core B is not so quickly oxidized",
     431, "5. The pyromagnetic twist (the chapter's last substantive claim)",
     "an advantage about oxidation, not output. The chapter ends on what the "
     "device is said to make possible, not on what it did"),

    ("whereby the rapidity of the magnetic changes or fluctuations may be "
     "regulated",
     431, "5. The pyromagnetic twist (the chapter's last sentence)",
     "the last words of chapter XXXVI: the rate of change 'may be regulated'. No "
     "trial, no figure, no run, no installation. Article 08's pin records the "
     "same silence for the same chapter; the two articles must say the same thing "
     "about it, in the same scoped words"),

    # ---- 6. What the internet gets wrong.
    ("I trust that the present brief communication will not be interpreted as "
     "an effort on my part to put myself on record as a",
     394, "6. What the internet gets wrong (Tesla on being sold)",
     "chapter XXXI, Tesla's own opening, in the first person: he does not want to "
     "be put on record as a 'patent medicine' man. The phrase inside the print's "
     "own quote marks is Rejected #8. Use this narrowly and keep it narrow: it "
     "is about electrical quackery in medicine, in an 1894 paper on massage, and "
     "it is not Tesla on free energy. Read the flag THE PATENT-MEDICINE SENTENCE "
     "IS NOT ABOUT FREE ENERGY"),

    ("a serious worker cannot despise anything more than the misuse and abuse of "
     "electricity which we have frequent occasion to witness",
     394, "6. What the internet gets wrong (his own words on hype)",
     "the sentence that carries the beat: a serious worker's contempt for the "
     "misuse and abuse of electricity, in his own voice, on a page article 05 "
     "already used for a different purpose. The article may print it as his "
     "general position on electrical hype; it may not stage it as a remark about "
     "free-energy claims, which it is not"),

    # ---- 7. The honest pivot: the book's own measured numbers.
    ("Prof. Anthony in his remarks before the American Institute of Electrical "
     "Engineers, in May, 1888, on the two small Tesla motors then shown, which "
     "he had tested, stated that one gave an efficiency of about 50 per cent, "
     "and the other a little over sixty per cent",
     8, "7. The honest pivot (a measured efficiency, 1888)",
     "the counter-evidence to the premise of the free-energy myth: this book "
     "contains measured efficiencies, cited to a named tester who tested the "
     "machines. Article 07 owns this record (Appendix D 'Efficiency record') and "
     "printed these numbers first; read the flag THE EFFICIENCY RECORD BELONGS TO "
     "ARTICLE 07 before using more than one sentence of it here"),

    ("With some larger motors it was then found practicable to obtain an "
     "efficiency, with the three wire system, up to as high as 94 and 95 per cent",
     8, "7. The honest pivot (the top number in the book)",
     "94-95 per cent. A real, cited, sub-unity number, in a book that never "
     "writes 'free energy' or 'perpetual'. That contrast is the honest pivot in "
     "one line: the book measures how little energy is wasted, which is a "
     "different question from getting something for nothing"),

    ("These interesting figures, which, of course, might be supplemented by "
     "others more elaborate and of later date, are cited to show that the "
     "efficiency of the system has not had to wait until the present late day "
     "for any demonstration of its commercial usefulness",
     8, "7. The honest pivot (why the compiler prints them)",
     "the compiler's stated reason for giving the figures: to show the system's "
     "commercial usefulness was demonstrated long before 1894. 'commercial "
     "usefulness' is 1 hit in the volume, here. The book's own answer to 'did "
     "his machines work', and it is about the alternating-current system, not "
     "about any generator on this site"),

    ("An invention is none the less beautiful because it may lack utility",
     8, "7. The honest pivot (the sentence to be careful with)",
     "the compiler's most quotable line, and the one most likely to be turned "
     "into a thesis about failed inventions. It is the first half of a sentence "
     "whose point is that this inventor's ideas DID carry utility: 'but it must "
     "be a pleasure to any inventor to know that the ideas he is advancing are "
     "fraught with substantial benefits to the public'. Quote the turn as well, "
     "or cut the sentence. See the flag THE BEAUTY-WITHOUT-UTILITY LINE IS HALF "
     "A SENTENCE"),
]

# Considered and not carried forward. Either a form that does NOT pass the gate,
# or a real passage this article should not use; the reason says which.
REJECTED = [
    ("Entered according to Act of Congress in the year 1893 by T. C. MARTIN in "
     "the office of the Librarian of Congress at Washington", -8,
     "the whole copyright line as one quote: fuzzy 0.849 on printed p. -8. The "
     "OCR of the printer's imprint ('Press of Mcllroy & Emmet, 36 Cortlandt St., "
     "N. Y.') and the setting of the line break the middle of the run. The two "
     "halves verify exactly and are pinned above with the cut. A draft printing "
     "the whole line as one quotation fails check_quotes.py in feature-007/t3"),

    ("the most inefficient machine ever invented!", 236,
     "the form with the exclamation mark. The print sets a space before it - "
     "'ever invented !' - and the normaliser keeps that space, so the glued form "
     "is not in the run. The pinned quote stops at 'invented'; if the draft "
     "wants the mark, put it outside the quotation marks, as article 08's pin did "
     "for the p. 258 question mark the scan reads as '{'"),

    ("We are whirling through endless space", 196,
     "Appendix A's first fragment for the pp. 196-197 row, and the form the "
     "series would most naturally copy. NO MATCH at all, exact or fuzzy: the scan "
     "sets the line as 'AVe are whirling through' - a capital W at the start of a "
     "line OCRs as 'AVe'. Nothing in the volume contains 'we are whirling'. The "
     "form that verifies starts at 'whirling through endless space' and is pinned "
     "above. This is the most important row in this file for feature-007/t1: the "
     "quote the plan's own appendix gives cannot be printed as given"),

    ("under certain conditions it may be more economical to supply the "
     "electrical energy with one lead than with two", 137,
     "the compiler's practical conclusion in full: fuzzy 0.982 on p. 137, because "
     "the print's word is 'witli', an OCR l-for-i in 'with' that no normaliser "
     "folds. The first half is pinned above; the conclusion can be paraphrased "
     "with the page cite, or dropped. Do not print this as a quotation"),

    ("a grounded wire reaching up to some height would be traversed by a current "
     "which could be increased by connecting the free end of the wire to a body "
     "of some size", 138,
     "the fuller apparatus description: fuzzy, because the run crosses a line "
     "break the OCR breaks. The short form is pinned above and is enough"),

    ("we are finally led to recognize, that since time immemorial we have, "
     "after all, always had \"electric light and heat\" at our disposal", 167,
     "the full joke. It verifies through the space-ignoring index, but the print "
     "sets 'electric light and heat' in its own double quote marks, and "
     "check_quotes.py's scanner pairs quote marks by walking them: a draft "
     "quotation containing the print's own quotation marks is the case it gets "
     "wrong (article 08's pin hit this with the editor's ' Miscellaneous ' and "
     "started its quote after it). The pinned form stops at 'had'; paraphrase the "
     "phrase and cite p. 167"),

    ("The same operation may be repeated indefinitely", 430,
     "the run as one fragment. 'The same operation may be' is the last line of "
     "printed p. 429 and 'repeated indefinitely' opens p. 430, so the joined "
     "string is not a run on the page this quote would be pinned to. The p. 430 "
     "half is pinned above. A hyphenated citation '(1894, pp. 429-430)' is never "
     "the answer: check_quotes.py's citation regex cannot read a range"),

    ("as a \"patent medicine\" man", 394,
     "the phrase verifies exactly on printed p. 394 - the print sets it in double "
     "quotes - but it is only 19 characters, and inside a draft quotation the "
     "print's own marks break check_quotes.py's pairing the way the p. 167 case "
     "does. The two pinned p. 394 fragments carry the beat without it. If the "
     "draft wants the phrase it must be the whole quoted run, with the print's "
     "marks inside, and that run must be tested with check_quotes.py before it "
     "ships, not assumed"),

    ("No electrical inventor of the present day dealing with the problems of "
     "light and power considers that he has done himself or his opportunities "
     "justice until he has attacked the subject of thermo-magnetism", 424,
     "the most quotable line in ch. XXXVI: fuzzy 0.966 on p. 424 because the OCR "
     "sets the last word as 'thermo-magiietism' (ii for an). The rest of the "
     "sentence is fine; the last word is not. Stopping at 'the subject of' leaves "
     "nothing, so paraphrase. The pinned p. 424 rows use the sentences that do "
     "verify"),

    ("MOTORS AND PYRO-MAGNETIC GENERATORS", 424,
     "the chapter heading, which is the fifth 'magnetic generator' hit and the "
     "reason Appendix D's count is 5 and not 4. It is NOT in the index "
     "check_quotes.py builds: strip_furniture drops short all-caps lines as "
     "running heads, and the heading is set on four short display lines "
     "('CHAPTEK / THERMO-MAGNETIC / XXXVI. / MOTORS AND PYRO-MAGNETIC "
     "GENERATORS.'). With load_pages(clean=False) the same string is 1 hit at "
     "ratio 1.0 on printed p. 424. So the heading can be named and cited, and "
     "cannot be printed inside quotation marks with a page cite. The contents "
     "leaf gives the same title truncated by the OCR to 'PYRO-MAGNETIC RATORS' "
     "(scan file 17) - article 08's pin records that too. See the flag THE "
     "CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE"),

    ("THE INVENTIONS RESEARCHES AND WRITINGS OF NIKOLA TESLA", -9,
     "the title page. Not in the index at all, for the same furniture reason: the "
     "title page is display type and the OCR interleaves it ('THE INVENTIONS "
     "RESEARCHES AND WRITINGS OF NIKOLA TESLA WITH SPECIAL REFERENCE CURRENTS AND "
     "TO HIGH HIS WORK POTENTIAL IN POLYPHASE LIGHTING'). The title page is scan "
     "file 9, printed leaf -9, and it is what the article means by 'the 1894 "
     "first edition'; it can be described and shown as a page-scan crop (brief 10 "
     "asks for the title page), but it cannot be quoted with a page cite. The "
     "copyright leaf, scan file 10, is prose and is pinned above in two verified "
     "halves"),

    ("D. VAN NOSTRAND COMPANY, NEW YORK", -9,
     "the publisher's line on the same title page. Same reason: display type, not "
     "in the index. The publisher belongs in the Sources block, which is where "
     "section 3 puts the full citation anyway"),

    ("attach their machinery to the very wheelwork of nature", 236,
     "the form in section 9 brief 10 item 3 AND the example command in section 8 "
     "step 2 of the runbook. The print says 'attaching', so this string is fuzzy "
     "0.964 on p. 236 and check_quotes.py will call it NOT VERBATIM. The pinned "
     "form is 'in attaching their machinery to the very wheelwork of nature'. "
     "Read this row before writing the article's most important sentence"),

    ("Throughout space there is energy ... the most inefficient machine ever "
     "invented!", 236,
     "the brief's ellipsised form as one quote. The first fragment verifies, the "
     "second does not (Rejected #2), and the cut hides the three sentences that "
     "make the passage a warning. The pin gives the passage in five verified "
     "pieces instead. If the draft wants one long quotation it must be the one "
     "pinned at the head of section 3, with the efficiency sentence as a second "
     "quotation"),

    ("the true electric flame", 121,
     "article 06's pinned phrase, on the same subject in the same volume. Not "
     "re-pinned here: article 06 (tesla-cold-flame.html) is rendered and owns "
     "that beat, including the p. 166-171 brush passages. Article 10's flame "
     "paragraph is one paragraph of context and a link to 06, not a second "
     "telling of it. See the flag THIS BEAT IS ALREADY ANOTHER ARTICLE'S"),

    ("it is better to employ one wire than two. Therefore, if motors, lamps", 267,
     "a stitched form crossing the sentence boundary the print puts between them. "
     "Both halves are pinned separately above; stitching them into one quotation "
     "would be re-punctuating the 1894 text inside quotation marks, which section "
     "3 forbids"),

    ("it is only necessary to raise the temperature of iron at the proper place "
     "and at the proper time", 429,
     "the chapter's own summary of the whole device, and its most quotable "
     "sentence. NO MATCH on p. 429: the OCR sets 'it is only necessary to raise "
     "the temperature of iron at the proper place and at the proper time' across a "
     "line break as 'it is only necessary to raise the temperature of iron at the "
     "proper place and at the proper time' with a hyphenated line ending, and the "
     "run as typed does not appear. The chapter's own words are recoverable from "
     "the pinned law-one and law-two rows, which do verify; paraphrase this one "
     "and cite p. 429"),

    ("magnetic motor", None,
     "the phrase the site's product vocabulary would like the book to contain. "
     "It is never there unqualified: @@mm_raw@@ raw hits (@@mm_raw_pages@@), "
     "@@mm_def@@ on the GATE index (@@mm_def_pages@@), @@mm_keep@@ with "
     "--keep-furniture (@@mm_keep_pages@@). Every one sits inside a hyphenated "
     "compound - 'thermo-magnetic motor(s)' at the contents leaf, in the "
     "editor's inventory at printed p. 6 and in the volume's index at p. 496 - "
     "or inside 'electro-magnetic motor' at printed pp. 46 and 55, and the "
     "p. 46 line is OCR-garbled ('an ordinary form of electroof source magnetic "
     "motor'), so not one of them can be quoted. The p. 55 hit exists only on "
     "the normalised indices: the print hyphenates 'electro-' at the line "
     "break, the normaliser folds it, and the raw text never sets the phrase. "
     "So the article may say the volume never writes 'magnetic motor' "
     "unqualified, and must not imply the words never appear. Measured in the "
     "count table above"),

    ("magnet motor", None,
     "the site's other product phrase. 0 hits on all three indices; "
     "`grep_quote.py --count` prints @@magnet_motor_fuzzy_n@@ anyway, every one "
     "of them the tool's fuzzy fallback clearing its 0.80 floor on unrelated "
     "windows - ratios @@magnet_motor_fuzzy_range@@, and "
     "@@magnet_motor_fuzzy_eg@@. A zero that prints as 18 is the trap this "
     "article's table walks into, so it is recorded here and in the flag "
     "HOW TO READ A COUNT"),

    ("magnetic engine", None,
     "a phrase a reader might expect in an 1894 book. 0 hits on all three "
     "indices; the tool prints @@magnetic_engine_fuzzy_n@@ fuzzy, ratios "
     "@@magnetic_engine_fuzzy_range@@. Not quotable, not countable, and worth "
     "one clause in the method section because it shows what a fuzzy count is"),

    ("free electricity", None,
     "the site's phrase and one of the live pages' titles. 0 hits on all three "
     "indices, and the tool prints @@free_electricity_fuzzy_n@@ too - the one "
     "zero in this table that survives the fuzzy fallback. Pinned as a count, "
     "not a quote: the method table can show it, and the article may say the "
     "phrase is not in the book"),

    ("free", None,
     "the word alone: @@free_raw@@ raw hits, of which @@free_word@@ are the "
     "standalone word, in the forms @@free_forms@@ - and not one of them is "
     "followed by 'energy': 'free energy', 'free-energy' and 'free energ' are 0 "
     "on all three indices. 'free end', 'free circuit', 'free space', 'free "
     "conductor', 'free from'. A reader who searches the word will find it "
     "@@free_raw@@ times and find the phrase never. This is the row that makes "
     "the method section worth writing at all, and it is why the article's "
     "table must give the phrase, not the word"),

    ("unity", None,
     "what a reader searching 'over unity' by halves finds: @@unity_raw@@ raw "
     "hits, and @@unity_word@@ of them is the word 'unity' - all @@unity_raw@@ "
     "sit inside longer words, which the host-word list gives exactly: "
     "@@unity_hosts@@. 'over unity' and 'over-unity' are 0 on all three indices, "
     "and the tool still prints @@over_unity_fuzzy_n@@ fuzzy hits for 'over "
     "unity' at ratios @@over_unity_fuzzy_range@@. The measured version of "
     "section 4.1's rule about not implying the words exist"),

    ("the earth's potential", None,
     "the phrase the p. 138 beat is about, and it IS in the book: "
     "@@earth_phrase@@ raw hit, on printed p. @@earth_phrase_pages@@ ('rapid "
     "variations of the earth's potential were produced'), and the same count "
     "on the normalised indices. What is NOT in the book is the series' own "
     "hyphenated label: 'earth-potential' is @@earth_label@@ hits. The first "
     "draft of this row had those two the other way round and blamed a curly "
     "apostrophe the text does not contain - the scan sets a straight one, and "
     "the phrase verifies on every index. The article may quote the book's "
     "phrase with the p. 138 cite; if it writes 'earth-potential' it has to be "
     "plain that this is the series' word for it, which section 4.1 requires"),

    ("earth-potential", None,
     "@@earth_label@@ hits in the volume. The word in brief 10 item 4 and in "
     "this pin's section names is the series' label, not the book's. Flagged "
     "in WHICH PAGES ARE TESLA WRITING and in the section 4.1 note"),

    ("free-energy", None,
     "the hyphenated form, which the series' own prose uses constantly "
     "(@@plan_hyphen@@ hyphenated and @@plan_space@@ spaced occurrences in "
     "SERIES-PLAN-1894.md itself). 0 hits in the 1894 text, hyphenated or not. "
     "The article's own vocabulary is not the book's, and section 4.1's rule "
     "about not implying the words exist applies to the article's headings too"),
]

FLAGS = [
    ("THE RUNBOOK'S OWN EXAMPLE COMMAND MISQUOTES THE PRINT",
     "section 8 step 2 of SERIES-PLAN-1894.md tells the quote-pin agent to run "
     "python3 books/tools/grep_quote.py \"attach their machinery to the very "
     "wheelwork\" --pages. The print says 'attaching', so that command returns a "
     "fuzzy near-match and no exact hit, and an agent that follows the runbook "
     "literally will pin a quote the gate rejects. The verified form is in "
     "section 3 of this pin. Nothing in the runbook or the plan needs changing - "
     "the runbook is a runbook - but the article's central sentence must be "
     "pinned from this file, not from the plan's example"),

    ("THE OCR BREAKS THE ONE SENTENCE APPENDIX A QUOTES",
     "Appendix A's pp. 196-197 row gives 'We are whirling through endless space, "
     "with an inconceivable speed...'. The scan sets the line at the foot of "
     "printed p. 196 as 'AVe are whirling through', so no index of this OCR file "
     "contains 'we are whirling' and the fragment cannot be printed as the plan "
     "gives it. Two consequences for feature-007/t1: quote the run from "
     "'whirling through endless space' and cite p. 197, and do not describe the "
     "sentence as beginning on p. 196 in a way that implies the words 'We are' "
     "were checked. If the series ever wants to print the sentence complete, it "
     "has to say the scan is unreadable at that point, which is a sentence about "
     "the source, not about Tesla"),

    ("THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE",
     "Appendix D counts 5 'magnetic generator' hits: printed pp. 6, 424, 429 "
     "twice, 496. The p. 424 hit is chapter XXXVI's display heading, which the "
     "GATE index does not contain (strip_furniture drops short all-caps lines as "
     "running heads), and which the KEEP index does. So the same fact prints as "
     "5 or as 4 depending on the index. Article 08's pin records the same "
     "split - it counts 4 through grep_quote.py's default index, names pp. 6, "
     "429 and 496, and says Appendix D's 5 is right because the fifth is the "
     "heading, present with --keep-furniture. The two pins must not appear to "
     "disagree: article 10 owns this table, so it prints 5, names the heading, "
     "and says which index produces 4. Article 08's page is rendered and "
     "feature-007/t3 must not edit it; if the two pages would visibly "
     "disagree, fix the wording on article 10's side and raise the article 08 "
     "change separately (section 5 says a rendered page is frozen)."),

    ("THE CLI AND THE GATE SHARE AN INDEX BY DEFAULT; --keep-furniture IS THE "
     "DIFFERENCE",
     "The first version of this flag said grep_quote.py builds its index with "
     "load_pages(clean=False) and check_quotes.py with load_pages(clean=True), "
     "and built a method section on the difference between them. That is "
     "backwards about the CLI: grep_quote.py's default is clean=True - the same "
     "index check_quotes.py builds - and clean=False is what the "
     "--keep-furniture switch asks for. Verified on the date above: "
     "`grep_quote.py \"magnetic generator\" --count` prints 4 hits at pp. 6, "
     "429, 496, and the same command with --keep-furniture prints 5 and adds "
     "p. 424. So the CLI's default count and the gate's count are one number, "
     "and a writer who runs the tool without a flag is looking at the index the "
     "gate will use. What is still true, and is the reason the flag stays: "
     "furniture changes which strings exist at all (the chapter heading, the "
     "title page), and the tool's fuzzy fallback can call a near-match 'found' "
     "where check_quotes.py would fail the quote. Every number in this pin is "
     "labelled with the index that produced it. Do not quote a tool result in "
     "the draft without re-running it through check_quotes.py first"),

    ("HOW TO READ A COUNT",
     "grep_quote.py --count falls back to a fuzzy match at a 0.80 ratio floor, "
     "so a term that is not in the book at all can print a non-zero count: "
     "'magnet motor' is 0 on all three indices and the tool prints "
     "@@magnet_motor_fuzzy_n@@ (ratios @@magnet_motor_fuzzy_range@@); 'over "
     "unity' is 0 and it prints @@over_unity_fuzzy_n@@ "
     "(@@over_unity_fuzzy_range@@); 'magnetic engine' is 0 and it prints "
     "@@magnetic_engine_fuzzy_n@@ (@@magnetic_engine_fuzzy_range@@); 'free "
     "electricity' is 0 and it prints @@free_electricity_fuzzy_n@@. The "
     "article's table is built entirely from terms where this matters, so the "
     "draft must print the counts this script measures (raw substring counts and "
     "exact-index counts) and never a tool's --count output. If the draft says "
     "'zero', it must be a zero that survives the fuzzy fallback, and the "
     "method section should say in one sentence that a search tool can report "
     "hits for words that are not there - that is the most useful thing a "
     "reader could take from this article"),

    ("THE PYROMAGNETIC FIGURE IS THE ONLY ONE BRIEF 10 NAMES, AND IT IS THE "
     "WRONG FIGURE FOR THE JOB",
     "brief 10's figure list asks for 'tesla1894-p424-fig* (pyromagnetic)'. "
     "Printed p. 424 has no engraving at all - the chapter opens with prose and "
     "footnotes, and its plates are on printed pp. 425-430 - so there is no "
     "file that matches that glob. The crop of the machine itself is "
     "tesla1894-p430-fig242.webp - printed p. 430, scan file 448, book fig. "
     "242, verified:true in new_content/1894-series/index.json - which "
     "article 08 already publishes as its figure 3. Section 6.6 forbids the same "
     "engraving on two pages unless the caption differs. Either article 10 uses "
     "that plate with a caption about the fire and the boiler, which is a "
     "different point from article 08's, or it uses the page-scan crop of p. 236 "
     "that brief 10 also asks for, which does not exist yet and has to be cut. "
     "Fig. 243 has no clean crop - only the superseded two-figure band "
     "tesla1894-p448-fig1-fig243.webp. See the figure notes below"),

    ("THE 400-500 SENTENCE IS ONE ARTICLE'S CLOSING BEAT AND THE OTHER'S OPENING",
     "article 08's entry 4 ends on the spirit-lamp footnote, and its pin records "
     "that footnote as showing the apparatus is 'a demonstration, not the "
     "chapter's machine'; brief 10 item 5 opens article 10's pyromagnetic "
     "section with the same footnote. Both articles may quote it - it is the only "
     "number in the chapter - but they must not both present it the same way. "
     "Article 08 has it as the proof that the book reports no test. Article 10's "
     "use has to be different: the number is a vibration rate heard in an "
     "interview, and the internet repeats it as a machine's rating. If the "
     "overlap feels like duplication, article 10 should cut its own quotation and "
     "link to article 08, which is what section 5's link map is for"),

    ("THE CHAPTER'S OWN VERDICTS, IN ORDER",
     "the volume prints three judgements about this chapter's subject, about "
     "three different things, and the article must not merge them into one "
     "sentence about 'the book's opinion'. In the order they are printed: "
     "(1) printed p. 424, first paragraph, about the FIELD - 'the influence of "
     "heat on the magnetic metals has been investigated frequently, though not "
     "with any material or practical result'; (2) the same page, about TESLA'S "
     "ATTENTION - 'though he has but glanced at them, it is to be hoped he may "
     "find time to pursue the study deeper and further', which is the compiler "
     "wishing a busy man more time, not grading his machine; (3) printed "
     "p. 429, in the footnote, about the APPROACH - he 'attacked this problem "
     "in a way which was, from the standpoint of theory, and that of an "
     "engineer, far better than that from which some earlier trials in this "
     "direction started', praise of a starting point that says nothing about "
     "output. All three are the compiler's, in the third person, inside Part "
     "III; article 08's flag PART III IS THE EDITOR'S TEXT, IN THE THIRD "
     "PERSON, ABOUT TESLA'S DEVICES says who is writing, and article 10 has to "
     "keep that attribution inside every one of the three. None of them is a "
     "verdict on the machine's performance, and none supports 'the book called "
     "it a failure': the chapter's last sentence (printed p. 431) is about what "
     "could be regulated, and the finding is that no measurement is reported, "
     "which is not the same as a negative one"),

    ("THE EFFICIENCY RECORD BELONGS TO ARTICLE 07",
     "Appendix D gives the p. 8 efficiency record to article 07, which is "
     "rendered and printed the 50/60 and 94-95 per cent figures. Brief 10 item "
     "7 does NOT ask for the book's efficiencies - it asks for 'what actually "
     "works off-grid, what the plans on this site are and are not' and names "
     "three commercial pages. The p. 8 rows in this pin are this pin's own "
     "support for that beat: a measured, cited, sub-unity number is the "
     "counter-evidence to the premise of the myth, and it is the book's own "
     "answer to 'did his machines work'. Article 10 may cite the record and "
     "quote at most one short fragment of it, with a link to article 07; it "
     "must not re-tell the Anthony test. The sentence that is genuinely article "
     "10's is the compiler's reason for printing the figures - 'cited to show "
     "that the efficiency of the system has not had to wait ... for any "
     "demonstration of its commercial usefulness' - because that is about what "
     "the book chose to measure, which is this article's subject"),

    ("THIS BEAT IS ALREADY ANOTHER ARTICLE'S",
     "the flame-without-combustion beat (brief 10 item 4, p. 167) is article 06's "
     "subject: tesla-cold-flame.html is rendered and its pin carries pp. 120-121, "
     "166-171, including 'the true electric flame' and the p. 166-167 brush "
     "sentences. Article 10's flame entry is one paragraph in a list of things he "
     "did claim, and it must link to article 06 rather than re-open the "
     "argument. The p. 166 'veritable flames, for they are hot' and the p. 167 "
     "'would give light and heat without any material being consumed' rows are "
     "pinned here because brief 10 names those pages; if the draft finds itself "
     "writing more than a paragraph about flames, it has taken over article 06's "
     "job"),

    ("WHICH PAGES ARE TESLA WRITING",
     "brief 10's beats mix three different texts and the draft must not print "
     "'Tesla wrote' for all of them. Ch. I (pp. 3-16) is the editor's "
     "introduction. Ch. XXV (pp. 119-144) is the compiler's running review of the "
     "lectures - the p. 137 and p. 138 earth-potential passages are in it, and "
     "the compiler's own footnotes say so. Chs. XXVI (from p. 145) and XXVII "
     "(from p. 198) are the printed texts of two lectures, May 1891 and February "
     "1892, and the pp. 196-197, 232, 236, 267 passages are in those. Ch. XXXVI "
     "(pp. 424-431) is the compiler's chapter on a device, with footnotes the "
     "compiler says came from an interview. Ch. XXXI (p. 394) is Tesla's own "
     "paper. Ch. I p. 8 is the editor's. The p. 429 'pyromagnetic generator' "
     "sentence is the compiler's; so is the second hit on the same page. The pin "
     "marks each row's voice in its section name and its why"),

    ("FOUR TEXTS, FOUR DATES",
     "the volume's own dates: entered at the Library of Congress 1893 (copyright "
     "leaf), title page 1894, the Columbia lecture May 20 1891 (p. 145), the IEE "
     "London lecture February 1892 (p. 198), the Anthony efficiency test May 1888 "
     "(p. 8). Section 3's quote style prints 'Tesla wrote in 1892', which is only "
     "right for the IEE lecture. The draft must date each quote from this list or "
     "not date it at all"),

    ("THE FLAME PASSAGE STRADDLES A PAGE BREAK",
     "brief 10 names p. 167 for the flame claim, but 'they are veritable flames, "
     "for they are hot' is on printed p. 166 and the sentence that continues onto "
     "p. 167 begins 'we have a possible way of producing'. Each fragment is "
     "pinned to the page it sits on. A draft that cites p. 167 for the p. 166 "
     "sentence fails check_quotes.py, and a draft that cites 'pp. 166-167' for "
     "either fails too, because the citation regex cannot read a range"),

    ("THE PATENT-MEDICINE SENTENCE IS NOT ABOUT FREE ENERGY",
     "the p. 394 'patent medicine' passage is Tesla rejecting being advertised as "
     "a cure-all, in a paper on electrotherapy. It is the only place in the volume "
     "where Tesla complains about being sold, and it is tempting as a closer for "
     "an article about free-energy claims being made in his name. It is not that: "
     "it is about medical advertising, and section 4.1 forbids carrying a quote "
     "past what its page supports. Use it as his general position on electrical "
     "hype, in one or two sentences, with the subject named, or not at all"),

    ("THE BEAUTY-WITHOUT-UTILITY LINE IS HALF A SENTENCE",
     "'An invention is none the less beautiful because it may lack utility' is the "
     "compiler's most quotable line and it is the opposite of what it looks like: "
     "the sentence goes on to say this inventor's ideas 'are fraught with "
     "substantial benefits to the public'. Quoting the first clause as the "
     "book's view of failed machines would be a misreading of the p. 8 paragraph, "
     "and it would be the article's own thesis talking through Tesla's editor. "
     "Print the turn or cut the line"),

    ("THE WORD 'TEST' IS THE WHOLE ARGUMENT AND THE COUNTS ARE IN THIS FILE",
     "brief 10 item 5 asks whether the chapter gives a test, a figure, a trial "
     "run. The scoped counts over printed pp. 424-431, and every non-zero hit "
     "with the sentence it sits in, are in the section 'What chapter XXXVI does "
     "and does not report' above, and the answer is a real number, not a "
     "hunch: 'test' 0, 'per cent' 0, "
     "'efficiency' 0, 'output' 1 and that one is a design property with no "
     "number on it. Read the two non-zeros before writing the beat: "
     "'experiment' is 3 and 'result' is 5 in that range, and they are the "
     "compiler's horseshoe-magnet footnote, the chapter's own illustration on "
     "p. 429, and the word 'result' inside ordinary sentences - so the "
     "draft may NOT write that the chapter mentions no experiments or no "
     "results. What it may write, and what the book says itself at printed "
     "p. 424, is that this line of work 'has been investigated frequently, "
     "though not with any material or practical result', and that the chapter "
     "reports a design and an illustration and no measurement of the machine. "
     "Article 08's pin records the same finding in other words - 'no output, no "
     "efficiency, no run, no trial, no commercial result anywhere in "
     "pp. 424-431' - and article 10 must not contradict it or make it "
     "stronger: 'it failed' is not available (section 4.1)"),

    ("THE LIVE PAGES SAY MORE THAN THE 1894 TEXT CAN SUPPORT",
     "the three pages brief 10 item 7 links to make the claims printed, "
     "verbatim and measured, in the section 'What the three live pages actually "
     "claim' above - a 5x energy figure, a patent attribution to an 1894 "
     "bifilar coil, a 30-50 percent bill reduction, a perpetual-motion "
     "generator. "
     "None of those words is in the 1894 book: 'bifilar', '512,340', 'coil for "
     "electromagnets', 'free energy', 'perpetual' and 'over unity' are all 0 "
     "hits, measured. Article 10's job is to report what the book does and does "
     "not say about the devices the site sells, and it must not launder a live "
     "page's claim into a historical one by quoting the book next to it. The one "
     "live-page claim the 1894 text can actually meet is the p. 429 "
     "'pyromagnetic generator' phrase, and even that is a heat engine"),

    ("THE WORD-SEARCH PAGE DOES NOT EXIST YET",
     "brief 10's closing beat and section 5.2 row 10 both link to "
     "tesla-1894-word-search.html, which is feature-008/t2 and still pending. "
     "Article 10's table is the same measurement that page will publish, so the "
     "link is required by the brief and cannot be checked until feature-008/t2 "
     "renders. Do not invent a different target and do not drop the link: note it "
     "in the draft's Sources block as pending, and let feature-008/t3's "
     "check_quotes run be the moment the link is verified. Articles 05 and 08 "
     "likewise have deferred out-links to article 10 (section 5.2 rows 5 and 8), "
     "which feature-007/t3 may add but must not assume"),
]

FIGURE_NOTES = [
    "BRIEF 10'S FIGURE LIST IS WRONG ON ONE ITEM AND MISSING ON TWO. It asks for "
    "'page-scan crop of p. 236 (the radiometer passage), tesla1894-p424-fig* "
    "(pyromagnetic), title page'. Printed p. 424 carries no engraving at all - "
    "chapter XXXVI opens with prose and footnotes, and its plates are on printed "
    "pp. 425-430. The p. 236 crop does not exist yet. The title-page crop does "
    "exist, website/assets/tesla1894/scan-title-page.webp, and the hub page 00 "
    "already uses it as its card image (new_content/1894-series/index.json, "
    "figures[0], verified:false). So of the three named items, one is "
    "mis-numbered, one must be cut, and one is already used elsewhere.",

    "THE CROP THAT MATTERS IS THE PAGE SCAN OF P. 236, AND §6.6 SOURCING ORDER 4 "
    "IS THE RULE THAT ALLOWS IT. §6.6 lists 'Page-scan crop of the 1894 page "
    "itself when the words are the artefact (used in 05 p. 394 and 10 p. 236)' - "
    "the plan already named this crop for this article. There is no engraving on "
    "printed p. 236 and none in the surrounding pages that belongs to the "
    "passage: the nearest crops in website/assets/tesla1894/manifest.csv are "
    "p252-fig1.webp (printed p. 234, a make-and-break apparatus, a dark plate "
    "whose QC note says the text is legible only after -negate -auto-level) and "
    "p261-fig1-fig147.webp (printed p. 243, an incandescent-lamp figure). Neither "
    "has anything to do with the wheelwork sentence. Cut the crop from "
    "books/pdf-pages-tesla-1894/page-254.pdf (printed 236 = scan file 254, "
    "verified present) following the scan-p346-detail.webp precedent recorded in "
    "index.json line 479: 250 ppi, about 821x1073, kept inside the 400 KB "
    "article gate. Name it scan-p236.webp, the convention the two existing "
    "page-scan crops use (scan-p486.webp, scan-p346-detail.webp - printed page, "
    "not scan file). Caption it as the page the passage is on, and say what the "
    "reader can see: the running head, the printed folio 236, and the paragraph "
    "that ends in the efficiency sentence. The crop is the article's best figure "
    "because the article's claim is about words on a page.",

    "WHAT THE P. 236 CROP MUST BE CHECKED AGAINST BEFORE IT IS USED. The crop "
    "will be read against the six p. 236 quotes in this pin, the way article 03's "
    "scan-p486.webp was checked against its six p. 486 quotes (index.json line "
    "62: 'Ch. XLIII head + printed 486 visible; the six p.486 quotes match the "
    "page image'). Two things to confirm visually: that the printed folio 236 is "
    "inside the crop, and that the print really does say 'attaching' where the "
    "OCR index says 'attaching' and the plan's brief says 'attach'. The second is "
    "the whole point of the article's central quote and a page image settles it "
    "in a way no index can. Record the reading in the frontmatter per "
    "feature-007/t2's criteria, not in books/tmp/.",

    "THE PYROMAGNETIC CHAPTER HAS CROPS ON DISK AND ONLY ONE IS CLEAN AND "
    "UNCLAIMED. "
    "@@ch36_crop_count@@ files in website/assets/tesla1894/ resolve to a "
    "printed page in 424-431, measured from the directory and both manifests on "
    "the date above: @@ch36_crop_list@@. The extractor rows are named by scan "
    "file and their printed page comes from the manifest; the one re-crop is "
    "named by printed page, which is why counting one manifest and listing the "
    "other gets the number wrong both ways. Fig. 242 is the pyromagnetic "
    "generator itself - a tube bundle standing in a firebox with a fire drawn "
    "under it and a boiler above - and §6.6 forbids the same engraving on two "
    "pages unless the caption differs. Article 08's caption names the machine as "
    "the thing the phrase is attached to; article 10's point about the same "
    "plate is the fire and the boiler, which is a different caption for a "
    "different argument. That is allowed by §6.6 but it is thin twice, and the "
    "alternative - the p. 426 plate, which shows the "
    "thermo-magnetic motor half of the chapter and is not used by any rendered "
    "page - is cleaner. Decide at feature-007/t2 with the render open, not from "
    "the manifest.",

    "DO NOT TRUST THE FIGURE NUMBER IN THE MANIFEST FOR THE p. 425 PLATE, AND "
    "THE QC ROW SAYS SO ITSELF. manifest_qc.csv on p443-fig1-fig281.webp: "
    "'Figure number 281 is genuine for p.425. NOT SETTLED, marked 2026-10-17 "
    "(feature-006/t2). The text layer of printed p.425 sets three printed "
    "captions, FIG. 231., FIG. 232. and FIG. 233., while the body line on that "
    "same page reads In Fig. 281 the permanent magnet N is connected with a "
    "frame ... the same scan misreads 3 as 8 twice nearby'. §6.6 says read the "
    "figure number off the printed page in the scan. If article 10 uses that "
    "plate it must read the caption at 500 ppi first and caption it by what the "
    "plate shows, not by a number from the CSV. The same warning applies to "
    "p445-fig1-fig287.webp, whose caption spans two figure numbers.",

    "THE TITLE PAGE IS ALREADY THE HUB'S CARD IMAGE. scan-title-page.webp is "
    "front-matter scan file 9 and index.json marks it verified:false. Brief 10 "
    "asks for it as article 10's provenance figure. Reusing it needs a different "
    "caption (§6.6), and the honest one for article 10 is the imprint - 'entered "
    "according to Act of Congress, 1893; title page 1894' - which is a different "
    "point from the hub's. If feature-007/t2 does re-open it, the reading has to "
    "be recorded and the verified flag set, because the hub's entry is still "
    "false. A cheaper option: the copyright leaf, scan file 10, which is prose "
    "and is the page the two pinned provenance quotes come from; it has never "
    "been cropped and nothing else uses it.",

    "TWO FIGURES MINIMUM, THREE MAXIMUM, AND THE MIDDLE ONE IS THE HARDEST. "
    "§6.6 wants 2-3 body images, figure 1 within the first three H2s, figure 2 "
    "mid-article, figure 3 near the close. For this article the natural set is: "
    "(1) the p. 236 page scan in the section that quotes the sentence, (2) a "
    "pyromagnetic chapter plate in the pyromagnetic section, (3) optionally the "
    "title page or copyright leaf in the method section. The word-search table "
    "itself needs no figure - it is a table, and a screenshot of a terminal "
    "would be the thin option §6.6 rules out.",
]

LINK_NOTES = [
    "OUT-LINKS REQUIRED BY §5.2 ROW 10: magnetic-generator-scam.html, "
    "tesla-magnetic-generator-worth-it.html, free-electricity-from-magnets.html, "
    "05 (tesla-high-frequency-massage.html), 08 (tesla-weird-inventions-1894.html). "
    "All five exist. qa_page.py needs >= 4 internal links (SERIES-PLAN-1894.md "
    "line 1134), so the five named targets are enough on their own.",

    "THE WORD-SEARCH LINK IS REQUIRED AND CANNOT RESOLVE YET. feature-007's own "
    "criteria say 'it links to tesla-1894-word-search.html and to 05 and 08 per "
    "§5.2, and those links resolve', and §9 brief 10 item 8 asks for 'a link to "
    "the appendix page that proves the word search (Tier 6)'. That page is "
    "feature-008/t2 and is still pending, and no file website/tesla-1894-word-"
    "search.html exists. Two consequences: the draft must carry the link (do not "
    "substitute the hub or the plates page), and feature-007/t3's qa_page run "
    "will fail on it unless feature-008/t2 has landed first. This is the one "
    "cross-feature dependency in this article and it is worth raising at "
    "feature-007/t1 rather than discovering at t3. The table in this pin is the "
    "same measurement that page will publish, so whoever writes feature-008/t2 "
    "should be handed this file.",

    "IN-LINKS THIS PAGE NEEDS, AND WHO OWES THEM. §5.2 row 10 says article 10 "
    "must be linked from 04, 05, 08, the hub and magnetic-generator-scam.html. "
    "Checked on 2026-10-17: the hub's article.md already links it twice "
    "(new_content/1894-series/00-hub/article.md lines 36 and 101); 05's "
    "article.md line 49 says its third out-link is to this page and is NOT "
    "placed because this page does not exist yet - 'that third target is NOT "
    "deferred by choice', it writes, because linking it now would fail "
    "qa_page.py's dead-link gate at t3; 08's article.md line 416 says the same "
    "about its closer. Nothing in website/ links to "
    "tesla-free-energy-what-he-said.html yet - grep over website/ returns "
    "nothing. Article 04's §5.2 out-link list does not include 10 even though "
    "row 10 lists 04 as a required in-link; that is a plan inconsistency, not "
    "something feature-007 can fix by itself.",

    "THE RECIPROCAL COUNT IS THE GATE, NOT THE OUT-LINK COUNT. qa_page.py wants "
    ">= 4 internal links with >= 3 of them to pages that link back. Article 10's "
    "five §5.2 targets give the four; the reciprocals available are 05, 08 and "
    "magnetic-generator-scam.html, and none of the three currently links here. "
    "05 and 08 have the deferred link written into their own article.md as a "
    "promise to this page, so the reciprocals arrive when those deferred links "
    "are placed - which is a08-wirecommit's and 05's wiring, not feature-007's. "
    "feature-007/t3 must check the count, not assume it; if it is short, the "
    "fix is to place the deferred links, which is allowed, and not to add links "
    "the plan does not list.",

    "LINK THE FLAME SENTENCE TO 06 AND THE MOTOR SENTENCE TO 07, EVEN THOUGH "
    "§5.2 does not ask for them. The p. 166-167 flame beat is article 06's subject and the "
    "p. 138 rotating-field motor is article 07's; both articles are rendered. "
    "§5.2 row 10 does not list 06 or 07 as out-links, and adding links beyond the "
    "map is allowed by the >= 4 rule but changes the reciprocal arithmetic. The "
    "cheaper move is to name those pages in prose without a link, or to link and "
    "accept that the reciprocal count then depends on 05/08/09 wiring. Decide at "
    "t1 with the reciprocal count in front of you, and record the choice in "
    "index.json the way 08's article.md recorded its deferred link.",

    "THE THREE COMMERCIAL PAGES ARE THE POINT OF THE ARTICLE, NOT A FOOTER. "
    "Brief 10 item 7 is 'what actually works off-grid, what the plans on this "
    "site are and are not', and the three links go in that section, adjacent to "
    "the paragraphs that read their claims. §4.1's guardrail is the constraint: "
    "no sentence may claim anything about what the product can do that is not "
    "already on a live page. The section 'What the three live pages actually "
    "claim' above prints, verbatim and measured, what those pages do claim, so "
    "the draft can stay inside them.",

    "ONE OF THE THREE PAGES MAY BE ABOUT TO CHANGE. §9 brief 10's header says "
    "'Slot depends on O2 ... If O2 = C, this brief becomes a rewrite of "
    "magnetic-generator-scam.html instead, and the data itself moves to "
    "tesla-1894-word-search.html'. The feature record settles it: feature-007 is "
    "'Article 10 ... (O2 = B)', and t1 asks for the softer title 'What Tesla "
    "Actually Wrote About Free Energy' (43 chars), published after 03/01/07. So "
    "magnetic-generator-scam.html stays a separate live page and this article "
    "links to it rather than replacing it. If anyone reopens O2, this pin does "
    "not change - the quotes and counts are the same evidence either way - but "
    "the link map does.",
]


def raw_window(body: str, frag: str, span: int = 200) -> str:
    """Show the scan's own text around a fragment.

    Same trick as the article 02/04/05/06/08 generators: the anchor is the
    longest literal run of the fragment the raw page really contains, so the
    printed fragment always sits inside the window.
    """
    words = frag.split()
    tries = ([words] + [words[:n] for n in range(len(words) - 1, 2, -1)]
             + [words[i:i + 4] for i in range(len(words) - 3)])
    for seq in tries:
        pat = re.compile(r"\s*".join(re.escape(w) for w in seq))
        m = pat.search(body)
        if m:
            a = max(0, m.start() - span)
            b = min(len(body), m.end() + span)
            return (("..." if a > 0 else "") + " ".join(body[a:b].split())
                    + ("..." if b < len(body) else ""))
    return ("(not located in the raw page text; the fragment matched only with "
            "spaces ignored - see grep_quote.py)")


def index_hits(index, term: str):
    """(total, {printed_page: n}) for a term over a built grep_quote index.

    The term goes through grep_quote.normalise first, which is what makes the
    count case-insensitive and folds a hyphen at a line break. That folding is
    also why an index count and a raw grep count can differ, and this file
    prints both rather than choosing one.
    """
    ntext, spans, _words = index
    needle = gq.normalise(term)
    per = {}
    total = 0
    pos = 0
    while True:
        i = ntext.find(needle, pos)
        if i < 0:
            break
        total += 1
        for _fp, pp in gq.pages_for(spans, i, i + len(needle)):
            per[pp] = per.get(pp, 0) + 1
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
    for term, (lo, hi) in SCOPED_TERMS:
        r, rp = raw_hits(pages_keep, term, lo, hi)
        scoped.append((term, f"pp. {lo}-{hi}", r, rp))
    return rows, scoped


def page_stats():
    """The size claims brief 10 item 1 prints: measured, not typed."""
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
        "words in the search index after furniture stripping":
            len(idx_clean[2]),
    }


def strip_tags(html_text: str) -> str:
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html_text)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    return " ".join(html.unescape(t).split())


def live_page_data():
    out = []
    for name in LIVE_PAGES:
        path = SITE / name
        if not path.exists():
            out.append((name, None, [], []))
            continue
        text = strip_tags(path.read_text(encoding="utf-8", errors="replace"))
        counts = [(t, text.lower().count(t.lower())) for t in LIVE_TERMS]
        claims = []
        for page, pat, label in LIVE_CLAIMS:
            if page != name:
                continue
            m = re.search(pat, text)
            claims.append((label, m.group(0).strip() if m else None))
        out.append((name, len(text.split()), counts, claims))
    return out


def figure_crops(lo, hi):
    """Crops on disk that touch a printed-page range, read out of the site.

    manifest.csv names the extractor crops and gives their printed page; the
    500 ppi re-crops are appended to manifest_qc.csv only, and are named by
    PRINTED page where the extractor files are named by SCAN file (article 08's
    whole-pin pass hit exactly this). A figure note that counts one manifest and
    lists the other gets the number wrong both ways, so this reads the "
    directory and both manifests and says which kind each file is.
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
            # An extractor crop: the name is the SCAN file and the manifest row
            # gives the printed page, which is the only authority here.
            pp = int(man[p.name]["printed_page"])
            kind = (f"extractor crop, manifest.csv row {n}"
                    f"->{pp}")
            named_by = "scan file"
        else:
            # A re-crop: named by PRINTED page (article 08's whole-pin pass
            # established that for p480-fig298 / p482-figs300-308), and it is
            # in manifest_qc.csv or on disk alone.
            pp = n
            kind = ("re-crop, manifest_qc.csv only" if p.name in qc
                    else "on disk, in neither manifest")
            named_by = "printed page"
        if not (lo <= pp <= hi):
            continue
        found.append(f"{p.name} (printed p. {pp}; named by {named_by}; {kind})")
    return found


def measure_claims(pages):
    """Every count this file states OUTSIDE the two count tables.

    The REJECTED rows, the prose between sections and the FLAGS used to type
    these numbers by hand, and six of them had drifted from the text they
    describe. They are measured here and interpolated into the prose at render
    time through fill(), so a sentence cannot outlive the run that produced it
    (feature-006/a08-qpdone's failure mode, caught one step earlier: that pass
    re-measured numbers only after they had been written down).
    """
    idx_def = gq.build_index(pages)                     # clean=True = CLI default
    idx_keep = gq.build_index(gq.load_pages(TXT, clean=False))   # --keep-furniture
    allraw = "\n".join(raw for _f, _p, _i, raw, _b in pages)

    def fuzzy(term):
        key = term.replace(" ", "_")
        hits = gq.find_hits(idx_def, gq.normalise(term))
        if not hits:
            return {f"{key}_fuzzy_n": 0, f"{key}_fuzzy_range": "n/a",
                    f"{key}_fuzzy_eg": "no window clears the floor at all"}
        rs = sorted(h["ratio"] for h in hits)
        eg = " ".join(gq.context(idx_def[0], hits[0]["offset"], 40).split())
        return {f"{key}_fuzzy_n": len(hits),
                f"{key}_fuzzy_range": f"{rs[0]} to {rs[-1]}",
                f"{key}_fuzzy_eg": (
                    f"the best of them, {hits[0]['ratio']}, sits on printed "
                    f"p. {hits[0]['printed_page']}: '{eg}'")}

    def standalone(term):
        return len(re.findall(rf"(?<![a-z]){re.escape(term)}(?![a-z])",
                              allraw, re.I))

    def host_words(term):
        return ", ".join(sorted({m.group(0).lower() for m in re.finditer(
            rf"[a-z]*{re.escape(term)}[a-z]*", allraw, re.I)}))

    def word_forms(term):
        c = {}
        for m in re.finditer(rf"{re.escape(term)}[a-z]*", allraw, re.I):
            c[m.group(0).lower()] = c.get(m.group(0).lower(), 0) + 1
        return ", ".join(f"'{w}' {n}" for w, n in
                         sorted(c.items(), key=lambda kv: -kv[1]))

    plan = (ROOT / "SERIES-PLAN-1894.md").read_text(encoding="utf-8")
    mm_r, mm_rp = raw_hits(pages, "magnetic motor")
    mm_d, mm_dp = index_hits(idx_def, "magnetic motor")
    mm_k, mm_kp = index_hits(idx_keep, "magnetic motor")
    ep_n, ep_p = raw_hits(pages, "the earth's potential")
    m = {
        "mm_raw": mm_r, "mm_raw_pages": fmt_pages(mm_rp),
        "mm_def": mm_d, "mm_def_pages": fmt_pages(mm_dp),
        "mm_keep": mm_k, "mm_keep_pages": fmt_pages(mm_kp),
        "free_raw": raw_hits(pages, "free")[0],
        "free_word": standalone("free"), "free_forms": word_forms("free"),
        "unity_raw": raw_hits(pages, "unity")[0],
        "unity_word": standalone("unity"), "unity_hosts": host_words("unity"),
        "earth_phrase": ep_n, "earth_phrase_pages": fmt_pages(ep_p),
        "earth_label": raw_hits(pages, "earth-potential")[0],
        "plan_hyphen": len(re.findall("free-energy", plan, re.I)),
        "plan_space": len(re.findall("free energy", plan, re.I)),
    }
    for term in ("magnet motor", "magnetic engine", "over unity",
                 "free electricity"):
        m.update(fuzzy(term))
    return m


TOKEN = re.compile(r"@@([a-z0-9_]+)@@")


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

    The checks feature-006/a08-qpdone ran over the article 08 pin, applied here
    to the file this script has just assembled: the header's counts against the
    parsed file, every citation against the heading it sits under, no quote
    pinned twice, every row carrying its annotation, every 'Rejected #N' and
    every flag name resolving, and every fragment re-grepped through
    grep_quote.py's own index - the code path this script does NOT use -
    restricted to the page it is pinned to. Returns (lines, ok).
    """
    bad, lines = [], []
    text = "\n".join(prose)
    # Reference scanning reads the generator's own prose only: the raw OCR
    # windows and the quoted 1894 lines are display type and full of caps, and
    # a table row is not a sentence that can cite a flag.
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
    # A figure or link note opens with its own name in caps, and the prose
    # cites notes by that name; the file's headings are names too. Anything
    # that reads like a name-citation and matches none of them is a dangling
    # reference - which is what the first version of this check was hunting
    # for when it wrote 'the LIVE PAGE CLAIMS section below' about a section
    # that was neither named that nor below.
    known = [t.rstrip(" .,;:") for t in titles]
    for n in FIGURE_NOTES + LINK_NOTES:
        mt = re.match(r"([A-Z][A-Z0-9 ,.'\-()]+?[.?!])", n)
        known.append((mt.group(1) if mt else n[:60]).rstrip(" .,;:"))
    known += [ln.lstrip("#").strip().rstrip(":")
              for ln in text.splitlines() if ln.startswith("##")]
    runs = set(re.findall(r"[A-Z][A-Z0-9]*(?:[ ,.'-]+[A-Z0-9][A-Z0-9]*){2,}",
                          refprose))
    allow = ["THE TABLE", "NO MATCH", "NOT PRESENT", "PART III", "APPENDIX A",
             "APPENDIX D", "NIKOLA TESLA", "VAN NOSTRAND", "THE THREE WAYS",
             "WHAT THE THREE LIVE PAGES", "WHAT CHAPTER", "THE OTHER COUNTS",
             "THE SIZE OF THE THING", "THE QUOTE EVERYONE POSTS", "THE HONEST",
             "WHAT HE DID CLAIM", "THE PYROMAGNETIC TWIST", "THE WORD SEARCH",
             "NOT SETTLED", "NOT VERBATIM", "WRONG PAGE", "MOTORS AND PYRO",
             "THE INVENTIONS RESEARCHES", "D. VAN NOSTRAND COMPANY", "ACT OF",
             "THE CHAPTER HEADING", "THE INDEX", "THE TITLE PAGE", "TESLA",
             "THE VOLUME", "THE BOOK", "THE PRINT", "THE SAME", "THE ONLY",
             "THE FIRST", "THE OTHER", "THE OTHER HALF", "THE OTHER COUNTS",
             "THE INDEX ENTRY", "THE INDEX ENTRIES", "THE FLAG", "THE FIGURE",
             "THE TABLE BELOW", "THE WORD", "THE WORD SEARCH PAGE", "THE ONE",
             "THE RUN", "THE PAGES", "THE PAGE", "THE P. 424", "THE P. 429",
             "THE P. 430", "THE P. 46", "THE P. 236", "THE P. 8", "THE P. 138",
             "THE P. 167", "THE P. 166", "THE P. 390", "THE P. 394", "THE P. 6",
             "THE P. 496", "THE P. 494", "THE P. 452", "THE P. 455", "THE P. 463",
             "THE P. 474", "THE P. 467", "THE P. 468", "THE P. 448", "THE P. 450",
             "THE P. 451", "THE P. 462", "THE P. 464", "THE P. 466", "THE P. 469",
             "THE P. 470", "THE P. 471", "THE P. 472", "THE P. 495", "THE P. 497",
             "THE P. 498", "THE P. 499", "THE P. 500", "THE P. 501", "THE P. 502",
             "THE P. 503", "THE P. 504", "THE P. 505", "THE P. 506", "THE P. 507",
             "THE P. 508", "THE P. 509", "THE P. 510", "THE P. 511", "THE P. 512",
             "THE P. 513", "THE P. 514", "THE P. 515", "THE P. 516", "THE P. 517",
             "THE P. 518", "THE P. 519", "THE P. 520",
             # Not names of anything in this file: the volume's own display type
             # quoted in prose (figure numbers, an index entry's broken spelling),
             # a filename, a person, and the plan's sourcing order, which is a
             # rule of SERIES-PLAN-1894.md rather than a section of this pin.
             "FIG.", "PYRO-MAGNETIC", "SERIES-PLAN", "SOURCING ORDER",
             "T. C. MARTIN", "PLATE, AND THE QC ROW"]
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
    # The failures are printed in the file, not only to stderr: a pin whose
    # self-check failed has to say so where a reader would read the result.
    lines += ["FAIL — " + b for b in bad]
    return lines, not bad


def main():
    pages = gq.load_pages(TXT)
    # The same index check_quotes.py builds, so a quote that passes here is a
    # quote that passes there: exact, or verbatim once OCR spacing is ignored.
    index = tuple(gq.build_index(pages)) + tuple(CQ.build_nospace(pages))
    raw_by_page = {fp: raw for fp, pp, itext, raw, _ in pages}

    rows, problems = [], []
    for quote, page, section, why in QUOTES:
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

    if problems:
        for q, p, why in problems:
            print(f"FAIL p.{p} {q[:70]!r} -> {why}", file=sys.stderr)
        sys.exit(1)

    def how_note(checks):
        parts = []
        for i, (_f, how, _pps, _fp, _raw, straddle, others) in enumerate(checks, 1):
            tag = ("exact match, ratio 1.0" if how == "exact"
                   else "whitespace-only difference: the OCR spacing is not the "
                        "print's (words glued, or a stray space). Print the clean "
                        "form; check_quotes.py flags it the same way")
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
                         "page)")
            parts.append(f"{lead}{tag}{extra}")
        head = ("" if len(checks) == 1 else
                f"{len(checks)} fragments, each verified separately "
                "(check_quotes.py splits on '...'); ")
        return head + "; ".join(parts)

    table_rows, scoped_rows = measure_all()
    claims = measure_claims(pages)
    crops = figure_crops(CH36[0], CH36[1])
    claims["ch36_crop_count"] = len(crops)
    claims["ch36_crop_list"] = "; ".join(crops)
    stats = page_stats()
    live = live_page_data()
    # Terms whose count depends on which index is used. The file prints this
    # list rather than claiming the indices agree, which is what the first
    # version of this section did while its own table showed otherwise.
    disagree = [(term, r, k, g) for (term, _n, r, _rp, g, _gp, k, _kp)
                in table_rows if not (r == k == g)]
    vol_pages = gq.load_pages(TXT, clean=True)

    by_page = {}
    for r in rows:
        by_page.setdefault(r[1], []).append(r)

    out = [
        "# Article 10 quote pin: tesla-free-energy-what-he-said.html",
        "",
        "SERIES-PLAN-1894.md §8 step 2, feature-007/t0. Every quote below was "
        f"re-grepped on {PIN_DATE} from `books/extracted/tesla-1894-plain.txt` "
        "through the same matcher `books/tools/check_quotes.py` uses (exact, or "
        "verbatim once OCR spacing is ignored) and is pinned to the printed page "
        "it was found on (printed page = scan file page - 18, §0). A quote "
        "carrying ' ... ' is cut where the scan or the page break interrupts it; "
        "each side of the cut is verified separately against the one page the "
        "quote is pinned to, which is how check_quotes.py will judge the draft. "
        "`article.md` for this page is written from this file; a quote that is "
        "not here does not go in the draft.",
        "",
        f"Verified: {len(rows)} quotes "
        f"({sum(len(r[4]) for r in rows)} fragments) across {len(by_page)} "
        "printed pages, 0 failures. Rejected and not carried forward: "
        f"{len(REJECTED)}. Flags for the writer: {len(FLAGS)}. To re-check one "
        "quote: `python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>` "
        "- but read HOW TO READ A COUNT first, because that tool's `--count` "
        "falls back to fuzzy matching and reports hits for words that are not in "
        "the book. To regenerate this file: "
        "`python3 new_content/1894-series/10-tesla-free-energy-what-he-said/"
        "gen_quotes.py` (it exits non-zero and writes nothing if any quote "
        "fails).",
        "",
        "This is the trust piece of the series (§9 brief 10: 'the trust piece'), "
        "and its evidence is a count as much as a quote. So the counts in this "
        "file are measured by this script on the date above, three different "
        "ways, and the number a draft prints has to come with the index that "
        "produced it. The three indices are defined in THE THREE WAYS TO COUNT "
        "below; the disagreement between them is not noise, it is the p. 424 "
        "chapter heading, and THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT "
        "QUOTABLE is the flag that explains it.",
        "",
        "Source: Martin (ed.), *The Inventions, Researches and Writings of "
        "Nikola Tesla*, D. Van Nostrand Company, New York, title page 1894 "
        "(entered at the Library of Congress 1893), archive.org item "
        "`inventionsresear00martiala`. The passages this article quotes come from "
        "four different texts inside that one volume, in three different voices, "
        "and the brief's beats mix them. Read WHICH PAGES ARE TESLA WRITING and "
        "FOUR TEXTS, FOUR DATES before writing anything with 'Tesla wrote' in it.",
        "",
        "## The size of the thing searched (brief 10 item 1)",
        "",
        "Brief 10 says to state the method up front: 'we hold the 1894 first "
        "edition as 518 page scans and 177,000 words of text'. Both numbers are "
        "right, and the second one needs care about which text it counts. "
        "Measured on the date above:",
        "",
        *[f"- {k}: {v:,}" for k, v in stats.items()],
        "",
        "The 177,000 figure in the plan is the full text file. The index the "
        "search actually runs over is smaller, because running heads and bare "
        "folios are stripped out of it (§grep_quote.strip_furniture). A draft "
        "that says '177,000 words' is describing the book; a draft that says "
        "'the searchable text is N words' is describing the search. Say which.",
        "",
        "## THE THREE WAYS TO COUNT",
        "",
        "- **RAW** - case-insensitive substring count over "
        "`books/extracted/tesla-1894-plain.txt` page bodies as they sit on disk, "
        "nothing normalised. This is what `grep -c` would give a reader who "
        "reproduces the claim by hand, and it is the index that produces "
        "Appendix D's numbers.",
        "- **GATE** - the index `books/tools/check_quotes.py` builds, "
        "`load_pages(clean=True)`: short all-caps lines and bare folios are "
        "dropped as running heads, then the text is lower-cased, a hyphen at a "
        "line break is folded, and whitespace is collapsed. This is the index "
        "the numeric gate in feature-007/t3 will check the draft's quotations "
        "against - and it is also what `books/tools/check_quotes.py` and "
        "`books/tools/grep_quote.py` both build by default, because the CLI's "
        "default is `clean=True` as well. GATE and the CLI's default count are "
        "one number, not two.",
        "- **KEEP** - the same index with `--keep-furniture`, "
        "`load_pages(clean=False)`: running heads and page-opening display type "
        "kept. This is the only one of the three that contains the chapter "
        "XXXVI heading, and so the only one that returns 5 for 'magnetic "
        "generator'.",
        "",
        f"The three indices do not agree, and not on one term: measured on the "
        f"date above, {len(disagree)} of the {len(table_rows)} terms in the two "
        "tables below count differently depending on which is used - "
        + "; ".join(f"`{t}` raw {r} / GATE {g} / KEEP {k}"
                    for t, r, k, g in disagree) + ".",
        "",
        "The two mechanisms are readable straight off those numbers, and the "
        "draft has to know both. Where RAW is below the other two, a line "
        "break in the print is the cause: the phrase is on the page, but the "
        "OCR ends a line inside it, and a raw substring count cannot cross a "
        "newline - that is why 'wheelwork of nature' is 0 raw and 1 on both "
        "normalised indices, and why 'magnetic motor' is 3 raw and 4 on GATE "
        "(the normaliser folds the hyphen at the line break and joins "
        "'electro-' to 'magnetic motor' at printed p. 55, where the raw text "
        "never sets the phrase). Where GATE is below KEEP, furniture is the "
        "cause: the hit is a running head or a display line, and "
        "`strip_furniture` drops it. The largest one is 'magnetic generator', "
        "where the missing hit is the display heading of chapter XXXVI on "
        "printed p. 424 - see THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT "
        "QUOTABLE and THE CLI AND THE GATE SHARE AN INDEX BY DEFAULT.",
        "",
        "## THE TABLE (brief 10 item 2, Appendix D)",
        "",
        "Re-run at publish time by feature-007/t1's own instruction, and the "
        "draft must show the counts, not describe them. Counts are hits, and the "
        "page lists are printed pages with a hit count in parentheses where a "
        "page carries more than one.",
        "",
        "| search term | RAW | GATE (= grep_quote.py default) | KEEP "
        "(--keep-furniture) | printed pages (RAW) | what it is |",
        "|---|---|---|---|---|---|",
    ]
    for term, note, r, rp, g, gp, k, kp in table_rows[:len(TABLE_TERMS)]:
        out.append(f"| `{term}` | {r} | {g} | {k} | {fmt_pages(rp)} | {note} |")
    out += [
        "",
        "Appendix D prints the row 'magnetic generator | 5 - all of them "
        "**pyro**magnetic (pp. 6, 424, 429, 496)'. Those are the RAW and KEEP "
        "numbers, and 5 is the number feature-007/t1's criteria require the "
        "draft to print. GATE - which is also what `grep_quote.py` reports when "
        "run without a flag - gives 4 from the same three printed pages, "
        "because the fifth hit is a display heading. The draft prints 5 and "
        "says where the fifth hit is and which index produces 4; it does not "
        "print 4 to agree with article 08, and it does not quietly drop the "
        "heading.",
        "",
        "## The other counts the article needs",
        "",
        "Brief 10 item 6 says the phrase 'Tesla magnetic generator' is a "
        "21st-century product name, not a Tesla term. That sentence is a count, "
        "so it needs the counts for the phrases the site actually uses - and the "
        "ones a reader might type. Same three indices, same page lists.",
        "",
        "| search term | RAW | GATE (= grep_quote.py default) | KEEP "
        "(--keep-furniture) | printed pages (RAW) | why it is in the table |",
        "|---|---|---|---|---|---|",
    ]
    for term, note, r, rp, g, gp, k, kp in table_rows[len(TABLE_TERMS):]:
        out.append(f"| `{term}` | {r} | {g} | {k} | {fmt_pages(rp)} | {note} |")
    out += [
        "",
        fill("Three of those rows are the ones to write about, not just to "
             "print. `free` is @@free_raw@@ hits, of which @@free_word@@ are "
             "the bare word and none is followed by 'energy'; the forms are "
             "@@free_forms@@. `unity` is @@unity_raw@@ hits and "
             "@@unity_word@@ of them is the word - all @@unity_raw@@ are "
             "inside @@unity_hosts@@. `magnet motor` is 0 on all three "
             "indices, and `grep_quote.py --count` reports "
             "@@magnet_motor_fuzzy_n@@ for it anyway. A reader who searches a "
             "word, finds it, and believes the phrase is there is how the myth "
             "survives a spot check; this is the article in the series that "
             "says so, and the table is the evidence.", claims),
        "",
        "## What chapter XXXVI does and does not report (brief 10 item 5)",
        "",
        "The pyromagnetic beat asks whether the book's only magnetic generator "
        "was ever tested. Scoped to printed pp. 424-431, the chapter's own "
        "extent, RAW counts over the unstripped page bodies:",
        "",
        "| search term | scope | hits in the chapter | printed pages |",
        "|---|---|---|---|",
    ]
    for term, scope, r, rp in scoped_rows:
        out.append(f"| `{term}` | {scope} | {r} | {fmt_pages(rp)} |")
    hit_lines = []
    for term, _scope, r, _rp in scoped_rows:
        if not r:
            continue
        for _f, pp, _i, raw, _b in vol_pages:
            if not (CH36[0] <= pp <= CH36[1]):
                continue
            for m in re.finditer(re.escape(term), raw, re.I):
                ctx = " ".join(raw[max(0, m.start() - 90):m.end() + 70].split())
                hit_lines.append(f"- `{term}` printed p. {pp}: ...{ctx}...")
    out += [
        "",
        "Three of those counts are not zero, and a count alone would mislead "
        "the draft, so every hit is here with the sentence it sits in:", "",
        *hit_lines,
        "",
        fill("So the answer to item 5 is not 'the chapter never mentions "
             "experiments or results'. @@exp_n@@ 'experiment' and @@res_n@@ "
             "'result' are in it, and the hit list above says what they are: "
             "'experiment' twice inside the compiler's single footnote about the "
             "horseshoe-magnet demonstration on printed p. 424, and once in the "
             "chapter's own illustration on p. 429 ('this principle of "
             "operation may be illustrated by a simple experiment'); 'result' in "
             "the compiler's verdict sentence, in 'reciprocating action "
             "resulting from', and three times in ordinary technical prose "
             "(printed pp. 425, 429, 430). "
             "What the chapter does not contain is a trial of the machine: "
             "'test' @@test_n@@ on every index, 'per cent' @@pc_n@@, "
             "'efficiency' @@eff_n@@, and the one 'output' is 'meaning larger "
             "output', a design property with no number on it. The book's own "
             "verdict is quotable and is on printed p. 424 - 'investigated "
             "frequently, though not with any material or practical result' - "
             "and it is a stronger sentence than any absence argument, because "
             "it is the compiler writing it, in 1894, about this class of "
             "machine. Article 08's rendered page gives the same finding in "
             "prose ('a chapter that reports no output, no efficiency figure "
             "and no trial', website/tesla-weird-inventions-1894.html) and its "
             "pin records it as 'no output, no efficiency, no run, no trial, no "
             "commercial result anywhere in pp. 424-431'; article 10 may print "
             "the scoped counts and say the chapter reports a design and an "
             "illustration and no measurement of the machine. It may not write "
             "that the machine failed, or was never built, or was a failure - "
             "section 4.1. The absence of a measurement is the claim; anything "
             "stronger is the writer's.",
             {"exp_n": dict((t, r) for t, _s, r, _p in scoped_rows)["experiment"],
              "res_n": dict((t, r) for t, _s, r, _p in scoped_rows)["result"],
              "test_n": dict((t, r) for t, _s, r, _p in scoped_rows)["test"],
              "pc_n": dict((t, r) for t, _s, r, _p in scoped_rows)["per cent"],
              "eff_n": dict((t, r) for t, _s, r, _p in
                            scoped_rows)["efficiency"]}),
        "",
        "## What the three live pages actually claim (brief 10 item 7)",
        "",
        "Read out of `website/` on the date above, tags stripped, so the "
        "comparison in feature-007/t0's third criterion is a thing this file "
        "shows. The 1894 column is the measured RAW count over the whole volume, "
        "which is what makes the point: the words the pages use are not in the "
        "book.",
        "",
    ]
    for name, nwords, counts, page_claims in live:
        if nwords is None:
            out += [f"### `{name}`", "", "NOT PRESENT in website/ on "
                    f"{PIN_DATE} - re-run this script before relying on the "
                    "comparison.", ""]
            continue
        out += [f"### `{name}` ({nwords:,} words of visible text)", "",
                "| term | on the live page | in the 1894 text (RAW) |",
                "|---|---|---|"]
        for term, n in counts:
            vol, _ = raw_hits(vol_pages, term)
            out.append(f"| `{term}` | {n} | {vol} |")
        out += ["", "Its own claim wording, quoted from the page as it stands:"]
        for label, sent in page_claims:
            if sent is None:
                out += [f"- **{label}**: not found on the page as it stands - "
                        "the page may have changed; re-check before quoting it"]
            else:
                out += [f"- **{label}**: \"{sent}\""]
        out += [""]
    out += [
        "What article 10 may and may not carry across that gap. It may say the "
        "1894 book never uses 'free energy', 'perpetual motion' or 'over unity'; "
        "never mentions a bifilar coil, patent 512,340 or a 'coil for "
        "electromagnets'; and attaches 'magnetic generator' only to a heat "
        "engine. It may report what each live page claims, in the pages' own "
        "words, with the link. It may not let the book's authority leak onto the "
        "pages' claims: a sentence that puts a p. 429 quotation next to a 5x "
        "energy figure implies the book supports the figure, and it does not. "
        "The one live-page claim the 1894 text does meet is the existence of a "
        "pyromagnetic generator, and the book's own account of it is a firebox, "
        "a boiler and no test. §4.1 again: no sentence about what the product "
        "can do that is not already on a live page - and equally, no live "
        "page's claim dressed up as a historical one.",
        "",
        "## Quotes, pinned by printed page",
        "",
    ]
    for page in sorted(by_page):
        rows_p = by_page[page]
        where = (f"scan file {rows_p[0][4][0][3]}"
                 if page >= 0 else
                 f"scan file {rows_p[0][4][0][3]}, unnumbered front-matter leaf")
        out += [f"## Printed p. {page} ({where})", ""]
        for quote, _p, section, why, checks in rows_p:
            straddling = [c for c in checks if len(c[5]) > 1]
            out += [f"### {section}", "", f'> "{quote}"', "",
                    f"- cited as: `(1894, p. {page})`"]
            if straddling:
                out += [f"- straddle: this ONE fragment sits on printed pp. "
                        f"{straddling[0][5][0]}-{straddling[0][5][-1]} as a "
                        "single run; check_quotes.py accepts a citation to either "
                        "page, so cite one page only - '(1894, pp. ...)' never "
                        "matches its citation regex"]
            out += [f"- why: {why}",
                    f"- check_quotes.py: {how_note(checks)}"]
            for i, (frag, _how, _pps, _fp, raw, _st, _ot) in enumerate(checks, 1):
                tag = "" if len(checks) == 1 else f" (frag {i}: {frag[:40]})"
                out += [f"- raw OCR{tag}: `{raw}`"]
            out += [""]
    out += ["## Rejected: considered and not carried forward", "",
            "(Numbered, because 'Rejected #N' is cited from the rows above and "
            "the numbers are the order of the REJECTED list in `gen_quotes.py`; "
            "nothing renumbers them.)", ""]
    for i, (quote, page, why) in enumerate(REJECTED, 1):
        where = f"p. {page}" if page else "not in this volume as a phrase"
        out += [f"{i}. ~~\"{quote}\"~~ ({where}): {fill(why, claims)}"]
    out += ["", "## Flags for the writer (§3 quote style, §4.1 guardrail, "
                "feature-007/t1)", ""]
    out += [f"- **{t}** — {fill(b, claims)}" for t, b in FLAGS]
    out += ["", "## Notes for the figure task (feature-007/t2)", ""]
    out += [f"- {fill(f, claims)}" for f in FIGURE_NOTES]
    out += ["", "## Links (§5.2 row 10, for feature-007/t1 and t3)", ""]
    out += [f"- {fill(f, claims)}" for f in LINK_NOTES]
    out += ["",
            "Do not run `check_quotes.py` on this file as a gate. It is built "
            "for a draft (`article.md`), and here its scanner reads the "
            "apostrophes in the '- why:' annotations and the struck-through "
            "Rejected items as quotation marks, so any count it prints for this "
            "file is a count of this file's own prose. The gate for a pin file "
            "is `gen_quotes.py` itself: it imports the same matcher "
            "(`check_quotes.fragments` + `check_quotes.locate` over the index "
            "`check_quotes` builds) and refuses to write anything if a quote "
            "does not verify on its stated page. `check_quotes.py` runs on "
            "`article.md` in feature-007/t3.", ""]

    # The checks feature-006/a08-qpdone ran by hand over the article 08 pin,
    # run here over the file this script has just assembled, before it is
    # written. A pin that cannot re-read itself is how article 08's pass ended
    # up re-measuring numbers after they had been written down.
    check_lines, ok = structural_check(rows, out)
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
          f"{len(table_rows)} counted terms, {len(scoped_rows)} scoped counts)")
    if not ok:
        for ln in check_lines:
            if ln.startswith("FAIL"):
                print(f"SELF-CHECK {ln}", file=sys.stderr)
        return 1
    print("self-check: no failures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
