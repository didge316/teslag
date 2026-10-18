# Article 12 quote pin: tesla-glowing-tubes-vacuum.html

SERIES-PLAN-1894.md §8 step 2, feature-006/t9. Every quote below was re-grepped on 2026-10-18 from `books/extracted/tesla-1894-plain.txt` through the same matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR spacing is ignored) and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). A quote carrying ' ... ' is cut where the scan breaks; each side of the cut is verified separately against the one page the quote is pinned to, which is how check_quotes.py will judge the draft. `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Verified: 115 quotes (118 fragments) across 29 printed pages, 0 failures. Rejected and not carried forward: 35. Flags for the writer: 21. Counted terms: 60 over the whole volume, plus 15 OCR spelling variants of them, and 30 scoped to four ranges. To re-check one quote by hand: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>` - but that tool's `--count` falls back to fuzzy matching and reports hits for words that are not in the book, so a zero it prints is not evidence of absence. Every count in this file comes from one of the three indices defined in THE THREE WAYS TO COUNT and is printed as a number, never described. To regenerate this file: `python3 new_content/1894-series/12-tesla-glowing-tubes-vacuum/gen_quotes.py`. It writes each quote to this file the moment it verifies, so a run that stops part-way leaves a PARTIAL pin naming what is confirmed and what stopped it, rather than nothing.

This article's evidence is a count as much as a quote. Brief 12 asks for a tube that glows with no wires in it, using the words 'vacuum tube', 'capacitor', 'Geissler tube', 'striae' and 'X-rays', and the book answers some of those words and none of the others; item 5 says the internet gets the energy wrong, which is a claim about what the volume never reports. So the vocabulary table and the scoped absence table are evidence here, not commentary, and they are measured three ways on the date above. Read THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO NOT MEAN WHAT THE QUERY MEANS and NO NUMBER IN THIS ARTICLE'S SUBJECT, AND THE ABSENCE IS THE CLAIM before writing either beat.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand Company, New York, title page 1894 (entered at the Library of Congress 1893), archive.org item `inventionsresear00martiala`. Chapter XXXII is four different texts by four different people in nine pages, and the brief's beats mix them without saying so. Read FOUR TEXTS, FOUR VOICES, ONE CHAPTER and TWO THOMSONS IN ONE PARAGRAPH before writing any sentence that begins 'Tesla wrote'.

## Where the pin puts each beat of brief 12

Counted out of the section labels of the pinned rows, not typed. The page list is the printed pages this file pins for that beat; every one of them is re-grepped on its own page in the self-check at the end.

| beat | pinned quotes | printed pages |
|---|---|---|
| 0. Provenance | 9 | 6, 145, 198, 293, 396, 404, 405, 406, 494 |
| 1. The strangest demo | 3 | 288, 289, 290 |
| 2. Why a tube lights with no wires | 15 | 175, 176, 186, 289, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406 |
| 3. Tesla's lamp research | 8 | 6, 177, 214, 253, 254, 255, 405, 494 |
| 4. The vacuum problem | 6 | 175, 177, 288, 398, 402, 403 |
| 5. What the internet gets wrong | 9 | 176, 213, 288, 289, 292, 401, 404, 405, 406 |

## The size of the thing searched

Measured on the date above, so the method sentence in the draft states numbers it can re-run:

- scan page files in books/pdf-pages-tesla-1894: 518
- page markers in tesla-1894-plain.txt: 506
- whitespace words, tesla-1894-plain.txt: 174,169
- whitespace words, tesla-1894-fulltext.txt: 176,810
- words in the search index after furniture stripping: 167,998

The searchable index is smaller than the text file because running heads and bare folios are stripped out of it (§grep_quote.strip_furniture). A draft that prints a word count is describing the book; a draft that prints the index count is describing the search. Say which. The chapter title itself is a special case of the same stripping - read THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE.

## THE THREE WAYS TO COUNT

- **RAW** - case-insensitive substring count over the raw OCR page bodies as they sit on disk, nothing normalised. This is what `grep -io` would give a reader who reproduces the claim by hand.
- **GATE** - the index `books/tools/check_quotes.py` builds, `load_pages(clean=True)`: short all-caps lines and bare folios are dropped as running heads, then the text is lower-cased, a hyphen at a line break is folded, and whitespace is collapsed. This is the index the numeric gate will check the draft against, and the same one `grep_quote.py` builds by default. GATE and the CLI's default count are one number, not two.
- **KEEP** - the same index with `--keep-furniture`, `load_pages(clean=False)`: running heads and page-opening display type kept.

The three indices do not agree, and not on one term: measured on the date above, 12 of the 75 counted terms and spelling variants count differently depending on which is used. Where raw is below the other two, a line break in the print is the cause - the phrase is on the page but the OCR ends a line inside it, and a raw substring count cannot cross a newline. Where gate is below keep, furniture is the cause: the hit is a running head or a display line. A draft that prints one of these numbers has to say which index produced it.

| term | raw | gate | keep |
|---|---|---|---|
| `exhausted tube` | 31 | 32 | 32 |
| `vacuum tube` | 12 | 12 | 15 |
| `luminous` | 99 | 100 | 99 |
| `electric discharge` | 4 | 2 | 5 |
| `electrostatic` | 173 | 170 | 173 |
| `condenser` | 225 | 218 | 225 |
| `experiment` | 429 | 425 | 429 |
| `without wires` | 4 | 5 | 5 |
| `brush` | 261 | 253 | 261 |
| `end of the wire` | 3 | 6 | 6 |
| `induction coil` | 96 | 101 | 101 |
| `Carborundum Button for Tesla Lamps` | 0 | 1 | 1 |

## THE VOCABULARY TABLE (brief 12 items 1, 2, 5)

Hits over the whole volume, with the printed pages each hit sits on. The page list is from the raw index; a count in parentheses means that page carries more than one hit. A zero in the gate column is the evidence for a sentence that says the book does not use a word - and only that, never that the thing does not exist.

| search term | raw | gate | keep | printed pages (raw) | what it is |
|---|---|---|---|---|---|
| `exhausted tube` | 31 | 32 | 32 | 121, 135, 141, 144, 184, 186, 189(2), 190(4), 210, 217, 218, 234, 236, 281, 286(2), 339, 359, 369, 383, 399(2), 401, 402, 404, 405, 406 | the period's ordinary phrase for what the brief calls a 'vacuum tube' / 'Geissler tube'; the phrase the draft should use in quotes, because it is what the book says |
| `vacuum tube` | 12 | 12 | 15 | -2, 210, 218, 279, 286, 287, 369, 372, 396(2), 403, 404 | the modern phrase, and it IS in the book - but as 'a vacuum tube' meaning an exhausted glass envelope, not a valve. Read the flag THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO NOT MEAN WHAT THE QUERY MEANS |
| `Geissler` | 5 | 5 | 5 | 175, 190, 195(2), 384 | brief 12 item 1's word. It is in the book, four times in the 1891 New York lecture and once elsewhere, and never in chapter XXXII |
| `glowing` | 1 | 1 | 1 | 333 | the word in this article's own title. The book does not use it; it says 'luminous', 'luminosity', 'glow'. The title is ours, and the draft must not put the word in quote marks as if it were his |
| `glow` | 36 | 36 | 36 | 120, 123, 129, 145, 218(2), 238(3), 239(2), 250, 251(3), 257, 258, 261, 290, 327, 330(4), 331, 333, 350, 351, 352(2), 399, 400, 402, 403(2), 485 | the noun the book does use, including in the two glow sentences this pin pins (p. 403 Thomson's, p. 400 Tesla's) |
| `purplish` | 4 | 4 | 4 | 129, 218, 400, 403 | the colour word in both of those glow sentences. Counted here because the row that quotes it claims the two occurrences are one in chapter XXXII his and one Thomson's - see the flag THE RING OF LIGHT IS THOMSON'S, THE BROAD GLOW IS TESLA'S |
| `luminous` | 99 | 100 | 99 | 122(2), 128(4), 129(3), 130, 136(2), 137, 141(2), 155, 159, 160(3), 164(2), 168, 175(3), 184, 185, 186, 189(3), 190(2), 201, 202, 214(2), 215(2), 216(3), 217(3), 218, 223(3), 235, 249(2), 252, 256(2), 257, 273, 274(3), 275, 284, 286(3), 295, 349, 350, 354, 357, 359, 369(2), 370(2), 371, 372, 397, 398, 399(5), 400, 401(3), 402(3), 403(2), 404(2), 405, 494, 495 | the book's adjective for what the brief calls 'the glow' |
| `luminosity` | 33 | 33 | 33 | 120(2), 166, 185, 187, 190, 228, 238, 256(2), 285, 295(2), 333, 349, 357, 365, 370, 384, 385, 396, 398, 399(2), 401, 404, 405(3), 406(4) | the book's noun for the effect; chapter XXXII's own first sentence is about it (row 3) |
| `luminescence` | 0 | 0 | 0 | - | not in the volume at all, though it is the period's word in English physics papers; he says 'luminosity' and 'phosphorescence' |
| `phosphorescence` | 68 | 68 | 68 | 140, 141(2), 144, 160, 221, 228, 245, 248, 251, 253, 255(2), 256(2), 257(4), 258, 260(2), 263(3), 270, 271(2), 282(3), 289(2), 291, 345, 349(2), 359, 364(7), 365(4), 366(8), 367(6), 368(2), 495(2), 496 | the word for the light that persists after the excitation stops, and the word the carborundum question turns on |
| `phosphorescent` | 38 | 38 | 38 | 141, 144, 161, 187(2), 200, 236(2), 249, 251(2), 255, 258, 262, 264, 271, 279, 280, 285, 289, 290(2), 314, 359(2), 364, 365(3), 366(3), 367, 368, 401(2), 485(2) | the adjective form, used of the coated bulbs and of the sulphide of zinc experiments |
| `electric discharge` | 4 | 2 | 5 | -2, 396(2), 494 | the chapter's own subject phrase; the volume's index files it as 'Electric Discharges in Vacuum Tubes 396' (row 10) |
| `electrostatic` | 173 | 170 | 173 | -2, 120(7), 121, 122, 129, 130, 131, 132(2), 134, 136(2), 137, 139, 141(4), 142(2), 143(2), 149(4), 151, 167, 174(5), 175(6), 176, 182(2), 184(2), 185, 186(4), 187, 189(6), 190(4), 191, 192(2), 195, 207, 213, 218, 228, 229(3), 230(3), 232, 235(2), 238, 241(3), 242, 274(4), 275(3), 279, 287(6), 288(2), 289(2), 291, 292(2), 311, 318(5), 319, 321, 322, 323(2), 324, 325, 326(2), 327(2), 330(4), 333(3), 346, 364, 368, 369(6), 392, 398(2), 399(3), 400, 401(2), 402(2), 404(4), 405(4), 406(8), 494(3), 496 | the word the whole 1891 argument is about, in both directions; chapter XXVI alone is dense with it |
| `condenser` | 225 | 218 | 225 | -3(2), -2, 6, 7, 101(10), 102(2), 103(4), 104(10), 105(4), 106(7), 108(3), 122(3), 123, 125(5), 126, 127, 128, 130, 132, 135(3), 136(2), 141, 150, 152, 162, 164, 165, 175, 176, 177, 179, 181, 182(2), 183(4), 186, 187, 191(5), 192, 193(4), 202, 203, 204(3), 206(2), 207, 210, 212(2), 213(5), 222(2), 223, 224, 225(4), 226(2), 233, 234, 235, 238, 245(2), 246(4), 261, 264, 265, 267(4), 268(5), 269(2), 273, 274, 279, 286, 292, 304(9), 309(2), 313, 314, 315(2), 316(2), 317, 334, 336(4), 337(2), 338(3), 339, 342(2), 343, 344(3), 345, 347, 350, 351, 352, 377, 382, 383(3), 385, 386(2), 390(5), 391(6), 396, 418(4), 419(6), 485, 488, 492, 494, 495(3) | the component he reasons with, in the period's word; the Leyden-jar and insulated-body argument of chapter XXXII is built on it |
| `condenser action` | 6 | 6 | 6 | 152, 164, 165, 177, 186, 385 | the exact phrase brief 12 item 2 asks for, and the one sentence that uses it as an explanation is in the New York lecture (row 92) |
| `capacitor` | 0 | 0 | 0 | - | brief 12 item 2's word. Not in the volume in any spelling. The physics is his, the word is ours |
| `molecular bombardment` | 15 | 15 | 15 | 121, 139, 151, 160, 178, 182, 245, 253, 254, 291, 327(2), 333, 400, 418 | the mechanism phrase, used by him and by the compiler; the first-person sentences are in chapter XXVI and XXVII |
| `bombard` | 97 | 97 | 97 | 121, 133(2), 139(2), 140(2), 143, 144, 151, 152, 160(4), 161, 176, 178, 182, 195, 223, 231, 232, 240, 241, 242(2), 243, 244, 245, 246, 247(4), 248(3), 249, 252, 253, 254(2), 255, 259, 260(4), 261(2), 266, 271(2), 282, 283, 291, 327(2), 333, 351, 352, 353(3), 354(3), 356(3), 357(2), 360(3), 361, 362(7), 363(4), 364, 367, 394, 395(2), 400, 401(2), 418 | the verb family, across the whole book |
| `invisible hammers` | 1 | 1 | 1 | 175 | the image brief 12 item 3 quotes; once in the volume, at printed p. 175 |
| `trillions` | 1 | 1 | 1 | 175 | the number in that image - and it is the only 'trillions' in the book, so it is rhetoric, not a count |
| `striae` | 4 | 4 | 4 | 144, 186, 370(2) | brief 12 item 5's word for the bands. In the book three times, never in chapter XXXII; the quotable striae sentence is in the New York lecture at printed p. 186 (row 92) |
| `stratification` | 1 | 1 | 1 | 402 | the same phenomenon in Thomson's reported speech, p. 402 (row 61) |
| `stratifications` | 1 | 1 | 1 | 402 | the plural, in the one sentence that says they were ABSENT (row 61) |
| `after-glow` | 1 | 1 | 1 | 402 | the persistence of the light, once in the volume, in the sentence this pin pins at p. 402 (row 46) |
| `non-striking` | 6 | 6 | 6 | 175, 242(2), 275, 282, 283 | brief 12 item 4's term of art for the vacuum that will not striate; his own method for beating it is at printed p. 175 (row 88) |
| `Hittorf` | 1 | 1 | 1 | 405 | the prior art he concedes on printed p. 405 (row 76); once in the volume, and it is his sentence, not the compiler's |
| `six weeks` | 1 | 1 | 1 | 406 | the duration the internet gives Tesla. Once in the volume, on printed p. 406, and the 'I' is J. J. Thomson (row 79) |
| `mean free path` | 5 | 5 | 5 | 141, 166, 178, 282(2) | the physics he reaches for at printed p. 282 and in the New York lecture; the reason Rejected #21 matters |
| `carborundum` | 23 | 23 | 23 | 140, 253(3), 254(4), 255(8), 257(3), 258, 259, 494(2) | the lamp material of brief 12 item 3; the passage is the densest in the book |
| `diamond` | 10 | 10 | 10 | 249, 253(3), 255(4), 258, 259 | the comparison material, in the same passage |
| `diamond dust` | 1 | 1 | 1 | 255 | the specific thing he tried, once in the volume, at printed p. 255 |
| `candle power` | 5 | 5 | 5 | 123, 127, 177, 376, 384 | the period's brightness unit, as two words; brief 12 item 3's 'any desired candle power' is in the New York lecture |
| `candlepower` | 0 | 0 | 0 | - | the modern closed spelling. Not in the volume |
| `efficiency` | 33 | 33 | 33 | 5(2), 8(6), 24(2), 25, 30, 51, 95, 103, 105(2), 109, 172, 176, 178(5), 192, 272, 286, 377, 434, 455, 481, 492 | the word he does use, including in the one sentence that says his lamp showed 'no appreciable waste of energy' (row 91) - and never with a number |
| `per cent` | 5 | 5 | 5 | 8(4), 452 | the unit an efficiency claim would need. Five hits, none in this article's chapters |
| `watt` | 0 | 0 | 0 | - | the unit a lamp output claim would need. Not in the volume |
| `electron` | 0 | 0 | 0 | - | the particle the mechanism would need. Not in the volume; Thomson's corpuscle paper is 1897 |
| `ionis` | 1 | 1 | 1 | 301 | the ionisation word family. Once in the volume |
| `ultraviolet` | 0 | 0 | 0 | - | not in the volume |
| `X-ray` | 0 | 0 | 0 | - | brief 12's flagged 'needs source' item. Not in the volume; see the flag THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895 |
| `X rays` | 0 | 0 | 0 | - | the two-word period form, as Röntgen's own paper was titled in English. Not in the volume |
| `x ray` | 0 | 0 | 0 | - | the lower-case form, counted separately so a reader can see the zero is not a capitalisation artefact |
| `Röntgen` | 0 | 0 | 0 | - | the discoverer's name. Not in the volume, in any spelling |
| `roentgen` | 0 | 0 | 0 | - | the same name unaccented, counted separately |
| `free energy` | 0 | 0 | 0 | - | the phrase article 10 exists to correct. Not in the volume |
| `light without energy` | 0 | 0 | 0 | - | the modern phrase brief 12 item 5 says is wrong. Not in the volume, so it cannot be quoted at anyone in 1894 |
| `test` | 94 | 94 | 94 | -6, 5(3), 7, 8(3), 9, 17(2), 20, 21, 33, 55, 76(2), 77, 78, 79, 94, 103, 109, 132, 137, 150, 157(2), 159, 161(3), 169, 170(3), 172(4), 198, 201, 202, 205, 213, 227, 230(2), 237, 238, 253, 257, 258(2), 259, 268, 272, 297(3), 298, 299, 311, 321, 323, 326, 337, 343(3), 347(2), 357, 362, 363(3), 364, 382, 389(2), 416, 434, 440(2), 443, 453, 460, 463, 481(2), 485, 489, 494 | the word a 'he measured it' story needs. In the volume constantly and in chapter XXXII not once; see the scoped table |
| `experiment` | 429 | 425 | 429 | -3, -2, 3(2), 5(2), 6, 11, 18, 19(2), 119(2), 120(5), 121(3), 122(4), 123(3), 124, 125, 126, 128(2), 129(2), 131(2), 132(2), 133, 136(4), 138(5), 139, 140(3), 141(3), 142(3), 143(6), 144(3), 149, 150(3), 151(2), 152(5), 155, 161(4), 163, 164, 165(3), 166, 168, 170(4), 171(2), 172, 173, 174(4), 178, 181, 182, 184, 185, 186(3), 187(2), 190, 191, 193, 195(2), 196(2), 198(2), 199(3), 200(2), 201(3), 202(2), 203(2), 204(2), 205(2), 206(3), 207(2), 209, 210(2), 212(4), 213(7), 214, 215(2), 216, 217(3), 218(2), 219(2), 220(3), 222, 224, 225(3), 230(4), 231(4), 232(3), 233(4), 234(3), 236(2), 237, 238, 239, 241, 244, 247, 248, 249(2), 251(2), 253, 254(2), 257(4), 258(2), 259, 261, 262, 263(4), 264(2), 265(2), 267(2), 268(2), 269, 271, 273(4), 274(2), 275, 276, 277(2), 278, 280, 281(2), 282(2), 285(2), 286(2), 287(2), 289(2), 292, 295, 300(4), 301, 302(9), 308, 311, 312(2), 314(4), 315, 317, 318(4), 320, 321(4), 322, 323, 324, 326, 327, 329, 330(2), 333(2), 336(3), 337(2), 338(2), 339(4), 340(4), 341, 342(4), 344, 345, 346, 347, 348, 349, 350(4), 351, 352(3), 353, 356, 357(2), 358(2), 359, 360, 362(2), 364, 365(3), 367, 369, 371, 372, 374(2), 376, 377(2), 382, 383, 384(4), 385, 386(2), 390(2), 392, 396(7), 397(2), 398(3), 399(4), 400, 401(3), 402(4), 404(4), 405, 406(10), 418(4), 424(2), 429, 467, 470, 471(2), 472, 481, 485, 487(2), 488, 489(2) | what those chapters do contain, by the hundred |
| `excite it by means` | 1 | 1 | 1 | 288 | the exact phrase of the p. 288 question sentence (row 22); once in the volume, which is why the truncated form in Rejected #2 is a different sentence |
| `without wires` | 4 | 5 | 5 | 132, 292, 495, 496 | article 01's title phrase. In the volume five times, never in chapter XXXII |
| `cold flame` | 0 | 0 | 0 | - | article 06's title phrase. Not in the volume in any form - he says 'brush' and 'flame' separately |
| `brush` | 261 | 253 | 261 | -1(2), 3, 5, 6, 28(2), 33(5), 34(4), 35, 41, 43(2), 46, 56, 57(4), 58(3), 61, 62, 63, 65, 66, 103, 111, 126(2), 127(3), 130(2), 131(10), 132(2), 137(3), 158, 159, 163(3), 166(3), 167(8), 168, 169, 170, 171, 202, 205(4), 206(4), 218, 219, 222(3), 226(3), 227(3), 228(2), 229(7), 230(7), 231(2), 245, 258(2), 259, 268, 272, 375, 390(3), 412(2), 413, 432(8), 433(4), 435, 437, 438(12), 439(17), 440(9), 441(19), 442(10), 443(19), 444(4), 445(15), 446(2), 447(2), 451, 454, 455, 465(3), 494(3) | the book's word for the discharge at a wire end, which is what article 06 is about |
| `end of the wire` | 3 | 6 | 6 | 53, 138, 291 | the phrase the brush sentences use |
| `torricellian` | 3 | 3 | 3 | 277(2), 402 | the vacuum standard he reports failing to reach at printed p. 402 (row 47) |
| `Ruhmkorff` | 1 | 1 | 1 | 385 | the induction coil by its usual period name; once in the volume, and he mostly says 'induction coil' or 'disruptive discharge coil' |
| `induction coil` | 96 | 101 | 101 | 53(2), 54, 57, 58, 63, 64, 94, 97(2), 120, 121(2), 123, 125, 126, 127, 132, 145, 150, 151, 155, 156, 162(2), 163(2), 164(3), 170, 174(2), 185, 189, 191, 193(2), 194, 201(4), 202, 203, 204(3), 205, 210, 220, 222, 223, 224, 225(2), 228, 231, 234, 265(2), 302(2), 306, 315(2), 318, 323, 328(2), 329(2), 330(3), 331, 332(2), 333(2), 341, 344, 345, 352, 357, 362, 366, 382, 385, 386, 393, 398, 403, 411(2), 495 | the apparatus phrase, across the whole book |
| `Crookes` | 14 | 14 | 14 | 121, 126, 176, 178, 198(2), 201, 236, 243, 282, 290, 322, 327, 362 | the prior experimenter he argues against on printed p. 282 and elsewhere |
| `no consumption of material` | 1 | 1 | 1 | 214 | the conservation sentence of the gas-lamp argument (row 95); once in the volume |
| `economize the energy` | 2 | 2 | 2 | 259, 289 | the p. 289 sentence about the same subject (row 28) |
| `energy which is obtained` | 1 | 1 | 1 | 289 | the rest of that p. 289 sentence |

## The spellings the book actually sets, inside the quotes this pin carries

Not a style note. Each of these is a specific defect at a specific page inside a quote this file pins, and the rule the pin uses is in the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX: a quote carries the scan, and where the scan is unreadable the quote is cut or the sentence is paraphrased and cited. A silently corrected 1894 fails the matcher and cannot be checked by a reader either.

| as printed | raw | gate | keep | where |
|---|---|---|---|---|
| `vaciium` | 1 | 1 | 1 | printed p. 402, inside row 64's quote |
| `plaeed` | 1 | 1 | 1 | printed p. 403, inside row 62's quote |
| `inclose proximity` | 1 | 1 | 1 | printed p. 403, inside row 62's quote. 'inclosed' is the book's ordinary word and it is spelled right eleven times; this one instance is the book's own error, not the scan's |
| `to eparate` | 1 | 1 | 1 | printed p. 406, inside row 82's quote: the book drops the leading 's' |
| `viorate` | 1 | 1 | 1 | printed p. 176, inside row 89's quote |
| `efficiencv` | 1 | 1 | 1 | printed p. 176, the sentence Rejected #18 quotes |
| `eifects` | 4 | 4 | 4 | printed pp. 169, 175 (twice), 176 - a recurring OCR failure, not a one-off |
| `sitw qua` | 1 | 1 | 1 | printed p. 175, for 'sine qua non'; 'sine qua non' itself is 0 in the volume, which is how you can tell the phrase is the scan's and not his |
| `f rictional` | 2 | 2 | 2 | printed p. 288, inside row 23's quote; the same pattern of a space after a first letter appears again at p. 341 |
| `J urther` | 1 | 1 | 1 | printed p. 403, inside row 59's quote |
| `sniall` | 1 | 1 | 1 | printed p. 258, Rejected #10 |
| `Avill` | 1 | 1 | 1 | printed p. 253, inside the carborundum row's quote |
| `II. S. A.` | 1 | 1 | 1 | printed p. 253, for 'U. S. A.', same sentence |
| `NonConsuming` | 1 | 1 | 1 | printed p. 494, the volume's own index entry 'Flames, Electrostatic, NonConsuming 166, 272' - the index hyphen is lost in the scan, which is why the index entry cannot be quoted as furniture |
| `Carborundum Button for Tesla Lamps` | 0 | 1 | 1 | printed p. 494, the volume's own index entry for the lamp passage, filing it at 140 and 253 - the second of those is this article's page, the first is the compiler's chapter |

## The scoped counts: what these chapters never report

The same terms, counted inside four ranges instead of the whole volume. This is the evidence for brief 12 item 3's 'no efficiency figure' and item 5's correction, and it is why those beats can be written at all. A scoped zero says the passage does not contain the word; it does not say the passage contains no claim, and it does not say anything about what he did or did not measure. Read NO NUMBER IN THIS ARTICLE'S SUBJECT, AND THE ABSENCE IS THE CLAIM and HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS.

| term | ch. XXXII 396-406 | lamp passage 253-259 | ch. XXVI 145-197 | ch. XXVII 198-293 | why it is in the table |
|---|---|---|---|---|---|
| `test` | 0 | 5 (253, 257, 258(2), 259) | 15 (150, 157(2), 159, 161(3), 169, 170(3), 172(4)) | 17 (198, 201, 202, 205, 213, 227, 230(2), 237, 238, 253, 257, 258(2), 259, 268, 272) | a 'he tested it' story needs this word in the passage it is describing |
| `experiment` | 38 (396(7), 397(2), 398(3), 399(4), 400, 401(3), 402(3), 404(4), 405, 406(10)) | 10 (253, 254(2), 257(4), 258(2), 259) | 52 (149, 150(3), 151(2), 152(5), 155, 161(4), 163, 164, 165(3), 166, 168, 170(4), 171(2), 172, 173, 174(4), 178, 181, 182, 184, 185, 186(3), 187(2), 190, 191, 193, 195(2), 196(2)) | 137 (198, 199(3), 200(2), 201(3), 202(2), 203(2), 204(2), 205(2), 206(3), 207(2), 209, 210(2), 212(4), 213(7), 214, 215(2), 216, 217(3), 218(2), 219(2), 220(3), 222, 224, 225(3), 230(4), 231(4), 232(3), 233(4), 234(3), 236(2), 237, 238, 239, 241, 244, 247, 248, 249(2), 251(2), 253, 254(2), 257(4), 258(2), 259, 261, 262, 263(4), 264(2), 265(2), 267(2), 268(2), 269, 271, 273(4), 274(2), 275, 276, 277(2), 278, 280, 281(2), 282(2), 285(2), 286(2), 287(2), 289(2), 292) | what the passages are actually full of |
| `efficiency` | 0 | 0 | 8 (172, 176, 178(5), 192) | 2 (272, 286) | brief 12 item 3's 'no efficiency figure' |
| `per cent` | 0 | 0 | 0 | 0 | the unit such a figure would be written in |
| `watt` | 0 | 0 | 0 | 0 | the unit an output figure would be written in |
| `candle power` | 0 | 0 | 1 (177) | 0 | the brightness unit the period did have |
| `volts` | 0 | 0 | 5 (151, 168, 169, 183, 193) | 5 (206, 223, 262, 286, 287) | an electrical measurement he had instruments for |
| `ampere` | 0 | 0 | 1 (149) | 1 (290) | the other one |
| `output` | 0 | 0 | 4 (158, 172, 192, 193) | 1 (224) | the quantity a lamp claim would state |
| `cost` | 0 | 0 | 0 | 1 (223) | the commercial claim the compiler's chapter at p. 140 makes and the lecture does not |
| `life` | 0 | 0 | 1 (181) | 4 (198, 200, 260, 262) | as in 'lamp life', the durability claim brief 12 item 3's diamond-dust sentence is about |
| `hours` | 0 | 0 | 0 | 5 (200, 201, 221, 228, 278) | the unit of that claim |
| `measure` | 0 | 1 (256) | 2 (146(2)) | 3 (198, 256, 267) | the verb itself |
| `commercial` | 0 | 0 | 3 (158, 169, 172) | 1 (275) | the adjective the compiler uses and the lecturer does not |
| `energy` | 0 | 8 (256(3), 257(3), 258, 259) | 44 (145(2), 146, 157(2), 160, 162(4), 172, 174(5), 176(2), 178, 180(2), 181, 182(2), 184, 187, 189(2), 190(4), 191, 192(2), 193(3), 196(3), 197(3)) | 87 (200(4), 205, 213, 214, 223(2), 224, 235(3), 236(5), 237(2), 238, 239, 240(3), 241(2), 242(3), 243(3), 245, 246, 250, 252(5), 256(3), 257(3), 258, 259, 260, 261(3), 262(5), 264, 265(2), 266(4), 267(7), 269(5), 272, 280, 282(2), 284, 287, 289, 291(3)) | the word brief 12 item 5's 'capacitively coupled' sentence is about. Chapter XXXII does not use it once in nine pages |
| `striae` | 0 | 0 | 1 (186) | 0 | brief 12 item 5's word |
| `stratification` | 1 (402) | 0 | 0 | 0 | the same thing in Thomson's words |
| `after-glow` | 1 (402) | 0 | 0 | 0 | the persistence he does discuss |
| `Geissler` | 0 | 0 | 4 (175, 190, 195(2)) | 0 | brief 12 item 1's tube |
| `X-ray` | 0 | 0 | 0 | 0 | brief 12's flagged item |
| `vacuum tube` | 4 (396(2), 403, 404) | 0 | 0 | 5 (210, 218, 279, 286, 287) | the modern phrase |
| `exhausted tube` | 7 (399(2), 401, 402, 404, 405, 406) | 0 | 9 (184, 186, 187, 189(2), 190(4)) | 8 (210, 217, 218, 234, 236, 281, 286(2)) | the period phrase |
| `phosphorescence` | 0 | 10 (253, 255(2), 256(2), 257(4), 258) | 1 (160) | 29 (221, 228, 245, 248, 251, 253, 255(2), 256(2), 257(4), 258, 260(2), 263(3), 270, 271(2), 282(3), 289(2), 291) | the light he is describing |
| `carborundum` | 0 | 20 (253(3), 254(4), 255(8), 257(3), 258, 259) | 0 | 20 (253(3), 254(4), 255(8), 257(3), 258, 259) | the lamp material |
| `electrode` | 7 (396, 402(3), 404(2), 406) | 19 (253(2), 256, 257(3), 258(4), 259(9)) | 6 (150, 161(2), 175, 184, 187) | 67 (226, 227, 241, 242, 246, 247, 248(4), 249(7), 253(2), 256, 257(3), 258(4), 259(9), 260(6), 261(7), 263(2), 264, 268(3), 269(3), 270(3), 271, 272(3), 284(2)) | the thing his tubes do not have |
| `without wires` | 0 | 0 | 0 | 1 (292) | article 01's phrase for the same demonstration |
| `brush` | 0 | 3 (258(2), 259) | 20 (158, 159, 163(3), 166(3), 167(8), 168, 169, 170, 171) | 44 (202, 205(4), 206(4), 218, 219, 222(3), 226(3), 227(3), 228(2), 229(7), 230(7), 231(2), 245, 258(2), 259, 268, 272) | article 06's subject |
| `condenser` | 1 (396) | 0 | 28 (150, 152, 162, 164, 165, 175, 176, 177, 179, 181, 182(2), 183(4), 186, 187, 191(5), 192, 193(4)) | 55 (202, 203, 204(3), 206(2), 207, 210, 212(2), 213(5), 222(2), 223, 224, 225(4), 226(2), 233, 234, 235, 238, 245(2), 246(4), 261, 264, 265, 267(4), 268(5), 269(2), 273, 274, 279, 286, 292) | the component in the chapter's own argument |
| `electrostatic` | 26 (398(2), 399(3), 400, 401(2), 402(2), 404(4), 405(4), 406(8)) | 0 | 42 (149(4), 151, 167, 174(5), 175(6), 176, 182(2), 184(2), 185, 186(4), 187, 189(6), 190(4), 191, 192(2), 195) | 39 (207, 213, 218, 228, 229(3), 230(3), 232, 235(2), 238, 241(3), 242, 274(4), 275(3), 279, 287(6), 288(2), 289(2), 291, 292(2)) | the question the chapter is arguing about |
| `luminous` | 19 (397, 398, 399(5), 400, 401(3), 402(3), 403(2), 404(2), 405) | 3 (256(2), 257) | 20 (155, 159(2), 160(3), 164(2), 168, 175(3), 184, 185, 186, 189(3), 190(2)) | 32 (201, 202, 214(2), 215(2), 216(3), 217(3), 218, 223(3), 235, 249(2), 252, 256(2), 257, 273, 274(3), 275, 284, 286(3)) | the book's word for the light |

## What the live series pages already print

Every fragment in this pin was compared, whitespace-normalised, against the rendered text of the series pages that are live on the date above. A draft that reprints a sentence another page of this series has already printed is not wrong about the book, it is wrong about the series - so each row below is a sentence to link to, not to reprint. This is how the ownership flags were measured rather than remembered.

| pinned page | fragment this pin carries | already printed on the live page(s) |
|---|---|---|
| p. 198 | `Lecture delivered before the Institution of Electrical Engineers, London, February, 1892` | `tesla-cold-flame.html`, `tesla-free-energy-what-he-said.html` |
| p. 145 | `A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891` | `tesla-cold-flame.html`, `tesla-free-energy-what-he-said.html` |
| p. 6 | `The present volume deals simply with his work accomplished to date` | `tesla-free-energy-what-he-said.html` |
| p. 288 | `I may put it away for a few weeks or months, still it retains the faculty of being excited` | `tesla-lit-lamps-without-wires.html` |
| p. 288 | `What change have I produced in the tube in the act of exciting it?` | `tesla-lit-lamps-without-wires.html` |

The live pages this compared against, and the 1894 pages each already cites:

| page | visible words | 1894 pages it cites (count) |
|---|---|---|
| `tesla-lit-lamps-without-wires.html` | 2,989 | 125 (1), 145 (2), 179 (1), 183 (4), 184 (3), 185 (3), 186 (2), 187 (3), 193 (3), 199 (1), 200 (3), 288 (2), 289 (1) |
| `tesla-one-wire-power.html` | 3,359 | 184 (3), 228 (1), 232 (2), 233 (2), 234 (7), 235 (7), 236 (8), 267 (7), 333 (1), 334 (2) |
| `tesla-earthquake-machine.html` | 2,346 | 486 (5), 487 (7), 488 (2), 491 (1) |
| `tesla-wireless-power-1893.html` | 4,256 | 138 (7), 143 (2), 151 (4), 189 (2), 196 (3), 197 (2), 344 (1), 346 (12), 347 (8), 348 (5), 349 (4) |
| `tesla-high-frequency-massage.html` | 4,389 | 162 (4), 393 (3), 394 (13), 395 (17), 495 (1) |
| `tesla-cold-flame.html` | 7,087 | 121 (2), 145 (1), 166 (8), 167 (17), 168 (13), 169 (5), 171 (5), 198 (1), 213 (2), 226 (4), 227 (1), 228 (4), 258 (7), 259 (5), 291 (3), 322 (2), 376 (2), 381 (2) |
| `rotating-magnetic-field-1888.html` | 3,213 | 8 (5), 9 (7), 10 (3), 11 (2), 12 (1), 13 (2), 14 (4), 15 (2), 16 (1), 17 (2), 20 (4), 21 (3), 22 (2), 23 (1), 24 (1), 479 (1), 496 (1) |
| `tesla-weird-inventions-1894.html` | 4,099 | 6 (2), 390 (1), 409 (3), 412 (1), 418 (2), 419 (2), 420 (3), 422 (1), 423 (2), 424 (4), 429 (1), 432 (3), 434 (2), 436 (1), 437 (1), 438 (2), 441 (1), 448 (3), 450 (2), 451 (2), 463 (1), 464 (1), 465 (1), 467 (3), 468 (1), 474 (3), 496 (1) |
| `tesla-worlds-fair-1893.html` | 2,086 | 477 (5), 479 (6), 480 (1), 481 (3), 483 (2), 485 (5) |
| `tesla-free-energy-what-he-said.html` | 5,206 | 6 (1), 8 (3), 35 (1), 46 (1), 119 (2), 120 (1), 138 (4), 145 (1), 167 (1), 196 (4), 197 (2), 198 (1), 232 (1), 236 (7), 267 (1), 394 (1), 424 (8), 429 (4), 430 (2), 494 (2), 496 (2) |

## Quotes, pinned by printed page

Each block prints its own `- row:` line: that number is the order of the QUOTES list in `gen_quotes.py`, and it is what the '- why:' notes, the flags and the figure notes mean when they say 'row 40'. Nothing renumbers it. The check at the end of this file resolves every one of those references the same way it resolves 'Rejected #N'.

## Printed p. 6 (scan file 24, 18 leaves of offset)

### 0. Provenance (ch. I, the editor's date fence)

> "The present volume deals simply with his work accomplished to date"

- row: 15
- cited as: `(1894, p. 6)`
- why: the editor's own limit on the whole volume, and the sentence that settles brief 12's X-ray warning for good: nothing in this book was written after 1894 and the copyright leaf is 1893, so the volume cannot mention a discovery made in December 1895. Article 10 and article 08 both pin this line; the three pages must use it the same way (a date fence, not a comment on Tesla's foresight)
- check_quotes.py: exact match, ratio 1.0, printed p. 6
- raw OCR: `he conversion of alternating into direct currents, etc. It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting ideas and inventions, tobe made public in due course. The present volume deals simply with his work accomplished to date.`

### 0. Provenance (ch. I, the editor on what is NOT in the volume)

> "It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting ideas and inventions, tobe made public in due course"

- row: 16
- cited as: `(1894, p. 6)`
- why: the other half of the date fence, and the reason the absence of X-rays is not a finding about Tesla: the compiler says work in progress is held back. The OCR glues 'tobe'; the print has the space, so this verifies only through the space-ignoring index and the draft prints the clean form. Article 08's pin carries the same sentence with the same annotation
- check_quotes.py: exact match, ratio 1.0, printed p. 6
- raw OCR: `tic motors, third-brush regulation, improvements in dynamos, new forms of incandescent lamps, electrical meters, condensers, unipolar dynamos, the conversion of alternating into direct currents, etc. It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting ideas and inventions, tobe made public in due course. The present volume deals simply with his work accomplished to date.`

### 3. Tesla's lamp research (the editor's inventory lists lamps)

> "new forms of incandescent lamps"

- row: 17
- cited as: `(1894, p. 6)`
- why: the editor's own inventory of the volume puts 'new forms of incandescent lamps' in the Miscellaneous section, printed p. 6. It is the sentence that licenses brief 12 item 3 as part of this book's subject matter rather than a digression. Article 08's pin quotes the same inventory at greater length for its own list; take only these five words here
- check_quotes.py: exact match, ratio 1.0, printed p. 6
- raw OCR: `aneous "section of this volume includes a great many other inventions in arc lighting, transformers, pyro-magnetic generators, thermo-magnetic motors, third-brush regulation, improvements in dynamos, new forms of incandescent lamps, electrical meters, condensers, unipolar dynamos, the conversion of alternating into direct currents, etc. It is needless to say that at this moment Mr. Tesla is engaged on a number of interesting id`

## Printed p. 145 (scan file 163, 18 leaves of offset)

### 0. Provenance (ch. XXVI footnote, the date of the New York lecture)

> "A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891."

- row: 14
- cited as: `(1894, p. 145)`
- why: dates the chapter that carries the p. 186 condenser-action sentence and the p. 175 'trillions of invisible hammers' passage. Three dates, three texts, one article: May 1891, July 1891, February 1892. If the draft attaches a year to a quote it has to be this one or that one, and the p. 175 and p. 186 sentences are May 1891, not 1892. Read the flag FOUR TEXTS, FOUR VOICES, ONE CHAPTER
- check_quotes.py: exact match, ratio 1.0, printed p. 145
- raw OCR: `is still conjecture, yet we know that the truth cannot be much longer hidden, and instinctively we feel that the understanding is dawning upon us. We still admire these beautiful phenomena, these 1. A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891.`

## Printed p. 175 (scan file 193, 18 leaves of offset)

### 2. Why a tube lights with no wires (the position, stated in 1891)

> "the luminous effects, which are producible by induction in a tube devoid of electrodes, I am inclined to consider as being of an electrostatic nature"

- row: 85
- cited as: `(1894, p. 175)`
- why: the thesis of the whole article, in his own words, in the New York lecture of May 1891, a year and a half before the London lecture the brief's hook comes from: 'I am inclined to consider'. That hedge is the sentence's honest content and it must be quoted with the claim, not trimmed to 'is of an electrostatic nature'. The preceding sentence names a Geissler tube, which is the brief's other query term
- check_quotes.py: exact match, ratio 1.0, printed p. 175
- raw OCR: `gnetic disturbances may pass readily through miles of air. Such dark waves, unless they are of the length of true light waves, cannot, it would seem, excite luminous radiation in a Geissler tube, and the luminous effects, which are producible by induction in a tube devoid of electrodes, I am inclined to consider as being of an electrostatic nature. To produce such luminous effects, straight electrostatic thrusts are required; these, whatever be their frequency, may disturb the molecular charges and produce light. Since current impulses of the`

### 2. Why a tube lights with no wires (Geissler, and what he ruled out)

> "Such dark waves, unless they are of the length of true light waves, cannot, it would seem, excite luminous radiation in a Geissler tube"

- row: 86
- cited as: `(1894, p. 175)`
- why: the only place in the volume where a Geissler tube is used as an argument rather than as a prop: he rules out long electromagnetic waves exciting a Geissler tube, and infers the effect must be electrostatic. 'it would seem' again. Brief 12's query list includes 'geissler tube tesla', and 'Geissler' is in the volume 5 times (measured): 4 of them inside the 1891 New York lecture at printed pp. 145-197, and one more, 1, outside that chapter. A sentence that says the word appears only in the lecture is wrong by one hit, and the table below gives the pages
- check_quotes.py: exact match, ratio 1.0, printed p. 175
- raw OCR: `, cause them to vibrate and to emit light. Long transverse waves cannot, apparently, produce such effects, since excessively small electro-magnetic disturbances may pass readily through miles of air. Such dark waves, unless they are of the length of true light waves, cannot, it would seem, excite luminous radiation in a Geissler tube, and the luminous effects, which are producible by induction in a tube devoid of electrodes, I am inclined to consider as being of an electrostatic nature. To produce such luminous effects, straight`

### 2. Why a tube lights with no wires (the mechanism, in his best sentence)

> "we may place a body of some refractory material in a closed, and preferably more or less exhausted, globe, connect it to a source of ... high, rapidly alternating potential, causing the molecules of the gas to strike it many times a second at enormous speeds, and in this manner, with trillions of invisible hammers, pound it until it gets incandescent"

- row: 87
- cited as: `(1894, p. 175)`
- why: the mechanism of a lamp with no filament leads, stated as an image: trillions of invisible hammers. It is the sentence that connects beat 2 to beat 3 - the gas molecules are the power source and the button is what they hit - and it is dated May 1891, before the carborundum work of 1892. The cut is a stray OCR bullet at the end of a printed line, not an ellipsis in the text; see Rejected #16 for the uncut form
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 175; frag 2: exact match, ratio 1.0, printed p. 175
- raw OCR (frag 1: we may place a body of some refractory m): `ion of powerful electrostatic effects becomes an imperative necessity. It has occurred to me, however, that electrostatic effects are in many ways available for the production of light. For instance, we may place a body of some refractory material in a closed, and preferably more or less exhausted, globe, connect it to a source of • high, rapidly alternating potential, causing the molecules of the gas to strike it many times a second at enormous speeds, and in this manner, with trillions of invisible hammers, pound it until it`
- raw OCR (frag 2: high, rapidly alternating potential, cau): `n many ways available for the production of light. For instance, we may place a body of some refractory material in a closed, and preferably more or less exhausted, globe, connect it to a source of • high, rapidly alternating potential, causing the molecules of the gas to strike it many times a second at enormous speeds, and in this manner, with trillions of invisible hammers, pound it until it gets incandescent ; or we may place a body in a very highly exhausted globe, in a non-striking vacuum, and, by employing very`

### 4. The vacuum problem (the method for beating a non-striking vacuum)

> "we may place a body in a very highly exhausted globe, in a non-striking vacuum, and, by employing very high frequencies and potentials, transfer sufficient energy from it to other bodies in the vicinity, or in general to the surroundings, to maintain it at any degree of incandescence"

- row: 88
- cited as: `(1894, p. 175)`
- straddle: this ONE fragment sits on printed pp. 175-176 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches its citation regex
- why: the method, in one sentence, and the phrase 'transfer sufficient energy' is the conservation language the article needs for beat 5: energy is moved, not generated. The fragment straddles printed pp. 175-176 as one run, so cite one page only. 'non-striking vacuum' here is the term of art brief 12 item 4 is about, and this is where it is first defined in the volume
- check_quotes.py: exact match, ratio 1.0, printed p. 175 (this ONE fragment straddles printed pp. 175-176; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `ting potential, causing the molecules of the gas to strike it many times a second at enormous speeds, and in this manner, with trillions of invisible hammers, pound it until it gets incandescent ; or we may place a body in a very highly exhausted globe, in a non-striking vacuum, and, by employing very`

## Printed p. 176 (scan file 194, 18 leaves of offset)

### 2. Why a tube lights with no wires (the shortest statement of the mechanism)

> "causing them to viorate and to emit light"

- row: 89
- cited as: `(1894, p. 176)`
- why: the mechanism in six words: disturb the ether or static charges carried by the gas molecules, make them vibrate, get light. The OCR prints 'viorate' for 'vibrate' - a real scan error the space-ignoring index cannot fix, so the draft must print the OCR's word or cut the word out. Read the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX
- check_quotes.py: exact match, ratio 1.0, printed p. 176
- raw OCR: `oundings, to maintain it at any degree of incandescence ; or we may, by means of such rapidly alternating high potentials, disturb the ether carried by the molecules of a gas or their static charges, causing them to viorate and to emit light. But, electrostatic eifects being dependent upon the potential and frequency, to produce the most powerful action it is desirable to increase both as far as practicable. It may be possible to obtain`

### 2. Why a tube lights with no wires (the one comparison he reports as a fact)

> "the physiological effect of the current required to maintain at a certain degree of brightness a tube four feet long, provided at the ends with outside and inside condenser coatings, is so powerful that, I think, it might produce serious injury to those not accustomed to such shocks ; whereas, with twenty thousand alternations per second, the tube may be maintained at the same degree of brightness without any effect being felt"

- row: 90
- cited as: `(1894, p. 176)`
- why: the closest thing in the article's subject to a controlled comparison: same tube, same brightness, low frequency hurts, 20,000 per second does not. It is a physiological observation, not a photometric one, and it is about a four-foot tube with condenser coatings, which is the apparatus description the article needs. Article 01 already prints the p. 125 sentence about physiological effects being small for a different apparatus, so the two must not be blended: read the flag ARTICLE 01 OWNS THE SAFETY SENTENCE
- check_quotes.py: exact match, ratio 1.0, printed p. 176
- raw OCR: `tain frequency, for, first, the potential then becomes so great that it is dangerous ; and, secondly, the light production is less efficient. I have found that, by using the ordinary low frequencies, the physiological effect of the current required to maintain at a certain degree of brightness a tube four feet long, provided at the ends with outside and inside condenser coatings, is so powerful that, I think, it might produce serious injury to those not accustomed to such shocks ; whereas, with twenty thousand alternations per second, the tube may be maintained at the same degree of brightness without any effect being felt. This is due principally to the fact that a much smaller potential is required to produce the same light effect, and also to the higher efficiency in the light production. It is evident that the effi`

### 5. What the internet gets wrong (he uses the word efficiency)

> "This is due principally to the fact that a much smaller potential is required to produce the same light effect, and also to the higher efficiency in the light production"

- row: 91
- cited as: `(1894, p. 176)`
- why: 'efficiency' appears in the volume 33 times (measured), and this is one of the few places it is used about a LIGHTING apparatus with a comparison attached: a smaller potential for the same light effect, plus a higher efficiency in light production. The whole sentence is on printed p. 176 - it does NOT straddle the page break, which is why the quote is carried in full here rather than cut. The next sentence is in Rejected #18 because the OCR prints 'efficiencv' inside it. It is the strongest available answer to 'he never compared anything', and it is still not a number
- check_quotes.py: exact match, ratio 1.0, printed p. 176
- raw OCR: `rious injury to those not accustomed to such shocks ; whereas, with twenty thousand alternations per second, the tube may be maintained at the same degree of brightness without any effect being felt. This is due principally to the fact that a much smaller potential is required to produce the same light effect, and also to the higher efficiency in the light production. It is evident that the efficiencv in such cases is the greater, the higher the frequency, for the quicker the process of charging and discharging the molecules, the less energy will be lost in the f`

## Printed p. 177 (scan file 195, 18 leaves of offset)

### 3. Tesla's lamp research (the ambition, a year and a half earlier)

> "in this manner a simple lamp capable of giving any desired candle power is provided"

- row: 113
- cited as: `(1894, p. 177)`
- why: the largest claim this article's subject ever gets in the volume: a lamp of 'any desired candle power' from the same bombardment. It is in the New York lecture of May 1891, before the carborundum work, and it is the sentence the pp. 253-255 failure answers. 'candle power' (two words) is in the volume 5 times and 'candlepower' (one word) 0 times (measured), so the unit is period and the spelling is not, and no number is attached to any of those hits. Quote the claim with 'any desired' in it; the hedge is the claim
- check_quotes.py: exact match, ratio 1.0, printed p. 177
- raw OCR: `rbon filament, or, preferably, a button of some refractory material (Fig. 115), even if it be a comparatively poor conductor, inclosed in an exhausted globe, may be rendered highly incandescent ; and in this manner a simple lamp capable of giving any desired candle power is provided. The success of lamps of this kind would depend largely on the selection of the light-giving bodies contained within the bulb. Since, under the conditions described, refractory bodies — which are ver`

### 3. Tesla's lamp research (he names the problem before he meets it)

> "The success of lamps of this kind would depend largely on the selection of the light-giving bodies contained within the bulb"

- row: 114
- cited as: `(1894, p. 177)`
- why: the design problem stated in 1891, in his own words: the lamp lives or dies by what is inside the bulb. That is exactly what the carborundum passage of 1892 is an attempt at, and the two sentences a year and a half apart are the whole plot of this article's third beat. 'Would depend largely' is a conditional about a future trial, not a result
- check_quotes.py: exact match, ratio 1.0, printed p. 177
- raw OCR: `if it be a comparatively poor conductor, inclosed in an exhausted globe, may be rendered highly incandescent ; and in this manner a simple lamp capable of giving any desired candle power is provided. The success of lamps of this kind would depend largely on the selection of the light-giving bodies contained within the bulb. Since, under the conditions described, refractory bodies — which are very poor conductors and capable of withstanding for a long time excessively high degrees of temperature — may be used, such illu`

### 4. The vacuum problem (the opposite of what the reader expects)

> "the better the vacuum the more easily the bodies are brought to incandescence"

- row: 115
- cited as: `(1894, p. 177)`
- why: the intuition is that a better vacuum means less to heat and so less light; he tested it and prints the contrary, and marks it as his own experience ('This is not confirmed by my experience; quite the contrary'). It belongs with the p. 288 'another tube might not light' moment and the p. 402 Torricellian failure: three different pages, one hard problem, and no solution in the volume
- check_quotes.py: exact match, ratio 1.0, printed p. 177
- raw OCR: `be done by the use of the best apparatus — the heating would be much less intense, and that in a perfect vacuum it could not occur at all. This is not confirmed by my experience; quite the contrary, the better the vacuum the more easily the bodies are brought to incandescence. This result is interesting for many reasons. At the outset of this work the idea presented itself to me, whether two bodies of refractory material enclosed in a bulb exhausted to such a degree that`

## Printed p. 186 (scan file 204, 18 leaves of offset)

### 2. Why a tube lights with no wires (the word the brief wants, in his sentence)

> "an exhausted tube be introduced from the other side in the hollow space, the tube is lighted most intensely because of the increased condenser action, and in this position the striae are most sharply defined. In all these experiments described, and in many others, the action is clearly electrostatic"

- row: 92
- cited as: `(1894, p. 186)`
- why: 'condenser action' is in the volume 6 times (measured) and this is the one that says an exhausted TUBE is lighted by it; the others are about a wire, a terminal or a loss. It is also the only place that puts 'striae' and 'clearly electrostatic' in the same paragraph. Brief 12 item 2's 'the tube is one plate of a capacitor' has its 1891 warrant here. Article 01 quotes two OTHER sentences from this same printed page (the observer-standing-on-an-insulated-support sentence and the 'wiping out the light' sentence), so the draft must not re-quote those; this one is free. Read the flag ARTICLE 01 HAS THREE SENTENCES ON p. 186 AND p. 187
- check_quotes.py: exact match, ratio 1.0, printed p. 186
- raw OCR: `t the same time withdrawing it gently from the coil, judging properly the distance so that the tube remains dark afterwards. If the primary coil is placed sidewise, as in Fig. 112 B for instance, and an exhausted tube be introduced from the other side in the hollow space, the tube is lighted most intensely because of the increased condenser action, and in this position the striae are most sharply defined. In all these experiments described, and in many others, the action is clearly electrostatic. The effects of screening also indicate the electrostatic nature of the phenomena and show something of the nature of electrification through the air. For instance, if a tube is placed in the directi`

## Printed p. 198 (scan file 216, 18 leaves of offset)

### 0. Provenance (ch. XXVII footnote, the date of the lecture)

> "Lecture delivered before the Institution of Electrical Engineers, London, February, 1892."

- row: 13
- cited as: `(1894, p. 198)`
- why: dates the chapter that carries the p. 288 tube demo, the p. 255 carborundum passage, the p. 289 field experiments, the p. 290 Crookes bulbs and the p. 292 closing statement. Every 'Tesla said in 1892' in this article needs this footnote, not memory. Article 06's pin carries the same footnote for the same reason; the two pages must not date the same lecture differently
- check_quotes.py: exact match, ratio 1.0, printed p. 198
- raw OCR: `which led me to these advances — which even by myself cannot be considered trifling, since they are so appreciated by you — I believe that their real origin, that which started me to work in this 1. Lecture delivered before the Institution of Electrical Engineers, London, February, 1892.`

## Printed p. 213 (scan file 231, 18 leaves of offset)

### 5. What the internet gets wrong (the law he states and does not claim to have proved)

> "My opinion is that the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential"

- row: 93
- cited as: `(1894, p. 213)`
- why: the quantitative law he believes in: light and heat go as frequency times potential squared. 'My opinion is that' and 'should be' are in the sentence, and the next row is him saying verification would be very hard. This pair is the article's answer to 'did he measure it': he wrote down what he thought the law was AND said he had not established it. 'under otherwise equal conditions of test' is the phrase of someone who knows what a controlled test would need. Article 06's rendered page already prints this sentence with a p. 213 cite, so it is not new material here; read the flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT
- check_quotes.py: exact match, ratio 1.0, printed p. 213
- raw OCR: `osses are very small. In the preceding experiment it is of considerable interest to know what relation the quantity of the light emitted bears to the frequency and potential of the electric impulses. My opinion is that the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential, but the experimental verification of the law, whatever it may be, would be exceedingly`

### 5. What the internet gets wrong (his own hedge on the lamp)

> "the experimental verification of the law, whatever it may be, would be exceedingly difficult. One thing is certain, at any rate, and that is, that in augmenting the potential and frequency we rapidly intensify the streams ; and, though it may be very sanguine, it is surely not altogether hopeless to expect that we may succeed in producing a practical illuminant on these lines"

- row: 94
- cited as: `(1894, p. 213)`
- straddle: this ONE fragment sits on printed pp. 213-214 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches its citation regex
- why: the hedge, verbatim, and it is the sentence the whole lamp section should be read through: 'though it may be very sanguine', 'surely not altogether hopeless'. Double negatives are his own caution, and the article should print them rather than paraphrase them as optimism. The fragment straddles printed pp. 213-214 as one run; cite one page. The missing word at the page break ('exceedingly difficult') is on p. 214 and the matcher joins it. Article 06's rendered page already prints the first clause of this sentence with a p. 213 cite; read the flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT
- check_quotes.py: exact match, ratio 1.0, printed p. 213 (this ONE fragment straddles printed pp. 213-214; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `ric impulses. My opinion is that the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential, but the experimental verification of the law, whatever it may be, would be exceedingly`

## Printed p. 214 (scan file 232, 18 leaves of offset)

### 3. Tesla's lamp research (what he thought the lamp would be)

> "We would then be simply using burners or flames, in which there would be no chemical process, no consumption of material, but merely a transfer of energy"

- row: 95
- cited as: `(1894, p. 214)`
- why: the claim of the whole gas-lamp idea in one line, and it is a claim about a TRANSFER of energy, not a creation of it - the same word as the p. 175 and p. 289 rows. It is also the sentence that makes the article's bridge to the free-energy pages legitimate rather than decorative: he is describing a device that consumes nothing, and he is careful to call it a transfer. 'burners or flames' is his own framing, which article 06's cold-flame page owns as a topic - read the flag ARTICLE 06 OWNS THE COLD FLAME
- check_quotes.py: exact match, ratio 1.0, printed p. 214
- raw OCR: `requency we rapidly intensify the streams ; and, though it may be very sanguine, it is surely not altogether hopeless to expect that we may succeed in producing a practical illuminant on these lines. We would then be simply using burners or flames, in which there would be no chemical process, no consumption of material, but merely a transfer of energy, and which would, in all probability, emit more light and less heat than ordinary flames. The luminous intensity of the streams is, of course, considerably FIG. 137. increased when they are focused u`

## Printed p. 253 (scan file 271, 18 leaves of offset)

### 3. Tesla's lamp research (how many trials, and what worked)

> "In the course of these experiments a great many trials were made with all kinds of carbon buttons. Electrodes made of ordinary carbon buttons were decidedly more durable when the buttons were obtained by the application of enormous pressure"

- row: 96
- cited as: `(1894, p. 253)`
- why: the scale claim, in his words: 'a great many trials', with all kinds of carbon. It is not a number, and the article must not make it one. The finding attached to it is a materials fact he can state as observed: pressure-sintered buttons lasted longer. This is the sentence that licenses 'he tested many materials' and no more than that
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 253 In the course of these experiments a great many trials were made with all kinds of carbon buttons. Electrodes made of ordinary carbon buttons were decidedly more durable when the buttons were obtained by the application of enormous pressure. Electrodes prepared by depositing carbon in well known ways did not show up well ; they blackened the globe very quickly. From many experiences I conclude that lamp filaments obtained in this manner`

### 3. Tesla's lamp research (what the bombardment does to the button)

> "there can be no doubt that all kinds of carbon are fused under the molecular bombardment, but the liquid state must be one of great instability"

- row: 97
- cited as: `(1894, p. 253)`
- why: the mechanism of the lamp, from the other end: the gas molecules do not gently warm the button, they fuse it, and the fused state is unstable. That is the physical reason the lamp is hard, and it is stated as an inference from observation ('there can be no doubt', 'must be'). Pair it with the p. 401 heating-of-the-glass row and the p. 175 'invisible hammers' row: three pages, one mechanism, described from three angles
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `order to bring them to the point of fusion, it is necessary to employ very small buttons. In this case the observation isrendered very difficult on account of the intense heat produced. Nevertheless there can be no doubt that all kinds of carbon are fused under the molecular bombardment, but the liquid state must be one of great instability. Of all the bodies tried there were two which withstood best — diamond and carborundum. These two showed up about equally, but the latter was preferable for many reasons. As it is more than likely th`

### 3. Tesla's lamp research (the two winners, and the comparison)

> "Of all the bodies tried there were two which withstood best - diamond and carborundum. These two showed up about equally, but the latter was preferable for many reasons"

- row: 98
- cited as: `(1894, p. 253)`
- why: brief 12 item 3's starting point, and it is a comparison between two materials with a result attached: diamond and carborundum came out about equal, and carborundum was preferred 'for many reasons' - which he does not enumerate here. 'Showed up about equally' is the plainest comparative statement in the passage and it has no number on it, which is exactly the shape the article should report. The print sets an em dash around 'diamond and carborundum'; the form above is the ASCII form the normaliser folds, and the draft must not print a dash (section 0 non-negotiable 5)
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `on account of the intense heat produced. Nevertheless there can be no doubt that all kinds of carbon are fused under the molecular bombardment, but the liquid state must be one of great instability. Of all the bodies tried there were two which withstood best — diamond and carborundum. These two showed up about equally, but the latter was preferable for many reasons. As it is more than likely that this body is not yet generally known, I Avill venture to c`

### 3. Tesla's lamp research (the lecture turns to a new material)

> "As it is more than likely that this body is not yet generally known, I Avill venture to call your attention to it"

- row: 99
- cited as: `(1894, p. 253)`
- why: the pivot in the lecture: he stops talking about his own apparatus and starts explaining a commercial product. It is also a clean example of an OCR defect the space-ignoring index cannot repair - the print reads 'Will' and the OCR prints 'Avill' (a V for W), so the quote carries the scan's letters and the draft either prints them or cuts the word. Read the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `be one of great instability. Of all the bodies tried there were two which withstood best — diamond and carborundum. These two showed up about equally, but the latter was preferable for many reasons. As it is more than likely that this body is not yet generally known, I Avill venture to call your attention to it. It has been recently produced by Mr. E. G. Acheson, of Monongahela City, Pa., II. S. A. It is intended to replace ordinary diamond powder for polishing precious stones, etc., and I have been informe`

### 3. Tesla's lamp research (where the material came from)

> "It has been recently produced by Mr. E. G. Acheson, of Monongahela City, Pa., II. S. A."

- row: 100
- cited as: `(1894, p. 253)`
- why: the supply chain of the lamp research, in one line: Acheson, Monongahela City, and the carborundum company's town. This is the fact that keeps the lamp section from being only an idea - a named manufacturer was already making the stuff in 1892. The OCR prints 'II. S. A.' for 'U. S. A.'; quote it as set or write 'U. S. A.' and say the scan is broken. Same defect class as the row above
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `. These two showed up about equally, but the latter was preferable for many reasons. As it is more than likely that this body is not yet generally known, I Avill venture to call your attention to it. It has been recently produced by Mr. E. G. Acheson, of Monongahela City, Pa., II. S. A. It is intended to replace ordinary diamond powder for polishing precious stones, etc., and I have been informed that it accomplishes this object quite succes ful y. Ido not know why the name " carbo`

### 3. Tesla's lamp research (the two tests he actually ran)

> "Through the kindness of the inventor, I obtained a short while ago some samples which I desired to test in regard to their qualities of phosphorescence and capability of withstanding high degrees of heat"

- row: 101
- cited as: `(1894, p. 253)`
- why: the two properties he set out to test, in his own sentence, and the source of the samples: the inventor sent them. 'Test' appears 5 times in printed pp. 253-259 (measured), and this is the sentence that says what the testing was for. It is also the bridge from beat 2 to beat 3: the reason he cares about a material that withstands bombardment is that the tube's own glass gets hot
- check_quotes.py: exact match, ratio 1.0, printed p. 253
- raw OCR: `ccomplishes this object quite succes ful y. Ido not know why the name " carborundum " has been given to it, unless there is something in the process of its manufacture which justifies this selection. Through the kindness of the inventor, I obtained a short while ago some samples which I desired to test in regard to their qualities of phosphorescence and capability of withstanding high degrees of heat. Carborundum can be obtained in two forms — in the form of "crystals" and of powder. The former appear to the naked eye dark colored, but are very brilliant ; the latter is of nearly the same color a`

## Printed p. 254 (scan file 272, 18 leaves of offset)

### 3. Tesla's lamp research (he says the study was not satisfactory)

> "The time has been too short to make a satisfactory study of the properties of this product, but enough experience has been gained in a few weeks I have experimented upon it to say that it does possess some remarkable properties in many respects"

- row: 102
- cited as: `(1894, p. 254)`
- why: the hedge on the whole lamp section, and it is printed in the middle of the passage, not at the end: the study was not satisfactory, the material had been in his hands a few weeks. Any sentence in the draft that reports a carborundum result has to be read against this sentence. It is the fourth of the four ways he records his own unfinished work - read the flag HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS. The sentence is ungrammatical as printed ('gained in a few weeks I have experimented upon it'); quote it as set or cut, do not repair it
- check_quotes.py: exact match, ratio 1.0, printed p. 254
- raw OCR: `nduct very well, but not as well as ordinary carbon. The powder, which is obtained from the crystals in some way, is practically non-conducting. Itaffords a magnificent polishing material for stones. The time has been too short to make a satisfactory study of the properties of this product, but enough experience has been gained in a few weeks I have experimented upon it to say that it does possess some remarkable properties in many respects. It withstands excessively high degrees of heat, it is little deteriorated by molecular bombardment, and it does not blacken the globe as ordinary carbon does. The only difficulty which I have experi`

### 3. Tesla's lamp research (the actual engineering obstacle)

> "The only difficulty which I have experienced in its use in connection with these experiments was to find some binding material which would resist the heat and the effect of the bombardment as successfully as carborundum itself does"

- row: 103
- cited as: `(1894, p. 254)`
- why: the real problem, stated by him as the only one: not the button, the glue. This is the sentence that answers 'why is there no carborundum lamp' without inventing a cause, and it is a claim about a specific failure mode, not a general pessimism. The word 'only' is his
- check_quotes.py: exact match, ratio 1.0, printed p. 254
- raw OCR: `remarkable properties in many respects. It withstands excessively high degrees of heat, it is little deteriorated by molecular bombardment, and it does not blacken the globe as ordinary carbon does. The only difficulty which I have experienced in its use in connection with these experiments was to find some binding material which would resist the heat and the effect of the bombardment as successfully as carborundum itself does. I have here a number of bulbs which I have provided with buttons of carborundum. To make such a button of carborundum crystals I proceed in the following manner: I take an ordinary lamp filament and`

### 3. Tesla's lamp research (the objects on the lecture table)

> "I have here a number of bulbs which I have provided with buttons of carborundum"

- row: 104
- cited as: `(1894, p. 254)`
- why: the showmanship half of the lamp passage: he is holding the things while he says it. It is the same rhetorical move as the p. 288 tube-in-hand demo, one chapter later and about a lamp, and the article can put the two in the same paragraph because both are in the same lecture. Nothing here claims the bulbs worked
- check_quotes.py: exact match, ratio 1.0, printed p. 254
- raw OCR: `experienced in its use in connection with these experiments was to find some binding material which would resist the heat and the effect of the bombardment as successfully as carborundum itself does. I have here a number of bulbs which I have provided with buttons of carborundum. To make such a button of carborundum crystals I proceed in the following manner: I take an ordinary lamp filament and dip its point in tar, or some other thick substance or paint which may be readil`

### 3. Tesla's lamp research (the process, in his words)

> "I take an ordinary lamp filament and dip its point in tar, or some other thick substance or paint which may be readily carbonized"

- row: 105
- cited as: `(1894, p. 254)`
- why: the method in one step, and it is a workshop method: a lamp filament, tar, a hot plate. The binder is tar, which is why the sentence above about a binding material matters. Quote the process rather than summarising it; the summarised version always sounds more engineered than it was
- check_quotes.py: exact match, ratio 1.0, printed p. 254
- raw OCR: `cessfully as carborundum itself does. I have here a number of bulbs which I have provided with buttons of carborundum. To make such a button of carborundum crystals I proceed in the following manner: I take an ordinary lamp filament and dip its point in tar, or some other thick substance or paint which may be readily carbonized. I next pass the point of the filament through the crystals, and then hold it vertically over a hot plate. The tar softens and forms a drop on the point of the filament, the crystals adhering to the`

### 3. Tesla's lamp research (the vacuum step, and the beating)

> "The button being mounted in a bulb, when a good vacuum has been reached, first a weak and then a strong discharge is passed through the bulb to carbonize the tar and expel all gases, and later it is brought to a very intense incandescence"

- row: 106
- cited as: `(1894, p. 254)`
- why: the making of the lamp, and it is a vacuum procedure: pump it down, then a weak discharge, then a strong one, then incandescence. This is the practical counterpart of brief 12 item 4's vacuum problem - the same exhausted-globe requirement shows up here as a manufacturing step, with 'a good vacuum' as the condition and no number attached to it
- check_quotes.py: exact match, ratio 1.0, printed p. 254
- raw OCR: `d mass which firmly binds the crystals. When a larger button is required I repeat the process several times, and I generally also cover the filament a certain distance below the button with crystals. The button being mounted in a bulb, when a good vacuum has been reached, first a weak and then a strong discharge is passed through the bulb to carbonize the tar and expel all gases, and later it is brought to a very intense incandescence. When the powder is used I have found it best to proceed as follows : I make a thick paint of carborundum and tar, and pass a lamp filament through the paint. Taking then most of the`

## Printed p. 255 (scan file 273, 18 leaves of offset)

### 3. Tesla's lamp research (why the lamp did not work)

> "The difficulty is that the binding material gives way, and the carborundum is slowly thrown off after some time"

- row: 107
- cited as: `(1894, p. 255)`
- why: the failure, in one sentence, with the mechanism named: the binder lets go and the material is sputtered off. 'After some time' is his only durability measure, and it is not a measure - the article must not turn it into a lifetime. This is the sentence that makes the lamp section an honest one, and it belongs next to the ambition sentence below, not instead of it
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `that such a button — properly prepared under great pressure — of carborundum, especially of powder of the best quality, will withstand the effect of the bombardment fully as well as anything we know. The difficulty is that the binding material gives way, and the carborundum is slowly thrown off after some time. As it does not seem to blacken the globe in the least, it might be found useful for coating the filaments of ordinary incandescent lamps, and I think that it is even possible to produce thin threads`

### 3. Tesla's lamp research (the brief's quote, with its hedge attached)

> "it might be found useful for coating the filaments of ordinary incandescent lamps, and I think that it is even possible to produce thin threads or sticks of carborundum which will replace the ordinary filaments in an incandescent lamp"

- row: 108
- cited as: `(1894, p. 255)`
- why: brief 12 item 3's first quoted fragment, verbatim, and the words that carry it: 'might be found useful', 'I think that it is even possible'. The plan quotes 'thin threads or sticks of carborundum' as if it were a proposal; in print it is the second half of a speculative sentence about coating ordinary lamps. Quote the whole run or do not quote the phrase. This is also the sentence that ties the lamp work to the tube work: the same bombardment that lights a tube is what he is trying to survive
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `ly as well as anything we know. The difficulty is that the binding material gives way, and the carborundum is slowly thrown off after some time. As it does not seem to blacken the globe in the least, it might be found useful for coating the filaments of ordinary incandescent lamps, and I think that it is even possible to produce thin threads or sticks of carborundum which will replace the ordinary filaments in an incandescent lamp. A carborundum coating seems to be more durable than other coatings, not only because the carborundum can withstand high degrees of heat, but also because it seems to unite with the carbon better tha`

### 3. Tesla's lamp research (the brief's second quote, a real comparison)

> "I prepared buttons of diamond dust in the same manner as of carborundum, and these came in durability nearest to those prepared of carborundum, but the binding paste gave way much more quickly in the diamond buttons"

- row: 109
- cited as: `(1894, p. 255)`
- why: brief 12 item 3's second quoted fragment, verbatim, and it is the closest thing in the volume to a materials trial with a ranking: diamond dust came nearest to carborundum, and both failed at the binder. 'Came in durability nearest to' is a comparative with no number, and 'much more quickly' is a second comparative with no number. The article may print the ranking; it may not print a lifetime, a rate, or a percentage
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `degrees of heat, but also because it seems to unite with the carbon better than any other material I have tried. A coating of zirconia or any other oxide, for instance, is far more quickly destroyed. I prepared buttons of diamond dust in the same manner as of carborundum, and these came in durability nearest to those prepared of carborundum, but the binding paste gave way much more quickly in the diamond buttons ; this, however, I attributed to the size and irregularity of the grains of the diamond. It was of interest to find whether carborundum possesses the quality of phosphorescence. One is, of course, pr`

### 3. Tesla's lamp research (his explanation of the diamond failure)

> "this, however, I attributed to the size and irregularity of the grains of the diamond"

- row: 110
- cited as: `(1894, p. 255)`
- why: 'I attributed' again - the fourth inference verb in this article's sources, after 'argues for', 'speak for' and 'I would say'. It is the same habit as the p. 402 nodes sentence and the p. 400 tinfoil sentence: he names a cause and marks it as his own attribution. The article should print the marker with the cause
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `of diamond dust in the same manner as of carborundum, and these came in durability nearest to those prepared of carborundum, but the binding paste gave way much more quickly in the diamond buttons ; this, however, I attributed to the size and irregularity of the grains of the diamond. It was of interest to find whether carborundum possesses the quality of phosphorescence. One is, of course, prepared to encounter two difficulties : first, as regards the rough product, the "crystal`

### 3. Tesla's lamp research (the question he asked the material)

> "It was of interest to find whether carborundum possesses the quality of phosphorescence"

- row: 111
- cited as: `(1894, p. 255)`
- why: the research question, stated as research: does this substance phosphoresce. It is the sentence that connects the lamp passage to the phosphorescent-bulb material at printed p. 290 and to the coating question in brief 12 item 2, and it is the reason the word 'phosphorescence' appears 10 times inside printed pp. 253-259 (measured). Keep the framing: he is asking, not reporting
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `rest to those prepared of carborundum, but the binding paste gave way much more quickly in the diamond buttons ; this, however, I attributed to the size and irregularity of the grains of the diamond. It was of interest to find whether carborundum possesses the quality of phosphorescence. One is, of course, prepared to encounter two difficulties : first, as regards the rough product, the "crystals," they are good conducting, and it is a fact that conductors do not phosphoresce; secon`

### 3. Tesla's lamp research (the physics constraint he runs into)

> "they are good conducting, and it is a fact that conductors do not phosphoresce"

- row: 112
- cited as: `(1894, p. 255)`
- why: the reason the rough product cannot answer the question: conducting materials do not phosphoresce, and the crystals conduct. 'It is a fact that' is a claim about the state of knowledge, not a measurement, and the sentence is a dead end he reports as a dead end. This is the honest shape of a negative result and the article can use it as one
- check_quotes.py: exact match, ratio 1.0, printed p. 255
- raw OCR: `was of interest to find whether carborundum possesses the quality of phosphorescence. One is, of course, prepared to encounter two difficulties : first, as regards the rough product, the "crystals," they are good conducting, and it is a fact that conductors do not phosphoresce; second, the powder, being exceedingly fine, would not be apt to exhibit very prominently this quality, since we know that when crystals, even such as diamond or ruby, are finely powdered, they lose`

## Printed p. 288 (scan file 306, 18 leaves of offset)

### 1. The strangest demo (the sentence the article opens on)

> "I take a tube in my hand and move it about, and it is lighted wherever I may hold it; throughout space the invisible forces act"

- row: 18
- cited as: `(1894, p. 288)`
- why: brief 12 item 1's hook, verbatim, and the only sentence of the four the brief quotes from p. 288 that article 01's live page does NOT already print. Present tense on a stage, first person, no apparatus named. Note the semicolon: the print runs the two clauses as one sentence, and the draft's voice rule forbids dashes, so keep the semicolon or split the sentence and cite both halves
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `y those which are noted in an electrostatic field acting through considerable distance; and the best an unskilled lecturer can do is to begin and finish with the exhibition of these singular effects. I take a tube in my hand and move it about, and it is lighted wherever I may hold it; throughout space the invisible forces act. But I may take another tube and it might not light, the vacuum being very high. I excite it by means of a disruptive discharge coil, and now it will light in the electrostatic FIG. 163. FIG. 164. fi`

### 4. The vacuum problem (the second tube, on the same table)

> "But I may take another tube and it might not light, the vacuum being very high"

- row: 19
- cited as: `(1894, p. 288)`
- why: brief 12 item 4's evidence, and it is the same paragraph as the hook: the demo that fails, on the same page, in the same breath. Article 01's page PARAPHRASES this ('A tube with too high a vacuum will not light in the electrostatic field until it has been excited by a disruptive discharge coil') and quotes the next sentence but one; the verbatim wording is free here. The comma before 'the vacuum being very high' is the print's causal clause - it is the explanation, not an aside
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `is to begin and finish with the exhibition of these singular effects. I take a tube in my hand and move it about, and it is lighted wherever I may hold it; throughout space the invisible forces act. But I may take another tube and it might not light, the vacuum being very high. I excite it by means of a disruptive discharge coil, and now it will light in the electrostatic FIG. 163. FIG. 164. field. I may put it away for a few weeks or months, still it retains the faculty o`

### 4. The vacuum problem (what fixes it, in his words)

> "I excite it by means of a disruptive discharge coil, and now it will light in the electrostatic field"

- row: 20
- cited as: `(1894, p. 288)`
- why: the action that changes the tube from dark to lit. The phrase 'excite it by means of a disruptive discharge coil' returns 1 hit in this text (measured), which is as near to a named procedure as the volume gets. 'Excited' is the book's technical word throughout chapter XXXII too, so this sentence and the p. 396 definition use the same verb; the draft can build on that consistency instead of inventing one
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `tube in my hand and move it about, and it is lighted wherever I may hold it; throughout space the invisible forces act. But I may take another tube and it might not light, the vacuum being very high. I excite it by means of a disruptive discharge coil, and now it will light in the electrostatic FIG. 163. FIG. 164. field. I may put it away for a few weeks or months, still it retains the faculty of being excited. What change have I produced in the tube in the act of exciting it? If a motion i`

### 4. The vacuum problem (the persistence)

> "I may put it away for a few weeks or months, still it retains the faculty of being excited"

- row: 21
- cited as: `(1894, p. 288)`
- why: the part of the demo that is actually strange, and the sentence article 01 already prints with a page cite. It is pinned here because brief 12 item 1 quotes it in the plan, and because the article cannot answer 'what changed' without it. The draft must NOT re-quote it as if it were new: cite it as the same passage article 01 has, or link to that page. Read the flag ARTICLE 01 OWNS THE p. 288 SENTENCES IT HAS ALREADY PRINTED
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `I may take another tube and it might not light, the vacuum being very high. I excite it by means of a disruptive discharge coil, and now it will light in the electrostatic FIG. 163. FIG. 164. field. I may put it away for a few weeks or months, still it retains the faculty of being excited. What change have I produced in the tube in the act of exciting it? If a motion imparted to atoms, it is difficult to perceive how it can persist so long without being arrested by f rictional losses`

### 1. The strangest demo (the question he leaves open)

> "What change have I produced in the tube in the act of exciting it?"

- row: 22
- cited as: `(1894, p. 288)`
- why: the question he asks his own audience and does not answer. It is the hinge of brief 12 item 5: the honest article does not answer it either, it reports that it was asked in 1892 and answers it differently now. Article 01's page ends its p. 288 quote at this question mark, so the answer half below is the part that has not been used
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `means of a disruptive discharge coil, and now it will light in the electrostatic FIG. 163. FIG. 164. field. I may put it away for a few weeks or months, still it retains the faculty of being excited. What change have I produced in the tube in the act of exciting it? If a motion imparted to atoms, it is difficult to perceive how it can persist so long without being arrested by f rictional losses ; and if a strain exerted in the dielectric, such as a simple electr`

### 5. What the internet gets wrong (his first hypothesis, and his reason for doubting it)

> "If a motion imparted to atoms, it is difficult to perceive how it can persist so long without being arrested by f rictional losses"

- row: 23
- cited as: `(1894, p. 288)`
- why: the first of the two explanations he weighs, and his reason for doubting it: frictional losses. The OCR breaks 'frictional' as 'f rictional' with a space after the f, which is a scan artefact of the line break, so the quote carries it and the draft prints 'frictional' - this verifies through the space-ignoring index only, and check_quotes.py flags it the same way. The sentence is ungrammatical as printed ('If a motion imparted to atoms') because the print continues from the previous clause; see the raw window
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `electrostatic FIG. 163. FIG. 164. field. I may put it away for a few weeks or months, still it retains the faculty of being excited. What change have I produced in the tube in the act of exciting it? If a motion imparted to atoms, it is difficult to perceive how it can persist so long without being arrested by f rictional losses ; and if a strain exerted in the dielectric, such as a simple electrification would produce, it is easy to see how it may persist indefinitely, but very difficult to understand why such a condition s`

### 5. What the internet gets wrong (his second hypothesis, and the part that still fits)

> "if a strain exerted in the dielectric, such as a simple electrification would produce, it is easy to see how it may persist indefinitely, but very difficult to understand why such a condition should aid the excitation when we have to deal with potentials which are rapidly alternating"

- row: 24
- cited as: `(1894, p. 288)`
- why: the second explanation, and the one that survives: a strain in the dielectric, i.e. charge, persists indefinitely. He rejects it only because of the alternating potentials, which is exactly the part a modern reader can resolve (the excitation is not the stored charge). This is the single best quote for brief 12 item 5's 'a charge/ionisation state, not stored free power', because it is him reasoning toward it and stopping one step short for a reason we now know is fixable
- check_quotes.py: exact match, ratio 1.0, printed p. 288
- raw OCR: `change have I produced in the tube in the act of exciting it? If a motion imparted to atoms, it is difficult to perceive how it can persist so long without being arrested by f rictional losses ; and if a strain exerted in the dielectric, such as a simple electrification would produce, it is easy to see how it may persist indefinitely, but very difficult to understand why such a condition should aid the excitation when we have to deal with potentials which are rapidly alternating.`

## Printed p. 289 (scan file 307, 18 leaves of offset)

### 1. The strangest demo (what he did after the applause)

> "Since I have exhibited these phenomena for the first time, I have obtained some other interesting effects"

- row: 25
- cited as: `(1894, p. 289)`
- why: the sentence that turns the demo into a program: the next paragraph is the work, not the show. It dates the field-incandescence results as after his first exhibition of these effects, which is the London lecture of February 1892 itself - so 'since I have exhibited' means within weeks of the lecture. Useful for the article's second act without inventing a timeline
- check_quotes.py: exact match, ratio 1.0, printed p. 289
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 289 Since I have exhibited these phenomena for the first time, I have obtained some other interesting effects. For instance, I have produced the incandescence of a button, filament, or wire enclosed in a tube. To get to this result it was necessary to economize the energy which is obtained from the field, an`

### 2. Why a tube lights with no wires (the two ways, in one sentence)

> "These coatings are merely used to enable me to perform two experiments with the tube - namely, to produce the effect desired either by direct connection of the body of the experimenter or of another body to the wire w, or by acting inductively through the glass"

- row: 26
- cited as: `(1894, p. 289)`
- why: the cleanest statement in the volume that there are two distinct mechanisms on the same table: contact with the body, or induction through the glass. Brief 12 item 2 has to separate them or the reader conflates the body-as-wire case with the field case; this sentence is his own separation, and 'merely' is his own lowering of the coatings to a convenience. The dashes are the print's em dashes, ASCII form above
- check_quotes.py: exact match, ratio 1.0, printed p. 289
- raw OCR: `copper wire w. The tube is provided with outside and inside coatings, c and GJ, respectively, and is filled as far as the coatings reach with conducting, and the space above with insulating, powder. These coatings are merely used to enable me to perform two experiments with the tube — namely, to produce the effect desired either by direct connection of the body of the experimenter or of another body to the wire w, or by acting inductively through the glass. The stem s is provide`

### 5. What the internet gets wrong (the energy comes from the field, in his words)

> "I have produced the incandescence of a button, filament, or wire enclosed in a tube. To get to this result it was necessary to economize the energy which is obtained from the field, and direct most of it on the small body to be rendered incandescent"

- row: 27
- cited as: `(1894, p. 289)`
- why: brief 12 item 5's central correction, stated by him: the energy is obtained FROM THE FIELD and economised, not created in the tube. 'A necessary to economize' is the verb of a conservation argument, and it is on the same page as the tube-in-hand demo the myth is built on. This is the row to quote if the article quotes only one sentence against 'light without energy'
- check_quotes.py: exact match, ratio 1.0, printed p. 289
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 289 Since I have exhibited these phenomena for the first time, I have obtained some other interesting effects. For instance, I have produced the incandescence of a button, filament, or wire enclosed in a tube. To get to this result it was necessary to economize the energy which is obtained from the field, and direct most of it on the small body to be rendered incandescent. At the beginning the task appeared difficult, but the experiences gathered permitted me to reach the result easily. In Fig. 163 and Fig. 164, two such tubes are illustrated, which are prepared for t`

### 1. The strangest demo (the bulb on a plate, not in the hand)

> "Intense phosphorescence may be excited in a bulb by merely connecting it to a plate within the field, and the plate need not be any larger than an ordinary lamp shade"

- row: 28
- cited as: `(1894, p. 289)`
- why: the version of the demo that does not need a person in it, and the size of the electrode: a lamp shade. Brief 12 item 2's mechanism, in a demonstration. Article 01's page covers the plate-as-circuit-part at printed pp. 183-184 from the New York lecture; this is the London lecture of 1892 saying the same thing a year later with a bigger object, which is the point the article can make about why the trick scales
- check_quotes.py: exact match, ratio 1.0, printed p. 289
- raw OCR: `, is bent properly and fastened to the aluminum tube. When the glass tube is held anywhere in the electrostatic field the platinum wire becomes incandescent, and the mica vanes are rotated very fast. Intense phosphorescence may be excited in a bulb by merely connecting it to a plate within the field, and the plate need not be any larger than an ordinary lamp shade. The phosphorescence excited with these currents is incomparably more powerful than with ordinary apparatus. A small phosphorescent bulb, when attached to a wire connected to a coil, emits sufficient`

### 1. The strangest demo (the one brightness claim on the page)

> "A small phosphorescent bulb, when attached to a wire connected to a coil, emits sufficient light to allow reading ordinary print at a distance of five to six paces"

- row: 29
- cited as: `(1894, p. 289)`
- straddle: this ONE fragment sits on printed pp. 289-290 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches its citation regex
- why: the only brightness number in the demo passage: readable print at five to six paces. It is a comparison, not a measurement, and it is the number the article can print where chapter XXXII gives none (see the scoped-absence table). The fragment straddles printed pp. 289-290 as one run, so cite one page only
- check_quotes.py: exact match, ratio 1.0, printed p. 289 (this ONE fragment straddles printed pp. 289-290; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `a plate within the field, and the plate need not be any larger than an ordinary lamp shade. The phosphorescence excited with these currents is incomparably more powerful than with ordinary apparatus. A small phosphorescent bulb, when attached to a wire connected to a coil, emits sufficient light`

## Printed p. 290 (scan file 308, 18 leaves of offset)

### 1. The strangest demo (Crookes lent him the bulbs)

> "It was of interest to see how some of the phosphorescent bulbs of Professor Crookes would behave with these currents, and he has had the kindness to lend me a few for the occasion"

- row: 30
- cited as: `(1894, p. 290)`
- why: the human fact behind the demo, and the link to the one Crookes quote the series already prints (article 10's p. 236 'Crookes came nearest to doing it'). Here the two men are in the same room by proxy: Crookes lent the apparatus for the London lecture. Nothing in the volume says Crookes approved of Tesla's conclusions, and the article must not imply it
- check_quotes.py: exact match, ratio 1.0, printed p. 290
- raw OCR: `290 INVENTIONS OF NIKOLA TESLA. to allow reading ordinary print at a distance of five to six paces. It was of interest to see how some of the phosphorescent bulbs of Professor Crookes would behave with these currents, and he has had the kindness to lend me a few for the occasion. The effects produced are magnificent, especially by the sulphide of calcium and sulphide of zinc. With the disruptive discharge coil they glow intensely merely by holding them in the hand and connec`

### 1. The strangest demo (which coatings worked)

> "The effects produced are magnificent, especially by the sulphide of calcium and sulphide of zinc"

- row: 31
- cited as: `(1894, p. 290)`
- why: the two phosphor coatings he names, which is the substance behind brief 12 item 2's 'phosphorescent coatings'. A specific material fact from the page, not a description of glow. Note the word 'magnificent' is about a visual effect on a stage, and is the kind of adjective the article should attribute rather than adopt
- check_quotes.py: exact match, ratio 1.0, printed p. 290
- raw OCR: `five to six paces. It was of interest to see how some of the phosphorescent bulbs of Professor Crookes would behave with these currents, and he has had the kindness to lend me a few for the occasion. The effects produced are magnificent, especially by the sulphide of calcium and sulphide of zinc. With the disruptive discharge coil they glow intensely merely by holding them in the hand and connecting the body to the terminal of the coil. To whatever results investigations of this kind may lea`

### 1. The strangest demo (the bulbs in the hand, again)

> "With the disruptive discharge coil they glow intensely merely by holding them in the hand and connecting the body to the terminal of the coil"

- row: 32
- cited as: `(1894, p. 290)`
- why: the mechanism of the hand-lit bulb in one clause: hold it, connect the body to one terminal. Same page as the Crookes bulbs, so the article can put the mechanism and the object in one paragraph without stitching two pages. 'Merely' again does the work brief 12 item 5 needs: no mystery apparatus, just a body and a terminal
- check_quotes.py: exact match, ratio 1.0, printed p. 290
- raw OCR: `okes would behave with these currents, and he has had the kindness to lend me a few for the occasion. The effects produced are magnificent, especially by the sulphide of calcium and sulphide of zinc. With the disruptive discharge coil they glow intensely merely by holding them in the hand and connecting the body to the terminal of the coil. To whatever results investigations of this kind may lead, the chief interest lies, for the present, in the possibilities they offer for the production of an efficient illuminating device. In no bran`

## Printed p. 292 (scan file 310, 18 leaves of offset)

### 5. What the internet gets wrong (what he says the lecture was for)

> "It has been, my chief aim in presenting these results to point out phenomena or features of novelty, and to advance ideas which I am hopeful will serve as starting points of new departures"

- row: 33
- cited as: `(1894, p. 292)`
- why: his own statement of what the lecture claims: phenomena, features of novelty, ideas as starting points. Not a claim of a working lamp. This is the sentence to close brief 12 item 5 with, because it is the author setting the size of his own claim, on the last page of the chapter. The comma after 'been' is the print's
- check_quotes.py: exact match, ratio 1.0, printed p. 292
- raw OCR: `with the present state of knowledge and the experiences gained, no attempt is being made to disturb the electrostatic or magnetic condition of the earth, and transmit, if nothing else, intelligence. It has been, my chief aim in presenting these results to point out phenomena or features of novelty, and to advance ideas which I am hopeful will serve as starting points of new departures. It has been my chief desire this evening to entertain you with some novel experiments. Your applause, so frequently and generously accorded, has told me that I have succeeded. In conclusion, let me`

## Printed p. 293 (scan file 311, 18 leaves of offset)

### 0. Provenance (the last page of the lecture)

> "the pleasure I have had in presenting these results to a gathering of so many able men"

- row: 34
- cited as: `(1894, p. 293)`
- why: the last sentence of chapter XXVII, and the reason the p. 292 row above is the lecture's own closer rather than an editorial summary. Quote it only if the article needs to show the lecture ending on courtesy; it is not evidence of anything technical. The full sentence carries an em dash the draft cannot print - see Rejected #34
- check_quotes.py: exact match, ratio 1.0, printed p. 293
- raw OCR: `HJGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 293 addressing such a distinguished audience, the pleasure I have had in presenting these results to a gathering of so many able men — and among them also some of those in whose work for many years past I have found enlightenment and constant pleasure — I shall never forget.`

## Printed p. 396 (scan file 414, 18 leaves of offset)

### 0. Provenance (ch. XXXII footnote 1, the date of the chapter's main text)

> "Article by Mr. Tesla in The Electrical Engineer. N. Y., July 1, 1891."

- row: 1
- cited as: `(1894, p. 396)`
- why: the footnote that dates the whole first part of chapter XXXII: Tesla's own article, published July 1, 1891, six months before the London lecture the brief's p. 288 quote comes from. This is the earliest first-person account in the volume of lighting a tube with no wires in it, and the only one devoted to it. The print sets a period after 'Engineer' and after 'Y'; quote it as set
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `ight. My investigations in this line occupied me principally during the winter and spring of the past year. During this time many different experiments were performed, and in my exchanges of ideas 1. Article by Mr. Tesla in The Electrical Engineer. N. Y., July 1, 1891.`

### 0. Provenance (ch. XXXII, the date of the work itself)

> "My investigations in this line occupied me principally during the winter and spring of the past year"

- row: 2
- cited as: `(1894, p. 396)`
- why: the article's own date for the bench work: the winter and spring before July 1891, so spring 1891 at the latest. It is the only date for the work in this chapter, and it is earlier than the May 20, 1891 New York lecture the same volume prints as chapter XXVI, which makes the priority question in the chapter a question about who published first, not who thought first. Say 'he says' - the sentence is his, the date inside it is relative to the footnote above it
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `d who has been the first to make his results known. These peculiarities noted by me would seem to be at variance with the views of Prof. J. J. Thomson, and present the phenomena in a different light. My investigations in this line occupied me principally during the winter and spring of the past year. During this time many different experiments were performed, and in my exchanges of ideas 1. Article by Mr. Tesla in The Electrical Engineer. N. Y., July 1, 1891.`

### 0. Provenance (ch. XXXII opening, the occasion of the article)

> "In The Electrical Engineer of June 10 I have noted the description of some experiments of Prof. J. J. Thomson, on the"

- row: 3
- cited as: `(1894, p. 396)`
- why: the sentence that starts the chapter, and the reason it exists: a trade paper reported J. J. Thomson's experiments and Tesla wrote in about them. The quoted title that follows is in the print's own quote marks, which would split the run in check_quotes.py's scanner, so the quote stops at 'on the'. See the flag THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `CHAPTEE XXXII. ELECTRIC DISCHARGE IN VACUUM TUBES.* IN The Electrical Engineer of June 10 I have noted the description of some experiments of Prof. J. J. Thomson, on the " Electric Discharge in Vacuum Tubes," and in your issue of June 24 Prof. Elihu Thomson describes an experiment`

### 0. Provenance (ch. XXXII opening, the second Thomson)

> "in your issue of June 24 Prof. Elihu Thomson describes an experiment of the same kind"

- row: 4
- cited as: `(1894, p. 396)`
- why: the trap in this chapter's prose: 'Prof. Thomson' unqualified is J. J., and Elihu Thomson is a different man, a different experiment, in the same issue run. The chapter names both within two sentences. Any draft sentence about 'Thomson' has to say which one. Read the flag TWO THOMSONS IN ONE PARAGRAPH
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `. ELECTRIC DISCHARGE IN VACUUM TUBES.* IN The Electrical Engineer of June 10 I have noted the description of some experiments of Prof. J. J. Thomson, on the " Electric Discharge in Vacuum Tubes," and in your issue of June 24 Prof. Elihu Thomson describes an experiment of the same kind. The fundamental idea in these experiments is to set up an electromotive force in a vacuum tube — preferably devoid of any electrodes — by means of electro-magnetic induction, and to excite the tube`

### 2. Why a tube lights with no wires (the definition of the thing)

> "The fundamental idea in these experiments is to set up an electromotive force in a vacuum tube - preferably devoid of any electrodes - by means of electro-magnetic induction, and to excite the tube in this manner"

- row: 5
- cited as: `(1894, p. 396)`
- why: the one sentence in the volume that defines the whole subject in the article's own terms: an EMF set up inside a tube with no electrodes in it. Brief 12 item 2 asks what is happening in a tube with no wires; this is the 1891 description of the setup. The print's dashes around 'preferably devoid of any electrodes' are em dashes; the form above uses the ASCII form the normaliser folds, and the draft must print commas or brackets, not dashes (section 0 non-negotiable 5)
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `ed the description of some experiments of Prof. J. J. Thomson, on the " Electric Discharge in Vacuum Tubes," and in your issue of June 24 Prof. Elihu Thomson describes an experiment of the same kind. The fundamental idea in these experiments is to set up an electromotive force in a vacuum tube — preferably devoid of any electrodes — by means of electro-magnetic induction, and to excite the tube in this manner. As I view the subject I should, think that to any experimenter who had carefully`

### 2. Why a tube lights with no wires (the tube as a condenser, in his words)

> "the idea of replacing the tinfoil coatings of a Leyden jar by rarefied gas and exciting luminosity in the condenser thus obtained by repeatedly charging and discharging it"

- row: 6
- cited as: `(1894, p. 396)`
- why: the closest thing in the book to brief 12 item 2's 'the tube is one plate of a capacitor', and it is his own analogy, not ours: the gas replaces the two coatings of a Leyden jar, so the jar and the tube are the same component. It is inside a sentence about how obvious the idea seemed, so quote it with the sentence's point (see the next row). The book's word is 'condenser'; 'capacitor' is 0 in the volume, table below
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `I should, think that to any experimenter who had carefully studied the problem confronting us and who attempted to find a solution of it, this idea must present itself as naturally as, for instance, the idea of replacing the tinfoil coatings of a Leyden jar by rarefied gas and exciting luminosity in the condenser thus obtained by repeatedly charging and discharging it. The idea being obvious, whatever merit there is in this line of investigation must depend upon the completeness of the study of the subject and the correctness of the observations. The following lin`

### 0. Provenance (ch. XXXII, his own standard for priority)

> "The idea being obvious, whatever merit there is in this line of investigation must depend upon the completeness of the study of the subject and the correctness of the observations"

- row: 7
- cited as: `(1894, p. 396)`
- why: the sentence that governs how this article should talk about priority at all. He concedes the idea was obvious and puts the merit on completeness and correctness of observation. That is the standard the article can hold its own claims to, and it is a quote, not a paraphrase of his character
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `aturally as, for instance, the idea of replacing the tinfoil coatings of a Leyden jar by rarefied gas and exciting luminosity in the condenser thus obtained by repeatedly charging and discharging it. The idea being obvious, whatever merit there is in this line of investigation must depend upon the completeness of the study of the subject and the correctness of the observations. The following lines are not penned with any desire on my part to put myself on record as one who has performed similar experiments, but with a desire to assist other experimenters by pointing out ce`

### 0. Provenance (ch. XXXII, what he says the article is for)

> "The following lines are not penned with any desire on my part to put myself on record as one who has performed similar experiments, but with a desire to assist other experimenters by pointing out certain peculiarities of the phenomena observed"

- row: 8
- cited as: `(1894, p. 396)`
- why: the disclaimant he opens with, and it is the opposite of the claim the myth needs: he is not claiming the discovery, he is claiming observations the other man had not noted. Pair it with the p. 404 row where he says he was misread. Note the print's 'I should, think' stray comma in the sentence before this one - see Rejected #3
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `nd discharging it. The idea being obvious, whatever merit there is in this line of investigation must depend upon the completeness of the study of the subject and the correctness of the observations. The following lines are not penned with any desire on my part to put myself on record as one who has performed similar experiments, but with a desire to assist other experimenters by pointing out certain peculiarities of the phenomena observed, which, to all appearances, have not been noted by Prof. J. J. Thomson, who, however, seems to have gone about systematically in his investigations, and who has been the first to make his results kno`

### 0. Provenance (ch. XXXII, the obvious-idea sentence in full)

> "I should, think that to any experimenter who had carefully studied the problem confronting us and who attempted to find a solution of it, this idea must present itself as naturally as"

- row: 9
- cited as: `(1894, p. 396)`
- why: the first half of the obviousness claim, with the print's stray comma after 'should' inside it. Quote it as set or not at all; a cleaned form does not verify. The sentence runs on into the Leyden-jar comparison, so the two rows above and this one are one paragraph in three pieces
- check_quotes.py: exact match, ratio 1.0, printed p. 396
- raw OCR: `ments is to set up an electromotive force in a vacuum tube — preferably devoid of any electrodes — by means of electro-magnetic induction, and to excite the tube in this manner. As I view the subject I should, think that to any experimenter who had carefully studied the problem confronting us and who attempted to find a solution of it, this idea must present itself as naturally as, for instance, the idea of replacing the tinfoil coatings of a Leyden jar by rarefied gas and exciting luminosity in the condenser thus obtained by repeatedly charging and discharging it. The idea be`

## Printed p. 397 (scan file 415, 18 leaves of offset)

### 2. Why a tube lights with no wires (what happened every time)

> "In all forms of apparatus used there was no special difficulty in exciting a luminous circle or cylinder in proximity to the primary"

- row: 35
- cited as: `(1894, p. 397)`
- why: the base rate of the whole chapter: the effect was not occasional, it reproduced in every form of apparatus he built. The article needs this before it can call anything a result. Note the sentence's second half is a different claim (about the circles' position) and is pinned separately below
- check_quotes.py: exact match, ratio 1.0, printed p. 397
- raw OCR: `used principally with the view of enabling me to place a polished reflecting surface on the inside of the tube, and for this purpose the last turn of the primary was covered with a thin silver sheet. In all forms of apparatus used FIG. 210. there was no special difficulty in exciting a luminous circle or cylinder in proximity to the primary. As to the number of turns, I cannot quite understand why Prof. J. J. Thomson should th`

### 2. Why a tube lights with no wires (the apparatus the brief's figure shows)

> "Fig. 210 may serve as an example of one of the many forms of apparatus used. This consisted of a large glass tube sealed at one end and projecting into an ordinary incandescent lamp bulb"

- row: 36
- cited as: `(1894, p. 397)`
- why: the sentence that describes the brief's first figure, Fig. 210 on printed p. 397, in the book's own words: a large glass tube sealed at one end and projecting INTO an ordinary incandescent lamp bulb. If the article uses that crop it has the caption from the same page, which is what §6.6 wants (read the number off the printed page, and caption from the text beside it). 'one of the many forms' is also his own statement that this was a class of apparatus, not a single device
- check_quotes.py: exact match, ratio 1.0, printed p. 397
- raw OCR: `HIGH POTENTIAL CURRENTS. 397 on this subject with Mr. Alfred S. Brown, of the "Western Union Telegraph Company, various different dispositions were suggested which were carried out by me in practice. Fig. 210 may serve as an example of one of the many forms of apparatus used. This consisted of a large glass tube sealed at one end and projecting into an ordinary incandescent lamp bulb. The primary, usually consisting of a few turns of thick, well-insulated copper sheet was inserted within the tube, the inside space of the bulb furnishing the secondary. This form of apparatus was a`

## Printed p. 398 (scan file 416, 18 leaves of offset)

### 2. Why a tube lights with no wires (the circuit need not be closed)

> "To excite luminosity in the tube it is not absolutely necessary that the conductor should be closed"

- row: 37
- cited as: `(1894, p. 398)`
- why: the sentence that removes the reader's first objection ('where does the current come back through?'). A closed conductor is not necessary. This is the 1891 version of the fact article 01 states in modern words as 'the insulated body serves to give off the energy into the surrounding space, and is equivalent to a return wire' (p. 184), which article 01 has already quoted; the two are the same finding in two vocabularies, and the article should link rather than re-explain
- check_quotes.py: exact match, ratio 1.0, printed p. 398
- raw OCR: `y conductor consists of a rarefied FIG. 212. gas, and that under such conditions electrostatic effects must play an important part. In support of my view I will describe a few experiments made by me. To excite luminosity in the tube it is not absolutely necessary that the conductor should be closed. For instance, if`

### 4. The vacuum problem (the effect is already there before the spark)

> "before the disruptive discharge takes place, the tube or bulb is slightly excited and the formation of the luminous circle is decidedly facilitated"

- row: 38
- cited as: `(1894, p. 398)`
- why: the observation that connects chapter XXXII to the p. 288 'retains the faculty' sentence: the tube is partly excited BEFORE the discharge, so excitation is a state the tube can be in, not a magic event. This is the strongest support in the volume for brief 12 item 5's 'a charge/ionisation state', and it is a laboratory observation rather than a lecture trick
- check_quotes.py: exact match, ratio 1.0, printed p. 398
- raw OCR: `. NVENTION8 OF NIKOLA TESLA. nations per second to excite the induction coil for charging the Leyden jar which discharges through the primary — shown diagrammatically in Fig. 211, — as in such case, before the disruptive discharge takes place, the tube or bulb is slightly excited and the formation of the luminous circle is decidedly facilitated. FIG. 211. But I have also used a Wimshurst machine in some experiments. Prof. J. J. Thomson's view of the phenomena under consideration seems to be that they are wholly due to electro-magnetic actio`

### 2. Why a tube lights with no wires (the conditions that make it work)

> "It must be remembered that in these experiments we have to deal with primary currents of an enormous frequency or rate of change and of high potential, and that the secondary conductor consists of a rarefied gas, and that under such conditions electrostatic effects must play an important part"

- row: 39
- cited as: `(1894, p. 398)`
- why: the sentence that states the boundary conditions of every effect in this article: enormous frequency, high potential, and a rarefied gas as the secondary conductor. 'must play an important part' is a conditional, not a conclusion, and the article should quote it as the condition under which the rest of the chapter holds. The whole demo fails without those three conditions, which is why none of it can be tried at home
- check_quotes.py: exact match, ratio 1.0, printed p. 398
- raw OCR: `wholly due to electro-magnetic action. I was, at one time, of the same opinion, but upon carefully investigating the subject I was led to the conviction that they are more of an electrostatic nature. It must be remembered that in these experiments we have to deal with primary currents of an enormous frequency or rate of change and of high potential, and that the secondary conductor consists of a rarefied FIG. 212. gas, and that under such conditions electrostatic effects must play an important part. In support of my view I will describe a few experiments made by me. To excite luminosity in the tube i`

## Printed p. 399 (scan file 417, 18 leaves of offset)

### 2. Why a tube lights with no wires (the tube inside a coil)

> "an ordinary exhausted tube (preferably of large diameter) be surrounded by a spiral of thick copper wire serving as the primary ... feebly luminous spiral may be induced in the tube"

- row: 40
- cited as: `(1894, p. 399)`
- why: the arrangement the brief's Fig. 215 crop shows: a spiral of thick copper wire around an exhausted tube, and the tube lights without being connected to anything. 'feebly' is his own word for the brightness, and it is the counterweight to every modern retelling that says the tube blazed. The cut in the middle is where the scan breaks, and the break is measured, not assumed: the print carries a footnote marker at the end of 'primary' and the OCR then sets 'primary^ afeebly', gluing the following article to the word after it, so the strict index has no 'a feebly' in the book at all (0 hits, measured). The second fragment therefore starts at 'feebly', which is exact on the pinned page, ratio 1.0. The joined form with a comma is only fuzzy 0.967 and is Rejected #8
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 399; frag 2: exact match, ratio 1.0, printed p. 399
- raw OCR (frag 1: an ordinary exhausted tube (preferably o): `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 399 an ordinary exhausted tube (preferably of large diameter) be surrounded by a spiral of thick copper wire serving as the primary^ afeebly luminous spiral may be induced in the tube, roughly shown in Fig. 212. In one of these experiments a curious phenomenon was observed ; namely, two intensely luminous circles, each of them cl`
- raw OCR (frag 2: feebly luminous spiral may be induced in): `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 399 an ordinary exhausted tube (preferably of large diameter) be surrounded by a spiral of thick copper wire serving as the primary^ afeebly luminous spiral may be induced in the tube, roughly shown in Fig. 212. In one of these experiments a curious phenomenon was observed ; namely, two intensely luminous circles, each of them close to a turn of the primary spiral, were formed ins`

### 2. Why a tube lights with no wires (adding a plate makes it brighter)

> "the lamp-bulb was provided with a tinfoil coating on the side opposite to the primary and each time the tinfoil coating was connected to the ground or to a large object the luminosity of the circle was considerably increased. This was evidently due to electrostatic action"

- row: 41
- cited as: `(1894, p. 399)`
- why: the experiment that shows the effect is a coupling between two electrodes with the glass between them: adding a tinfoil plate opposite the primary, and connecting it to ground or to a large object, makes it brighter. That is a capacitor being tuned, described without the word. 'This was evidently due to electrostatic action' is his own inference, on the same breath as the observation, and the article should keep them together so the reader can see which part is the measurement and which is the reading of it
- check_quotes.py: exact match, ratio 1.0, printed p. 399
- raw OCR: `in Fig. 214. In this case an ordinary lamp-bulb was surrounded by one or two turns of thick copper wire P and the luminous circle L excited in the bulb by discharging the jar through the primary. The lamp-bulb was provided with a tinfoil coating on the side opposite to the primary and each time the tinfoil coating was connected to the ground or to a large object the luminosity of the circle was considerably increased. This`

### 2. Why a tube lights with no wires (how he argued, not what he saw)

> "the fact that a glow can be produced along the primary in the form of an open spiral argues for an electrostatic effect"

- row: 42
- cited as: `(1894, p. 399)`
- why: 'argues for' is the phrase to teach from: this is an inference from a second observation, not a proof. The article's beat 2 has to separate what the tube did from what he concluded, and this sentence shows him doing both in one line. Chapter XXXII's whole argument is of this form, which is why the chapter reads as a debate and not as a lab report
- check_quotes.py: exact match, ratio 1.0, printed p. 399
- raw OCR: `to strain the jar to the utmost. The turns of the spiral tend to close and form circles, but this, of course, would be expected, and does not necessarily indicate an electro-magnetic effect ; whereas the fact that a glow can be produced along the primary in the form of an open spiral argues for an electrostatic effect. FIG. 213. In using Dr. Lodge's recoil circuit, the electrostatic action is likewise apparent. The arrangement is illustrated in Fig. 213. In his experiment two hollow exhausted tubes H H were slippe`

### 2. Why a tube lights with no wires (standing waves in the coil)

> "two intensely luminous circles, each of them close to a turn of the primary spiral, were formed inside of the tube, and I attributed this phenomenon to the existence of nodes on the primary"

- row: 43
- cited as: `(1894, p. 399)`
- why: the observation that the light sits at fixed places, and his explanation (nodes on the primary). 'I attributed' is again an attribution, and it is the one claim in the chapter about WHY the pattern is where it is. Useful for beat 2's striae/stratification material: the bands are not random, and in 1891 the only available explanation was a property of the coil, not of the gas
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 399
- raw OCR: `ral of thick copper wire serving as the primary^ afeebly luminous spiral may be induced in the tube, roughly shown in Fig. 212. In one of these experiments a curious phenomenon was observed ; namely, two intensely luminous circles, each of them close to a turn of the primary spiral, were formed inside of the tube, and I attributed this phenomenon to the existence ofnodes on the primary. The circles were connected by a faint luminous spiral parallel to the primary and in close proximity to it. To produce this effect I have found it necessary to strain the jar to the utmost. The turn`

## Printed p. 400 (scan file 418, 18 leaves of offset)

### 2. Why a tube lights with no wires (the closer the coil, the easier)

> "the circles were always in close proximity to the primary and were considerably easier produced when the latter was very close to the glass ... and these facts speak for an electrostatic effect"

- row: 44
- cited as: `(1894, p. 400)`
- why: the distance dependence, stated as an observation: always near the primary, easier when the primary was close to the glass. 'speak for' is his third inference-verb in three pages ('argues for', 'I attributed', 'speak for'), which is the pattern the article can name instead of characterising him. The cut is the page's figure label between the two halves of the sentence
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 400; frag 2: exact match, ratio 1.0, printed p. 400
- raw OCR (frag 1: the circles were always in close proximi): `my experiments they were broad and often the whole of the bulb or tube was illuminated ;and in one case I have observed an intensely purplish FIG. 214. glow, to which Prof. J. J. Thomson refers. But the circles were always in close proximity to the primary and were considerably easier produced when the latter was very close to the glass, much more so than would be expected assuming the action to be elec- FIG. 215. tromagnetic and considering the distance ; and these facts speak for an electrostatic effect. Furthermore I have observe`
- raw OCR (frag 2: and these facts speak for an electrostat): `were considerably easier produced when the latter was very close to the glass, much more so than would be expected assuming the action to be elec- FIG. 215. tromagnetic and considering the distance ; and these facts speak for an electrostatic effect. Furthermore I have observed that there is a molecular bombardment inthe plane of the luminous circle at right angles to the glass — supposing the circle to be in the plane of the primary`

### 2. Why a tube lights with no wires (his tubes were not thin rings)

> "in my experiments they were broad and often the whole of the bulb or tube was illuminated"

- row: 45
- cited as: `(1894, p. 400)`
- why: the correction to the drawing most retellings give: his effects were broad and often filled the whole bulb. It is a first-person claim about his own apparatus, made in reply to Thomson's narrower rings, so it is also part of the argument - see the flag THE RING OF LIGHT IS THOMSON'S, THE BROAD GLOW IS TESLA'S
- check_quotes.py: exact match, ratio 1.0, printed p. 400
- raw OCR: `INVENTIONS OF NIKOLA TESLA. more sharply defined ; but I have not noted that, generally speaking, the circles induced were very sharply defined, as Prof. J. J. Thomson has observed ; on the contrary, in my experiments they were broad and often the whole of the bulb or tube was illuminated ;and in one case I have observed an intensely purplish FIG. 214. glow, to which Prof. J. J. Thomson refers. But the circles were always in close proximity to the primary and were considerably easier`

### 2. Why a tube lights with no wires (the colour, and whose observation it is)

> "I have observed an intensely purplish glow, to which Prof. J. J. Thomson refers"

- row: 46
- cited as: `(1894, p. 400)`
- why: the colour of the glow, and the sentence is a cross-reference: he is confirming a detail Thomson reported. 'purplish' is in the volume 4 times and in chapter XXXII 2 times (measured): his at printed p. 400 and Thomson's at printed p. 403, which is the one he refers to. His colour claim is corroborative rather than original, and the two glows must not be blended into one. Brief 12's query list includes 'tesla phosphorescence', and the Tier 3 backlog topic 'tesla-phosphorescent-colours' is this same chapter, so the colour material here is also a future article's - keep it short
- check_quotes.py: exact match, ratio 1.0, printed p. 400
- raw OCR: `es induced were very sharply defined, as Prof. J. J. Thomson has observed ; on the contrary, in my experiments they were broad and often the whole of the bulb or tube was illuminated ;and in one case I have observed an intensely purplish FIG. 214. glow, to which Prof. J. J. Thomson refers. But the circles were always in close proximity to the primary and were considerably easier produced when the latter was very close to the glass, m`

### 2. Why a tube lights with no wires (the mechanism he proposes)

> "there is a molecular bombardment inthe plane of the luminous circle at right angles to the glass"

- row: 47
- cited as: `(1894, p. 400)`
- why: the mechanism sentence: molecular bombardment in the plane of the circle, at right angles to the glass. This is the closest the chapter comes to a physical picture of what makes the light, and it is the 1891 counterpart of the 'trillions of invisible hammers' sentence at printed p. 175. The OCR glues 'inthe'; the print has the space, so this verifies only through the space-ignoring index and the draft prints 'in the'
- check_quotes.py: exact match, ratio 1.0, printed p. 400
- raw OCR: `more so than would be expected assuming the action to be elec- FIG. 215. tromagnetic and considering the distance ; and these facts speak for an electrostatic effect. Furthermore I have observed that there is a molecular bombardment inthe plane of the luminous circle at right angles to the glass — supposing the circle to be in the plane of the primary`

## Printed p. 401 (scan file 419, 18 leaves of offset)

### 2. Why a tube lights with no wires (the coupling depends on the medium)

> "when the specific inductive capacity of the medium between the primary and secondary is increased, the inductive effect is augmented"

- row: 48
- cited as: `(1894, p. 401)`
- why: the sentence that says the effect between primary and secondary depends on the specific inductive capacity of what is between them. That is a dielectric constant, and it is the mechanism brief 12 item 5 calls capacitive coupling, in the period's words. The book's word for the component is 'condenser' (measured, table below); 'capacitor' is 0
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `circumferentially, the former plate would be rendered more intensely phosphorescent. For want of time I have, however, not been able to perform the experiment. Another observation made by me was that when the specific inductive capacity of the medium between the primary and secondary is increased, the inductive effect is augmented. This is roughly illustrated in Fig. 215. In this case luminosity was excited in an exhausted tube or bulb B and a glass tube T slipped between the primary and the bulb, when the effect pointed out w`

### 2. Why a tube lights with no wires (a test that could have failed)

> "a glass tube T slipped between the primary and the bulb, when the effect pointed out was noted. Were the action wholly electromagnetic no change could possibly have been observed"

- row: 49
- cited as: `(1894, p. 401)`
- why: a designed discriminating test: put a glass tube between primary and bulb and the effect changes, which a purely electromagnetic action could not do. 'no change could possibly have been observed' is the counterfactual, and it is the best evidence in the chapter that he was trying to falsify himself. Pair it with the p. 401 tinfoil row below and with the flag HE TRIED TO SCREEN IT OUT AND THE SCREENING FAILED
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `dium between the primary and secondary is increased, the inductive effect is augmented. This is roughly illustrated in Fig. 215. In this case luminosity was excited in an exhausted tube or bulb B and a glass tube T slipped between the primary and the bulb, when the effect pointed out was noted. Were the action wholly electromagnetic no change could possibly have been observed. I have likewise noted that when a bulb is surrounded by a wire closed upon itself and in the plane of the primary, the formation of the luminous circle within the bulb is not prevented. But if inste`

### 2. Why a tube lights with no wires (a second counterfactual, from heat)

> "this bombardment being evident from the rapid heating of the glass near the primary. Were the bombardment not at right angles to the glass the heating could not be so rapid"

- row: 50
- cited as: `(1894, p. 401)`
- why: the same reasoning style from a different sense: the glass got hot, and only a bombardment at right angles could do that. It is an inference from a burnt bulb, and the article should say so. It also gives the article a physical consequence of the mechanism (the glass heats), which matters for beat 3's lamp problem: the glass must be kept away from the hot part
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 401 — this bombardment being evident from the rapid heating of the glass near the primary. Were the bombardment not at right angles to the glass the heating could not be so rapid. If there is a circumferential movement of the molecules constituting the luminous circle, I have thought that it might be rendered manifest by placing within the tube or bulb, radially to the circle`

### 2. Why a tube lights with no wires (a shorted turn does not stop it)

> "when a bulb is surrounded by a wire closed upon itself and in the plane of the primary, the formation of the luminous circle within the bulb is not prevented"

- row: 51
- cited as: `(1894, p. 401)`
- why: the null result that kills the simple transformer story: a closed wire round the bulb, which is a shorted turn, does not stop the light. Any reader who has worked out 'the tube is the secondary of a transformer' will expect a shorted turn to kill it, and it does not. This is the single best quote for brief 12 item 5's 'the energy is capacitively coupled', because it is a measurement that discriminates between the two stories
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `tube T slipped between the primary and the bulb, when the effect pointed out was noted. Were the action wholly electromagnetic no change could possibly have been observed. I have likewise noted that when a bulb is surrounded by a wire closed upon itself and in the plane of the primary, the formation of the luminous circle within the bulb is not prevented. But if instead of the wire a broad strip of tinfoil is glued upon the bulb, the formation of the luminous band was prevented, because then the action was distributed over a greater surface. The effe`

### 2. Why a tube lights with no wires (what does stop it)

> "But if instead of the wire a broad strip of tinfoil is glued upon the bulb, the formation of the luminous band was prevented, because then the action was distributed over a greater surface"

- row: 52
- cited as: `(1894, p. 401)`
- why: the positive control for the row above: a broad tinfoil strip DOES prevent the band, and he gives the reason (distribution over a greater surface). Two experiments on one page that bracket the effect. Note the tense change in the print ('is glued' then 'was prevented'); quote it as set
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `een observed. I have likewise noted that when a bulb is surrounded by a wire closed upon itself and in the plane of the primary, the formation of the luminous circle within the bulb is not prevented. But if instead of the wire a broad strip of tinfoil is glued upon the bulb, the formation of the luminous band was prevented, because then the action was distributed over a greater surface. The effect of the closed tinfoil was no doubt of an electrostatic nature, for it presented a much greater resistance than the closed wire and produced therefore a much smaller electromagnetic effect`

### 5. What the internet gets wrong (an experiment he did not do)

> "For want of time I have, however, not been able to perform the experiment"

- row: 53
- cited as: `(1894, p. 401)`
- why: the plain admission that a test he described had not been run. It belongs in the article wherever a claim of his is reported as a finding, because it is his own record of the boundary between what he tried and what he sketched. Read the flag HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS
- check_quotes.py: exact match, ratio 1.0, printed p. 401
- raw OCR: `d with some phosphorescent material and another such plate tangentially to the circle. If the molecules would move circumferentially, the former plate would be rendered more intensely phosphorescent. For want of time I have, however, not been able to perform the experiment. Another observation made by me was that when the specific inductive capacity of the medium between the primary and secondary is increased, the inductive effect is augmented. This is roughly illustra`

## Printed p. 402 (scan file 420, 18 leaves of offset)

### 2. Why a tube lights with no wires (the difficulty, in Thomson's abstract)

> "To produce discharges in tubes devoid of electrodes was, however, not easy to accomplish, for the only available means of producing an electromotive force in the discharge circuit was by electro-magnetic induction"

- row: 54
- cited as: `(1894, p. 402)`
- why: the difficulty stated, but the voice is not his and the draft must not print it as if it were: this sentence is inside the abstract of J. J. Thomson's paper, in third-person reportage, on the same page as the heading that begins 'SOME EXPERIMENTS ON THE ELECTRIC DISCHARGE BY PROF. J. J. THOMSON'. It is the one sentence in this chapter that reads like Tesla's prose and is not his. Read the flag THE ABSTRACT IS THIRD PERSON AND THE PROSE IS FLUENT, WHICH IS THE TRAP
- check_quotes.py: exact match, ratio 1.0, printed p. 402
- raw OCR: `lified when their path was wholly gaseous, the complication of the dark space surrounding the negative electrode, and the stratifications so commonly observed in ordinary vaciium tubes, being absent. To produce discharges in FIG. 216. FIG. 2V, tubes devoid of electrodes was, however, not easy to accomplish, for the only available means of producing an electromotive force in the discharge circuit was by electro-magnetic i`

### 2. Why a tube lights with no wires (his principal argument)

> "I have experimentally proved that if the same discharge which is barely sufficient to excite a luminous band in the bulb when passed through the primary circuit be so directed as to exalt the electrostatic inductive effect - namely, by converting upwards - an exhausted tube, devoid of electrodes, may be excited at a distance of several feet"

- row: 55
- cited as: `(1894, p. 402)`
- why: 'My principal argument is the following' is the sentence that introduces this one, on the same page, and it is the only place in the chapter where he labels his own best case. The claim is quantitative in a way the rest is not: the SAME discharge, redirected, lights a tube several feet away. 'exalt' is the period's verb for strengthening a coupling. The dashes are the print's em dashes and cannot be printed; cut at them or use brackets
- check_quotes.py: exact match, ratio 1.0, printed p. 402
- raw OCR: `a vacuum was produced by the Torricellian method, I was unable to produce the luminous band, but this may have been due to the weak exciting current employed. My principal argument is the following : I have experimentally proved that if the same discharge which is barely sufficient to excite a luminous band in the bulb when passed through the primary circuit be so directed as to exalt the electrostatic inductive effect — namely, by converting upwards — an exhausted tube, devoid of electrodes, may be excited at a distance of several feet. SOME EXPERIMENTS ON THE BY PROF. ELECTRIC DISCHARGE J. J. THOMSON, IN VACUUM T`

### 2. Why a tube lights with no wires (what makes it stop)

> "the introduction of mercury or the heating of the bulb prevents the formation of the luminous band or shortens the after-glow; and also why in some cases a platinum wire may prevent the excitation of the tube"

- row: 56
- cited as: `(1894, p. 402)`
- why: three things that spoil the effect, in one sentence: mercury in the bulb, heat, and a platinum wire inside it. The article needs the negative cases or the demo sounds like magic; and 'after-glow' is the one occurrence of that word in the volume (measured, table below), which is the word the brief's 'retains the faculty' beat is about in laboratory terms
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 402
- raw OCR: `NTIONS OF NIKOLA TE8LA. only, that is, supposing the vacuous space to be non-conducting. On the assumption that in these phenomena electrostatic actions are concerned we find it easily explicable why the introduction of mercury or the heating of the bulb prevents the formation of the luminous band or shortens the after-glow ; and also why in some cases a platinum wire may prevent the excitation of the tube. Nevertheless some of the experiments of Prof. J. J. Thomson would seem to indicate an electromagnetic e`

### 4. The vacuum problem (a failure, and his guess at the cause)

> "in one of my experiments in which a vacuum was produced by the Torricellian method, I was unable to produce the luminous band, but this may have been due to the weak exciting current employed"

- row: 57
- cited as: `(1894, p. 402)`
- why: a negative result with the reason attached, and the reason is his own apparatus, not the tube. This is the laboratory version of the p. 288 'another tube might not light' moment, and it is dated 1891 in his own article. 'Torricellian method' is the barometric vacuum, i.e. the best vacuum he had; the failure is exactly the non-striking problem of brief 12 item 4, described before he had the high-frequency apparatus to beat it
- check_quotes.py: exact match, ratio 1.0, printed p. 402
- raw OCR: `why in some cases a platinum wire may prevent the excitation of the tube. Nevertheless some of the experiments of Prof. J. J. Thomson would seem to indicate an electromagnetic effect. I may add that in one of my experiments in which a vacuum was produced by the Torricellian method, I was unable to produce the luminous band, but this may have been due to the weak exciting current employed. My principal argument is the following : I have experimentally proved that if the same discharge which is barely sufficient to excite a luminous band in the bulb when passed through the primary circ`

### 2. Why a tube lights with no wires (stratification, in the other man's words)

> "The phenomena of vacuum discharges were, Prof. Thomson said, greatly simplified when their path was wholly gaseous, the complication of the dark space surrounding the negative electrode, and the stratifications so commonly observed in ordinary vaciium tubes, being absent"

- row: 64
- cited as: `(1894, p. 402)`
- why: the word the brief asks for ('striae') appears in this chapter as 'stratifications', in THOMSON'S reported speech, and the sentence says those bands are absent when the path is wholly gaseous. So the chapter that the brief treats as the striae source actually reports their ABSENCE. The real striae sentences are in the New York lecture at printed p. 186. The print's typo 'vaciium' is inside this quote and must be reproduced or cut - see the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX
- check_quotes.py: exact match, ratio 1.0, printed p. 402
- raw OCR: `rting upwards — an exhausted tube, devoid of electrodes, may be excited at a distance of several feet. SOME EXPERIMENTS ON THE BY PROF. ELECTRIC DISCHARGE J. J. THOMSON, IN VACUUM TUBES. M.A., F.R.S. The phenomena of vacuum discharges were, Prof. Thomson said, greatly simplified when their path was wholly gaseous, the complication of the dark space surrounding the negative electrode, and the stratifications so commonly observed in ordinary vaciium tubes, being absent. To produce discharges in FIG. 216. FIG. 2V, tubes devoid of electrodes was, however, not easy to accomplish, for the only available means of producing an electromotive force in the discharge circuit`

## Printed p. 403 (scan file 421, 18 leaves of offset)

### 4. The vacuum problem (the same failure, in Thomson's apparatus)

> "On exhausting the jar, however, the luminous discharge grew fainter, and a point was reached at which no secondary discharge was visible"

- row: 58
- cited as: `(1894, p. 403)`
- why: THOMSON'S observation, not Tesla's, and it is the same phenomenon: pump the air out further and the light goes out. Two men, two apparatuses, one page apart, both hitting the vacuum limit. That is the strongest possible support for brief 12 item 4's point that the vacuum is the hard part, and it is also the reason the article must name whose apparatus is whose
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `ed by a primary spiral, was contained in a bell-jar, and when the pressure of air in the jar was about that of the atmosphere, the secondary discharge occurred in the bulb, as is ordinarily the case. On exhausting the jar, however, the luminous discharge grew fainter, and a point was reached at which no secondary discharge was visible. J urther exhaustion of the jar caused the secondary discharge to appear outside of the bulb. The fact of obtaining no luminous discharge, either in the bulb or jar, the author`

### 4. The vacuum problem (where the light goes when the tube stops)

> "J urther exhaustion of the jar caused the secondary discharge to appear outside of the bulb"

- row: 59
- cited as: `(1894, p. 403)`
- why: the continuation of the row above, and the detail that makes it a mechanism rather than a failure: past the limit, the discharge moves outside the bulb. The OCR prints 'J urther' with a space after the J, an artefact of a capital J at the start of a line; the print reads 'Further', so this verifies only through the space-ignoring index
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `ry discharge occurred in the bulb, as is ordinarily the case. On exhausting the jar, however, the luminous discharge grew fainter, and a point was reached at which no secondary discharge was visible. J urther exhaustion of the jar caused the secondary discharge to appear outside of the bulb. The fact of obtaining no luminous discharge, either in the bulb or jar, the author`

### 2. Why a tube lights with no wires (the source of the high frequency)

> "Leyden jar, which combines the two essentials of a current whose maximum value is enormous, and whose rapidity of alternation is immensely great"

- row: 60
- cited as: `(1894, p. 403)`
- why: THOMSON'S account of how he got the frequency, and it is the answer to the reader's question 'what drove this': a Leyden jar discharged oscillatory. The sentence begins at the foot of printed p. 402 with 'recourse was had to the oscillatory discharge of a', and the two halves do NOT join in the index: the page's own footnote ('1. Abstract of a paper read before Physical Society of London.') sits between them in the page body and strip_furniture keeps it, so the joined run returns no match at all and the p. 402 half is Rejected #11. Quote the p. 403 half only. The whole chapter's effects come from a spark-gap and a jar, which is also why the numbers are not reproducible to modern tolerances. Attribute to Thomson's abstract
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `HIGH FREQUENCY AND HTGII POTENTIAL CURRENTS. 403 Leyden jar, which combines the two essentials of a current whose maximum value is enormous, and whose rapidity of alternation is immensely great. The discharge circuits, which may take the shape of bulbs, or of tubes bent in the form of coils, were placed in close proximity to glass tubes filled with mercury, which formed the path of the osci`

### 2. Why a tube lights with no wires (Fig. 216 is Thomson's)

> "The two or three turns, as shown in Fig. 216, in each, were found to be quite sufficient"

- row: 61
- cited as: `(1894, p. 403)`
- why: the sentence that names Fig. 216, and it is THOMSON'S figure, not Tesla's. The brief does not ask for Fig. 216, but it asks for Fig. 218, which is on the same page and is also Thomson's. This row exists so the figure task does not caption a plate of Thomson's apparatus as Tesla's. Read the flag THE BRIEF'S FIG. 218 IS THOMSON'S APPARATUS
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `charge path in the latter. Increasing the self-induction of the primary reduces the E. M. F. induced in the secondary, whilst lengthening the secondary does not increase the E. M. F. per unit length. The two or three turns, as shown in Fig. 216, in each, were found to be quite sufficient, and, on discharging the Leyden jar between two highly polished knobs in the primary FIG. 218. FIG. 219. circuit, a plain uniform band of light was seen to pass round the secondary. An exhausted bulb`

### 2. Why a tube lights with no wires (the ring of light, and its duration)

> "An exhausted bulb, Fig. 217, containing traces of oxygen was plaeed within a primary spiral of three turns, and, on passing the jar discharge, a circle of light was seen within the bulb inclose proximity to the primary circuit, accompanied by a purplish glow, which lasted for a second or more"

- row: 62
- cited as: `(1894, p. 403)`
- why: THOMSON'S apparatus and THOMSON'S observation, and it is the origin of the 'ring of light' that the popular story attaches to Tesla. 'lasted for a second or more' is a duration, which is the fact the persistence beat needs in laboratory terms. Two OCR defects sit inside this one quote: 'plaeed' for 'placed' and 'inclose' for 'in close'. The first is a real OCR error the space-ignoring index cannot fix, so the quote is cut around it - see Rejected #12
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `quite sufficient, and, on discharging the Leyden jar between two highly polished knobs in the primary FIG. 218. FIG. 219. circuit, a plain uniform band of light was seen to pass round the secondary. An exhausted bulb, Fig. 217, containing traces of oxygen was plaeed within a primary spiral of three turns, and, on passing the jar discharge, a circle of light was seen within the bulb inclose proximity to the primary circuit, accompanied by a purplish glow, which lasted for a second or more. On heating the bulb, the duration of the glow was greatly diminished, and it could be instantly extinguished by the presence of an electro-magnet. Another exhausted bulb, Fig. 218, surrounded by a p`

### 2. Why a tube lights with no wires (heat and magnetism kill it)

> "On heating the bulb, the duration of the glow was greatly diminished, and it could be instantly extinguished by the presence of an electro-magnet"

- row: 63
- cited as: `(1894, p. 403)`
- why: THOMSON'S, and it is the counter-experiment to the persistence story: heat shortens the glow and a magnet kills it. If the article reports that a tube 'remembers', this is the sentence that shows the memory is physical and can be erased. Attribute to the abstract, not to Tesla
- check_quotes.py: exact match, ratio 1.0, printed p. 403
- raw OCR: `three turns, and, on passing the jar discharge, a circle of light was seen within the bulb inclose proximity to the primary circuit, accompanied by a purplish glow, which lasted for a second or more. On heating the bulb, the duration of the glow was greatly diminished, and it could be instantly extinguished by the presence of an electro-magnet. Another exhausted bulb, Fig. 218, surrounded by a primary spiral, was contained in a bell-jar, and when the pressure of air in the jar was about that of the atmosphere, the secondary discharge occur`

## Printed p. 404 (scan file 422, 18 leaves of offset)

### 5. What the internet gets wrong (he changed his own mind, in public)

> "at the outset, I myself looked for a purely electrodynamic effect and believed that I had obtained it. But many experiments performed at that time proved to me that the electrostatic effects were generally of far greater importance"

- row: 65
- cited as: `(1894, p. 404)`
- why: the sentence that makes this chapter a record of a mind changing: he looked for one effect, believed he had it, and was proved wrong by his own experiments. It is the best anti-myth quote available, because it is the author reporting his own error in a published reply. 'generally' and 'far greater' are hedged on purpose; the draft must not turn it into 'he disproved himself'
- check_quotes.py: exact match, ratio 1.0, printed p. 404
- raw OCR: `ts, that all possible precautions had been taken to exclude these effects. I did not doubt that luminosity could be excited in a closed tube when electrostatic action is completely excluded. In fact, at the outset, I myself looked for a purely electrodynamic effect and believed that I had obtained it. But many experiments performed at that time proved to me that the electrostatic effects were generally of far greater importance, and admitted of a more satisfactory explanation of most of the phenomena observed. In using the term electrostatic I had reference rather to the nature of the action than to a stationary condition,`

### 2. Why a tube lights with no wires (what he means by electrostatic)

> "In using the term electrostatic I had reference rather to the nature of the action than to a stationary condition, which is the usual acceptance of the term"

- row: 66
- cited as: `(1894, p. 404)`
- why: the definition sentence, and it is a warning to the modern reader: his 'electrostatic' does NOT mean stationary, it means the action is of the kind associated with charge rather than with current. Every sentence in the article that uses the word has to be read against this. It is also the reason 'capacitively coupled' is a fair translation and 'static electricity' is not
- check_quotes.py: exact match, ratio 1.0, printed p. 404
- raw OCR: `riments performed at that time proved to me that the electrostatic effects were generally of far greater importance, and admitted of a more satisfactory explanation of most of the phenomena observed. In using the term electrostatic I had reference rather to the nature of the action than to a stationary condition, which is the usual acceptance of the term. To express myself more clearly, I will suppose that near a closed exhausted tube be placed a small sphere charged to a very high potential. The sphere would act inductively upon the tube, and by dis`

### 0. Provenance (the reply, in his words)

> "I did not, as Prof. J. J. Thomson seems to believe, misunderstand his position in regard to the cause of the phenomena considered, but I thought that in his experiments, as well as in my own, electrostatic effects were of great importance"

- row: 67
- cited as: `(1894, p. 404)`
- why: the opening of Tesla's published reply to Thomson, and the pair of it is on printed p. 406 in Thomson's own words ('He seems, however, to have misunderstood my position'). Two men, two printed pages, each saying the other had misunderstood him. That is the honest shape of the discovery story and the article should show it once, plainly, with both pages. Read the flag TWO MEN, ONE VOLUME, EACH SAYING THE OTHER MISREAD HIM
- check_quotes.py: exact match, ratio 1.0, printed p. 404
- raw OCR: `r of August 12, I find some remarks of Prof. J. J. Thomson, which appeared originally in the London Electrician and which have a bearing upon some experiments described by me in your issue of July 1. I did not, as Prof. J. J. Thomson seems to believe, misunderstand his position in regard to the cause of the phenomena considered, but I thought that in his experiments, as well as in my own, electrostatic effects were of great importance. It did not appear, from the meagre description of his experiments, that all possible precautions had been taken to exclude these effects. I did not doubt that luminosity could be excited in a closed`

### 0. Provenance (his criticism of the other man's evidence)

> "It did not appear, from the meagre description of his experiments, that all possible precautions had been taken to exclude these effects"

- row: 68
- cited as: `(1894, p. 404)`
- why: 'meagre description' is a published criticism of a published report, and it is also a description of the state of the evidence in this whole controversy: nobody in the volume has enough detail from the other side to settle it. That is a fact about 1891 priority disputes that the article can state, and this is the quote that licenses it
- check_quotes.py: exact match, ratio 1.0, printed p. 404
- raw OCR: `to believe, misunderstand his position in regard to the cause of the phenomena considered, but I thought that in his experiments, as well as in my own, electrostatic effects were of great importance. It did not appear, from the meagre description of his experiments, that all possible precautions had been taken to exclude these effects. I did not doubt that luminosity could be excited in a closed tube when electrostatic action is completely excluded. In fact, at the outset, I myself looked for a purely electrodynamic effect and bel`

### 2. Why a tube lights with no wires (the thought experiment)

> "I will suppose that near a closed exhausted tube be placed a small sphere charged to a very high potential. The sphere would act inductively upon the tube"

- row: 70
- cited as: `(1894, p. 404)`
- why: the model he builds to explain the effect: a charged sphere near a closed tube acts on it inductively. This is the mechanism brief 12 item 5 calls capacitive coupling, drawn as an object. It is a supposition, not an experiment - 'I will suppose' is in the sentence - and the article has to say that
- check_quotes.py: exact match, ratio 1.0, printed p. 404
- raw OCR: `observed. In using the term electrostatic I had reference rather to the nature of the action than to a stationary condition, which is the usual acceptance of the term. To express myself more clearly, I will suppose that near a closed exhausted tube be placed a small sphere charged to a very high potential. The sphere would act inductively upon the tube, and by distributing electricity over 1. Article by Mr. Tesla in The Electrical Engineer, N. Y., August 26, 1891.`

## Printed p. 405 (scan file 423, 18 leaves of offset)

### 2. Why a tube lights with no wires (he conceded the other case)

> "Without doubting in the least that, with the care and precautions taken by Prof. J. J. Thomson, the luminosity excited was due solely to electrodynamic action, I would say that in many experiments I have observed curious instances of the ineffectiveness of the screening"

- row: 69
- cited as: `(1894, p. 405)`
- why: the concession, which the article must not skip: he accepted that Thomson's result was genuine, and offered only that his own screens did not work. Without this row, beat 5 reads as Tesla winning an argument he never had. 'curious instances of the ineffectiveness of the screening' is also the understatement that hides how much his own apparatus leaked
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `appeared from rough estimation that an oxygen tube when excited under similar conditions — that is, as far as could be determined — gives more light ; but this, of course, may be due to many causes. Without doubting in the least that, with the care and precautions taken by Prof. J. J. Thomson, the luminosity excited was due solely to electrodynamic action, I would say that in many experiments I have observed curious instances of the ineffectiveness of the screening, and I have also found that the electritica. tion through the air is often of very great importance, and may, in some cases, determine the excitation of the tube. In his original communication to the`

### 5. What the internet gets wrong (the limit of his own model)

> "the same would undoubtedly produce luminosity (if the potential be sufficiently high), until a permanent condition would be reached"

- row: 71
- cited as: `(1894, p. 405)`
- why: the conditional inside his model: it would produce light if the potential were high enough, until a permanent condition was reached. The parenthetical condition and the 'permanent condition' limit are both in the print, and they are the two places where the model stops. Quote them with the claim
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 405 the same would undoubtedly produce luminosity (if the potential be sufficiently high), until a permanent condition would be reached. Assuming the tube to be perfectly well insulated, there would be only one instantaneous flash during the act of distribution. This would be due to the electrostatic action simply. But now, suppose t`

### 5. What the internet gets wrong (the answer to 'what changed in the tube')

> "Assuming the tube to be perfectly well insulated, there would be only one instantaneous flash during the act of distribution. This would be due to the electrostatic action simply. But now, suppose the charged sphere to be moved at short intervals with great speed along the exhausted tube. The tube would now be permanently excited, as the moving sphere would cause a constant redistribution of electricity and collisions of the molecules of the rarefied gas"

- row: 72
- cited as: `(1894, p. 405)`
- why: the single best quote in the volume for brief 12 item 5, and it is a thought experiment, not a measurement: one flash if the charge is stationary, permanent excitation if the charge keeps moving, because a constant redistribution of electricity keeps colliding the gas molecules. That is exactly the distinction the p. 288 question needs: the persistent state is not stored power, it is a condition that a moving charge can maintain. He never ran this as an experiment; 'Assuming' and 'suppose' are in the sentence. Read the flag HE ANSWERS HIS OWN QUESTION ON THE NEXT PAGE AND NOBODY QUOTES IT
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 405 the same would undoubtedly produce luminosity (if the potential be sufficiently high), until a permanent condition would be reached. Assuming the tube to be perfectly well insulated, there would be only one instantaneous flash during the act of distribution. This would be due to the electrostatic action simply. But now, suppose the charged sphere to be moved at short intervals with great speed along the exhausted tube. The tube would now be permanently excited, as the moving sphere would cause a constant redistribution of electricity and collisions of the molecules of the rarefied gas. We would still have to deal with an electrostatic eifect, and in addition an electrodynamic effect would be observed. But if it were found that, for instance, the effect produced depended more on th`

### 3. Tesla's lamp research (the glass is part of the device)

> "the importance of the quality of glass of which the tube is made"

- row: 73
- cited as: `(1894, p. 405)`
- why: the glass matters, and it is a practical engineering statement inside a theoretical passage. It connects beat 2 to beat 3: the envelope is not a container, it is part of the coupling and it heats. This is the sentence that makes the carborundum passage a lamp problem rather than a curiosity
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `the spirit of the above example that I used the terms " more of an electrostatic nature," and have investigated the influence ofbodies of high specific inductive capacity, and observed, for instance, the importance of the quality of glass of which the tube is made. I also endeavored to ascertain the influence of a medium of high permeability by using oxygen. It appeared from rough estimation that an oxygen tube when excited under similar conditions — that is,`

### 2. Why a tube lights with no wires (he tried a different gas)

> "I also endeavored to ascertain the influence of a medium of high permeability by using oxygen"

- row: 74
- cited as: `(1894, p. 405)`
- why: the gas-variable experiment, in his own first person. Note the word choice: 'permeability' for a gas, which is the period's usage and not ours. The result is in the next row and it is hedged by him, so the two rows belong together
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `electrostatic nature," and have investigated the influence ofbodies of high specific inductive capacity, and observed, for instance, the importance of the quality of glass of which the tube is made. I also endeavored to ascertain the influence of a medium of high permeability by using oxygen. It appeared from rough estimation that an oxygen tube when excited under similar conditions — that is, as far as could be determined — gives more light ; but this, of course, may be due to many caus`

### 5. What the internet gets wrong (a result he refuses to interpret)

> "an oxygen tube when excited under similar conditions - that is, as far as could be determined - gives more light; but this, of course, may be due to many causes"

- row: 75
- cited as: `(1894, p. 405)`
- why: a comparative observation with the comparison itself disclaimed: 'as far as could be determined' and 'may be due to many causes'. This is the model sentence for how the article should report any comparison he makes, including the 20-times lamp claim in beat 3. The dashes are the print's em dashes and cannot be printed; cut at them
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 405
- raw OCR: `the importance of the quality of glass of which the tube is made. I also endeavored to ascertain the influence of a medium of high permeability by using oxygen. It appeared from rough estimation that an oxygen tube when excited under similar conditions — that is, as far as could be determined — gives more light ; but this, of course, may be due to many causes. Without doubting in the least that, with the care and precautions taken by Prof. J. J. Th`

### 0. Provenance (the prior art he names himself)

> "the luminosity in a tube near a wire through which a Leyden jar was discharged was noted by Hittorf"

- row: 76
- cited as: `(1894, p. 405)`
- why: the name he gives for the earliest observation of this kind, Hittorf, which is the sentence that stops the article from saying Tesla saw it first. It is Tesla's own citation, in Tesla's own article, and it is on the same page as the claim that his effects were much stronger. Read the flag PRIORITY IN THIS CHAPTER IS ABOUT WHO PUBLISHED AND WHO NOTED
- check_quotes.py: exact match, ratio 1.0, printed p. 405
- raw OCR: `the air is often of very great importance, and may, in some cases, determine the excitation of the tube. In his original communication to the Electrician, Prof. J. J. Thomson refers to the fact that the luminosity in a tube near a wire through which a Leyden jar was discharged was noted by Hittorf. I think that the feeble luminous effect referred to has`

## Printed p. 406 (scan file 424, 18 leaves of offset)

### 0. Provenance (his actual priority claim)

> "been noted by many experimenters, but in my experiments the effects were much more powerful than those usually noted"

- row: 77
- cited as: `(1894, p. 406)`
- why: the whole of his priority claim, and it is a claim about intensity, not about being first: many experimenters noted it, his was stronger. The sentence begins on printed p. 405 and finishes at the top of p. 406, before the Thomson communication starts, so the voice is Tesla's. This is the row that settles brief 12 item 5's framing: he never claimed the effect was unknown, he claimed his version was bigger
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `406 INVENTIONS OF NIKOLA TESLA. been noted by many experimenters, but in my experiments the effects were much more powerful than those usually noted. The following is the communication1 referred to :— "Mr. Tesla seems to ascribe the effects he observed to electrostatic action, and I have no doubt, from the description he gives of his method of co`

### 2. Why a tube lights with no wires (the other man's screen)

> "Wet blotting paper is a sufficiently good conductor to screen off a stationary electrostatic effect, though it is not a good enough one to stop waves of alternating electromotive intensity"

- row: 78
- cited as: `(1894, p. 406)`
- why: THOMSON'S method and THOMSON'S reasoning, in his own words in his own published note: a wet paper screen stops a stationary electrostatic effect but not alternating electromotive waves. That is a shielding rule of thumb that is still right, and it is the counterweight to Tesla's 'ineffectiveness of the screening'. The two sentences on this page are the actual technical content of the 1891 dispute
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `il was connected to earth, and, as a further precaution, the primary was separated from the discharge tube by a screen of blotting paper, moistened with dilute sulphuric acid, and connected to earth. Wet blotting paper is a sufficiently good conductor to screen off a stationary electrostatic effect, though it is not a good enough one to stop waves of alternating electromotive intensity. When showing the experiments to the Physical Society I could not, of course, keep the tubes covered up, but, unless my memory deceives me, I stated the precautions which had b«en taken against the e`

### 0. Provenance (the six weeks are THOMSON'S, not Tesla's)

> "the first experiment I tried with the discharge of a Leyden jar produced luminosity in the tube, but it was not until after six weeks' continuous experimenting that I was able to get a discharge in the exhausted tube which I was satisfied was due to what is ordinarily called electrodynamic action"

- row: 79
- cited as: `(1894, p. 406)`
- why: the trap in this chapter, and the reason this row is here rather than in the mechanism section: the famous 'six weeks' sentence is J. J. THOMSON describing HIS OWN Leyden-jar work, inside the communication quoted on printed p. 406. Any article that writes 'Tesla spent six weeks' has taken Thomson's sentence. Read the flag THE SIX WEEKS BELONG TO THOMSON
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `ion is excluded. As a matter of fact, it is very much easier to get the luminosity when these electrostatic effects are operative than when they are not. As an illustration of this I may mention that the first experiment I tried with the discharge of a Leyden jar produced luminosity in the tube, but it was not until after six weeks' continuous experimenting that I was able to get a discharge in the exhausted tube which I was satisfied was due to what is ordinarily called electrodynamic action. It is advisable to have a clear idea of what we mean by electrostatic action. If, previous to the discharge of the jar, the primary coil is raised to a high potential, itwill induce over the glass o`

### 0. Provenance (the other man's verdict on him)

> "Mr. Tesla seems to ascribe the effects he observed to electrostatic action, and I have no doubt, from the description he gives of his method of conducting his experiments, that in them electrostatic action plays a very important part"

- row: 80
- cited as: `(1894, p. 406)`
- why: THOMSON'S published assessment of Tesla's experiments, and it is conceding, not denying: electrostatic action 'plays a very important part' in them. The article can use this to show that the 1891 dispute was not about whether the effect was electrostatic but about whether it could also be produced without it. Third person about Tesla, first person about Thomson, one sentence
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `6 INVENTIONS OF NIKOLA TESLA. been noted by many experimenters, but in my experiments the effects were much more powerful than those usually noted. The following is the communication1 referred to :— "Mr. Tesla seems to ascribe the effects he observed to electrostatic action, and I have no doubt, from the description he gives of his method of conducting his experiments, that in them electrostatic action plays a very important part. He seems, however, to have misunderstood my position with respect to the cause of these discharges, which is not, as he implies, that luminosity in tubes without electrodes cannot be produced by ele`

### 0. Provenance (the misunderstanding, in his words)

> "He seems, however, to have misunderstood my position with respect to the cause of these discharges, which is not, as he implies, that luminosity in tubes without electrodes cannot be produced by electrostatic action, but that it can also be produced when this action is excluded"

- row: 81
- cited as: `(1894, p. 406)`
- why: the other half of the duelling pair, and it is a precise statement of Thomson's actual position, which is NOT that electrostatic action cannot light a tube. Without this row the article will make Thomson the opponent of the electrostatic explanation, which is exactly what he said he was not arguing. Pair with the p. 404 row
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `cts he observed to electrostatic action, and I have no doubt, from the description he gives of his method of conducting his experiments, that in them electrostatic action plays a very important part. He seems, however, to have misunderstood my position with respect to the cause of these discharges, which is not, as he implies, that luminosity in tubes without electrodes cannot be produced by electrostatic action, but that it can also be produced when this action is excluded. As a matter of fact, it is very much easier to get the luminosity when these electrostatic effects are operative than when they are not. As an illustration of this I may mention that the first exper`

### 5. What the internet gets wrong (the question is the wrong question)

> "Whilst the discharge of the jar is going on, it is difficult, and, from a theoretical point of view, undesirable, to eparate the effect into parts, one of which is called electrostatic, the other electromagnetic ; what we can prove is that in this case the discharge is not such as would be produced by electromotive forces derived from a potential function"

- row: 82
- cited as: `(1894, p. 406)`
- why: THOMSON'S sentence, and it is the modern answer to brief 12 item 5 stated in 1891: during a jar discharge it is difficult and theoretically undesirable to split the effect into an electrostatic part and an electromagnetic part. The article's beat 5 can end on this, because it is not a modern correction smuggled into a Victorian text - a participant in the dispute said it. The OCR prints 'eparate' for 'separate'; the quote carries it and the draft prints 'separate', which verifies only through the space-ignoring index
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `istribution of electricity. When the potential of the primary suddenly falls, this electrification will redistribute itself, and may pass through the rarefied gas and produce luminosity in doing so. "Whilst the discharge of the jar is going on, it is difficult, and, from a theoretical point of view, undesirable, to eparate the effect into parts, one of which is called electrostatic, the other electromagnetic ; what we can prove is that in this case the discharge is not such as would be produced by electromotive forces derived from a potential function. In my experiments the primary coil was connected to earth, and, as a further precaution, the primary was separated from the discharge tube by a screen of blotting paper, moistened with dilute sulphu`

### 0. Provenance (why the record is thin)

> "The account of the experiments in the Electrician was from a reporter's note, and was not written, or even read, by me"

- row: 83
- cited as: `(1894, p. 406)`
- why: THOMSON explaining why the published account of his own experiments was thin: a reporter wrote it and he did not read it. It is the reason the whole dispute in this chapter is unresolvable from the printed record, and it is a fact about sources that the article's sources section can state. It also explains Tesla's 'meagre description' jab
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `«en taken against the electrostatic effect. To correct misapprehension I may state that I did not read a formal paper to the Society, my object being to exhibit a few of the most typical experiments. The account of the experiments in the Electrician was from a reporter's note, and was not written, or even read, by me. I have now almost finished writing out, and hope very shortly to publish, an account of these and a large number of allied experiments, including some analogous to those mentioned by Mr. Tesla on th`

### 0. Provenance (the promise, and what the volume contains instead)

> "I have now almost finished writing out, and hope very shortly to publish, an account of these and a large number of allied experiments"

- row: 84
- cited as: `(1894, p. 406)`
- why: THOMSON'S promise at the end of his communication, and the article's sources section needs it: the fuller account he promised is not in this book. His communication's last words on printed p. 406 are 'for which, however, I must refer to my paper', and the chapter ends there. What the reader has here is a magazine article, an abstract, a reply and a note, which is the whole of the evidence base for this article
- check_quotes.py: exact match, ratio 1.0, printed p. 406
- raw OCR: `the Society, my object being to exhibit a few of the most typical experiments. The account of the experiments in the Electrician was from a reporter's note, and was not written, or even read, by me. I have now almost finished writing out, and hope very shortly to publish, an account of these and a large number of allied experiments, including some analogous to those mentioned by Mr. Tesla on the effect of conductors placed near the discharge tube, which I find, in some cases, to produce a diminution, in others an increase, in t`

## Printed p. 494 (scan file 512, 18 leaves of offset)

### 0. Provenance (the volume's own index entry for the chapter)

> "Electric Discharges in Vacuum Tubes"

- row: 10
- cited as: `(1894, p. 494)`
- why: the book's own label for the subject, from its index, printed p. 494, and the string the draft should use if it names the chapter at all. The index sets the page number '396' on its own OCR line, which strip_furniture drops as a bare folio, so 'Electric Discharges in Vacuum Tubes 396' does NOT verify on the default index (it comes back fuzzy 0.828) and does with --keep-furniture. Quote the label without the number, or say which index you used. The chapter's display heading is a different matter - see the flag THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE
- check_quotes.py: exact match, ratio 1.0, printed p. 494
- raw OCR: `mena... .. 212 Dynamos, Improved Direct Current 448 Early Phase Motors 477 Effects with High Frequency and High Potential Currents. 119 Electrical Congress Lecture, Chicago 486 Electric Resonance 340 Electric Discharges in Vacuum Tubes 396 Electrolytic Registering Meter. 420 Eye, Observations on the 294 Flames, Electrostatic, Non-Consuming 166,272 Forbes Unipolar Generator. 468, 474 Franklin Institute Lecture 294 Generators, Pyroma`

### 3. Tesla's lamp research (the volume's own index label for p. 253)

> "Carborundum Button for Tesla Lamps"

- row: 11
- cited as: `(1894, p. 494)`
- why: the index entry for the lamp passage, printed p. 494, and it names the thing in the book's own words: a carborundum BUTTON for Tesla lamps, at printed pp. 140 and 253. Useful if the draft wants to show the volume itself filed this under lamps and not under lighting theory. The index sets 'Lamps' and '140, 253' on their own OCR lines; the joined string verifies because '140, 253' is not a bare folio and so is not stripped
- check_quotes.py: exact match, ratio 1.0, printed p. 494
- raw OCR: `for Producing High Vacua 276 Arc Lighting, Tesla Direct, System 451 Auxiliary Brush Regulation ... 438 Biography, Tesla 4 Brush. Anti-Sparking 432 " Third, Regulation 438 Phenomena in High Vacuum 226 Carborundum Button for Tesla Lamps 140, 253 Commutator, Anti-Sparking. . . . 432 Combination of Synchronizing and Torque Motor 94 Condensers with Plates in Oil. . 418 Conversion with Disruptive Discharge 193,204, 303 Current or Dynami`

### 0. Provenance (the index entry for the brush chapter, article 06's)

> "High Potential, High Frequency : Brush Phenomena in High Vacuum"

- row: 12
- cited as: `(1894, p. 494)`
- why: the index entry that shows how the volume files the other high-vacuum light effect: 'Brush Phenomena in High Vacuum' at printed p. 226, which is chapter XXVII's own section and article 06's page. The two index labels - 'Electric Discharges in Vacuum Tubes' and 'Brush Phenomena in High Vacuum' - are the book's own distinction between the two things this series splits across two articles. Use it to keep 06 and 12 apart
- check_quotes.py: exact match, ratio 1.0, printed p. 494
- raw OCR: `olytic Registering Meter. 420 Eye, Observations on the 294 Flames, Electrostatic, Non-Consuming 166,272 Forbes Unipolar Generator. 468, 474 Franklin Institute Lecture 294 Generators, Pyromagnetic 429 High Potential, High Frequency : Brush Phenomena in High Vacuum 226 Carborundum Buttons.. 140, 253 Disruptivemena Discharge Pheno- 212 Flames, Electrostatic, NonConsuming 166, 272 Impedance, Novel Phenomena 194, 338 Lighting Lamps Through Body 359 Luminous Effect`

## Rejected: considered and not carried forward

(Numbered, because 'Rejected #N' is cited from the rows above and from the flags, and an unnumbered list cannot answer one. The numbers are the order of the REJECTED list in `gen_quotes.py`; nothing renumbers them.)

1. ~~"Of all these phenomena observed with currents, or electric impulses, of high frequency, the most fascinating for an audience are certainly those which are noted in an electrostatic field acting through considerable distance; and the best an unskilled lecturer can do is to begin and finish with the exhibition of these singular effects"~~ (p. 288): the showmanship sentence, and the one brief 12's beat 1 is really echoing. It verifies at ratio 1.0, and it is already printed verbatim on tesla-lit-lamps-without-wires.html with a p. 288 cite (measured: the sibling-overlap table below reports which pinned fragments already appear on a live page). Article 01 owns it. The article may link to that page and describe the move, but it may not print the sentence again
2. ~~"What change have I produced in the tube?"~~ (p. 288): the form books and quote-index.md section B print. It does NOT verify: the matcher returns only a fuzzy 0.987 window, because the print's question continues 'in the tube in the act of exciting it?'. The truncated form makes him ask a different, dumber question. Row 22 pins the real one
3. ~~"I should think that to any experimenter who had carefully studied the problem confronting us and who attempted to find a solution of it, this idea must present itself as naturally as"~~ (p. 396): the tidied form of the obviousness sentence, with the print's stray comma after 'should' removed. It does not verify: fuzzy 0.995, and the missing half a character is the comma. Row 9 pins it as set. Either quote the comma or do not quote the clause; a silently corrected Tesla is the failure mode this whole file exists to stop
4. ~~"the luminous effects, which are producible by induction in a tube devoid of electrodes, is of an electrostatic nature"~~ (p. 175): the trimmed version of the thesis sentence that drops 'I am inclined to consider as being'. It does not verify (the words 'is of an electrostatic nature' are not in the volume in that construction), and it turns a hedged opinion into a finding. Row 85 pins the hedged form, and the hedge is the point
5. ~~"Electric Discharges in Vacuum Tubes 396"~~ (p. 494): the index entry with its folio attached. On the default index it comes back fuzzy 0.828, because strip_furniture drops the bare '396' the index sets on its own OCR line; with --keep-furniture it is 1.0. Row 10 pins the label without the number. A draft that wants the number has to say which index it used
6. ~~"SOME EXPERIMENTS ON THE ELECTRIC DISCHARGE BY PROF. J. J. THOMSON"~~ (p. 402): the chapter's own display heading for the abstract. It is not in the index the gate uses, for the same reason as the row above: short all-caps lines are dropped as running heads. It is in the raw page body, so a reader who greps the file will find it and the gate will not. Name the abstract in prose instead of quoting a heading; see the flag THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE
7. ~~"Further exhaustion of the jar caused the secondary discharge to appear outside of the bulb"~~ (p. 403): the corrected spelling of row 59. It does not verify: the OCR prints 'J urther' with a space after the capital J, and the space-ignoring index glues that to 'Jurther', which is not 'Further'. Row 59 carries the scan's letters. This one is a judgement call the draft has to make consciously, not by accident: print the scan or print the print
8. ~~"an ordinary exhausted tube (preferably of large diameter) be surrounded by a spiral of thick copper wire serving as the primary, a feebly luminous spiral may be induced in the tube"~~ (p. 399): the joined form of row 40 with the cut removed. It does not verify: fuzzy 0.967 on the pinned page, measured, and the reason is the scan, not the print: the OCR sets 'primary^ afeebly', a footnote marker glued to the next word, so no comma-and-space form of the sentence is in the index. Row 40 cuts around it with ' ...', which is what check_quotes.py will accept in the draft
9. ~~"the circles were always in close proximity to the primary and were considerably easier produced when the latter was very close to the glass and these facts speak for an electrostatic effect"~~ (p. 400): the joined form of row 44. It does not verify: fuzzy 0.86, same cause, a figure label inside the run. Row 44 cuts
10. ~~"The production of a small electrode, capable of withstanding enormous temperatures"~~ (p. 258): the sentence a retelling of the lamp section wants. It does not verify: fuzzy 0.844, because the OCR reads 'sniall' for 'small' and 'wit hstan< ling' for 'withstanding' inside it. Two scan defects in eight words. Also printed p. 258 is inside the passage article 06's page already quotes. Read the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX
11. ~~"recourse was had to the oscillatory discharge of a"~~ (p. 402): the top of the Leyden-jar sentence, which is on printed p. 402. It verifies alone at ratio 1.0, and it must not be quoted alone: the object of the preposition is the first words of printed p. 403, and the two halves never join in the index, because the page's own footnote sits between them in the page body and strip_furniture keeps footnotes. Row 60 pins the p. 403 half and says so
12. ~~"An exhausted bulb, Fig. 217, containing traces of oxygen was placed within a primary spiral of three turns, and, on passing the jar discharge, a circle of light was seen within the bulb in close proximity to the primary circuit"~~ (p. 403): the cleaned form of row 62, with 'plaeed' repaired to 'placed' and 'inclose' split to 'in close'. It does not verify: the scan really prints those letters, and the space-ignoring index can glue a space but cannot un-glue a wrong letter. Row 62 carries the scan and cuts around the worst of it. This is the ring-of-light sentence the popular story puts on Tesla, and it is Thomson's apparatus either way
13. ~~"it was not until after six weeks' continuous experimenting"~~ (p. 406): verifies at ratio 1.0, and it is not his. It is J. J. Thomson describing his own Leyden-jar work inside the communication printed on p. 406. Rejected as an article-12 quote of Tesla's persistence, because every 'Tesla worked six weeks' sentence on the internet is this sentence misattached. Row 79 pins it as Thomson's; read the flag THE SIX WEEKS BELONG TO THOMSON
14. ~~"I take a tube in my hand and move it about, and it is lighted wherever I may hold it ... I may put it away for a few weeks or months, still it retains the faculty of being excited ... What change have I produced in the tube?"~~ (p. 288): the p. 288 block as quote-index.md section B prints it, three fragments in one quote. Rejected as one quote for two reasons: the last fragment is the truncated question of Rejected #2, and two of the three parts are already printed verbatim on article 01's page (measured). Quote the parts separately, each with its own citation, or link to article 01
15. ~~"In one of the experiments this evening a brush was produced at the end of a wire"~~ (p. 258): the cold-flame opening, and article 06's page prints it verbatim with a p. 258 cite (measured). It is a fine sentence and it is not this article's. Read the flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT
16. ~~"we may place a body of some refractory material in a closed, and preferably more or less exhausted, globe, connect it to a source of high, rapidly alternating potential, causing the molecules of the gas to strike it many times a second at enormous speeds, and in this manner, with trillions of invisible hammers, pound it until it gets incandescent"~~ (p. 175): the 'invisible hammers' sentence as one continuous run. It does not verify: the printed line ends 'connect it to a source of' and the next glyph in the OCR is a stray bullet, so the run has a '•' inside it that no normaliser removes. Row 87 cuts at it with ' ...' and says the cut is a scan artefact, not an elision in the text
17. ~~"powerful electrostatic eifects are a sitw qua -non of light production on the lines indicated by theory"~~ (p. 175): the strongest condition sentence in the New York lecture, and it verifies at ratio 1.0 only because the quote carries the scan's mangling: 'eifects' for 'effects' twice and 'sitw qua -non' for 'sine qua non'. Printed as set, a reader assumes the transcriber made the error; corrected, it does not verify. Paraphrase the condition and cite the page. Read the flag SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX
18. ~~"It is evident that the efficiencv in such cases is the greater, the higher the frequency, for the quicker the process of charging and discharging the molecules, the less energy will be lost in the form of dark radiation"~~ (p. 176): the theory behind the efficiency sentence in row 91, and the best statement in the volume of why he thought high frequency made light. It verifies only because the quote carries 'efficiencv', which is what the scan prints for 'efficiency' in that sentence; the corrected form does not verify there. Rejected on that ground, not on its content. The row-92 quote stops before it for the same reason
19. ~~"An intense phosphorescence then spreads at first over the globe"~~ (p. 228): does not verify: fuzzy 0.976. And printed p. 228 is inside 'Brush Phenomena in High Vacuum', the chapter section the volume's own index files at p. 226 (row 12 pins that index entry) and which article 06's page cites twice. Two independent reasons not to carry it
20. ~~"In bulbs provided with a conducting terminal, though it be of aluminum"~~ (p. 226): verifies, and it is the brush-in-a-high-vacuum bulb, which is article 06's subject and its page's beat, not this one's. Rejected to keep the two pages apart; the volume's own index labels put them in different sections (row 12)
21. ~~"It is now a fact that a body may be rendered incandescent or phosphorescent"~~ (p. 236): does not verify at all: no window clears the fuzzy floor anywhere in the volume. The sentence is a paraphrase remembered as a quote. If the article wants that claim it has to be written as prose, not inside quote marks
22. ~~"I think that in a bulb a molecule, or atom, does not precisely move in a straight line"~~ (p. 282): does not verify at all (no match anywhere). The mean-free-path passage on printed p. 282 says something adjacent in different words, and 'mean free path' is in the volume 5 times (measured), so the mechanism is quotable - but not this sentence, and not from memory
23. ~~"Any one who has studied Crookes' work must have received the impression that the ' radiant state ' is a property of the gas inseparably connected with the vacuum"~~ (p. 282): the outer clause verifies on its own, but the block cannot be quoted as one run: the print sets its own quote marks around ' radiant state ', and check_quotes.py's scanner pairs quote marks, so the inner pair ends the quote early and everything after it is mis-paired. Cut before the inner marks or drop the block. 'Radiant state' is Crookes' vocabulary, which is a second reason to be careful whose words are being printed
24. ~~"A thought which early and naturally suggested itself to Mr. Tesla, was the possibility of producing light and heat by molecular bombardment"~~ (p. 141): does not verify: no match at all, and the sentence is the compiler's third person about him, not his writing. It is the shape every retelling uses and the reason this pin exists. The same idea in his own first person is row 87 and row 89
25. ~~"it is conceivable that a person entirely nude at the North Pole might walk barefoot on the snow"~~ (p. 395): does not verify: no match at all. A remembered image from the high-frequency safety material; the real sentences there are article 01's p. 125 quote (read the flag ARTICLE 01 OWNS THE SAFETY SENTENCE)
26. ~~"The eternal recipient and transmitter of this infinite energy is the ether."~~ (p. 145): verifies, and article 01's page already prints it with a p. 145 cite (measured). It is also the sentence the free-energy myth feeds on, and article 10's page is the series' answer to that. Rejected here on both counts
27. ~~"We are whirling through endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy."~~ (p. 196): the London lecture's closing flourish, carried in Appendix A and quote-index.md section L, and it straddles printed pp. 196-197 as one run. Nothing to do with a tube, and another page's to use. Listed so a writer reaching for a grand ending finds the reason not to
28. ~~"Here is a simple glass tube from which the air has been partially exhausted. I take hold of it ; I bring my body in contact with a wire conveying alternating currents of high potential, and the tube in my hand is brilliantly lighted."~~ (p. 200): the other tube-in-hand demo, from the same February 1892 lecture, printed verbatim on article 01's page with a p. 200 cite (measured). Article 01 is the page for that demonstration; this article's is the p. 288 one. Read the flag FOUR TEXTS, FOUR VOICES, ONE CHAPTER before writing a sentence that says 'he always opened with'
29. ~~"tubes devoid of any electrodes may be used, and there is no difficulty in producing by their means sufficient light to read by"~~ (p. 187): verifies, and article 01's page prints it verbatim with a p. 187 cite (measured). It is also the closest thing in the volume to a brightness claim for an electrodeless tube, so if the draft wants it, it has to credit article 01 and link, not re-quote
30. ~~"the observer may, standing upon an insulated support between coil and tube, light the latter by approaching the hand to it"~~ (p. 186): verifies, and article 01's page prints it verbatim with a p. 186 cite (measured). Row 92 pins a different sentence from the same printed page; read the flag ARTICLE 01 HAS THREE SENTENCES ON p. 186 AND p. 187
31. ~~"the singular effect of wiping out the light of the tube may be produced by passing the hand quickly along the tube"~~ (p. 186): verifies, and article 01's page prints it verbatim with a p. 186 cite (measured). Same flag as the row above
32. ~~"In all cases the insulated body serves to give off the energy into the surrounding space, and is equivalent to a return wire."~~ (p. 184): verifies, and article 01's page prints it verbatim with a p. 184 cite (measured). Row 37 exists precisely so this article can point at that sentence in one clause instead of reprinting it
33. ~~"X rays"~~ (not in this volume): not a quote but a claim check, and the one brief 12 flags with 'needs source'. No spelling of it is in the volume: 'X-ray' 0, 'X rays' 0, 'x ray' 0, 'Röntgen' 0, 'roentgen' 0 (measured, all three indices). Röntgen's paper was December 1895 and this volume's newest text is February 1892. There is nothing to quote, so the article must not imply a connection; read the flag THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895
34. ~~"light without energy"~~ (not in this volume): the phrase brief 12 item 5 says the internet gets wrong. It is not in the volume (0 hits, measured), so nobody in 1894 said it and it cannot be quoted at him. The correction has to be made against the modern phrase, with his own conservation sentence (row 27) as the counterweight
35. ~~"the pleasure I have had in presenting these results to a gathering of so many able men - and among them also some of those in whose work for many years past I have found enlightenment and constant pleasure - I shall never forget"~~ (p. 293): the full closing sentence of chapter XXVII, carried in quote-index.md section L. It verifies at ratio 1.0 (the normaliser folds the dashes), and it cannot be printed: section 0 non-negotiable 5 forbids em and en dashes in series prose, and the print sets two pairs of them around a paren-thought. Row 34 pins the dash-free half, which is all a draft of this series can use

## Flags for the writer (§3 quote policy, §4.1 guardrail, feature-006/t10)

- **FOUR TEXTS, FOUR VOICES, ONE CHAPTER** — Chapter XXXII, printed pp. 396-406, is not one text. The footnotes on the pages date four: Tesla's own article in The Electrical Engineer, N. Y., July 1, 1891 (row 1); an abstract of a paper read by Prof. J. J. Thomson to the Physical Society of London (the footnote on printed p. 402, and the heading Rejected #6); Tesla's reply in the same magazine, Aug. 26, 1891 (the footnote on printed p. 404); and Thomson's note in the London Electrician, July 24, 1891 (the footnote on printed p. 406). Two more texts this article quotes are whole chapters of their own: chapter XXVI, the New York lecture of May 20, 1891 (row 14), and chapter XXVII, the London lecture of February 1892 (row 13). So 'Tesla wrote it in 1894' is wrong six different ways: the volume is 1894, the texts are 1891 and 1892, and three of the passages in chapter XXXII are not by him. Every sentence in the draft that attributes something has to name which text and which man. The footnotes are the evidence and rows 1, 13, 14 pin them
- **TWO THOMSONS IN ONE PARAGRAPH** — Printed p. 396 names J. J. Thomson and Elihu Thomson within two sentences (rows 3 and 4). J. J. is the Cambridge man whose abstract and note fill pp. 402-406; Elihu is the American, a different experiment, in a different magazine. The chapter's own prose says 'Prof. Thomson' unqualified, which in context means J. J. A draft sentence that says 'Thomson' without a first initial is ambiguous in exactly the way the source is not. Spell out which one, every time
- **THE ABSTRACT IS THIRD PERSON AND THE PROSE IS FLUENT, WHICH IS THE TRAP** — The abstract on printed pp. 402-403 is reportage about Thomson's work in the third person ('the author had also observed', 'Prof. Thomson said'), and it reads like the surrounding prose, which is why it is so often quoted as Tesla's. Row 54, row 60, row 62, row 63 and row 64 are all inside it. The tell is grammar: 'he', 'the author', 'Prof. Thomson said' versus Tesla's 'I', 'my experiments', 'in my experiments they were broad'. Before any quote from pp. 402-406 goes in the draft, check which of the four texts it came from and whose pronouns it uses
- **THE SIX WEEKS BELONG TO THOMSON** — The most-misquoted sentence in this article's sources: 'it was not until after six weeks' continuous experimenting that I was able to get a discharge in the exhausted tube which I was satisfied was due to what is ordinarily called electrodynamic action' (row 79). The 'I' is J. J. Thomson, in his own published note on printed p. 406, about his own Leyden-jar apparatus. Tesla's own bench time is dated differently, and by himself: 'My investigations in this line occupied me principally during the winter and spring of the past year' (row 2), relative to a July 1891 issue. If the article wants a duration, it has to say whose
- **TWO MEN, ONE VOLUME, EACH SAYING THE OTHER MISREAD HIM** — Printed p. 404, Tesla: 'I did not, as Prof. J. J. Thomson seems to believe, misunderstand his position' (row 67). Printed p. 406, Thomson: 'He seems, however, to have misunderstood my position' (row 81). Both sentences are in the volume, one page apart, and both are about the same question, which is whether the effect can be produced with electrostatic action EXCLUDED (Thomson's actual position, row 81) rather than whether it can be produced by it. Print the pair or print neither. A story where one of them wins is not supported by these pages
- **THE RING OF LIGHT IS THOMSON'S, THE BROAD GLOW IS TESLA'S** — The popular drawing - a thin ring of light inside a bulb near a coil - is Thomson's observation, in his abstract, on printed p. 403 (row 62, 'a circle of light was seen within the bulb inclose proximity to the primary circuit, accompanied by a purplish glow, which lasted for a second or more'). Tesla's reply on printed p. 400 is a claim about a different appearance: 'in my experiments they were broad and often the whole of the bulb or tube was illuminated' (row 45). The two descriptions are in the same chapter and disagree. The article should say which drawing belongs to which man, because the retellings do not
- **THE BRIEF'S FIG. 218 IS THOMSON'S APPARATUS** — Brief 12 shortlists Figs. 210, 212, 215 and 218. Fig. 218 is on printed p. 403, inside the abstract, and the text beside it is Thomson's (rows 61-63 are the sentences on those pages). Fig. 216, on printed p. 402, is also Thomson's and is named in row 61 for exactly that reason. A caption that says 'Tesla's apparatus' under a crop from pp. 402-403 is a factual error about a figure the reader can see. Read the figure notes before writing any caption
- **PRIORITY IN THIS CHAPTER IS ABOUT WHO PUBLISHED AND WHO NOTED** — He names the prior art himself: 'the luminosity in a tube near a wire through which a Leyden jar was discharged was noted by Hittorf' (row 76, printed p. 405, and 'Hittorf' is in the volume 1 time, there). And his own claim is about intensity, not firstness: 'been noted by many experimenters, but in my experiments the effects were much more powerful than those usually noted' (row 77). Plus the disclaimant on printed p. 396: 'The idea being obvious, whatever merit there is in this line of investigation must depend upon the completeness of the study' (row 7). The article may say his effects were stronger and that he said so. It may not say he discovered it
- **HE SAYS WHAT HE DID NOT DO, IN FOUR WAYS** — Four admissions, in four different texts, all in this pin: 'For want of time I have, however, not been able to perform the experiment' (row 53, printed p. 401); 'the experimental verification of the law, whatever it may be, would be exceedingly difficult' (row 94, printed p. 213); 'The time has been too short to make a satisfactory study of the properties of this product' (the carborundum row, printed p. 254); and 'I have now almost finished writing out, and hope very shortly to publish, an account of these and a large number of allied experiments' (row 84 - which is Thomson's, and the promised account is not in this book). Any claim the draft reports as his finding should be checked against these four first
- **HE TRIED TO SCREEN IT OUT AND THE SCREENING FAILED** — The discriminating tests are in the sources and they cut both ways. Tesla: a glass tube T slipped between primary and bulb changes the effect, 'were the action wholly electromagnetic no change could possibly have been observed' (row 49); a closed wire round the bulb does not stop the light (row 51); a broad tinfoil strip does (row 52). Thomson: a wet blotting-paper screen to earth, which stops a stationary electrostatic effect and does not stop alternating electromotive waves (row 78), and his criticism that the published account did not show 'all possible precautions had been taken to exclude these effects' (row 68). Tesla's own answer is that he saw 'curious instances of the ineffectiveness of the screening' (row 69). The article should present the screening argument as the live disagreement it was, not as Tesla having proved the point
- **HE ANSWERS HIS OWN QUESTION ON THE NEXT PAGE AND NOBODY QUOTES IT** — Printed p. 288 he asks 'What change have I produced in the tube in the act of exciting it?' (row 22) and weighs two answers, motion in atoms and strain in the dielectric, rejecting both for stated reasons (rows 23, 24). Printed p. 405, in the reply to Thomson, he sketches the mechanism that dissolves the question: one instantaneous flash if the charge is stationary, permanent excitation if it keeps moving, because 'a constant redistribution of electricity' keeps colliding the gas molecules (row 72). It is a thought experiment, and he marks it as one ('Assuming', 'suppose'). The honest ending for beat 5 is that the question was asked in 1892, and an answer of a kind was printed in 1891 and never run as a test
- **SPELLINGS THE BOOK GETS WRONG AND THE DRAFT MUST NOT SILENTLY FIX** — Measured inside this article's own quotes: 'vaciium' for 'vacuum' (row 64, printed p. 402), 'plaeed' for 'placed' and 'inclose' for 'in close' (row 63, p. 403), 'viorate' for 'vibrate' (row 89, p. 176), 'Avill' for 'Will' and 'II. S. A.' for 'U. S. A.' (the two carborundum rows, p. 253), 'efficiencv' for 'efficiency' (Rejected #18, p. 176), 'eifects' and 'sitw qua -non' (Rejected #17, p. 175), 'f rictional' with a space after the f (row 23, p. 288), 'J urther' (row 59, p. 403), 'eparate' for 'separate' (row 82, p. 406), 'sniall' and 'wit hstan< ling' (Rejected #10, p. 258). The rule this pin uses: a quote carries the scan, and where the scan is unreadable the quote is cut or the sentence is paraphrased and cited. What is not allowed is a silently corrected 1894, because the reader cannot check it and the gate cannot check it either - the matcher fails on the corrected form
- **THE CHAPTER TITLE IS NOT IN THE INDEX BUT THE SAME WORDS ARE** — The chapter's display heading and the contents-page line do not verify on the index the gate uses, because strip_furniture drops short all-caps lines as running heads (Rejected #6). What does verify is the volume's own index label, 'Electric Discharges in Vacuum Tubes' (row 10, printed p. 494), and the first words of the chapter's own first sentence (row 3). If the draft names the chapter, it names it the way the index does, without a page number, or it does not put the name in quote marks
- **ARTICLE 01 OWNS THE p. 288 SENTENCES IT HAS ALREADY PRINTED** — Measured, not remembered: the sibling-overlap table below checks every fragment in this pin against the rendered text of the live series pages. Article 01's page prints the showmanship sentence (Rejected #1), 'I may put it away for a few weeks or months, still it retains the faculty of being excited' (row 21) and 'What change have I produced in the tube in the act of exciting it?' (row 22), all cited to p. 288. Rows 21 and 22 are pinned here because brief 12 item 1 quotes them, and the article cannot raise the question without the question sentence. So: use them, but say they are the same passage article 01 has, and link to that page. The one p. 288 sentence article 01 has NOT printed is the hook, row 18
- **ARTICLE 01 HAS THREE SENTENCES ON p. 186 AND p. 187** — Measured from the rendered page: article 01 quotes two sentences from printed p. 186 (the insulated-support sentence and the wiping-out-the-light sentence, Rejected #29 and #30) and one from p. 187 (the read-by sentence, Rejected #28). Row 92 pins a fourth sentence from p. 186, the one that says the tube is lighted by condenser action, and that one is free. The page is shared; the sentences are not. Do not put two article-01 sentences and this one in the same paragraph as if they were one passage
- **ARTICLE 01 OWNS THE SAFETY SENTENCE** — The p. 125 sentence about physiological effects being small is on article 01's page with its own caution attached. Row 90 pins a different observation, from the New York lecture of May 1891: at low frequency a four-foot tube with condenser coatings gives a shock he thinks could do 'serious injury to those not accustomed to such shocks', and at twenty thousand alternations per second the same brightness is felt as nothing. The two are not the same claim and must not be blended into one sentence about safety. Neither is a safety instruction for a reader at home
- **ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT** — Measured from the rendered page: article 06's page prints the brush-flame sentences at printed pp. 258-259, and it prints the p. 213 law ('the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential') and the first clause of the p. 213 hedge. Rows 93 and 94 are pinned here because the law is the best evidence in the volume that he wanted a controlled test and said he had not done it. If the draft uses them it must say the series' cold-flame page has them too, and link. The volume's own index also splits the two subjects: 'Brush Phenomena in High Vacuum' at p. 226 (row 12) is article 06's, 'Electric Discharges in Vacuum Tubes' at p. 396 is this one's
- **THE VOLUME CANNOT MENTION A DISCOVERY MADE IN DECEMBER 1895** — Brief 12 flags an X-ray connection as 'needs source: do not assert without a citation'. There is no citation, because the words are not there: 'X-ray' 0 hits, 'X rays' 0, 'x ray' 0, 'Röntgen' 0, 'roentgen' 0, measured on all three indices. And the volume says its own limit: 'The present volume deals simply with his work accomplished to date' (row 15, printed p. 6), with the compiler adding that work in progress is being held back (row 16). The newest text this article quotes is February 1892. So the absence of X-rays from these chapters is not a finding about Tesla's foresight either way; it is a date fence. Do not write 'he never saw X-rays' as a fact about him, and do not write 'he anticipated them'
- **THE WORDS 'VACUUM TUBE' AND 'CAPACITOR' DO NOT MEAN WHAT THE QUERY MEANS** — Measured: 'vacuum tube' is in the volume 12 times, and inside chapter XXXII alone 4 times (printed pp. 396, 403, 404). It does not mean a thermionic valve: it means a tube exhausted of air, and the period's usual phrase is 'exhausted tube' (32 hits). 'capacitor' is 0, and the component he reasons with is a 'condenser' (218 hits). 'electron' is 0, 'watt' 0, 'candlepower' 0 though 'candle power' as two words is 5, 'ionis' 1, 'ultraviolet' 0, 'free energy' 0. A reader searching 'tesla vacuum tube experiment' wants 1904, and this book is 1891-1892. The article should say what the words meant then, and not let the modern word stand unexplained
- **NO NUMBER IN THIS ARTICLE'S SUBJECT, AND THE ABSENCE IS THE CLAIM** — Measured over chapter XXXII, printed pp. 396-406: 'test' 0, 'efficiency' 0, 'per cent' 0, 'watt' 0, 'candle power' 0, 'volts' 0, 'ampere' 0, 'output' 0, 'commercial' 0, 'measure' 0, 'striae' 0, 'Geissler' 0, 'X-ray' 0. Over the carborundum passage, printed pp. 253-259: 'efficiency' 0, 'per cent' 0, 'watt' 0, 'candle power' 0, 'volts' 0, 'ampere' 0, 'output' 0, 'cost' 0, 'life' 0, 'hours' 0. What those chapters do contain is the word 'experiment' 38 times in chapter XXXII and 10 times in the lamp passage, and comparative sentences with no numbers on them. So the article may write: he described apparatus and comparisons and printed no measurement of the light. It may not write that he failed to measure something he never claimed to have measured, and it may not print a figure of its own inventing one
- **THE BRIEF'S FIGURE NAMES ARE PRINTED PAGES AND THE FILES ON DISK ARE SCAN FILES** — Brief 12 lists 'tesla1894-p400-fig215', 'p403-fig218', 'p403-fig212', 'p397-fig210'. None of those four file names exists. The extractor names its crops by SCAN file, and printed page = scan file - 18, so the real files are p415-fig1-fig210 (printed 397), p416-fig1-fig212 and p416-fig2-fig212 (printed 398), p418-fig1-fig215 and p418-fig2-fig215 (printed 400), p421-fig1-fig218 (printed 403). The figure notes below enumerate what is actually on disk and in the two manifests. This is the same trap article 08's whole-pin pass hit at pp. 480-482

## Notes for the figure task (feature-006/t6, a12-figrec)

- Crops touching printed pp. 396-406 and the lamp passage, read out of the site directory and both manifests at generation time (the extractor names by scan file, the re-crops by printed page, which is why one list is not enough): p397-fig210.webp (printed p. 397; named by printed page; re-crop, manifest_qc.csv only; QC verdict keep); p403-fig218.webp (printed p. 403; named by printed page; re-crop, manifest_qc.csv only; QC verdict keep); p415-fig1-fig210.webp (printed p. 397; named by scan file; extractor crop, manifest.csv row 415->397; QC verdict keep); p416-fig1-fig212.webp (printed p. 398; named by scan file; extractor crop, manifest.csv row 416->398; QC verdict keep); p416-fig2-fig212.webp (printed p. 398; named by scan file; extractor crop, manifest.csv row 416->398; QC verdict keep); p417-fig1-fig214.webp (printed p. 399; named by scan file; extractor crop, manifest.csv row 417->399; QC verdict keep); p418-fig1-fig215.webp (printed p. 400; named by scan file; extractor crop, manifest.csv row 418->400; QC verdict keep); p418-fig2-fig215.webp (printed p. 400; named by scan file; extractor crop, manifest.csv row 418->400; QC verdict keep); p420-fig1-fig216.webp (printed p. 402; named by scan file; extractor crop, manifest.csv row 420->402; QC verdict keep); p421-fig1-fig218.webp (printed p. 403; named by scan file; extractor crop, manifest.csv row 421->403; QC verdict keep). The brief's four names are printed pages, not file names; see the flag THE BRIEF'S FIGURE NAMES ARE PRINTED PAGES AND THE FILES ON DISK ARE SCAN FILES
- FIG. 210, printed p. 397, is the one figure in the shortlist whose own description is quotable from the same page: 'Fig. 210 may serve as an example of one of the many forms of apparatus used. This consisted of a large glass tube sealed at one end and projecting into an ordinary incandescent lamp bulb' (row 36). Caption from the text beside the crop, figure number read off the print, per section 6.6. The QC row already on file says keep, subject 'Vacuum lamp with an internal cylindrical element on a stem', quality A, caption_ok yes - read it before re-rendering the page
- FIG. 212, printed p. 398, has TWO bands on disk (p416-fig1 and p416-fig2). The QC rows say: fig1 keep, quality B, 'Thin band; usable full-width only'; fig2 keep, quality C, caption_ok no, 'Dark plate - negate; low illustrative value'. If the article uses 212 it uses fig1, full width, and says what the circuit diagram shows in the caption rather than letting a thin band float
- FIG. 215, printed p. 400, also has TWO bands. The QC rows call fig1 a dark plate with 'subject ambiguous, verify against p.400 text before use' and fig2 'A spiral coil wound round a cylinder with a vacuum lamp suspended inside, leads P and P1', quality A, 'Clean; good lamp inside a coil illustration'. The text that matches fig2 is row 40, on printed p. 399: 'an ordinary exhausted tube (preferably of large diameter) be surrounded by a spiral of thick copper wire serving as the primary ... feebly luminous spiral may be induced in the tube' (the scan sets 'primary^ afeebly', so the quote starts the second fragment at 'feebly'; read row 40). Use fig2. The QC note's 'verify against p.400 text' is answered by that row, and 'feebly' is the word the caption should carry, not 'blazing'
- FIG. 216 (printed p. 402) and FIG. 218 (printed p. 403) are THOMSON'S apparatus, inside the abstract (rows 61, 62, 63; read the flag THE BRIEF'S FIG. 218 IS THOMSON'S APPARATUS). The QC row for p420-fig1-fig216 already notes 'OCR FIG. 2V is a mis-read; two book figures in one band' and caption_ok no. If either is used, the caption names J. J. Thomson and the abstract, and the alt text says so too
- The lamp passage has its own figures, which the brief does not list but beat 3 might want: the carborundum button apparatus is described on printed pp. 254-255 and the Crookes radiometer-type apparatus at printed p. 176 (Fig. 114, Fig. 115, named in the text beside them). Check the manifest before promising any of them; nothing in this pin has verified a lamp figure against a scan, and the figure task must not caption an unviewed crop

## Links (§5.2 row 12, for feature-006/t5 and a12-wirecommit)

- Section 5.2 row 12: article 12 links out to `free-electricity-from-magnets.html`, `electricity-using-magnets.html`, article 01 and article 06, and must be linked from 01, 06 and the hub. Four out-links is the minimum the plan sets; the two money pages are the bridge brief 12 item 6 asks for
- Measured on the date above: neither `tesla-lit-lamps-without-wires.html` nor `tesla-cold-flame.html` contains a link to `tesla-glowing-tubes-vacuum.html` yet (0 occurrences of the file name across the whole site). The in-links the plan requires do not exist until the wiring task adds them, and qa_page.py's dead-link gate is the thing that will catch a link added before the page exists. Add the page first, then the backlinks, in one commit
- The bridge to the free-energy pages is legitimate only through his own conservation sentence: 'no consumption of material, but merely a transfer of energy' (row 95) and 'it was necessary to economize the energy which is obtained from the field' (row 27). Article 10's page is the series' trust piece on what the book does and does not say about free energy, and 'free energy' is 0 in the volume (measured). Do not let a p. 289 sentence sit next to a modern energy claim in a way that makes the book endorse it
- Article 01 is the page for the 1891 New York demonstration and the p. 184 return-wire explanation (Rejected #31, and row 37 links rather than re-quotes). Article 06 is the page for the brush and the cold flame and it already prints the p. 213 law (read the flag ARTICLE 06 OWNS THE COLD FLAME AND THE p. 213 LAW WITH IT). Every overlap this pin found is listed in the sibling-overlap table below; the draft should link at each one instead of reprinting
- Canonical URL `/tesla-glowing-tubes-vacuum`, file `tesla-glowing-tubes-vacuum.html` (section 5.1 row 12). The plan's note is explicit: `/tesla-glowing-tubes-before-tubes` only makes sense as an alias and an alias costs a hop; prefer the file name and write no `_redirects` rule. tid `1894_12`, FAQ schema yes, 1,300 words (section 9 brief 12)

Do not run `check_quotes.py` on this file as a gate. It is built for a draft (`article.md`), and here its scanner reads the apostrophes in the '- why:' annotations and the struck-through Rejected items as quotation marks, so any count it prints for this file is a count of this file's own prose. The gate for a pin file is `gen_quotes.py` itself: it imports the same matcher (`check_quotes.fragments` + `check_quotes.locate` over the index `check_quotes` builds), writes each quote to this file the moment it verifies, and if a quote does not verify it reports the failure and leaves the confirmed quotes on disk marked PARTIAL rather than throwing the run's work away. `check_quotes.py` runs on `article.md` in feature-006/t7.

## How this file checks itself

`gen_quotes.py` re-reads the file it has just assembled and prints the result here, so a claim in this pin is a claim the generator can re-run, not a claim a reader has to trust. Run `python3 gen_quotes.py` in this directory to reproduce every number in the file, including the ones in this section. If any line below says FAIL, the file is still written (so a restart resumes from the confirmed quotes rather than re-pinning them) and the script exits non-zero.

row structure: 115 quote blocks re-parse to 115 `> "` lines, 115 `- cited as:` lines, 115 `- why:` lines and 115 `- check_quotes.py:` annotations - no row is missing one
every `- cited as:` page is the page of the `## Printed p.` heading it sits under: 0 exceptions
no quote is pinned twice: 0 duplicates over 115 quote lines
every 'Rejected #N' reference names a row that exists: 15 distinct references, highest #34, against 35 rows, 0 unresolved
every flag, figure-note, link-note and section name cited in the prose exists in this file: 0 unresolved. 0 of 21 flags are never cited from the prose (none)
every fragment re-grepped through grep_quote.py's own index (load_pages + build_index + find_hits), each restricted to the printed page this file pins it to: 118 fragments - 115 return only exact hits, 3 return a fuzzy window there and verify here through the space-ignoring index check_quotes.py additionally builds, 0 return nothing
  - p. 399 'two intensely luminous circles, each of them ' - best 0.984 on that index
  - p. 402 'the introduction of mercury or the heating of' - best 0.985 on that index
  - p. 405 'an oxygen tube when excited under similar con' - best 0.974 on that index
the header's stated counts are re-parsed out of the rendered body and agree: quotes 115, fragments 118, printed pages 29, Rejected rows 35, flags 21, counted terms 60, spelling variants 15, scoped counts 30 - 0 disagreements
every 'row N' reference names a quote this pin actually carries (the numbering is the order of the QUOTES list in `gen_quotes.py`, and each block below prints its own `- row:` line): 55 distinct references, highest #95, against 115 rows, 0 unresolved
every 'row N' reference that quotes the words it points at resolves to the row it names: 22 of the 55 references quote their target and are checkable this way, 0 mismatches
