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
# page on a journal PDF. Measured at the smoke render below (books/tmp/f06a08d3/qa_smoke.out).
# Fixing it is an owner call at feature-006/t3, not a silent edit here: either the ABB citation
# loses its url and keeps the bibliographic text, or a non-.pdf location is found for the same
# article. Inventing a URL is the one thing not to do.
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
  - text: "Lars Jonsson and Rutger Johansson, 'High-voltage bushings: 100 years of technical advancement', ABB Review 3/2009, pp. 66 to 70, for the modern half of entry 2: oil-impregnated paper became the predominant condenser bushing technology in the 1960s and the article reports it still holding more than 80 percent of that market, and oil impregnation under vacuum is used because 'oil fills out all parts of the bushing and remains in a liquid phase throughout its entire life', void-free"
    url: "https://library.e.abb.com/public/45d14c404e73a375c125762d00485f4f/66-70%203M998_ENG72dpi.pdf"
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
#   figures, frontmatter figure record, og_image, card_image   feature-006/t2, a08-figrec
#   render and numeric gates   feature-006/t3; visual QA   feature-006/t4
# WHAT A SMOKE RENDER OF THIS DRAFT ALREADY FAILS, measured 2026-10-17 by rendering it to
# books/tmp/f06a08d3/tesla-weird-inventions-1894.html and running qa_page.py on that (output at
# books/tmp/f06a08d3/qa_smoke.out): 26 of 28 gates, 2 failures, both named with their owner. The
# reciprocal-links gate wants 3 links to pages that link back and finds none, because nothing links
# to this page yet - that is feature-006/a08-wirecommit's in-link work, not a defect in the draft.
# The D4 book-PDF gate is the ABB url noted above. Everything else passes, including the H2 count
# (6, inside 5-9) and the heading-case gate, which is why the headings are written to that case in
# the draft rather than left to be fixed on the page (decision 16).
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

### 2. Condensers With the Plates in Oil

In high-frequency, high-potential apparatus the expected insulators are wrong: glass and mica, the bodies with the highest specific inductive capacity, are "inferior as insulators" (1894, p. 418). The reason is gas. It is "very desirable to exclude all gaseous matter from the apparatus" (1894, p. 418), because molecular bombardment in it wastes energy and injures the device. The device is a can. Its plates are held apart by porous strips "used merely for the purpose of maintaining them in position" (1894, p. 419): the oil is the dielectric. The book hedges its own novelty: oil between conductors "has been a common practice" (1894, p. 419). That hedge is why this entry did not lose. Vacuum oil impregnation is still how high-voltage paper insulation is made, because oil leaves no voids; oil-impregnated bushings hold more than 80 percent of that market (Jonsson and Johansson, 2009). Nobody builds the 1894 form.

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

The pages here about magnet motors and perpetual motion are [the Tesla magnet motor](magnet-motor.html) and [perpetual motion machines](perpetual-motion-generator.html). Neither cites this book, and nothing on this page is evidence for what they sell. What this page can say is narrower: the only magnetic generator in the 1894 volume is a heat engine, and none of the nine machines here is one either.

The book never says these nine failed. For seven of them it records no trial, no output and no result. For two it records something else: entry 2's principle is still how high-voltage paper insulation is made, and entry 9's machines "worked satisfactorily" until their inventor ran out of time (1894, p. 474).

{{FAQ}}

{{CTA}}

{{SOURCES}}
