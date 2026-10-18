---
# feature-007/t1. Written from new_content/1894-series/10-tesla-free-energy-what-he-said/quotes.md,
# which is the accepted output of feature-007/t0: 72 verified quotes over 23 printed pages, 26
# rejected, 18 flags. A quote that is not in that file is not in this draft. Every count printed
# below was re-run on 2026-10-18 by word_counts.py in this directory, and it matches
# SERIES-PLAN-1894.md Appendix D exactly: free energy 0, free-energy 0, perpetual 0, over unity 0,
# over-unity 0, magnetic generator 5 at printed pp. 6, 424, 429 twice, 496.
title: "What Tesla Actually Wrote About Free Energy"
slug: tesla-free-energy-what-he-said.html
# §5.1 row 10: this row needs no _redirects rule. pretty_slug restates the file name, which is the
# condition on which redirect_rules() emits nothing, exactly as articles 01 to 06 do.
pretty_slug: /tesla-free-energy-what-he-said
description: "A word search of the 1894 first edition: free energy 0, perpetual 0, over unity 0, and five hits for magnetic generator, all of them a heat engine."
keywords: [did tesla invent free energy, tesla free energy machine true or false, tesla wheelwork of nature, tesla magnetic generator real or fake, tesla free energy myth checked]
# DRAFTING DATE, not a publish date. feature-006/a08-wirecommit settled that the publish date is
# fixed at the wiring task, one page per date in wiring order, and the ten wired pages run
# 10-14 through 10-24. This page is the eleventh, so 10-25 is the arithmetic candidate; it is
# settled at feature-007/a10-wirecommit against the state of articles.html at that moment, not here.
# §11's publish order for this page is S4, after 03, 01 and 07, so a reader meets three neutral
# history pieces before the myth-check (O2 = B, the plan's recommendation, settled in
# specs/prd.md line 86 and in this feature's own name).
date_published: "2026-10-18"
date_modified: "2026-10-18"
series_no: 10
primary_query: did tesla invent free energy
tid: "1894_10"
# og_image is the path every page in this series carries and no page in this series has the file
# yet: feature-010/t2 generates them with the script feature-010/t1 writes. Setting the path here
# is the series convention, not a claim that the file exists.
og_image: assets/og/tesla-free-energy-what-he-said.webp
# card_image is figure 1 of the page on every other article in the series, so it waits for
# feature-007/t2 with the rest of the figure record.
standfirst: "The sentence most often quoted as Nikola Tesla's promise of free energy is printed in a book that never uses the phrase. We searched our copy of the 1894 first edition and printed what came back: free energy 0, perpetual 0, over unity 0, and five hits for 'magnetic generator', every one of them inside a pyro- compound, attached to a machine that has a fire under it."
# FIGURES: none in this batch. feature-007/t2 reads the figure evidence and feature-007/a10-claims
# writes the index.json row. What the register's figure notes say, so the next task starts there
# rather than re-deriving it: of the three crops §9 brief 10 names, one is mis-numbered (printed
# p. 424 carries no engraving at all; chapter XXXVI's plates are on printed pp. 425 to 430), one
# does not exist yet (the page-scan crop of printed p. 236, which §6.6 sourcing order 4 already
# names for this article and which should be cut from books/pdf-pages-tesla-1894/page-254.pdf as
# scan-p236.webp, following the scan-p486.webp precedent), and one is already the hub's card image
# (scan-title-page.webp, index.json figures[0], still verified:false). The pyromagnetic plate
# tesla1894-p430-fig242.webp is on disk and is article 08's figure 3; §6.6 allows it here only with
# a caption about the fire and the boiler, which is a different point from article 08's. The p. 426
# plate is the unclaimed alternative. The word-search table needs no figure: it is a table.
#
# LINKS. §5.2 row 10 gives five out-links and this draft carries all five, plus the
# tesla-1894-word-search.html link that §9 brief 10 item 8 and this feature's own criteria require.
# That is six, at the top of §5.2's 4 to 6 band, so the flame sentence and the grounded-motor
# sentence name articles 06 and 07 in prose without a link, which is what the register's link notes
# recommend; adding them would put the page outside the band and move the reciprocal arithmetic.
# tesla-1894-word-search.html is feature-008/t2 and does not exist yet. The link stays, and
# feature-007/t3's qa_page run will report it dead until feature-008/t2 lands. That is the one
# cross-feature dependency in this article and it is named here rather than discovered at t3.
# COUNTS, RE-RUN 2026-10-18 BY word_counts.py IN THIS DIRECTORY, AND WHAT THE FIRST DRAFT GOT
# WRONG. The Appendix D rows agree exactly (free energy 0, free-energy 0, perpetual 0, over unity 0,
# over-unity 0, magnetic generator 5 at printed pp. 6, 424, 429 twice, 496). Four measurements the
# first draft printed wrongly, each with the number that replaces it, so none of them comes back:
#   - The corpus sentence now names the file. books/extracted/tesla-1894-plain.txt is 174,169
#     whitespace words as a file and 172,651 in its 506 page bodies, which is what the counts run
#     over; tesla-1894-fulltext.txt, the other text file of the same scan, is 176,810, and that is
#     the plan's '177,000 words'. The first draft printed 176,810 next to plain.txt, four times.
#     The stripped GATE index is 167,998 (grep_quote.build_index over load_pages(clean=True)), so
#     the honest comparison in the body is 167,998 against 174,169, not against 176,810.
#   - 'magnetic motor' is 3, not 0 (printed pp. 6, 46, 496): two are 'Thermo-Magnetic Motors' in
#     the editor's inventory and the volume's index, one is inside an OCR-broken 'electro-magnetic
#     motor' at p. 46. quotes.md flag 18 says the draft may say the phrase is never there
#     unqualified and must not imply the words never appear; the body now says exactly that. A
#     regex for a magnet word next to a generator word, either order, returns 5 (all pyro-) and 0
#     the other way, which is the sentence the first draft had wrong.
#   - Printed p. 8: the 94-and-95-per-cent three-wire sentence names no tester. The named tests on
#     that page are Prof. Anthony's in the winter of 1887-8 and the 1889 Pittsburgh tests made by
#     Tesla and Albert Schmid. Chapter I is the editor's, so 'the compiler says why he printed such
#     figures' is now 'the editor says'.
#   - Printed p. 236, counted on the page: the hedge paragraph is two paragraphs after the
#     wheelwork paragraph, not four, and Crookes is named in the sentence after it, not four
#     sentences later. The chapter heading the body names is the print's full heading,
#     'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS', which is also how article 08's
#     sources list writes it; the first draft named half of it.
# CROSS-PAGE, AND IT IS NOT NEW. website/tesla-weird-inventions-1894.html (live since
# feature-006/a08-wirecommit) prints 'four hits on three printed pages' for 'magnetic gener'
# because that article searched the GATE index; its own register records 4 and 5 side by side. This
# page prints 5 on 4 pages and now says in the body why the two numbers differ. If the owner wants
# one number on both pages, the edit is to make article 08's sentence name its index, and that
# belongs to feature-009/t2, which touches that page anyway, not to this task.
# SHAPE: §9 brief 10 item 2 asks for 'the table'. make_article.py's md_to_html has branches for
# headings, paragraphs, blockquotes, images, lists and the three placeholders, and no branch for a
# markdown table, so a table would render as a paragraph of pipes. The counts are a list instead,
# and every list item is one physical line: the list branch ends an item at the first line that
# does not start with '- ', and two wrapped items in the first draft rendered as stray paragraphs
# outside the list. Re-rendered and confirmed fixed. A real table is a make_article.py change and
# out of this task.
# WHAT WAS RUN ON THIS DRAFT, AND WHAT IT RETURNED. make_article.py into books/tmp/f07t1/ (not
# website/, so nothing was wired): 47,624 bytes, 1 h1, 8 h2, 8 h3. qa_page.py on that render:
# 26/29. The three failures are not this draft's and t3 owns them: /tesla-1894-word-search is dead
# until feature-008/t2; the reciprocal-link gate returns [] until a10-wirecommit and feature-009/t2
# put in-links on the page; and the 'Frequently asked questions' H2 is emitted sentence case by
# make_article.py's faq_block and fixed on the rendered page by titlecase_headings.py, which is how
# live pages 03 and 07 read 'Frequently Asked Questions'. check_quotes.py on this draft: 0 quote
# problems, exit 0. titlecase_headings.py --check on this draft: 0 headings not title case. Body
# 2,532 words against §9's 1,800, which is the series' existing range measured the same way (03 is
# 1,787 against 1,700, 08 is 2,128 against 1,500, 09 is 1,704 against 1,500, 06 is 5,503 against
# 1,200); no numeric gate reads word count.
cta:
  text: "The 1894 book measures what its machines wasted, and never once says a machine gives something for nothing. If you are sizing a real supply for a shed, a workshop or a small off-grid structure, the plans we recommend come with a parts list and a straight answer about output."
  href_suffix: "1894_10"
# Pages of the 1894 edition this draft cites, printed pages, measured from the body: grep the
# body for '(1894, p.' and this list is that list.
pages_used: [6, 8, 119, 120, 138, 167, 196, 197, 232, 236, 267, 394, 424, 429, 430, 494, 496]
faq:
  - q: "Did Tesla Invent Free Energy?"
    a: "Nothing in the 1894 book supports the claim. A word search of its text layer returns 0 occurrences of 'free energy', 'free-energy', 'perpetual', 'over unity' and 'over-unity'. The closest sentence in the volume is a claim about a method, not a machine: 'there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium' (1894, p. 196). On the same page he declines to say what any of it is worth in practice: 'How far the results here borne out are capable of practical applications will be decided in the future' (1894, p. 196). No device, no output, no measurement."
  - q: "What Did Tesla Actually Say About Free Energy?"
    a: "He said space is full of energy, and that a way of using it more directly ought to exist. 'Throughout space there is energy. Is this energy static or kinetic ? If static our hopes are in vain; if kinetic - and this we know it is, for certain - then it is a mere question of time when men will succeed in attaching their machinery to the very wheelwork of nature' (1894, p. 236). The next two sentences name the machine he has in mind, William Crookes' radiometer, and the same paragraph ends by putting it on record as 'the most inefficient machine ever invented' (1894, p. 236). The passage is a warning about efficiency, and the paragraph after it says what the passage was for: one-wire demonstrations."
  - q: "Does the 1894 Book Mention Perpetual Motion?"
    a: "No. 'perpetual' returns 0 hits, and so does the stem 'perpetu', so no inflected form either. The book does describe a generator that runs on heat: chapter XXXVI reports a pyromagnetic generator, and the volume's own index files it twice, under 'Generators, Pyromagnetic' (1894, p. 494) and 'Pyromagnetic Generators' (1894, p. 496), both pointing at printed p. 429. Over that chapter's own eight printed pages, 'test', 'per cent' and 'efficiency' all return 0. The chapter reports a design, an illustration and a boiler of water, and no measurement of the machine."
  - q: "Is a Tesla Magnetic Generator a Real Thing?"
    a: "Not in this book's vocabulary. 'magnetic generator' occurs 5 times in the 1894 volume, at printed pp. 6, 424, 429 twice and 496, and every one of those five sits inside 'pyro-magnetic' or 'pyromagnetic'. 'magnet motor', 'magnetic engine', 'magnetic dynamo', 'free electricity', 'bifilar' and the patent number '512,340' return 0 hits each. What the 1894 text describes is a heat engine whose magnetic circuit is opened and closed by heat: the page that names the generator also says 'Above the fire is a boiler K, containing water' (1894, p. 430). The phrase a shopper types today is a product name, and it belongs to this century."
sources:
  - text: "Chapter I, the editor's introduction, printed pp. 3 to 16 of the 1894 edition. The inventory sentence and the date fence are printed p. 6, and the efficiency figures are printed p. 8. Chapter I is the editor writing about Tesla in the third person, not Tesla"
  - text: "Chapter XXV, 'INTRODUCTION. - THE SCOPE OF THE TESLA LECTURES', printed pp. 119 to 144, which is the compiler's running review of three lectures and not Tesla's text. The one-wire summary at printed p. 137 and the grounded-motor passage at printed p. 138 are in it. The compiler labels his own chapter: 'We may now proceed to a running review of the lectures themselves' (1894, p. 119)"
  - text: "Chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY', the lecture delivered at Columbia College on May 20, 1891, dated by the chapter's own footnote: 'A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891.' (1894, p. 145). The flame passage is printed pp. 166 to 167"
  - text: "Chapter XXVII, the lecture delivered before the Institution of Electrical Engineers, London, February 1892, dated by its own footnote: 'Lecture delivered before the Institution of Electrical Engineers, London, February, 1892.' (1894, p. 198). The energy-from-the-medium passage is printed pp. 196 to 197, the one-wire sentence is printed p. 232, the wheelwork passage is printed p. 236, and the one-wire prediction is printed p. 267"
  - text: "Chapter XXXI, the paper on high-frequency currents and the body, printed p. 394, from which the 'misuse and abuse of electricity' sentence is quoted here. That paper is about medical advertising, and this article uses it only as his general position on electrical hype. The paper itself is worked through in the site's article on Tesla's high-frequency 'massage'"
  - text: "Chapter XXXVI, on thermo-magnetism and pyro-magnetism, printed pp. 424 to 431, which is the compiler's chapter about a device, with footnotes he says came from an interview with Tesla: 'In an interview with Mr. Tesla on this subject, the compiler learned of an experiment which will interest students' (1894, p. 424). The chapter's display heading is named in this article, not quoted: it is display type, and the search index that strips running heads does not contain it"
  - text: "The volume's own index, printed pp. 494 and 496, for the two entries that file the machine under pyromagnetic"
  - text: "The word search: books/extracted/tesla-1894-plain.txt, the text layer of our scan of archive.org item inventionsresear00martiala, whole volume, exact substring counts, case-insensitive, with printed page = scan file page minus 18. Re-run on 2026-10-18 by new_content/1894-series/10-tesla-free-energy-what-he-said/word_counts.py, which prints the counts three ways (raw text, the index books/tools/check_quotes.py builds, and that index with running heads and display type kept) and prints the counts scoped to printed pp. 424 to 431. The raw counts are the ones SERIES-PLAN-1894.md Appendix D prints, and they are the ones this page shows. The near-match fallback in books/tools/grep_quote.py is why no count on this page is taken from that tool's output"
  - text: "The three pages on this site that the article reads, and whose own words it reports: 'Is the magnetic generator a scam?', 'Is a Tesla Magnetic Generator Worth It?' and 'Free Electricity from Magnets: How It Works'. They are this site's current commercial pages, not sources about Tesla, and the article's rule is that it reports what they claim rather than repeating it"
  - text: "The word-search page that shows this method and its counts, tesla-1894-word-search, is not on the site yet. It is planned, and this article's table is the same measurement it will publish. The link is left in place rather than substituted, and it is recorded here as pending so the dead-link check reports it instead of hiding it"
  - text: "Every quote in this article was re-grepped and pinned to its printed page before drafting. The register is new_content/1894-series/10-tesla-free-energy-what-he-said/quotes.md, re-runnable with books/tools/grep_quote.py and regenerated by gen_quotes.py in that directory; it records 72 verified quotes, 26 rejected ones, and the flags this draft writes around"
---
**Standfirst.** The sentence most often quoted as Nikola Tesla's promise of free energy is printed
in a book that never uses the phrase. We searched our copy of the 1894 first edition: 518 page
scans, and a text file of 174,169 words. What came back: free energy 0, perpetual 0, over unity 0,
and five hits for 'magnetic generator', every one of them inside a pyro- compound, attached to a
machine with a fire under it.

## How We Searched, and What the Search Returned

The corpus is Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van
Nostrand, New York. Our copy is 518 page images and one text file of 174,169 words, marked into 506
page bodies; the counts below run over those page bodies, which are 172,651 words. Counts are exact
substrings, case-insensitive, over the whole volume. Printed pages are the book's own; the scan files
run 18 ahead. A second text file of the same scan runs 176,810 words, and that is the figure the
plan's '177,000 words' refers to; no count on this page comes from it. A word count is only
reproducible if the file and the text it was taken from are named, so this page names both here and
in the Sources block.

One thing about counting matters more than the rest. The index the quote checker builds strips
running heads and bare folios, and it is 167,998 words rather than 174,169. Over the text as it
sits on disk 'magnetic generator' counts 5, on four printed pages; over the stripped index it counts
4, on three. The missing hit is chapter XXXVI's display heading, which is display type and so is
named in this article rather than quoted: 'THERMO-MAGNETIC MOTORS AND PYRO-MAGNETIC GENERATORS'
(1894, p. 424). Five is what the printed book contains and four is what the default index reports.
The second number is the one this site's own article on nine lost inventions prints today, because
that article searched the default index; both counts are in that article's own quote register, so the
disagreement is a known thing here rather than a new one. This page prints five, because the claim it
is supporting is about the book and not about a search tool. Every number below is an exact count
from the script named in the Sources block.

The counts the brief asks for, whole volume:

- 'free energy' and 'free-energy': 0
- 'perpetual': 0, and the stem 'perpetu' 0, so no inflected form either
- 'over unity' and 'over-unity': 0
- 'magnetic generator': 5, at printed pp. 6, 424, 429 twice and 496, all five inside 'pyro-magnetic' or 'pyromagnetic'
- 'free' 97 times, and not once before the word 'energy'; 'unity' 9 times, and none of them the word, all 9 inside community, impunity and opportunity

The editor sets the volume's own limit: "The present volume deals simply with his work accomplished
to date" (1894, p. 6).

## The Sentence Everyone Posts

As the page has it, with the punctuation the printer set: "Throughout space there is energy. Is this
energy static or kinetic ? If static our hopes are in vain; if kinetic - and this we know it is, for
certain - then it is a mere question of time when men will succeed in attaching their machinery to
the very wheelwork of nature" (1894, p. 236).

The version in circulation ends at 'nature', prints 'attach' for the page's 'attaching', and stops
four sentences early. What follows names William Crookes, then the machine: "His radiometer will turn
in the light of day and in the darkness of the night; it will turn everywhere where there is heat,
and heat is everywhere" (1894, p. 236). Then the verdict: "this beautiful little machine, while it
goes down to posterity as the most interesting, must likewise be put on record as the most
inefficient machine ever invented" (1894, p. 236).

It is a conditional about kinetic energy, it names a radiometer, and it ends by calling the nearest
thing to its own idea the worst machine ever invented. Then the paragraph breaks and the book says
what the passage was for: the radiometer is one of many experiments that can be done on a single
wire at high potential and high frequency (1894, p. 236). Two paragraphs later he hedges the plan:
impracticable in many cases it may look, but "certainly seems practicable, and even recommendable,
in the production of light" (1894, p. 236).

## What He Did Claim, and in Whose Voice

This article quotes from four texts in three voices. Chapters XXVI and XXVII are the printed texts of
two lectures, his, of 1891 and 1892. Chapter XXV is the compiler's running review of those lectures,
which he says he is writing (1894, p. 119). Chapter XXXVI is the compiler's chapter about a device.
Chapter I is the editor's.

### Energy From the Medium

In the London lecture he settles the practical question first: "How far the results here borne out
are capable of practical applications will be decided in the future" (1894, p. 196). Then the
proposition: "there is a possibility of obtaining energy not only in the form of light, but motive
power, and energy of any other form, in some more direct way from the medium" (1894, p. 196). A
possibility about a method, with no machine, no output and no measurement in it. The sentence that
gets quoted is on the next page and is a wish about humanity: "There must be some way of availing
ourselves of this energy more directly" (1894, p. 197). He calls the supply a store forever
inexhaustible, which is the only time that word appears in the volume (1894, p. 197). Nothing is
demonstrated on either page.

### One Wire

"A most curious feature of alternate currents of high frequencies and potentials is that they enable
us to perform many experiments by the use of one wire only" (1894, p. 232). Experiments, at high
frequency and high potential, on a bench. The prediction, thirty-five printed pages later, carries
its condition inside the sentence: "if motors, lamps, or devices of any kind are perfected ...
economical reasons will make it advisable to use only one wire" (1894, p. 267). The condition is a
class of machine he did not have. What happened to the idea is in the site's article on one-wire
power.

### A Motor Grounded to the Earth

The compiler's, in chapter XXV, describing a rotating-field motor run from a single insulated line
(1894, p. 138); the machine is the one the site's rotating-magnetic-field article is about. Then the
claim: "Experiments of this kind seem to bring it within possibility to operate a motor at any point
of the earth's surface from a central source, without any connection to the same except through the
earth" (1894, p. 138). What follows is a chain of conditionals, none of them a build (1894, p. 138).
Then the sentence that decides what is being claimed: "In this manner, even if it were not possible
to operate machinery, intelligence might be transmitted quite certainly" (1894, p. 138). He gives up
the machinery and keeps the signalling. The book's phrase is 'the earth's potential', and it occurs
once, here.

### A Flame That Consumes No Material, in Someone Else's Words

In the 1891 lecture he writes that "we have a possible way of producing - by other than chemical
means - a veritable flame, which would give light and heat without any material being consumed"
(1894, p. 167), and the price, in the same sentence, is frequencies and potentials he did not have.
Forty-seven printed pages earlier the compiler paraphrases the idea in his own words, and his version
is the one that sounds like a free-energy claim: a flame "which consumes no material and in which no
chemical action whatever takes place" (1894, p. 120). An article that quotes that with a p. 167
citation has invented a Tesla sentence. The rest of that argument is the site's cold-flame article's.

## The Only Magnetic Generator in the Book Has a Fire Under It

The volume indexes its own generator twice and both entries point at one page. Under G:
"Generators, Pyromagnetic" (1894, p. 494). Under P: "Pyromagnetic Generators" (1894, p. 496). The
page they give is printed p. 429, and the sentence there is the prose hit the count is about:
"Mr. Tesla has also devoted his attention to the development of a pyromagnetic generator of
electricity" (1894, p. 429). The compiler's footnote on the same page is a second hit there, which is
why five hits and four pages are both true.

The machine works because heat destroys magnetism: the chapter credits that fact to William Gilbert,
an iron bar heated to redness losing its magnetism (1894, p. 424). Its stated laws are ordinary
induction plus that effect, and nothing in them is free. The generator is illustrated by a bench
setup with a flame taken to orange red (1894, p. 429), and the page describing the device says what
sits above the fire: "Above the fire is a boiler K, containing water" (1894, p. 430).

The compiler prints two judgements in that chapter, about different things, and they should not be
merged. On the field of study: "since that time the influence of heat on the magnetic metals has
been investigated frequently, though not with any material or practical result" (1894, p. 424). On
how much attention Tesla gave it: "though he has but glanced at them" (1894, p. 424). Neither is a
verdict on performance, because no performance is reported: over the chapter's eight printed pages
'test', 'per cent' and 'efficiency' are all 0, and 'output' is 1, a design property with no number
on it. An absence of measurement is not a negative measurement. The book never says this machine
failed, and this article does not either. What the book does say is that Tesla had "worked out one or
two operative devices worthy of note" (1894, p. 424).

The one number in the chapter is a vibration rate: the compiler heard about a demonstration in an
interview with Tesla, a horseshoe magnet, an L of sheet iron and a spirit lamp, vibrating "as rapidly
as 400 to 500 times a minute" (1894, p. 424). That string occurs once in the volume, and it is a
footnote about a bench demonstration, not a rating of any machine the chapter describes.
[The site's list of nine inventions that did not catch on](tesla-weird-inventions-1894.html) carries
the same footnote for a different purpose.

## What the Internet Gets Wrong

**That the phrase is his.** It is not in this book as a product name. 'magnet motor' 0,
'magnetic engine' 0, 'magnetic dynamo' 0, 'free electricity' 0, 'bifilar' 0, '512,340' 0,
'coil for electromagnets' 0. 'magnetic motor' is 3, and never stands alone: two of the three are
'Thermo-Magnetic Motors' in the editor's inventory and in the volume's own index (1894, pp. 6, 496),
and the third is inside a line the print breaks and the OCR cannot read, 'electro-magnetic motor'
(1894, p. 46), so not one of the three can be quoted as a phrase. Set a regex for a magnet word next
to a generator word in either order and the volume returns 5, all of them 'pyro-magnetic generator(s)'
or 'pyromagnetic generator(s)', and 0 in the other order. The site's review of what a Tesla magnetic
generator is attributes the device to a patent number that does not appear in this book.

**That the wheelwork sentence is a promise.** It is a conditional that ends four sentences later in
an insult about a machine's efficiency. The cut version is what circulates.

**That 400 to 500 is a rating.** It is the vibration rate of a bench demonstration the compiler says
he heard about in an interview with Tesla, and the same footnote opens by saying the chapter's own
machines vibrate 'very slow' (1894, p. 424). Print the number as a machine's rating and you have
taken a footnote out of the page it sits on. It is one string in 174,169 words.

**That he complained about free-energy hype.** He did complain about being sold, and the page is
about something else. In a two-page paper on high-frequency currents and the body, a trade article
about medical advertising, he writes that "a serious worker cannot despise anything more than the
misuse and abuse of electricity which we have frequent occasion to witness" (1894, p. 394). That is his
position on electrical hype, not a remark about free energy; what he was and was not willing to
warrant in that paper is in
[the site's article on Tesla's high-frequency 'massage'](tesla-high-frequency-massage.html).

## What This Site Sells, and What the 1894 Book Can Carry

Three pages here sell the device; the honest thing is to report what they claim in their own words.
The review of whether one is worth buying attributes the device to a Tesla patent granted in 1894,
and in its own list of drawbacks says such a machine is 'not truly free energy' and 'requires a
prime mover'. The free-electricity page describes a design that 'keeps spinning as long as the
magnets are in place'. The scam page says a device 'actually produces roughly 5 times more energy
than it consumes'. Those are this site's claims, not Tesla's, and the reader is linked to them.

What the 1894 book supplies instead is measurement. Its top efficiency figure is 94 and 95 per cent,
for larger motors on the three-wire system, and the trials below it say who ran them: Prof. Anthony's
in the winter of 1887-8, and the 1889 Pittsburgh tests made by Tesla and Albert Schmid (1894, p. 8).
The editor says why he printed such figures: they "are cited to show that the efficiency of the system has not
had to wait until the present late day for any demonstration of its commercial usefulness"
(1894, p. 8). A book that measures how little energy is wasted is not a book that promises something
for nothing. The one claim a commercial page makes that the 1894 text can meet is the existence of a
pyromagnetic generator, and the book's account of it is a firebox, a boiler and no test.

The useful thing here is not a set of zeros but a method: ask for the phrase, in the book, on the
page; ask which index a count came from; ask who is writing, since a Victorian editor summarising a
lecture is not the lecturer. The counts above are re-run and published at
[the 1894 word search](tesla-1894-word-search.html), and the two questions behind this page, what a
device is claimed to deliver and what has been measured, are worked through at
[Is the magnetic generator a scam?](magnetic-generator-scam.html),
[Is a Tesla Magnetic Generator Worth It?](tesla-magnetic-generator-worth-it.html) and
[Free Electricity from Magnets](free-electricity-from-magnets.html).

{{FAQ}}

{{CTA}}

{{SOURCES}}
