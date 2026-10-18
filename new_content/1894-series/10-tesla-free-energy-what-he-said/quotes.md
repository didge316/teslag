# Article 10 quote pin: tesla-free-energy-what-he-said.html

SERIES-PLAN-1894.md §8 step 2, feature-007/t0. Every quote below was re-grepped on 2026-10-17 from `books/extracted/tesla-1894-plain.txt` through the same matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR spacing is ignored) and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). A quote carrying ' ... ' is cut where the scan or the page break interrupts it; each side of the cut is verified separately against the one page the quote is pinned to, which is how check_quotes.py will judge the draft. `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Verified: 72 quotes (73 fragments) across 23 printed pages, 0 failures. Rejected and not carried forward: 26. Flags for the writer: 18. To re-check one quote: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>` - but read HOW TO READ A COUNT first, because that tool's `--count` falls back to fuzzy matching and reports hits for words that are not in the book. To regenerate this file: `python3 new_content/1894-series/10-tesla-free-energy-what-he-said/gen_quotes.py` (it exits non-zero and writes nothing if any quote fails).

This is the trust piece of the series (§9 brief 10: 'the trust piece'), and its evidence is a count as much as a quote. So the counts in this file are measured by this script on the date above, three different ways, and the number a draft prints has to come with the index that produced it. The three indices are defined in THE THREE WAYS TO COUNT below; the disagreement between them is not noise, it is the p. 424 chapter heading, and THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE is the flag that explains it.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand Company, New York, title page 1894 (entered at the Library of Congress 1893), archive.org item `inventionsresear00martiala`. The passages this article quotes come from four different texts inside that one volume, in three different voices, and the brief's beats mix them. Read WHICH PAGES ARE TESLA WRITING and FOUR TEXTS, FOUR DATES before writing anything with 'Tesla wrote' in it.

## The size of the thing searched (brief 10 item 1)

Brief 10 says to state the method up front: 'we hold the 1894 first edition as 518 page scans and 177,000 words of text'. Both numbers are right, and the second one needs care about which text it counts. Measured on the date above:

- scan page files in books/pdf-pages-tesla-1894: 518
- page markers in tesla-1894-plain.txt: 506
- whitespace words, tesla-1894-plain.txt: 174,169
- whitespace words, tesla-1894-fulltext.txt: 176,810
- words in the search index after furniture stripping: 167,998

The 177,000 figure in the plan is the full text file. The index the search actually runs over is smaller, because running heads and bare folios are stripped out of it (§grep_quote.strip_furniture). A draft that says '177,000 words' is describing the book; a draft that says 'the searchable text is N words' is describing the search. Say which.

## THE THREE WAYS TO COUNT

- **RAW** - case-insensitive substring count over `books/extracted/tesla-1894-plain.txt` page bodies as they sit on disk, nothing normalised. This is what `grep -c` would give a reader who reproduces the claim by hand, and it is the index that produces Appendix D's numbers.
- **GATE** - the index `books/tools/check_quotes.py` builds, `load_pages(clean=True)`: short all-caps lines and bare folios are dropped as running heads, then the text is lower-cased, a hyphen at a line break is folded, and whitespace is collapsed. This is the index the numeric gate in feature-007/t3 will check the draft's quotations against - and it is also what `books/tools/check_quotes.py` and `books/tools/grep_quote.py` both build by default, because the CLI's default is `clean=True` as well. GATE and the CLI's default count are one number, not two.
- **KEEP** - the same index with `--keep-furniture`, `load_pages(clean=False)`: running heads and page-opening display type kept. This is the only one of the three that contains the chapter XXXVI heading, and so the only one that returns 5 for 'magnetic generator'.

The three indices do not agree, and not on one term: measured on the date above, 8 of the 37 terms in the two tables below count differently depending on which is used - `magnetic generator` raw 5 / GATE 4 / KEEP 5; `magnetic gener` raw 5 / GATE 4 / KEEP 5; `magnetic generators` raw 3 / GATE 2 / KEEP 3; `pyro-magnetic` raw 3 / GATE 1 / KEEP 3; `thermo-magnetic` raw 5 / GATE 3 / KEEP 5; `magnetic motor` raw 3 / GATE 4 / KEEP 5; `wheelwork of nature` raw 0 / GATE 1 / KEEP 1; `experiment` raw 429 / GATE 425 / KEEP 429.

The two mechanisms are readable straight off those numbers, and the draft has to know both. Where RAW is below the other two, a line break in the print is the cause: the phrase is on the page, but the OCR ends a line inside it, and a raw substring count cannot cross a newline - that is why 'wheelwork of nature' is 0 raw and 1 on both normalised indices, and why 'magnetic motor' is 3 raw and 4 on GATE (the normaliser folds the hyphen at the line break and joins 'electro-' to 'magnetic motor' at printed p. 55, where the raw text never sets the phrase). Where GATE is below KEEP, furniture is the cause: the hit is a running head or a display line, and `strip_furniture` drops it. The largest one is 'magnetic generator', where the missing hit is the display heading of chapter XXXVI on printed p. 424 - see THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE and THE CLI AND THE GATE SHARE AN INDEX BY DEFAULT.

## THE TABLE (brief 10 item 2, Appendix D)

Re-run at publish time by feature-007/t1's own instruction, and the draft must show the counts, not describe them. Counts are hits, and the page lists are printed pages with a hit count in parentheses where a page carries more than one.

| search term | RAW | GATE (= grep_quote.py default) | KEEP (--keep-furniture) | printed pages (RAW) | what it is |
|---|---|---|---|---|---|
| `free energy` | 0 | 0 | 0 | - | free energy / free-energy |
| `free-energy` | 0 | 0 | 0 | - | free energy / free-energy |
| `perpetual` | 0 | 0 | 0 | - | perpetual |
| `over unity` | 0 | 0 | 0 | - | over unity / over-unity |
| `over-unity` | 0 | 0 | 0 | - | over unity / over-unity |
| `magnetic generator` | 5 | 4 | 5 | 6, 424, 429(2), 496 | magnetic generator |

Appendix D prints the row 'magnetic generator | 5 - all of them **pyro**magnetic (pp. 6, 424, 429, 496)'. Those are the RAW and KEEP numbers, and 5 is the number feature-007/t1's criteria require the draft to print. GATE - which is also what `grep_quote.py` reports when run without a flag - gives 4 from the same three printed pages, because the fifth hit is a display heading. The draft prints 5 and says where the fifth hit is and which index produces 4; it does not print 4 to agree with article 08, and it does not quietly drop the heading.

## The other counts the article needs

Brief 10 item 6 says the phrase 'Tesla magnetic generator' is a 21st-century product name, not a Tesla term. That sentence is a count, so it needs the counts for the phrases the site actually uses - and the ones a reader might type. Same three indices, same page lists.

| search term | RAW | GATE (= grep_quote.py default) | KEEP (--keep-furniture) | printed pages (RAW) | why it is in the table |
|---|---|---|---|---|---|
| `magnetic gener` | 5 | 4 | 5 | 6, 424, 429(2), 496 | the stem article 08's closing beat searches |
| `magnetic generators` | 3 | 2 | 3 | 6, 424, 496 | the plural |
| `pyromagnetic` | 4 | 4 | 4 | 429(2), 494, 496 | unhyphenated |
| `pyro-magnetic` | 3 | 1 | 3 | -1, 6, 424 | hyphenated |
| `pyromagnetism` | 0 | 0 | 0 | - | the noun the chapter title uses |
| `thermo-magnetic` | 5 | 3 | 5 | -1, 6, 424, 495, 496 | the other half of ch. XXXVI's title |
| `magnetic motor` | 3 | 4 | 5 | 6, 46, 496 | the phrase the site's product vocabulary invites |
| `magnet motor` | 0 | 0 | 0 | - | the site's other product phrase |
| `magnetic engine` | 0 | 0 | 0 | - | a plausible-sounding 19th-century phrase |
| `magnetic dynamo` | 0 | 0 | 0 | - | ditto |
| `free electricity` | 0 | 0 | 0 | - | the site's phrase, and a live page's title |
| `free energ` | 0 | 0 | 0 | - | any inflected free-energy form |
| `perpetu` | 0 | 0 | 0 | - | any perpetual form |
| `unity` | 9 | 9 | 9 | 3, 4, 119, 142, 143, 156, 193, 327, 477 | what a reader searching 'over unity' by halves finds |
| `free` | 97 | 97 | 97 | 3, 11(2), 17, 32, 34, 39, 40, 43, 73, 74(2), 75(2), 90, 108, 109, 121, 122, 126(3), 128, 130, 136, 137, 138(2), 141, 145, 157, 158, 159, 165, 166, 169, 178(2), 217, 224, 231, 233(3), 234(2), 235, 242, 243, 252, 265, 275, 278, 279(2), 282(2), 289, 318, 319, 324(2), 330, 334, 337(3), 343(2), 345, 347(2), 352, 360(4), 363, 364, 369, 370(2), 382, 420, 421, 427(2), 433, 435, 445(2), 456, 457, 458(2), 470, 492 | the word alone |
| `energy` | 243 | 243 | 243 | 10, 25(2), 26(2), 49(2), 60, 81(4), 84, 120, 122, 123(2), 126, 128, 133(8), 134(2), 135(3), 137, 139(5), 140, 141, 143, 144, 145(2), 146, 157(2), 160, 162(4), 172, 174(5), 176(2), 178, 180(2), 181, 182(2), 184, 187, 189(2), 190(4), 191, 192(2), 193(3), 196(3), 197(3), 200(4), 205, 213, 214, 223(2), 224, 235(3), 236(5), 237(2), 238, 239, 240(3), 241(2), 242(3), 243(3), 245, 246, 250, 252(5), 256(3), 257(3), 258, 259, 260, 261(3), 262(5), 264, 265(2), 266(4), 267(7), 269(5), 272, 280, 282(2), 284, 287, 289, 291(3), 296, 297, 298(3), 301(5), 304(2), 309(3), 310(8), 311, 312, 314, 318, 320(4), 321, 322, 327, 332(2), 333, 336, 337, 346(2), 348(2), 351(3), 352, 353, 356, 359, 360(3), 364, 367(2), 368(2), 381, 382, 391, 409, 418, 420(2), 421(2), 423(2), 429 | the word alone |
| `wheelwork` | 2 | 2 | 2 | 236, 488 | the phrase everyone posts |
| `wheelwork of nature` | 0 | 1 | 1 | - | the phrase as quoted |
| `radiometer` | 4 | 4 | 4 | 126, 232(2), 236 | Crookes' instrument |
| `Crookes` | 14 | 14 | 14 | 121, 126, 176, 178, 198(2), 201, 236, 243, 282, 290, 322, 327, 362 | the man the passage names |
| `efficiency` | 33 | 33 | 33 | 5(2), 8(6), 24(2), 25, 30, 51, 95, 103, 105(2), 109, 172, 176, 178(5), 192, 272, 286, 377, 434, 455, 481, 492 | the book's own measured quantity |
| `commercial usefulness` | 1 | 1 | 1 | 8 | the p. 8 phrase |
| `inexhaustible` | 1 | 1 | 1 | 197 | the p. 197 word |
| `bifilar` | 0 | 0 | 0 | - | the live page's coil word |
| `512,340` | 0 | 0 | 0 | - | the live page's patent number |
| `coil for electromagnets` | 0 | 0 | 0 | - | the live page's patent title |
| `test` | 94 | 94 | 94 | -6, 5(3), 7, 8(3), 9, 17(2), 20, 21, 33, 55, 76(2), 77, 78, 79, 94, 103, 109, 132, 137, 150, 157(2), 159, 161(3), 169, 170(3), 172(4), 198, 201, 202, 205, 213, 227, 230(2), 237, 238, 253, 257, 258(2), 259, 268, 272, 297(3), 298, 299, 311, 321, 323, 326, 337, 343(3), 347(2), 357, 362, 363(3), 364, 382, 389(2), 416, 434, 440(2), 443, 453, 460, 463, 481(2), 485, 489, 494 | does ch. XXXVI report one |
| `experiment` | 429 | 425 | 429 | -3, -2, 3(2), 5(2), 6, 11, 18, 19(2), 119(2), 120(5), 121(3), 122(4), 123(3), 124, 125, 126, 128(2), 129(2), 131(2), 132(2), 133, 136(4), 138(5), 139, 140(3), 141(3), 142(3), 143(6), 144(3), 149, 150(3), 151(2), 152(5), 155, 161(4), 163, 164, 165(3), 166, 168, 170(4), 171(2), 172, 173, 174(4), 178, 181, 182, 184, 185, 186(3), 187(2), 190, 191, 193, 195(2), 196(2), 198(2), 199(3), 200(2), 201(3), 202(2), 203(2), 204(2), 205(2), 206(3), 207(2), 209, 210(2), 212(4), 213(7), 214, 215(2), 216, 217(3), 218(2), 219(2), 220(3), 222, 224, 225(3), 230(4), 231(4), 232(3), 233(4), 234(3), 236(2), 237, 238, 239, 241, 244, 247, 248, 249(2), 251(2), 253, 254(2), 257(4), 258(2), 259, 261, 262, 263(4), 264(2), 265(2), 267(2), 268(2), 269, 271, 273(4), 274(2), 275, 276, 277(2), 278, 280, 281(2), 282(2), 285(2), 286(2), 287(2), 289(2), 292, 295, 300(4), 301, 302(9), 308, 311, 312(2), 314(4), 315, 317, 318(4), 320, 321(4), 322, 323, 324, 326, 327, 329, 330(2), 333(2), 336(3), 337(2), 338(2), 339(4), 340(4), 341, 342(4), 344, 345, 346, 347, 348, 349, 350(4), 351, 352(3), 353, 356, 357(2), 358(2), 359, 360, 362(2), 364, 365(3), 367, 369, 371, 372, 374(2), 376, 377(2), 382, 383, 384(4), 385, 386(2), 390(2), 392, 396(7), 397(2), 398(3), 399(4), 400, 401(3), 402(4), 404(4), 405, 406(10), 418(4), 424(2), 429, 467, 470, 471(2), 472, 481, 485, 487(2), 488, 489(2) | ditto |
| `result` | 260 | 260 | 260 | -7, 4, 6(2), 7(2), 10(2), 11(2), 12, 13(3), 14(3), 15(4), 16(2), 18, 20(2), 21, 22, 23(3), 24(3), 25(2), 29(2), 30, 31(2), 33(2), 41, 43, 44, 45, 47, 48, 58, 60, 62, 63, 64(2), 70, 72, 76(2), 80, 81, 82, 83(3), 85(3), 88, 92, 93, 94, 96, 97, 103, 105, 109, 111(2), 112, 113, 114, 120, 121, 122(2), 124, 132, 135, 136(2), 137(2), 140, 141, 142, 144(2), 145, 147(2), 150(2), 151(2), 157, 174, 176, 177(2), 190, 191, 195, 196(4), 198, 199(2), 201(2), 202, 213(2), 217, 218, 221, 222, 226, 231(2), 232(2), 234, 235, 237, 238(2), 239, 249, 256, 259, 260, 261, 262, 264, 267, 272(2), 273(3), 274, 275(3), 276, 277, 283, 286, 287, 289(2), 290, 292, 293, 295, 298, 301, 307, 309, 313, 317, 320, 322, 323, 324, 331, 332, 333(2), 340(3), 342(2), 343, 344, 346(2), 350, 351, 352, 353(4), 354(2), 355(2), 357, 367(2), 368, 371, 373(2), 376, 382, 384, 385(2), 388(2), 390(3), 394(2), 395(2), 396, 397(2), 409, 411(2), 412, 413(2), 414(2), 416, 417, 418, 424(2), 425, 429, 430, 434, 465, 466, 468, 469, 470(6), 471, 477, 482, 487, 489, 493, 496 | ditto |
| `per cent` | 5 | 5 | 5 | 8(4), 452 | ditto |
| `output` | 19 | 19 | 19 | 8, 25, 103, 122, 158, 172, 192, 193, 224, 381, 389(3), 393, 429, 468(2), 481, 492 | ditto |

Three of those rows are the ones to write about, not just to print. `free` is 97 hits, of which 49 are the bare word and none is followed by 'energy'; the forms are 'free' 49, 'freely' 36, 'freedom' 11, 'freed' 1. `unity` is 9 hits and 0 of them is the word - all 9 are inside community, impunity, opportunity. `magnet motor` is 0 on all three indices, and `grep_quote.py --count` reports 18 for it anyway. A reader who searches a word, finds it, and believes the phrase is there is how the myth survives a spot check; this is the article in the series that says so, and the table is the evidence.

## What chapter XXXVI does and does not report (brief 10 item 5)

The pyromagnetic beat asks whether the book's only magnetic generator was ever tested. Scoped to printed pp. 424-431, the chapter's own extent, RAW counts over the unstripped page bodies:

| search term | scope | hits in the chapter | printed pages |
|---|---|---|---|
| `test` | pp. 424-431 | 0 | - |
| `experiment` | pp. 424-431 | 3 | 424(2), 429 |
| `result` | pp. 424-431 | 5 | 424(2), 425, 429, 430 |
| `per cent` | pp. 424-431 | 0 | - |
| `efficiency` | pp. 424-431 | 0 | - |
| `output` | pp. 424-431 | 1 | 429 |
| `free energy` | pp. 424-431 | 0 | - |
| `perpetual` | pp. 424-431 | 0 | - |

Three of those counts are not zero, and a count alone would mislead the draft, so every hit is here with the sentence it sits in:

- `experiment` printed p. 424: ...n temperature. In an interview with Mr. Tesla on this subject, the compiler learned of an experiment which will interest students. A simple horseshoe magnet is taken and...
- `experiment` printed p. 424: ...re it is easily set in vibration oscillating as rapidly as 400 to 500 times a minute. The experiment is very easily performed and is interesting principally on account of...
- `experiment` printed p. 429: ...n the source of the magnetism. This principle of operation may be illustrated by a simple experiment : Place end to end, and preferably in actual contact, a permanently m...
- `result` printed p. 424: ...gnetic metals has been investigated frequently, though not with any material or practical result. For a man of Mr. Tesla's inventive ability, the problems in this fie...
- `result` printed p. 424: ...operative devices worthy of note.1 He obtains mechanical power by a reciprocating action resulting from the joint operations of heat, magnetism, and a spring or weig...
- `result` printed p. 425: ...an directly against a permanent magnet, thereby avoiding the loss of magnetism that might result in the permanent magnet by the action of heat. Mr. Tesla also provide...
- `result` printed p. 429: ...in the magnetic influence to which the coil is exposed, and a current in the coil is the result. Then remove the flame or in any other way reduce the temperature of...
- `result` printed p. 430: ...e end of the iron bar or plate. The device illustrated below is a means of obtaining this result, the features of novelty in the invention being, first, the employmen...
- `output` printed p. 429: ...construction also permits of more rapid magnetic changes per unit of time, meaning larger output....

So the answer to item 5 is not 'the chapter never mentions experiments or results'. 3 'experiment' and 5 'result' are in it, and the hit list above says what they are: 'experiment' twice inside the compiler's single footnote about the horseshoe-magnet demonstration on printed p. 424, and once in the chapter's own illustration on p. 429 ('this principle of operation may be illustrated by a simple experiment'); 'result' in the compiler's verdict sentence, in 'reciprocating action resulting from', and three times in ordinary technical prose (printed pp. 425, 429, 430). What the chapter does not contain is a trial of the machine: 'test' 0 on every index, 'per cent' 0, 'efficiency' 0, and the one 'output' is 'meaning larger output', a design property with no number on it. The book's own verdict is quotable and is on printed p. 424 - 'investigated frequently, though not with any material or practical result' - and it is a stronger sentence than any absence argument, because it is the compiler writing it, in 1894, about this class of machine. Article 08's rendered page gives the same finding in prose ('a chapter that reports no output, no efficiency figure and no trial', website/tesla-weird-inventions-1894.html) and its pin records it as 'no output, no efficiency, no run, no trial, no commercial result anywhere in pp. 424-431'; article 10 may print the scoped counts and say the chapter reports a design and an illustration and no measurement of the machine. It may not write that the machine failed, or was never built, or was a failure - section 4.1. The absence of a measurement is the claim; anything stronger is the writer's.

## What the three live pages actually claim (brief 10 item 7)

Read out of `website/` on the date above, tags stripped, so the comparison in feature-007/t0's third criterion is a thing this file shows. The 1894 column is the measured RAW count over the whole volume, which is what makes the point: the words the pages use are not in the book.

### `magnetic-generator-scam.html` (1,373 words of visible text)

| term | on the live page | in the 1894 text (RAW) |
|---|---|---|
| `free energy` | 6 | 0 |
| `free-energy` | 1 | 0 |
| `perpetual` | 3 | 0 |
| `over unity` | 0 | 0 |
| `over-unity` | 0 | 0 |
| `magnetic generator` | 36 | 5 |
| `1894` | 0 | 1 |
| `512,340` | 0 | 0 |
| `bifilar` | 0 | 0 |
| `patent` | 0 | 3 |
| `wheelwork` | 0 | 2 |
| `efficiency` | 0 | 33 |
| `Tesla` | 12 | 428 |

Its own claim wording, quoted from the page as it stands:
- **over-unity claim**: "However, it actually produces roughly 5 times more energy than it consumes."
- **the worked 5x number**: "So if you put in 100 watts you get about 500 watts out."
- **the page's own framing of the sceptics' case**: "They say that generating energy from perpetual motion is simply impossible."

### `tesla-magnetic-generator-worth-it.html` (2,130 words of visible text)

| term | on the live page | in the 1894 text (RAW) |
|---|---|---|
| `free energy` | 2 | 0 |
| `free-energy` | 1 | 0 |
| `perpetual` | 4 | 0 |
| `over unity` | 0 | 0 |
| `over-unity` | 0 | 0 |
| `magnetic generator` | 39 | 5 |
| `1894` | 2 | 1 |
| `512,340` | 1 | 0 |
| `bifilar` | 5 | 0 |
| `patent` | 3 | 3 |
| `wheelwork` | 0 | 2 |
| `efficiency` | 1 | 33 |
| `Tesla` | 25 | 428 |

Its own claim wording, quoted from the page as it stands:
- **patent claim**: "What Is a Tesla Magnetic Generator? A Tesla magnetic generator is a compact, DIY power device based on Nikola Tesla's Patent No. 512,340, filed in 1893 and granted in 1894."
- **the 1894 attribution**: "Can We Use Magnets to Generate Electricity Is Magnetic Energy Renewable or Nonrenewable Unleashing The Magnet Magic Renewable Energy Using Magnets Is a Tesla Magnetic Generator Worth It? An Honest 2026 Review Published: December 7, 2025 | Updated: May 22, 2026 If you've been searching for ways to reduce your electricity bills or achieve energy independence, you've probably come across the Tesla magnetic generator , a DIY device inspired by Nikola Tesla's 1894 bifilar coil patent that claims to produce free, continuous electricity from magnets and copper wire."
- **the page's own hedge - the one clause article 10 can agree with**: "tenance , no oil changes, no fuel, no spark plugs Long lifespan , magnets don't degrade; bearings may need replacement after years DIY-friendly , clear blueprints and step-by-step guides available Eco-friendly , no emissions, no fossil fuels Cons Modest output , typically 50-300 watts, not enough for whole-home power Requires a prime mover , needs wind, water, or manual rotation to generate power Not truly "free energy" , follows the laws of thermodynamics; you put energy in to get energy out Learning curve , building one correctly requires some electrical knowledge Variable results , output depends on build quality, magnet grade, and drive mechanism Is It Worth It? The answer depends on your goals: Yes, if you want: A supplemental power source for a shed, workshop, or small off-grid structure A hands-on DIY project with real-world results A low-cost entry into magnetic generator technology A silent, emission-free power source for specific applications Maybe not, if you expect: To eliminate your entire electricity bill To power a whole house on its own A plug-and-play solution with zero building required Bottom Line A Tesla magnetic generator is absolutely worth it if you understand what it is and what it does ."

### `free-electricity-from-magnets.html` (1,343 words of visible text)

| term | on the live page | in the 1894 text (RAW) |
|---|---|---|
| `free energy` | 3 | 0 |
| `free-energy` | 1 | 0 |
| `perpetual` | 3 | 0 |
| `over unity` | 0 | 0 |
| `over-unity` | 0 | 0 |
| `magnetic generator` | 24 | 5 |
| `1894` | 0 | 1 |
| `512,340` | 0 | 0 |
| `bifilar` | 0 | 0 |
| `patent` | 0 | 3 |
| `wheelwork` | 0 | 2 |
| `efficiency` | 0 | 33 |
| `Tesla` | 9 | 428 |

Its own claim wording, quoted from the page as it stands:
- **perpetual-motion claim**: "The perpetual motion generator design keeps spinning as long as the magnets are in place."
- **a savings number**: "The exact savings depend on your household size and power consumption, but a single unit can reduce your bill by 30 to 50 percent."

What article 10 may and may not carry across that gap. It may say the 1894 book never uses 'free energy', 'perpetual motion' or 'over unity'; never mentions a bifilar coil, patent 512,340 or a 'coil for electromagnets'; and attaches 'magnetic generator' only to a heat engine. It may report what each live page claims, in the pages' own words, with the link. It may not let the book's authority leak onto the pages' claims: a sentence that puts a p. 429 quotation next to a 5x energy figure implies the book supports the figure, and it does not. The one live-page claim the 1894 text does meet is the existence of a pyromagnetic generator, and the book's own account of it is a firebox, a boiler and no test. §4.1 again: no sentence about what the product can do that is not already on a live page - and equally, no live page's claim dressed up as a historical one.

## Quotes, pinned by printed page

## Printed p. -8 (scan file 10, unnumbered front-matter leaf)

### 0. Provenance (the copyright leaf)

> "Entered according to Act of Congress in the year 1893 ... in the office of the Librarian of Congress at Washington"

- cited as: `(1894, p. -8)`
- why: the method section says it searched 'the 1894 first edition', and this is the leaf that dates the book: entered 1893, title page 1894. Both halves verify; the whole line does not, because the OCR of the printer's imprint breaks the run - Rejected #1. Cite it as an unnumbered front-matter leaf by its scan file, never as 'p. -8'
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0; frag 2: exact match, ratio 1.0
- raw OCR (frag 1: Entered according to Act of Congress in ): `Entered according to Act of Congress in the year 1893 by T. C. MARTIN in the office of the Librarian of Congress at Washington Press of Mcllroy & Emmet, 36 Cortlandt St., N. Y.`
- raw OCR (frag 2: in the office of the Librarian of Congre): `Entered according to Act of Congress in the year 1893 by T. C. MARTIN in the office of the Librarian of Congress at Washington Press of Mcllroy & Emmet, 36 Cortlandt St., N. Y.`

## Printed p. 6 (scan file 24)

### 0. Provenance (ch. I, the editor's date fence)

> "The present volume deals simply with his work accomplished to date"

- cited as: `(1894, p. 6)`
- why: the editor's own limit on the whole volume: everything in it is work already done by 1894. That is what licenses the article's question - these are devices described and written up by 1894, so asking what the book actually says about energy is fair and no 'Tesla predicted the future' framing is needed (section 4.1). Article 08's pin quotes the same line; the two articles must use it the same way
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...he conversion of alternating into direct currents, etc. It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting ideas and inventions, tobe made public in due course. The present volume deals simply with his work accomplished to date.`

### 2. The table (the editor's own inventory, ch. I)

> "includes a great many other inventions in arc lighting, transformers, pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, improvements in dynamos, new forms of incandescent lamps, electrical meters, condensers, unipolar dynamos, the conversion of alternating into direct currents"

- cited as: `(1894, p. 6)`
- why: the first of the five 'magnetic generator' hits, and the only place in the volume where the phrase is hyphenated 'pyro-magnetic generators'. It is also the book's own inventory of the devices the phrase is attached to, and the only generator word in it is a pyro- one. Start the quote at 'includes': the print sets ' Miscellaneous ' in its own quote marks, which would split the run in check_quotes.py's scanner
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...in this volume, with a few supplementary notes. Mr. Tesla's work ranges far beyond the vast departments of polyphase currents and high potential lighting. The " Miscellaneous "section of this volume includes a great many other inventions in arc lighting, transformers, pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, improvements in dynamos, new forms of incandescent lamps, electrical meters, condensers, unipolar dynamos, the conversion of alternating into direct currents, etc. It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting ideas and inventions, tobe made public in due course. The present volume deals simply with his work acc...`

## Printed p. 8 (scan file 26)

### 7. The honest pivot (a measured efficiency, 1888)

> "Prof. Anthony in his remarks before the American Institute of Electrical Engineers, in May, 1888, on the two small Tesla motors then shown, which he had tested, stated that one gave an efficiency of about 50 per cent, and the other a little over sixty per cent"

- cited as: `(1894, p. 8)`
- why: the counter-evidence to the premise of the free-energy myth: this book contains measured efficiencies, cited to a named tester who tested the machines. Article 07 owns this record (Appendix D 'Efficiency record') and printed these numbers first; read the flag THE EFFICIENCY RECORD BELONGS TO ARTICLE 07 before using more than one sentence of it here
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ble development next to be witnessed. Incidental reference has been made to the efficiency of rotating field motors, a matter of much importance, though it is not the intention to dwell upon it here. Prof. Anthony in his remarks before the American Institute of Electrical Engineers, in May, 1888, on the two small Tesla motors then shown, which he had tested, stated that one gave an efficiency of about 50 per cent, and the other a little over sixty per cent. In 1889, some tests were reported from Pittsburgh, made by Mr. Tesla and Mr. Albert Schmid, on motors up to 10 H. p. and weighing about 850 pounds. These machines showed an efficiency of nearly 90 p...`

### 7. The honest pivot (the top number in the book)

> "With some larger motors it was then found practicable to obtain an efficiency, with the three wire system, up to as high as 94 and 95 per cent"

- cited as: `(1894, p. 8)`
- why: 94-95 per cent. A real, cited, sub-unity number, in a book that never writes 'free energy' or 'perpetual'. That contrast is the honest pivot in one line: the book measures how little energy is wasted, which is a different question from getting something for nothing
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `..., some tests were reported from Pittsburgh, made by Mr. Tesla and Mr. Albert Schmid, on motors up to 10 H. p. and weighing about 850 pounds. These machines showed an efficiency of nearly 90 per cent. With some larger motors it was then found practicable to obtain an efficiency, with the three wire system, up to as high as 94 and 95 per cent. These interesting figures, which, of course, might be supplemented by others more elaborate and of later date, are cited to show that the efficiency of the system has not had to wait until the prese...`

### 7. The honest pivot (why the compiler prints them)

> "These interesting figures, which, of course, might be supplemented by others more elaborate and of later date, are cited to show that the efficiency of the system has not had to wait until the present late day for any demonstration of its commercial usefulness"

- cited as: `(1894, p. 8)`
- why: the compiler's stated reason for giving the figures: to show the system's commercial usefulness was demonstrated long before 1894. 'commercial usefulness' is 1 hit in the volume, here. The book's own answer to 'did his machines work', and it is about the alternating-current system, not about any generator on this site
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...se machines showed an efficiency of nearly 90 per cent. With some larger motors it was then found practicable to obtain an efficiency, with the three wire system, up to as high as 94 and 95 per cent. These interesting figures, which, of course, might be supplemented by others more elaborate and of later date, are cited to show that the efficiency of the system has not had to wait until the present late day for any demonstration of its commercial usefulness. An invention is none the less beautiful because it may lack utility, but it must be a pleasure to any inventor to know that the ideas he is advancing are fraught with substantial benefits to the pub...`

### 7. The honest pivot (the sentence to be careful with)

> "An invention is none the less beautiful because it may lack utility"

- cited as: `(1894, p. 8)`
- why: the compiler's most quotable line, and the one most likely to be turned into a thesis about failed inventions. It is the first half of a sentence whose point is that this inventor's ideas DID carry utility: 'but it must be a pleasure to any inventor to know that the ideas he is advancing are fraught with substantial benefits to the public'. Quote the turn as well, or cut the sentence. See the flag THE BEAUTY-WITHOUT-UTILITY LINE IS HALF A SENTENCE
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...nted by others more elaborate and of later date, are cited to show that the efficiency of the system has not had to wait until the present late day for any demonstration of its commercial usefulness. An invention is none the less beautiful because it may lack utility, but it must be a pleasure to any inventor to know that the ideas he is advancing are fraught with substantial benefits to the public.`

## Printed p. 119 (scan file 137)

### 0. Provenance (ch. XXV opening - the compiler's voice)

> "BEFORE proceeding to study the three Tesla lectures here presented, the reader may find it of some assistance to have his attention directed to the main points of interest and significance therein"

- cited as: `(1894, p. 119)`
- why: printed pp. 119-144 are chapter XXV, the compiler's introduction to the lectures, not Tesla writing. The brief's 'earth-potential motors (p. 138)' sits inside it. This sentence proves it: he is introducing 'the three Tesla lectures', first person plural, about Tesla in the third
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `CHAPTER XXV. INTRODUCTION. — THE SCOPE OF THE TESLA LECTURES. BEFORE proceeding to study the three Tesla lectures here presented, the reader may find it of some assistance to have his attention directed to the main points of interest and significance therein. The lirst of these lectures was delivered in New York, at Columbia College, before the American Institute of Electrical Engineers, May 20, 1891. The urgent desire expressed immediately from all part...`

### 0. Provenance (ch. XXV, the compiler labels his own chapter)

> "We may now proceed to a running review of the lectures themselves"

- cited as: `(1894, p. 119)`
- why: the compiler says his chapter is a running review. So the p. 138 earth-potential passage is a book writer's summary of a demonstration Tesla gave, not Tesla's own claim. The draft may still use it and must attribute it. See the flag WHICH PAGES ARE TESLA WRITING
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...need of the hour and occasion, Mr. Tesla did not hesitate to show many new and brilliant experiments, and to advance the frontier of discovery far beyond any point he had theretofore marked publicly. We may now proceed to a running review of the lectures themselves. The ground covered by them is so vast that only the`

## Printed p. 120 (scan file 138)

### 4. What he did claim: a flame without combustion (the compiler paraphrases it first)

> "the production of a veritable flame by the agitation of electrostatically charged molecules"

- cited as: `(1894, p. 120)`
- why: chapter XXV, the compiler, two chapters and forty-seven printed pages before Tesla's own sentence. He calls it 'a veritable flame' too, and adds that it points to a flame consuming no material. Two voices, one idea, two pages: an article that quotes the compiler's sentence with a p. 167 cite has invented a Tesla sentence
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...electrical and magnetic effects may be referred to ek-ctrostajtic _irLolecular _ forces. This opinion finds a singular confirmation in one of the most striking experiments which he describes, namely, the production of a veritable flame by the agitation of electrostatically charged molecules. It is of the highest interest to observe that this result points out a way of obtaining a flame which consumes no material and in which no chemical action whatever takes place. It also throws a ligh...`

### 4. What he did claim: a flame without combustion (the compiler's version)

> "this result points out a way of obtaining a flame which consumes no material and in which no chemical action whatever takes place"

- cited as: `(1894, p. 120)`
- why: the compiler's wording, which is closer to brief 10's phrase 'a flame without combustion' than Tesla's is. Pinned so the draft can see which sentence it is actually quoting
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...of the most striking experiments which he describes, namely, the production of a veritable flame by the agitation of electrostatically charged molecules. It is of the highest interest to observe that this result points out a way of obtaining a flame which consumes no material and in which no chemical action whatever takes place. It also throws a light on the nature of the ordinary flame, which Mr. Tesla believes to be due to electrostatic molecular actions, which, if true, would lead directly to the idea that even chemical...`

## Printed p. 137 (scan file 155)

### 4. What he did claim: one wire (the compiler's version, ch. XXV)

> "An interesting feature of these high frequency currents is that they allow of operating all kinds of devices by connecting the device with only one leading wire to the electric source"

- cited as: `(1894, p. 137)`
- why: the earliest one-wire statement in the volume, and it is the compiler's, in the introduction, describing a demonstration. Not in brief 10, which names pp. 232 and 267; pinned because the 'what happened' half needs the sequence - the compiler states the practical case first, Tesla states it twice later in his own voice. Attribute this one to the book, not to Tesla
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...translation through measurable space would cease, and, with a sufficiently high frequency and intensity of the stress, the carriers would be drawn towards the electrode, and compression would result. An interesting feature of these high frequency currents is that they allow of operating all kinds of devices by connecting the device with only one leading wire to the electric source. In fact, under certain conditions it may be more economical to supply the electrical energy witli one lead than with two.`

### 4. What he did claim: one wire (the half that verifies)

> "it may be more economical to supply the electrical energy"

- cited as: `(1894, p. 137)`
- why: the second half of the compiler's p. 137 sentence, cut short because the print's next words are 'witli one lead', an OCR l-for-i no index folds. The full sentence is Rejected #4. The draft may quote this half and paraphrase the rest, or leave p. 137 out and use pp. 232 and 267, which is what the brief asks for
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ure of these high frequency currents is that they allow of operating all kinds of devices by connecting the device with only one leading wire to the electric source. In fact, under certain conditions it may be more economical to supply the electrical energy witli one lead than with two.`

## Printed p. 138 (scan file 156)

### 4. What he did claim: an earth-potential motor (the demonstration)

> "An experiment of special interest shown by Mr. Tesla, is the running, by the use of only one insulated line, of a motor operating on the principle of the rotating magnetic field enunciated by Mr. Tesla"

- cited as: `(1894, p. 138)`
- why: what was actually shown, on one insulated line, with the rotating-field motor - the machine article 07 is about. The compiler wrote it, in the third person, naming him twice. This is the 'what he demonstrated' half of brief 10 item 4 for this entry, and it is the honest one: a disc turned on a bench
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `138 INVENTIONS OF NIKOLA TESLA. An experiment of special interest shown by Mr. Tesla, is the running, by the use of only one insulated line, of a motor operating on the principle of the rotating magnetic field enunciated by Mr. Tesla. A simple form of such a motor is obtained by winding upon a laminated iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc wit...`

### 4. What he did claim: an earth-potential motor (the claim)

> "Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth"

- cited as: `(1894, p. 138)`
- why: brief 10 item 4's fourth entry. Read the hedges: 'seem to bring it within possibility'. The claim is that a thing is possible in principle, not that a machine was built. Article 10's whole argument is the difference between those two, so the hedges stay in the quote
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...nals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment, the disc is set in rotation. Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by co...`

### 4. What he did claim: an earth-potential motor (the proposed apparatus)

> "a grounded wire reaching up to some height would be traversed by a current"

- cited as: `(1894, p. 138)`
- why: the apparatus he proposes, in the conditional: 'If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire ... would be traversed by a current'. Nothing in the volume says it was built. The longer form is Rejected #5 - the OCR breaks its middle
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, whic...`

### 4. What he did claim: an earth-potential motor (the second conditional)

> "The current might be converted to low tension and used to operate a motor or other device"

- cited as: `(1894, p. 138)`
- why: 'might' - a chain of conditionals: if the variations were produced a wire would carry a current, which might be converted, which might drive a motor. Four steps, none of them a build. This is what a 19th-century 'energy from the earth' claim actually looks like in print
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might b...`

### 4. What he did claim: an earth-potential motor (the ship)

> "The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea"

- cited as: `(1894, p. 138)`
- why: Appendix A's p. 138 row. He never claims a machine; he says an experiment would be interesting and would probably work best on a ship. 'best succeed on a ship at sea' is 1 hit in the volume, here ('ship at sea' is 2, the other at p. 168 in the same lecture). The internet prints this as Tesla predicting wireless power; the sentence is about a scientific experiment
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...aversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly. In the course of this experimental study special attention was devoted to the he...`

### 4. What he did claim: an earth-potential motor (what he actually claims for it)

> "In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly"

- cited as: `(1894, p. 138)`
- why: the claim he does make is about signalling, and he concedes machinery may not be possible in the same breath. If the article wants one sentence to show the gap between the myth and the text, this is it
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...e current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly. In the course of this experimental study special attention was devoted to the heating effects produced by these currents, which are not only striking, but open up the possibility of producing a more...`

## Printed p. 145 (scan file 163)

### 0. Provenance (ch. XXVI footnote)

> "A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891."

- cited as: `(1894, p. 145)`
- why: dates the chapter that carries the p. 167 flame passage. Two dates, two chapters, and the article quotes from both: if it says '1892' about the flame or '1891' about the wheelwork sentence it is wrong. Read the flag FOUR TEXTS, FOUR DATES before writing brief 10 item 4
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...is still conjecture, yet we know that the truth cannot be much longer hidden, and instinctively we feel that the understanding is dawning upon us. We still admire these beautiful phenomena, these 1. A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891.`

## Printed p. 166 (scan file 184)

### 4. What he did claim: a flame without combustion (the argument)

> "But they do not only resemble, they are veritable flames, for they are hot"

- cited as: `(1894, p. 166)`
- why: his argument for calling the brush a flame, in his own lecture (ch. XXVI, May 1891). Pinned to p. 166, not 167: the sentence is on the page before the one brief 10 names, and the page break falls inside the passage. See the flag THE FLAME PASSAGE STRADDLES A PAGE BREAK
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...value, one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure (Fig. 110). But they do not only resemble, they are veritable flames, for they are hot. Certainly they are not as hot as a gas burner, but they would be so if the frequency cmd the potential would be sufficiently high. Produced with, say, twenty thousand alternations per second, the he...`

### 4. What he did claim: a flame without combustion (the number)

> "Produced with, say, twenty thousand alternations per second, the heat is easily perceptible even if the potential is not excessively high"

- cited as: `(1894, p. 166)`
- why: a worked number attached to a demonstration, on the same page - the counterweight to the aspirational passages: here he gives a frequency and a sensory result. Article 11's chapter is the machine that produced such frequencies and article 06's page is built on this same brush passage; read the flag THIS BEAT IS ALREADY ANOTHER ARTICLE'S before writing it up
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...y do not only resemble, they are veritable flames, for they are hot. Certainly they are not as hot as a gas burner, but they would be so if the frequency cmd the potential would be sufficiently high. Produced with, say, twenty thousand alternations per second, the heat is easily perceptible even if the potential is not excessively high. The heat developed is, of course, due to the impact of the air molecules against the terminals and against each other. As, at the ordinary pressures, the mean free path is excessively small, it is p...`

## Printed p. 167 (scan file 185)

### 4. What he did claim: a flame without combustion (the claim)

> "a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place"

- cited as: `(1894, p. 167)`
- why: brief 10 item 4's fifth entry and Appendix A's p. 167 row, in the form that verifies. Note the conditional 'would give' and that the sentence begins 'we have a possible way of producing'. The compiler paraphrased the same idea two chapters earlier in his own words (p. 120, pinned below), so the article must be clear which voice says what
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...we have, after all, always had " electric light and heat " at our disposal. It is also of no little interest to contemplate, that we have a possible way of producing — by other than chemical means — a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods of producing enormous frequencies and potentials. I have no doubt that if the potential could be made to alternate with sufficient rapidity an...`

### 4. What he did claim: a flame without combustion (the whole conditional, with its price)

> "we have a possible way of producing - by other than chemical means - a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods of producing enormous frequencies and potentials"

- cited as: `(1894, p. 167)`
- why: the full sentence including the condition: 'we only need to perfect methods of producing enormous frequencies and potentials'. The print's em dashes are typed as ' - '. Print this if the article wants the claim and its price in one quote
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...heating, we are finally led to recognize, that since time immemorial we have, after all, always had " electric light and heat " at our disposal. It is also of no little interest to contemplate, that we have a possible way of producing — by other than chemical means — a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only nee...`

### 4. What he did claim: a flame without combustion (the rhetorical end)

> "it seems strange that after all these centuries past of familiarity with the flame, now, in this era of electric lighting and heating, we are finally led to recognize, that since time immemorial we have, after all, always had"

- cited as: `(1894, p. 167)`
- why: his own joke on the same page: we have always had 'electric light and heat' at our disposal. Pinned only up to 'had' because the next words are set by the print in its own quotation marks, which breaks check_quotes.py's pairing - Rejected #6. Paraphrase the phrase and cite the page
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...r some purpose or other suggests itself. When contemplating this singular phenomenon of the hot brush, we cannot help being convinced that a similar process must take place in the ordinary flame, and it seems strange that after all these centuries past of familiarity with the flame, now, in this era of electric lighting and heating, we are finally led to recognize, that since time immemorial we have, after all, always had " electric light and heat " at our disposal. It is also of no little interest to contemplate, that we have a possible way of producing — by other than chemical means — a veritable flame, which would...`

## Printed p. 196 (scan file 214)

### 4. What he did claim: energy from the medium (the hedge first)

> "How far the results here borne out are capable of practical applications will be decided in the future"

- cited as: `(1894, p. 196)`
- why: the sentence that comes before the passage the free-energy posters quote. He declines to claim a practical application, in the same lecture, on the page before. If the article quotes pp. 196-197 without this, it has reproduced the internet's error with better sources
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...many observations I have selected only those which I thought most likely to interest you. The field is wide and completely unexplored, and at every step a new truth is gleaned, a novel fact observed. How far the results here borne out are capable of practical applications will be decided in the future. As regards the production of light, some results already reached are encouraging and make me confident in asserting that the practical solution of the problem lies in the direction I have endeavored...`

### 4. What he did claim: energy from the medium (the claim)

> "there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium"

- cited as: `(1894, p. 196)`
- why: the actual proposition, in his words: energy 'in some more direct way from the medium'. The closest the 1894 book comes to a free-energy sentence, and it is a possibility claim about a method, not a device. Brief 10 item 4's first entry
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...le to obtain the higher light vibrations without going through the lower heat vibrations. It is the problem of imparting to a body a certain velocity without passing through all lower velocities. But there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium. The time will be when this will be accomplished, and the time has come when one may utter such words before an enlightened audience without being considered a visionary. AVe are whirling through`

### 4. What he did claim: energy from the medium (he knows how it sounds)

> "the time has come when one may utter such words before an enlightened audience without being considered a visionary"

- cited as: `(1894, p. 196)`
- why: he flags his own claim as visionary, in the impersonal third person ('one may utter'), to an institution. The honest pivot needs this: the book's own author tells the audience how the claim will land
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...bility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium. The time will be when this will be accomplished, and the time has come when one may utter such words before an enlightened audience without being considered a visionary. AVe are whirling through`

## Printed p. 197 (scan file 215)

### 4. What he did claim: energy from the medium (the sentence that straddles a page break)

> "whirling through endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy"

- cited as: `(1894, p. 197)`
- straddle: this ONE fragment sits on printed pp. 196-197 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches its citation regex
- why: Appendix A's pp. 196-197 row, in the form that verifies. The run starts on printed p. 196 and ends on 197, and its first words are the ones the OCR cannot read: the scan sets 'AVe are whirling through' at the foot of p. 196, so Appendix A's 'We are whirling through endless space' does not verify at all - Rejected #3. Cite p. 197, where the fragment ends and where check_quotes.py will accept the citation. Read the flag THE OCR BREAKS THE ONE SENTENCE APPENDIX A QUOTES
- check_quotes.py: exact match, ratio 1.0 (this ONE fragment straddles printed pp. 196-197; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `moil FREQUENCY AND HIGH POTENTIAL CURRENTS. 197 endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy. There must be some way of availing ourselves of this energy more directly. Then, with the light...`

### 4. What he did claim: energy from the medium (the demand)

> "There must be some way of availing ourselves of this energy more directly"

- cited as: `(1894, p. 197)`
- why: 'there must be' - an assertion about what ought to exist, right after the description of space as full of energy. The strongest sentence in the volume for the free-energy reading, and it names no machine, no output and no method
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `moil FREQUENCY AND HIGH POTENTIAL CURRENTS. 197 endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy. There must be some way of availing ourselves of this energy more directly. Then, with the light obtained from the medium, with the power derived from it, with every form of energy obtained without effort, from the store forever inexhaustible, humanity will advance with gia...`

### 4. What he did claim: energy from the medium (the hope, uncut)

> "Then, with the light obtained from the medium, with the power derived from it, with every form of energy obtained without effort, from the store forever inexhaustible, humanity will advance with giant strides"

- cited as: `(1894, p. 197)`
- why: 'without effort', 'forever inexhaustible' - the words a free-energy reader would want, in a sentence about humanity, not about a generator. 'inexhaustible' is 1 hit in the whole volume and it is here; the article can say that. It is a wish in a lecture close: the paragraph ends by saying the contemplation of these possibilities 'fills our hearts with supreme delight'
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy. There must be some way of availing ourselves of this energy more directly. Then, with the light obtained from the medium, with the power derived from it, with every form of energy obtained without effort, from the store forever inexhaustible, humanity will advance with giant strides. The mere contemplation of these magnificent possibilities expands our minds, strengthens our hopes and fills our hearts with supreme delight.`

## Printed p. 198 (scan file 216)

### 0. Provenance (ch. XXVII footnote)

> "Lecture delivered before the Institution of Electrical Engineers, London, February, 1892."

- cited as: `(1894, p. 198)`
- why: dates the chapter that carries the p. 236 quote, the pp. 196-197 'energy from the medium' passage, the p. 232 one-wire sentence and the p. 267 one-wire prediction. Section 3's quote style prints 'Tesla wrote in 1892', so the date has to be in the pin, not in memory. Article 06's pin carries the same footnote for the same reason
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...which led me to these advances — which even by myself cannot be considered trifling, since they are so appreciated by you — I believe that their real origin, that which started me to work in this 1. Lecture delivered before the Institution of Electrical Engineers, London, February, 1892.`

## Printed p. 232 (scan file 250)

### 4. What he did claim: one wire (Tesla's own, ch. XXVII)

> "A most curious feature of alternate currents of high frequencies and potentials is that they enable us to perform many experiments by the use of one wire only"

- cited as: `(1894, p. 232)`
- why: brief 10 item 4's second entry, in his own voice, in the chapter that carries the wheelwork passage. Note what the claim is scoped to: 'experiments', with high frequency and high potential. It is not a power-transmission claim, and the sentence four pages later (p. 236) says the plan may be impracticable
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...with the electric radiometer the potential should not exceed a certain limit, as then the electrostatic attraction between the vanes and the glass of the bulb may be so great as to stop the rotation. A most curious feature of alternate currents of high frequencies and potentials is that they enable us to perform many experiments by the use of one wire only. In many respects this feat, ure is of great interest.`

## Printed p. 236 (scan file 254)

### 3. The quote everyone posts (ch. XXVII, the sentence itself)

> "Throughout space there is energy. Is this energy static or kinetic ? If static our hopes are in vain; if kinetic - and this we know it is, for certain - then it is a mere question of time when men will succeed in attaching their machinery to the very wheelwork of nature"

- cited as: `(1894, p. 236)`
- why: the sentence the internet prints, in the form the print actually has. Two things the brief's version gets wrong and the draft must not copy: the print says 'attaching', not 'attach', and the sentence is not a promise - it is a conditional about kinetic energy that ends, four sentences later, in an insult about a machine's efficiency. The print's em dashes are typed here as ' - ', the form the normaliser folds to. See the flag THE RUNBOOK'S OWN EXAMPLE COMMAND MISQUOTES THE PRINT
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...myth of Antheus, who derives power from the earth ; we find it among the subtle speculations of one of your splendid mathematicians, and in many hints and statements of thinkers of the present time. Throughout space there is energy. Is this energy static or kinetic ? If static our hopes are in vain; if kinetic — and this we know it is, for certain — then it is a mere question of time when men will succeed in attaching their machinery to the very wheelwork of nature. Of all, living or dead, Crookes came nea...`

### 3. The quote everyone posts (the sentence the posts cut)

> "Of all, living or dead, Crookes came nearest to doing it"

- cited as: `(1894, p. 236)`
- why: the sentence immediately after the famous one, and the reason the passage is about a machine at all. Crookes is named, so the next quote has a subject. No internet version of the quote includes this line
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...static our hopes are in vain; if kinetic — and this we know it is, for certain — then it is a mere question of time when men will succeed in attaching their machinery to the very wheelwork of nature. Of all, living or dead, Crookes came nearest to doing it. His radiometer will turn in the light of day and in the darkness of the night; it will turn everywhere where there is heat, and heat is everywhere. But, unfortunately, this beautiful little machine,...`

### 3. The quote everyone posts (the radiometer)

> "His radiometer will turn in the light of day and in the darkness of the night; it will turn everywhere where there is heat, and heat is everywhere"

- cited as: `(1894, p. 236)`
- why: what 'attaching machinery to the wheelwork of nature' looks like in the book: a radiometer running on heat. This makes the passage about a heat engine, not about magnets - the same category error as the pyromagnetic beat, running the other way
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...w it is, for certain — then it is a mere question of time when men will succeed in attaching their machinery to the very wheelwork of nature. Of all, living or dead, Crookes came nearest to doing it. His radiometer will turn in the light of day and in the darkness of the night; it will turn everywhere where there is heat, and heat is everywhere. But, unfortunately, this beautiful little machine, while it goes down to posterity as the most interesting, must likewise be put on record as the most inefficient machine ever invented ! The precedi...`

### 3. The quote everyone posts (the warning)

> "this beautiful little machine, while it goes down to posterity as the most interesting, must likewise be put on record as the most inefficient machine ever invented"

- cited as: `(1894, p. 236)`
- why: the beat brief 10 item 3 asks for and the end of the passage: Tesla's own verdict on the machine he has just held up as the nearest thing to his own idea. Stop the quote before the exclamation mark - the print sets a space before it, 'ever invented !', and the glued form is not in the run. Rejected #2
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ookes came nearest to doing it. His radiometer will turn in the light of day and in the darkness of the night; it will turn everywhere where there is heat, and heat is everywhere. But, unfortunately, this beautiful little machine, while it goes down to posterity as the most interesting, must likewise be put on record as the most inefficient machine ever invented ! The preceding experiment is only one of many equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency. We may connect an...`

### 3. The quote everyone posts (what the passage is actually about)

> "The preceding experiment is only one of many equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency"

- cited as: `(1894, p. 236)`
- why: the paragraph break lands here: the wheelwork passage is the preface to the one-wire demonstrations, and the book says so in its own transition. This sentence lets the article connect brief 10 item 3 to item 4 without inventing a link
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...everywhere. But, unfortunately, this beautiful little machine, while it goes down to posterity as the most interesting, must likewise be put on record as the most inefficient machine ever invented ! The preceding experiment is only one of many equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency. We may connect an insulated line to a source of such currents, we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusi...`

### 3. The quote everyone posts (the demonstration on the same page)

> "we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusing a thick copper wire"

- cited as: `(1894, p. 236)`
- why: Appendix A's p. 236 row. What he actually demonstrated, on the same printed page as the famous sentence: a small current in, a heavy current out at any point of the wire. It is a transformer effect, not an energy claim, and the article must not let the two readings merge
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ny equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency. We may connect an insulated line to a source of such currents, we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusing a thick copper wire. Or we may, by the help of some artifice, decompose a solution in any electrolytic cell by connecting only one pole of the cell to the line or source of energy. Or we may, by attaching to the line, o...`

### 4. What he did claim: one wire (his own hedge, same page)

> "However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light"

- cited as: `(1894, p. 236)`
- why: Tesla hedging his own one-wire plan in the same lecture, four paragraphs after the famous sentence. 'However impracticable ... it certainly seems practicable' is the register the article should be quoting when it separates what he claimed from what he demonstrated
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...pole of the cell to the line or source of energy. Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire. It is now a fact that a body may be rendered incandes...`

### 4. What he did claim: one wire (the conditional)

> "A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire"

- cited as: `(1894, p. 236)`
- why: 'if wires were used at all' - a conditional, not a plan. Brief 10 item 4 asks for 'what he said, what he demonstrated, what happened', and this is the 'what he said' half in the weakest form he himself used
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `..., an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire. It is now a fact that a body may be rendered incandescent or phosphorescent by bringing it either in single contact or merely in the vicinity of a source of electric impulses of the proper character...`

## Printed p. 267 (scan file 285)

### 4. What he did claim: one wire (the reasoning)

> "when transmitted through conductors, it follows that, on the whole, it is better to employ one wire than two"

- cited as: `(1894, p. 267)`
- why: the reasoning behind the one-wire case, in his own lecture, thirty-five printed pages after p. 232. 'on the whole' is in the sentence and stays in the quote
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ller, the higher the frequency. But since, on the assumption before made, the loss is diminished with the square of the density, and since currents of very high frequencies involve considerable waste when transmitted through conductors, it follows that, on the whole, it is better to employ one wire than two. Therefore, if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequency, economical reasons will make it advisable to use...`

### 4. What he did claim: one wire (the prediction, and its condition)

> "if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequency, economical reasons will make it advisable to use only one wire, especially if the distances are great"

- cited as: `(1894, p. 267)`
- why: brief 10 item 4's third entry. The prediction is real and it is conditional: it depends on motors and lamps first being 'perfected'. That is the 'what he said vs what happened' beat in one sentence, and the article must print the condition, not only the prediction
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ensity, and since currents of very high frequencies involve considerable waste when transmitted through conductors, it follows that, on the whole, it is better to employ one wire than two. Therefore, if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequency, economical reasons will make it advisable to use only one wire, especially if the distances are great. When energy is absorbed in a condenser, the same behaves as though its capacity were increased. Absorption always exists more or less, but generally it is small and of no consequence us long as the...`

## Printed p. 394 (scan file 412)

### 6. What the internet gets wrong (Tesla on being sold)

> "I trust that the present brief communication will not be interpreted as an effort on my part to put myself on record as a"

- cited as: `(1894, p. 394)`
- why: chapter XXXI, Tesla's own opening, in the first person: he does not want to be put on record as a 'patent medicine' man. The phrase inside the print's own quote marks is Rejected #8. Use this narrowly and keep it narrow: it is about electrical quackery in medicine, in an 1894 paper on massage, and it is not Tesla on free energy. Read the flag THE PATENT-MEDICINE SENTENCE IS NOT ABOUT FREE ENERGY
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `CHAPTER XXXI. " MASSAGE " WITH CURRENTS OF HIGH FREQUENCY.1 I TRUST that the present brief communication will not be interpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electr...`

### 6. What the internet gets wrong (his own words on hype)

> "a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness"

- cited as: `(1894, p. 394)`
- why: the sentence that carries the beat: a serious worker's contempt for the misuse and abuse of electricity, in his own voice, on a page article 05 already used for a different purpose. The article may print it as his general position on electrical hype; it may not stage it as a remark about free-energy claims, which it is not
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...XXI. " MASSAGE " WITH CURRENTS OF HIGH FREQUENCY.1 I TRUST that the present brief communication will not be interpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness. My remarks are elicited by the lively interest which prominent medical practitioners evince at every real advance in electrical investigation. The progress in recent years has been so great that eve...`

## Printed p. 424 (scan file 442)

### 5. The pyromagnetic twist (the physics the chapter starts from)

> "a loadstone or iron bar when heated to redness loses its magnetism"

- cited as: `(1894, p. 424)`
- why: the chapter's opening fact, attributed to William Gilbert 'as far back as the beginning of the seventeenth century'. The machine works because heat destroys magnetism - which is why it is a heat engine. Brief 10 item 5's opening
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ies justice until he has attacked the subject of thermo-magiietism. As far back as the beginning of the seventeenth century it was shown by Dr. William Gilbert, the father of modern electricity, that a loadstone or iron bar when heated to redness loses its magnetism ; and since that time the influence of heat on the magnetic metals has been investigated frequently, though not with any material or practical result. For a man of Mr. Tesla's inventive ability, the...`

### 5. The pyromagnetic twist (the compiler's verdict before the machine)

> "since that time the influence of heat on the magnetic metals has been investigated frequently, though not with any material or practical result"

- cited as: `(1894, p. 424)`
- why: the compiler's own assessment in the chapter's first paragraph: this line of work had produced nothing practical. A verdict inside the book, in 1894, about this class of machine, and the strongest sentence article 10 has for the pyromagnetic beat. It is not a verdict on Tesla's machine - read the flag THE CHAPTER'S OWN VERDICTS, IN ORDER
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...r back as the beginning of the seventeenth century it was shown by Dr. William Gilbert, the father of modern electricity, that a loadstone or iron bar when heated to redness loses its magnetism ; and since that time the influence of heat on the magnetic metals has been investigated frequently, though not with any material or practical result. For a man of Mr. Tesla's inventive ability, the problems in this field have naturally had no small fascination, and though he has but glanced at them, it is to be hoped he may find time to pursue th...`

### 5. The pyromagnetic twist (he only glanced at it)

> "For a man of Mr. Tesla's inventive ability, the problems in this field have naturally had no small fascination, and though he has but glanced at them, it is to be hoped he may find time to pursue the study deeper and further"

- cited as: `(1894, p. 424)`
- why: 'though he has but glanced at them'. The compiler, in the same paragraph, says Tesla barely touched this field. That clause disposes of any reading of the pyromagnetic generator as Tesla's great project; print it rather than paraphrase it
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...n bar when heated to redness loses its magnetism ; and since that time the influence of heat on the magnetic metals has been investigated frequently, though not with any material or practical result. For a man of Mr. Tesla's inventive ability, the problems in this field have naturally had no small fascination, and though he has but glanced at them, it is to be hoped he may find time to pursue the study deeper and further. For such as he, the investigation must undoubtedly bear fruit. Meanwhile he has worked out one or two operative devices worthy of note.1 He obtains mechanical power by a reciprocating action resulti...`

### 5. The pyromagnetic twist (what the chapter actually claims)

> "Meanwhile he has worked out one or two operative devices worthy of note"

- cited as: `(1894, p. 424)`
- why: 'one or two' and 'worthy of note' - the extent of the claim. No trial, no output, no installation anywhere in the chapter (see the scoped counts in THE TABLE). The article may write that the book reports no test; it may not write that the machine failed (section 4.1)
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...no small fascination, and though he has but glanced at them, it is to be hoped he may find time to pursue the study deeper and further. For such as he, the investigation must undoubtedly bear fruit. Meanwhile he has worked out one or two operative devices worthy of note.1 He obtains mechanical power by a reciprocating action resulting from the joint operations of heat, magnetism, and a spring or weight or other force — that is to say he subjects a body magnetized by...`

### 5. The pyromagnetic twist (what the thermo-magnetic motor is)

> "He obtains mechanical power by a reciprocating action resulting from the joint operations of heat, magnetism, and a spring or weight or other force"

- cited as: `(1894, p. 424)`
- why: the motor half of the chapter in one sentence: heat, magnetism and a spring. A reciprocating heat engine with a magnetic valve in it. This is what the 'motors' in the chapter title are, and it makes the pyromagnetic point without any word search at all
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...hoped he may find time to pursue the study deeper and further. For such as he, the investigation must undoubtedly bear fruit. Meanwhile he has worked out one or two operative devices worthy of note.1 He obtains mechanical power by a reciprocating action resulting from the joint operations of heat, magnetism, and a spring or weight or other force — that is to say he subjects a body magnetized by induction or otherwise to the action of heat until the magnetism is sufficiently neutralized to allow a weight or spring to give motion to the body a...`

### 5. The pyromagnetic twist (the limitation, in the compiler's footnote)

> "the vibration obtained in this manner is very slow owing to the inability of the iron to follow rapid changes in temperature"

- cited as: `(1894, p. 424)`
- why: the compiler's footnote explains why these machines are slow: iron cannot follow rapid temperature changes. A physical limit stated in the book itself, in 1894, about this class of machine. The 'why it did not catch on' half can rest on this sentence instead of on speculation
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...g to give motion to the body and lessen the action of the heat, so that the magnetism may be sufficiently restored to move the 1. It will, of course, be inferred from the nature of these devices that the vibration obtained in this manner is very slow owing to the inability of the iron to follow rapid changes in temperature. In an interview with Mr. Tesla on this subject, the compiler learned of an experiment which will interest students. A simple horseshoe magnet is taken and a piece of sheet iron bent in the form of a...`

### 5. The pyromagnetic twist (where the famous number comes from)

> "In an interview with Mr. Tesla on this subject, the compiler learned of an experiment which will interest students"

- cited as: `(1894, p. 424)`
- why: the provenance of the 400-500 figure: the compiler heard about a demonstration in an interview with Tesla. So the number the internet quotes as a machine's operating rate is a hearsay demonstration, and the book says so on the same page. Cite the footnote as the compiler's, not as Tesla's claim
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...1. It will, of course, be inferred from the nature of these devices that the vibration obtained in this manner is very slow owing to the inability of the iron to follow rapid changes in temperature. In an interview with Mr. Tesla on this subject, the compiler learned of an experiment which will interest students. A simple horseshoe magnet is taken and a piece of sheet iron bent in the form of an L is brought in contact with one of the poles and placed in such a position that it is kept in the attraction of t...`

### 5. The pyromagnetic twist (the spirit lamp)

> "A spirit lamp is placed under the sheet iron piece and when the iron is heated to a certain temperature it is easily set in vibration oscillating as rapidly as 400 to 500 times a minute"

- cited as: `(1894, p. 424)`
- why: the demonstration itself: a horseshoe magnet, an L-shaped strip of sheet iron, a spirit lamp, and a vibration. '400 to 500' is 1 hit in the whole volume, here. Article 08's pin carries the same sentence for its entry 4; the two articles must not both present it as a machine's rating. Read the flag THE 400-500 SENTENCE IS ONE ARTICLE'S CLOSING BEAT AND THE OTHER'S OPENING
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...d a piece of sheet iron bent in the form of an L is brought in contact with one of the poles and placed in such a position that it is kept in the attraction of the opposite pole delicately suspended. A spirit lamp is placed under the sheet iron piece and when the iron is heated to a certain temperature it is easily set in vibration oscillating as rapidly as 400 to 500 times a minute. The experiment is very easily performed and is interesting principally on account of the very rapid rate of vibration.`

### 5. The pyromagnetic twist (what the demonstration was for)

> "The experiment is very easily performed and is interesting principally on account of the very rapid rate of vibration"

- cited as: `(1894, p. 424)`
- why: the compiler's note on the demonstration: it is interesting because of the vibration rate, not because of any power produced. No watts, no output, no efficiency in the footnote
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...y suspended. A spirit lamp is placed under the sheet iron piece and when the iron is heated to a certain temperature it is easily set in vibration oscillating as rapidly as 400 to 500 times a minute. The experiment is very easily performed and is interesting principally on account of the very rapid rate of vibration.`

## Printed p. 429 (scan file 447)

### 2. The table (the body-text hit, ch. XXXVI)

> "Mr. Tesla has also devoted his attention to the development of a pyromagnetic generator of electricity"

- cited as: `(1894, p. 429)`
- why: the volume's prose attaching 'generator' to a magnet word - and the heat word is in the same sentence, 'pyro'. The trailing footnote digit on 'electricity1' does not break the match, so the phrase is quotable. This is the machine the table's row 4 is about
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `THEKMO-MAGNETISM AND PT110-MAGNETISM. 429 Mr. Tesla has also devoted his attention to the development of a pyromagnetic generator of electricity1 based upon the following laws : First, that electricity or electrical energy is developed in any conducting body by subjecting such body to a varying magnetic influence ; and second, that the magnet...`

### 2. The table (the compiler's footnote - the second hit on the same page)

> "The enlargement of these ideas will be found in Mr. Tesla's work on the pyromagnetic generator, treated in this chapter"

- cited as: `(1894, p. 429)`
- why: the second of two body hits on printed p. 429, in the compiler's own footnote on that page. It matters for the count: one page carries two of the five, which is why '5 hits' and '4 pages' are both true and neither is an error. It also says the compiler thinks the machine is covered twice in one chapter
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...oted is that Mr. Tesla attacked this problem in a way which was, from the standpoint of theory, and that of an engineer, far better than that from which some earlier trials in this direction started. The enlargement of these ideas will be found in Mr. Tesla's work on the pyromagnetic generator, treated in this chapter. The chief effort of the inventor was to economize the heat, which was accomplished by inclosing the iron in a source of heat well insulated, and by cooling the iron by means of steam, utilizing the...`

### 5. The pyromagnetic twist (the generator claims to rest on physics)

> "based upon the following laws"

- cited as: `(1894, p. 429)`
- why: the sentence introducing the two laws the pyromagnetic generator is said to rest on. Short, but it is the hinge between the table row and the physics, and it verifies exactly
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `THEKMO-MAGNETISM AND PT110-MAGNETISM. 429 Mr. Tesla has also devoted his attention to the development of a pyromagnetic generator of electricity1 based upon the following laws : First, that electricity or electrical energy is developed in any conducting body by subjecting such body to a varying magnetic influence ; and second, that the magnetic properties of iron or other...`

### 5. The pyromagnetic twist (law one)

> "First, that electricity or electrical energy is developed in any conducting body by subjecting such body to a varying magnetic influence"

- cited as: `(1894, p. 429)`
- why: the first law is plain induction. Nothing free about it, and the chapter says so in the same structure it uses to sell the machine. This is the sentence that lets the article say the pyromagnetic generator is a heat engine driving an ordinary induction effect
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `THEKMO-MAGNETISM AND PT110-MAGNETISM. 429 Mr. Tesla has also devoted his attention to the development of a pyromagnetic generator of electricity1 based upon the following laws : First, that electricity or electrical energy is developed in any conducting body by subjecting such body to a varying magnetic influence ; and second, that the magnetic properties of iron or other magnetic substance may be partially or entirely destroyedor caused to disappear by raising it to a certain temperature, but restored and ca...`

### 5. The pyromagnetic twist (law two)

> "the magnetic properties of iron or other magnetic substance may be partially or entirely destroyed or caused to disappear by raising it to a certain temperature"

- cited as: `(1894, p. 429)`
- why: the second law: heat destroys the magnetism. Verifies only through the space-ignoring index, because the OCR glues 'destroyedor' at a line end; the print has the space. Annotated in the entry, and the two indices are set out in the section 'THE THREE WAYS TO COUNT'
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way
- raw OCR: `...lectricity1 based upon the following laws : First, that electricity or electrical energy is developed in any conducting body by subjecting such body to a varying magnetic influence ; and second, that the magnetic properties of iron or other magnetic substance may be partially or entirely destroyedor caused to disappear by raising it to a certain temperature, but restored and caused to reappear by again lowering its temperature to a certain degree. These laws may be applied in the production of electrical currents in many ways, the principle of which is...`

### 5. The pyromagnetic twist (the demonstration the generator rests on)

> "This principle of operation may be illustrated by a simple experiment"

- cited as: `(1894, p. 429)`
- why: what the generator is illustrated by: a bar, a coil and a flame, on a bench. The chapter never moves from the illustration to a machine that was run
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...a varying magnetic influence, producing such variations by the application ofheat, or, more strictly speaking, by the application or action of a varying temperature upon the source of the magnetism. This principle of operation may be illustrated by a simple experiment : Place end to end, and preferably in actual contact, a permanently magnetized steel bar and a strip or bar of soft iron. Around the end of the iron bar or plate wind a coil of insulated wire. Then a...`

### 5. The pyromagnetic twist (the flame again)

> "Then apply to the iron between the coil and the steel bar a flame or other source of heat which will be capable of raising that portion of the iron to an orange red"

- cited as: `(1894, p. 429)`
- why: the heat source in the book's own words: a flame, to orange red, about 600 degrees centigrade. Every version of this machine has fire in it, which is the point of brief 10 item 5
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...riment : Place end to end, and preferably in actual contact, a permanently magnetized steel bar and a strip or bar of soft iron. Around the end of the iron bar or plate wind a coil of insulated wire. Then apply to the iron between the coil and the steel bar a flame or other source of heat which will be capable of raising that portion of the iron to an orange red, or a temperature of about 600° centigrade. "When this condition is reached, the iron somewhat suddenly loses its magnetic properties, if it be very thin, and the same effect is produced as though th...`

### 5. The pyromagnetic twist (the compiler's praise, and its limits)

> "The chief point to be noted is that Mr. Tesla attacked this problem in a way which was, from the standpoint of theory, and that of an engineer, far better than that from which some earlier trials in this direction started"

- cited as: `(1894, p. 429)`
- why: the footnote praises the theory, not the machine: 'from the standpoint of theory, and that of an engineer'. The closest thing to a favourable verdict in the chapter, and it still says nothing about output. Quotable, with the qualifier kept
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...re is accompanied by a return of its magnetic properties, and another change of magnetic conditions occurs, accompanied by a current in an opposite direction in the coil. The same operation may be 1. The chief point to be noted is that Mr. Tesla attacked this problem in a way which was, from the standpoint of theory, and that of an engineer, far better than that from which some earlier trials in this direction started. The enlargement of these ideas will be found in Mr. Tesla's work on the pyromagnetic generator, treated in this chapter. The chief effort of the inventor was to economize the heat, which was accompl...`

### 5. The pyromagnetic twist (a boiler, in the footnote)

> "The chief effort of the inventor was to economize the heat, which was accomplished by inclosing the iron in a source of heat well insulated, and by cooling the iron by means of steam, utilizing the steam over again"

- cited as: `(1894, p. 429)`
- why: the design effort was heat management: an insulated heat source and reused steam cooling. Read with the p. 430 engraving, which shows a firebox, a fire and a boiler of water, this settles what the machine is. It is the compiler's footnote, not Tesla's words, and the article must not present it as his
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...far better than that from which some earlier trials in this direction started. The enlargement of these ideas will be found in Mr. Tesla's work on the pyromagnetic generator, treated in this chapter. The chief effort of the inventor was to economize the heat, which was accomplished by inclosing the iron in a source of heat well insulated, and by cooling the iron by means of steam, utilizing the steam over again. The construction also permits of more rapid magnetic changes per unit of time, meaning larger output.`

### 5. The pyromagnetic twist (the only output sentence in the chapter)

> "The construction also permits of more rapid magnetic changes per unit of time, meaning larger output"

- cited as: `(1894, p. 429)`
- why: 'meaning larger output' - a design property with no number attached. The scoped counts in THE TABLE show what the chapter does not contain: no 'per cent', no efficiency figure, no test. The article may say the chapter states a design intention and reports no measurement
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...of the inventor was to economize the heat, which was accomplished by inclosing the iron in a source of heat well insulated, and by cooling the iron by means of steam, utilizing the steam over again. The construction also permits of more rapid magnetic changes per unit of time, meaning larger output.`

## Printed p. 430 (scan file 448)

### 5. The pyromagnetic twist (the run that starts on the page before)

> "repeated indefinitely, the effect upon the coil being similar to that which would follow from moving the magnetized bar to and from the end of the iron bar or plate"

- cited as: `(1894, p. 430)`
- why: the first three words are at the foot of printed p. 429, so the quote is pinned to p. 430, where the rest of it sits and where the citation will be accepted. The full run across the break is Rejected #7. It matters because it is the chapter's own description of the machine as a repeating cycle - a heat engine in the ordinary sense
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `430 INVENTIONS OF NIKOLA TESLA. repeated indefinitely, the effect upon the coil being similar to that which would follow from moving the magnetized bar to and from the end of the iron bar or plate. The device illustrated below is a means of obtaining this result, the features of novelty in the invention being, first, the employment of an artificial cooling device, and, second, inclosing the so...`

### 5. The pyromagnetic twist (what is claimed as new)

> "the features of novelty in the invention being, first, the employment of an artificial cooling device, and, second, inclosing the source of heat"

- cited as: `(1894, p. 430)`
- why: the two features of novelty: a cooling device and an enclosed heat source. Not a new physics and not a free source: a boiler arrangement. This is the claim the chapter actually makes, and it is what the engraving on the same page illustrates
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...t upon the coil being similar to that which would follow from moving the magnetized bar to and from the end of the iron bar or plate. The device illustrated below is a means of obtaining this result, the features of novelty in the invention being, first, the employment of an artificial cooling device, and, second, inclosing the source of heat and that portion of the magnetic circuit exposed to the heat and artificially cooling the heated part. These improvements are applicable generally to the generators constructed on the plan above desc...`

### 5. The pyromagnetic twist (the boiler, in the body text)

> "Above the fire is a boiler K, containing water"

- cited as: `(1894, p. 430)`
- why: the plainest sentence in the chapter, and the one the pyromagnetic beat should print: there is a fire and there is a boiler of water. A steam engine's furniture, in a chapter whose title says magnetic
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...in which the currents are developed. In the circuits of these coils are current-consuming devices, as F F'. n is a furnace or closed fire-box, through which the central portion of the core B extends. Above the fire is a boiler K, containing water. The flue L from the fire-box may extend up through the boiler. G is a water-supply pipe, and H is the steam-exhaust pipe, which communicates with all the tubes c in the armature B, so that steam esc...`

## Printed p. 431 (scan file 449)

### 5. The pyromagnetic twist (the chapter's last substantive claim)

> "There are special advantages in the employment of a cooling device, in that the metal of the core B is not so quickly oxidized"

- cited as: `(1894, p. 431)`
- why: an advantage about oxidation, not output. The chapter ends on what the device is said to make possible, not on what it did
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...ent of which the valve is opened or closed. In such a case as this the heat of the fire may he utilized for other purposes after as much of it as may be needed has been applied to heating the core u. There are special advantages in the employment of a cooling device, in that the metal of the core B is not so quickly oxidized. Moreover, the difference between the temperature of the applied heat and of the steam, air, or whatever gas or fluid be applied as the cooling medium, may be increased or decreased at will, whereby...`

### 5. The pyromagnetic twist (the chapter's last sentence)

> "whereby the rapidity of the magnetic changes or fluctuations may be regulated"

- cited as: `(1894, p. 431)`
- why: the last words of chapter XXXVI: the rate of change 'may be regulated'. No trial, no figure, no run, no installation. Article 08's pin records the same silence for the same chapter; the two articles must say the same thing about it, in the same scoped words
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...oxidized. Moreover, the difference between the temperature of the applied heat and of the steam, air, or whatever gas or fluid be applied as the cooling medium, may be increased or decreased at will, whereby the rapidity of the magnetic changes or fluctuations may be regulated.`

## Printed p. 494 (scan file 512)

### 2. The table (the volume's own index, G entry)

> "Generators, Pyromagnetic"

- cited as: `(1894, p. 494)`
- why: the same entry alphabetised the other way, on a different index leaf. Two index entries, both pointing at printed p. 429, and nothing anywhere else in the volume. The strongest single piece of evidence for the article's claim that the book's only generator-with-magnets is a heat engine: the book's own indexers filed it that way twice
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...es in Vacuum Tubes 396 Electrolytic Registering Meter. 420 Eye, Observations on the 294 Flames, Electrostatic, Non-Consuming 166,272 Forbes Unipolar Generator. 468, 474 Franklin Institute Lecture 294 Generators, Pyromagnetic 429 High Potential, High Frequency : Brush Phenomena in High Vacuum 226 Carborundum Buttons.. 140, 253 Disruptivemena Discharge Pheno- 212 Flames, Electrostatic, NonConsuming 166, 272 Impedance, Nove...`

## Printed p. 496 (scan file 514)

### 2. The table (the volume's own index, P entry)

> "Pyromagnetic Generators"

- cited as: `(1894, p. 496)`
- why: the fifth hit. The volume indexes its own generator under 'Pyromagnetic Generators', and the page number it gives - 429 - is set on a separate OCR line, so quote the entry without the number and cite the index leaf; the joined string comes back fuzzy. Article 08's pin records the same behaviour for its index lines
- check_quotes.py: exact match, ratio 1.0
- raw OCR: `...etic Motors 424 Physiological Effects of High Thomson, J. J., on Vacuum Frequency 162, 394 Tubes 397,402, 406 Polyphase Systems 26 Polyphase Transformer 109 j Thomson, Sir W., Current Accumulator 471 Pyromagnetic Generators 429 Transformers : Regulator for Rotary Current Motors 45 Alternating 7' Magnetic Shield 113 Resonance, Electric, Phenomena of 340 Polyphase, 109 Rotating Field 9 ' ' Resultant Attraction " 7 Rotatin...`

### 2. The table (the index entry for the other half of the chapter)

> "Thermo-Magnetic Motors"

- cited as: `(1894, p. 496)`
- why: the index line for the 'motors' half of ch. XXXVI's title, pointing at printed p. 424. Note the annotation this row carries: the same words also occur on printed p. 6 inside the editor's inventory, so cite p. 496 for the index and p. 6 for the inventory, never one cite for both
- check_quotes.py: exact match, ratio 1.0 (the same words also occur on printed pp. 6; cite the pinned page)
- raw OCR: `...Production of 171 Telegraphy without Wires. . . . 346 Phenomena Produced by Electrostatic Force 319 Transformer with Shield between Primary and SecondPhosphorescence and Sulphide of Zinc 367 ary 113 Thermo-Magnetic Motors 424 Physiological Effects of High Thomson, J. J., on Vacuum Frequency 162, 394 Tubes 397,402, 406 Polyphase Systems 26 Polyphase Transformer 109 j Thomson, Sir W., Current Accumulator 471 Pyromagneti...`

## Rejected: considered and not carried forward

(Numbered, because 'Rejected #N' is cited from the rows above and the numbers are the order of the REJECTED list in `gen_quotes.py`; nothing renumbers them.)

1. ~~"Entered according to Act of Congress in the year 1893 by T. C. MARTIN in the office of the Librarian of Congress at Washington"~~ (p. -8): the whole copyright line as one quote: fuzzy 0.849 on printed p. -8. The OCR of the printer's imprint ('Press of Mcllroy & Emmet, 36 Cortlandt St., N. Y.') and the setting of the line break the middle of the run. The two halves verify exactly and are pinned above with the cut. A draft printing the whole line as one quotation fails check_quotes.py in feature-007/t3
2. ~~"the most inefficient machine ever invented!"~~ (p. 236): the form with the exclamation mark. The print sets a space before it - 'ever invented !' - and the normaliser keeps that space, so the glued form is not in the run. The pinned quote stops at 'invented'; if the draft wants the mark, put it outside the quotation marks, as article 08's pin did for the p. 258 question mark the scan reads as '{'
3. ~~"We are whirling through endless space"~~ (p. 196): Appendix A's first fragment for the pp. 196-197 row, and the form the series would most naturally copy. NO MATCH at all, exact or fuzzy: the scan sets the line as 'AVe are whirling through' - a capital W at the start of a line OCRs as 'AVe'. Nothing in the volume contains 'we are whirling'. The form that verifies starts at 'whirling through endless space' and is pinned above. This is the most important row in this file for feature-007/t1: the quote the plan's own appendix gives cannot be printed as given
4. ~~"under certain conditions it may be more economical to supply the electrical energy with one lead than with two"~~ (p. 137): the compiler's practical conclusion in full: fuzzy 0.982 on p. 137, because the print's word is 'witli', an OCR l-for-i in 'with' that no normaliser folds. The first half is pinned above; the conclusion can be paraphrased with the page cite, or dropped. Do not print this as a quotation
5. ~~"a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size"~~ (p. 138): the fuller apparatus description: fuzzy, because the run crosses a line break the OCR breaks. The short form is pinned above and is enough
6. ~~"we are finally led to recognize, that since time immemorial we have, after all, always had "electric light and heat" at our disposal"~~ (p. 167): the full joke. It verifies through the space-ignoring index, but the print sets 'electric light and heat' in its own double quote marks, and check_quotes.py's scanner pairs quote marks by walking them: a draft quotation containing the print's own quotation marks is the case it gets wrong (article 08's pin hit this with the editor's ' Miscellaneous ' and started its quote after it). The pinned form stops at 'had'; paraphrase the phrase and cite p. 167
7. ~~"The same operation may be repeated indefinitely"~~ (p. 430): the run as one fragment. 'The same operation may be' is the last line of printed p. 429 and 'repeated indefinitely' opens p. 430, so the joined string is not a run on the page this quote would be pinned to. The p. 430 half is pinned above. A hyphenated citation '(1894, pp. 429-430)' is never the answer: check_quotes.py's citation regex cannot read a range
8. ~~"as a "patent medicine" man"~~ (p. 394): the phrase verifies exactly on printed p. 394 - the print sets it in double quotes - but it is only 19 characters, and inside a draft quotation the print's own marks break check_quotes.py's pairing the way the p. 167 case does. The two pinned p. 394 fragments carry the beat without it. If the draft wants the phrase it must be the whole quoted run, with the print's marks inside, and that run must be tested with check_quotes.py before it ships, not assumed
9. ~~"No electrical inventor of the present day dealing with the problems of light and power considers that he has done himself or his opportunities justice until he has attacked the subject of thermo-magnetism"~~ (p. 424): the most quotable line in ch. XXXVI: fuzzy 0.966 on p. 424 because the OCR sets the last word as 'thermo-magiietism' (ii for an). The rest of the sentence is fine; the last word is not. Stopping at 'the subject of' leaves nothing, so paraphrase. The pinned p. 424 rows use the sentences that do verify
10. ~~"MOTORS AND PYRO-MAGNETIC GENERATORS"~~ (p. 424): the chapter heading, which is the fifth 'magnetic generator' hit and the reason Appendix D's count is 5 and not 4. It is NOT in the index check_quotes.py builds: strip_furniture drops short all-caps lines as running heads, and the heading is set on four short display lines ('CHAPTEK / THERMO-MAGNETIC / XXXVI. / MOTORS AND PYRO-MAGNETIC GENERATORS.'). With load_pages(clean=False) the same string is 1 hit at ratio 1.0 on printed p. 424. So the heading can be named and cited, and cannot be printed inside quotation marks with a page cite. The contents leaf gives the same title truncated by the OCR to 'PYRO-MAGNETIC RATORS' (scan file 17) - article 08's pin records that too. See the flag THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE
11. ~~"THE INVENTIONS RESEARCHES AND WRITINGS OF NIKOLA TESLA"~~ (p. -9): the title page. Not in the index at all, for the same furniture reason: the title page is display type and the OCR interleaves it ('THE INVENTIONS RESEARCHES AND WRITINGS OF NIKOLA TESLA WITH SPECIAL REFERENCE CURRENTS AND TO HIGH HIS WORK POTENTIAL IN POLYPHASE LIGHTING'). The title page is scan file 9, printed leaf -9, and it is what the article means by 'the 1894 first edition'; it can be described and shown as a page-scan crop (brief 10 asks for the title page), but it cannot be quoted with a page cite. The copyright leaf, scan file 10, is prose and is pinned above in two verified halves
12. ~~"D. VAN NOSTRAND COMPANY, NEW YORK"~~ (p. -9): the publisher's line on the same title page. Same reason: display type, not in the index. The publisher belongs in the Sources block, which is where section 3 puts the full citation anyway
13. ~~"attach their machinery to the very wheelwork of nature"~~ (p. 236): the form in section 9 brief 10 item 3 AND the example command in section 8 step 2 of the runbook. The print says 'attaching', so this string is fuzzy 0.964 on p. 236 and check_quotes.py will call it NOT VERBATIM. The pinned form is 'in attaching their machinery to the very wheelwork of nature'. Read this row before writing the article's most important sentence
14. ~~"Throughout space there is energy ... the most inefficient machine ever invented!"~~ (p. 236): the brief's ellipsised form as one quote. The first fragment verifies, the second does not (Rejected #2), and the cut hides the three sentences that make the passage a warning. The pin gives the passage in five verified pieces instead. If the draft wants one long quotation it must be the one pinned at the head of section 3, with the efficiency sentence as a second quotation
15. ~~"the true electric flame"~~ (p. 121): article 06's pinned phrase, on the same subject in the same volume. Not re-pinned here: article 06 (tesla-cold-flame.html) is rendered and owns that beat, including the p. 166-171 brush passages. Article 10's flame paragraph is one paragraph of context and a link to 06, not a second telling of it. See the flag THIS BEAT IS ALREADY ANOTHER ARTICLE'S
16. ~~"it is better to employ one wire than two. Therefore, if motors, lamps"~~ (p. 267): a stitched form crossing the sentence boundary the print puts between them. Both halves are pinned separately above; stitching them into one quotation would be re-punctuating the 1894 text inside quotation marks, which section 3 forbids
17. ~~"it is only necessary to raise the temperature of iron at the proper place and at the proper time"~~ (p. 429): the chapter's own summary of the whole device, and its most quotable sentence. NO MATCH on p. 429: the OCR sets 'it is only necessary to raise the temperature of iron at the proper place and at the proper time' across a line break as 'it is only necessary to raise the temperature of iron at the proper place and at the proper time' with a hyphenated line ending, and the run as typed does not appear. The chapter's own words are recoverable from the pinned law-one and law-two rows, which do verify; paraphrase this one and cite p. 429
18. ~~"magnetic motor"~~ (not in this volume as a phrase): the phrase the site's product vocabulary would like the book to contain. It is never there unqualified: 3 raw hits (6, 46, 496), 4 on the GATE index (6, 46, 55, 496), 5 with --keep-furniture (-1, 6, 46, 55, 496). Every one sits inside a hyphenated compound - 'thermo-magnetic motor(s)' at the contents leaf, in the editor's inventory at printed p. 6 and in the volume's index at p. 496 - or inside 'electro-magnetic motor' at printed pp. 46 and 55, and the p. 46 line is OCR-garbled ('an ordinary form of electroof source magnetic motor'), so not one of them can be quoted. The p. 55 hit exists only on the normalised indices: the print hyphenates 'electro-' at the line break, the normaliser folds it, and the raw text never sets the phrase. So the article may say the volume never writes 'magnetic motor' unqualified, and must not imply the words never appear. Measured in the count table above
19. ~~"magnet motor"~~ (not in this volume as a phrase): the site's other product phrase. 0 hits on all three indices; `grep_quote.py --count` prints 18 anyway, every one of them the tool's fuzzy fallback clearing its 0.80 floor on unrelated windows - ratios 0.8 to 0.923, and the best of them, 0.923, sits on printed p. 46: '…te an ordinary form of electroof source magnetic motor provided with an armature…'. A zero that prints as 18 is the trap this article's table walks into, so it is recorded here and in the flag HOW TO READ A COUNT
20. ~~"magnetic engine"~~ (not in this volume as a phrase): a phrase a reader might expect in an 1894 book. 0 hits on all three indices; the tool prints 7 fuzzy, ratios 0.8 to 0.875. Not quotable, not countable, and worth one clause in the method section because it shows what a fuzzy count is
21. ~~"free electricity"~~ (not in this volume as a phrase): the site's phrase and one of the live pages' titles. 0 hits on all three indices, and the tool prints 0 too - the one zero in this table that survives the fuzzy fallback. Pinned as a count, not a quote: the method table can show it, and the article may say the phrase is not in the book
22. ~~"free"~~ (not in this volume as a phrase): the word alone: 97 raw hits, of which 49 are the standalone word, in the forms 'free' 49, 'freely' 36, 'freedom' 11, 'freed' 1 - and not one of them is followed by 'energy': 'free energy', 'free-energy' and 'free energ' are 0 on all three indices. 'free end', 'free circuit', 'free space', 'free conductor', 'free from'. A reader who searches the word will find it 97 times and find the phrase never. This is the row that makes the method section worth writing at all, and it is why the article's table must give the phrase, not the word
23. ~~"unity"~~ (not in this volume as a phrase): what a reader searching 'over unity' by halves finds: 9 raw hits, and 0 of them is the word 'unity' - all 9 sit inside longer words, which the host-word list gives exactly: community, impunity, opportunity. 'over unity' and 'over-unity' are 0 on all three indices, and the tool still prints 4 fuzzy hits for 'over unity' at ratios 0.8 to 0.824. The measured version of section 4.1's rule about not implying the words exist
24. ~~"the earth's potential"~~ (not in this volume as a phrase): the phrase the p. 138 beat is about, and it IS in the book: 1 raw hit, on printed p. 138 ('rapid variations of the earth's potential were produced'), and the same count on the normalised indices. What is NOT in the book is the series' own hyphenated label: 'earth-potential' is 0 hits. The first draft of this row had those two the other way round and blamed a curly apostrophe the text does not contain - the scan sets a straight one, and the phrase verifies on every index. The article may quote the book's phrase with the p. 138 cite; if it writes 'earth-potential' it has to be plain that this is the series' word for it, which section 4.1 requires
25. ~~"earth-potential"~~ (not in this volume as a phrase): 0 hits in the volume. The word in brief 10 item 4 and in this pin's section names is the series' label, not the book's. Flagged in WHICH PAGES ARE TESLA WRITING and in the section 4.1 note
26. ~~"free-energy"~~ (not in this volume as a phrase): the hyphenated form, which the series' own prose uses constantly (10 hyphenated and 13 spaced occurrences in SERIES-PLAN-1894.md itself). 0 hits in the 1894 text, hyphenated or not. The article's own vocabulary is not the book's, and section 4.1's rule about not implying the words exist applies to the article's headings too

## Flags for the writer (§3 quote style, §4.1 guardrail, feature-007/t1)

- **THE RUNBOOK'S OWN EXAMPLE COMMAND MISQUOTES THE PRINT** — section 8 step 2 of SERIES-PLAN-1894.md tells the quote-pin agent to run python3 books/tools/grep_quote.py "attach their machinery to the very wheelwork" --pages. The print says 'attaching', so that command returns a fuzzy near-match and no exact hit, and an agent that follows the runbook literally will pin a quote the gate rejects. The verified form is in section 3 of this pin. Nothing in the runbook or the plan needs changing - the runbook is a runbook - but the article's central sentence must be pinned from this file, not from the plan's example
- **THE OCR BREAKS THE ONE SENTENCE APPENDIX A QUOTES** — Appendix A's pp. 196-197 row gives 'We are whirling through endless space, with an inconceivable speed...'. The scan sets the line at the foot of printed p. 196 as 'AVe are whirling through', so no index of this OCR file contains 'we are whirling' and the fragment cannot be printed as the plan gives it. Two consequences for feature-007/t1: quote the run from 'whirling through endless space' and cite p. 197, and do not describe the sentence as beginning on p. 196 in a way that implies the words 'We are' were checked. If the series ever wants to print the sentence complete, it has to say the scan is unreadable at that point, which is a sentence about the source, not about Tesla
- **THE CHAPTER TITLE IS THE FIFTH HIT AND IT IS NOT QUOTABLE** — Appendix D counts 5 'magnetic generator' hits: printed pp. 6, 424, 429 twice, 496. The p. 424 hit is chapter XXXVI's display heading, which the GATE index does not contain (strip_furniture drops short all-caps lines as running heads), and which the KEEP index does. So the same fact prints as 5 or as 4 depending on the index. Article 08's pin records the same split - it counts 4 through grep_quote.py's default index, names pp. 6, 429 and 496, and says Appendix D's 5 is right because the fifth is the heading, present with --keep-furniture. The two pins must not appear to disagree: article 10 owns this table, so it prints 5, names the heading, and says which index produces 4. Article 08's page is rendered and feature-007/t3 must not edit it; if the two pages would visibly disagree, fix the wording on article 10's side and raise the article 08 change separately (section 5 says a rendered page is frozen).
- **THE CLI AND THE GATE SHARE AN INDEX BY DEFAULT; --keep-furniture IS THE DIFFERENCE** — The first version of this flag said grep_quote.py builds its index with load_pages(clean=False) and check_quotes.py with load_pages(clean=True), and built a method section on the difference between them. That is backwards about the CLI: grep_quote.py's default is clean=True - the same index check_quotes.py builds - and clean=False is what the --keep-furniture switch asks for. Verified on the date above: `grep_quote.py "magnetic generator" --count` prints 4 hits at pp. 6, 429, 496, and the same command with --keep-furniture prints 5 and adds p. 424. So the CLI's default count and the gate's count are one number, and a writer who runs the tool without a flag is looking at the index the gate will use. What is still true, and is the reason the flag stays: furniture changes which strings exist at all (the chapter heading, the title page), and the tool's fuzzy fallback can call a near-match 'found' where check_quotes.py would fail the quote. Every number in this pin is labelled with the index that produced it. Do not quote a tool result in the draft without re-running it through check_quotes.py first
- **HOW TO READ A COUNT** — grep_quote.py --count falls back to a fuzzy match at a 0.80 ratio floor, so a term that is not in the book at all can print a non-zero count: 'magnet motor' is 0 on all three indices and the tool prints 18 (ratios 0.8 to 0.923); 'over unity' is 0 and it prints 4 (0.8 to 0.824); 'magnetic engine' is 0 and it prints 7 (0.8 to 0.875); 'free electricity' is 0 and it prints 0. The article's table is built entirely from terms where this matters, so the draft must print the counts this script measures (raw substring counts and exact-index counts) and never a tool's --count output. If the draft says 'zero', it must be a zero that survives the fuzzy fallback, and the method section should say in one sentence that a search tool can report hits for words that are not there - that is the most useful thing a reader could take from this article
- **THE PYROMAGNETIC FIGURE IS THE ONLY ONE BRIEF 10 NAMES, AND IT IS THE WRONG FIGURE FOR THE JOB** — brief 10's figure list asks for 'tesla1894-p424-fig* (pyromagnetic)'. Printed p. 424 has no engraving at all - the chapter opens with prose and footnotes, and its plates are on printed pp. 425-430 - so there is no file that matches that glob. The crop of the machine itself is tesla1894-p430-fig242.webp - printed p. 430, scan file 448, book fig. 242, verified:true in new_content/1894-series/index.json - which article 08 already publishes as its figure 3. Section 6.6 forbids the same engraving on two pages unless the caption differs. Either article 10 uses that plate with a caption about the fire and the boiler, which is a different point from article 08's, or it uses the page-scan crop of p. 236 that brief 10 also asks for, which does not exist yet and has to be cut. Fig. 243 has no clean crop - only the superseded two-figure band tesla1894-p448-fig1-fig243.webp. See the figure notes below
- **THE 400-500 SENTENCE IS ONE ARTICLE'S CLOSING BEAT AND THE OTHER'S OPENING** — article 08's entry 4 ends on the spirit-lamp footnote, and its pin records that footnote as showing the apparatus is 'a demonstration, not the chapter's machine'; brief 10 item 5 opens article 10's pyromagnetic section with the same footnote. Both articles may quote it - it is the only number in the chapter - but they must not both present it the same way. Article 08 has it as the proof that the book reports no test. Article 10's use has to be different: the number is a vibration rate heard in an interview, and the internet repeats it as a machine's rating. If the overlap feels like duplication, article 10 should cut its own quotation and link to article 08, which is what section 5's link map is for
- **THE CHAPTER'S OWN VERDICTS, IN ORDER** — the volume prints three judgements about this chapter's subject, about three different things, and the article must not merge them into one sentence about 'the book's opinion'. In the order they are printed: (1) printed p. 424, first paragraph, about the FIELD - 'the influence of heat on the magnetic metals has been investigated frequently, though not with any material or practical result'; (2) the same page, about TESLA'S ATTENTION - 'though he has but glanced at them, it is to be hoped he may find time to pursue the study deeper and further', which is the compiler wishing a busy man more time, not grading his machine; (3) printed p. 429, in the footnote, about the APPROACH - he 'attacked this problem in a way which was, from the standpoint of theory, and that of an engineer, far better than that from which some earlier trials in this direction started', praise of a starting point that says nothing about output. All three are the compiler's, in the third person, inside Part III; article 08's flag PART III IS THE EDITOR'S TEXT, IN THE THIRD PERSON, ABOUT TESLA'S DEVICES says who is writing, and article 10 has to keep that attribution inside every one of the three. None of them is a verdict on the machine's performance, and none supports 'the book called it a failure': the chapter's last sentence (printed p. 431) is about what could be regulated, and the finding is that no measurement is reported, which is not the same as a negative one
- **THE EFFICIENCY RECORD BELONGS TO ARTICLE 07** — Appendix D gives the p. 8 efficiency record to article 07, which is rendered and printed the 50/60 and 94-95 per cent figures. Brief 10 item 7 does NOT ask for the book's efficiencies - it asks for 'what actually works off-grid, what the plans on this site are and are not' and names three commercial pages. The p. 8 rows in this pin are this pin's own support for that beat: a measured, cited, sub-unity number is the counter-evidence to the premise of the myth, and it is the book's own answer to 'did his machines work'. Article 10 may cite the record and quote at most one short fragment of it, with a link to article 07; it must not re-tell the Anthony test. The sentence that is genuinely article 10's is the compiler's reason for printing the figures - 'cited to show that the efficiency of the system has not had to wait ... for any demonstration of its commercial usefulness' - because that is about what the book chose to measure, which is this article's subject
- **THIS BEAT IS ALREADY ANOTHER ARTICLE'S** — the flame-without-combustion beat (brief 10 item 4, p. 167) is article 06's subject: tesla-cold-flame.html is rendered and its pin carries pp. 120-121, 166-171, including 'the true electric flame' and the p. 166-167 brush sentences. Article 10's flame entry is one paragraph in a list of things he did claim, and it must link to article 06 rather than re-open the argument. The p. 166 'veritable flames, for they are hot' and the p. 167 'would give light and heat without any material being consumed' rows are pinned here because brief 10 names those pages; if the draft finds itself writing more than a paragraph about flames, it has taken over article 06's job
- **WHICH PAGES ARE TESLA WRITING** — brief 10's beats mix three different texts and the draft must not print 'Tesla wrote' for all of them. Ch. I (pp. 3-16) is the editor's introduction. Ch. XXV (pp. 119-144) is the compiler's running review of the lectures - the p. 137 and p. 138 earth-potential passages are in it, and the compiler's own footnotes say so. Chs. XXVI (from p. 145) and XXVII (from p. 198) are the printed texts of two lectures, May 1891 and February 1892, and the pp. 196-197, 232, 236, 267 passages are in those. Ch. XXXVI (pp. 424-431) is the compiler's chapter on a device, with footnotes the compiler says came from an interview. Ch. XXXI (p. 394) is Tesla's own paper. Ch. I p. 8 is the editor's. The p. 429 'pyromagnetic generator' sentence is the compiler's; so is the second hit on the same page. The pin marks each row's voice in its section name and its why
- **FOUR TEXTS, FOUR DATES** — the volume's own dates: entered at the Library of Congress 1893 (copyright leaf), title page 1894, the Columbia lecture May 20 1891 (p. 145), the IEE London lecture February 1892 (p. 198), the Anthony efficiency test May 1888 (p. 8). Section 3's quote style prints 'Tesla wrote in 1892', which is only right for the IEE lecture. The draft must date each quote from this list or not date it at all
- **THE FLAME PASSAGE STRADDLES A PAGE BREAK** — brief 10 names p. 167 for the flame claim, but 'they are veritable flames, for they are hot' is on printed p. 166 and the sentence that continues onto p. 167 begins 'we have a possible way of producing'. Each fragment is pinned to the page it sits on. A draft that cites p. 167 for the p. 166 sentence fails check_quotes.py, and a draft that cites 'pp. 166-167' for either fails too, because the citation regex cannot read a range
- **THE PATENT-MEDICINE SENTENCE IS NOT ABOUT FREE ENERGY** — the p. 394 'patent medicine' passage is Tesla rejecting being advertised as a cure-all, in a paper on electrotherapy. It is the only place in the volume where Tesla complains about being sold, and it is tempting as a closer for an article about free-energy claims being made in his name. It is not that: it is about medical advertising, and section 4.1 forbids carrying a quote past what its page supports. Use it as his general position on electrical hype, in one or two sentences, with the subject named, or not at all
- **THE BEAUTY-WITHOUT-UTILITY LINE IS HALF A SENTENCE** — 'An invention is none the less beautiful because it may lack utility' is the compiler's most quotable line and it is the opposite of what it looks like: the sentence goes on to say this inventor's ideas 'are fraught with substantial benefits to the public'. Quoting the first clause as the book's view of failed machines would be a misreading of the p. 8 paragraph, and it would be the article's own thesis talking through Tesla's editor. Print the turn or cut the line
- **THE WORD 'TEST' IS THE WHOLE ARGUMENT AND THE COUNTS ARE IN THIS FILE** — brief 10 item 5 asks whether the chapter gives a test, a figure, a trial run. The scoped counts over printed pp. 424-431, and every non-zero hit with the sentence it sits in, are in the section 'What chapter XXXVI does and does not report' above, and the answer is a real number, not a hunch: 'test' 0, 'per cent' 0, 'efficiency' 0, 'output' 1 and that one is a design property with no number on it. Read the two non-zeros before writing the beat: 'experiment' is 3 and 'result' is 5 in that range, and they are the compiler's horseshoe-magnet footnote, the chapter's own illustration on p. 429, and the word 'result' inside ordinary sentences - so the draft may NOT write that the chapter mentions no experiments or no results. What it may write, and what the book says itself at printed p. 424, is that this line of work 'has been investigated frequently, though not with any material or practical result', and that the chapter reports a design and an illustration and no measurement of the machine. Article 08's pin records the same finding in other words - 'no output, no efficiency, no run, no trial, no commercial result anywhere in pp. 424-431' - and article 10 must not contradict it or make it stronger: 'it failed' is not available (section 4.1)
- **THE LIVE PAGES SAY MORE THAN THE 1894 TEXT CAN SUPPORT** — the three pages brief 10 item 7 links to make the claims printed, verbatim and measured, in the section 'What the three live pages actually claim' above - a 5x energy figure, a patent attribution to an 1894 bifilar coil, a 30-50 percent bill reduction, a perpetual-motion generator. None of those words is in the 1894 book: 'bifilar', '512,340', 'coil for electromagnets', 'free energy', 'perpetual' and 'over unity' are all 0 hits, measured. Article 10's job is to report what the book does and does not say about the devices the site sells, and it must not launder a live page's claim into a historical one by quoting the book next to it. The one live-page claim the 1894 text can actually meet is the p. 429 'pyromagnetic generator' phrase, and even that is a heat engine
- **THE WORD-SEARCH PAGE DOES NOT EXIST YET** — brief 10's closing beat and section 5.2 row 10 both link to tesla-1894-word-search.html, which is feature-008/t2 and still pending. Article 10's table is the same measurement that page will publish, so the link is required by the brief and cannot be checked until feature-008/t2 renders. Do not invent a different target and do not drop the link: note it in the draft's Sources block as pending, and let feature-008/t3's check_quotes run be the moment the link is verified. Articles 05 and 08 likewise have deferred out-links to article 10 (section 5.2 rows 5 and 8), which feature-007/t3 may add but must not assume

## Notes for the figure task (feature-007/t2)

- BRIEF 10'S FIGURE LIST IS WRONG ON ONE ITEM AND MISSING ON TWO. It asks for 'page-scan crop of p. 236 (the radiometer passage), tesla1894-p424-fig* (pyromagnetic), title page'. Printed p. 424 carries no engraving at all - chapter XXXVI opens with prose and footnotes, and its plates are on printed pp. 425-430. The p. 236 crop does not exist yet. The title-page crop does exist, website/assets/tesla1894/scan-title-page.webp, and the hub page 00 already uses it as its card image (new_content/1894-series/index.json, figures[0], verified:false). So of the three named items, one is mis-numbered, one must be cut, and one is already used elsewhere.
- THE CROP THAT MATTERS IS THE PAGE SCAN OF P. 236, AND §6.6 SOURCING ORDER 4 IS THE RULE THAT ALLOWS IT. §6.6 lists 'Page-scan crop of the 1894 page itself when the words are the artefact (used in 05 p. 394 and 10 p. 236)' - the plan already named this crop for this article. There is no engraving on printed p. 236 and none in the surrounding pages that belongs to the passage: the nearest crops in website/assets/tesla1894/manifest.csv are p252-fig1.webp (printed p. 234, a make-and-break apparatus, a dark plate whose QC note says the text is legible only after -negate -auto-level) and p261-fig1-fig147.webp (printed p. 243, an incandescent-lamp figure). Neither has anything to do with the wheelwork sentence. Cut the crop from books/pdf-pages-tesla-1894/page-254.pdf (printed 236 = scan file 254, verified present) following the scan-p346-detail.webp precedent recorded in index.json line 479: 250 ppi, about 821x1073, kept inside the 400 KB article gate. Name it scan-p236.webp, the convention the two existing page-scan crops use (scan-p486.webp, scan-p346-detail.webp - printed page, not scan file). Caption it as the page the passage is on, and say what the reader can see: the running head, the printed folio 236, and the paragraph that ends in the efficiency sentence. The crop is the article's best figure because the article's claim is about words on a page.
- WHAT THE P. 236 CROP MUST BE CHECKED AGAINST BEFORE IT IS USED. The crop will be read against the six p. 236 quotes in this pin, the way article 03's scan-p486.webp was checked against its six p. 486 quotes (index.json line 62: 'Ch. XLIII head + printed 486 visible; the six p.486 quotes match the page image'). Two things to confirm visually: that the printed folio 236 is inside the crop, and that the print really does say 'attaching' where the OCR index says 'attaching' and the plan's brief says 'attach'. The second is the whole point of the article's central quote and a page image settles it in a way no index can. Record the reading in the frontmatter per feature-007/t2's criteria, not in books/tmp/.
- THE PYROMAGNETIC CHAPTER HAS CROPS ON DISK AND ONLY ONE IS CLEAN AND UNCLAIMED. 5 files in website/assets/tesla1894/ resolve to a printed page in 424-431, measured from the directory and both manifests on the date above: p430-fig242.webp (printed p. 430; named by printed page; re-crop, manifest_qc.csv only); p443-fig1-fig281.webp (printed p. 425; named by scan file; extractor crop, manifest.csv row 443->425); p444-fig1-fig235.webp (printed p. 426; named by scan file; extractor crop, manifest.csv row 444->426); p445-fig1-fig287.webp (printed p. 427; named by scan file; extractor crop, manifest.csv row 445->427); p448-fig1-fig243.webp (printed p. 430; named by scan file; extractor crop, manifest.csv row 448->430). The extractor rows are named by scan file and their printed page comes from the manifest; the one re-crop is named by printed page, which is why counting one manifest and listing the other gets the number wrong both ways. Fig. 242 is the pyromagnetic generator itself - a tube bundle standing in a firebox with a fire drawn under it and a boiler above - and §6.6 forbids the same engraving on two pages unless the caption differs. Article 08's caption names the machine as the thing the phrase is attached to; article 10's point about the same plate is the fire and the boiler, which is a different caption for a different argument. That is allowed by §6.6 but it is thin twice, and the alternative - the p. 426 plate, which shows the thermo-magnetic motor half of the chapter and is not used by any rendered page - is cleaner. Decide at feature-007/t2 with the render open, not from the manifest.
- DO NOT TRUST THE FIGURE NUMBER IN THE MANIFEST FOR THE p. 425 PLATE, AND THE QC ROW SAYS SO ITSELF. manifest_qc.csv on p443-fig1-fig281.webp: 'Figure number 281 is genuine for p.425. NOT SETTLED, marked 2026-10-17 (feature-006/t2). The text layer of printed p.425 sets three printed captions, FIG. 231., FIG. 232. and FIG. 233., while the body line on that same page reads In Fig. 281 the permanent magnet N is connected with a frame ... the same scan misreads 3 as 8 twice nearby'. §6.6 says read the figure number off the printed page in the scan. If article 10 uses that plate it must read the caption at 500 ppi first and caption it by what the plate shows, not by a number from the CSV. The same warning applies to p445-fig1-fig287.webp, whose caption spans two figure numbers.
- THE TITLE PAGE IS ALREADY THE HUB'S CARD IMAGE. scan-title-page.webp is front-matter scan file 9 and index.json marks it verified:false. Brief 10 asks for it as article 10's provenance figure. Reusing it needs a different caption (§6.6), and the honest one for article 10 is the imprint - 'entered according to Act of Congress, 1893; title page 1894' - which is a different point from the hub's. If feature-007/t2 does re-open it, the reading has to be recorded and the verified flag set, because the hub's entry is still false. A cheaper option: the copyright leaf, scan file 10, which is prose and is the page the two pinned provenance quotes come from; it has never been cropped and nothing else uses it.
- TWO FIGURES MINIMUM, THREE MAXIMUM, AND THE MIDDLE ONE IS THE HARDEST. §6.6 wants 2-3 body images, figure 1 within the first three H2s, figure 2 mid-article, figure 3 near the close. For this article the natural set is: (1) the p. 236 page scan in the section that quotes the sentence, (2) a pyromagnetic chapter plate in the pyromagnetic section, (3) optionally the title page or copyright leaf in the method section. The word-search table itself needs no figure - it is a table, and a screenshot of a terminal would be the thin option §6.6 rules out.

## Links (§5.2 row 10, for feature-007/t1 and t3)

- OUT-LINKS REQUIRED BY §5.2 ROW 10: magnetic-generator-scam.html, tesla-magnetic-generator-worth-it.html, free-electricity-from-magnets.html, 05 (tesla-high-frequency-massage.html), 08 (tesla-weird-inventions-1894.html). All five exist. qa_page.py needs >= 4 internal links (SERIES-PLAN-1894.md line 1134), so the five named targets are enough on their own.
- THE WORD-SEARCH LINK IS REQUIRED AND CANNOT RESOLVE YET. feature-007's own criteria say 'it links to tesla-1894-word-search.html and to 05 and 08 per §5.2, and those links resolve', and §9 brief 10 item 8 asks for 'a link to the appendix page that proves the word search (Tier 6)'. That page is feature-008/t2 and is still pending, and no file website/tesla-1894-word-search.html exists. Two consequences: the draft must carry the link (do not substitute the hub or the plates page), and feature-007/t3's qa_page run will fail on it unless feature-008/t2 has landed first. This is the one cross-feature dependency in this article and it is worth raising at feature-007/t1 rather than discovering at t3. The table in this pin is the same measurement that page will publish, so whoever writes feature-008/t2 should be handed this file.
- IN-LINKS THIS PAGE NEEDS, AND WHO OWES THEM. §5.2 row 10 says article 10 must be linked from 04, 05, 08, the hub and magnetic-generator-scam.html. Checked on 2026-10-17: the hub's article.md already links it twice (new_content/1894-series/00-hub/article.md lines 36 and 101); 05's article.md line 49 says its third out-link is to this page and is NOT placed because this page does not exist yet - 'that third target is NOT deferred by choice', it writes, because linking it now would fail qa_page.py's dead-link gate at t3; 08's article.md line 416 says the same about its closer. Nothing in website/ links to tesla-free-energy-what-he-said.html yet - grep over website/ returns nothing. Article 04's §5.2 out-link list does not include 10 even though row 10 lists 04 as a required in-link; that is a plan inconsistency, not something feature-007 can fix by itself.
- THE RECIPROCAL COUNT IS THE GATE, NOT THE OUT-LINK COUNT. qa_page.py wants >= 4 internal links with >= 3 of them to pages that link back. Article 10's five §5.2 targets give the four; the reciprocals available are 05, 08 and magnetic-generator-scam.html, and none of the three currently links here. 05 and 08 have the deferred link written into their own article.md as a promise to this page, so the reciprocals arrive when those deferred links are placed - which is a08-wirecommit's and 05's wiring, not feature-007's. feature-007/t3 must check the count, not assume it; if it is short, the fix is to place the deferred links, which is allowed, and not to add links the plan does not list.
- LINK THE FLAME SENTENCE TO 06 AND THE MOTOR SENTENCE TO 07, EVEN THOUGH §5.2 does not ask for them. The p. 166-167 flame beat is article 06's subject and the p. 138 rotating-field motor is article 07's; both articles are rendered. §5.2 row 10 does not list 06 or 07 as out-links, and adding links beyond the map is allowed by the >= 4 rule but changes the reciprocal arithmetic. The cheaper move is to name those pages in prose without a link, or to link and accept that the reciprocal count then depends on 05/08/09 wiring. Decide at t1 with the reciprocal count in front of you, and record the choice in index.json the way 08's article.md recorded its deferred link.
- THE THREE COMMERCIAL PAGES ARE THE POINT OF THE ARTICLE, NOT A FOOTER. Brief 10 item 7 is 'what actually works off-grid, what the plans on this site are and are not', and the three links go in that section, adjacent to the paragraphs that read their claims. §4.1's guardrail is the constraint: no sentence may claim anything about what the product can do that is not already on a live page. The section 'What the three live pages actually claim' above prints, verbatim and measured, what those pages do claim, so the draft can stay inside them.
- ONE OF THE THREE PAGES MAY BE ABOUT TO CHANGE. §9 brief 10's header says 'Slot depends on O2 ... If O2 = C, this brief becomes a rewrite of magnetic-generator-scam.html instead, and the data itself moves to tesla-1894-word-search.html'. The feature record settles it: feature-007 is 'Article 10 ... (O2 = B)', and t1 asks for the softer title 'What Tesla Actually Wrote About Free Energy' (43 chars), published after 03/01/07. So magnetic-generator-scam.html stays a separate live page and this article links to it rather than replacing it. If anyone reopens O2, this pin does not change - the quotes and counts are the same evidence either way - but the link map does.

Do not run `check_quotes.py` on this file as a gate. It is built for a draft (`article.md`), and here its scanner reads the apostrophes in the '- why:' annotations and the struck-through Rejected items as quotation marks, so any count it prints for this file is a count of this file's own prose. The gate for a pin file is `gen_quotes.py` itself: it imports the same matcher (`check_quotes.fragments` + `check_quotes.locate` over the index `check_quotes` builds), writes each quote to this file the moment it verifies, and if a quote does not verify it reports the failure and leaves the confirmed quotes on disk marked PARTIAL rather than throwing the run's work away. `check_quotes.py` runs on `article.md` in feature-007/t3.

## How this file checks itself

`gen_quotes.py` re-reads the file it has just assembled and prints the result here, so a claim in this pin is a claim the generator can re-run, not a claim a reader has to trust. Run `python3 gen_quotes.py` in this directory to reproduce every number in the file, including the ones in this section. If any line below says FAIL, the file is still written (so a restart resumes from the confirmed quotes rather than re-pinning them) and the script exits non-zero.

row structure: 72 quote blocks re-parse to 72 `> "` lines, 72 `- cited as:` lines, 72 `- why:` lines and 72 `- check_quotes.py:` annotations - no row is missing one
every `- cited as:` page is the page of the `## Printed p.` heading it sits under: 0 exceptions
no quote is pinned twice: 0 duplicates over 72 quote lines
every 'Rejected #N' reference names a row that exists: 8 distinct references, highest #8, against 26 rows, 0 unresolved
every flag, figure-note, link-note and section name cited in the prose exists in this file: 0 unresolved. 0 of 18 flags are never cited from the prose (none)
every fragment re-grepped through grep_quote.py's own index (load_pages + build_index + find_hits), each restricted to the printed page this file pins it to: 73 fragments - 72 return only exact hits, 1 return a fuzzy window there and verify here through the space-ignoring index check_quotes.py additionally builds, 0 return nothing
  - p. 429 'the magnetic properties of iron or other magn' - best 0.981 on that index
