# Article 02 quote pin: tesla-one-wire-power.html

SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped from `books/extracted/tesla-1894-plain.txt` with `books/tools/grep_quote.py` on 2026-10-10 and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. The relevant text is chapter XXVII, 'Experiments of Alternate Currents of High Potential and Frequency' (London lecture, Feb 3 1892), printed pp. 232-237 and 267, plus one sentence from chapter XXVI (New York lecture, May 20 1891), printed p. 184.

Verified: 28 quotes, 0 failures. To re-check any single quote: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>`, or regenerate this whole file: `python3 new_content/1894-series/02-tesla-one-wire-power/gen_quotes.py`.

## Printed p. 184 (scan file 202)

### 4. Why it is not magic

> "In all cases the insulated body serves to give off the energy into the surrounding space, and is equivalent to a return wire"

- cited as: `(1894, p. 184)`
- why: the sentence that ends the 'no return path' reading; from the 1891 lecture
- grep_quote.py: exact match, ratio 1.0, printed p. 184
- raw OCR line: `184 INVENTIONS OF NIKOLA TKSLA. terminal of the lamp to one terminal of the source, and the other to an insulated body of the required size. In all cases the insulated body serves to give off the energy into the surrounding space, and is equivalent to a return wire. Obviously, in the two last-named cases, instead of connecting the wires to an insulated body, connections may be made to the ground. The experiments which will prove most suggestive and of most interest to the investig...`

## Printed p. 232 (scan file 250)

### 2. His statement

> "A most curious feature of alternate currents of high frequencies and potentials is that they enable us to perform many experiments by the use of one wire only"

- cited as: `(1894, p. 232)`
- why: the H1 promise, quoted in full and at the top of the second H2
- grep_quote.py: exact match, ratio 1.0, printed p. 232
- raw OCR line: `...receding experiment with the electric radiometer the potential should not exceed a certain limit, as then the electrostatic attraction between the vanes and the glass of the bulb may be so great as to stop the rotation. A most curious feature of alternate currents of high frequencies and potentials is that they enable us to perform many experiments by the use of one wire only. In many respects this feat, ure is of great interest.`

## Printed p. 233 (scan file 251)

### 3. What he actually did with it

> "a coil wound upon an iron core and traversed by an alternating current creates a moving field of force, capable of setting an armature in rotation"

- cited as: `(1894, p. 233)`
- why: why the demo motor needs only one coil, and the honest 'must remain an open question' about why
- grep_quote.py: exact match, ratio 1.0, printed p. 233
- raw OCR line: `...to my hand, I found the idea of the time lag advocated. Whether there is a true time lag, or whether the retardation isdue to eddy currents circulating in minute paths, must remain an open question, but the fact is that a coil wound upon an iron core and traversed by an alternating current creates a moving field of force, capable of setting an armature in rotation. It is of some interest, in conjunction with the historical Arago experiment, to mention that in lag or phase motors I have produced rotation in the opposite direction to the moving field, which means that in that exper...`

## Printed p. 234 (scan file 252)

### 3. What he actually did with it

> "this motor rotates with one single connection between it and the generator"

- cited as: `(1894, p. 234)`
- why: the demo he chose for the lecture: a coil, a copper disc, one wire. OCR glues 'itand'; see flags below
- grep_quote.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 234
- raw OCR line: `234 INVENTIONS OF NIKOLA TESLA. show you is that this motor rotates with one single connection between itand the generator; that is to say, one terminal of the motor is connected to one terminal of the generator — in this case the secondary of a high-tension induction coil — the other terminals of motor and generator being insulated in spac...`

### 3. What he actually did with it

> "the other terminals of motor and generator being insulated in space"

- cited as: `(1894, p. 234)`
- why: the part people leave out: the second terminal is not missing, it is open
- grep_quote.py: exact match, ratio 1.0, printed p. 234
- raw OCR line: `...tor rotates with one single connection between itand the generator; that is to say, one terminal of the motor is connected to one terminal of the generator — in this case the secondary of a high-tension induction coil — the other terminals of motor and generator being insulated in space. To produce rotation it is generally (but not absolutely ) necessary to connect the free end of the motor coil to an insulated body of some size. The experimenter's body is more than sufficient. If he touches the free t...`

### 4. Why it is not magic

> "To produce rotation it is generally (but not absolutely) necessary to connect the free end of the motor coil to an insulated body of some size"

- cited as: `(1894, p. 234)`
- why: the size of the missing conductor is a design variable. OCR has a stray space inside '(but not absolutely )'; see flags below
- grep_quote.py: whitespace-only difference: the OCR spacing is not the print's (words glued, or a stray space). Print the clean form; check_quotes.py flags it the same way, printed p. 234
- raw OCR line: `...hat is to say, one terminal of the motor is connected to one terminal of the generator — in this case the secondary of a high-tension induction coil — the other terminals of motor and generator being insulated in space. To produce rotation it is generally (but not absolutely ) necessary to connect the free end of the motor coil to an insulated body of some size. The experimenter's body is more than sufficient. If he touches the free terminal with an object held in the hand, a cur...`

### 3. What he actually did with it

> "The experimenter's body is more than sufficient"

- cited as: `(1894, p. 234)`
- why: one-line bridge to article 01 (lamps in hand), which is the same trick
- grep_quote.py: exact match, ratio 1.0, printed p. 234
- raw OCR line: `...oil — the other terminals of motor and generator being insulated in space. To produce rotation it is generally (but not absolutely ) necessary to connect the free end of the motor coil to an insulated body of some size. The experimenter's body is more than sufficient. If he touches the free terminal with an object held in the hand, a current passes through the coil and the copper disc is set in rotation. If an exhausted tube is put in series with the coil, the tube lights brilliantl...`

### 3. What he actually did with it

> "If an exhausted tube is put in series with the coil, the tube lights brilliantly, showing the passage of a strong current"

- cited as: `(1894, p. 234)`
- why: the proof it is not a static effect: a real current flows through one wire
- grep_quote.py: exact match, ratio 1.0, printed p. 234
- raw OCR line: `...an insulated body of some size. The experimenter's body is more than sufficient. If he touches the free terminal with an object held in the hand, a current passes through the coil and the copper disc is set in rotation. If an exhausted tube is put in series with the coil, the tube lights brilliantly, showing the passage of a strong current. In- PIG. 146. stead of the experimenter's body, a small metal sheet suspended on a cord may be used with the same result. In this case the plate acts as a condenser in series with the coil. It counteracts the self-indu...`

### 4. Why it is not magic

> "the plate acts as a condenser in series with the coil"

- cited as: `(1894, p. 234)`
- why: Tesla's own mechanism, in his words: series capacitance, not magic
- grep_quote.py: exact match, ratio 1.0, printed p. 234
- raw OCR line: `...with the coil, the tube lights brilliantly, showing the passage of a strong current. In- PIG. 146. stead of the experimenter's body, a small metal sheet suspended on a cord may be used with the same result. In this case the plate acts as a condenser in series with the coil. It counteracts the self-induction of the latter and allows a strong current to pass. In such a combination, the greater the self-induction of the coil the smaller need be the plate, and this means that a lower frequenc...`

### 4. Why it is not magic

> "It counteracts the self-induction of the latter and allows a strong current to pass"

- cited as: `(1894, p. 234)`
- why: why he picked a single-coil motor for the demo (high self-induction)
- grep_quote.py: exact match, ratio 1.0, printed p. 234
- raw OCR line: `...passage of a strong current. In- PIG. 146. stead of the experimenter's body, a small metal sheet suspended on a cord may be used with the same result. In this case the plate acts as a condenser in series with the coil. It counteracts the self-induction of the latter and allows a strong current to pass. In such a combination, the greater the self-induction of the coil the smaller need be the plate, and this means that a lower frequency, or eventually a lower potential, is required to operate the motor. A single coil w...`

## Printed p. 235 (scan file 253)

### 4. Why it is not magic

> "it is not necessary to have even a single connection between the motor and generator, except, perhaps, through the ground"

- cited as: `(1894, p. 235)`
- why: he pushes it to zero wires, and names the alternative path himself
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...hrough a condenser, it is almost essential, in order to produce rotation, to make the primary and secondary coils overlap each other more or less. But there is an additional feature of interest about this motor, namely, it is not necessary to have even a single connection between the motor and generator, except, perhaps, through the ground; for not only is an insulated plate capable of giving off energy into space, but it is likewise capable of deriving it from an alternating electrostatic field, though in the latter case the available energy is much smal...`

### 4. Why it is not magic

> "not only is an insulated plate capable of giving off energy into space, but it is likewise capable of deriving it from an alternating electrostatic field"

- cited as: `(1894, p. 235)`
- why: the receive half of the same statement
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...other more or less. But there is an additional feature of interest about this motor, namely, it is not necessary to have even a single connection between the motor and generator, except, perhaps, through the ground; for not only is an insulated plate capable of giving off energy into space, but it is likewise capable of deriving it from an alternating electrostatic field, though in the latter case the available energy is much smaller. In this instance one of the motor terminals is connected to the insulated plate or body located within the alternating electrostatic field, and the other...`

### 1. The rule you were taught

> "such " no wire " motors, as they might be called"

- cited as: `(1894, p. 235)`
- why: his own label for it, quoted with the 1894 spacing inside the marks (see flags)
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...is instance one of the motor terminals is connected to the insulated plate or body located within the alternating electrostatic field, and the other terminal preferably to the ground. It is quite possible, however, that such " no wire " motors, as they might be called, could be operated by conduction through the rarefied air at considerable distances. Alternate currents, especially of high frequencies, pass with astonishing freedom through even slightly rarefied gases. The upper stra...`

### 6. What the internet gets wrong

> "Alternate currents, especially of high frequencies, pass with astonishing freedom through even slightly rarefied gases"

- cited as: `(1894, p. 235)`
- why: the rarefied-air path he actually considered, before he drops the idea
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...and the other terminal preferably to the ground. It is quite possible, however, that such " no wire " motors, as they might be called, could be operated by conduction through the rarefied air at considerable distances. Alternate currents, especially of high frequencies, pass with astonishing freedom through even slightly rarefied gases. The upper strata of the air are rarefied. To reach a number of miles out into space requires the overcoming of difficulties of a merely mechanical nature. There is no doubt that with the enormous potentials obtainable...`

### 6. What the internet gets wrong

> "But such schemes are mentioned merely as possibilities"

- cited as: `(1894, p. 235)`
- why: the sentence that kills the 'Tesla said no wires needed' version
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...ight be passed through many miles of rarefied air, and that, by thus directing the energy of many hundreds or thousands of horsepower, motors or lamps might be operated at considerable distances from stationary sources. But such schemes are mentioned merely as possibilities. We shall have no need to transmit power in this way. We shall have no need to transmit power at all. Ere many generations pass, our machinery will be driven by a power obtainable at any point of the universe. This idea...`

### 6. What the internet gets wrong

> "We shall have no need to transmit power at all"

- cited as: `(1894, p. 235)`
- why: the sentence that gets quoted as prophecy; here it is with the sentence before it
- grep_quote.py: exact match, ratio 1.0, printed p. 235
- raw OCR line: `...thousands of horsepower, motors or lamps might be operated at considerable distances from stationary sources. But such schemes are mentioned merely as possibilities. We shall have no need to transmit power in this way. We shall have no need to transmit power at all. Ere many generations pass, our machinery will be driven by a power obtainable at any point of the universe. This idea is`

## Printed p. 236 (scan file 254)

### 3. What he actually did with it

> "We may connect an insulated line to a source of such currents, we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusing a thick copper wire"

- cited as: `(1894, p. 236)`
- why: the one-wire distribution claim, with the inappreciable line current attached
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...most inefficient machine ever invented ! The preceding experiment is only one of many equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency. We may connect an insulated line to a source of such currents, we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusing a thick copper wire. Or we may, by the help of some artifice, decompose a solution in any electrolytic cell by connecting only one pole of the cell to the line or source of energy. Or we may, by attaching to the line, or only bringing into...`

### 3. What he actually did with it

> "decompose a solution in any electrolytic cell by connecting only one pole of the cell to the line or source of energy"

- cited as: `(1894, p. 236)`
- why: single-pole electrolysis, the second of the three demos
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...e of such currents, we may pass an inappreciable current over the line, and on any point of the same we are able to obtain a heavy current, capable of fusing a thick copper wire. Or we may, by the help of some artifice, decompose a solution in any electrolytic cell by connecting only one pole of the cell to the line or source of energy. Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases,...`

### 3. What he actually did with it

> "Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb"

- cited as: `(1894, p. 236)`
- why: the third demo, and the one the site's readers picture
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...ain a heavy current, capable of fusing a thick copper wire. Or we may, by the help of some artifice, decompose a solution in any electrolytic cell by connecting only one pole of the cell to the line or source of energy. Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires we...`

### 5. Tesla's own economic case

> "However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light"

- cited as: `(1894, p. 236)`
- why: where he thought one-wire was actually worth it: lighting, not power
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...connecting only one pole of the cell to the line or source of energy. Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire. It is now a fact that a body may be rendered incandescent or phosphoresce...`

### 5. Tesla's own economic case

> "A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire"

- cited as: `(1894, p. 236)`
- why: he admits the return wire and argues for dropping it, in the same breath
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...an incandescent lamp, an exhausted tube, or a phosphorescent bulb. However impracticable this plan of working may appear in many cases, it certainly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire. It is now a fact that a body may be rendered incandescent or phosphorescent by bringing it either in single contact or merely in the vicinity of a source of electric impulses of the proper character, and that in this m...`

### 3. What he actually did with it

> "It is now a fact that a body may be rendered incandescent or phosphorescent by bringing it either in single contact or merely in the vicinity of a source of electric impulses of the proper character"

- cited as: `(1894, p. 236)`
- why: what he claims is settled, and how carefully he words it
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...nly seems practicable, and even recommendable, in the production of light. A perfected lamp would require but little energy, and if wires were used at all we ought to be able to supply that energy without a return wire. It is now a fact that a body may be rendered incandescent or phosphorescent by bringing it either in single contact or merely in the vicinity of a source of electric impulses of the proper character, and that in this manner a quantity of light sufficient to afford a practical illuminant may be produced. It is, therefore, to say the least, worth while to attempt to determine the best conditions and to invent the bes...`

### 6. What the internet gets wrong

> "the most inefficient machine ever invented"

- cited as: `(1894, p. 236)`
- why: the free-energy beat, one clause only; the full quote belongs to article 10
- grep_quote.py: exact match, ratio 1.0, printed p. 236
- raw OCR line: `...e night; it will turn everywhere where there is heat, and heat is everywhere. But, unfortunately, this beautiful little machine, while it goes down to posterity as the most interesting, must likewise be put on record as the most inefficient machine ever invented ! The preceding experiment is only one of many equally interesting experiments which may be performed by the use of only one wire with alternations of high potential and frequency. We may connect an insulated line to a...`

## Printed p. 267 (scan file 285)

### 6. What the internet gets wrong

> "the total energy lost must be proportionate to the product of the frequency and the square of the electric density"

- cited as: `(1894, p. 267)`
- why: the loss law, and he flags it himself as unconfirmed
- grep_quote.py: exact match, ratio 1.0, printed p. 267
- raw OCR line: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 267 to the molecule is proportionate to that density. I conclude from this that the total energy lost must be proportionate to the product of the frequency and the square of the electric density ; but this law needs experimental confirmation. Assuming the preceding- considerations to be true, then, by rapidly alternating the potential of a body immersed in an insulating gaseous medium, any amount of energy may...`

### 5. Tesla's own economic case

> "currents of very high frequencies involve considerable waste when transmitted through conductors"

- cited as: `(1894, p. 267)`
- why: the reason one wire can be cheaper: the copper is where the loss is
- grep_quote.py: exact match, ratio 1.0, printed p. 267
- raw OCR line: `...the dissipation, it is necessary to work with a small electric density — the smaller, the higher the frequency. But since, on the assumption before made, the loss is diminished with the square of the density, and since currents of very high frequencies involve considerable waste when transmitted through conductors, it follows that, on the whole, it is better to employ one wire than two. Therefore, if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequen...`

### 5. Tesla's own economic case

> "it follows that, on the whole, it is better to employ one wire than two"

- cited as: `(1894, p. 267)`
- why: the engineering conclusion, not a vision statement
- grep_quote.py: exact match, ratio 1.0, printed p. 267
- raw OCR line: `...the frequency. But since, on the assumption before made, the loss is diminished with the square of the density, and since currents of very high frequencies involve considerable waste when transmitted through conductors, it follows that, on the whole, it is better to employ one wire than two. Therefore, if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequency, economical reasons will make it advisable to use only one wire, espec...`

### 5. Tesla's own economic case

> "economical reasons will make it advisable to use only one wire, especially if the distances are great"

- cited as: `(1894, p. 267)`
- why: the sentence the brief asks for, in full
- grep_quote.py: exact match, ratio 1.0, printed p. 267
- raw OCR line: `...follows that, on the whole, it is better to employ one wire than two. Therefore, if motors, lamps, or devices of any kind are perfected, capable of being advantageously operated by currents of extremely high frequency, economical reasons will make it advisable to use only one wire, especially if the distances are great. When energy is absorbed in a condenser, the same behaves as though its capacity were increased. Absorption always exists more or less, but generally it is small and of no consequence us long as the frequencies are not...`

### 4. Why it is not magic

> "To reduce the dissipation, it is necessary to work with a small electric density"

- cited as: `(1894, p. 267)`
- why: the cost side: high frequency is not free, it is traded against potential
- grep_quote.py: exact match, ratio 1.0, printed p. 267
- raw OCR line: `...distance, as is thought most generally, but is consumed — in the case of an insulated sphere, for example — in impact and collisional losses — that is, heat vibrations — on the surface and in the vicinity of the sphere. To reduce the dissipation, it is necessary to work with a small electric density — the smaller, the higher the frequency. But since, on the assumption before made, the loss is diminished with the square of the density, and since currents of very high frequencies involve considerable waste when trans...`

## Rejected: considered and not carried forward

- ~~"In many respects this feature is of great interest"~~ (p. 232): the OCR of the same line reads 'this feat, ure is of great interest' (ratio 0.882). The comma is an artefact of the scan, but §3 only allows silent normalisation of long-s and S-for-8, so do not print this fragment
- ~~"we may take another tube and it might not light"~~ (p. 288): no match as typed. The real line is 'But I may take another tube and it might not light' (p. 288, ratio 1.0), which is the Philadelphia/St. Louis lecture and article 01's material, not this chapter. Exactly the kind of half-remembered quote §0 forbids: not used here
- ~~"the current might be converted to low tension and used to operate a motor or other device"~~ (p. 138): verifies on p. 138, but that is the 1891 earth-return passage and belongs to article 04 (wireless power 1893). Link to 04 instead of quoting it here

## Flags for the writer (§3 quote policy)

- p. 234 'between it and the generator': the OCR glues the words ('itand'). grep_quote.py matches it fuzzily (ratio 0.954) and check_quotes.py will pass it as a space-normalised match. The printed page has the space; print it with the space.
- p. 234 '(but not absolutely)': the OCR carries a stray space before the closing bracket ('absolutely )', ratio 0.979). Same handling: print the clean form, the scan shows no gap.
- p. 236 'A perfected lamp would require but little energy': the capital A is genuine, it starts a sentence in the print. Quote it as it stands.
- p. 236 'the most inefficient machine ever invented': the print puts a space before the exclamation mark ('invented !'). Quote the words only and end the sentence outside the quotation marks. The full 'wheelwork of nature' passage is article 10's; here take the one clause and link to 10.
- p. 235 'such " no wire " motors': the 1894 text sets the phrase in spaced double quotes. Inside our own quotation marks use single quotes for the term and drop the 1894 spacing; do not add [sic].
- p. 267 the loss law: he adds 'but this law needs experimental confirmation' in the same sentence. Quote the law and keep that clause; it is the honest version.

## Notes for the figure task (t2)

- the diagram the text calls Fig. 146 is the one-wire motor: 'Here, then, is a motor (diagrammatically illustrated in Fig. 146)' (printed p. 233), and the plate itself sits on printed p. 234 (scan file 252). The §9 brief 02 figure list names fig144 / fig151 / fig153 instead; Fig. 146 is the one that shows the experiment this article describes.
- the extractor crop for that plate is website/assets/tesla1894/p252-fig1.webp and carries no figure number in its name. Read the number off the scan before using it (the OCR of the printed caption reads 'PIG. 146.').
- brief 02's figure names are printed pages, the asset filenames are scan files: fig144 = printed p. 228 = p246-fig1-fig144.webp, fig151 = printed p. 247 = p265-fig1-fig151.webp, fig153 = printed p. 263 = p281-fig1-fig153.webp. All three are lamp sections, not one-wire circuits.

## Links (§5.2, for t1 and t4)

Out per the map: `diy-magnetic-generator.html`, `can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html`, `tesla-high-frequency-alternator.html` (11), and the hub when it exists. In per the map: 01, 04, 11, hub. None of those link to 02 yet, because 02 does not exist yet.

The reciprocal gate (qa_page.py: >= 3 out-links to pages that link back) cannot pass on 02 from the §5.2 out-list alone: 11 links out to 02, so 02 <-> 11 is one pair; 04 links out to 02 (feature-004/t5), so 02 -> 04 makes a second; 01 is listed as a required in-link for 02 but 01's own out-list does not name 02, so 01 needs an added out-link to 02 and 02 an out-link to 01 to make the third. That re-render of 01 and 11 is feature-009/t2's job; record it in index.json when 02 ships.
