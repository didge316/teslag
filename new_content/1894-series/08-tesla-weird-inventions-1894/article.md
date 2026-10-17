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
date_published: "2026-10-17"
date_modified: "2026-10-17"
series_no: 8
primary_query: tesla lesser known inventions
tid: "1894_08"
# og_image and card_image are set at feature-006/t2 and a08-figrec, once a figure has been read
# against its printed page. card_image is figure 1 of the page on every other article in this
# series, so it waits for the same reason the figures do. App. C's candidates for this page are
# p422-fig230, p434-fig247, p446-fig266, p457-fig281, p460-fig283, p466-fig290; entry 2's
# engravings (Figs. 227 and 228, printed p. 418) have no crop and no manifest row at all, and
# books/pdf-pages-tesla-1894/page-436.pdf is there to cut them from.
standfirst: "Nine devices, each cited to the printed page of the 1894 book that collected them. The volume never says any of them failed, and for most of the nine it says nothing at all about what became of them. What it does record, entry by entry, is the thing each machine needed and had not got: a rotating armature turning in step with the line, a dielectric with no gas in it, a current that had to be reversed after every reading."
# FIGURES: none used in either draft batch. feature-006/t2 reads the figure evidence and a08-figrec
# writes the index.json row. One engraving per entry is the brief's plan; entries 1 and 3 already
# have QCd crops, entry 2 has none, and entries 4 to 6 have no crop on disk either - entry 5's
# figure is App. C's p434-fig247, which is in the candidate list below. The two crops are named on
# disk by scan file, not by printed page,
# so the names are given here as the files have them: website/assets/tesla1894/p428-fig1-fig220.webp
# (fig. 220, printed p. 410, entry 1) and website/assets/tesla1894/p440-fig1-fig230.webp (fig. 230,
# printed p. 422, entry 3), both manifest_qc keep/A at rows 149 and 157 of that CSV. Listing the
# printed-page names here instead sent the next task looking for two files that do not exist.
# App. C's own row for this page uses the same scan-file names (p440-fig230 p.422, etc.), so the
# printed-page forms in §9 brief 08 are a shorthand, not filenames. Two manifest_qc subject lines
# describe those meters wrongly, which is why the captions come from the prose and the figure
# numbers from the printed page.
#
# PAGES USED so far, to be completed with entries 7 to 9. This list is rendered into the published
# Sources block by make_article.py sources_block(), so it is the pages the page actually cites, not
# the pages consulted: printed p. 416 was read but is not cited anywhere in this draft, because the
# 'active (as distinguished from a dead) resistance' quote was left out (see LENGTH below), so 416
# is not in the list and returns only if that quote is added. The same is true of the pages this
# batch read and did not cite: 425, 428, 430, 431, 433, 439, 443 and 447 are pinned in the register
# and absent from the draft, and each returns only if its quote is added. Printed p. 390 IS here,
# because entry 6 quotes the third-brush claim from it; it is ch. XXIX, not Part III, and it is the
# same chapter article 11's page is built on. The list below is not typed by hand: it is the set of
# pages in the '(1894, p. N)' citations in the body, read out with the citation regex
# check_quotes.py uses, so it cannot disagree with the body it sits above.
pages_used: [390, 409, 412, 418, 419, 420, 422, 423, 424, 429, 432, 434, 436, 437, 438, 441]
#
# SOURCES. The two modern ones are not decoration: the register's Rejected #7 requires a modern
# source for any sentence placing entry 1 in a history of rectifiers, and the flag ENTRY 2 IS THE
# ENTRY THAT DID NOT LOSE requires one for the claim that the principle won. Both were fetched at
# drafting time on 2026-10-17 and each is listed below with the sentence it is used for. Modern
# sources are paraphrased in the body and never put inside quotation marks: check_quotes.py matches
# every double-quoted run in the body against the 1894 text, so a modern quotation in quotes is a
# FAIL there by construction, and that is how article 06 handles it too.
sources:
  - text: "Chapter XXXIII, 'METHOD OF OBTAINING DIRECT FROM ALTERNATING CURRENTS', printed pp. 409 to 417 (scan files 427 to 435). Entry 1 and the provenance quote 'Mr. Tesla divides such circuit at any desired point into two branches or paths' are from it. The chapter is the volume's editor writing about Tesla in the third person, not Tesla's writing"
  - text: "Chapter XXXIV, 'CONDENSERS WITH PLATES IN OIL', printed pp. 418 to 419 (scan files 436 to 437). Entry 2, including the editor's own footnote on printed p. 418, which is quoted in the register and not used in this draft"
  - text: "Chapter XXXV, 'ELECTROLYTIC REGISTERING METER', printed pp. 420 to 423 (scan files 438 to 441). Entry 3, including the editor's verdict on electrolytic meters at printed p. 423"
  - text: "Chapter XXXVI, 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS', printed pp. 424 to 431 (scan files 442 to 449). Entry 4. The 400-to-500-a-minute number is in the compiler's footnote on printed p. 424, about a horseshoe-magnet bench experiment he says he learned of in an interview with Tesla, and the same footnote says the chapter's own devices vibrate 'very slow'; the draft prints the number only as that footnote prints it"
  - text: "Chapter XXXVII, 'ANTI-SPARKING BRUSH AND COMMUTATOR', printed pp. 432 to 437 (scan files 450 to 455). Entry 5. The chapter gives no year for either device, only 'some years ago' and 'A few years later', and prints no patent number anywhere in it"
  - text: "Chapter XXXVIII, 'AUXILIARY BRUSH REGULATION OF DIRECT CURRENT DYNAMOS', printed pp. 438 to 447 (scan files 456 to 465). Entry 6, including 'devised by him as far back as 1885' at printed p. 438, which is the compiler's date and not Tesla's"
  - text: "Chapter XXIX, the author's own account of high-frequency alternating-current generators, printed pp. 374 to 391 (scan files 392 to 409). NOT Part III: it is the author writing about himself in the third person. Entry 6's priority claim at printed p. 390 is his own sentence with his own hedges in it. Article 11 (feature-007) is built on this same chapter and says nothing about the voice, so the two pages do not contradict each other today; if either page ever describes that voice, both must be checked together"
  - text: "Thomas J. Blalock, 'The Rotary Era, Part 2: Early AC-to-DC Power Conversion, Continued', IEEE Power and Energy Magazine, November/December 2013, for the modern half of entry 1: the mercury arc rectifier 'did away with the need to maintain bearings, commutators, and brushes as was necessary with rotary converters', Con Edison shut its last New York rotary converter substations in 1977 and moved those direct-current customers onto solid-state rectifier units, and the last IND 60-Hz rotary was shut down in 2005"
    url: "https://magazine.ieee-pes.org/novemberdecember-2013/history-10"
  - text: "Lars Jonsson and Rutger Johansson, 'High-voltage bushings: 100 years of technical advancement', ABB Review 3/2009, pp. 66 to 70, for the modern half of entry 2: oil-impregnated paper became the predominant condenser bushing technology in the 1960s and the article reports it still holding more than 80 percent of that market, and oil impregnation under vacuum is used because 'oil fills out all parts of the bushing and remains in a liquid phase throughout its entire life', void-free"
    url: "https://library.e.abb.com/public/45d14c404e73a375c125762d00485f4f/66-70%203M998_ENG72dpi.pdf"
  - text: "Every 1894 quote on this page is taken from the register new_content/1894-series/08-tesla-weird-inventions-1894/quotes.md, 126 quotes and 132 fragments across 51 printed pages with 0 failures, regenerated by gen_quotes.py in that directory, which exits non-zero and writes nothing if any quote misses. Re-runnable one at a time with books/tools/grep_quote.py"
# DRAFT STATE, feature-006/a08-draft2 (2026-10-17). This file is entries 1 to 6 of nine: batch 1
# (feature-006/t1) wrote entries 1 to 3 and this task wrote entries 4 to 6 from the register's
# batch-2 rows, with no change to entries 1 to 3. What is not here yet, and which task owns it:
#   entries 7 to 9, the intro, the closer on the only 'magnetic generator' in the volume, the
#   Part III provenance paragraph, and the FAQ   feature-006/a08-draft3
# The provenance paragraph is the intro's job and this batch does not duplicate it, but it is not
# optional: the register flag PART III IS NOT ALL THE COMPILER'S PROSE requires the page to say,
# once and early, that chs. XXXIII to XXXVIII are the compiler's third-person prose about Tesla
# ('Mr. Tesla divides such circuit', printed p. 409; 'attributable to Mr. Tesla', printed p. 420),
# that ch. XLI is Tesla's own reprinted article from printed p. 467, and that ch. XXIX (the source
# of the p. 390 claim used by entry 6) is the author writing about himself in the third person.
# Entry 1 was written without that sentence to stay inside the brief's length, so the intro must
# carry it; entry 3's 'attributable to Mr. Tesla' is the book's attribution formula, and a reader
# who is not told that will read it as Tesla writing about himself.
#   figures, frontmatter figure record, og_image, card_image   feature-006/t2, a08-figrec
#   render and numeric gates   feature-006/t3; visual QA   feature-006/t4
#   out-links and in-links per §5.2 (magnet-motor.html, perpetual-motion-generator.html, 10 out;
#   03, 10 and the hub in)   feature-006/a08-wirecommit, and no link is placed before its target
#   exists, because qa_page.py fails a dead relative href
#   cta block   assembly, with the rest of the page furniture
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
#      first try.
# LENGTH. §9 brief 08 asks for nine entries of roughly 130 words in a 1,500-word listicle. These
# six are counted with the command below, because a count without its method is the failure this
# register has already been corrected for twice:
#   python3 - <<'PY'   # split the body on '\n## ', count whitespace tokens in each section body
#   entry 1: 150 words, entry 2: 149, entry 3: 148   [feature-006/t1's three, re-measured
#   2026-10-17 by that method and unchanged]   entry 4: 156, entry 5: 153, entry 6: 156
#   [feature-006/a08-draft2's three, measured 2026-10-17 by that same command on the bytes this
#   file now holds; re-measure again at assembly, because the counts move with the text and a count
#   taken before the sentence reporting it was written is a stale count]
# All six are 14 to 20 percent over the brief's number, and the overage is the register's rules, not
# padding: entry 1 needs the synchronism sentence to say why it lost, entry 2 needs the finding and
# the book's own hedge on its novelty, entry 3 needs the reversal step and the editor's verdict,
# entry 4 needs the sentence that puts the brief's 400-to-500 number on a bench experiment instead
# of on the machine, entry 5 needs the sentence that says the fault is a generator's and the hedge
# inside the book's own claim, and entry 6 needs both hedges of the p. 390 claim, which is the
# longest quoted run in this draft at 24 words.
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
# this file holds: exit 0, 1 file, 27 quote fragments, 27 verbatim and page-cited, 0 problems
# (books/tmp/f06a08d2/cq_final.out). That is batch 1's 13 plus this batch's 14. The count is stated
# with the command, the date, the exit code and the output file, per the register's rule that a
# count without its method is a claim the next draft copies wrong. The tool counts fragments, not
# quoted runs, and splits a quotation cut by ' ... ' into its two halves, which is why 27 fragments
# come from 25 quoted runs: the p. 412 synchronism quote in batch 1 and the p. 390 claim in this
# batch are each one run cut in two, which is visible in the tool's own output as two adjacent
# fragments of one sentence. Batch 1's own pass recorded 17 fragments for a body the tool reports as
# 13, and 17 does not reproduce on any version of those bytes. One fragment ('the electrical
# resistance of the conductor is varied in a definite proportion to the strength of the current',
# printed p. 420) verifies through the space-ignoring index because the OCR glues 'isvaried'; the
# register annotates it the same way and the clean form is the print's. The other 26 are exact
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

## 1. Direct Current From Alternating Current

Chapter XXXIII splits an alternating circuit "at any desired point into two branches or paths" (1894, p. 409). One branch opposes one sign of the wave, the other the opposite sign, so the two halves go different ways. What comes out is "two or more direct currents without the employment of any commutator" (1894, p. 409). Not needing a commutator is the claim.

The volume never says the scheme failed. What it says three times, of three machines, is that they must turn in step with the supply: "the rotation and action of the commutator must be in synchronism ... with the periods of the alternations" (1894, p. 412). That is the difficulty: a rotating part tied to the line frequency. Conversion later went to static devices, and the last rotary converters feeding New York direct current were shut down in 1977 and replaced by solid-state rectifier units (Blalock, 2013).

## 2. Condensers With the Plates in Oil

In high-frequency, high-potential apparatus the expected insulators are wrong: glass and mica, the bodies with the highest specific inductive capacity, are "inferior as insulators" (1894, p. 418). The reason is gas. It is "very desirable to exclude all gaseous matter from the apparatus" (1894, p. 418), because molecular bombardment in it wastes energy and injures the device. The device is a can. Its plates are held apart by porous strips "used merely for the purpose of maintaining them in position" (1894, p. 419): the oil is the dielectric. The book hedges its own novelty: oil between conductors "has been a common practice" (1894, p. 419). That hedge is why this entry did not lose. Vacuum oil impregnation is still how high-voltage paper insulation is made, because oil leaves no voids; oil-impregnated bushings hold more than 80 percent of that market (Jonsson and Johansson, 2009). Nobody builds the 1894 form.

## 3. Electrolytic Registering Meter

Chapter XXXV opens with "an ingenious form of electrolytic meter attributable to Mr. Tesla" (1894, p. 420): metal is plated onto one conductor and stripped from the other until "the electrical resistance of the conductor is varied in a definite proportion to the strength of the current" (1894, p. 420). The unit is the lamp-hour: the book measures "the increase of resistance of one conductor or the diminution of the resistance of the other per lamp hour" (1894, p. 422). Then the fatal step, in the same chapter: after every registration the current must be reversed, "so that the deposit will be taken from the conductor which has gained and added to that which has lost" (1894, p. 423). The editor's own verdict on the whole class closes the chapter: such meters "seem to need every auxiliary advantage to make them permanently popular and successful" (1894, p. 423).

## 4. Thermo-Magnetic Motor and Pyromagnetic Generator

Heat destroys magnetism: an iron bar "when heated to redness loses its magnetism" (1894, p. 424). Tesla's thermo-magnetic motor runs on that: a burner heats an armature that a magnet pulls. The pyromagnetic generator puts the same effect to work in a coil (1894, p. 429). The compiler's own hedge on how far the work went: "he has but glanced at them" (1894, p. 424).

The spirit lamp and the L-shaped iron strip are a bench experiment, not the machine: the compiler heard of it in an interview with Tesla, and the strip vibrates against a horseshoe magnet "as rapidly as 400 to 500 times a minute" (1894, p. 424). The same footnote gives the limit - vibration is "very slow owing to the inability of the iron to follow rapid changes in temperature" (1894, p. 424). Neither machine is reported built, run or measured, and no efficiency figure appears in printed pp. 424 to 431.

## 5. Anti-Sparking Brush and Commutator

The fault is a generator's, not a motor's. In "direct current dynamos of great electromotive force - such, for instance, as those used for arc lighting" a spark appears when a commutator bar leaves the brush (1894, p. 432). The book calls the older fixes "expensive or not fully available" (1894, p. 432). Tesla's first device was mica or asbestos behind the brush, dated only as "some years ago" (1894, p. 432). His second was two matched discs, commutator and collector built alike, so the short circuit and the break "occur at the same instant" (1894, p. 434). The claim is hedged: it promises "a reduction which amounts practically to a suppression of the spark" (1894, p. 434). The insulating segments are stone: "glass, marble, or soapstone" (1894, p. 436). The last version has liquid mercury for segments (1894, p. 437). Neither is reported tested or run in printed pp. 432 to 437.

## 6. Auxiliary-Brush Regulation of Direct Current Dynamos

Chapter XXXVIII is the only one of the six chapters entries 1 to 6 come from that gives a device a year: "devised by him as far back as 1885" (1894, p. 438). No other year appears in them. The regulator adds a third brush on the commutator, bridged to a point on the field winding. Move it and "more or less of the current through the field-helices is diverted through the shunt" (1894, p. 438); set it right and, on the book's own rule, the brush carries no current at normal load (1894, p. 441).

The priority claim is his own, in another chapter, on high-frequency alternators, where he writes of himself in the third person: "as far as records go, he seems to have been the first who has successfully regulated machines ... by means of a third brush" (1894, p. 390). Chapter XXXVIII reports no installation, load test or result for the regulator.
