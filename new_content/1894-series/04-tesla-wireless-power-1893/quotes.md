# Article 04 quote pin: tesla-wireless-power-1893.html

SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped on 2026-10-11 from `books/extracted/tesla-1894-plain.txt` through the same matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR spacing is ignored) and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). A quote carrying an ellipsis is cut where the scan is corrupt; each side of the cut is verified separately, which is how check_quotes.py will judge the draft. `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. Three different texts are quoted, and they are not the same voice:

- chapter XXV, 'INTRODUCTION. — THE SCOPE OF THE TESLA LECTURES.' (printed pp. 119-144) — the editor's recap, third person. Printed pp. 137-138, 143.
- chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY AND THEIR APPLICATION TO METHODS OF ARTIFICIAL ILLUMINATION', Columbia College, New York, May 20 1891 (printed pp. 145-197). Tesla's own text. Printed pp. 151, 196-197.
- chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', delivered before the Franklin Institute, Philadelphia, February 1893, and before the National Electric Light Association, St. Louis, March 1893 (footnote 1, printed p. 294; printed pp. 294-373). Tesla's own text. Printed pp. 346-349 — this is the 1893 material the title promises.

Verified: 40 quotes (43 fragments) across 9 printed pages, 0 failures. To re-check one quote: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>`. To regenerate this file: `python3 new_content/1894-series/04-tesla-wireless-power-1893/gen_quotes.py` (it exits non-zero and writes nothing if any quote fails).

## Printed p. 138 (scan file 156)

### 1. The paragraph nobody quotes

> "Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly"

- cited as: `(1894, p. 138)`
- why: brief 04 asks for this paragraph in full; it verifies as one continuous run, so 'in full' is safe. It is the editor's review of the 1891 lecture, not Tesla speaking: see the first flag
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment, the disc is set in rotation. Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly. In the course of this experimental study special attention was devoted to the heating effects produced by these currents, which are not only striking, but open up the possibility of producing a more efficient illumiuan...`

### 1. The paragraph nobody quotes

> "Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth"

- cited as: `(1894, p. 138)`
- why: the sentence the myth is built on, with the words 'seem to bring it within possibility' left in
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment, the disc is set in rotation. Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free en...`

### 1. The paragraph nobody quotes

> "If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size"

- cited as: `(1894, p. 138)`
- why: the transmitting apparatus as the book describes it: a grounded wire and a body of some size
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...is set in rotation. Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through the earth. If, by means of powerful machinery, rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner,...`

### 1. The paragraph nobody quotes

> "The current might be converted to low tension and used to operate a motor or other device"

- cited as: `(1894, p. 138)`
- why: the half people leave out: he would transform it back to low tension. Article 02's quotes.md defers this exact sentence to this article
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...rapid variations of the earth's potential were produced, a grounded wire reaching up to some height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite...`

### 1. The paragraph nobody quotes

> "The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea"

- cited as: `(1894, p. 138)`
- why: the ship-at-sea line. Not the p. 168 lightning passage of the same name; see rejected
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...e height would be traversed by a current which could be increased by connecting the free end of the wire to a body of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly. In the course of this experimental study special attention was devoted to the heating effects produc...`

### 1. The paragraph nobody quotes

> "In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly"

- cited as: `(1894, p. 138)`
- why: where he retreats: signals, not power, is the certain part
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...ody of some size. The current might be converted to low tension and used to operate a motor or other device. The experiment, which would be one of great scientific interest, would probably best succeed on a ship at sea. In this manner, even if it were not possible to operate machinery, intelligence might be transmitted quite certainly. In the course of this experimental study special attention was devoted to the heating effects produced by these currents, which are not only striking, but open up the possibility of producing a more efficient illumiuan...`

### 2. The apparatus behind the claim

> "An experiment of special interest shown by Mr. Tesla, is the running, by the use of only one insulated line, of a motor operating on the principle of the rotating magnetic field"

- cited as: `(1894, p. 138)`
- why: the demonstration the claim rests on. The printed sentence continues 'enunciated by Mr. Tesla'; cut before that and the quote still verifies
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `138 INVENTIONS OF NIKOLA TESLA. An experiment of special interest shown by Mr. Tesla, is the running, by the use of only one insulated line, of a motor operating on the principle of the rotating magnetic field enunciated by Mr. Tesla. A simple form of such a motor is obtained by winding upon a laminated iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc...`

### 2. The apparatus behind the claim

> "A simple form of such a motor is obtained by winding upon a laminated iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc within the influence of the moving field"

- cited as: `(1894, p. 138)`
- why: what was actually on the table: iron core, two coils, a copper disc
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...OF NIKOLA TESLA. An experiment of special interest shown by Mr. Tesla, is the running, by the use of only one insulated line, of a motor operating on the principle of the rotating magnetic field enunciated by Mr. Tesla. A simple form of such a motor is obtained by winding upon a laminated iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc within the influence of the moving field. The secondary coil may, however, be omitted. When one of the ends of the primary coil of the motor is connected to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which,...`

### 2. The apparatus behind the claim

> "The secondary coil may, however, be omitted"

- cited as: `(1894, p. 138)`
- why: one line, and it is why the demo is a single-coil machine
- check_quotes.py: exact match, ratio 1.0, printed p. 138
- raw OCR: `...such a motor is obtained by winding upon a laminated iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc within the influence of the moving field. The secondary coil may, however, be omitted. When one of the ends of the primary coil of the motor is connected to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necess...`

### 2. The apparatus behind the claim

> "one of the ends of the primary coil of the motor is connected to one of the terminals of the high frequency coil ... the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment"

- cited as: `(1894, p. 138)`
- why: the connection as drawn, plus his own note that the plate is optional. Cut at the scan's 'arid' misprint; see flags
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 138; frag 2: exact match, ratio 1.0, printed p. 138
- raw OCR (frag 1: one of the ends of the primary coil of t): `...ed iron core a primary and close to it a secondary coil, closing the ends of the latter and placing a freely movable metal disc within the influence of the moving field. The secondary coil may, however, be omitted. When one of the ends of the primary coil of the motor is connected to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment, the disc is set in rotation. Experiments of this kind seem to bring it within po...`
- raw OCR (frag 2: the other end to an insulated metal plat): `...etal disc within the influence of the moving field. The secondary coil may, however, be omitted. When one of the ends of the primary coil of the motor is connected to one of the terminals of the high frequency coil arid the other end to an insulated metal plate, which, it should be stated, is not absolutely necessary for the success of the experiment, the disc is set in rotation. Experiments of this kind seem to bring it within possibility to operate a motor at any point of the earth's surface from a central source, without any connection to the same except through...`

## Printed p. 143 (scan file 161)

### 2. The apparatus behind the claim

> "without any return circuit"

- cited as: `(1894, p. 143)`
- why: the bridge to article 02: the point of the one-wire demos, in the book's own summary. Stop the quote at 'circuit'; the words before it carry an OCR misprint
- check_quotes.py: exact match, ratio 1.0, printed p. 143 (the same words also occur on printed pp. 328; cite the pinned p. 143)
- raw OCR: `...in a number of experiments a variety of effects by the employment of only a single wire with the evident intent of impressing upon his audience the idea that electric vibration or current can be transmitted witli ease, without any return circuit ; also how currents so transmitted can be converted and used for many practical purposes. A number of experiments are then shown, illustrating the effects of frequency, self-induction and capacity; then a number of ways...`

### 5. What the internet gets wrong

> "He expressed his firm conviction that by observing proper conditions, intelligence, and possibly even power, can be transmitted through the medium or through the earth; and he considers this problem worthy of serious and immediate consideration"

- cited as: `(1894, p. 143)`
- why: the editor's summary of the same lecture: 'by observing proper conditions'. Third person, so it cannot be introduced as Tesla's words
- check_quotes.py: exact match, ratio 1.0, printed p. 143
- raw OCR: `...novel impedance phenomena are also shown which cannot fail to arouse interest. Mr. Tesla next dwelt upon a subject which he thinks of great importance, that is, electrical resonance, which he explained in a popular way. He expressed his firm conviction that by observing proper conditions, intelligence, and possibly even power, can be transmitted through the medium or through the earth; and he considers this problem worthy of serious and immediate consideration. Coming now to the light phenomena in particular, lie illustrated the four distinct kinds of these phenomena in an original way, which to many must have been a revelation. Mr. Tesla attributes these light effects to mol...`

## Printed p. 151 (scan file 169)

### 3. His transmission arithmetic

> "there is no particular difficulty encountered in conveying currents from a machine giving ... say, 20,000 alternations per second, to quite a distance. This number of alternations, however, is by far too small for many purposes, though quite sufficient for some practical applications"

- cited as: `(1894, p. 151)`
- why: the brief's number, in full and with his own caveat attached. Cut at the scan's stray caret; see flags
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 151; frag 2: exact match, ratio 1.0, printed p. 151
- raw OCR (frag 1: there is no particular difficulty encoun): `..., for instance, the dielectric losses being no doubt greater in the former. The difficulty of insulating, of course, only exists when the potentials are excessively high, for with potentials such as a few thousand volts there is no particular difficulty encountered in conveying currents from a machine giving^ say, 20,000 alternations per second, to quite a distance. This number of alternations, however, is by far too small for many purposes, though quite sufficient for some practical applications. This difficulty of insulat...`
- raw OCR (frag 2: say, 20,000 alternations per second, to ): `...of insulating, of course, only exists when the potentials are excessively high, for with potentials such as a few thousand volts there is no particular difficulty encountered in conveying currents from a machine giving^ say, 20,000 alternations per second, to quite a distance. This number of alternations, however, is by far too small for many purposes, though quite sufficient for some practical applications. This difficulty of insulating is fortunately not a vital drawback ;`

### 6. Why it did not happen

> "it will be found difficult to provide the requisite insulation without considerably increasing the size of the apparatus, for the potentials required are high, and, owing to the rapidity of the alternations, the insulation presents peculiar difficulties"

- cited as: `(1894, p. 151)`
- why: the insulation wall, in his own words, from the 1891 lecture
- check_quotes.py: exact match, ratio 1.0, printed p. 151
- raw OCR: `...derful results. First will be met the difficulty of obtaining the required frequencies bymeans of mechanical apparatus, and, if they be ob. tained otherwise, obstacles of a different nature will present themselves. Next it will be found difficult to provide the requisite insulation without considerably increasing the size of the apparatus, for the potentials required are high, and, owing to the rapidity of the alternations, the insulation presents peculiar difficulties. So, for instance, when a gas is present, the discharge may work, by the molecular bombardment of the gas and consequent heating, through as much as an inch of the best solid insulating material, such as glass, hard rub...`

### 6. Why it did not happen

> "The chief requisite in the insulation of the apparatus is, therefore, the exclusion of any gaseous matter"

- cited as: `(1894, p. 151)`
- why: the engineering consequence: the machine has to be sealed, which is a cost
- check_quotes.py: exact match, ratio 1.0, printed p. 151
- raw OCR: `...ombardment of the gas and consequent heating, through as much as an inch of the best solid insulating material, such as glass, hard rubber, porcelain, sealing wax, etc. ; in fact, through any known insulating substance. The chief requisite in the insulation of the apparatus is, therefore, the exclusion of any gaseous matter. In general my experience tends to show that bodies which possess the highest specific inductive capacity, such as glass, afford a rather inferior insulation to others, which, while they are good insulators, have a much...`

## Printed p. 196 (scan file 214)

### 4. The ambition, in his own rhetoric

> "But there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium"

- cited as: `(1894, p. 196)`
- why: the actual proposition: not free energy, obtaining power 'in some more direct way'
- check_quotes.py: exact match, ratio 1.0, printed p. 196
- raw OCR: `...r, it will not be possible to obtain the higher light vibrations without going through the lower heat vibrations. It is the problem of imparting to a body a certain velocity without passing through all lower velocities. But there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium. The time will be when this will be accomplished, and the time has come when one may utter such words before an enlightened audience without being considered a visionary. AVe are whirling through`

### 4. The ambition, in his own rhetoric

> "the time has come when one may utter such words before an enlightened audience without being considered a visionary"

- cited as: `(1894, p. 196)`
- why: the brief's line, and he is defending the right to say it, not claiming it is done
- check_quotes.py: exact match, ratio 1.0, printed p. 196
- raw OCR: `...But there is a possibility of obtaining energy not only in the form of light, but motive power, and energy of any other form, in some more direct way from the medium. The time will be when this will be accomplished, and the time has come when one may utter such words before an enlightened audience without being considered a visionary. AVe are whirling through`

### 5. What the internet gets wrong

> "How far the results here borne out are capable of practical applications will be decided in the future"

- cited as: `(1894, p. 196)`
- why: he dates the verdict, not himself; from the 1891 lecture
- check_quotes.py: exact match, ratio 1.0, printed p. 196
- raw OCR: `...t length, and among many observations I have selected only those which I thought most likely to interest you. The field is wide and completely unexplored, and at every step a new truth is gleaned, a novel fact observed. How far the results here borne out are capable of practical applications will be decided in the future. As regards the production of light, some results already reached are encouraging and make me confident in asserting that the practical solution of the problem lies in the direction I have endeavored to indicate. Still,...`

## Printed p. 197 (scan file 215)

### 4. The ambition, in his own rhetoric

> "are whirling through endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy"

- cited as: `(1894, pp. 196-197)`
- why: the rhetoric the brief asks for. The pinned fragment starts after 'We'; the scan prints 'AVe'. See flags
- check_quotes.py: exact match, ratio 1.0, printed p. 197 (the printed sentence runs across pp. 196-197; cite 'pp. 196-197', either page alone also satisfies the citation check)
- raw OCR: `moil FREQUENCY AND HIGH POTENTIAL CURRENTS. 197 endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy. There must be some way of availing ourselves of this energy more directly. Then, with the light obtained from the me...`

### 4. The ambition, in his own rhetoric

> "There must be some way of availing ourselves of this energy more directly"

- cited as: `(1894, p. 197)`
- why: the sentence that follows, which asks for a method rather than claiming one
- check_quotes.py: exact match, ratio 1.0, printed p. 197
- raw OCR: `moil FREQUENCY AND HIGH POTENTIAL CURRENTS. 197 endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy. There must be some way of availing ourselves of this energy more directly. Then, with the light obtained from the medium, with the power derived from it, with every form of energy obtained without effort, from the store forever inexhaustible, humanity will advance with giant strides. The mere...`

## Printed p. 346 (scan file 364)

### 5. What the internet gets wrong

> "I mean the transmission of intelligible signals or perhaps even power to any distance without the use of wires"

- cited as: `(1894, p. 346)`
- why: his own statement of the plan, with 'perhaps even' doing the work
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...e effects and the problem of transmission of energy over a single conductor which was previously considered, I would say a few words on a subject which constantly fills my thoughts and which concerns the welfare of all. I mean the transmission of intelligible signals or perhaps even power to any distance without the use of wires. I am becoming daily more convinced of the practicability of the scheme ; and though I know full well that the great majority of scientific men will not believe that such results can be practically and immediately reali...`

### 5. What the internet gets wrong

> "I am becoming daily more convinced of the practicability of the scheme"

- cited as: `(1894, p. 346)`
- why: conviction of practicability, not a working system
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...ould say a few words on a subject which constantly fills my thoughts and which concerns the welfare of all. I mean the transmission of intelligible signals or perhaps even power to any distance without the use of wires. I am becoming daily more convinced of the practicability of the scheme ; and though I know full well that the great majority of scientific men will not believe that such results can be practically and immediately realized, yet I think that all consider the developments in recent years by a...`

### 5. What the internet gets wrong

> "though I know full well that the great majority of scientific men will not believe that such results can be practically and immediately realized"

- cited as: `(1894, p. 346)`
- why: he names the scepticism himself, in the same sentence as his claim
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...h concerns the welfare of all. I mean the transmission of intelligible signals or perhaps even power to any distance without the use of wires. I am becoming daily more convinced of the practicability of the scheme ; and though I know full well that the great majority of scientific men will not believe that such results can be practically and immediately realized, yet I think that all consider the developments in recent years by a number of workers to have been such as to encourage thought and experiment in this direction. My conviction has grown so strong, that I no longer look...`

### 5. What the internet gets wrong

> "I no longer look upon this plan of energy or intelligence transmission as a mere theoretical possibility, but as a serious problem in electrical engineering, which must be carried out some day"

- cited as: `(1894, p. 346)`
- why: the honest form of the ambition: an unsolved engineering problem
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...diately realized, yet I think that all consider the developments in recent years by a number of workers to have been such as to encourage thought and experiment in this direction. My conviction has grown so strong, that I no longer look upon this plan of energy or intelligence transmission as a mere theoretical possibility, but as a serious problem in electrical engineering, which must be carried out some day. The idea of transmitting intelligence without wires is the natural outcome of the most recent results of electrical investigations. Some enthusiasts have expressed their belief that telephony to any distance by inducti...`

### 5. What the internet gets wrong

> "Some enthusiasts have expressed their belief that telephony to any distance by induction through the air is possible"

- cited as: `(1894, p. 346)`
- why: the claim he refuses to make: he attributes it to 'some enthusiasts'
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...but as a serious problem in electrical engineering, which must be carried out some day. The idea of transmitting intelligence without wires is the natural outcome of the most recent results of electrical investigations. Some enthusiasts have expressed their belief that telephony to any distance by induction through the air is possible. I cannot stretch my imagination so far, but I do firmly believe that it is practicable to disturb by means of powerful machines the electrostatic condition of the earth and thus transmit intelligible signals and perhap...`

### 5. What the internet gets wrong

> "I cannot stretch my imagination so far, but I do firmly believe that it is practicable to disturb by means of powerful machines the electrostatic condition of the earth and thus transmit intelligible signals and perhaps power"

- cited as: `(1894, p. 346)`
- why: what he does claim, hedged twice: 'signals and perhaps power'
- check_quotes.py: exact match, ratio 1.0, printed p. 346
- raw OCR: `...ligence without wires is the natural outcome of the most recent results of electrical investigations. Some enthusiasts have expressed their belief that telephony to any distance by induction through the air is possible. I cannot stretch my imagination so far, but I do firmly believe that it is practicable to disturb by means of powerful machines the electrostatic condition of the earth and thus transmit intelligible signals and perhaps power. In fact, what is there against the carrying out of such a scheme ? We now know that electric vibration may be transmitted through a single conductor. Why then not try to avail ourselves of the earth for this purpose ?...`

### 6. Why it did not happen

> "We now know that electric vibration may be transmitted through a single conductor. Why then not try to avail ourselves of the earth for this purpose?"

- cited as: `(1894, p. 346)`
- why: the step from article 02's one-wire work to the earth. The scan's spacing differs; see flags
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 346
- raw OCR: `...practicable to disturb by means of powerful machines the electrostatic condition of the earth and thus transmit intelligible signals and perhaps power. In fact, what is there against the carrying out of such a scheme ? We now know that electric vibration may be transmitted through a single conductor. Why then not try to avail ourselves of the earth for this purpose ? We need not be frightened by the idea of distance. To the weary wanderer counting the mile-posts the earth may appear very large, but to that happiest of all men, the astronomer, who gazes at the heavens and b...`

### 6. Why it did not happen

> "A point of great importance would be first to know what is the capacity of the earth?"

- cited as: `(1894, p. 346)`
- why: the first unknown, and he does not know it. The scan sets a space before the mark; see flags
- check_quotes.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 346
- raw OCR: `...it appears very small. And so I think it must seem to the electrician, for when he considers the speed with which an electric disturbance is propagated through the earth all his ideas of distance must completely vanish. A point of great importance would be first to know what is the capacity of the earth ? and what charge does it contain if electrified ? Though we have no positive evidence of a charged body existing in space without other oppositely electrified bodies beingnear, there is a fair probability that th...`

## Printed p. 347 (scan file 365)

### 2. The apparatus behind the claim

> "One of the terminals of the source would be connected to earth as, for instance, to the city water mains ... the other to an insulated body of large surface"

- cited as: `(1894, p. 347)`
- why: the 1893 experiment as he specified it: one terminal to the water mains, one to a large insulated body. Cut at the scan's footnote marker; see flags
- check_quotes.py: 2 fragments, each verified separately (check_quotes.py splits on '...'); frag 1: exact match, ratio 1.0, printed p. 347; frag 2: exact match, ratio 1.0, printed p. 347
- raw OCR (frag 1: One of the terminals of the source would): `...wn circuit, we shall know a fact possibly of the greatest importance to the welfare of the human race. I propose to seek for the period by means of an electrical oscillator, or a source of alternating electric currents. One of the terminals of the source would be connected to earth as, for instance, to the city water mains* the other to an insulated body of large surface. It is possible that the outer conducting air strata, or free space, contain an opposite charge and that, together with the earth, they form a condenser of very large cap...`
- raw OCR (frag 2: the other to an insulated body of large ): `...ropose to seek for the period by means of an electrical oscillator, or a source of alternating electric currents. One of the terminals of the source would be connected to earth as, for instance, to the city water mains* the other to an insulated body of large surface. It is possible that the outer conducting air strata, or free space, contain an opposite charge and that, together with the earth, they form a condenser of very large capacity. In such case the period of vibration may b...`

### 2. The apparatus behind the claim

> "By varying the frequency of the currents and carefully observing the potential of the insulated body and watching for the disturbance at various neighboring points of the earth's surface resonance might be detected"

- cited as: `(1894, p. 347)`
- why: the method: hunt for resonance, and the whole plan turns on finding it
- check_quotes.py: exact match, ratio 1.0, printed p. 347
- raw OCR: `...erve for the purpose of the experiment. I would then transform the current to a potential as high as it would be found possible and connect the ends of the high tension secondary to the ground and to the insulated body. By varying the frequency of the currents and carefully observing the potential of the insulated body and watching for the disturbance at various neighboring points of the earth's surface resonance might be detected. Should, as the majority of scientific men in all probability believe, the period be extremely small, then a dynamo machine would not do and a proper electrical oscillator would have to be produced and perhaps it might...`

### 6. Why it did not happen

> "If ever we can ascertain at what period the earth's charge, when disturbed, oscillates with respect to an oppositely electrified system or known circuit, we shall know a fact possibly of the greatest importance to the welfare of the human race"

- cited as: `(1894, p. 347)`
- why: the measurement the whole scheme depends on, which he had not made
- check_quotes.py: exact match, ratio 1.0, printed p. 347
- raw OCR: `...et an idea of what quantity of electricity the earth contains. It is difficult to say whether we shall ever acquire this necessary knowledge, but there is hope that we may, and that is, by means of electrical resonance. If ever we can ascertain at what period the earth's charge, when disturbed, oscillates with respect to an oppositely electrified system or known circuit, we shall know a fact possibly of the greatest importance to the welfare of the human race. I propose to seek for the period by means of an electrical oscillator, or a source of alternating electric currents. One of the terminals of the source would be connected to earth as, for instance, to the city water ma...`

### 6. Why it did not happen

> "Should, as the majority of scientific men in all probability believe, the period be extremely small, then a dynamo machine would not do and a proper electrical oscillator would have to be produced and perhaps it might not be possible to obtain such rapid vibrations"

- cited as: `(1894, p. 347)`
- why: the condition that ends the plan, and he states it as the likely answer
- check_quotes.py: exact match, ratio 1.0, printed p. 347
- raw OCR: `...dy. By varying the frequency of the currents and carefully observing the potential of the insulated body and watching for the disturbance at various neighboring points of the earth's surface resonance might be detected. Should, as the majority of scientific men in all probability believe, the period be extremely small, then a dynamo machine would not do and a proper electrical oscillator would have to be produced and perhaps it might not be possible to obtain such rapid vibrations. But whether this be possible or not, and whether the earth contains a charge or not, and whatever may be its period of vibration, it certainly is possible — for of this we have daily evidence — to produce some electric...`

## Printed p. 348 (scan file 366)

### 6. Why it did not happen

> "But the disturbance will diminish with the distance, and the distance at which the effect will still be perceptible will depend on the quantity of electricity set in motion"

- cited as: `(1894, p. 348)`
- why: the loss problem stated plainly
- check_quotes.py: exact match, ratio 1.0, printed p. 348
- raw OCR: `...currents will pass through the earth, converging to,or diverging from, the point c where the ground connection is made. In this manner neighboring points on the earth's surface within a certain radius will be disturbed. But the disturbance will diminish with the distance, and the distance at which the effect will still be perceptible will depend on the quantity of electricity set in motion. Since the body p is insulated, in order to displace a considerable quantity, the potential of the source must be excessive, since there would be limitations as to the surface of p. The conditions might be adjusted so t...`

### 6. Why it did not happen

> "Since the body p is insulated, in order to displace a considerable quantity, the potential of the source must be excessive"

- cited as: `(1894, p. 348)`
- why: and the price of beating it: an excessive potential, which is the p. 151 insulation problem come back
- check_quotes.py: exact match, ratio 1.0, printed p. 348
- raw OCR: `...ce within a certain radius will be disturbed. But the disturbance will diminish with the distance, and the distance at which the effect will still be perceptible will depend on the quantity of electricity set in motion. Since the body p is insulated, in order to displace a considerable quantity, the potential of the source must be excessive, since there would be limitations as to the surface of p. The conditions might be adjusted so that the generator or source s will set up the same electrical movement as though its circuit were closed. Thus it is certain...`

### 6. Why it did not happen

> "Theoretically, then, it could not require a great amount of energy to produce a disturbance perceptible at great distance, or even all over the surface of the globe"

- cited as: `(1894, p. 348)`
- why: the theory in his favour, which he marks as theory
- check_quotes.py: exact match, ratio 1.0, printed p. 348
- raw OCR: `...emely small considering the size of the earth, the air would not act as a very disturbing factor, and there would be not much energy lost through the action of the air, which would be the case if the density were great. Theoretically, then, it could not require a great amount of energy to produce a disturbance perceptible at great distance, or even all over the surface of the globe. . tq Now, it is quite certain that at any point within a certain radius of the source s a properly adjusted self-induction and capacity device can be set in action by resonance. But not only can this be done, but anoth...`

### 6. Why it did not happen

> "at what distance such a vibration might be made perceptible can only be conjectured"

- cited as: `(1894, p. 348)`
- why: the honest limit of what he could calculate in 1893
- check_quotes.py: exact match, ratio 1.0, printed p. 348
- raw OCR: `...up the same electrical movement as though its circuit were closed. Thus it is certainly $2 practicable to impress an electric vibration at least g of a certain low period upon the earth by means of proper machinery. At what distance such a vibration might be made perceptible can only be conjectured. Ihave on another occasion considered the question how the earth might behave to electric disturbances. There is no doubt that, since in such an experiment the...`

## Printed p. 349 (scan file 367)

### 4. The ambition, in his own rhetoric

> "I am firmly convinced that it can be done and hope that we shall live to see it done"

- cited as: `(1894, p. 349)`
- why: the close of the 1893 earth section. Print it only after the conditions from pp. 347-348, or it becomes the prophecy this article exists to correct
- check_quotes.py: exact match, ratio 1.0, printed p. 349
- raw OCR: `...h or environing medium. If this is at all possible, distance does not mean anything. Proper apparatus must first be produced by means of which the problem can be attacked and I have devoted much thought to this subject. I am firmly convinced that it can be done and hope that we shall live to see it done. ON THE LIGHT PHENOMENA PRODUCED BY HIGH-FREQUENCY CURRENTS OF HIGH POTENTIAL AND GENERAL REMARKS RELATING TO THE SUBJECT. Returning now to the light effects which it has been the chief object to investigate, it is thou...`

### 5. What the internet gets wrong

> "I think that beyond doubt it is possible to operate electrical devices in a city through the ground or pipe system by resonance from an electrical oscillator located at a central point"

- cited as: `(1894, p. 349)`
- why: the modest version of the plan, which is nothing like the wireless-power myth
- check_quotes.py: exact match, ratio 1.0, printed p. 349
- raw OCR: `.... 349 to work in synchronism with the latter, and the vibration thus intensified and spread over a large area, or a flow of electricity produced to or from the source st if the same be of opposite phase to the source s. I think that beyond doubt it is possible to operate electrical devices in a city through the ground or pipe system by resonance from an electrical oscillator located at a central point. But the practical solution of this problem would be of incomparably smaller benefit to man than the realization of the scheme of transmitting intelligence, or perhaps power, to any distance through the earth or environ...`

### 5. What the internet gets wrong

> "But the practical solution of this problem would be of incomparably smaller benefit to man than the realization of the scheme of transmitting intelligence, or perhaps power, to any distance through the earth or environing medium"

- cited as: `(1894, p. 349)`
- why: he ranks the two ideas, and the earth-power one is the lesser
- check_quotes.py: exact match, ratio 1.0, printed p. 349
- raw OCR: `...f opposite phase to the source s. I think that beyond doubt it is possible to operate electrical devices in a city through the ground or pipe system by resonance from an electrical oscillator located at a central point. But the practical solution of this problem would be of incomparably smaller benefit to man than the realization of the scheme of transmitting intelligence, or perhaps power, to any distance through the earth or environing medium. If this is at all possible, distance does not mean anything. Proper apparatus must first be produced by means of which the problem can be attacked and I have devoted much thought to this subject. I am firmly convinced...`

### 6. Why it did not happen

> "Proper apparatus must first be produced by means of which the problem can be attacked and I have devoted much thought to this subject"

- cited as: `(1894, p. 349)`
- why: what was missing in 1893: the apparatus, not the idea
- check_quotes.py: exact match, ratio 1.0, printed p. 349
- raw OCR: `...ller benefit to man than the realization of the scheme of transmitting intelligence, or perhaps power, to any distance through the earth or environing medium. If this is at all possible, distance does not mean anything. Proper apparatus must first be produced by means of which the problem can be attacked and I have devoted much thought to this subject. I am firmly convinced that it can be done and hope that we shall live to see it done. ON THE LIGHT PHENOMENA PRODUCED BY HIGH-FREQUENCY CURRENTS OF HIGH POTENTIAL AND GENERAL REMARKS RELATING TO THE SUBJECT. Returning...`

## Rejected: considered and not carried forward

- ~~"electric vibration or current can be transmitted with ease, without any return circuit"~~ (p. 143): the OCR reads 'transmitted witli ease' (ratio 0.983). 'witli' is not a long-s or S-for-8 artefact, so §3 does not allow silent normalisation and check_quotes.py would fail it. Pin the fragment that ends at 'circuit' instead
- ~~"under certain conditions it may be more economical to supply the electrical energy with one lead than with two"~~ (p. 137): the OCR reads 'witli one lead' (ratio 0.982), and the same claim is already pinned and used in article 02 from printed p. 267. Link to 02, do not quote it here
- ~~"An interesting feature of these high frequency currents is that they allow of operating all kinds of devices by connecting the device with only one leading wire to the electric source"~~ (p. 137): verifies exactly on p. 137, but it is article 02's subject and already used there. Link to 02
- ~~"We are whirling through endless space with an inconceivable speed, all around us everything is spinning, everything is moving, everywhere is energy"~~ (p. 196): as typed it returns no hit at all: the scan prints 'AVe are whirling'. The pinned form starts at 'are whirling'; see flags
- ~~"with potentials such as a few thousand volts there is no particular difficulty encountered in conveying currents from a machine giving, say, 20,000 alternations per second, to quite a distance"~~ (p. 151): as one run the OCR gives ratio 0.995: it carries a stray caret, 'giving^ say'. The two pinned fragments either side of the caret verify exactly
- ~~"to produce some electrical disturbance sufficiently powerful to be perceptible by suitable instruments at any point of the earth's surface"~~ (p. 347): the OCR of that line is scrambled by the column break: 'perof the earth's surface. ceptible by suitable instruments' (ratio 0.83). Do not print it; the sense is carried by the p. 348 quotes
- ~~"Assume that a source of alternating currents be connected, as in Fig. 185, with one of its terminals to earth"~~ (p. 348): the OCR doubles the s ('currentss', ratio 0.983). Describe Fig. 185 in our own words and cite the figure
- ~~"Thus it is certainly practicable to impress an electric vibration at least of a certain low period upon the earth by means of proper machinery"~~ (p. 348): the OCR interleaves the figure's lettering into this line ('$2 ... g', ratio 0.919). Do not print
- ~~"a ship at sea may, in this manner, catch fire at many points at once"~~ (p. 168): a different 'ship at sea': the lightning and cold-flame passage, which is article 06's material. Not this article's
- ~~"it would turn at any point of the earth's surface"~~ (p. 229): a false friend for the p. 138 phrase: this is the rotating brush in a vacuum bulb, not conduction through the earth. Do not mix the two
- ~~"through as much as an inch of the best solid insulating material"~~ (p. 151): verifies on p. 151, but article 11 already quotes it for the insulation beat (website/tesla-high-frequency-alternator.html). Use the p. 151 insulation sentence above and link to 11
- ~~"economical reasons will make it advisable to use only one wire, especially if the distances are great"~~ (p. 267): article 02's, already used there. Link to 02 instead of repeating it
- ~~"world system"~~ (not in this volume): 0 hits in the 1894 volume, as are 'Wardenclyffe' and 'Colorado Springs'. That phrase is later Tesla writing; if the draft uses it it needs a modern source (§4.1), not a page cite

## Flags for the writer (§3 quote policy, feature-004/t5)

- WHO IS SPEAKING. The three blocks of text this article quotes are not the same voice. Printed pp. 137-143 are chapter XXV, 'INTRODUCTION. — THE SCOPE OF THE TESLA LECTURES.' (printed pp. 119-144), the editor's recap of the lectures, in the third person — the same page opens 'An experiment of special interest shown by Mr. Tesla'. The p. 138 paragraph the brief calls 'the paragraph nobody quotes' is therefore the editor's summary, not Tesla's sentence: introduce it as the book's summary of the 1891 lecture, or quote it and say whose words they are. Never 'Tesla wrote'.
- Printed pp. 151, 196-197 are chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY AND THEIR APPLICATION TO METHODS OF ARTIFICIAL ILLUMINATION', the lecture delivered at Columbia College, New York, May 20 1891 (printed pp. 145-197). Tesla's own first-person text.
- Printed pp. 346-349 are chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', whose footnote on printed p. 294 dates it: 'A lecture delivered before the Franklin Institute, Philadelphia, February 1893, and before the National Electric Light Association, St. Louis, March [1893]' (the footnote is cut at the page break in this scan; the year of the second lecture is not on the page — say 'early 1893' or cite the two bodies, do not print a month you cannot see). This is the only block in the pin that is 1893 and first person, so it is what carries the brief's title 'In His Own Words (1893)'. Do not date the p. 138 or p. 151 material 1893.
- p. 138 'the high frequency coil arid the other end': the scan prints 'arid' for 'and'. That is a misprint, not a long-s or S-for-8 form, so §3 does not allow silently correcting it inside quotation marks. The pinned quote cuts there with an ellipsis; check_quotes.py then checks the two sides separately and both pass.
- p. 143 'electric vibration or current can be transmitted witli ease, without any return circuit': the scan reads 'witli'. Same handling — the pin starts after the misprint, at 'without any return circuit'.
- p. 347 'to the city water mains ... the other to an insulated body of large surface': the scan carries a footnote marker glued to 'mains'. The ellipsis in the pin covers it; do not print the marker.
- p. 151 'a machine giving, say, 20,000 alternations per second': the scan sets a stray caret, 'giving^ say', which makes the whole run a 0.995 near-match and therefore a FAIL in check_quotes.py. The pinned form cuts at the caret. Do not 'repair' the comma: the fragment as pinned is what verifies.
- p. 197 'We are whirling through endless space': the scan prints 'AVe are whirling', so the full sentence returns no hit at all. The pinned fragment starts at 'are whirling'; if the draft wants the sentence to begin, start the quotation at 'We' outside the marks and put the quoted words after — e.g. he writes that we 'are whirling…'. The printed sentence also runs across the page break: 'AVe are whirling through' ends printed p. 196 and 'endless space with an inconceivable speed…' begins printed p. 197, so cite it as pp. 196-197, not p. 197 alone.
- p. 346 'We now know that electric vibration may be transmitted through a single conductor. Why then not try…': the OCR spacing differs from the print (words glued at the line end). check_quotes.py passes this as a space-normalised match; print the clean form, no [sic].
- p. 346 'what is the capacity of the earth?': the 1894 compositor sets a space before the question mark. Quote the words and put the mark where our own style wants it; this is punctuation, not wording, and §3 allows it.
- p. 348 'the potential of the source must be excessive': the text calls the insulated body 'p' in lower case because it is labelled p in Fig. 185. Keep the lower case if the sentence is quoted, or paraphrase the figure and cite it.
- Two of the pinned quotes are the editor speaking about Tesla in the third person (p. 143 'He expressed his firm conviction…', and the p. 138 block). They may be quoted, but only as the book's report of the lecture. The article's case — a proposal with conditions — is carried by Tesla's own hedges on pp. 346-349 ('perhaps even power', 'I cannot stretch my imagination so far'), so prefer those where the point is what he claimed.
- The brief's section 3 wording, 'at a few thousand volts there is no particular difficulty…', is close to the print but not it: printed p. 151 reads 'for with potentials such as a few thousand volts there is no particular difficulty encountered in conveying currents from a machine giving^ say, 20,000 alternations per second, to quite a distance'. As one run that is a 0.995 near-match (the caret) and therefore a FAIL. Quote the pinned two fragments, or write the 'few thousand volts' point in our own words and cite p. 151.

## Notes for the figure task (feature-004/t6)

- the §9 brief 04 list names figures by PRINTED page: fig99 = printed p. 154 = website/assets/tesla1894/p172-fig1-fig99.webp, fig117 = printed p. 179 = p197-fig1-fig117.webp. The asset whose filename contains 'p179', p179-figs116-117.webp, is scan file 179 = printed p. 161 and is a different plate. Do not pick on the filename (§8 step 3).
- fig117 (printed p. 179) and Fig. 124 (printed p. 185) are already used by article 01 (index.json: /assets/tesla1894/p179-figs116-117.webp, re-cropped from scan file 197, supersedes p197-fig1-fig117.webp; and p185-fig124.webp, supersedes p203-fig1-fig124.webp). Reusing the same plate in 04 is allowed but pointless: 01 and 04 sit next to each other in the series. Choose a different second engraving.
- brief 04 asks for 'one elevation/earth-current engraving from pp. 183-190'. There is no earth-current engraving in that range. What is printed there: Figs. 120, 121A/B (printed p. 182, lamps with condenser coatings), Figs. 122 and 123 (printed p. 184, the same lamps with an outside coating, 'Lamps of this kind are illustrated in Fig. 122 and Fig. 123'), Fig. 124 (printed p. 185, one-wire plan of connection, used by 01), Fig. 125 (printed p. 188, two suspended metal sheets, the electrostatic-field room, 'I suspend two sheets as illustrated in Fig. 125'). Fig. 125 is the closest thing to the article's subject in that range and is unused by any article.
- the actual earth diagrams are in chapter XXVIII, not pp. 183-190: Fig. 184 on printed p. 344 (website/assets/tesla1894/p362-fig1-fig184.webp, 'In Fig. 184 I. is shown a plan which has been followed in the study of the resonance effects by means of a high frequency alternator') and Fig. 186a/b/c on printed p. 351 (p369-fig1-fig186.webp). Fig. 185 is referred to twice on printed p. 348 ('connected, as in Fig. 185, with one of its terminals to earth') but no 'FIG. 185' caption appears anywhere in the OCR of pp. 344-358 and the extractor cut no figure block from scan file 366. View scan file 366 before claiming that figure exists; if it is not on the page, cite Fig. 184 or Fig. 186 instead, or use a page-scan crop of printed p. 346 the way article 03 used p. 486.
- Fig. 99 (printed p. 154) is a machine, not a wireless apparatus: the text on that page calls it 'a smaller machine, in many respects similar to the former, only here the armature conductors and the exciting…' — it belongs to the high-frequency alternator discussion in chapter XXVI. If it is used, caption it as the machine of that chapter, not as the wireless transmitter. Article 11 covers that machine's chapter (XXIX, printed pp. 374-391) with Figs. 199-206 and does not use Fig. 99.

## Links (§5.2, for feature-004/t5 and t8)

- Out per the §9 brief 04 map and the §5.2 row for 04: whole-house.html, solar.html, 02 (tesla-one-wire-power.html), 11 (tesla-high-frequency-alternator.html), and the hub. §5.2 row 10 lists 04 among the pages that link to 10, which row 04's out-list does not — the map contradicts itself there. 10 does not exist yet (feature-007), so add 04 -> 10 when it is written and record the contradiction in index.json rather than inventing an out-link now.
- the reciprocal gate (qa_page.py: >= 3 out-links to pages that link back) cannot pass on 04 today, and not because of anything 04 does. Checked on 2026-10-11 against the drafts and index.json internal_links: 02's article.md links out to diy-magnetic-generator, magnetic-marvel, 11 and 01 — there is no href to 04, even though 02's quotes.md says 'link to 04'; 11's out-links are earthquake, worlds-fair, plans-review and dynamo; 01's are 11, worlds-fair, dynamo and electricity-using-magnets; the hub names 04 in index.json but is not rendered until feature-012. So 04 -> 02 is not yet a pair and no page links to 04 at all. That is feature-009/t2's job ('close the §5.2 out-link map on all 13 series pages'): if a failing reciprocal count shows up in t7, record it in index.json the way 11's entry records its backlink pass; do not pad 04 with off-map links to make the number.
- 02's quotes.md defers the sentence 'The current might be converted to low tension and used to operate a motor or other device' to this article; it is pinned here from printed p. 138, so 04 may use it and 02 may not.
