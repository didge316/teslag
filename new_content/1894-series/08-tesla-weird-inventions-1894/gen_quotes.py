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
BATCH2_DATE = "2026-10-16"
BATCH = ("batches 1-2 of 3 are in: §9 brief 08 entries 1-6, the six Part III "
         "chapters at printed pp. 409-447, plus one quote from the author's own "
         "chapter at printed p. 390 (batch 1 = entries 1-3, batch 2 = entries 4-6)")

# This pin was sent back as SUSPECT, not as wrong: feature-005/a06-wipcommit burned
# its whole retry budget, and everything downstream of it went to rework with it
# (harness/rework.json, maxImpactDepth 3). The re-proof is to re-run the pin, not to
# rewrite it, and to say so here so the next session does not re-derive it a third
# time. Re-grepping is cheap; re-arguing it is not.
REVERIFIED = (
    "RE-PROVED ON 2026-10-16 (feature-006/t0 rework pass). This batch went to "
    "rework because feature-005/a06-wipcommit exhausted its retry budget and "
    "everything downstream of it was marked suspect, not because any quote in it "
    "failed. It was re-run, not rewritten. `python3 new_content/1894-series/"
    "08-tesla-weird-inventions-1894/gen_quotes.py` exits 0 and reproduced the pin "
    "byte for byte against the commit that first landed it (347e8b5) - 29 quotes, 29 "
    "fragments, 12 printed pages, 0 failures, 16 rejected. What has been added since "
    "is this re-proof paragraph, the two batch-2 paragraphs, and batch 2's 35 quotes - "
    "all of it added to the generator, never hand-written into the file, and batch 1's "
    "29 quotes are unchanged in every re-run since. Seven of the 29 were then "
    "re-grepped a second time through the independent CLI, one per entry plus the "
    "awkward ones, each returning exactly one hit on its stated printed page: "
    "`grep_quote.py \"includes a great many other inventions in arc lighting, "
    "transformers, pyro-magnetic generators\" --page 6-6`; `\"an active (as "
    "distinguished from a dead) resistance or opposition to the currents of one "
    "sign\" --page 416-416`; `\"The current in either branch may be used in the "
    "same way and for the same purposes as any other direct current - that is\" "
    "--page 410-410` (the ASCII ' - ' form, which folds to the print's em dash); "
    "`\"The space within the can is filled with oil G\" --page 419-419`; `\"it has "
    "been a common practice to interpose a body of oil between two conductors\" "
    "--page 419-419` (the form that starts after the print's doubled 'it'); "
    "`\"the increase of resistance of one conductor or the diminution of the "
    "resistance of the other per lamp hour\" --page 422-422`; `\"Electrolytic "
    "meters seem to need every auxiliary advantage to make them permanently "
    "popular\" --page 423-423`. The OCR artefacts this pin relies on were counted "
    "in the raw text again: 'isvaried' 1, 'bychanges' 1, 'should -be changed' 1, "
    "'for a -given time' 1, 'what may termed' 1, and the doubled 'it' at printed "
    "p. 419, which the OCR splits across a line break ('and it\\nit has been a "
    "common practice'), so it does not appear as 'it it has been' and only the "
    "form pinned above, which starts after it, matches. Every ' ... ' cut, every "
    "rejected item and every page number above still describes the scan as it is.")

# Batch 2 (feature-006/a08-qp2, entries 4-6) is what this paragraph records: it is
# in the generator, not hand-written into quotes.md, so the next batch cannot lose it.
BATCH2 = (
    "BATCH 2 ADDED 2026-10-16 (feature-006/a08-qp2): entries 4-6, the three Part III "
    "chapters at printed pp. 424-447 - 35 quotes, 38 fragments, 17 printed pages - "
    "plus one quote from printed p. 390. Every quote below was re-grepped at "
    "generation time by this script through the same matcher check_quotes.py uses; ten "
    "of them were then re-grepped a second time through the independent CLI, one or two "
    "per entry plus the awkward cases (the p. 428 quote whose folio OCRs as '438', the "
    "two-fragment mercury cut on p. 437, the p. 447 fragments, the p. 390 claim), each "
    "returning exactly one hit on its stated printed page and none of them fuzzy. Four "
    "things this batch found that batch 1 could not have: (1) §9 brief 08's entry-4 "
    "hook is the one hook in the whole brief that greps verbatim - 'oscillating as "
    "rapidly as 400 to 500 times a minute' is 1 hit in the volume, printed p. 424 - "
    "and it is still wrong about the entry, because that sentence is a footnote "
    "describing a horseshoe-magnet demonstration the compiler heard about in an "
    "interview, not the thermo-magnetic motor the chapter is about; (2) the volume "
    "contains a date for entry 6's device - 'devised by him as far back as 1885', "
    "printed p. 438, and '1885' is 1 hit in the whole volume - which is the only dated "
    "invention statement anywhere in these six chapters, while ch. XXXVII gives nothing "
    "but 'some years ago' and 'A few years later'; (3) entry 6 is the one entry of the "
    "nine where Tesla's own words are in this volume: printed p. 390, in ch. XXIX, he "
    "claims the third brush himself, in the third person he uses about himself ('it may "
    "not be thought immodest of the writer'); (4) neither ch. XXXVI nor ch. XXXVIII "
    "reports any result for its machine - 'efficiency' 0 hits on pp. 424-431 and 0 on "
    "pp. 438-447, 'per cent' 0 anywhere in pp. 424-447 - an absence the draft may "
    "state in its own words, recorded in Rejected #21 and #22. Chs. XXXVI-XXXVIII are "
    "still the compiler's prose about him. See the flags.")

# What the first pass of batch 2 got wrong, and what the re-check found. Recorded in
# the generator for the same reason the re-proof paragraph is: a pin that overstates
# what the scan says is the failure this task exists to prevent, and the next batch
# should know which claims were re-checked rather than assumed.
BATCH2_CORRECTED = (
    "BATCH 2 CORRECTED ON 2026-10-16 before it was committed, on four points the first "
    "pass got wrong. (a) 'Curie' was recorded as 0 hits in the volume. It is 0 exact, "
    "and grep_quote.py --count returns 4 - all of them fuzzy matches on the words "
    "'cured' and 'curved' at printed pp. 69 and 453. The claim was right in substance "
    "and wrong in method, and the method is what the draft will copy, so the flag now "
    "says how to read a count. (b) The p. 429 note said the chapter's own phrase 'a "
    "pyromagnetic generator of electricity' cannot be quoted because the print hangs a "
    "footnote digit on 'electricity'. It can: it verifies exactly on p. 429 through "
    "this script's own matcher, because a trailing '1' does not break a substring "
    "match. Entry 4 may name the device in the book's words. (c) Rejected #16 said the "
    "fifth 'magnetic gener' hit is the ch. XXXVI heading mis-OCRd as 'PYRO-MAGNETIC "
    "RATORS'. The heading on scan file 442 is complete - 'CHAPTEK THERMO-MAGNETIC "
    "XXXVI. MOTORS AND PYRO-MAGNETIC GENERATORS.' - and it is the contents-page line "
    "at scan file 17 that the OCR truncates. The heading is missing from the tool's "
    "default count only because page-opening display type is stripped as furniture: "
    "with --keep-furniture the count is 5 and names printed p. 424, which is what "
    "Appendix D reports. Appendix D was right and the default index was not; the "
    "closing beat still stands, because all five are PYRO-magnetic. (d) Six notes "
    "pointed at Rejected rows and flags that had not been written. They are written "
    "now - Rejected #17-#22 and six batch-2 flags - and the word-counts flag carries "
    "batch 2's counts, re-run on this date, with batch 1's counts re-run alongside them "
    "to confirm the method still reproduces them. No candidate list was kept as a "
    "scratch file: what was considered and not carried is in Rejected, which is where "
    "the next batch should look.")

# Chapters this pin draws on, in the order the volume prints them. Batch 3 appends
# its own rows here rather than editing the header prose.
CHAPTERS = [
    "chapter I, the editor's biography of Tesla, printed pp. 3-10. Two quotes, "
    "both printed p. 6: the editor's own inventory of the 'Miscellaneous' section, "
    "which is §9 brief 08's list, and the editor's date fence on the volume.",
    "chapter XXXIII, 'METHOD OF OBTAINING DIRECT FROM ALTERNATING CURRENTS', "
    "printed pp. 409-417 (scan files 427-435). Entry 1. The book's text, third "
    "person: 'Mr. Tesla divides such circuit'.",
    "chapter XXXIV, 'CONDENSERS WITH PLATES IN OIL', printed pp. 418-419 (scan "
    "files 436-437). Entry 2. Includes an editor's footnote on printed p. 418, "
    "quoted as the editor's.",
    "chapter XXXV, 'ELECTROLYTIC REGISTERING METER', printed pp. 420-423 (scan "
    "files 438-441). Entry 3, including the editor's verdict on electrolytic "
    "meters, printed p. 423.",
    "chapter XXXVI, 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS', "
    "printed pp. 424-431 (scan files 442-449). Entry 4, and the closing beat of "
    "the article: the only '...magnetic generator' in the volume is the PYRO-"
    "magnetic one, a heat engine. Includes two compiler's footnotes, printed "
    "p. 424 (the L-shaped iron strip and the 400-500 vibrations a minute, learned "
    "'in an interview with Mr. Tesla') and printed p. 429 (the steam-cooling "
    "attempt). The chapter's own title is set out in full at the head of the chapter; "
    "it is the contents-page line that the OCR truncates to 'PYRO-MAGNETIC RATORS'; "
    "see the heading flag and Rejected #16.",
    "chapter XXXVII, 'ANTI-SPARKING BRUSH AND COMMUTATOR', printed pp. 432-437 "
    "(scan files 450-455). Entry 5. Two devices in one chapter, an early one and a "
    "later one, dated only as 'some years ago' and 'A few years later'.",
    "chapter XXXVIII, 'AUXILIARY BRUSH REGULATION OF DIRECT CURRENT DYNAMOS', "
    "printed pp. 438-447 (scan files 456-465). Entry 6, including the compiler's "
    "footnote on printed p. 438 and the one dated invention statement in the "
    "volume ('devised by him as far back as 1885').",
    "chapter XXIX, the author's own account of high-frequency alternating-current "
    "generators, printed pp. 374-391 (scan files 392-409). NOT Part III: this is "
    "the author writing about himself in the third person ('the writer', 'it may "
    "not be thought immodest of the writer'). One quote, printed p. 390: his own "
    "claim of the third brush, which is entry 6's priority claim and the only "
    "first-person material in this pin. Article 11's page is built on this chapter "
    "(feature-007), so the two pages share a source and must not contradict each "
    "other on who is speaking.",
]

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

    # ==================== BATCH 2 (feature-006/a08-qp2): entries 4-6 ====================
    # --- Entry 4. Thermo-magnetic motors / pyromagnetic generator
    #     (ch. XXXVI, printed pp. 424-431)
    ("As far back as the beginning of the seventeenth century it was shown by Dr. "
     "William Gilbert, the father of modern electricity, that a loadstone or iron "
     "bar when heated to redness loses its magnetism ; and since that time the "
     "influence of heat on the magnetic metals has been investigated frequently, "
     "though not with any material or practical result",
     424, "Entry 4. Thermo-magnetic motor and pyromagnetic generator (ch. XXXVI opening)",
     "the chapter's own opening claim, and the honest frame for the entry: heat "
     "destroying magnetism was three centuries old in 1894 and had produced, in the "
     "compiler's words, no material or practical result. That is why the entry is not "
     "a discovery story. Note the spaced ';' is the print's, and 'Gilbert' is 1 hit "
     "in the whole volume, here"),
    ("the problems in this field have naturally had no small fascination, and though "
     "he has but glanced at them, it is to be hoped he may find time to pursue the "
     "study deeper and further",
     424, "Entry 4. Thermo-magnetic motor and pyromagnetic generator",
     "the compiler's own hedge on how far Tesla took this: 'he has but glanced at "
     "them'. The same paragraph says he 'has worked out one or two operative devices "
     "worthy of note' - one or two, not a programme. This is the in-book basis for "
     "saying the thermo-magnetic line was a side excursion, and it needs no invented "
     "judgement about Tesla's priorities (§4.1)"),
    ("the vibration obtained in this manner is very slow owing to the inability of "
     "the iron to follow rapid changes in temperature",
     424, "Entry 4. Thermo-magnetic motor (the compiler's footnote, printed p. 424)",
     "the physical limit, stated by the book itself before the device is described: "
     "thermal inertia. This is entry 4's 'why it lost' and it is quoted from the "
     "footnote, not invented - a machine whose cycle time is set by how fast iron "
     "cools cannot compete with one whose cycle time is set by the supply. It also "
     "contradicts the brief's 400-500-a-minute hook for the chapter's own devices; "
     "see the flag THE 400-500-A-MINUTE NUMBER IS A FOOTNOTE, NOT A SPEC"),
    ("In an interview with Mr. Tesla on this subject, the compiler learned of an "
     "experiment which will interest students",
     424, "Entry 4. The L-shaped strip experiment (compiler's footnote, provenance)",
     "the provenance of the most quotable sentence in this entry: the compiler heard "
     "about it in an interview and reports it second-hand. It is not a test of the "
     "patented device, it is not described as Tesla's apparatus, and the footnote "
     "says so. Attribute it to the compiler's interview, never as 'Tesla reported"),
    ("A simple horseshoe magnet is taken and a piece of sheet iron bent in the form "
     "of an L is brought in contact with one of the poles",
     424, "Entry 4. The L-shaped strip experiment (compiler's footnote)",
     "what the 400-500-a-minute object actually is: a horseshoe magnet and a bent "
     "piece of sheet iron, on a bench. §9 brief 08's hook ('a spirit lamp under an "
     "L-shaped iron strip') is accurate about the apparatus, and this is the sentence "
     "that shows the apparatus is a demonstration, not the chapter's machine. The "
     "rest of the sentence ('placed in such a position that it is kept in the "
     "attraction of the opposite pole delicately suspended') verifies exactly on the "
     "same page if the draft wants the whole setup"),
    ("A spirit lamp is placed under the sheet iron piece and when the iron is heated "
     "to a certain temperature it is easily set in vibration oscillating as rapidly "
     "as 400 to 500 times a minute",
     424, "Entry 4. The L-shaped strip experiment (compiler's footnote, the brief's hook)",
     "the only §9 brief 08 hook in this batch that greps verbatim: '400 to 500' is 1 "
     "hit in the whole volume and it is this footnote. Use it, but use it as what it "
     "is - a bench vibration the compiler was told about, in a footnote whose first "
     "sentence says the chapter's own devices vibrate 'very slow'. The number is not "
     "an output, a speed or a claim about the machine, and the draft must not print "
     "it as one"),
    ("The experiment is very easily performed and is interesting principally on "
     "account of the very rapid rate of vibration",
     424, "Entry 4. The L-shaped strip experiment (compiler's footnote, the verdict)",
     "the compiler's own verdict on the experiment: easy to perform, interesting as a "
     "spectacle. That is the whole of the book's claim for the fastest thing in this "
     "entry, and it is the sharpest available evidence that none of these devices was "
     "offered as a machine that went anywhere"),
    ("the heat is directed against a body that is magnetized by induction, rather "
     "than directly against a permanent magnet, thereby avoiding the loss of "
     "magnetism that might result in the permanent magnet by the action of heat",
     425, "Entry 4. Thermo-magnetic motor (the design refinement)",
     "the engineering thought inside the crude device: heat the induced body, not the "
     "permanent magnet, so the magnet does not lose its field. This is what lifts the "
     "entry above 'a magnet and a flame'. Note 'might result' - the loss being avoided "
     "is a possibility the design guards against, not a measured effect"),
    ("so that the fly-wheel will be revolved as rapidly as the armature can be "
     "heated and cooled to the necessary extent",
     428, "Entry 4. Thermo-magnetic motor (why it lost, the speed limit in the drawing)",
     "the same thermal limit stated in the machine's own drawing (Fig. 240, the "
     "armature linked to a crank on a fly-wheel): the fly-wheel turns only as fast as "
     "the iron heats and cools. PIN THE PAGE CAREFULLY: this is printed p. 428, and "
     "the running folio on that scan page OCRs as '438', which is entry 6's page. "
     "Printed page = scan file - 18 (scan 446), always"),
    ("based upon the following laws : First, that electricity or electrical energy is "
     "developed in any conducting body by subjecting such body to a varying magnetic "
     "influence",
     429, "Entry 4. Pyromagnetic generator (ch. XXXVI second half, the principle)",
     "the pyromagnetic generator's stated basis, and the sentence the article's "
     "closing beat rests on. The chapter's own naming phrase 'a pyromagnetic "
     "generator of electricity' verifies exactly on this page too - the footnote "
     "digit the print hangs on 'electricity' ('electricity1') does not break a "
     "substring match - so entry 4 may name the device in the book's own words; this "
     "quote is the one that carries the principle. The spaced ':' is the print's"),
    ("Then apply to the iron between the coil and the steel bar a flame or other "
     "source of heat which will be capable of raising that portion of the iron to an "
     "orange red, or a temperature of about 600° centigrade",
     429, "Entry 4. Pyromagnetic generator (the number in the book)",
     "the one temperature figure in this entry, and the concrete detail the entry "
     "needs. It is also the accuracy trap: the book's 600° is what it reports for a "
     "thin strip, and the volume never names the effect - 'Curie' has 0 exact hits, "
     "and grep_quote.py --count returns 4 only as fuzzy matches on the words 'cured' "
     "and 'curved' (printed pp. 69, 453). '600' and 'centigrade' are each 1 hit in "
     "the volume, both here. Do not equate 600° with the Curie point, and do not "
     "print the modern figure either, without a modern source (see the flag THE "
     "BOOK'S 600° IS NOT THE CURIE POINT)"),
    ("the features of novelty in the invention being, first, the employment of an "
     "artificial cooling device, and, second, inclosing the source of heat and that "
     "portion of the magnetic circuit exposed to the heat and artificially cooling "
     "the heated part",
     430, "Entry 4. Pyromagnetic generator (what was actually claimed as new)",
     "what the book says is new in the machine - not heat, not magnetism, but a "
     "cooling system. That is the honest way to describe the invention, and it is "
     "also the reason the entry reads as engineering rather than as a curiosity: the "
     "claim is about managing heat"),
    ("the difference between the temperature of the applied heat and of the steam, "
     "air, or whatever gas or fluid be applied as the cooling medium, may be "
     "increased or decreased at will, whereby the rapidity of the magnetic changes "
     "or fluctuations may be regulated",
     431, "Entry 4. Pyromagnetic generator (the chapter's last sentence)",
     "the last sentence of ch. XXXVI. Pin it because what it does NOT do is the "
     "finding: the chapter ends on what could be regulated, with no output, no "
     "efficiency, no run, no trial, no commercial result anywhere in pp. 424-431. "
     "That absence is recorded in Rejected #21 with the counts that establish it; the "
     "draft may state it as an absence, never as a 1894 verdict"),

    # --- Entry 5. Anti-sparking brush and commutator
    #     (ch. XXXVII, printed pp. 432-437)
    ("IN direct current dynamos of great electromotive force - such, for instance, "
     "as those used for arc lighting - when one commutator bar or plate comes out of "
     "contact with the collecting-brush a spark is apt to appear on the commutator",
     432, "Entry 5. Anti-sparking brush and commutator (ch. XXXVII opening)",
     "the problem as the book states it, and it is narrower than §9 brief 08's hook "
     "('the problem every DC motor had'): this is about high-EMF direct-current "
     "DYNAMOS used for arc lighting. The chapter does say motors later, and it says "
     "Tesla worked to dispense with the commutator in 'dynamos and motors', but the "
     "fault described here is a generator fault. Write the entry from the sentence, "
     "not from the hook. The ' - ' forms fold to the print's em dashes"),
    ("This spark may be due to the break of the complete circuit, or to a shunt of "
     "low resistance formed by the brush between two or more commutator-bars",
     432, "Entry 5. Anti-sparking brush and commutator (the two causes)",
     "the mechanism of the fault in one sentence, and the reason the fix is a "
     "commutation problem rather than a brush-material problem: the spark has two "
     "causes and the second one is the brush short-circuiting adjacent bars. Note "
     "'may be due to' - the book does not claim to know which cause is operating"),
    ("but all these devices are expensive or not fully available, and seldom attain "
     "the object desired",
     432, "Entry 5. Anti-sparking brush and commutator (the prior remedies)",
     "the compiler's verdict on every remedy already in use (a path for the current, "
     "short-circuiting the field helices, more commutator bars). It is the only "
     "comparative claim in this chapter and it is asserted, not measured - so the "
     "entry can say the book dismissed the alternatives, and cannot say anything "
     "about which remedy actually won in the market"),
    ("To prevent this sparking in a simple manner, Mr. Tesla some years ago employed "
     "with the commutator-bars and intervening insulating material, mica, asbestos "
     "paper or other insulating and incombustible material, arranged to bear on the "
     "surface of the commutator, near to and behind the brush",
     432, "Entry 5. The first device (undated)",
     "the first of the chapter's two devices: insulating sheets bearing on the "
     "commutator behind the brush. The date is the trap - 'some years ago' is all "
     "the volume gives, and this chapter contains no year at all. 'asbestos' is 4 "
     "hits in the whole volume, all of them on printed pp. 432-433, i.e. only here. "
     "Never give a year for this device without a patent record checked under §6.3"),
    ("the commutator had always been prominent in his thoughts, and that so much of "
     "his work was even aimed at dispensing with it entirely as an objectionable and "
     "unnecessary part of dynamos and motors",
     433, "Entry 5. Anti-sparking brush and commutator (the book's own statement of the aim)",
     "the sentence that connects this entry to entry 1 and to articles 07 and 11: "
     "the compiler says part of Tesla's work aimed at dispensing with the commutator "
     "altogether. It is the compiler's characterisation, in the same paragraph that "
     "dates the second device only as 'A few years later', so quote it as his view. "
     "It is also the best in-book bridge the article has - better than any invented "
     "connection between the nine entries"),
    ("Mr. Tesla constructs a commutator and the collectors therefor in two parts "
     "mutually adapted to one another, and, so far as the essential features are "
     "concerned, alike in mechanical structure",
     433, "Entry 5. The disc commutator (the design idea)",
     "the second device in one sentence: the collector is built like the commutator, "
     "so the two faces match. That symmetry is what the timing argument in the next "
     "quote depends on, so the entry needs it before it can explain the claim"),
    ("the short-circuiting and the breaking of the armature coil connected to the "
     "commutator-segments occur at the same instant, and from the nature of the "
     "construction this will be done with the greatest precision",
     434, "Entry 5. The disc commutator (the timing argument)",
     "why the matched faces were supposed to kill the spark: the two events that "
     "cause it are made simultaneous, so their effects cancel. 'from the nature of "
     "the construction' and 'with the greatest precision' are the book's grounds - "
     "an argument from the design, not a measurement"),
    ("The first results in a reduction which amounts practically to a suppression of "
     "the spark, since the break and the short circuit produce opposite effects in "
     "the armature-coil",
     434, "Entry 5. The disc commutator (the claim, and its hedge)",
     "the strongest claim in the chapter, and note the hedge inside it: 'a reduction "
     "which amounts practically to a suppression'. The book never says the spark is "
     "gone, and no test, current, or run is reported anywhere in pp. 432-437. This "
     "is the sentence to quote if the draft wants to show how these claims are "
     "worded"),
    ("while lessening the duration of the short circuit obviously increases the "
     "efficiency of the machine",
     434, "Entry 5. The disc commutator (an efficiency claim with no figure)",
     "'obviously increases the efficiency' - an efficiency claim with no number "
     "attached, and the only efficiency statement in this chapter. Pair it with the "
     "p. 434 suppression quote: that is what an 1894 claim of improvement looks "
     "like, and it is why the article's 'never caught on' framing cannot be charged "
     "to the book"),
    ("Such materials as glass, marble, or soapstone may be advantageously used",
     436, "Entry 5. The disc commutator (the materials)",
     "the concrete oddity the listicle needs, in six words: the insulating segments "
     "of this commutator are glass, marble or soapstone, polished, with sharp edges. "
     "The same paragraph faces the metal segments with 'a facing or edge of durable "
     "material - such as platinum or the like - where the sparks are liable to occur' "
     "(printed p. 436, verifies, not carried); the further sentence 'It is considered "
     "best to coat them with platinum or silver' is on printed p. 437, in the mercury "
     "variant's paragraph, and is kept in Rejected #17 as a second materials quote in "
     "one entry"),
    ("instead of solid segments, a fluid is employed ... These chambers or recesses "
     "are filled with mercury",
     437, "Entry 5. The mercury variant (printed p. 437)",
     "the last form in the chapter, and the weirdest: a commutator whose segments "
     "are recesses of liquid mercury. Two fragments, both exact on printed p. 437, "
     "cut where the intervening sentences describe the discs. 'mercury' is 26 hits "
     "in the volume but only here is it a commutator. The design tension is in the "
     "same paragraph - pistons that compensate for the mercury's expansion and "
     "contraction with temperature and must still 'not yield to the pressure of the "
     "fluid due to centrifugal action'; that sentence verifies exactly and is kept in "
     "Rejected #18, because a third construction quote in one entry is padding"),

    # --- Entry 6. Auxiliary-brush (third-brush) regulation of DC dynamos
    #     (ch. XXXVIII, printed pp. 438-447; plus the author's own claim at p. 390)
    ("In machines of this type, devised by him as far back as 1885, he makes use of "
     "two main brushes to which the ends of the field magnet coils are connected, an "
     "auxiliary brush, and a branch or shunt connection from an intermediate point",
     438, "Entry 6. Third-brush regulation (ch. XXXVIII opening, the dated claim)",
     "the only dated invention statement in these six chapters, and '1885' is 1 hit "
     "in the whole volume. It gives entry 6 something none of the other eight entries "
     "has: a date inside the book, for a device the book says was already in use by "
     "then. End the quote at 'point': the next words are 'of the field wire to the "
     "auxiliary brush', and the OCR reads 'iield', which no normaliser fixes (see "
     "Rejected #20). The chapter's own naming sentence ('that which has come to be known "
     "as the \"third brush\" method') cannot be quoted cleanly - the print sets the "
     "term in quotation marks, which splits the run in check_quotes.py's scanner, and "
     "the OCR reads 'has' as 'lias'. Name the method from the p. 6 inventory already "
     "pinned in batch 1, or from the contents page"),
    ("the electric condition is disturbed and more or less of the current through the "
     "field-helices is diverted through the shunt or a current is passed over the "
     "shunt to the field-helices",
     438, "Entry 6. Third-brush regulation (the mechanism)",
     "what the third brush actually does: move it, and part of the field current is "
     "diverted the other way. 'more or less' is the book's own precision. This is the "
     "sentence the entry's plain-English explanation has to be built on, because it is "
     "the only one in the chapter that states the action without a diagram"),
    ("The compiler has learned partially from statements made on several occasions in "
     "journals and partially by personal inquiry of Mr. Tesla, that a great deal of "
     "work in this interesting line is unpublished",
     438, "Entry 6. Third-brush regulation (the compiler's footnote, provenance)",
     "the compiler saying out loud how he knows this chapter's material: journal "
     "statements plus asking Tesla. That is the provenance of entry 6 in one sentence, "
     "and it is why the chapter's account of what Tesla did is not evidence of what "
     "Tesla did. It also supports the article's claim that the 1894 book is a "
     "compilation, not a record"),
    ("This auxiliary brush invention, it will be remembered, was very much discussed "
     "a few years ago, and it may be of interest that this work of Mr. Tesla, then "
     "unknown in this field, is now brought to light",
     438, "Entry 6. Third-brush regulation (the compiler's footnote, the priority frame)",
     "the compiler's claim that the method had been 'very much discussed' and that "
     "Tesla's work was 'then unknown in this field' - a priority claim made in "
     "passing, with no dates and no references. The sentence is cut at the foot of the "
     "page: 'brought to light' is 1 hit in the volume and the scan's next words resume "
     "the chapter's own text, so the footnote ends here as printed. Quote it as an "
     "argument, not as a fact about priority; the p. 390 quote below is the claim"),
    ("it may not be thought immodest of the writer to mention that, as far as records "
     "go, he seems to have been the first who has successfully regulated machines by "
     "providing a bridge connection between a point of the external circuit and the "
     "commutator by means of a third brush",
     390, "Entry 6. Third-brush regulation (the author's own claim, ch. XXIX)",
     "the only place in this volume where the author claims one of these nine devices "
     "for Tesla in his own words - and note where it is: NOT ch. XXXVIII but ch. "
     "XXIX, printed p. 390, in the author's own writing about himself in the third "
     "person ('the writer', 'it may not be thought immodest'). Every hedge is in the "
     "sentence and must be kept: 'as far as records go', 'he seems to have been'. "
     "'third brush' is 2 hits in the volume, here and at printed p. 438. This is the "
     "quote that lets entry 6 say what the other eight cannot: that Tesla himself "
     "claimed it, in these words, with these qualifications"),
    ("the potentials of the points x and Y will be equal, and no current will flow "
     "over the auxiliary brush",
     439, "Entry 6. Third-brush regulation (the balance condition)",
     "the counter-intuitive core of the design: at the right brush position nothing at "
     "all flows through the third brush. The capitals 'x and Y' are the print's "
     "(the same nodes are lower-case 'x' and 'y' on printed p. 443, where the "
     "sentence verifies in that form too - cite p. 439 for the form pinned here)"),
    ("In all cases the adjustment should be such that no current flows over the "
     "auxiliary brush when the dynamo is running with its normal load",
     441, "Entry 6. Third-brush regulation (the design goal, stated plainly)",
     "the same idea as the p. 439 quote but stated as a design rule, and the best "
     "single sentence for the entry: the regulating brush is meant to carry no "
     "current at all in normal operation. It is also the answer to 'why did this "
     "need a moving brush' - the brush sets a balance rather than carrying load"),
    ("It is true that auxiliary brushes have been used in connection with the "
     "helices of the field-wire ... these brushes could not be taken off without "
     "breaking the circuit through the field",
     441, "Entry 6. Third-brush regulation (the book's own prior art)",
     "the book admitting that auxiliary brushes already existed, and saying what "
     "Tesla's version improves: the older brushes carried the whole field current and "
     "could not be lifted without breaking the field circuit. Two fragments, both "
     "exact on printed p. 441, cut where the Fig. 255 engraving sits between them in "
     "the column. This is the strongest 'the idea was in the air' evidence in this "
     "batch, and it is the book's, not ours"),
    ("In practice it is sufficient to move only the auxiliary brush, as shown in Fig. "
     "264, as the regulation is very sensitive to the slightest changes",
     443, "Entry 6. Third-brush regulation (in practice)",
     "the closest the chapter comes to reporting practice: 'in practice it is "
     "sufficient to move only the auxiliary brush'. It is a statement about what the "
     "design needs, not a record of a machine in service - the chapter reports no "
     "installation, no load test and no result. Keep 'in practice' in the quote and "
     "keep that distinction in the prose"),
    ("a great number of lights may be put on without diminishing the ... power of "
     "the lamps in the circuit, as the brushes assume at once the proper position",
     447, "Entry 6. Third-brush regulation (the payoff claim, printed p. 447)",
     "what the regulator was for, in the book's words: putting lamps on a circuit "
     "without dimming the others. The ' ... ' cut is where the print hyphenates "
     "'light- power' with a space after the hyphen, so the clean single-run form "
     "cannot be quoted (see Rejected #19); both fragments verify exactly on printed "
     "p. 447. This is "
     "the concrete benefit the entry can name, and it is a claim, not a measurement"),
    ("lights or other devices may be put on or out with scarcely any perceptible "
     "difference",
     447, "Entry 6. Third-brush regulation (the chapter's last claim)",
     "the last substantive claim of ch. XXXVIII, and the hedge in it ('scarcely any "
     "perceptible') is the honest ending: like ch. XXXVI, this chapter closes on what "
     "the device is said to do, with no trial, no figure and no commercial result "
     "anywhere in printed pp. 438-447. Record that as an absence (see Rejected #22), "
     "never as an 1894 verdict"),
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
     "4 hits for 'magnetic gener' in the whole volume through grep_quote.py's default "
     "index: printed p. 6 (the editor's list, 'pyro-magnetic generators'), p. 429 "
     "('pyromagnetic generator of electricity'), p. 496 (the index, 'Pyromagnetic "
     "Generators 429'). Every one is PYRO-magnetic, which is what §9 brief 08's "
     "closing beat claims and it holds. Appendix D says 5 hits and lists p. 424, and "
     "Appendix D is right: the fifth is the ch. XXXVI chapter heading, which this scan "
     "reads in full - 'CHAPTEK THERMO-MAGNETIC XXXVI. MOTORS AND PYRO-MAGNETIC "
     "GENERATORS.' at the head of scan file 442 - but the tool strips page-opening "
     "display type as furniture, so it is missing from the default count and present "
     "with --keep-furniture, which returns 5 hits and names p. 424. What IS truncated "
     "is the contents-page entry, scan file 17: 'THERMO-MAGNETIC MOTORS AND "
     "PYRO-MAGNETIC RATORS', where the OCR drops 'GENE'; the contents pages carry no "
     "printed folio, so that line cannot be cited at all. State the closing beat from "
     "the prose at pp. 429 and 496; the heading may be described as a heading but is "
     "display type, not a sentence to quote. Batch 2 owns entry 4 (printed pp. 424-431)"),
    ("It is considered best to coat them with platinum or silver", 437,
     "verifies exactly on printed p. 437, in the paragraph describing the metal plates "
     "of the mercury variant, and it is the companion of the p. 436 sentence about "
     "facing the metal segments 'with platinum or the like - where the sparks are "
     "liable to occur' (which also verifies). Neither is carried: entry 5 already has "
     "its materials quote on p. 436, and a second materials quote in one entry is "
     "padding (§3 'Do not pad'). Both are here if the draft wants the platinum detail"),
    ("which compensate for the expansion and contraction of the mercury under varying "
     "temperatures, but which are sufficiently strong not to yield to the pressure of "
     "the fluid due to centrifugal action", 437,
     "verifies exactly on printed p. 437. Not carried: it is the third construction "
     "quote in one entry (§3 'Do not pad'), and the pinned two-fragment mercury quote "
     "already carries the oddity. Kept because the design tension it states - a liquid "
     "commutator that must compensate for thermal expansion while resisting "
     "centrifugal pressure - is the best available evidence that this form was a "
     "drawing, not a machine anyone ran"),
    ("a great number of lights may be put on without diminishing the light-power of "
     "the lamps in the circuit, as the brushes assume at once the proper position", 447,
     "the single-run form is a FAIL as the word is actually set. The scan reads 'the "
     "light- power' with a space after the hyphen, and grep_quote.py's normaliser "
     "folds a hyphen only when whitespace follows it, so a typed 'light-power' stays "
     "'light-power' and matches only fuzzily (ratio 0.99 over the first half, a FAIL). "
     "Typing the scan's own 'light- power' verifies exactly, but that is not the "
     "printed word, so the ' ... ' cut stands and both fragments are cited to p. 447"),
    ("an auxiliary brush, and a branch or shunt connection from an intermediate point "
     "of the field wire to the auxiliary brush", 438,
     "the scan reads 'the iield wire', and no normaliser turns 'iield' into 'field', "
     "so the full sentence matches only fuzzily (ratio 0.983, a FAIL). The pinned "
     "quote ends at 'an intermediate point'; the rest of the sentence is our own "
     "words, unquoted"),
    ("any output, efficiency, trial or commercial result for the thermo-magnetic motor "
     "or the pyromagnetic generator", 0,
     "no such sentence anywhere in printed pp. 424-431, and the counts say so: "
     "'efficiency' 0 hits on 424-431 (33 in the volume, none in this chapter), 'per "
     "cent' 0 hits on 424-447 (5 in the volume, at pp. 8 and 452). The chapter's own "
     "hedges are pinned instead. This is an absence, not a quote: the draft states it "
     "in our own words as an absence and never as an 1894 verdict (§4.1)"),
    ("any installation, load test or commercial result for the third-brush regulator", 0,
     "no such sentence anywhere in printed pp. 438-447 either: 'efficiency' 0 hits "
     "there too. What the chapter does say is pinned, including 'In practice it is "
     "sufficient to move only the auxiliary brush' (p. 443), which is a statement "
     "about what the design needs, not a record of a machine in service. Same rule as "
     "the row above; both are ch. XXXVI and ch. XXXVIII's shared silence, and §9 brief "
     "08's 'why it lost' beat is built from it"),
]

# Notes the writer needs before drafting (feature-006/t1..t3). §3 quote policy.
FLAGS = [
    "PART III IS THE EDITOR'S TEXT, IN THE THIRD PERSON, ABOUT TESLA'S DEVICES. All "
    "six chapters pinned so far sit in Part III, 'MISCELLANEOUS INVENTIONS AND "
    "WRITINGS' (contents, scan file 16): ch. XXXIII 'METHOD OF OBTAINING DIRECT FROM "
    "ALTERNATING CURRENTS' (printed pp. 409-417), ch. XXXIV 'CONDENSERS WITH PLATES "
    "IN OIL' (printed pp. 418-419), ch. XXXV 'ELECTROLYTIC REGISTERING METER' "
    "(printed pp. 420-423), ch. XXXVI 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC "
    "GENERATORS' (printed pp. 424-431), ch. XXXVII 'ANTI-SPARKING BRUSH AND "
    "COMMUTATOR' (printed pp. 432-437) and ch. XXXVIII 'AUXILIARY BRUSH REGULATION OF "
    "DIRECT CURRENT DYNAMOS' (printed pp. 438-447). None is a Tesla paper or lecture. "
    "The prose says 'Mr. Tesla divides such circuit', 'In carrying out this idea Mr. "
    "Tesla employs', 'an ingenious form of electrolytic meter attributable to Mr. "
    "Tesla', 'Mr. Tesla some years ago employed', 'Mr. Tesla constructs a commutator', "
    "'In machines of this type, devised by him as far back as 1885, he makes use of'. "
    "Never 'Tesla wrote in 1894', never put this prose in his mouth, and attribute it "
    "as the book's account of his devices. This is the same trap the article 06 pin "
    "flags for ch. XXIX, and it is the biggest accuracy risk in article 08: a listicle "
    "about 'Tesla's weird inventions' naturally writes about him in the third person "
    "too, "
    "and the two third-persons blur into one. The fix is to name the chapter and the "
    "page every time, and to say once, early, that Part III is the editor's writing.",
    "THE NINE ENTRIES ARE THE BOOK'S, NOT OURS. The editor's inventory at printed p. "
    "6 maps onto §9 brief 08's table almost item for item (see the pinned quote). Say "
    "so in the intro: the list comes out of the volume's own contents pages and its "
    "own editor. That also proves the nine are real and dated, which is the article's "
    "whole claim to trust. The contents pages are scan files 16-17 and carry no "
    "printed folio, so cite the running text at printed p. 6 for the inventory and the "
    "chapter openings for the individual devices.",
    "CHAPTER NUMBERS AND HEADINGS OCR BADLY IN PART III. The contents page (scan "
    "files 16-17) gives XXXIII, XXXIV and XXXV correctly, but it interleaves the "
    "titles with the page numbers ('CHAPTER ANTI-SPARKING DYNAMO 424 XXXVII. 432') and "
    "it truncates one title outright: ch. XXXVI's contents line reads 'THERMO-MAGNETIC "
    "MOTORS AND PYRO-MAGNETIC RATORS'. The chapter headings themselves print as "
    "'CHAPTER XXXIY.' (for XXXIV, printed p. 418) and 'CHAPTER ELECTROLYTIC XXXY. "
    "REGISTERING METER.' (for XXXV, printed p. 420, where the display type and the "
    "chapter title are interleaved in the OCR). Batch 2's are noisier but complete: "
    "ch. XXXVI's reads 'CHAPTEK THERMO-MAGNETIC XXXVI. MOTORS AND PYRO-MAGNETIC "
    "GENERATORS.', ch. XXXVII's reads 'CHAPTEK ANTI-SPAKKING DYNAMO XXXVII. BRUSH AND "
    "COMMUTATOR.' and ch. XXXVIII's reads 'CHAPTER XXXVIII. AUXILIARY BKUSH REGULATION "
    "OF DIRECT CURRENT DYNAMOS.' - the roman numerals are right there, 'BRUSH' is not. "
    "The running heads in this range are useless ('TlIK II MO- MAGNETISM AND PYRO "
    "MAGNKTIHM' on p. 425, 'THEKMO-MAGNETISM AND PT110-MAGNETISM' on p. 429, 'U8II "
    "RKO ULA TION' on p. 447), and the printed folio on scan file 446 OCRs as '438' "
    "when it is printed p. 428. All of these are the raw scan with its line breaks "
    "collapsed, which is how the raw OCR lines in this file are shown; they are not "
    "greppable strings and none of them is quotable. Do not quote a roman numeral, a "
    "heading or a running head: name the chapter by its title, which is unambiguous, "
    "and cite the page. If a chapter number must appear, take it from the contents page "
    "and say it is from the contents.",
    "THE BRIEF'S HOOKS ARE NOT THE PRINT'S, AND FOUR OF THE SIX PINNED SO FAR ARE "
    "WRONG OR MISLEADING. §9 brief 08 gives entry 3 as 'an amp-hour meter that counts "
    "bubbles' and entry 2 as 'the reason your capacitor is not in air'. The meter "
    "counts no bubbles and its unit is the lamp-hour (rejected #8, #9); the condenser "
    "claim is about high-frequency, high-potential apparatus only and the modern step "
    "is ours (rejected #10). Entry 4's hook does grep verbatim - 'oscillating as "
    "rapidly as 400 to 500 times a minute', 1 hit, printed p. 424 - and is still "
    "wrong about the entry, because the sentence describes a horseshoe-magnet bench "
    "experiment in a footnote, not the chapter's machine (see the flag THE "
    "400-500-A-MINUTE NUMBER IS A FOOTNOTE, NOT A SPEC). Entry 5's hook, 'the "
    "problem every DC motor had', is narrower in the print and about a different "
    "machine class (see the flag ENTRY 5'S HOOK IS ABOUT MOTORS; THE PRINT'S FAULT IS "
    "A GENERATOR FAULT). Entry 6's hook cell is empty in the brief, which is a "
    "fairness gift, not a gap: the entry writes itself from the pinned mechanism. The "
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
    "416). Batch 2's are the same shape: 'a reduction which amounts practically to a "
    "suppression of the spark' (p. 434), 'lessening the duration of the short circuit "
    "OBVIOUSLY increases the efficiency' (p. 434, an efficiency claim with no figure "
    "on it), 'more or less of the current through the field-helices is diverted' (p. "
    "438), 'the adjustment SHOULD be such that no current flows over the auxiliary "
    "brush' (p. 441), 'lights or other devices may be put on or out with SCARCELY ANY "
    "PERCEPTIBLE difference' (p. 447), and the compiler's own estimate of how far "
    "Tesla carried the thermo-magnetic work - 'though he has but glanced at them', 'one "
    "or two operative devices worthy of note' (p. 424). No experiment, efficiency "
    "figure, tariff or sales result is reported for any of the six devices. The "
    "article's case - real devices, real ingenuity, no evidence of commercial success "
    "- is carried by these hedges; nothing needs to be "
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
    "STRAY HYPHENS ARE THE MAIN OCR TRAP IN PART III. Four otherwise quotable "
    "sentences are killed by stray hyphens the scan inserts mid-sentence: 'should -be "
    "changed' (p. 423), 'for a -given time' (p. 421), and 'the light- power of the "
    "lamps' (p. 447, rejected #19 - the normaliser folds a hyphen only when "
    "whitespace follows it, so the print's hyphenated word cannot be typed the way the "
    "print sets it). A fifth is not a hyphen at all but a misread: 'the iield wire' "
    "(p. 438, rejected #20), which no normaliser fixes. All four are recorded as "
    "rejected with the alternative pin. Expect more in entries 7-9: this part of the "
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
    "outside this volume (rejected #7, #10, #11). Batch 2 adds three more: the "
    "Curie-point comparison for entry 4's 600° (see the flag THE BOOK'S 600° IS NOT "
    "THE CURIE POINT), any sentence about third-brush regulation surviving into later "
    "starting and lighting systems (entry 6 - this volume stops at 1894 and says "
    "nothing about what came after), and any sentence about commutator sparking being "
    "solved by something else (entry 5 - the book only says the older remedies were "
    "'expensive or not fully available', p. 432). feature-006/t1 must fetch and read "
    "each source it uses, keep those sentences visibly separate from the 1894 "
    "material, give them no quotation marks and no page cite, and list them in the "
    "Sources block separately from the book - the way article 06's draft handled its "
    "three modern sources. If a source is not fetched, the sentence is cut.",
    "SAFETY (§4.1). Nothing in these six chapters is safe to imply the reader should "
    "try at home: ch. XXXIV is high-potential apparatus in a sealed can of hot oil, "
    "ch. XXXV passes the whole lighting current through two conductors in an open "
    "solution, ch. XXXVI runs a spirit lamp under iron beside a permanent magnet, "
    "ch. XXXVII's last commutator holds liquid mercury in recesses between spinning "
    "discs, and ch. XXXVIII is a direct-current dynamo of the class the book calls "
    "'of great electromotive force - such, for instance, as those used for arc "
    "lighting' (p. 432). The in-book basis for the caution is the chapters' own "
    "framing ('currents of high frequency and high potential', p. 418; 'the whole of "
    "the current to be measured may be passed through the instrument', p. 423). Use it "
    "for 'do not try this', never for a health or materials claim.",
    "WORD COUNTS RE-RUN AT PIN TIME (batch 1's on 2026-10-12 and every count in this "
    "flag re-run on 2026-10-16, over the normalised text layer of our scan, whole "
    "volume, with grep_quote.py --count). Read the page list before repeating any "
    "count: --count is substring matching with a fuzzy fallback, so a short string can "
    "return OCR near-matches rather than the word - 'Curie' returns 4 and every one is "
    "'cured' or 'curved'. Batch 1: 'rectif' 0, 'diode' 0, 'semiconductor' 0, "
    "'ampere-hour' 0, 'solid-state' 0. "
    "'lamp hour' 1 (printed p. 422). 'ohm-meter' 1 (printed p. 423; 'ohm meter' 0). "
    "'electrolytic' 8 (printed pp. 236, 314, 371, 420, 423, 494). 'bubble' 9 (printed "
    "pp. 130, 173, 222, 223, 251). 'condenser' 218. 'specific inductive capacity' 18 "
    "(printed pp. 122, 126, 130, 151, 152, 160, 161, 401, 404, 405, 406, 418). "
    "'molecular bombardment' 15, of which printed p. 418 is one. "
    "'commutator' 92. 'synchronism' 35, of which this chapter's three are pp. 412, "
    "413, 416. 'valve' 4 (pp. 431, "
    "447), 'oscillation valve' 6 (pp. 129, 191, 217, 316, 492). Batch 2: '400 to 500' "
    "1 (p. 424). '1885' 1 (p. 438). 'third brush' 2 (pp. 390, 438), 'third-brush' 1 "
    "(p. 6, the editor's inventory). 'Gilbert' 1 (p. 424). 'asbestos' 4 (pp. 432, "
    "433). 'mercury' 26 (pp. 246, 277, 278, 279, 343, 402, 403, 404, 437 - only p. "
    "437 is a commutator). 'spirit lamp' 2 (pp. 278, 424; the other is not this "
    "device). '600' 1 and 'centigrade' 1, both p. 429. 'Curie' 0 exact (the 4 the tool "
    "returns are 'cured'/'curved', pp. 69, 453). 'thermo-magnetic' 3 (pp. 6, 495, "
    "496), 'thermo-magnetism' 4 (pp. 6, 424, 495, 496), 'pyromagnetic' 4 (pp. 429, "
    "494, 496), 'pyro-magnetic' 1 (p. 6), 'pyro-magnetism' 5 (pp. 6, 429, 494, 496). "
    "'magnetic gener' 4 on the default index and 5 with --keep-furniture, which adds "
    "the ch. XXXVI heading on p. 424 - that is Appendix D's 5, and it is right (see "
    "rejected #16). 'efficiency' 33 in the volume, 0 on pp. 424-431 and 0 on pp. "
    "438-447, the only one in this range at p. 434. 'per cent' 5 in the volume (pp. 8, "
    "452), 0 anywhere in pp. 424-447. 'brought to light' 1 (p. 438). 'interview with "
    "Mr. Tesla' 1 (p. 424). These are the counts "
    "the draft may print; re-run them at draft time (feature-006/t1) rather than "
    "copying, exactly as article 06's draft did.",
    "THE 400-500-A-MINUTE NUMBER IS A FOOTNOTE, NOT A SPEC (entry 4). §9 brief 08's "
    "hook for entry 4 quotes 'oscillating as rapidly as 400 to 500 times a minute', "
    "and it is the one hook in the brief that greps verbatim - 1 hit in the volume, "
    "printed p. 424. It is also the one the print puts somewhere other than the brief "
    "does. The sentence is in the compiler's footnote, describing 'a simple horseshoe "
    "magnet' and 'a piece of sheet iron bent in the form of an L' with a spirit lamp "
    "under it, which the compiler says he 'learned of' in an interview with Tesla. The "
    "footnote's own first sentence is the opposite claim about the chapter's machines: "
    "'the vibration obtained in this manner is very slow owing to the inability of the "
    "iron to follow rapid changes in temperature'. The compiler's verdict on the "
    "experiment is that it 'is interesting principally on account of the very rapid "
    "rate of vibration' - a spectacle, not a machine. The number may be printed only as "
    "what that footnote says about a bench demonstration, never as a speed, an output "
    "or a claim about anything Tesla built, and the entry should carry the footnote's "
    "own 'very slow' sentence next to it. The thermo-magnetic motor's real limit is "
    "pinned twice: the footnote, and the drawing at p. 428 where the fly-wheel turns "
    "only 'as rapidly as the armature can be heated and cooled'.",
    "THE BOOK'S 600° IS NOT THE CURIE POINT (entry 4). The only temperature in this "
    "entry is 'an orange red, or a temperature of about 600° centigrade' (p. 429), and "
    "the book's own frame for it is a thin strip heated by a flame - 'if it be very "
    "thin'. The volume never names the effect: 'Curie' has 0 exact hits, and the 4 the "
    "tool returns are fuzzy matches on 'cured' and 'curved' (pp. 69, 453). So the "
    "draft may print the book's 600° with its page and its condition, and may not say "
    "that the book describes the Curie point, give a modern Curie temperature, or "
    "explain the effect in modern terms without a modern source carried separately "
    "(see the flag MODERN CLAIMS NEED MODERN SOURCES). 'pyromagnetic' is the book's "
    "own word for the generator and it is safe to use with a page cite.",
    "ENTRY 5'S HOOK IS ABOUT MOTORS; THE PRINT'S FAULT IS A GENERATOR FAULT. §9 brief "
    "08 gives entry 5 as 'the problem every DC motor had'. The chapter opens 'IN "
    "direct current dynamos of great electromotive force - such, for instance, as "
    "those used for arc lighting' (p. 432), and both devices it describes are fixes "
    "for commutators on generators. The bridge to motors is in the book, not in our "
    "imagination - the compiler says Tesla's work was 'aimed at dispensing with it "
    "entirely as an objectionable and unnecessary part of dynamos and motors' (p. 433) "
    "- but that sentence is the compiler's characterisation, in the same paragraph that "
    "dates the second device only as 'A few years later'. Write the entry from the "
    "p. 432 sentence and cite the p. 433 sentence as the compiler's view; do not "
    "generalise the fault to every DC motor on the strength of the hook.",
    "ENTRY 5 IS UNDATED IN THE VOLUME AND ENTRY 6 IS NOT. Ch. XXXVII gives no year at "
    "all: the first device is 'some years ago' and the second 'A few years later' (both "
    "p. 432-433, pinned). Ch. XXXVIII gives 'devised by him as far back as 1885' (p. "
    "438), and '1885' is 1 hit in the whole volume - the only dated invention statement "
    "in these six chapters. It is the compiler's date, not Tesla's, and it is the only "
    "date any of the nine entries may carry from this volume. No year may be attached to "
    "entry 5's devices without a patent record checked under §6.3, and neither ch. "
    "XXXVI, XXXVII nor XXXVIII prints a patent number anywhere, so there is nothing in "
    "the text to recall from memory.",
    "ENTRY 6'S PRIORITY CLAIM IS IN THE AUTHOR'S OWN VOICE, AND IT IS NOT ON ENTRY "
    "6'S PAGE. The compiler's footnote at p. 438 frames the third brush as 'very much "
    "discussed a few years ago' and Tesla's work as 'then unknown in this field' - no "
    "dates, no references, an argument. The claim itself is at printed p. 390, in ch. "
    "XXIX, where the author writes about himself in the third person: 'it may not be "
    "thought immodest of the writer to mention that, as far as records go, he seems to "
    "have been the first who has successfully regulated machines by providing a bridge "
    "connection between a point of the external circuit and the commutator by means of "
    "a third brush'. Both hedges are in the sentence and must be kept: 'as far as "
    "records go', 'he seems to have been'. This is the only one of the nine devices "
    "Tesla claims himself in this volume. Article 11 (feature-007) is built on the same "
    "chapter, so the two pages must not contradict each other about who is speaking or "
    "what is claimed; and the compiler's 1885 at p. 438 must never be turned into "
    "Tesla's own statement.",
    "NO RESULT IS REPORTED FOR EITHER MACHINE IN PP. 424-447, AND THAT IS AN ABSENCE, "
    "NOT A VERDICT. Chs. XXXVI and XXXVIII end on what the devices are said to do - "
    "'the rapidity of the magnetic changes or fluctuations may be regulated' (p. 431), "
    "'lights or other devices may be put on or out with scarcely any perceptible "
    "difference' (p. 447) - and neither reports an output, an efficiency figure, a run, "
    "an installation or a sale. The counts establish the absence and are in the flag "
    "above: 'efficiency' 0 on pp. 424-431 and 0 on pp. 438-447, 'per cent' 0 anywhere "
    "in pp. 424-447. Ch. XXXVII is the exception that proves the pattern: it does claim "
    "'lessening the duration of the short circuit obviously increases the efficiency of "
    "the machine' (p. 434), with no figure behind it. Rejected #21 and #22 record both "
    "silences. The draft may write 'the book reports no trial' and must not write that "
    "anyone in 1894 thought these devices had failed (§4.1).",
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
    "WHAT ALREADY EXISTS FOR ENTRIES 4-6, SO feature-006/t2 DOES NOT RE-RENDER IT. "
    "website/assets/tesla1894/ already carries nineteen crops from the batch-2 range, "
    "scan files 443-464, and manifest_qc.csv marks every one keep, quality A (one C, "
    "p460-fig2-fig258.webp, 'use only as an inset or drop'). File names are SCAN "
    "files: printed page = scan - 18. Entry 4 (ch. XXXVI, scan 442-449): "
    "p443-fig1-fig281.webp (printed p. 425), p444-fig1-fig235.webp (p. 426), "
    "p445-fig1-fig287.webp (p. 427), p448-fig1-fig243.webp (p. 430). Entry 5 (ch. "
    "XXXVII, scan 450-455): p451-fig1-fig244.webp (p. 433), p452-fig1-fig247.webp (p. "
    "434), p453-fig1-fig248.webp (p. 435), p454-fig1-fig251.webp (p. 436). Entry 6 "
    "(ch. XXXVIII, scan 456-465): p457-fig1-fig253.webp (p. 439), p458-fig1-fig257 "
    "(p. 440), p459-fig1-fig255 (p. 441), p460-fig1-fig259 and p460-fig2-fig258 (p. "
    "442), p462-fig1..fig4 (p. 444), p463-fig1-fig264 (p. 445), p464-fig1-fig266 (p. "
    "446). §9 brief 08's figure table names 'p434-fig247' and 'p446-fig266', which are "
    "p452-fig1-fig247.webp and p464-fig1-fig266.webp - the same scan-file/printed-page "
    "confusion the entry 1-3 note above describes.",
    "SEVEN OF THOSE QC ROWS DO NOT TRUST THEIR OWN FIGURE NUMBER, AND ENTRY 4 HAS NO "
    "CLEAN ONE. manifest_qc.csv flags p443-fig1-fig281 ('Figure number 281 is genuine "
    "for p.425' - a number that belongs to a much later chapter), p445-fig1-fig287 "
    "('Caption spans Figs.287 and 238 - figure order garbled'), p451-fig1-fig244 "
    "('Caption spans Figs.244-245'), p454-fig1-fig251 ('Caption spans Figs.251-252'), "
    "p458-fig1-fig257 ('p.440 tagged Fig.257 but the caption text is mid-sentence'), "
    "p462-fig1 and p462-fig3/fig4 ('number unreliable'), and p463-fig1-fig264 (whose "
    "QC note reads 'OCR Fro. 265 shows the caption spans two figures'). Clean and "
    "number-confirmed: "
    "p444-fig1-fig235, p448-fig1-fig243, p452-fig1-fig247, p453-fig1-fig248, "
    "p457-fig1-fig253, p459-fig1-fig255, p460-fig1-fig259, p462-fig2-fig263, "
    "p464-fig1-fig266. For entry 5 the number-confirmed p452-fig1-fig247.webp (printed "
    "p. 434) is the one the p. 434 prose introduces alongside the suppression and "
    "efficiency sentences, and it is what §9 brief 08 asks for. For entry 6, "
    "p464-fig1-fig266.webp (printed p. 446) is the tall regulator engraving next to the "
    "dashpot text; p459-fig1-fig255.webp (p. 441) is the one the 'auxiliary brushes "
    "have been used' paragraph sits against. For entry 4 nothing in the range is both "
    "clean and correctly numbered: the p. 428 drawing the fly-wheel sentence describes, "
    "and the p. 429 'simple experiment' setup, have no crop on disk at all (no "
    "p446-*/p447-* row exists). t2 must crop from books/pdf-pages-tesla-1894/ and read "
    "the number off the printed page, exactly as §8 step 3 requires, before entry 4 can "
    "carry an engraving.",
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
        f"{PIN_DATE} (batch 1) or {BATCH2_DATE} (batch 2) from "
        f"`books/extracted/tesla-1894-plain.txt` through the same "
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
        "Entries 1-6 all sit in Part III, 'MISCELLANEOUS INVENTIONS AND WRITINGS', "
        "and none of that Part III prose is Tesla's own writing: these chapters "
        "describe his devices about him in the third person. The one exception in this "
        "pin is the printed p. 390 quote, which is from Part II and is the author's "
        "own voice. The chapters, in the order the volume prints them:",
        "",
        *[f"- {c}" for c in CHAPTERS],
        "",
        f"Verified: {len(rows)} quotes ({sum(len(r[4]) for r in rows)} fragments) "
        f"across {len(by_page)} printed pages, 0 failures. To re-check one quote: "
        "`python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>`. To "
        "regenerate this file: "
        "`python3 new_content/1894-series/08-tesla-weird-inventions-1894/gen_quotes.py` "
        "(it exits non-zero and writes nothing if any quote fails).",
        "",
        REVERIFIED,
        "",
        BATCH2,
        "",
        BATCH2_CORRECTED,
        "",
        "Do not run `check_quotes.py` on this file as a gate. It is built for a "
        "draft (`article.md`), and here its scanner reads the apostrophes in the "
        "'- why:' annotations and the struck-through Rejected items as quotation "
        "marks, so it reports 107 problems on this file when run on 2026-10-16 - 84 "
        "'not verbatim' (the annotations and struck-through rows) and 23 'not cited' "
        "(the raw OCR windows, which carry no citation because the 'cited as:' line is "
        "what the draft will print). None of them is a quote failing. The gate "
        "for a pin file is `gen_quotes.py` itself: it imports the same matcher "
        "(`check_quotes.fragments` + `check_quotes.locate` over the index "
        "`check_quotes` builds) and refuses to write anything if a quote does not "
        "verify on its stated page. `check_quotes.py` runs on `article.md` in "
        "feature-006/t3.",
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
