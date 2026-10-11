# Article 05 quote pin: tesla-high-frequency-massage.html

SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped on 2026-10-11 from `books/extracted/tesla-1894-plain.txt` through the same matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR spacing is ignored) and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). A quote carrying ' ... ' is cut where the scan is corrupt; each side of the cut is verified separately, which is how check_quotes.py will judge the draft. `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. Three different texts are quoted and they are not the same paper:

- chapter XXXI, 'MASSAGE WITH CURRENTS OF HIGH FREQUENCY' (printed pp. 394-395) - Tesla's own paper, The Electrical Engineer, Dec 23 1891. This is the article's spine. Printed pp. 394, 395.
- chapter XXX, 'ALTERNATE CURRENT ELECTROSTATIC INDUCTION APPARATUS' (printed pp. 392-393) - a different paper, The Electrical Engineer, May 6 1891, and the chapter whose apparatus the brief's figure comes from. Printed p. 393.
- chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY', Columbia College, New York, May 20 1891 (printed pp. 145-197) - the physiological caution, which the book's own index (printed p. 495) files under 'Physiological Effects... 162, 394' together with the massage paper. Printed p. 162.

Verified: 24 quotes (24 fragments) across 4 printed pages, 0 failures. To re-check one quote: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>`. To regenerate this file: `python3 new_content/1894-series/05-tesla-high-frequency-massage/gen_quotes.py` (it exits non-zero and writes nothing if any quote fails).

## Printed p. 162 (scan file 180)

### 5. What the internet gets wrong

> "while it is an undeniable fact that they are incomparably less dangerous than currents of low frequencies, it should not be thought that they are altogether harmless"

- cited as: `(1894, p. 162)`
- why: the caution, from a different text (ch. XXVI, the Columbia College lecture of May 20 1891). The book's own index files this page with p. 394 under 'Physiological Effects'; see flags. Say which text it is from
- check_quotes.py: exact match, ratio 1.0, printed p. 162
- raw OCR: `..., but all the material, insulating and conducting, is uniformly heated. To avoid misunderstanding in regard to the physiological effect of alternating currents of very high frequency, I think it necessary to state that, while it is an undeniable fact that they are incomparably less dangerous than currents of low frequencies, it should not be thought that they are altogether harmless. What has just been said refers only to currents from an ordinary high tension induction coil, which currents are necessarily very small ; if received directly from a machine or from a secondary of low resistance, they...`

### 5. What the internet gets wrong

> "if received directly from a machine or from a secondary of low resistance, they produce more or less powerful effects, and may cause serious injury, especially when used in conjunction with condensers"

- cited as: `(1894, p. 162)`
- why: the same caution continued: the danger comes back with the size of the source. This is the §4.1 safety sentence, in his words rather than ours
- check_quotes.py: exact match, ratio 1.0, printed p. 162
- raw OCR: `...s of low frequencies, it should not be thought that they are altogether harmless. What has just been said refers only to currents from an ordinary high tension induction coil, which currents are necessarily very small ; if received directly from a machine or from a secondary of low resistance, they produce more or less powerful effects, and may cause serious injury, especially when used in conjunction with condensers.`

## Printed p. 393 (scan file 411)

### 6. Bridge: spotting a modern overclaim

> "The output of such an apparatus is very small"

- cited as: `(1894, p. 393)`
- why: the honest scale of the machine the article's figure shows (ch. XXX, the electrostatic induction apparatus). Different paper, different date: see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 393
- raw OCR: `...s is illustrated in Fig. 209. In this apparatus the two sets of tin-foil coatings are glued on a plate of ebonite, and a similar plate which is rotated, and the coatings of which are charged as in Fig. 208, is provided. The output of such an apparatus is very small, but some of the effects peculiar to alternating currents of short periods may l>e observed. The effects, however, cannot be compared with those obtainable with an induction coil which is operated by an alternate curren...`

### 6. Bridge: spotting a modern overclaim

> "The effects, however, cannot be compared with those obtainable with an induction coil which is operated by an alternate current machine of high frequency"

- cited as: `(1894, p. 393)`
- why: and what he said it was inferior to. The test any modern claim can be put through: what is the source, and what is its output
- check_quotes.py: exact match, ratio 1.0, printed p. 393
- raw OCR: `...h is rotated, and the coatings of which are charged as in Fig. 208, is provided. The output of such an apparatus is very small, but some of the effects peculiar to alternating currents of short periods may l>e observed. The effects, however, cannot be compared with those obtainable with an induction coil which is operated by an alternate current machine of high frequency, some of which were described by me a short while ago.`

## Printed p. 394 (scan file 412)

### 1. The paper, and its defensive opening

> "I trust that the present brief communication will not be interpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness"

- cited as: `(1894, p. 394)`
- why: the brief's opening quote in full. The 1894 page sets "patent medicine" in double quotes and the whole run verifies exactly with them; see the flags for how check_quotes.py splits the run in the draft
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `CHAPTER XXXI. " MASSAGE " WITH CURRENTS OF HIGH FREQUENCY.1 I TRUST that the present brief communication will not be interpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have...`

### 1. The paper, and its defensive opening

> "for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness"

- cited as: `(1894, p. 394)`
- why: the half that carries the point, with no nested quote marks in it. Safe on its own; Appendix A registers this fragment at p. 394
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `CHAPTER XXXI. " MASSAGE " WITH CURRENTS OF HIGH FREQUENCY.1 I TRUST that the present brief communication will not be interpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness. My remarks are elicited by the lively interest which prominent medical practitioners evince at every real advance in electrical investigation. The progress in recent years has been so great that every electrician and e...`

### 1. The paper, and its defensive opening

> "My remarks are elicited by the lively interest which prominent medical practitioners evince at every real advance in electrical investigation"

- cited as: `(1894, p. 394)`
- why: why the paper exists at all: doctors were writing to him. Sets up the market vs. the worker contrast
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...erpreted as an effort on my part to put myself on record as a "patent medicine" man, for a serious worker cannot despise anything more than the misuse and abuse of electricity which we have frequent occasion to witness. My remarks are elicited by the lively interest which prominent medical practitioners evince at every real advance in electrical investigation. The progress in recent years has been so great that every electrician and electrical engineer is confident that electricity will become the means of accomplishing many things that have been heretofore, with our existin...`

### 1. The paper, and its defensive opening

> "I have received many letters from noted physicians inquiring as to the physical effects of such currents of high frequency"

- cited as: `(1894, p. 394)`
- why: the demand, in his own words: physicians asking what the currents do to a body
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...pect to find in it a powerful tool and help in new curative processes. Since I had the honor to bring before the American Institute of Electrical Engineers some results in utilizing alternating currents of high tension, I have received many letters from noted physicians inquiring as to the physical effects of such currents of high frequency. Itmay be remembered that I then demonstrated that a body perfectly well insulated in air can be heated by simply connecting it with a source of rapidly alternating high potential. The heating in this case is due in all...`

### 1. The paper, and its defensive opening

> "progressive physicians also should expect to find in it a powerful tool and help in new curative processes"

- cited as: `(1894, p. 394)`
- why: the most he concedes to the medical use at the top of the paper. Starts after the OCR's garbled 'No wonder then'; see rejected
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...very electrician and electrical engineer is confident that electricity will become the means of accomplishing many things that have been heretofore, with our existing knowledge, deemed impossible. ]Sro wonder 'then that progressive physicians also should expect to find in it a powerful tool and help in new curative processes. Since I had the honor to bring before the American Institute of Electrical Engineers some results in utilizing alternating currents of high tension, I have received many letters from noted physicians inquiring as to th...`

### 2. The mechanism he described

> "a body perfectly well insulated in air can be heated by simply connecting it with a source of rapidly alternating high potential"

- cited as: `(1894, p. 394)`
- why: the demonstration he says he already gave, and the whole mechanism in one sentence. Starts after the OCR's glued 'Itmay'; see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...ilizing alternating currents of high tension, I have received many letters from noted physicians inquiring as to the physical effects of such currents of high frequency. Itmay be remembered that I then demonstrated that a body perfectly well insulated in air can be heated by simply connecting it with a source of rapidly alternating high potential. The heating in this case is due in all probability to the bombardment of the body by air, or possibly by some other medium, which is molecular or atomic in construction, and the presence of which has so far escaped our...`

### 2. The mechanism he described

> "The heating in this case is due in all probability to the bombardment of the body by air, or possibly by some other medium, which is molecular or atomic in construction, and the presence of which has so far escaped our analysis"

- cited as: `(1894, p. 394)`
- why: his explanation, with 'in all probability' and 'possibly' left in: it is a hypothesis about a medium, not a settled mechanism
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...cts of such currents of high frequency. Itmay be remembered that I then demonstrated that a body perfectly well insulated in air can be heated by simply connecting it with a source of rapidly alternating high potential. The heating in this case is due in all probability to the bombardment of the body by air, or possibly by some other medium, which is molecular or atomic in construction, and the presence of which has so far escaped our analysis — for according to my ideas, the true ether radiation with such frequencies as even a few millions per second must be very small. This body may be a good conductor or it may be a very poor conductor of electricity with...`

### 2. The mechanism he described

> "This body may be a good conductor or it may be a very poor conductor of electricity with little change in the result"

- cited as: `(1894, p. 394)`
- why: why this is not conduction through the tissue, which is what a modern device implies
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...ular or atomic in construction, and the presence of which has so far escaped our analysis — for according to my ideas, the true ether radiation with such frequencies as even a few millions per second must be very small. This body may be a good conductor or it may be a very poor conductor of electricity with little change in the result. The human body is, in such a case, a fine conductor, and if a person insulated in a room, or no matter where, is brought into contact with such a source of 1. Article by Mr. Tesla in Tlie EUctrical Engineer of Deo. 23d...`

### 2. The mechanism he described

> "The human body is, in such a case, a fine conductor"

- cited as: `(1894, p. 394)`
- why: the brief's line, verbatim, and the sentence the therapy market is built on
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...the true ether radiation with such frequencies as even a few millions per second must be very small. This body may be a good conductor or it may be a very poor conductor of electricity with little change in the result. The human body is, in such a case, a fine conductor, and if a person insulated in a room, or no matter where, is brought into contact with such a source of 1. Article by Mr. Tesla in Tlie EUctrical Engineer of Deo. 23d, 1891.`

### 2. The mechanism he described

> "if a person insulated in a room, or no matter where, is brought into contact with such a source of"

- cited as: `(1894, p. 394)`
- why: first half of the sentence that finishes on printed p. 395. The footnote is interleaved at the page break, so the two halves are pinned apart; see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...few millions per second must be very small. This body may be a good conductor or it may be a very poor conductor of electricity with little change in the result. The human body is, in such a case, a fine conductor, and if a person insulated in a room, or no matter where, is brought into contact with such a source of 1. Article by Mr. Tesla in Tlie EUctrical Engineer of Deo. 23d, 1891.`

### 5. What the internet gets wrong

> "every electrician and electrical engineer is confident that electricity will become the means of accomplishing many things that have been heretofore, with our existing knowledge, deemed impossible"

- cited as: `(1894, p. 394)`
- why: the overheated moment he is writing into, in his own words. His sentence about his audience, not a claim of his own
- check_quotes.py: exact match, ratio 1.0, printed p. 394
- raw OCR: `...ent occasion to witness. My remarks are elicited by the lively interest which prominent medical practitioners evince at every real advance in electrical investigation. The progress in recent years has been so great that every electrician and electrical engineer is confident that electricity will become the means of accomplishing many things that have been heretofore, with our existing knowledge, deemed impossible. ]Sro wonder 'then that progressive physicians also should expect to find in it a powerful tool and help in new curative processes. Since I had the honor to bring before the American Institute of Electrical Engineers so...`

## Printed p. 395 (scan file 413)

### 2. The mechanism he described

> "the skin is heated by bombardment"

- cited as: `(1894, p. 395)`
- why: the end of that same sentence, on the next page. Cite it to p. 395 on its own
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 395 rapidly alternating high potential, the skin is heated by bombardment. Itis a mere question of the dimensions and character of the apparatus to produce any degree of heating desired. It has occurred to me whether, with such apparatus properly prepared, it would not be possible for a skill...`

### 2. The mechanism he described

> "It is a mere question of the dimensions and character of the apparatus to produce any degree of heating desired"

- cited as: `(1894, p. 395)`
- why: the engineering claim, and the only one he makes here: heat is a design problem. The OCR glues 'Itis'; check_quotes.py passes it space-normalised
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 395
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 395 rapidly alternating high potential, the skin is heated by bombardment. Itis a mere question of the dimensions and character of the apparatus to produce any degree of heating desired. It has occurred to me whether, with such apparatus properly prepared, it would not be possible for a skilled physician to find in it a means for the effective treatment of various types of disease. The heating will, of...`

### 3. The North Pole thought experiment

> "It has occurred to me whether, with such apparatus properly prepared, it would not be possible for a skilled physician to find in it a means for the effective treatment of various types of disease"

- cited as: `(1894, p. 395)`
- why: the therapy sentence as he actually writes it: a conditional question, 'it would not be possible', with 'properly prepared' and 'a skilled physician' attached. 'disease' occurs once in the whole volume, here
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...NCY AND HIGH POTENTIAL CURRENTS. 395 rapidly alternating high potential, the skin is heated by bombardment. Itis a mere question of the dimensions and character of the apparatus to produce any degree of heating desired. It has occurred to me whether, with such apparatus properly prepared, it would not be possible for a skilled physician to find in it a means for the effective treatment of various types of disease. The heating will, of course, be superficial, that is, on the skin, and would result, whether the person operated on were in bed or walking around a room, whether dressed in thick clothes or whether reduced to nakedness...`

### 3. The North Pole thought experiment

> "The heating will, of course, be superficial, that is, on the skin, and would result, whether the person operated on were in bed or walking around a room, whether dressed in thick clothes or whether reduced to nakedness"

- cited as: `(1894, p. 395)`
- why: what the device does and does not reach: surface heating through clothing. This is the sentence that makes the North Pole joke
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...e of heating desired. It has occurred to me whether, with such apparatus properly prepared, it would not be possible for a skilled physician to find in it a means for the effective treatment of various types of disease. The heating will, of course, be superficial, that is, on the skin, and would result, whether the person operated on were in bed or walking around a room, whether dressed in thick clothes or whether reduced to nakedness. In fact, to put it broadly, it is conceivable that a person entirely nude at the North Pole might keep himself comfortably warm in this manner. Without vouching for all the results, which must, of course, be determined...`

### 3. The North Pole thought experiment

> "it is conceivable that a person entirely nude at the North Pole might keep himself comfortably warm in this manner"

- cited as: `(1894, p. 395)`
- why: the Appendix A line, and the passage the article is named for. 'it is conceivable' is doing the work; keep it in
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...be superficial, that is, on the skin, and would result, whether the person operated on were in bed or walking around a room, whether dressed in thick clothes or whether reduced to nakedness. In fact, to put it broadly, it is conceivable that a person entirely nude at the North Pole might keep himself comfortably warm in this manner. Without vouching for all the results, which must, of course, be determined by experience and observation, I can at least warrant the fact that heating would occur by the use of this method of subjecting the human body...`

### 4. What he explicitly did not claim

> "Without vouching for all the results, which must, of course, be determined by experience and observation"

- cited as: `(1894, p. 395)`
- why: the hedge the whole article is built on, and the brief's point: Tesla hedged, the market did not
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...d a room, whether dressed in thick clothes or whether reduced to nakedness. In fact, to put it broadly, it is conceivable that a person entirely nude at the North Pole might keep himself comfortably warm in this manner. Without vouching for all the results, which must, of course, be determined by experience and observation, I can at least warrant the fact that heating would occur by the use of this method of subjecting the human body to bombardment by alternating currents of high potential and frequency such as I have long worked with. It...`

### 4. What he explicitly did not claim

> "I can at least warrant the fact that heating would occur by the use of this method of subjecting the human body to bombardment by alternating currents of high potential and frequency such as I have long worked with"

- cited as: `(1894, p. 395)`
- why: exactly what he warrants: heat. Not a cure, not a treatment, heat
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...is conceivable that a person entirely nude at the North Pole might keep himself comfortably warm in this manner. Without vouching for all the results, which must, of course, be determined by experience and observation, I can at least warrant the fact that heating would occur by the use of this method of subjecting the human body to bombardment by alternating currents of high potential and frequency such as I have long worked with. It is only reasonable to expect that some of the novel effects will be wholly different from those obtainable with the old familiar therapeutic methods generally used. Whether they would all be beneficial or not remain...`

### 4. What he explicitly did not claim

> "It is only reasonable to expect that some of the novel effects will be wholly different from those obtainable with the old familiar therapeutic methods generally used"

- cited as: `(1894, p. 395)`
- why: he expects the effects to differ from the electrotherapy of his day, which is the opposite of endorsing it
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...on, I can at least warrant the fact that heating would occur by the use of this method of subjecting the human body to bombardment by alternating currents of high potential and frequency such as I have long worked with. It is only reasonable to expect that some of the novel effects will be wholly different from those obtainable with the old familiar therapeutic methods generally used. Whether they would all be beneficial or not remains to be proved.`

### 4. What he explicitly did not claim

> "Whether they would all be beneficial or not remains to be proved"

- cited as: `(1894, p. 395)`
- why: the last sentence of the paper. If the article quotes one hedge, quote this one
- check_quotes.py: exact match, ratio 1.0, printed p. 395
- raw OCR: `...tial and frequency such as I have long worked with. It is only reasonable to expect that some of the novel effects will be wholly different from those obtainable with the old familiar therapeutic methods generally used. Whether they would all be beneficial or not remains to be proved.`

## Rejected: considered and not carried forward

- ~~"I trust that the present brief communication will not be interpreted as an effort on my part to put myself on record as a 'patent medicine' man"~~ (p. 394): with single quotes around 'patent medicine' this is a near-match only (ratio 0.98) and check_quotes.py fails it: the printed page sets double quotes, and grep_quote.py folds curly doubles to a straight double quote but never to an apostrophe. Keep the print's double quotes, or cut the quote before them
- ~~"if a person insulated in a room, or no matter where, is brought into contact with such a source of rapidly alternating high potential, the skin is heated by bombardment"~~ (p. 394): as one run it returns no hit at all: the footnote '1. Article by Mr. Tesla in Tlie EUctrical Engineer of Deo. 23d, 1891.' sits between 'source of' and 'rapidly' in the OCR of the page break. The two halves are pinned separately, each to its own page
- ~~"The output of such an apparatus is very small, but some of the effects peculiar to alternating currents of short periods may be observed"~~ (p. 393): the OCR reads 'may l>e observed' (the b came out as '>'), ratio 0.99, a FAIL. Pin the first clause only
- ~~"No wonder then that progressive physicians"~~ (p. 394): the OCR line reads ']Sro wonder 'then'; no match at all. Start the quote at 'progressive physicians'
- ~~"Article by Mr. Tesla in The Electrical Engineer of Dec. 23d, 1891"~~ (p. 394): this is the massage paper's own footnote, and this scan garbles it ('Tlie EUctrical Engineer of Deo. 23d, 1891', ratio 0.931). Do not put it inside quotation marks. State the provenance in our own words and cite p. 394, footnote 1. By contrast the chapter XXX footnote verifies exactly as typed: 'Article by Mr. Tesla in The Electrical Engineer, N. Y., May 6, 1891.' (p. 392)
- ~~""Massage" with currents of high frequency"~~ (p. 394): the chapter heading is not in the search index at all: grep_quote.py's strip_furniture() drops display lines, so the only 'massage' in the searchable volume is the book's own index entries on printed pp. 494-495. The heading is genuinely on the printed page (view books/pdf-pages-tesla-1894/page-412.pdf), but check_quotes.py cannot verify it. Refer to the chapter heading in our own framing; do not print it as a quote
- ~~"violet ray / electric bath / electrotherapy / diathermy"~~ (not in this volume): 0 exact hits for each in the whole volume ('violet' alone occurs twice, printed pp. 163 and 218, about the colour of a discharge, never as 'violet ray'). The modern market vocabulary is not in this book: any sentence about violet rays, electric baths or diathermy needs a modern source (§4.1), not a page cite
- ~~"There is no breaking through, no local injury, but all the material, insulating and conducting, is uniformly heated"~~ (p. 162): verifies exactly, but 'the material' is the coil, not the body: the sentence explains that the coil absorbs the energy. A false friend for the heating claim
- ~~"the curious paradox exists, that, while with a given current through the primary the shock might be fatal, with many times that current it might be perfectly harmless"~~ (p. 162): verifies, but it is about a high tension induction coil's impedance, and it is the sentence a wellness page would most easily misuse. If it is used at all it needs the surrounding explanation; prefer the 'altogether harmless' sentence
- ~~"can be supported without any inconvenience, except perhaps a small burn"~~ (p. 125): Appendix A registers it and it verifies, but printed p. 125 is chapter XXV, the editor's recap of coil shocks in the third person, not Tesla's therapy paper. Not this article's material
- ~~"for according to my ideas, the true ether radiation with such frequencies as even a few millions per second must be very small"~~ (p. 394): verifies exactly, but it is his 1894 ether hypothesis. Printing it starts a physics argument this article does not need; if it is used, say plainly that it is his speculation about the medium
- ~~"It may be remembered that I then demonstrated"~~ (p. 394): the OCR glues 'Itmay', so the clean form matches only with spaces ignored. Not worth carrying: start the quote at 'a body perfectly well insulated in air'
- ~~"Physiological Effects"~~ (p. 495): the book's own index entry 'Physiological Effects... 162, 394' (printed p. 495) is why this article may put the p. 162 caution beside pp. 394-395 and still call it one subject. Index text is not prose: cite the index, do not quote it

## Flags for the writer (§3 quote policy, feature-005/t1)

- THREE TEXTS, THREE DATES, ONE ARTICLE. Printed pp. 394-395 are chapter XXXI, ' MASSAGE WITH CURRENTS OF HIGH FREQUENCY', Tesla's own first-person paper; its footnote dates it to The Electrical Engineer, Dec 23 1891 (that footnote is garbled in this scan; see rejected). The chapter is exactly two pages: it opens on printed p. 394 and its last sentence ends on printed p. 395, where chapter XXXII begins. Printed p. 393 is chapter XXX, 'ALTERNATE CURRENT ELECTROSTATIC INDUCTION APPARATUS', a different paper, The Electrical Engineer, May 6 1891 (that footnote does verify, p. 392). Printed p. 162 is chapter XXVI, the lecture delivered at Columbia College, New York, May 20 1891. Never write 'Tesla wrote in 1894': 1894 is the book, not the writing.
- WHY p. 162 BELONGS IN THIS ARTICLE. The volume's own index (printed p. 495) files the subject as 'Physiological Effects... 162, 394' - the book itself puts the 1891 lecture's physiological caution and the massage paper on one line. That is the justification for quoting p. 162 here. Say which page and which lecture the sentence comes from.
- THE HUB SAYS 1892 AND IS WRONG. new_content/1894-series/00-hub/article.md line 96 cards this article as 'the "patent medicine" complaint, 1892'. The book's footnote says Dec 23 1891 and §9 brief 05 says Dec 23 1891. Do not repeat 1892 in this article; record the contradiction in index.json for feature-012, which renders the hub.
- NESTED QUOTE MARKS. The print sets "patent medicine" in double quotes. If the draft prints the full sentence with them, check_quotes.py's scanner splits the run at the inner marks and checks the two halves separately; both halves verify, but each needs a '(1894, p. 394)' within 400 characters of its end. So put the citation immediately after the closing quote mark and put no other sentence in between. Do not switch to single quotes (rejected #1). If that is too fragile, print only the second half, which is pinned on its own.
- THE SCARE QUOTES IN THE TITLE ARE THE BOOK'S. The chapter is headed MASSAGE with currents of high frequency, with the word MASSAGE itself inside the printer's quote marks. The §9 title's scare quotes follow the printed page; 'Massage' in the title is quotation, not irony on our part. The heading itself cannot be quoted (rejected #6).
- NO CROSS-PAGE CITATION. The sentence running from printed p. 394 to p. 395 is pinned as two quotes, one per page, and each must be cited to its own page. '(1894, pp. 394-395)' does not satisfy check_quotes.py: its citation regex is '\(1894, p{1,2}s?\. ([\d,\s]+?)\)', which cannot match a hyphenated range. Article 04's pin could name a range only because its fragment straddled the break as one fragment; nothing here does.
- OCR SPACING, NOT WORDING. p. 395 'It is a mere question of the dimensions...' is glued in the scan as 'Itis'; p. 394 'a body perfectly well insulated...' follows a glued 'Itmay'. check_quotes.py passes the first as a space-normalised match and the second is pinned after the artefact. Print the clean form; no [sic], no bracketed correction.
- WHAT THE PAPER NEVER SAYS. 'cure' does not occur in this volume (0 exact hits; 'cured' occurs once, printed p. 69, about something else), 'disease' occurs once (printed p. 395, in the hypothetical sentence pinned above), and the paper names no condition it treats and reports no therapeutic result. The §9 title's word 'Cure' is ours and must stay outside quotation marks. The article's case - the market sold what the paper refused to vouch for - is carried by the pin without one invented claim.
- SAFETY (§4.1). The two p. 162 sentences are the only in-book basis for a caution, and they are about currents from a coil or a machine, not about a handheld device a reader might buy. Use them for 'do not try this with mains-derived high voltage', not for any medical claim, and never imply the reader should repeat the experiment.
- MODERN CLAIMS NEED MODERN SOURCES. Short-wave diathermy, the violet-ray market and 1890s electrotherapy are all outside this volume (rejected #7). If the draft keeps brief 05's section 5 descendant paragraph, it needs a cited modern source in the Sources block, kept visibly separate from the 1894 material, or the paragraph is cut.
- VOICE RULE (§0.5, enforced by qa_page.py). No em or en dashes, no curly quotes, no Unicode ellipsis in the article body. Every cut in this pin is ASCII ' ... ' for that reason; keep it that way in the draft.

## Notes for the figure task (feature-005/t2)

- chapter XXXI (printed pp. 394-395) carries no illustration at all: the extractor cut no figure from scan files 412-413 and website/assets/tesla1894/manifest_qc.csv has no row for them. That is why §6.3 requires a patent drawing for this page, and why the feature criteria say the chapter has no book illustration.
- the two crops Appendix C lists for 05 are from the adjacent chapter XXX, not from this chapter: website/assets/tesla1894/p410-fig1-fig208.webp is scan file 410 = printed p. 392, and p411-fig1-fig208.webp is scan file 411 = printed p. 393. §6.6 rule 2 allows neighbouring-chapter art for exactly this article ('Ch. XXX ... Figs. 208-09 for the massage article'), but the second filename's number is wrong: the p. 393 plate is the one the p. 393 text calls Fig. 209 ('Another form of apparatus is illustrated in Fig. 209'), and its printed caption came out of the OCR as 'FIG. 20«J'. manifest_qc.csv already records it: 'p.393 tagged Fig.208 (that is the p.392 ring) - number wrong, image clean'.
- manifest_qc.csv describes the p. 392 crop as 'Circular phase diagram: a ring with six marked points and radial/diagonal connecting lines', which is not how the p. 392 text describes Fig. 208 (a hard-wood ring with two sets of tin-foil coatings, and a charged cylinder rotating inside it, mica-lined). View the crop against books/pdf-pages-tesla-1894/page-410.pdf before using it, and caption from the prose on the page, never from the OCR caption or the QC subject line.
- the page-scan crop of printed p. 394 that brief 05 asks for is §6.6 rule 4 (the words are the artefact). Source page: books/pdf-pages-tesla-1894/page-412.pdf (scan file 412 = printed p. 394). Article 03 did the same for p. 486; follow its crop handling and credit line.
- the patent plate (§6.3, 'a 1890s-1900s high-frequency electrode patent') has no number fixed yet. Never ship an unverified number: confirm it on patents.google.com and credit it 'US patent NNN,NNN (year), Nikola Tesla.' (§4.2). Keep the §6.3 ratio: at most one patent plate per two 1894 engravings.
- never reuse an engraving another article already carries (§6.6). Check index.json figures[] before picking.

## Links (§5.2, for feature-005/t1 and t4)

- out-links per §5.2 row 05 and §9 brief 05: magnetic-generator-scam.html, How-Much-Noise-Does-a-Free-Energy-Device-Make.html, and 10 (tesla-free-energy-what-he-said.html). Both existing targets are present in website/ as of 2026-10-11. 10 is feature-007 and does not exist yet, so 05 -> 10 cannot be added in t4; record it in index.json the way article 04's pin records its own deferred link, and add it when 10 is written.
- in-links required by §5.2 row 05: from 10 and from the hub. Neither exists yet (feature-007, feature-012). The qa_page.py reciprocal gate ('>= 3 out-links to pages that link back') therefore cannot pass on 05 for any reason to do with 05: nothing in the site links to it. Record that in index.json the way article 11's entry records its backlink pass; do not pad 05 with off-map links to make the number.
- the bridge paragraph (brief 05 section 6) is where magnetic-generator-scam.html belongs: the article's method is 'check what the source actually outputs and what the seller vouches for', which is the same test that page applies to the generator. Link it as our take on overclaiming; do not repeat its product claims (§4.1).
- the hub card for 05 must be corrected to Dec 23 1891 when feature-012 renders it (see flags).
