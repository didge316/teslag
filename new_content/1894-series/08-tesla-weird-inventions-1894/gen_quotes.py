#!/usr/bin/env python3
"""Regenerate quotes.md for article 08 (feature-006/t0, batch 1: entries 1-3).

Run: python3 new_content/1894-series/08-tesla-weird-inventions-1894/gen_quotes.py

Every quote is re-grepped at generation time through the same matcher
books/tools/check_quotes.py uses (exact, or verbatim once OCR spacing is ignored);
if a quote does not verify on its stated printed page the script exits non-zero and
writes nothing. That is the point of the file (SERIES-PLAN-1894.md §8 step 2, §0
non-negotiable 2): the draft is written from this, never from memory.

BATCHES. feature-006 splits the quote pin into three batches so that one turn does
not die at the supervisor wall-clock cap: t0 = entries 1-3 (what this file holds
now), a08-qp2 = entries 4-6, a08-qp3 = entries 7-9, a08-qpdone = all nine
re-checked together. Append to QUOTES / REJECTED / FLAGS / FIGURE_NOTES /
LINK_NOTES in those tasks and re-run: the header counts and the per-page sections
are regenerated, so nothing in quotes.md is hand-maintained. Entries 1-3 are the
three chapters at printed pp. 409-423; entries 4-9 run printed pp. 424-476.

A pinned quote may carry " ..." where the printed text is cut for an OCR artefact.
Each fragment between the cuts is verified separately, which is exactly how
books/tools/check_quotes.py will judge the draft in feature-006/t1 - so this script
does not reimplement that check, it imports it (check_quotes.fragments +
check_quotes.locate over the index check_quotes builds). If a quote passes here it
passes there.
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
           "08-tesla-weird-inventions-1894/quotes.md")

PIN_DATE = "2026-10-12"
BATCH = ("batch 1 of 3: §9 brief 08 entries 1-3, the three Part III chapters at "
         "printed pp. 409-423")

# (quote as it will be printed, printed page, brief 08 entry, why it is in the piece)
QUOTES = [
    # --- Provenance. Part III is the editor's third-person account of Tesla's
    # devices, not Tesla's prose; the draft has to say so, and these are the proof.
    ("includes a great many other inventions in arc lighting, transformers, "
     "pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, "
     "improvements in dynamos, new forms of incandescent lamps, electrical meters, "
     "condensers, unipolar dynamos, the conversion of alternating into direct "
     "currents",
     6, "0. Provenance (the editor's own inventory, ch. I)",
     "the editor's own list of the 'Miscellaneous' section, printed p. 6, and it maps "
     "almost item for item onto §9 brief 08's nine entries: conversion of alternating "
     "into direct currents (entry 1), condensers (2), electrical meters (3), "
     "thermo-magnetic motors and pyro-magnetic generators (4), third-brush regulation "
     "(6), improvements in dynamos (7), arc lighting (8), unipolar dynamos (9). Use it "
     "to show the list is the book's, not ours. Start the quote at 'includes': the "
     "print sets ' Miscellaneous ' in its own quote marks, which would split the run "
     "in check_quotes.py's scanner. Also the only place in the volume where "
     "'pyro-magnetic generators' is hyphenated (see the closing-beat flag)"),
    ("The present volume deals simply with his work accomplished to date",
     6, "0. Provenance (ch. I)",
     "the editor's own date fence on the whole volume: everything in it is work "
     "already done by 1894. That is what licenses the article's question - these are "
     "devices built and written up by 1894, so asking why they never caught on is "
     "fair, and no 'Tesla predicted the future' framing is needed (§4.1)"),

    # --- Entry 1. Getting DC directly from AC (ch. XXXIII, printed pp. 409-417)
    ("THIS method consists in obtaining direct from alternating currents, or in "
     "directing the waves of an alternating current so as to produce direct or "
     "substantially direct currents",
     409, "Entry 1. Getting DC directly from AC (ch. XXXIII opening)",
     "the book's own one-sentence statement of the invention, in its opening line. "
     "Note 'substantially direct': the claim is never a pure direct current. Entry 1 "
     "opens here"),
    ("the waves of current of one sign will, partly or wholly, pass over one of the "
     "paths or branches, while those of the opposite sign pass over the other",
     409, "Entry 1. Getting DC directly from AC",
     "the mechanism in one clause: the two half cycles are separated and sent to two "
     "different circuits. This is not a one-way device - both halves are used, they "
     "just go different ways. The draft must not call it a rectifier in the modern "
     "single-output sense"),
    ("There may thus be obtained from an alternating current two or more direct "
     "currents without the employment of any commutator",
     409, "Entry 1. Getting DC directly from AC",
     "the claim the entry is built on, and the reason the brief's hook ('before "
     "solid-state rectifiers') is defensible: the book says expressly that no "
     "commutator is needed. Pinned to the end of the printed page; the sentence runs "
     "onto printed p. 410 and its far end is pinned there. Cite p. 409 for this half"),
    ("such as it has been heretofore regarded as necessary to use",
     410, "Entry 1. Getting DC directly from AC",
     "the far half of the same sentence, on printed p. 410. Pinned separately so each "
     "half carries its own page: check_quotes.py cannot read '(1894, pp. 409-410)'"),
    ("an active (as distinguished from a dead) resistance or opposition to the "
     "currents of one sign, for the purpose of diverting the currents of that sign "
     "through the other or another path, but permitting the currents of opposite sign "
     "to pass without substantial opposition",
     416, "Entry 1. Getting DC directly from AC",
     "the general principle as the book states it, after six variants: an ACTIVE "
     "opposition, not resistance in the ohmic sense. 'Active as distinguished from "
     "dead' is the distinction the entry has to explain, and it is why every working "
     "form of this needs a source of electromotive force or a machine, not a piece of "
     "semiconductor"),
    ("The current in either branch may be used in the same way and for the same "
     "purposes as any other direct current - that is, it may be made to charge "
     "secondary batteries, energize electro-magnets, or for any other analogous "
     "purpose",
     410, "Entry 1. Getting DC directly from AC",
     "what the direct current was for, in the book's words: battery charging and "
     "electro-magnets. The ASCII ' - ' form verifies exactly because grep_quote.py "
     "folds a typed ' - ' to the same text as the print's em dash; the draft may not "
     "print an em dash (§0 non-negotiable 5)"),
    ("the rotation and action of the commutator must be in synchronism or in proper "
     "accord with the periods of the alternations",
     412, "Entry 1. Getting DC directly from AC (why it lost)",
     "the catch, in the book's own words: the mechanical variant has to run in step "
     "with the supply. First of three pinned synchronism sentences; see the flag on "
     "why entry 1 lost"),
    ("The armatures are rotated in synchronism with the alternations from the source "
     "A",
     413, "Entry 1. Getting DC directly from AC (why it lost)",
     "the same requirement in the electro-magnetic variant (Fig. 223): a rotating "
     "machine locked to the line frequency"),
    ("designed to be rotated in synchronism with the alternations of current",
     416, "Entry 1. Getting DC directly from AC (why it lost)",
     "and in the 'magnetic' variant (Fig. 225), the one that drops the separate "
     "continuous-current source by using permanent magnets: still a synchronously "
     "rotating armature. Three pages, three variants, one requirement - that is the "
     "case against the device, and every clause of it is page-cited"),
    ("Mr. Tesla is enabled to produce a self -exciting alternating dynamo, or to "
     "operate direct current meters on alternating-current circuits or to run various "
     "devices - such as arc lamps - by direct currents in the same circuit with "
     "incandescent lamps or other devices operated by alternating currents",
     417, "Entry 1. Getting DC directly from AC",
     "what the book thought the invention was for: putting direct-current loads onto "
     "an alternating-current circuit, not making direct current for its own sake. It "
     "names operating DIRECT CURRENT METERS on alternating-current circuits, which is "
     "entry 3's meter - the two entries are linked inside the book, which is a better "
     "listicle than any invented connection. The 'self -exciting' spacing is the "
     "print's"),
    ("Mr. Tesla divides such circuit at any desired point into two branches or paths",
     409, "0. Provenance (the Part III voice)",
     "the evidence that this chapter is the EDITOR writing about Tesla in the third "
     "person ('Mr. Tesla divides', 'In one of these paths he inserts'), not Tesla "
     "writing. Pin it so the draft can say plainly that the Part III chapters are the "
     "book's account of his devices. Never 'Tesla wrote in 1894'"),

    # --- Entry 2. Condensers with the plates in oil (ch. XXXIV, printed pp. 418-419)
    ("In experimenting with currents of high frequency and high potential, Mr. Tesla "
     "has found that insulating materials such as glass, mica, and in general those "
     "bodies which possess the highest specific inductive capacity, are inferior as "
     "insulators in such devices when currents of the kind described are employed "
     "compared with those possessing high insulating power, together with a smaller "
     "specific inductive capacity",
     418, "Entry 2. Condensers with the plates in oil",
     "the counter-intuitive finding the entry is built on: the best insulators for "
     "this job are NOT the high-inductive-capacity ones (glass, mica). This is what "
     "lifts the entry above 'he put capacitors in oil'. Long, but it is one sentence "
     "and cutting it would change the claim"),
    ("it is very desirable to exclude all gaseous matter from the apparatus, or any "
     "access of the same to the electrified surfaces, in order to prevent heating by "
     "molecular bombardment and the loss or injury consequent thereon",
     418, "Entry 2. Condensers with the plates in oil",
     "the reason: gas in the space is heated by molecular bombardment, and it costs "
     "energy or destroys the device. The sentence the brief's hook ('the reason your "
     "capacitor is not in air') rests on - but see rejected #10: the step from here "
     "to a modern capacitor is OURS and needs a modern source"),
    ("he has shown that in a condenser a considerable amount of energy may be "
     "wasted, and the condenser may break down merely because gaseous matter is "
     "present between the surfaces",
     418, "Entry 2. Condensers with the plates in oil (the editor's footnote)",
     "the editor's own footnote on the same page, spelling out why the invention "
     "follows from the lectures. Attribute it to the editor, never to Tesla: it is "
     "third-person about 'Mr. Tesla's experiments', and it is a footnote, not the "
     "chapter's own text"),
    ("Mr. Tesla shows that in a fluid such as oil the losses are very small as "
     "compared with those incurred in a gas",
     418, "Entry 2. Condensers with the plates in oil (the editor's footnote)",
     "the case for oil specifically, from the same footnote. Note the hedge around it "
     "('as the careful reader of his three lectures will perceive'): the editor is "
     "deriving this from the three lectures, not reporting a measurement. That is also "
     "the proof that the book itself treats ch. XXXIV as following from the lecture "
     "material, which is a fact the article can use about the book"),
    ("The space within the can is filled with oil G. Such a condenser will prove "
     "highly efficient and will not become heated or permanently injured",
     419, "Entry 2. Condensers with the plates in oil",
     "the device as actually drawn: a sealed can, plates held apart by porous strips, "
     "the space filled with oil. 'Will prove' is a prediction, not a test result - the "
     "entry must not report a measured improvement"),
    ("The plates ordinarily are separated by strips of porous insulating material F, "
     "which are used merely for the purpose of maintaining them in position",
     419, "Entry 2. Condensers with the plates in oil",
     "the detail that makes the design intelligible: the solid insulator is only a "
     "spacer ('merely for the purpose of maintaining them in position'), because the "
     "dielectric is the oil. The one-sentence explanation of the whole invention"),
    ("it has been a common practice to interpose a body of oil between two "
     "conductors for purposes of insulation ; but Mr. Tesla believes he has "
     "discovered peculiar properties in oils which render them very valuable in this "
     "particular form of device",
     419, "Entry 2. Condensers with the plates in oil (why it is not obvious)",
     "the book's own hedge on the novelty: oil between conductors was already "
     "standard practice, and what is claimed is a belief ('Mr. Tesla believes he has "
     "discovered peculiar properties'). The spaced ';' is the print's; keep it and the "
     "quote verifies as an exact match. This is the honest 'why it lost' material "
     "entry 2 has: part of the idea was already in use"),

    # --- Entry 3. Electrolytic registering meter (ch. XXXV, printed pp. 420-423)
    ("an ingenious form of electrolytic meter attributable to Mr. Tesla is one in "
     "which a conductor is immersed in a solution",
     420, "Entry 3. Electrolytic registering meter (ch. XXXV opening)",
     "the opening line and the book's own attribution formula ('attributable to Mr. "
     "Tesla'), further evidence that the Part III chapters describe his devices for "
     "him. Entry 3 opens with the device, not with the brief's hook"),
    ("metal may be deposited from the solution or taken away in such a manner that "
     "the electrical resistance of the conductor is varied in a definite proportion to "
     "the strength of the current the energy of which is to be computed",
     420, "Entry 3. Electrolytic registering meter",
     "the mechanism: metal plates grow or shrink in the solution and their RESISTANCE "
     "changes in proportion to the current. Verifies only through check_quotes.py's "
     "space-ignoring index (the OCR glues 'isvaried'); print the clean form. This is "
     "the sentence that disproves the brief's 'counts bubbles' hook - see rejected #9"),
    ("the deposit is uniform along the whole of one of the conductors, while the "
     "metal is taken away uniformly from the other",
     420, "Entry 3. Electrolytic registering meter",
     "why the design is clever rather than crude: a constant potential difference along "
     "the whole immersed length makes the deposit uniform, so the resistance change is "
     "proportional instead of local. Its reason ('as there is a constant difference of "
     "potential between the two conductors throughout the entire extent that is "
     "exposed to the solution, the current density through such solution is the same "
     "at all corresponding points') verifies exactly on the same page if the draft "
     "wants it"),
    ("the increase of resistance of one conductor or the diminution of the resistance "
     "of the other per lamp hour",
     422, "Entry 3. Electrolytic registering meter",
     "the unit the book actually uses: per LAMP HOUR, not per ampere-hour. 'lamp hour' "
     "is 1 hit in the whole volume and it is here. The concrete quotable detail the "
     "entry needs, and it dates the meter to a lighting tariff"),
    ("These two measurements evidently serve as a check, since the gain of one "
     "conductor should equal the loss of the other",
     422, "Entry 3. Electrolytic registering meter",
     "how the meter was read: measure both conductors before and after, and the two "
     "readings check each other. Sets up the next quote, which is the fatal operating "
     "step"),
    ("the instrument reversed, so that the deposit will be taken from the conductor "
     "which has gained and added to that which has lost",
     423, "Entry 3. Electrolytic registering meter (why it lost)",
     "the fatal step, in the book's own text: after every registration you must "
     "reverse the current and plate the deposit back. Pinned from 'the instrument "
     "reversed' because the print reads 'should -be changed' with a stray hyphen (see "
     "rejected #1). This is the operational reason the meter lost, and it needs no "
     "invention of ours"),
    ("it is possible to read off directly the amount of the energy expended by means "
     "of a properly constructed ohm-meter and without resorting to weighing the "
     "deposit",
     423, "Entry 3. Electrolytic registering meter",
     "what this design claimed over the older weighing kind: read it off an ohm-meter. "
     "Note 'a properly constructed ohm-meter' - the reading instrument was itself part "
     "of the unsolved problem. 'ohm-meter' is 1 hit in the volume, here"),
    ("the accuracy of the instrument and correctness of the indications are but "
     "slightly affected by changes in temperature",
     423, "Entry 3. Electrolytic registering meter",
     "the last listed advantage and the one that reads most modern (thermal drift). "
     "Verifies through the space-ignoring index only ('bychanges' is glued in the "
     "OCR). Attribute the whole advantages list to the book: the sentence before it "
     "begins 'It is also said that such meters have the merit of', which is reported "
     "claim, not measurement"),
    ("Electrolytic meters seem to need every auxiliary advantage to make them "
     "permanently popular and successful, no matter how much ingenuity may be shown "
     "in their design",
     423, "Entry 3. Electrolytic registering meter (why it lost)",
     "the book's own verdict on this class of meter, closing the chapter, and the "
     "strongest 'why it lost' sentence in this batch: the 1894 editor already knew the "
     "type was not winning. Quote it as the editor's, and put it at the end of the "
     "entry"),
]

# Considered and NOT carried forward, with the reason. Each reason states what the
# scan really says, so the writer can see why the quote is unusable.
REJECTED = [
    ("the direction of the current should be changed or the instrument reversed, so "
     "that the deposit will be taken from the conductor which has gained and added to "
     "that which has lost", 423,
     "the print reads 'the direction of the current should -be changed' with a stray "
     "hyphen before 'be' (ratio 0.994 for the clean form, a FAIL, and the hyphen "
     "survives both normalisers). Pin from 'the instrument reversed' instead, which "
     "verifies exactly, and put the reversing step in our own words ahead of it"),
    ("Then a known current is passed through the instrument for a given time, and by "
     "a second measurement the increase and diminution of the resistances of the two "
     "conductors are respectively taken", 421,
     "the print reads 'for a -given time' with a stray hyphen (ratio 0.995, a FAIL). "
     "The measuring procedure is carried instead by the two p. 422 quotes pinned above "
     "('per lamp hour', and the gain-equals-loss check)"),
    ("Other modifications of these methods are possible, but need not be pointed out",
     417,
     "verifies exactly, but on printed p. 416, not p. 417: it is the last line of the "
     "p. 416 paragraph, before the p. 417 recap. If the draft wants the 'there were "
     "more variants' point it must cite p. 416. Not carried: the three synchronism "
     "quotes do more work for entry 1"),
    ("Fig. 227 is a section of a condenser constructed in accordance with this "
     "principle and having stationary plates", 418,
     "the FIG. 227 and FIG. 228 captions are printed on p. 418, but the sentence "
     "describing them is on printed p. 419 (ratio 1.0 there, no match on 418). Cite "
     "p. 419 for the description and p. 418 only for the engraving itself. The form "
     "that verifies is 'In the accompanying illustrations, Fig. 227 is a section of a "
     "condenser ...' on p. 419"),
    ("but it it has been a common practice to interpose a body of oil between two "
     "conductors", 419,
     "the print doubles the word: 'and it it has been a common practice'. The pinned "
     "form starts after the duplication. Do not repair it inside quotation marks (§3: "
     "never re-word inside the marks); start the quote at 'it has been a common "
     "practice'"),
    ("any 1894 verdict that the AC-to-DC conversion device was a failure, or that it "
     "was 'a simple matter'", 0,
     "no such sentence anywhere in the volume. Ch. XXXIII reports no commercial result "
     "at all: it gives six variants and their uses, and it actually DEFENDS the "
     "commutator variant ('The disadvantages of this arrangement, which would seem to "
     "result from the employment of sliding contacts, are in reality very slight', "
     "printed p. 413 - verified, kept below as rejected #15). So entry 1's 'why it "
     "lost' must be built from what the text does say - the synchronism requirement, "
     "pinned three times - plus a cited modern source for what replaced it. Never from "
     "an invented 1894 verdict (§4.1: no invented anecdotes, dates, or 'historians "
     "say')"),
    ("rectifier / rectification / solid-state / semiconductor / diode / valve (as a "
     "component)", 0,
     "'rectif' 0 hits in the whole volume, 'diode' 0, 'semiconductor' 0. 'valve' "
     "occurs only at printed pp. 431 and 447, and 'oscillation valve' at pp. 129, 191, "
     "217, 316, 492 - in every case his spark-gap air valve, never a rectifier "
     "component. The book's vocabulary for conversion is 'directing' the waves, "
     "'translating devices', 'active resistance', 'commutator'. So the brief's hook "
     "'before solid-state rectifiers' is OUR framing: it stays outside quotation marks, "
     "and any sentence placing this device in a history of rectifiers needs a modern "
     "source (§4.1) or it is cut. No modern source is carried in this batch; feature-"
     "006/t1 must fetch one if it keeps that sentence"),
    ("ampere-hour / amp-hour (as this meter's unit)", 0,
     "'ampere' occurs 7 times in the volume (printed pp. 81, 82, 124, 149, 290, 317, "
     "377) and never as a metering unit; 'ampere-hour' 0 hits. The unit this meter is "
     "specified in is the LAMP HOUR (printed p. 422, 1 hit in the volume). §9 brief "
     "08's 'an amp-hour meter' is our anachronism: write lamp-hour, or say plainly "
     "that the 1894 unit is the lamp-hour"),
    ("an amp-hour meter that counts bubbles", 0,
     "the brief's hook for entry 3, and it is wrong about the device. 'bubble' occurs "
     "9 times in the volume (printed pp. 130, 173, 222, 223, 251) and never in this "
     "chapter. The meter registers a CHANGE IN RESISTANCE caused by metal plating on "
     "and off two conductors, and the book expressly praises reading it off an ohm-"
     "meter 'without resorting to weighing the deposit' (printed p. 423). Nothing in "
     "it counts gas. Do not print the hook; write the entry from the pinned mechanism"),
    ("the reason your capacitor is not in air", 0,
     "our modern claim, not the book's. The 1894 text argues for excluding gas from "
     "condensers used with CURRENTS OF HIGH FREQUENCY AND HIGH POTENTIAL specifically "
     "(printed p. 418); it never generalises to ordinary power or tuning apparatus, and "
     "air-dielectric condensers were in ordinary use at the time ('condenser' 218 hits "
     "across the volume, 'specific inductive capacity' 18, 'molecular bombardment' 15, "
     "of which this chapter is one). The step from p. 418 to a modern capacitor needs "
     "a modern source (§4.1) or the sentence is cut, and the entry must state what the "
     "1894 claim is limited to"),
    ("that condensers with the plates in oil lost, or were superseded", 0,
     "the volume gives no failure for entry 2, and the honest reading is that this one "
     "did not simply lose: oil as a dielectric and as an impregnant became standard in "
     "high-voltage apparatus. What did not survive is the specific 1894 form - a can of "
     "oil with rod-adjustable plates (printed p. 419). If the draft keeps a 'why it "
     "lost' beat for entry 2 it has to be about that form, with a cited modern source "
     "for where oil dielectrics went; otherwise entry 2 is the one item in the list "
     "that wants reframing as 'the one that won', which §9 brief 08's title does not "
     "allow. Flag for feature-006/t1 and for the brief owner"),
    ("Figs. 221, 222, 223, and 224 illustrate what may termed", 411,
     "verifies exactly, but the print is itself defective: 'what may termed' is "
     "missing a word ('may be termed'). Quoting it needs '[sic]' or a bracketed "
     "repair, and §3 forbids re-wording inside the marks. Not carried; the figure "
     "references are covered by the p. 410 and p. 421 quotes pinned above"),
    ("the electrical resistance of the conductor is varied in a definite proportion "
     "to the strength of the current", 420,
     "verifies only through the space-ignoring index (the OCR glues 'isvaried'), so "
     "check_quotes.py passes it but flags it. Carried inside the longer form above "
     "rather than as a separate short quote, so the flagged fragment appears once"),
    ("it is not necessary to employ shunts, for the whole of the current to be "
     "measured may be passed through the instrument", 423,
     "verifies exactly, and it is the second listed advantage, but three advantage "
     "quotes in one entry is padding (§3 'Do not pad'). The ohm-meter and temperature "
     "quotes carry the advantages; this one is available if the draft needs it"),
    ("The disadvantages of this arrangement, which would seem to result from the "
     "employment of sliding contacts, are in reality very slight", 413,
     "verifies exactly, but it is the book arguing that the commutator variant IS "
     "practical, which cuts against entry 1's 'why it lost'. Kept here on purpose: if "
     "the draft is honest about why the device lost, this is the counter-evidence it "
     "should acknowledge rather than hide (see rejected #6)"),
    ("magnetic generator (as a name Tesla used for his own devices)", 0,
     "4 hits for 'magnetic gener' in the whole volume: printed p. 6 (the editor's "
     "list, 'pyro-magnetic generators'), p. 429 ('pyromagnetic generator of "
     "electricity'), p. 496 (the index, 'Pyromagnetic Generators 429'). Every one is "
     "PYRO-magnetic, which is what §9 brief 08's closing beat claims and it holds. But "
     "Appendix D says 5 hits and lists p. 424: the fifth is the ch. XXXVI heading "
     "itself, which this scan OCRs as 'MOTORS AND PYRO-MAGNETIC RATORS' because "
     "'GENE-' is cut at the foot of the page, so it cannot be re-grepped at all. State "
     "the closing beat from pp. 429 and 496 and treat the heading as a page-scan "
     "detail, not a greppable quote. Batch 2 owns entry 4 (printed pp. 424-431)"),
]

# Notes the writer needs before drafting (feature-006/t1..t3). §3 quote policy.
FLAGS = [
    "PART III IS THE EDITOR'S TEXT, IN THE THIRD PERSON, ABOUT TESLA'S DEVICES. All "
    "three chapters in this batch sit in Part III, 'MISCELLANEOUS INVENTIONS AND "
    "WRITINGS' (contents, scan file 16): ch. XXXIII 'METHOD OF OBTAINING DIRECT FROM "
    "ALTERNATING CURRENTS' (printed pp. 409-417), ch. XXXIV 'CONDENSERS WITH PLATES "
    "IN OIL' (printed pp. 418-419), ch. XXXV 'ELECTROLYTIC REGISTERING METER' "
    "(printed pp. 420-423). None is a Tesla paper or lecture. The prose says 'Mr. "
    "Tesla divides such circuit', 'In carrying out this idea Mr. Tesla employs', 'an "
    "ingenious form of electrolytic meter attributable to Mr. Tesla'. Never 'Tesla "
    "wrote in 1894', never put this prose in his mouth, and attribute it as the book's "
    "account of his devices. This is the same trap the article 06 pin flags for ch. "
    "XXIX, and it is the biggest accuracy risk in article 08: a listicle about "
    "'Tesla's weird inventions' naturally writes about him in the third person too, "
    "and the two third-persons blur into one. The fix is to name the chapter and the "
    "page every time, and to say once, early, that Part III is the editor's writing.",
    "THE NINE ENTRIES ARE THE BOOK'S, NOT OURS. The editor's inventory at printed p. "
    "6 maps onto §9 brief 08's table almost item for item (see the pinned quote). Say "
    "so in the intro: the list comes out of the volume's own contents pages and its "
    "own editor. That also proves the nine are real and dated, which is the article's "
    "whole claim to trust. The contents pages are scan files 16-17 and carry no "
    "printed folio, so cite the running text at printed p. 6 for the inventory and the "
    "chapter openings for the individual devices.",
    "CHAPTER NUMBERS OCR BADLY IN PART III. The contents page (scan file 16) gives "
    "XXXIII, XXXIV and XXXV correctly, but the chapter headings themselves print as "
    "'CHAPTER XXXIY.' (for XXXIV, printed p. 418) and 'CHAPTER ELECTROLYTIC XXXY. "
    "REGISTERING METER.' (for XXXV, printed p. 420, where the display type and the "
    "chapter title are interleaved in the OCR). Do not quote a roman numeral from the "
    "heading; name the chapter by its title, which is unambiguous, and cite the page. "
    "If a chapter number must appear, take it from the contents page and say it is "
    "from the contents.",
    "THE BRIEF'S HOOKS ARE NOT THE PRINT'S, AND TWO OF THEM ARE WRONG. §9 brief 08 "
    "gives entry 3 as 'an amp-hour meter that counts bubbles' and entry 2 as 'the "
    "reason your capacitor is not in air'. The meter counts no bubbles and its unit is "
    "the lamp-hour (rejected #8, #9); the condenser claim is about high-frequency, "
    "high-potential apparatus only and the modern step is ours (rejected #10). The "
    "hooks are prompts, not sources: nothing from the hooks goes inside quotation "
    "marks or carries a page cite, and where a hook contradicts the text the text "
    "wins. Entry 1's hook ('before solid-state rectifiers') is workable but needs a "
    "modern source for the history sentence (rejected #7).",
    "ENTRY 2 IS THE ENTRY THAT DID NOT LOSE. The brief asks for 'why it lost' nine "
    "times, and for entry 2 the honest answer is that the principle won (oil and "
    "oil-impregnated dielectrics are standard in high-voltage apparatus) while the "
    "particular 1894 form - plates in an oil-filled can, adjusted from outside by "
    "threaded rods - is nothing anyone builds. The 1894 text supports the second half "
    "of that sentence and not the first. Either write entry 2 that way, with a cited "
    "modern source for the first half, or flag it to the brief owner before drafting; "
    "do not invent a 1894 failure (rejected #11).",
    "WHY ENTRY 1 LOST, STATED ONLY FROM THE TEXT. The volume never says the "
    "conversion scheme failed; it defends it (rejected #15). What it does say, three "
    "times on three pages, is that every working variant has to run in step with the "
    "supply: 'the rotation and action of the commutator must be in synchronism or in "
    "proper accord with the periods of the alternations' (p. 412), 'The armatures are "
    "rotated in synchronism with the alternations from the source A' (p. 413), "
    "'designed to be rotated in synchronism with the alternations of current' (p. 416). "
    "It also says the opposition has to be ACTIVE, not ohmic (p. 416), and that the "
    "simplest form puts a battery or a continuous-current dynamo in each branch (p. "
    "409). Those five sentences are enough to explain, without one invented word, why "
    "the scheme waited for something that had neither a rotating part nor a synchronism "
    "requirement. Say what replaced it only with a modern source (rejected #7).",
    "WHAT THE BOOK HEDGES, AND WHAT IT DOES NOT. Keep the conditionals in view: 'Such "
    "a condenser WILL PROVE highly efficient' (p. 419, a prediction), 'Mr. Tesla "
    "BELIEVES he has discovered peculiar properties' (p. 419), 'It is ALSO SAID that "
    "such meters have the merit of superior economy and compactness' (p. 423), "
    "'produce direct OR SUBSTANTIALLY direct currents' (p. 409), 'partly or wholly' "
    "(p. 409), 'it will be sufficient if the waves are only PARTIALLY diverted' (p. "
    "416). No experiment, efficiency figure, tariff or sales result is reported for any "
    "of the three devices. The article's case - real devices, real ingenuity, no "
    "evidence of commercial success - is carried by these hedges; nothing needs to be "
    "invented, and any number we do not find in the text does not go in the draft.",
    "CROSS-PAGE SENTENCES: CITE ONE PAGE, NEVER A RANGE. One sentence in this batch "
    "straddles a folio: 'There may thus be obtained from an alternating current two or "
    "more direct currents without the employment of any commutator' (printed p. 409) "
    "ends 'such as it has been heretofore regarded as necessary to use' on printed p. "
    "410. Both halves are pinned separately, so each must be cited to its own page. "
    "'(1894, pp. 409-410)' never satisfies check_quotes.py: its citation regex is "
    "'\\(1894, p{1,2}s?\\. ([\\d,\\s]+?)\\)' and cannot read a hyphen. The same rule "
    "applies to the p. 418/p. 419 condenser split (rejected #4): the engravings are on "
    "p. 418, the sentence describing them is on p. 419.",
    "OCR SPACING AND GLUED WORDS, NOT WORDING. Three pinned quotes verify only through "
    "check_quotes.py's space-ignoring index because the OCR or the compositor glued "
    "them: 'the electrical resistance of the conductor IS VARIED' (p. 420, 'isvaried'), "
    "'affected BY CHANGES in temperature' (p. 423, 'bychanges'), 'the current density "
    "through SUCH SOLUTION' (p. 420). Print the clean spaced form; the tool passes it "
    "and flags it as a whitespace-only difference, which is not a licence to change any "
    "word. Two pinned quotes keep the print's spaced semicolon ('insulation ; but Mr. "
    "Tesla believes', p. 419) so they verify as exact matches. No [sic], no bracketed "
    "correction, and no repair of the print's doubled 'it it' (rejected #5) or its "
    "dropped 'be' (rejected #12) inside quotation marks.",
    "STRAY HYPHENS ARE THE MAIN OCR TRAP IN PART III. Two otherwise quotable "
    "sentences are killed by stray hyphens the scan inserts mid-sentence: 'should -be "
    "changed' (p. 423) and 'for a -given time' (p. 421). Both are recorded as "
    "rejected with the alternative pin. Expect more in entries 4-9: this part of the "
    "scan is the worst in the volume for mid-word hyphenation and for running-head "
    "interleaving, and grep_quote.py's furniture stripper does not remove every "
    "running head here (printed p. 413's folio OCRs as '418', and p. 415's as '4ir>'). "
    "Never trust a printed folio read out of the OCR: printed page = scan file - 18 "
    "(§0), and that is the only page number to cite.",
    "VOICE RULE (§0 non-negotiable 5, enforced by qa_page.py). No em or en dashes, no "
    "curly quotes, no Unicode ellipsis in the article body, figure alt text or "
    "captions. The print sets 'direct current - that is', 'self -exciting', 'devices - "
    "such as arc lamps - by direct currents' with em dashes; the pinned ASCII ' - ' "
    "forms verify exactly because grep_quote.py folds a typed ' - ' to the same "
    "normalised text as the print's em dash, so use those and never print the em dash. "
    "Every cut in this pin is ASCII ' ... '. Date and page ranges are written out.",
    "MODERN CLAIMS NEED MODERN SOURCES, AND NONE IS CARRIED IN THIS BATCH. The "
    "solid-state comparison (entry 1), the modern capacitor (entry 2), and any "
    "sentence about where oil dielectrics or electrolytic metering went are all "
    "outside this volume (rejected #7, #10, #11). feature-006/t1 must fetch and read "
    "each source it uses, keep those sentences visibly separate from the 1894 "
    "material, give them no quotation marks and no page cite, and list them in the "
    "Sources block separately from the book - the way article 06's draft handled its "
    "three modern sources. If a source is not fetched, the sentence is cut.",
    "SAFETY (§4.1). Nothing in these three chapters is safe to imply the reader should "
    "try at home: ch. XXXIV is high-potential apparatus in a sealed can of hot oil, and "
    "ch. XXXV passes the whole lighting current through two conductors in an open "
    "solution. The in-book basis for the caution is the chapter's own framing ('currents "
    "of high frequency and high potential', p. 418; 'the whole of the current to be "
    "measured may be passed through the instrument', p. 423). Use it for 'do not try "
    "this', never for a health or materials claim.",
    "WORD COUNTS RE-RUN AT PIN TIME (2026-10-12, whole-word matching over the "
    "normalised text layer of our scan, whole volume, with grep_quote.py --count): "
     "'rectif' 0, 'diode' 0, 'semiconductor' 0, 'ampere-hour' 0, 'solid-state' 0. "
    "'lamp hour' 1 (printed p. 422). 'ohm-meter' 1 (printed p. 423; 'ohm meter' 0). "
    "'electrolytic' 8 (printed pp. 236, 314, 371, 420, 423, 494). 'bubble' 9 (printed "
    "pp. 130, 173, 222, 223, 251). 'condenser' 218. 'specific inductive capacity' 18 "
    "(printed pp. 122, 126, 130, 151, 152, 160, 161, 401, 404, 405, 406, 418). 'molecular bombardment' 15, of which printed p. 418 is one. "
    "'commutator' 92. 'synchronism' 35, of which this chapter's three are pp. 412, "
    "413, 416. 'magnetic gener' 4, all pyro- (pp. 6, 429, 496). 'valve' 4 (pp. 431, "
    "447), 'oscillation valve' 6 (pp. 129, 191, 217, 316, 492). These are the counts "
    "the draft may print; re-run them at draft time (feature-006/t1) rather than "
    "copying, exactly as article 06's draft did.",
]

# Notes for the figure task (feature-006/t2, a08-figrec). Read the existing figure
# record before re-opening any figure (§ the t0 lesson from feature-005).
FIGURE_NOTES = [
    "WHAT ALREADY EXISTS FOR ENTRIES 1-3. website/assets/tesla1894/ already carries "
    "crops for ch. XXXIII and ch. XXXV, and manifest_qc.csv marks every one keep, "
    "quality A: p428-fig1-fig220.webp (printed p. 410), p429-fig1-fig221.webp (p. "
    "411), p430-fig1-fig222.webp (p. 412), p431-fig1-fig223.webp (p. 413), "
    "p432-fig1-fig225.webp (p. 414), p433-fig1-fig225.webp (p. 415), p434-fig1.webp "
    "(p. 416, no OCR caption, cite by page), p439-fig1-fig229.webp (p. 421), "
    "p440-fig1-fig230.webp (p. 422). File names are SCAN files; printed page = scan - "
    "18 (§0). §9 brief 08's figure table names printed pages, so its 'p440-fig230 "
    "p.422' is this p440-fig1-fig230.webp. Do not re-render what is already on disk "
    "and already QCd.",
    "ENTRY 2 HAS NO FIGURE, AND IT IS THE ONE THE ENTRY NEEDS. Ch. XXXIV's engravings "
    "are Figs. 227 and 228, printed on p. 418 (scan file 436): the p. 418 text carries "
    "the captions 'FIG. 227.' and 'FIG. 228.' between the columns, and the p. 419 "
    "prose says what they show ('Fig. 227 is a section of a condenser ... having "
    "stationary plates; and Fig. 228 is a similar view of a condenser with adjustable "
    "plates'). There is NO p436-* crop in website/assets/tesla1894/ and no manifest or "
    "manifest_qc row for scan file 436: the extractor cut nothing from that page. "
    "feature-006/t2 must crop Figs. 227 and 228 from books/pdf-pages-tesla-1894/"
    "page-436.pdf (that file exists), view the crop against the page, and add the "
    "manifest rows. Caption from the p. 419 prose, never from the caption guess.",
    "THE QC SUBJECT LINES FOR THE METER FIGURES ARE WRONG, AND FOR ENTRY 1'S FIRST "
    "FIGURE TOO. manifest_qc.csv describes p439-fig1-fig229.webp as 'A long "
    "spiral-wound tube with tapped terminals down one side and a galvanometer ... good "
    "coherer/retcoherer illustration' and p440-fig1-fig230.webp as 'A long tube with "
    "two coil ends and a row of tapped contacts'. Neither is a coherer: the p. 421 "
    "prose names Figs. 229 and 230 as the two forms of the ELECTROLYTIC METER ('A is a "
    "tube of glass, the ends of which are scaled, as by means of insulating plugs or "
    "caps B B. c c' are two conductors extending through the tube A ... These "
    "conductors may be corrugated or formed in other proper ways to offer the desired "
    "electrical resistance'). Likewise p428-fig1-fig220.webp is QCd as 'two lamps in "
    "opposite arms of a loop with a battery and switches', while the p. 410 prose calls "
    "it 'a plan of directing the alternating currents by means of devices purely "
    "electrical in character' with a generator in each branch. The standing rule applies "
    "(§8 step 3, §0): figure numbers are read off the printed page and captions come "
    "from the prose, never from the extractor filename or the QC note. Verify each crop "
    "against books/pdf-pages-tesla-1894/page-NNN.pdf before use.",
    "FIGURE CHOICE FOR THE THREE ENTRIES. §9 brief 08 asks for one engraving per "
    "entry, and §6.6 puts figure 1 inside the first three H2s. Entry 1: Fig. 220 "
    "(p428-fig1-fig220.webp, printed p. 410) is the one the p. 410 prose introduces, "
    "and it is the simplest of the six; Fig. 223 (p431, p. 413) is the one the "
    "synchronism quote points at, if the entry prefers the machine. Entry 2: Figs. "
    "227/228 (new crop from page-436.pdf) - the cutaway of plates in oil is the whole "
    "point of the entry. Entry 3: Fig. 229 (p439-fig1-fig229.webp, printed p. 421) or "
    "Fig. 230 (p440-fig1-fig230.webp, p. 422); Fig. 230 is the wider image and the "
    "manifest calls it 'Clean, wide', Fig. 229 is the one the prose walks through first. "
    "Check index.json before committing: §6.6 forbids reusing the same engraving on two "
    "articles with the same caption, and no figure in this batch is used by any "
    "rendered article today (index.json rows are hub, 01-07, 09, 11).",
    "IF A PATENT DRAWING IS USED FOR ANY OF THE THREE, CONFIRM THE NUMBER FIRST. "
    "Neither ch. XXXIII, XXXIV nor XXXV prints a patent number for its device anywhere "
    "in the text (checked across printed pp. 409-423). So a patent number must not be "
    "recalled from memory: §6.3 requires confirming it on patents.google.com and §4.2 "
    "requires the credit line 'US patent NNN,NNN (year), Nikola Tesla.' The 1894 "
    "chapters give no basis for a number, so treat any patent plate as optional and "
    "verify it independently, and remember §6.6's limit of one patent plate per two "
    "1894 engravings.",
]

# Links (§5.2 row 08, §9 brief 08's closing beat) for feature-006/t1 and a08-wirecommit.
LINK_NOTES = [
    "OUT-LINKS REQUIRED BY §5.2 ROW 08: magnet-motor.html, perpetual-motion-generator."
    "html, and article 10 (tesla-free-energy-what-he-said.html). §9 brief 08's closing "
    "beat names the same two money pages plus 10, and the bridge is the pyromagnetic "
    "generator (printed pp. 424-431, batch 2): the only 'magnetic generator' in the "
    "1894 volume is a heat-driven one, which is the sharpest sentence this article can "
    "write about this site's own product vocabulary. Check both files exist in website/ "
    "at draft time before linking them.",
    "ARTICLE 10 DOES NOT EXIST YET. index.json rows are hub, 01-07, 09, 11: 08 comes "
    "before 10 in the §sprint order (07, 01, 02, 04, 05, 06, 08, 10, 12), so at "
    "feature-006/t1 time tesla-free-energy-what-he-said.html is not rendered and cannot "
    "be linked. Record the deferred link in index.json the way article 06's pin records "
    "its deferred link to 12, and add it when 10 is written. Do not pad entry 08 with "
    "off-map links to make the number.",
    "IN-LINKS REQUIRED BY §5.2 ROW 08: from 03 (tesla-earthquake-machine.html), from 10 "
    "and from the hub. 03 is rendered, but it was written before 08 existed and cannot "
    "link to a page that was not there; 10 and the hub are unwritten (feature-010, "
    "feature-012). The qa_page.py reciprocal gate ('>= 4 internal links, >= 3 of them "
    "to pages that link back') therefore cannot pass on 08 for any reason to do with "
    "08: nothing on the site links to it yet. Record that in index.json the way article "
    "11's entry records its backlink pass, and do not treat it as an article 08 defect.",
    "THE BRIDGE SENTENCES MUST DESCRIBE WHAT THE TARGET PAGES ACTUALLY SAY (the "
    "feature-005/t1 lesson). Open magnet-motor.html and perpetual-motion-generator.html "
    "at draft time and describe them as this site's take on what you can actually "
    "build, without repeating any product claim (§4.1). Article 08 is the one article in "
    "the series whose subject is devices that did not work, so it is the page most "
    "likely to drift into a claim about what a generator can do; every such sentence "
    "either cites the 1894 page or is cut.",
    "THE HUB CARD FOR 08 IS FEATURE-012'S JOB, AND THIS PIN IS THE RECORD OF WHAT IT "
    "MUST NOT SAY. §9 brief 08's title is '9 Tesla Inventions From 1894 That Never "
    "Caught On'. The volume never says any of these nine never caught on, and entry 2 "
    "did catch on (rejected #11). The hub card and the article's own standfirst should "
    "say what is supportable: these are nine devices the 1894 volume describes, in the "
    "editor's own inventory at printed p. 6, with the book's own verdict where the book "
    "gives one (printed p. 423 for electrolytic meters).",
]


def raw_window(body: str, frag: str, span: int = 220) -> str:
    """Show the scan's own text around a fragment.

    Same trick as the article 02/04/05/06 generators: the anchor is the longest
    literal run of the fragment that the raw page really contains, so the printed
    fragment always sits inside the window.
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
        "# Article 08 quote pin: tesla-weird-inventions-1894.html",
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
        f"**{BATCH}.** §9 brief 08 has nine entries; feature-006 pins them in three "
        "batches (t0 = entries 1-3, a08-qp2 = 4-6, a08-qp3 = 7-9, a08-qpdone = all "
        "nine re-checked together). Append to the lists in `gen_quotes.py` and re-run; "
        "this file is generated, so nothing here is hand-maintained and the counts "
        "below describe the pin as it stands.",
        "",
        "Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola "
        "Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. "
        "Everything in this batch is from Part III, 'MISCELLANEOUS INVENTIONS AND "
        "WRITINGS', and none of it is Tesla's own writing: these chapters describe his "
        "devices about him in the third person. Three chapters, and the one "
        "biographical chapter they are introduced by:",
        "",
        "- chapter I, the editor's biography of Tesla, printed pp. 3-10. Two quotes, "
        "both printed p. 6: the editor's own inventory of the 'Miscellaneous' section, "
        "which is §9 brief 08's list, and the editor's date fence on the volume.",
        "- chapter XXXIII, 'METHOD OF OBTAINING DIRECT FROM ALTERNATING CURRENTS', "
        "printed pp. 409-417 (scan files 427-435). Entry 1. The book's text, third "
        "person: 'Mr. Tesla divides such circuit'.",
        "- chapter XXXIV, 'CONDENSERS WITH PLATES IN OIL', printed pp. 418-419 (scan "
        "files 436-437). Entry 2. Includes an editor's footnote on printed p. 418, "
        "quoted as the editor's.",
        "- chapter XXXV, 'ELECTROLYTIC REGISTERING METER', printed pp. 420-423 (scan "
        "files 438-441). Entry 3, including the editor's verdict on electrolytic "
        "meters, printed p. 423.",
        "",
        f"Verified: {len(rows)} quotes ({sum(len(r[4]) for r in rows)} fragments) "
        f"across {len(by_page)} printed pages, 0 failures. To re-check one quote: "
        "`python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>`. To "
        "regenerate this file: "
        "`python3 new_content/1894-series/08-tesla-weird-inventions-1894/gen_quotes.py` "
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
    out += ["", "## Flags for the writer (§3 quote policy, feature-006/t1)", ""]
    out += [f"- {f}" for f in FLAGS]
    out += ["", "## Notes for the figure task (feature-006/t2, a08-figrec)", ""]
    out += [f"- {f}" for f in FIGURE_NOTES]
    out += ["", "## Links (§5.2 row 08, for feature-006/t1 and a08-wirecommit)", ""]
    out += [f"- {f}" for f in LINK_NOTES]
    out += [""]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out))
    print(f"wrote {OUT} ({len(rows)} quotes, "
          f"{sum(len(r[4]) for r in rows)} fragments, "
          f"{len(by_page)} printed pages, {len(REJECTED)} rejected)")


if __name__ == "__main__":
    sys.exit(main())
