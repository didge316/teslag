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
# FIGURES: none used in this batch. feature-006/t2 reads the figure evidence and a08-figrec writes
# the index.json row. One engraving per entry is the brief's plan; entries 1 and 3 already have
# QCd crops, entry 2 has none. The two crops are named on disk by scan file, not by printed page,
# so the names are given here as the files have them: website/assets/tesla1894/p428-fig1-fig220.webp
# (fig. 220, printed p. 410, entry 1) and website/assets/tesla1894/p440-fig1-fig230.webp (fig. 230,
# printed p. 422, entry 3), both manifest_qc keep/A at rows 149 and 157 of that CSV. Listing the
# printed-page names here instead sent the next task looking for two files that do not exist.
# App. C's own row for this page uses the same scan-file names (p440-fig230 p.422, etc.), so the
# printed-page forms in §9 brief 08 are a shorthand, not filenames. Two manifest_qc subject lines
# describe those meters wrongly, which is why the captions come from the prose and the figure
# numbers from the printed page.
#
# PAGES USED so far, to be completed with entries 4 to 9. This list is rendered into the published
# Sources block by make_article.py sources_block(), so it is the pages the page actually cites, not
# the pages consulted: printed p. 416 was read but is not cited anywhere in this draft, because the
# 'active (as distinguished from a dead) resistance' quote was left out (see LENGTH below), so 416
# is not in the list and returns only if that quote is added.
pages_used: [409, 412, 418, 419, 420, 422, 423]
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
  - text: "Thomas J. Blalock, 'The Rotary Era, Part 2: Early AC-to-DC Power Conversion, Continued', IEEE Power and Energy Magazine, November/December 2013, for the modern half of entry 1: the mercury arc rectifier 'did away with the need to maintain bearings, commutators, and brushes as was necessary with rotary converters', Con Edison shut its last New York rotary converter substations in 1977 and moved those direct-current customers onto solid-state rectifier units, and the last IND 60-Hz rotary was shut down in 2005"
    url: "https://magazine.ieee-pes.org/novemberdecember-2013/history-10"
  - text: "Lars Jonsson and Rutger Johansson, 'High-voltage bushings: 100 years of technical advancement', ABB Review 3/2009, pp. 66 to 70, for the modern half of entry 2: oil-impregnated paper became the predominant condenser bushing technology in the 1960s and the article reports it still holding more than 80 percent of that market, and oil impregnation under vacuum is used because 'oil fills out all parts of the bushing and remains in a liquid phase throughout its entire life', void-free"
    url: "https://library.e.abb.com/public/45d14c404e73a375c125762d00485f4f/66-70%203M998_ENG72dpi.pdf"
  - text: "Every 1894 quote on this page is taken from the register new_content/1894-series/08-tesla-weird-inventions-1894/quotes.md, 126 quotes and 132 fragments across 51 printed pages with 0 failures, regenerated by gen_quotes.py in that directory, which exits non-zero and writes nothing if any quote misses. Re-runnable one at a time with books/tools/grep_quote.py"
# DRAFT STATE, feature-006/t1 (2026-10-17). This file is entries 1 to 3 of nine. What is not here
# yet, and which task owns it:
#   entries 4 to 6  feature-006/a08-draft2, from the register's batch-2 rows
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
# Three decisions this batch took, recorded where the next batch will read them:
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
# LENGTH. §9 brief 08 asks for nine entries of roughly 130 words in a 1,500-word listicle. These
# three are counted with the command below, because a count without its method is the failure this
# register has already been corrected for twice:
#   python3 - <<'PY'   # split the body on '\n## ', count whitespace tokens in each section body
#   entry 1: 150 words, entry 2: 149, entry 3: 148   [re-measured 2026-10-17 by that method and
#   unchanged; re-measure again at assembly, because the counts move with the text and a count
#   taken before the sentence reporting it was written is a stale count]
# They are 10 to 15 percent over the brief's number, and the overage is the register's rules, not
# padding: entry 1 needs the synchronism sentence to say why it lost, entry 2 needs the finding and
# the book's own hedge on its novelty, entry 3 needs the reversal step and the editor's verdict.
# Cutting to 130 would mean dropping a quote, and with it the page cite the entry exists to carry.
# Two quotes the register pins were left out for that reason and are available if the owner wants
# the entries longer: 'an active (as distinguished from a dead) resistance' (printed p. 416) for
# entry 1, and 'since the gain of one conductor should equal the loss of the other' (printed
# p. 422) for entry 3. This is a brief-owner call at VERIFY in the same shape as the article 06
# length flag, and qa_page.py has no word-count gate to catch it either.
#
# QUOTE CHECK, this batch only. python3 books/tools/check_quotes.py
# new_content/1894-series/08-tesla-weird-inventions-1894/article.md, re-run on 2026-10-17 on the
# bytes this file now holds (output kept at books/tmp/f06t1fix/cq_after_fix_run1.out): 1 file, 13
# quote fragments, 13 verbatim and page-cited, 0 problems. The first pass of this task recorded 17
# fragments and 17 verbatim here, and 17 does not reproduce on any version of these bytes: the tool
# reports 13, and 13 is what the body actually holds, because the tool counts fragments, not quoted
# runs, and splits a quotation cut by ' ... ' into its two halves (12 double-quoted runs in this
# draft, 13 fragments: the p. 412 synchronism quote is one run cut in two). The count is stated with the command,
# the date and the file the run is in, per the register's rule that a count without its method is a
# claim the next draft copies wrong. One
# fragment ('the electrical resistance of the conductor is varied in a definite proportion to the
# strength of the current', printed p. 420) verifies through the space-ignoring index because the
# OCR glues 'isvaried'; the register annotates it the same way and the clean form is the print's.
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
