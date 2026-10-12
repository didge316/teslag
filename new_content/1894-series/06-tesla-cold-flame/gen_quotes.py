#!/usr/bin/env python3
"""Regenerate quotes.md for this article (feature-005/t9).

Run: python3 new_content/1894-series/06-tesla-cold-flame/gen_quotes.py

Every entry is re-grepped at generation time through the same matcher
books/tools/check_quotes.py uses; if a quote does not verify on its stated printed
page the script fails and writes nothing. That is the whole point of the file
(SERIES-PLAN-1894.md §8 step 2, §0 non-negotiable 2): the draft is written from
this, not from memory.

A pinned quote may contain " ..." where the printed text is cut for an OCR
artefact. Each fragment between the cuts is verified separately, which is exactly
how books/tools/check_quotes.py will judge the draft in feature-005/t5 - so this
script does not reimplement that check, it imports it (check_quotes.fragments +
check_quotes.locate over the index check_quotes builds). If a quote passes here it
passes there.

Three sentences here run over a page break (printed pp. 166->167, 213->214,
258->259). Where a fragment straddles a break as ONE fragment, check_quotes.py
accepts a citation to either page it sits on; where the cut is made AT the break,
each half is pinned to its own page. A hyphenated range "(1894, pp. 258-259)" is
never used: check_quotes.py's citation regex cannot read one.
"""
import re
import sys
from pathlib import Path

TOOLS = Path("/home/matt/projects/other/tesla-generator/books/tools")
sys.path.insert(0, str(TOOLS))
import check_quotes as CQ  # noqa: E402
import grep_quote as gq  # noqa: E402

TXT = TOOLS.parent / "extracted" / "tesla-1894-plain.txt"
OUT = Path("/home/matt/projects/other/tesla-generator/new_content/1894-series/"
           "06-tesla-cold-flame/quotes.md")

PIN_DATE = "2026-10-11"

# (quote as it will be printed, printed page, brief 06 section, why it is in the piece)
QUOTES = [
    # --- 0. Provenance: the chapter footnotes, added at draft time (feature-005/t5).
    # The draft names which lecture each passage comes from, so the footnotes that
    # date the chapters are quoted rather than paraphrased. Both verify exactly.
    ("Lecture delivered before the Institution of Electrical Engineers, London, "
     "February, 1892.",
     198, "0. Provenance (ch. XXVII footnote)",
     "dates the London chapter, which carries the stage moment at printed p. 258. "
     "Added at draft time (feature-005/t5) so the article can name its text instead "
     "of asserting a date"),
    ("A lecture delivered before the American Institute of Electrical Engineers, "
     "at Columbia College, N. Y., May 20, 1891.",
     145, "0. Provenance (ch. XXVI footnote)",
     "dates the New York chapter, which carries the brush passages at printed "
     "pp. 166-171. Added at draft time (feature-005/t5). The two footnotes are "
     "quoted because the article's first job is to keep four texts apart"),
    ("the true electric flame",
     121, "5. What the internet gets wrong",
     "the short form the draft prints, inside the longer editorial sentence pinned "
     "above. Added at draft time (feature-005/t5) because the draft quotes the "
     "phrase, not the whole editorial run"),
    # --- 1. The stage moment (ch. XXVII, IEE London, Feb 1892; printed p. 258)
    ("In one of the experiments this evening a brush was produced at the end of "
     "a wire",
     258, "1. The stage moment",
     "he is describing a live demonstration, in the present tense, to an audience. "
     "This is what 'the stage moment' actually is: the sentence that puts the brush "
     "on a stage in front of the Institution of Electrical Engineers, London"),
    ("The brush was a flame, a source of heat and light. It did not emit much "
     "perceptible heat, nor did it glow with an intense light ; but is it the less "
     "a flame because it does not scorch my hand",
     258, "1. The stage moment",
     "the brief's opening quote, pinned in the form that verifies: the print's spaced "
     "semicolon kept, and stopped before the question mark, which this scan reads as "
     "'{'. See the flags and rejected #1"),
    ("Is it the less a flame because it does not hurt my eyes by its brilliancy",
     258, "1. The stage moment",
     "the second half of the same rhetorical move, on light instead of heat. Same "
     "'{' for '?' problem; put the question mark outside the quote marks"),
    ("The problem is precisely to produce in the bulb such a flame, much smaller "
     "in size, but incomparably more powerful",
     258, "1. The stage moment",
     "what he was trying to build, in his own one line: a lamp. Not a free-energy "
     "project - the anchor for section 5"),
    # --- 2. What a brush actually is (ch. XXVI, Columbia College, May 1891; pp. 166-167)
    ("one may produce two powerful brushes several inches long, nearly white at "
     "their roots, which in the dark bear a striking resemblance to two flames of "
     "a gas escaping under pressure",
     166, "2. What a brush actually is",
     "the observation the article's central image rests on, and the sentence that "
     "points at Fig. 110 on the same page - see the figure notes"),
    ("But they do not only resemble, they are veritable flames, for they are hot",
     166, "2. What a brush actually is",
     "the sentence this article's title has to answer: he insists the brush is hot. "
     "'Cold' is only true beside a gas flame"),
    ("The heat developed is, of course, due to the impact of the air molecules "
     "against the terminals and against each other",
     166, "2. What a brush actually is",
     "his mechanism in his own words: molecular bombardment. Section 2 explains this "
     "in plain English; it does not replace it with modern wording"),
    ("In the positive brush of a static machine the exchange of the molecules is "
     "very rapid, the stream is constantly of one direction, and there are fewer "
     "collisions ; hence the heating effect must be very small",
     167, "2. What a brush actually is",
     "why a brush can feel cool: rapid exchange, few collisions. The ' ;' is the "
     "print's spacing; see flags"),
    ("Anything that impairs the facility of exchange tends to increase the local "
     "heat produced",
     167, "2. What a brush actually is",
     "the rule, stated as a rule. It is what makes the tube and bulb demonstrations "
     "in the next two quotes work"),
    ("If a glass tube be held over the brush so as to allow the draught to carry "
     "the brush upwards, scorching hot air escapes at the top of the tube",
     167, "2. What a brush actually is",
     "the demonstration he does with a tube over the flame, and the air coming out "
     "scorching. 'Scorching' is his word, and it contradicts 'the flame that doesn't "
     "burn'"),
    ("Anything held within the brush is, of course, rapidly heated, and the "
     "possibility of using such heating effects for some purpose or other suggests "
     "itself",
     167, "2. What a brush actually is",
     "the practical consequence he draws, hedged with 'suggests itself'"),
    # Added at draft time (feature-005/t5, 2026-10-11). Printed p. 168 is the same
    # Columbia College lecture, one page on. Every fragment below was re-grepped with
    # books/tools/grep_quote.py --page 160-175 and verified exactly before being added
    # here; the draft does not use a quote that is not in this file.
    ("the air molecules are violently attracted and repelled, and by their impact "
     "produce such a powerful heating effect",
     168, "2. What a brush actually is",
     "the same mechanism stated at full scale, in the storm-fire paragraph. Cut "
     "before 'that a lire is started': the scan reads 'fire' as 'lire', ratio 0.989, "
     "so that clause is unusable - see rejected #4"),
    # --- 3. Tesla's bigger idea (ch. XXVI, printed pp. 167-168)
    ("When contemplating this singular phenomenon of the hot brush, we cannot help "
     "being convinced that a similar process must take place in the ordinary flame",
     167, "3. Tesla's bigger idea",
     "the inference that gives this article its name: he argues the hot brush IS the "
     "ordinary flame's process. 'the hot brush' is the book's own phrase - 2 hits in "
     "the volume, printed pp. 127 and 167"),
    ("we have a possible way of producing - by other than chemical means - a "
     "veritable flame, which would give light and heat without any material being "
     "consumed, without any chemical process taking place, and to accomplish this, "
     "we only need to perfect methods of producing enormous frequencies and "
     "potentials",
     167, "3. Tesla's bigger idea",
     "the brief's section 3 quote, in full and in a form that verifies. The print "
     "sets 'by other than chemical means' off with em dashes; grep_quote.py folds a "
     "typed ' - ' to the same normalised text, so this ASCII form matches exactly. "
     "The cut form with ' ... ' also verifies, fragment by fragment - see flags"),
    ("I have no doubt that if the potential could be made to alternate with "
     "sufficient rapidity and power, the brush formed at the end of a wire would "
     "lose its electrical characteristics and would become flamelike",
     167, "3. Tesla's bigger idea",
     "the claim with its condition attached: 'if the potential could be made to "
     "alternate with sufficient rapidity and power'. He does not say it works; he "
     "says what would have to be true for it to work"),
    ("The flame must be due to electrostatic molecular action",
     167, "3. Tesla's bigger idea",
     "his one-sentence theory of the flame. Short, and it is his, so it can carry "
     "quotation marks; the modern ionisation account is ours (see flags)"),
    ("It is well known that objects are often set on fire without the lightning "
     "striking them",
     167, "3. Tesla's bigger idea",
     "the consequence he draws in the next sentence after the electrostatic-molecular "
     "theory: storm accidents where nothing was struck. Added at draft time "
     "(feature-005/t5)"),
    ("perhaps many million times a second",
     168, "3. Tesla's bigger idea",
     "the frequency the explanation needs, in his own words, one page on in the same "
     "lecture. Against the 15,000 and 30,000 alternations per second of ch. XXIX this "
     "is the gap, and it is why section 4 is the article. Added at draft time"),
    ("It is conceivable that a ship at sea may, in this manner, catch fire at many "
     "points at once",
     168, "3. Tesla's bigger idea",
     "the consequence he leaves standing, unhedged except by 'It is conceivable', "
     "which is the same construction article 05's pin flags at p. 395. Added at "
     "draft time"),
    ("the local heating effect may be so exalted as to bring a body to "
     "incandescence",
     168, "3. Tesla's bigger idea",
     "the practical route from the brush to a lamp: stop the air exchanging and a "
     "body in an unexhausted globe glows. The sentence opens 'By preventing "
     "completely the exchange of the air molecules' and the scan prints 'molecules^' "
     "there, so the pin starts after that. Fig. 111 on the same page is the spinning "
     "filament: 'the appearance of a luminous funnel' verifies exactly (1 occurrence, "
     "printed p. 168) and is caption material for feature-005/t6. Added at draft "
     "time"),
    # --- 4. Why he never got it (printed pp. 166, 168, 169, 213, 259, 376, 381)
    ("Certainly they are not as hot as a gas burner, but they would be so if the "
     "frequency",
     166, "4. Why he never got it",
     "the honest scale of what he had: cooler than a gas burner, and it would not be "
     "only if the frequency were higher. Cut before the OCR's 'frequency cmd the "
     "potential'; see rejected #3"),
    ("The higher the frequency, the less the molecule is able to get away, and "
     "this the more so, as for a given effect the potential required is smaller",
     166, "4. Why he never got it",
     "the scaling argument that makes him think a high enough frequency is reachable. "
     "The sentence runs on across the page break onto printed p. 167; the next quote "
     "is its far end"),
    ("which practically the same molecules would strike the terminal",
     167, "4. Why he never got it",
     "the end of that sentence, on printed p. 167: a frequency at which the same "
     "molecules would be struck again and again. Pinned to its own page because the "
     "cut is at the break"),
    # Added at draft time (feature-005/t5, 2026-10-11). Both were re-grepped with
    # books/tools/grep_quote.py --page 160-175 and verified exactly before being added.
    ("Produced with, say, twenty thousand alternations per second, the heat is "
     "easily perceptible even if the potential is not excessively high",
     166, "4. Why he never got it",
     "the frequency the hot brush was actually made with, in the same paragraph as "
     "'veritable flames, for they are hot'. Set against 'perhaps many million times "
     "a second' (printed p. 168) this is the size of the gap, and it is the number "
     "section 4 is built on"),
    ("The possibility of bringing a body to incandescence in an exhausted globe, or "
     "even when not at all enclosed, would seem to afford a possible way of "
     "obtaining light ... might be rendered available for useful purposes",
     169, "4. Why he never got it",
     "the lamp sentence, and it marks itself as a possibility: 'would seem to afford "
     "a possible way'. Cut at the OCR's 'light eifects, which, in perfecting methods "
     "of producing rapidly alternating potentials,'; each side of the cut verifies "
     "separately on printed p. 169"),
    ("In employing a commercial coil, the production of very powerful brush effects "
     "is attended with considerable difficulties",
     169, "4. Why he never got it",
     "the practical blocker, in his words: the off-the-shelf apparatus of 1891 could "
     "not do this"),
    ("when these high frequencies and enormous potentials are used, the best "
     "insulation is apt to give way",
     169, "4. Why he never got it",
     "what actually failed: insulation. The printed page interleaves the caption "
     "'FIG. 112*.' between the two halves of this sentence; grep_quote.py's "
     "strip_furniture() drops the caption line, so the run verifies"),
    ("with potentials of no more than one or two hundred thousand volts, the "
     "heating effects are considerable",
     168, "4. Why he never got it",
     "the scale he actually had, stated by him as a premise for an inference, not a "
     "measurement. Also the in-book basis for the safety note (see flags). Added at "
     "draft time"),
    ("we may imagine how much more powerful they must be with frequencies and "
     "potentials many times greater",
     168, "4. Why he never got it",
     "the sentence that follows the last one, and it marks itself as reasoning: 'we "
     "may imagine', and then 'the above explanation seems, to say the least, very "
     "probable'. Added at draft time"),
    ("I am not aware that, up to the present ... the heating effects of a brush "
     "produced by a rapidly alternating potential ... have been experimentally "
     "demonstrated, at least not to such a remarkable degree",
     168, "4. Why he never got it",
     "his own claim-priority sentence about this exact effect, cut at the printed "
     "page's interposed caption 'FIG. ill.'; each of the three fragments verifies "
     "separately on printed p. 168, which is how check_quotes.py reads a cut quote. "
     "Added at draft time"),
    ("the heat as well as light effects produced should be proportionate, under "
     "otherwise equal conditions of test, to the product of frequency and square of "
     "potential",
     213, "4. Why he never got it",
     "the law he thought governed it: heat and light go as frequency times potential "
     "squared. This is why 'enormous frequencies and potentials' is the whole "
     "difficulty, quantitatively"),
    ("the experimental verification of the law, whatever it may be, would be "
     "exceedingly difficult",
     213, "4. Why he never got it",
     "his own hedge on that law, in the next sentence; 'whatever it may be' is doing "
     "a lot of work, keep it. The fragment straddles printed pp. 213-214; cite one "
     "page, not a range"),
    ("Were there means at hand for producing electric impulses of a sufficiently "
     "high frequency, and for transmitting them, the bulb could be done away with",
     258, "4. Why he never got it",
     "the counterfactual that answers brief 06 section 4 directly: the glass envelope "
     "was a workaround for apparatus he did not have. This fragment straddles printed "
     "pp. 258-259 as one fragment; cite p. 258 (or p. 259), never 'pp. 258-259'"),
    ("But as such means are not at disposal, it becomes necessary to place the "
     "terminal in the bulb and rarefy the air in the same",
     259, "4. Why he never got it",
     "the admission that follows it, on printed p. 259: 'such means are not at "
     "disposal'. This is the sentence section 4 is built on"),
    ("Up to about 15,000 alternations per second in an experimental machine, the "
     "former plan may be followed, but a more efficient machine is obtained on the "
     "second plan",
     376, "4. Why he never got it",
     "the ceiling of the machinery, in numbers. Printed p. 376 is chapter XXIX, the "
     "editor's chapter on the high-frequency alternators (article 11's chapter): "
     "third person, the book describing his machine. Attribute it to the book, not to "
     "Tesla's own paper - see flags"),
    ("the field had 480 polar projections on each side, and from this machine it "
     "was possible to obtain 30,000 alternations per second",
     381, "4. Why he never got it",
     "the best he had: 30,000 alternations a second, against the 'many million times "
     "a second' (p. 168) or 'enormous frequencies' (p. 167) the flame needs. Same "
     "editorial chapter; Appendix A registers this fragment at p. 381"),
    # --- 5. What the internet gets wrong (ch. XXVII p. 291; ch. XXVIII p. 322)
    ("It would, of course, be out of question to transmit such impulses through a "
     "wire immersed in a gaseous medium, even if the wire were provided with a thick "
     "and excellent insulation, for most of the energy would be lost in molecular "
     "bombardment and consequent heating",
     291, "5. What the internet gets wrong",
     "the energy bookkeeping in his words: a brush on a wire in air throws energy "
     "away. A 'cold fire' video is not getting something for nothing; it is a loss "
     "you can see. The form a draft would reach for ('it is out of the question') is "
     "not the print's - see rejected #8"),
    ("they always exist, consuming energy and modifying the action of the apparatus",
     322, "5. What the internet gets wrong",
     "the same point from the Philadelphia/St. Louis lecture: the brush discharge is "
     "a loss, always present, always consuming energy. Nothing in this volume supports "
     "a free-energy reading"),
    # --- 6. Where you see it now (ch. XXVI p. 171; ch. XXVII pp. 226-228)
    ("For the production of ozone, alternating currents of very high frequency are "
     "eminently suited",
     171, "6. Where you see it now",
     "the direct ancestor of the ozone generator, stated by him. 'ozone' occurs in the "
     "volume on printed pp. 127, 158, 171, 322, and in the index at pp. 495-496"),
    ("the ozonizing action of a discharge is dependent on the frequency as well as "
     "on the potential",
     171, "6. Where you see it now",
     "why frequency matters for the descendant devices, in his own account of his "
     "experiments"),
    ("it is a brush, formed at, or near, a single terminal in high vacuum",
     226, "6. Where you see it now",
     "what a plasma globe actually is, in his words, from the passage where he changes "
     "subject to the vacuum brushes ('I think it best at this juncture to bring before "
     "you a phenomenon...')"),
    # Added at the figure task (feature-005/t6). This is the sentence that describes the
    # plate printed on the same page as the figure, which is what a caption must follow.
    ("In Fig. 141 the bulb comprises an incandescent lamp globe ... in the neck of "
     "which is sealed a barometer tube ... the end of which is blown out to form a "
     "small sphere",
     226, "6. Where you see it now",
     "the book's own description of the plate used as figure 3, set on the same printed "
     "page beneath it. Every part named here - the globe, the barometer tube, the sphere "
     "- is drawn in the crop, which is how the crop was identified. The cuts are where "
     "the OCR drops the italic part letters (it prints 'globe Z' for globe L), so the "
     "quote is pinned in the fragments that verify; the letters themselves are named in "
     "the caption from the 500 ppi print, not from the text layer. Added at "
     "feature-005/t6 because the draft's first caption cited the p. 227 sentence about "
     "Figs. 143-145, which describes a different group of plates"),
    ("it is usually sufficient to grasp the globe L with the hand",
     228, "6. Where you see it now",
     "the plasma-globe demonstration, exactly as it is done today: hold the globe in "
     "your hand to excite it. Printed p. 228, chapter XXVII"),
    ("the approach of the observer at a few paces from the bulb will cause the "
     "brush to fly to the opposite side, and if he walks around the bulb it will "
     "always keep on the opposite side",
     228, "6. Where you see it now",
     "the behaviour every plasma globe shows, measured in 1892: the discharge follows "
     "the observer's body. This is the sentence that makes the modern device legible"),
    ("Figs. 143, 144 and 145 indicate different forms, or stages, of the brush",
     227, "6. Where you see it now",
     "the book's own description of the plates on printed pp. 227-228. Caption "
     "material for the figure task (feature-005/t6): the p. 228 plates are already "
     "article 02's, so read this sentence before choosing any crop"),

    # Added at draft time (feature-005/t5, 2026-10-11). Four more from the same
    # four texts, all re-grepped before use. The p. 171 pair is the same sentence
    # that names the biggest brush of the Columbia College lecture and then states
    # its chemical effect; the print sets the name in double quotes with a leading
    # space ('called " St. Elmo\'s hot fire,"'), which check_quotes.py's scanner
    # would split, so the draft quotes the run up to 'called' and gives the name
    # in our own sentence, unquoted. The p. 121 quote is the EDITOR's text about
    # 'Mr. Tesla', not a Tesla paper: it is the volume's own name for the effect.
    ("an excessively powerful brush, several inches long, which may be "
     "appropriately called",
     171, "2. What a brush actually is",
     "the name the 1894 text gives its own biggest brush, in the Columbia College "
     "lecture: St. Elmo's hot fire. This is the book's vocabulary, and it is not "
     "'cold'. The sentence continues into the ozonizer sentence below"),
    ("It is a most powerful ozonizer, so powerful indeed, that only a few minutes "
     "are sufficient to fill the whole room with the smell of ozone",
     171, "6. Where you see it now",
     "the ancestor of the ozone generator, stated by him as an observation about his "
     "own apparatus, and the in-book half of the modern health point"),
    ("This is done merely to enable the apparatus to perform the work which it is "
     "not capable of performing at ordinary air pressure",
     259, "4. Why he never got it",
     "the plain statement that the evacuated bulb is a workaround for machinery he "
     "did not have. It follows 'But as such means are not at disposal' on the same "
     "page and closes section 4"),
    ("if a coil, such as this one, is worked for a very long time it will make the "
     "atmosphere of a small room unbearable, for the eyes and throat are attacked",
     322, "6. Where you see it now",
     "his own account of what the chemistry does to a room, from the Philadelphia "
     "and St. Louis lecture, in the same passage as the 'they always exist, "
     "consuming energy' quote. The in-book basis for the safety paragraph; pair it "
     "with the EPA source, never with a health claim of ours"),
    ("starting from the thread-like discharge and passing through various stages to "
     "the true electric flame",
     121, "5. What the internet gets wrong",
     "the volume's own editorial introduction, third person about 'Mr. Tesla', "
     "classifying the discharge series as leading to 'the true electric flame'. "
     "Attribute to the editor, never to Tesla; it is the closest the 1894 book "
     "comes to naming this a flame, and it is not 'cold' either"),
]

# Considered and NOT carried forward, with the reason. Each reason states what the
# scan really says, so the writer can see why the quote is unusable.
REJECTED = [
    ("The brush was a flame, a source of heat and light. It did not emit much "
     "perceptible heat, nor did it glow with an intense light; but is it the less a "
     "flame because it does not scorch my hand?", 258,
     "the §9 brief 06 form of this line, and it FAILS: the printed page puts a space "
     "before the semicolon ('intense light ;'), and its question mark came out of this "
     "OCR as '{' ('scorch my hand { Is it the less'). The clean form with 'light;' "
     "still passes through check_quotes.py's space-ignoring index, but the trailing "
     "'?' never matches. Pin the run without the question mark and put the '?' outside "
     "the closing quote mark in the draft"),
    ("Is it the less a flame because it does not hurt my eyes by its brilliancy?",
     258,
     "same question-mark artefact: this scan gives 'its brilliancy ?' with a space "
     "before the mark, and the first one as '{'. Pin the words; keep the question mark "
     "outside the quotation marks"),
    ("but they would be so if the frequency and the potential would be sufficiently "
     "high", 166,
     "the OCR reads 'if the frequency cmd the potential would be sufficiently high' "
     "(and -> cmd), so no clean form of this clause matches at all. Pin 'Certainly "
     "they are not as hot as a gas burner, but they would be so if the frequency' and "
     "finish the thought in our own words"),
    ("The air molecules are violently attracted and repelled, and by their impact "
     "produce such a powerful heating effect that a fire is started", 168,
     "the OCR reads 'a lire is started' (fire -> lire), ratio 0.989, a FAIL. Pin up to "
     "'such a powerful heating effect' if the lightning-fire passage is used at all; it "
     "is section 4/5 material, not section 2"),
    ("The possibility of bringing a body to incandescence in an exhausted globe, or "
     "even when not at all enclosed, would seem to afford a possible way of obtaining "
     "light effects", 169,
     "the OCR reads 'light eifects' (effects -> eifects), ratio 0.991, a FAIL. The "
     "insulation sentence on the same page is the one this article needs"),
    ("In bulbs provided with a conducting terminal, though it be of aluminum, the "
     "brush has but an ephemeral existence", 226,
     "the OCR prints 'the brush -has' with a stray hyphen, ratio 0.991, a FAIL, and "
     "the hyphen survives both normalisers. Do not quote this sentence; the 'single "
     "terminal in high vacuum' sentence pinned above carries the same section"),
    ("An intense phosphorescence then spreads at first over the globe, but soon "
     "gives place to a white, misty light", 228,
     "the OCR reads 'at tirst' (first -> tirst), ratio 0.986, a FAIL. The two p. 228 "
     "quotes pinned above ('grasp the globe L with the hand', 'the approach of the "
     "observer...') verify exactly and do the same job"),
    ("it is out of the question to transmit such impulses through a wire immersed in "
     "a gaseous medium", 291,
     "no match at all: the print has no 'the' - it reads 'It would, of course, be out "
     "of question to transmit such impulses...' (ratio 0.983 for the form with 'the'). "
     "§9 brief 06 does not quote this line, but a draft written from memory will get it "
     "wrong; the pinned form is in section 5 above"),
    ("cold flame / cold fire / cold, flame / not hot", 0,
     "0 exact hits for each in the whole volume. The book's names for this phenomenon "
     "are 'the brush', 'the hot brush' (printed pp. 127 and 167 only), 'the streams' "
     "and 'a veritable flame'. The §9 title's 'Cold Flame' and 'Cold Fire' are ours "
     "and must stay outside quotation marks, and the article must say plainly that the "
     "1894 text never uses the phrase"),
    ("corona / corona discharge / plasma / ioniz- / electron / ultraviolet", 0,
     "0 exact hits for each in the whole volume ('electron' returns only fuzzy hits for "
     "'electrode'). The modern vocabulary of gas discharge is not in this book: the "
     "plain-English ionisation/corona explanation of brief 06 section 2 is OURS, so it "
     "gets no quotation marks and no page cite, and any modern physics claim needs a "
     "modern source (§4.1)"),
    ("resembling in every particular a flame and giving light and heat, yet without a "
     "chemical process taking place", 127,
     "printed p. 127 is chapter XXV, the editor's third-person introduction, not "
     "Tesla's lecture; it summarises the same Columbia College experiment, and it "
     "carries an OCR artefact ('jet' for 'yet'). Like article 05's p. 125 rejection: "
     "quote the lecture at pp. 166-167, not the recap at p. 127"),
    ("we are finally led to recognize, that since time immemorial we have, after all, "
     "always had \" electric light and heat \" at our disposal", 167,
     "the print sets ' electric light and heat ' in double quotes with spaces inside "
     "them, so check_quotes.py's scanner splits the run at the inner marks and each "
     "half needs its own '(1894, p. 167)' within 400 characters. It is a rhetorical "
     "flourish, not a claim; the 'veritable flame' sentence is what section 3 needs. "
     "If used at all, print only 'since time immemorial we have, after all, always "
     "had' and paraphrase the rest"),
    ("In no branch of electric industry is an advance more desired than in the "
     "manufacture of light", 290,
     "verifies exactly, but it is the London lecture's light-industry passage, not the "
     "cold-flame argument. Out of scope here (§1 scope discipline); it belongs to the "
     "light-production material at printed pp. 290-292"),
    ("It would enable us to obtain, by means of currents of very high frequencies, "
     "certainly 20 times, if not more, the quantity of light which is obtained in the "
     "present incandescent lamp by the same expenditure of energy", 258,
     "verifies exactly, and it is a tempting number, but it is a lamp-economy claim "
     "whose whole argument is the incandescence-of-the-gas passage on printed p. 258. "
     "A 20x figure quoted without that argument is exactly the kind of overclaim this "
     "series exists to catch. If used, quote the argument with it"),
    ("The higher the incandescence, the quicker the mean vibration, the greater is the "
     "economy of the light production", 258,
     "verifies, but it is the lamp argument again, and it reads like a thermodynamic "
     "law it is not. Not carried"),
    ("a frequency is conceivable - perhaps even obtainable - at", 166,
     "verifies through the dash folding, but it ends on a preposition and the sentence "
     "runs onto printed p. 167. The two halves are pinned separately above ('The higher "
     "the frequency...' on p. 166; 'which practically the same molecules...' on p. 167)"),
    ("the brush has but an ephemeral existence, and cannot, unfortunately, be "
     "indefinitely preserved in its most sensitive state", 226,
     "the ' -has' artefact again, and it is the start of that run. Not quotable; see "
     "rejected #6"),
    ("the glow of an incandescent lamp", 145,
     "'glow' occurs in the volume, but in the editor's introduction (printed p. 145) "
     "and about lamps, not about the brush. Do not build a 'glow' motif on it"),
]

# Notes the writer needs before drafting (feature-005/t5). §3 quote policy.
FLAGS = [
    "FOUR TEXTS, FOUR DATES, ONE ARTICLE. Printed pp. 166-171 are chapter XXVI, "
    "'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY'; its footnote "
    "verifies exactly as typed - 'A lecture delivered before the American Institute of "
    "Electrical Engineers, at Columbia College, N. Y., May 20, 1891.' (printed p. 145; "
    "the chapter runs printed pp. 145-197). Printed pp. 226-229, 258-259 and 290-292 "
    "are chapter XXVII, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF HIGH POTENTIAL AND "
    "HIGH FREQUENCY'; its footnote verifies exactly - 'Lecture delivered before the "
    "Institution of Electrical Engineers, London, February, 1892.' (printed p. 198; the "
    "chapter runs printed pp. 198-293). Printed p. 322 is chapter XXVIII, 'ON LIGHT AND "
    "OTHER HIGH FREQUENCY PHENOMENA', the Philadelphia and St. Louis lecture of "
    "February-March 1892 (printed pp. 294-373). Printed pp. 376 and 381 are chapter "
    "XXIX, the high-frequency alternator chapter, which is the EDITOR's text in the "
    "third person ('In one type of machine of this kind constructed by Mr. Tesla'), not "
    "a Tesla paper. Never write 'Tesla wrote in 1894': 1894 is the book, not the "
    "writing. Say which lecture a sentence comes from.",
    "THE STAGE MOMENT IS LONDON, NOT NEW YORK. §9 brief 06 section 1 quotes printed "
    "p. 258 and calls it 'the stage moment' without naming the text: it is the "
    "Institution of Electrical Engineers, London, February 1892 (ch. XXVII). Most of "
    "sections 2 and 3 are the Columbia College lecture, New York, May 20 1891 (ch. "
    "XXVI). These are two different papers a year apart; the article must not blend "
    "them into one 'Tesla on stage' scene, and each quote carries its own page for a "
    "reason.",
    "THE ALTERNATOR NUMBERS ARE THE BOOK'S, NOT TESLA'S. The 15,000 and 30,000 "
    "alternations-per-second figures (printed pp. 376, 381) come from chapter XXIX "
    "describing his machines in the third person. Cite them as the 1894 volume's account "
    "of the alternator, cross-checked against article 11 "
    "(11-tesla-high-frequency-alternator), which is built on that same chapter. Do not "
    "put them in his mouth, and do not use them to date the flame claim: the flame "
    "passages are 1891 and 1892.",
    "THE FLAME IS HOT. The §9 title is 'The Flame That Doesn't Burn: Tesla's Cold "
    "Fire', but the pinned text says the opposite three times: 'they are veritable "
    "flames, for they are hot' (p. 166), 'scorching hot air escapes at the top of the "
    "tube' (p. 167), 'Anything held within the brush is, of course, rapidly heated' "
    "(p. 167). What he actually claims is that it does not scorch the hand and does not "
    "dazzle the eye (p. 258) - cool beside a gas flame, not heatless. The article "
    "passes only if a reader comes away understanding that 'cold' is comparative.",
    "NO COLD FLAME IN THIS BOOK. 'cold flame' and 'cold fire' return 0 exact hits in "
    "the whole volume; so do 'corona', 'plasma', 'ioniz-', 'electron' (only fuzzy hits "
    "for 'electrode') and 'ultraviolet'. The book's words are 'brush', 'the hot brush' "
    "(printed pp. 127, 167), 'streams', 'a veritable flame'. So the title's 'Cold "
    "Flame'/'Cold Fire' stays outside quotation marks, and the modern explanation in "
    "section 2 is ours: no quotation marks, no page cite. 'ozone' is the one "
    "modern-sounding word that is his (printed pp. 127, 158, 171, 322).",
    "THE BRIEF'S QUOTE TEXT IS NOT THE PRINT'S. §9 brief 06 prints the p. 258 line with "
    "'light;' and a '?', and the p. 167 line with a Unicode ellipsis. The print has "
    "'intense light ;' (a space before the semicolon) and its question marks came out of "
    "this scan as '{' or ' ?'; the p. 167 sentence has em dashes, not an ellipsis. Use "
    "the forms in this file, not the brief's. The brief's p. 167 quote is also cut "
    "mid-sentence: it drops 'we have a possible way of producing' and 'and to "
    "accomplish this'.",
    "EM DASHES, AND THE TWO LEGAL FORMS OF THE p. 167 SENTENCE. The print sets 'by "
    "other than chemical means' off with em dashes. qa_page.py forbids em and en dashes "
    "in the article body, so the draft has exactly two safe forms: (a) the ASCII ' - ' "
    "form pinned here, which verifies exactly because grep_quote.py folds a typed ' - ' "
    "to the same normalised text as the print's em dash; or (b) the cut form 'a "
    "veritable flame, which would give light and heat without any material being "
    "consumed, without any chemical process taking place ... we only need to perfect "
    "methods of producing enormous frequencies and potentials', where check_quotes.py "
    "splits on the ASCII ' ... ' and each side verifies on printed p. 167. Do not print "
    "an em dash and do not print a Unicode ellipsis.",
    "OCR SPACING, NOT WORDING. The 1894 compositor puts a thin space before ';' and "
    "'?' in these passages ('intense light ;', 'fewer collisions ;'). The pinned forms "
    "keep that spacing so they pass as exact matches. If the draft prints the clean "
    "modern spacing ('light;'), check_quotes.py still passes it, through its "
    "space-ignoring index, and reports it as 'whitespace-only difference' - that is "
    "allowed, and it is not a licence to change any word. No [sic], no bracketed "
    "correction.",
    "CROSS-PAGE SENTENCES: CITE ONE PAGE, NEVER A RANGE. Three sentences here cross a "
    "folio: printed pp. 166->167 (the frequency thought), 213->214 (the verification "
    "hedge), 258->259 ('Were there means at hand...'). Where this file pins ONE "
    "fragment that straddles the break (pp. 213-214, 258-259), check_quotes.py accepts a "
    "citation to either page, so cite the page the sentence starts on. Where the file "
    "pins the two halves separately (pp. 166 and 167), each half must be cited to its "
    "own page. '(1894, pp. 258-259)' never satisfies check_quotes.py: its citation regex "
    "is '\\(1894, p{1,2}s?\\. ([\\d,\\s]+?)\\)', which cannot read a hyphen.",
    "NESTED QUOTE MARKS. The print sets \" electric light and heat \" in double quotes "
    "with spaces inside them (printed p. 167). check_quotes.py's scanner splits a quoted "
    "run at those inner marks and checks the halves separately, each needing its own "
    "citation within 400 characters. Prefer not to quote that sentence (rejected #12). "
    "In any quote that does contain inner double quotes, put the citation immediately "
    "after the closing mark and put nothing between.",
    "WHAT HE HEDGES, AND WHAT HE DOES NOT. The pinned set keeps his conditionals in "
    "view: 'I have no doubt that if the potential could be made to alternate with "
    "sufficient rapidity and power' (p. 167), 'a possible way of producing' (p. 167), "
    "'the experimental verification of the law, whatever it may be, would be exceedingly "
    "difficult' (p. 213), 'But as such means are not at disposal' (p. 259). He reports "
    "no working cold-flame lamp and no measured gain from one. The article's case - the "
    "idea was real, the apparatus was not - is carried by these sentences; no invented "
    "claim is needed.",
    "SAFETY (§4.1). The in-book basis for a caution is that these are coil and machine "
    "outputs at 'one or two hundred thousand volts' (p. 168) with 'scorching' air and a "
    "strong smell of ozone (pp. 167, 171). Use it for 'do not try this with "
    "mains-derived high voltage, and do not breathe the ozone', not for any health "
    "claim, and never imply the reader should repeat the experiment at home.",
    "HIS WORDING, NOT IDIOMATIC ENGLISH. The print reads 'It would, of course, be out "
    "of question to transmit...' (printed p. 291), with no 'the'; the modern idiom "
    "'out of the question' is a 0.983 near-match and check_quotes.py FAILS it. The same "
    "trap runs through this pin: 'flamelike', 'ozonizing', 'brilliancy', 'rarefy the air "
    "in the same', 'such means are not at disposal'. Quote his wording or drop the "
    "quotation marks; never modernise a phrase inside them.",
    "MODERN CLAIMS NEED MODERN SOURCES. Corona rings on high-voltage lines, commercial "
    "ozone generators, plasma globes and today's 'cold fire' videos are all outside this "
    "volume (rejected #9, #10). If the draft keeps brief 06 sections 5 and 6, each "
    "modern sentence needs a cited modern source in the Sources block, kept visibly "
    "separate from the 1894 material, or the sentence is cut.",
    "VOICE RULE (§0.5, enforced by qa_page.py). No em or en dashes, no curly quotes, no "
    "Unicode ellipsis in the article body. Every cut in this pin is ASCII ' ... ' for "
    "that reason; keep it that way in the draft.",
    "WORD COUNTS RE-RUN AT DRAFT TIME (feature-005/t5, 2026-10-11), not copied from "
    "this pin: whole-word matching over the text layer of our scan, whole volume. "
    "'cold flame' 0, 'cold fire' 0, 'corona' 0, 'plasma' 0, 'ioniz' 0, 'electron' 0, "
    "'ultraviolet' 0, 'combustion' 0. 'hot brush' 2 (printed pp. 127, 167). "
    "'veritable flame' 3 (printed pp. 120, 166, 167; p. 120 is the editor's "
    "introduction). 'ozone' 7 (printed pp. 127, 158, 171, 322, and the index at pp. "
    "495, 496). 'chemical process' 5 (printed pp. 127, 167, 214, 250, 272). "
    "'luminous funnel' 1 (printed p. 168). These are the counts the draft prints.",
    "MODERN SOURCES THE DRAFT CARRIES (§4.1: a modern technical claim needs a modern "
    "source or it is cut). All three were fetched and read on 2026-10-11, and every "
    "sentence they support is ours: no quotation marks, no page cite, kept visibly "
    "separate from the 1894 material. (1) Zobaa, A. M., Abdelnabi, H. H., Reda, R. M. "
    "and Mahmoud, A. G., 'Quantifying and mitigating electrical and environmental "
    "impacts of corona discharge', Scientific Reports 15, 41165 (2025), for corona on "
    "conductors: the field exceeding the dielectric strength of air (about 30 kV per cm "
    "at standard temperature and pressure), ionisation and an electron avalanche, a blue "
    "glow with audible noise, power loss and chemically active gas emissions, and "
    "corona rings, larger conductors and wider spacing as the mitigations. (2) US EPA, "
    "'Ozone Generators that are Sold as Air Cleaners', for ozone as a lung irritant "
    "(chest pain, coughing, shortness of breath, throat irritation at relatively low "
    "concentrations) and for the finding that at concentrations not exceeding public "
    "health standards ozone has little potential to remove indoor air contaminants. "
    "(3) Arizona State University Physics Instructional Resource Team, 'Plasma Globe', "
    "for the modern toy: low-pressure krypton, xenon or neon, an electrode at the "
    "centre, a high-voltage high-frequency transformer underneath at a few kilovolts "
    "and a frequency in the vicinity of 35 kHz, ionising the gas into filaments. No "
    "product claim from any site page is repeated here (§4.1).",
    "NESTED QUOTE MARKS AT PRINTED p. 171. The print sets the name of the biggest "
    "brush of the Columbia College lecture in double quotes with a leading space: "
    "'which may be appropriately called \" St. Elmo's hot fire,\" may be caused to "
    "appear at the other terminal of the secondary'. check_quotes.py's scanner splits "
    "a quoted run at inner double marks (same problem as the p. 167 \" electric light "
    "and heat \" flag), so the draft quotes only up to 'which may be appropriately "
    "called' and gives the name in our own sentence, unquoted. The name is the book's; "
    "it is 'St. Elmo's hot fire', which is the opposite of the title's word.",
    "THE OTHER NAME FOR THIS IS THE EDITOR'S, NOT TESLA'S. 'starting from the "
    "thread-like discharge and passing through various stages to the true electric "
    "flame' (printed p. 121) is the volume's editorial introduction writing about "
    "'Mr. Tesla' in the third person, like the p. 120 and p. 127 passages rejected "
    "above. Attribute it to the book, never to Tesla, and note that it is not 'cold' "
    "either: the 1894 names are 'the true electric flame' (editor), 'St. Elmo's hot "
    "fire' (Tesla, p. 171), 'the hot brush' (pp. 127, 167) and 'a veritable flame' "
    "(pp. 166, 167).",
    "'cold' IS IN THE BOOK SEVEN TIMES, AND NEVER HERE (re-run at draft time, "
    "feature-005/t5, whole-word over the normalised text layer): printed pp. 296, 300, "
    "311, 361, 362, 363, 387. They are the sensation of warmth or cold on skin, air "
    "condensed and solidified by intense cold, electrodes that may remain quite cold, "
    "an outer globe that stays cold while a button inside it is incandescent (twice), "
    "a medium that must be dark and cold, and a gas column between electrodes. Not one "
    "is about the brush or the flame. The string 'scorch' occurs three times, printed "
    "pp. 124, 167 and 258, and two of those are in the passages quoted here.",
    "THE BRIDGE PAGES WERE READ, NOT ASSUMED (the feature-005/t1 lesson). "
    "7-interesting-facts-about-magnets.html was opened at draft time, 2026-10-11: its "
    "H2s are lodestones, magnets around you, making a paperclip into a magnet, the "
    "Earth's magnetic poles and navigation, the Earth's magnetic core, electromagnets, "
    "roller coasters, and how magnets generate electricity. It contains no corona, no "
    "ozone and no plasma globe, so the bridge sentence describes it as this site's "
    "beginner page on magnetic fields and on magnet-generated current, and says "
    "plainly that the discharge is not on it. tesla-lit-lamps-without-wires.html and "
    "tesla-high-frequency-alternator.html were read the same way; their bridges "
    "describe what those pages actually do.",
]

# Notes for the figure task (feature-005/t6). Read the number off the scan.
FIGURE_NOTES = [
    "WHAT THE DRAFT (feature-005/t5) ALREADY COMMITS TO. article.md front matter names "
    "three figures, all marked NOT YET VISUALLY VERIFIED, and the body places them: "
    "figure 1 inside the first three H2s is /assets/tesla1894/p184-fig110.webp, which "
    "DOES NOT EXIST YET (crop Fig. 110 from books/pdf-pages-tesla-1894/page-184.pdf, "
    "the plate the p. 166 'two powerful brushes ... flames of a gas' sentence points "
    "at, add the manifest row, and use the p. 166 prose for the caption); figure 2 "
    "mid-article is /assets/tesla1894/p186-fig1.webp (printed p. 168, the spinning "
    "filament the prose calls Fig. 111 and the caption OCRs as 'FIG. ill.'), which "
    "exists and is unused but must be viewed against page-186.pdf first because "
    "manifest_qc.csv describes it as 'a primary coil with a pear-shaped vacuum lamp', "
    "which is not what the prose describes; figure 3 is /assets/tesla1894/p244-fig1-"
    "fig141.webp (printed p. 226, the vacuum bulb of Figs. 141-142), which exists, is "
    "unused, and is a dark plate needing negate and a gutter split. t7 renders only "
    "after t6 has created the p. 184 crop, because qa_page.py fails any <img> whose "
    "file is missing. If Fig. 110 will not crop useably, substitute the p. 228 "
    "page-scan crop described below and say so in the caption.",
    "the §9 brief 06 figure ids name PRINTED pages, but the files on disk are named by "
    "SCAN FILE (printed = scan - 18, §0). The three candidates map to: p247-fig151 -> "
    "website/assets/tesla1894/p265-fig1-fig151.webp (scan 265 = printed 247); "
    "p228-fig144 -> p246-fig1-fig144.webp, superseded by p228-figs144-145.webp; "
    "p179-fig117 -> p197-fig1-fig117.webp, superseded by p179-figs116-117.webp. Use "
    "the current filenames.",
    "TWO OF THE BRIEF'S THREE CANDIDATES ARE ALREADY USED. index.json figures[] read on "
    "2026-10-11: 1894_01 carries p179-figs116-117.webp, and 1894_02 carries "
    "p228-figs144-145.webp. §6.6's last rule says never reuse the same engraving on two "
    "articles unless the caption differs, and duplicate images across the series look "
    "thin. So the brief's p228-fig144 and p179-fig117 are blocked unless a genuinely "
    "different crop and caption are made.",
    "THE THIRD CANDIDATE DOES NOT SHOW A BRUSH. p265-fig1-fig151.webp is free, but the "
    "prose that names it is on printed p. 245: 'Fig. 151 illustrates a similar "
    "arrangement, with a large tube T protruding into the part of the bulb containing the "
    "refractory button' - a bulb construction detail. manifest_qc.csv row for it says "
    "'Caption spans Figs.151-152; the radiant-discharge half is the useful part - split "
    "at gutter; dark plate - negate'. It is not a flame and not a brush; brief 06's "
    "instruction to 'verify which show brush discharge visually' answers no for this one.",
    "THE FIGURE THE TEXT ACTUALLY POINTS AT HAS NO CROP. The p. 166 sentence pinned "
    "above ends '(Fig. 110)' - 'two powerful brushes several inches long, nearly white at "
    "their roots, which in the dark bear a striking resemblance to two flames of a gas "
    "escaping under pressure'. That is the article's central image, and there is no "
    "p184-* file in website/assets/tesla1894/ and no manifest_qc.csv row for scan file "
    "184: the extractor cut nothing from that page. feature-005/t6 must crop Fig. 110 "
    "from books/pdf-pages-tesla-1894/page-184.pdf, view it against the page, and add the "
    "manifest row. Caption from the p. 166 prose, never from a caption guess.",
    "FREE CROPS THAT DO SHOW THE PHENOMENA. (a) p186-fig1.webp (scan 186 = printed p. "
    "168) is unused; the p. 168 prose calls it Fig. 111 - 'the rapid spinning round in a "
    "circle of the top of the filament, thus presenting the appearance of a luminous "
    "funnel, Fig. Ill' (both the reference and the printed caption OCR as 'Ill' for 111; "
    "'luminous funnel' is 1 hit, printed p. 168). manifest_qc.csv describes the same file "
    "as 'a primary coil with a pear-shaped vacuum lamp glowing above it', which is not "
    "what the prose describes: verify against books/pdf-pages-tesla-1894/page-186.pdf "
    "before use and caption from the prose. (b) p244-fig1-fig141.webp (scan 244 = printed "
    "p. 226) and p245-fig1-fig141.webp (scan 245 = printed p. 227) are unused: these are "
    "the vacuum bulbs of Figs. 141-142, the apparatus behind the 'brush in high vacuum' "
    "passage quoted here, i.e. the plasma-globe ancestor. Both are dark plates; "
    "manifest_qc.csv says negate and split at the gutter.",
    "the book's own description of the brush-stage plates is pinned above: 'Figs. 143, 144 "
    "and 145 indicate different forms, or stages, of the brush' (printed p. 227). If 06 "
    "needs the plasma-globe look and the p. 228 plates are article 02's, either crop Fig. "
    "143 (printed p. 227, scan file 245) or use a page-scan crop of the p. 228 paragraph "
    "('it is usually sufficient to grasp the globe L with the hand'), which is §6.6 rule 4 "
    "- the words are the artefact. Article 03 did a page-scan crop of p. 486 and 05 of p. "
    "394; follow their crop handling and credit line.",
    "the §6.6 ratio and placement rules apply as everywhere: figure 1 within the first "
    "three H2s, figure 2 mid-article, at most one patent plate per two 1894 engravings. "
    "This chapter has plenty of its own art (Figs. 110, 111, 141-145), so a patent plate "
    "should not be needed; if one is used anyway, confirm the number on "
    "patents.google.com and credit it 'US patent NNN,NNN (year), Nikola Tesla.' (§4.2).",
    "index.json has no row for tid 1894_06 yet (rows exist for hub, 01-05, 07, 09, 11). "
    "feature-005/t6 creates it, with figures[] verified:true only after the crop has been "
    "viewed against the scan page, and quotes_pages/quotes_note pointing at this file.",
]

# Links (§5.2, for feature-005/t5 and t8).
LINK_NOTES = [
    "out-links per §5.2 row 06 and §9 brief 06: 7-interesting-facts-about-magnets.html, "
    "01 (tesla-lit-lamps-without-wires.html) and 12 (tesla-glowing-tubes-vacuum.html). "
    "Checked in website/ on 2026-10-11: 7-interesting-facts-about-magnets.html and "
    "tesla-lit-lamps-without-wires.html both exist; tesla-glowing-tubes-vacuum.html does "
    "not (it is feature-013 territory, not rendered). So 06 -> 12 cannot be added in t8; "
    "record it in index.json the way article 05's pin records its deferred link to 10, "
    "and add it when 12 is written.",
    "in-links required by §5.2 row 06: from 01, from 12 and from the hub. 01 is rendered "
    "(feature-001) but cannot link to a page that did not exist when it was written; 12 "
    "and the hub are unwritten (feature-013, feature-012). The qa_page.py reciprocal gate "
    "('>= 3 out-links to pages that link back') therefore cannot pass on 06 for any "
    "reason to do with 06: nothing on the site links to it yet. Record that in index.json "
    "the way article 11's entry records its backlink pass; do not pad 06 with off-map "
    "links to make the number.",
    "the natural bridge for brief 06 section 6 is 7-interesting-facts-about-magnets.html "
    "(the §5.2 row 06 target): corona rings, ozone smell and plasma globes are the "
    "everyday versions of what the 1894 brush is. Link it where the article turns to 'you "
    "have seen this', and do not repeat any product claim from it (§4.1).",
    "01 is the right sibling for the 'lamps lit without wires' material: brief 06 section "
    "4's point (the glass envelope was a workaround) is the same apparatus story 01 tells. "
    "Link 01 in that paragraph, not in the plasma-globe one.",
    "when feature-012 renders the hub, the hub card for 06 must not call this 'Tesla's "
    "cold flame' as if the phrase were his (see flags): the hub card wording is "
    "feature-012's job, and this pin is the record of what the phrase is not.",
]


def raw_window(body: str, frag: str, span: int = 220) -> str:
    """Show the scan's own text around a fragment.

    Same trick as the article 02/04/05 generators: the anchor is the longest literal
    run of the fragment that the raw page really contains, so the printed fragment
    always sits inside the window.
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


def main():
    pages = gq.load_pages(TXT)
    # The same index check_quotes.py builds, so a quote that passes here is a quote
    # that passes there: exact, or verbatim once OCR spacing is ignored.
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

    def how_note(checks, page):
        parts = []
        for i, (_f, how, _pps, _fp, _raw, straddle, others) in enumerate(checks, 1):
            tag = ("exact match, ratio 1.0" if how == "exact"
                   else "whitespace-only difference: the OCR spacing is not the "
                        "print's (words glued, or a stray space). Print the clean "
                        "form; check_quotes.py flags it the same way")
            lead = ("" if len(checks) == 1 else f"frag {i}: ")
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

    by_page = {}
    for r in rows:
        by_page.setdefault(r[1], []).append(r)

    out = [
        "# Article 06 quote pin: tesla-cold-flame.html",
        "",
        "SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped on "
        f"{PIN_DATE} from `books/extracted/tesla-1894-plain.txt` through the same "
        "matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR "
        "spacing is ignored) and is pinned to the printed page it was found on "
        "(printed page = scan file page - 18, §0). A quote carrying ' ... ' is cut "
        "where the scan is corrupt; each side of the cut is verified separately, "
        "which is how check_quotes.py will judge the draft. `article.md` for this "
        "page is written from this file; a quote that is not here does not go in the "
        "draft.",
        "",
        "Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola "
        "Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. "
        "Four different texts are quoted and they are not the same paper:",
        "",
        "- chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH "
        "FREQUENCY', a lecture delivered before the American Institute of Electrical "
        "Engineers at Columbia College, N. Y., May 20 1891 (printed pp. 145-197; the "
        "footnote verifies exactly, printed p. 145). This is the article's spine: the "
        "hot brush, the tube over the flame, the 'veritable flame' prospect. Printed "
        "pp. 166-167, 171.",
        "- chapter XXVII, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF HIGH POTENTIAL AND "
        "HIGH FREQUENCY', a lecture delivered before the Institution of Electrical "
        "Engineers, London, February 1892 (printed pp. 198-293; the footnote verifies "
        "exactly, printed p. 198). The stage moment, the vacuum brushes, the plasma "
        "globe. Printed pp. 226-229, 258-259, 291.",
        "- chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', the "
        "Philadelphia and St. Louis lecture, February-March 1892 (printed pp. "
        "294-373). One quote, on the brush discharge as an energy loss. Printed p. 322.",
        "- chapter XXIX, the high-frequency alternator chapter - the EDITOR's text in "
        "the third person, the same chapter article 11 is built on. The 15,000 and "
        "30,000 alternations-per-second figures. Printed pp. 376, 381. Attribute these "
        "to the book, not to Tesla.",
        "",
        f"Verified: {len(rows)} quotes ({sum(len(r[4]) for r in rows)} fragments) "
        f"across {len(by_page)} printed pages, 0 failures. To re-check one quote: "
        "`python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>`. To "
        "regenerate this file: "
        "`python3 new_content/1894-series/06-tesla-cold-flame/gen_quotes.py` "
        "(it exits non-zero and writes nothing if any quote fails).",
        "",
    ]
    for page in sorted(by_page):
        rows_p = by_page[page]
        out += [f"## Printed p. {page} (scan file {rows_p[0][4][0][3]})", ""]
        # rows_p[0][4][0][3] is the scan file page of the first verified fragment
        for quote, _p, section, why, checks in rows_p:
            straddling = [c for c in checks if len(c[5]) > 1]
            out += [f"### {section}", "", f'> "{quote}"', "",
                    f"- cited as: `(1894, p. {page})`"]
            if straddling:
                out += [f"- straddle: this ONE fragment sits on printed pp. "
                        f"{straddling[0][5][0]}-{straddling[0][5][-1]} as a single "
                        "run; check_quotes.py accepts a citation to either page, so "
                        "cite one page only - '(1894, pp. ...)' never matches"]
            out += [f"- why: {why}",
                    f"- check_quotes.py: {how_note(checks, page)}"]
            for i, (frag, _how, _pps, _fp, raw, _st, _ot) in enumerate(checks, 1):
                tag = "" if len(checks) == 1 else f" (frag {i}: {frag[:40]})"
                out += [f"- raw OCR{tag}: `{raw}`"]
            out += [""]
    out += ["## Rejected: considered and not carried forward", ""]
    for quote, page, why in REJECTED:
        where = f"p. {page}" if page else "not in this volume"
        out += [f"- ~~\"{quote}\"~~ ({where}): {why}"]
    out += ["", "## Flags for the writer (§3 quote policy, feature-005/t5)", ""]
    out += [f"- {f}" for f in FLAGS]
    out += ["", "## Notes for the figure task (feature-005/t6)", ""]
    out += [f"- {f}" for f in FIGURE_NOTES]
    out += ["", "## Links (§5.2, for feature-005/t5 and t8)", ""]
    out += [f"- {f}" for f in LINK_NOTES]
    out += [""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out))
    print(f"wrote {OUT} ({len(rows)} quotes, "
          f"{sum(len(r[4]) for r in rows)} fragments, "
          f"{len(by_page)} printed pages, {len(REJECTED)} rejected)")


if __name__ == "__main__":
    main()
