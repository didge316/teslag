# Article 06 quote pin: tesla-cold-flame.html

SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped on 2026-10-11 from `books/extracted/tesla-1894-plain.txt` through the same matcher `books/tools/check_quotes.py` uses (exact, or verbatim once OCR spacing is ignored) and is pinned to the printed page it was found on (printed page = scan file page - 18, §0). A quote carrying ' ... ' is cut where the scan is corrupt; each side of the cut is verified separately, which is how check_quotes.py will judge the draft. `article.md` for this page is written from this file; a quote that is not here does not go in the draft.

Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. Four different texts are quoted and they are not the same paper:

- chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY', a lecture delivered before the American Institute of Electrical Engineers at Columbia College, N. Y., May 20 1891 (printed pp. 145-197; the footnote verifies exactly, printed p. 145). This is the article's spine: the hot brush, the tube over the flame, the 'veritable flame' prospect. Printed pp. 166-167, 171.
- chapter XXVII, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF HIGH POTENTIAL AND HIGH FREQUENCY', a lecture delivered before the Institution of Electrical Engineers, London, February 1892 (printed pp. 198-293; the footnote verifies exactly, printed p. 198). The stage moment, the vacuum brushes, the plasma globe. Printed pp. 226-229, 258-259, 291.
- chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', the Philadelphia and St. Louis lecture, February-March 1892 (printed pp. 294-373). One quote, on the brush discharge as an energy loss. Printed p. 322.
- chapter XXIX, the high-frequency alternator chapter - the EDITOR's text in the third person, the same chapter article 11 is built on. The 15,000 and 30,000 alternations-per-second figures. Printed pp. 376, 381. Attribute these to the book, not to Tesla.

Verified: 34 quotes (34 fragments) across 14 printed pages, 0 failures. To re-check one quote: `python3 books/tools/grep_quote.py "<quote>" --page <lo>-<hi>`. To regenerate this file: `python3 new_content/1894-series/06-tesla-cold-flame/gen_quotes.py` (it exits non-zero and writes nothing if any quote fails).

## Printed p. 166 (scan file 184)

### 2. What a brush actually is

> "one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure"

- cited as: `(1894, p. 166)`
- why: the observation the article's central image rests on, and the sentence that points at Fig. 110 on the same page - see the figure notes
- check_quotes.py: exact match, ratio 1.0, printed p. 166
- raw OCR: `...shes cannot form anywhere except at the tops of the columns. If the conditions are carefully adjusted — which, of course, must be left to the skill of the experimenter — so that the potential rises to an enormous value, one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure (Fig. 110). But they do not only resemble, they are veritable flames, for they are hot. Certainly they are not as hot as a gas burner, but they would be so if the frequency cmd the potential would be sufficiently high....`

### 2. What a brush actually is

> "But they do not only resemble, they are veritable flames, for they are hot"

- cited as: `(1894, p. 166)`
- why: the sentence this article's title has to answer: he insists the brush is hot. 'Cold' is only true beside a gas flame
- check_quotes.py: exact match, ratio 1.0, printed p. 166
- raw OCR: `...rises to an enormous value, one may produce two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure (Fig. 110). But they do not only resemble, they are veritable flames, for they are hot. Certainly they are not as hot as a gas burner, but they would be so if the frequency cmd the potential would be sufficiently high. Produced with, say, twenty thousand alternations per second, the heat is easily percept...`

### 2. What a brush actually is

> "The heat developed is, of course, due to the impact of the air molecules against the terminals and against each other"

- cited as: `(1894, p. 166)`
- why: his mechanism in his own words: molecular bombardment. Section 2 explains this in plain English; it does not replace it with modern wording
- check_quotes.py: exact match, ratio 1.0, printed p. 166
- raw OCR: `...they would be so if the frequency cmd the potential would be sufficiently high. Produced with, say, twenty thousand alternations per second, the heat is easily perceptible even if the potential is not excessively high. The heat developed is, of course, due to the impact of the air molecules against the terminals and against each other. As, at the ordinary pressures, the mean free path is excessively small, it is possible that in spite of the enormous initial speed imparted to each molecule upon coming in contact with the terminal, its progress — by c...`

### 4. Why he never got it

> "Certainly they are not as hot as a gas burner, but they would be so if the frequency"

- cited as: `(1894, p. 166)`
- why: the honest scale of what he had: cooler than a gas burner, and it would not be only if the frequency were higher. Cut before the OCR's 'frequency cmd the potential'; see rejected #3
- check_quotes.py: exact match, ratio 1.0, printed p. 166
- raw OCR: `...hes long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure (Fig. 110). But they do not only resemble, they are veritable flames, for they are hot. Certainly they are not as hot as a gas burner, but they would be so if the frequency cmd the potential would be sufficiently high. Produced with, say, twenty thousand alternations per second, the heat is easily perceptible even if the potential is not excessively high. The heat developed is, of course,...`

### 4. Why he never got it

> "The higher the frequency, the less the molecule is able to get away, and this the more so, as for a given effect the potential required is smaller"

- cited as: `(1894, p. 166)`
- why: the scaling argument that makes him think a high enough frequency is reachable. The sentence runs on across the page break onto printed p. 167; the next quote is its far end
- check_quotes.py: exact match, ratio 1.0, printed p. 166
- raw OCR: `...n coming in contact with the terminal, its progress — by collision with other molecules — is retarded to such an extent, that it does not get away far from the terminal, but may strike the same many times in succession. The higher the frequency, the less the molecule is able to get away, and this the more so, as for a given effect the potential required is smaller ; and a frequency is conceivable — perhaps even obtainable — at`

## Printed p. 167 (scan file 185)

### 2. What a brush actually is

> "In the positive brush of a static machine the exchange of the molecules is very rapid, the stream is constantly of one direction, and there are fewer collisions ; hence the heating effect must be very small"

- cited as: `(1894, p. 167)`
- why: why a brush can feel cool: rapid exchange, few collisions. The ' ;' is the print's spacing; see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...ecules would be very slow, and the heat produced at, and very near, the terminal would be excessive. But if the frequency would go on increasing constantly, the heat produced would begin to diminish for obvious reasons. In the positive brush of a static machine the exchange of the molecules is very rapid, the stream is constantly of one direction, and there are fewer collisions ; hence the heating effect must be very small. Anything that impairs the facility of exchange tends to increase the local heat produced. Thus, if a bulb be held over the terminal of the coil so as to enclose the brush, the air contained in the bulb is very quickly...`

### 2. What a brush actually is

> "Anything that impairs the facility of exchange tends to increase the local heat produced"

- cited as: `(1894, p. 167)`
- why: the rule, stated as a rule. It is what makes the tube and bulb demonstrations in the next two quotes work
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...us reasons. In the positive brush of a static machine the exchange of the molecules is very rapid, the stream is constantly of one direction, and there are fewer collisions ; hence the heating effect must be very small. Anything that impairs the facility of exchange tends to increase the local heat produced. Thus, if a bulb be held over the terminal of the coil so as to enclose the brush, the air contained in the bulb is very quickly brought to a high temperature. If a glass tube be held over the brush so as to allow the d...`

### 2. What a brush actually is

> "If a glass tube be held over the brush so as to allow the draught to carry the brush upwards, scorching hot air escapes at the top of the tube"

- cited as: `(1894, p. 167)`
- why: the demonstration he does with a tube over the flame, and the air coming out scorching. 'Scorching' is his word, and it contradicts 'the flame that doesn't burn'
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...ility of exchange tends to increase the local heat produced. Thus, if a bulb be held over the terminal of the coil so as to enclose the brush, the air contained in the bulb is very quickly brought to a high temperature. If a glass tube be held over the brush so as to allow the draught to carry the brush upwards, scorching hot air escapes at the top of the tube. Anything held within the brush is, of course, rapidly heated, and the possibility of using such heating effects for some purpose or other suggests itself. When contemplating this singular phenomenon of the hot brush, w...`

### 2. What a brush actually is

> "Anything held within the brush is, of course, rapidly heated, and the possibility of using such heating effects for some purpose or other suggests itself"

- cited as: `(1894, p. 167)`
- why: the practical consequence he draws, hedged with 'suggests itself'
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...he air contained in the bulb is very quickly brought to a high temperature. If a glass tube be held over the brush so as to allow the draught to carry the brush upwards, scorching hot air escapes at the top of the tube. Anything held within the brush is, of course, rapidly heated, and the possibility of using such heating effects for some purpose or other suggests itself. When contemplating this singular phenomenon of the hot brush, we cannot help being convinced that a similar process must take place in the ordinary flame, and it seems strange that after all these centuries past of fam...`

### 3. Tesla's bigger idea

> "When contemplating this singular phenomenon of the hot brush, we cannot help being convinced that a similar process must take place in the ordinary flame"

- cited as: `(1894, p. 167)`
- why: the inference that gives this article its name: he argues the hot brush IS the ordinary flame's process. 'the hot brush' is the book's own phrase - 2 hits in the volume, printed pp. 127 and 167
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...brush upwards, scorching hot air escapes at the top of the tube. Anything held within the brush is, of course, rapidly heated, and the possibility of using such heating effects for some purpose or other suggests itself. When contemplating this singular phenomenon of the hot brush, we cannot help being convinced that a similar process must take place in the ordinary flame, and it seems strange that after all these centuries past of familiarity with the flame, now, in this era of electric lighting and heating, we are finally led to recognize, that since time immemorial we have, after all,...`

### 3. Tesla's bigger idea

> "we have a possible way of producing - by other than chemical means - a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods of producing enormous frequencies and potentials"

- cited as: `(1894, p. 167)`
- why: the brief's section 3 quote, in full and in a form that verifies. The print sets 'by other than chemical means' off with em dashes; grep_quote.py folds a typed ' - ' to the same normalised text, so this ASCII form matches exactly. The cut form with ' ... ' also verifies, fragment by fragment - see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...lectric lighting and heating, we are finally led to recognize, that since time immemorial we have, after all, always had " electric light and heat " at our disposal. It is also of no little interest to contemplate, that we have a possible way of producing — by other than chemical means — a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods...`

### 3. Tesla's bigger idea

> "I have no doubt that if the potential could be made to alternate with sufficient rapidity and power, the brush formed at the end of a wire would lose its electrical characteristics and would become flamelike"

- cited as: `(1894, p. 167)`
- why: the claim with its condition attached: 'if the potential could be made to alternate with sufficient rapidity and power'. He does not say it works; he says what would have to be true for it to work
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `..., which would give light and heat without any material being consumed, without any chemical process taking place, and to accomplish this, we only need to perfect methods of producing enormous frequencies and potentials. I have no doubt that if the potential could be made to alternate with sufficient rapidity and power, the brush formed at the end of a wire would lose its electrical characteristics and would become flamelike. The flame must be due to electrostatic molecular action. This phenomenon now explains in a manner which can hardly be doubted the frequent accidents occurring in storms. It is well known that objects are often set on f...`

### 3. Tesla's bigger idea

> "The flame must be due to electrostatic molecular action"

- cited as: `(1894, p. 167)`
- why: his one-sentence theory of the flame. Short, and it is his, so it can carry quotation marks; the modern ionisation account is ours (see flags)
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `...otentials. I have no doubt that if the potential could be made to alternate with sufficient rapidity and power, the brush formed at the end of a wire would lose its electrical characteristics and would become flamelike. The flame must be due to electrostatic molecular action. This phenomenon now explains in a manner which can hardly be doubted the frequent accidents occurring in storms. It is well known that objects are often set on fire without the lightning striking them. We shall present...`

### 4. Why he never got it

> "which practically the same molecules would strike the terminal"

- cited as: `(1894, p. 167)`
- why: the end of that sentence, on printed p. 167: a frequency at which the same molecules would be struck again and again. Pinned to its own page because the cut is at the break
- check_quotes.py: exact match, ratio 1.0, printed p. 167
- raw OCR: `HIGH FREQUENCY AND HIGH POTENTIAL CURRENTS. 167 which practically the same molecules would strike the terminal. Under such conditions the exchange of the molecules would be very slow, and the heat produced at, and very near, the terminal would be excessive. But if the frequency would go on increasing constantly, the heat produce...`

## Printed p. 169 (scan file 187)

### 4. Why he never got it

> "In employing a commercial coil, the production of very powerful brush effects is attended with considerable difficulties"

- cited as: `(1894, p. 169)`
- why: the practical blocker, in his words: the off-the-shelf apparatus of 1891 could not do this
- check_quotes.py: exact match, ratio 1.0, printed p. 169
- raw OCR: `...r even when not at all enclosed, would seem to afford a possible way of obtaining light eifects, which, in perfecting methods of producing rapidly alternating potentials, might be rendered available for useful purposes. In employing a commercial coil, the production of very powerful brush effects is attended with considerable difficulties, for FIG. 112*. when these high frequencies and enormous potentials are used, the best insulation is apt to give way. Usually the coil is insulated well enough to stand the strain from convolution to convolution, since...`

### 4. Why he never got it

> "when these high frequencies and enormous potentials are used, the best insulation is apt to give way"

- cited as: `(1894, p. 169)`
- why: what actually failed: insulation. The printed page interleaves the caption 'FIG. 112*.' between the two halves of this sentence; grep_quote.py's strip_furniture() drops the caption line, so the run verifies
- check_quotes.py: exact match, ratio 1.0, printed p. 169
- raw OCR: `...g rapidly alternating potentials, might be rendered available for useful purposes. In employing a commercial coil, the production of very powerful brush effects is attended with considerable difficulties, for FIG. 112*. when these high frequencies and enormous potentials are used, the best insulation is apt to give way. Usually the coil is insulated well enough to stand the strain from convolution to convolution, since two double silk covered paraffined wires will withstand a pressure of several thousand volts; the difficulty lies pri...`

## Printed p. 171 (scan file 189)

### 6. Where you see it now

> "For the production of ozone, alternating currents of very high frequency are eminently suited"

- cited as: `(1894, p. 171)`
- why: the direct ancestor of the ozone generator, stated by him. 'ozone' occurs in the volume on printed pp. 127, 158, 171, 322, and in the index at pp. 495-496
- check_quotes.py: exact match, ratio 1.0, printed p. 171
- raw OCR: `...fects. It is a most powerful ozonizer, so powerful indeed, that only a few minutes are sufficient to fill the whole room with the smell of ozone, and it undoubtedly possesses the quality of exciting chemical affinities. For the production of ozone, alternating currents of very high frequency are eminently suited, not only on account of the advantages they offer in the way of conversion but also because of the fact, that the ozonizing action of a discharge is dependent on the frequency as well as on the potential, this being und...`

### 6. Where you see it now

> "the ozonizing action of a discharge is dependent on the frequency as well as on the potential"

- cited as: `(1894, p. 171)`
- why: why frequency matters for the descendant devices, in his own account of his experiments
- check_quotes.py: exact match, ratio 1.0, printed p. 171
- raw OCR: `...cal affinities. For the production of ozone, alternating currents of very high frequency are eminently suited, not only on account of the advantages they offer in the way of conversion but also because of the fact, that the ozonizing action of a discharge is dependent on the frequency as well as on the potential, this being undoubtedly confirmed by observation. In these experiments if an iron core is used it should be carefully watched, as it is apt to get excessively hot in an incredibly short time. To give an idea of the rapi...`

## Printed p. 213 (scan file 231)

### 4. Why he never got it

> "the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential"

- cited as: `(1894, p. 213)`
- why: the law he thought governed it: heat and light go as frequency times potential squared. This is why 'enormous frequencies and potentials' is the whole difficulty, quantitatively
- check_quotes.py: exact match, ratio 1.0, printed p. 213
- raw OCR: `...losses are very small. In the preceding experiment it is of considerable interest to know what relation the quantity of the light emitted bears to the frequency and potential of the electric impulses. My opinion is that the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential, but the experimental verification of the law, whatever it may be, would be exceedingly`

### 4. Why he never got it

> "the experimental verification of the law, whatever it may be, would be exceedingly difficult"

- cited as: `(1894, p. 213)`
- straddle: this ONE fragment sits on printed pp. 213-214 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches
- why: his own hedge on that law, in the next sentence; 'whatever it may be' is doing a lot of work, keep it. The fragment straddles printed pp. 213-214; cite one page, not a range
- check_quotes.py: exact match, ratio 1.0, printed p. 213 (this ONE fragment straddles printed pp. 213-214; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `...tential of the electric impulses. My opinion is that the heat as well as light effects produced should be proportionate, under otherwise equal conditions of test, to the product of frequency and square of potential, but the experimental verification of the law, whatever it may be, would be exceedingly`

## Printed p. 226 (scan file 244)

### 6. Where you see it now

> "it is a brush, formed at, or near, a single terminal in high vacuum"

- cited as: `(1894, p. 226)`
- why: what a plasma globe actually is, in his words, from the passage where he changes subject to the vacuum brushes ('I think it best at this juncture to bring before you a phenomenon...')
- check_quotes.py: exact match, ratio 1.0, printed p. 226
- raw OCR: `...e purely scientific investigator may perhaps appear more interesting than any of the results which I have the privilege to present to you this evening. It may be quite properly ranked among the brush phenomena— in fact, it is a brush, formed at, or near, a single terminal in high vacuum. In bulbs provided with a conducting terminal, though it be of FIG. 141. FIG. 142. aluminum, the brush -has but an ephemeral existence, and cannot, unfortunately, be indefinitely preserved in its most sensitive state, e...`

## Printed p. 227 (scan file 245)

### 6. Where you see it now

> "Figs. 143, 144 and 145 indicate different forms, or stages, of the brush"

- cited as: `(1894, p. 227)`
- why: the book's own description of the plates on printed pp. 227-228. Caption material for the figure task (feature-005/t6): the p. 228 plates are already article 02's, so read this sentence before choosing any crop
- check_quotes.py: exact match, ratio 1.0, printed p. 227
- raw OCR: `...It is of advantage to make the tube £-very thick, the hole FIG. 143. through it very small, and to blow the sphere * very thin. It is of the greatest importance that the sphere * be placed in the centre of the globe L. Figs. 143, 144 and 145 indicate different forms, or stages, of the brush. Fig. 143 shows the brush as it first appears in a bulb provided with a conducting terminal ; but, as in such a bulb it very soon disappears — often after a few minutes — I will confine myself to the description of the...`

## Printed p. 228 (scan file 246)

### 6. Where you see it now

> "it is usually sufficient to grasp the globe L with the hand"

- cited as: `(1894, p. 228)`
- why: the plasma-globe demonstration, exactly as it is done today: hold the globe in your hand to excite it. Printed p. 228, chapter XXVII
- check_quotes.py: exact match, ratio 1.0, printed p. 228
- raw OCR: `INVENTIONS OF NIKOLA TESLA. 142) to the terminal of the induction coil. To excite it, it is usually sufficient to grasp the globe L with the hand. An intense phosphorescence then spreads at tirst over the globe, but soon gives place to a white, misty light. Shortly afterward one may notice that the luminosity is unevenly distributed in the globe, and after passin...`

### 6. Where you see it now

> "the approach of the observer at a few paces from the bulb will cause the brush to fly to the opposite side, and if he walks around the bulb it will always keep on the opposite side"

- cited as: `(1894, p. 228)`
- why: the behaviour every plasma globe shows, measured in 1892: the discharge follows the observer's body. This is the sentence that makes the modern device legible
- check_quotes.py: exact match, ratio 1.0, printed p. 228
- raw OCR: `...indicated in Fig. 145, it may be brought to a state of extreme sensitiveness to electrostatic FIG. 144. FIG. 145. and magnetic influence. The bulb hanging straight down from a wire, and all objects being remote from it, the approach of the observer at a few paces from the bulb will cause the brush to fly to the opposite side, and if he walks around the bulb it will always keep on the opposite side. It may begin to spin around the terminal long before it reaches that sensitive stage. When it begins to turn around, principally, but also before, it is affected by a magnet, and at a certain stage it is susceptible to...`

## Printed p. 258 (scan file 276)

### 1. The stage moment

> "In one of the experiments this evening a brush was produced at the end of a wire"

- cited as: `(1894, p. 258)`
- why: he is describing a live demonstration, in the present tense, to an audience. This is what 'the stage moment' actually is: the sentence that puts the brush on a stage in front of the Institution of Electrical Engineers, London
- check_quotes.py: exact match, ratio 1.0, printed p. 258
- raw OCR: `...of gas at a high degree of incandescence in a glass vessel, it will always be necessary to keep the incandescent mass away from the glass ; that is, to confine it as much as possible to the central portion of the globe. In one of the experiments this evening a brush was produced at the end of a wire. The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand { Is it the less a flame b...`

### 1. The stage moment

> "The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand"

- cited as: `(1894, p. 258)`
- why: the brief's opening quote, pinned in the form that verifies: the print's spaced semicolon kept, and stopped before the question mark, which this scan reads as '{'. See the flags and rejected #1
- check_quotes.py: exact match, ratio 1.0, printed p. 258
- raw OCR: `...ssary to keep the incandescent mass away from the glass ; that is, to confine it as much as possible to the central portion of the globe. In one of the experiments this evening a brush was produced at the end of a wire. The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand { Is it the less a flame because it does not hurt my eyes by its brilliancy ? The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful. Were there means at hand...`

### 1. The stage moment

> "Is it the less a flame because it does not hurt my eyes by its brilliancy"

- cited as: `(1894, p. 258)`
- why: the second half of the same rhetorical move, on light instead of heat. Same '{' for '?' problem; put the question mark outside the quote marks
- check_quotes.py: exact match, ratio 1.0, printed p. 258
- raw OCR: `...ced at the end of a wire. The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand { Is it the less a flame because it does not hurt my eyes by its brilliancy ? The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful. Were there means at hand for`

### 1. The stage moment

> "The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful"

- cited as: `(1894, p. 258)`
- why: what he was trying to build, in his own one line: a lamp. Not a free-energy project - the anchor for section 5
- check_quotes.py: exact match, ratio 1.0, printed p. 258
- raw OCR: `...It did not emit much perceptible heat, nor did it glow with an intense light ; but is it the less a flame because it does not scorch my hand { Is it the less a flame because it does not hurt my eyes by its brilliancy ? The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful. Were there means at hand for`

### 4. Why he never got it

> "Were there means at hand for producing electric impulses of a sufficiently high frequency, and for transmitting them, the bulb could be done away with"

- cited as: `(1894, p. 258)`
- straddle: this ONE fragment sits on printed pp. 258-259 as a single run; check_quotes.py accepts a citation to either page, so cite one page only - '(1894, pp. ...)' never matches
- why: the counterfactual that answers brief 06 section 4 directly: the glass envelope was a workaround for apparatus he did not have. This fragment straddles printed pp. 258-259 as one fragment; cite p. 258 (or p. 259), never 'pp. 258-259'
- check_quotes.py: exact match, ratio 1.0, printed p. 258 (this ONE fragment straddles printed pp. 258-259; check_quotes.py accepts a citation to either page, so cite one page - a hyphenated range never matches its citation regex)
- raw OCR: `...t does not scorch my hand { Is it the less a flame because it does not hurt my eyes by its brilliancy ? The problem is precisely to produce in the bulb such a flame, much smaller in size, but incomparably more powerful. Were there means at hand for`

## Printed p. 259 (scan file 277)

### 4. Why he never got it

> "But as such means are not at disposal, it becomes necessary to place the terminal in the bulb and rarefy the air in the same"

- cited as: `(1894, p. 259)`
- why: the admission that follows it, on printed p. 259: 'such means are not at disposal'. This is the sentence section 4 is built on
- check_quotes.py: exact match, ratio 1.0, printed p. 259
- raw OCR: `...producing electric impulses of a sufficiently high frequency, and for transmitting them, the bulb could be done away with, unless it were used to protect the electrode, or to economize the energy by confining the heat. But as such means are not at disposal, it becomes necessary to place the terminal in the bulb and rarefy the air in the same. This is done merely to enable the apparatus to perform the work which it is not capable of performing at ordinary air pressure. In the bulb we are able to intensify the action to any degree — so far that the brush emit...`

## Printed p. 291 (scan file 309)

### 5. What the internet gets wrong

> "It would, of course, be out of question to transmit such impulses through a wire immersed in a gaseous medium, even if the wire were provided with a thick and excellent insulation, for most of the energy would be lost in molecular bombardment and consequent heating"

- cited as: `(1894, p. 291)`
- why: the energy bookkeeping in his words: a brush on a wire in air throws energy away. A 'cold fire' video is not getting something for nothing; it is a loss you can see. The form a draft would reach for ('it is out of the question') is not the print's - see rejected #8
- check_quotes.py: exact match, ratio 1.0, printed p. 291
- raw OCR: `...ue, and let the flow correspondingly diminish, then such impulses — variations merely of pressure, as it were — can no doubt be transmitted through a wire even if their frequency be many hundreds of millions per second. It would, of course, be out of question to transmit such impulses through a wire immersed in a gaseous medium, even if the wire were provided with a thick and excellent insulation, for most of the energy would be lost in molecular bombardment and consequent heating. The end of the wire connected to the source would be heated, and the remote end would receive but a trifling part of the energy supplied. The prime necessity, then, if such electric impulses are to be used, is to find...`

## Printed p. 322 (scan file 340)

### 5. What the internet gets wrong

> "they always exist, consuming energy and modifying the action of the apparatus"

- cited as: `(1894, p. 322)`
- why: the same point from the Philadelphia/St. Louis lecture: the brush discharge is a loss, always present, always consuming energy. Nothing in this volume supports a free-energy reading
- check_quotes.py: exact match, ratio 1.0, printed p. 322
- raw OCR: `322 INVENTIONS OF NIKOLA TESLA. they always exist, consuming energy and modifying the action of the apparatus. When intense, as they are at present, they produce ozone in great quantity, and also, as Professor Crookes has pointed out, nitrous acid. So quick is the chemical action that if a coil, such as this one, is worked for...`

## Printed p. 376 (scan file 394)

### 4. Why he never got it

> "Up to about 15,000 alternations per second in an experimental machine, the former plan may be followed, but a more efficient machine is obtained on the second plan"

- cited as: `(1894, p. 376)`
- why: the ceiling of the machinery, in numbers. Printed p. 376 is chapter XXIX, the editor's chapter on the high-frequency alternators (article 11's chapter): third person, the book describing his machine. Attribute it to the book, not to Tesla's own paper - see flags
- check_quotes.py: exact match, ratio 1.0, printed p. 376
- raw OCR: `...ction of these machines are of a mechanical as well as an electrical nature. The machines may be designed on two plans : the field may be formed either of alternating poles, or of polar projections of the same polarity. Up to about 15,000 alternations per second in an experimental machine, the former plan may be followed, but a more efficient machine is obtained on the second plan. In the machine above described, which was capable of running two arcs of normal candle power, the field was composed of a`

## Printed p. 381 (scan file 399)

### 4. Why he never got it

> "the field had 480 polar projections on each side, and from this machine it was possible to obtain 30,000 alternations per second"

- cited as: `(1894, p. 381)`
- why: the best he had: 30,000 alternations a second, against the 'many million times a second' (p. 168) or 'enormous frequencies' (p. 167) the flame needs. Same editorial chapter; Appendix A registers this fragment at p. 381
- check_quotes.py: exact match, ratio 1.0, printed p. 381
- raw OCR: `...s. The conductor D is cut entirely through at one point to form terminals, from which insulated conductors T are led through the shaft to collecting-rings v. In one type of machine of this kind constructed by Mr. Tesla, the field had 480 polar projections on each side, and from this machine it was possible to obtain 30,000 alternations per second. As the polar projections must necessarily be very narrow, very thin wires or sheets must be used to avoid the eddy current effects. Mr. Tesla has thus constructed machines with a stationary armature and rotating field,...`

## Rejected: considered and not carried forward

- ~~"The brush was a flame, a source of heat and light. It did not emit much perceptible heat, nor did it glow with an intense light; but is it the less a flame because it does not scorch my hand?"~~ (p. 258): the §9 brief 06 form of this line, and it FAILS: the printed page puts a space before the semicolon ('intense light ;'), and its question mark came out of this OCR as '{' ('scorch my hand { Is it the less'). The clean form with 'light;' still passes through check_quotes.py's space-ignoring index, but the trailing '?' never matches. Pin the run without the question mark and put the '?' outside the closing quote mark in the draft
- ~~"Is it the less a flame because it does not hurt my eyes by its brilliancy?"~~ (p. 258): same question-mark artefact: this scan gives 'its brilliancy ?' with a space before the mark, and the first one as '{'. Pin the words; keep the question mark outside the quotation marks
- ~~"but they would be so if the frequency and the potential would be sufficiently high"~~ (p. 166): the OCR reads 'if the frequency cmd the potential would be sufficiently high' (and -> cmd), so no clean form of this clause matches at all. Pin 'Certainly they are not as hot as a gas burner, but they would be so if the frequency' and finish the thought in our own words
- ~~"The air molecules are violently attracted and repelled, and by their impact produce such a powerful heating effect that a fire is started"~~ (p. 168): the OCR reads 'a lire is started' (fire -> lire), ratio 0.989, a FAIL. Pin up to 'such a powerful heating effect' if the lightning-fire passage is used at all; it is section 4/5 material, not section 2
- ~~"The possibility of bringing a body to incandescence in an exhausted globe, or even when not at all enclosed, would seem to afford a possible way of obtaining light effects"~~ (p. 169): the OCR reads 'light eifects' (effects -> eifects), ratio 0.991, a FAIL. The insulation sentence on the same page is the one this article needs
- ~~"In bulbs provided with a conducting terminal, though it be of aluminum, the brush has but an ephemeral existence"~~ (p. 226): the OCR prints 'the brush -has' with a stray hyphen, ratio 0.991, a FAIL, and the hyphen survives both normalisers. Do not quote this sentence; the 'single terminal in high vacuum' sentence pinned above carries the same section
- ~~"An intense phosphorescence then spreads at first over the globe, but soon gives place to a white, misty light"~~ (p. 228): the OCR reads 'at tirst' (first -> tirst), ratio 0.986, a FAIL. The two p. 228 quotes pinned above ('grasp the globe L with the hand', 'the approach of the observer...') verify exactly and do the same job
- ~~"it is out of the question to transmit such impulses through a wire immersed in a gaseous medium"~~ (p. 291): no match at all: the print has no 'the' - it reads 'It would, of course, be out of question to transmit such impulses...' (ratio 0.983 for the form with 'the'). §9 brief 06 does not quote this line, but a draft written from memory will get it wrong; the pinned form is in section 5 above
- ~~"cold flame / cold fire / cold, flame / not hot"~~ (not in this volume): 0 exact hits for each in the whole volume. The book's names for this phenomenon are 'the brush', 'the hot brush' (printed pp. 127 and 167 only), 'the streams' and 'a veritable flame'. The §9 title's 'Cold Flame' and 'Cold Fire' are ours and must stay outside quotation marks, and the article must say plainly that the 1894 text never uses the phrase
- ~~"corona / corona discharge / plasma / ioniz- / electron / ultraviolet"~~ (not in this volume): 0 exact hits for each in the whole volume ('electron' returns only fuzzy hits for 'electrode'). The modern vocabulary of gas discharge is not in this book: the plain-English ionisation/corona explanation of brief 06 section 2 is OURS, so it gets no quotation marks and no page cite, and any modern physics claim needs a modern source (§4.1)
- ~~"resembling in every particular a flame and giving light and heat, yet without a chemical process taking place"~~ (p. 127): printed p. 127 is chapter XXV, the editor's third-person introduction, not Tesla's lecture; it summarises the same Columbia College experiment, and it carries an OCR artefact ('jet' for 'yet'). Like article 05's p. 125 rejection: quote the lecture at pp. 166-167, not the recap at p. 127
- ~~"we are finally led to recognize, that since time immemorial we have, after all, always had " electric light and heat " at our disposal"~~ (p. 167): the print sets ' electric light and heat ' in double quotes with spaces inside them, so check_quotes.py's scanner splits the run at the inner marks and each half needs its own '(1894, p. 167)' within 400 characters. It is a rhetorical flourish, not a claim; the 'veritable flame' sentence is what section 3 needs. If used at all, print only 'since time immemorial we have, after all, always had' and paraphrase the rest
- ~~"In no branch of electric industry is an advance more desired than in the manufacture of light"~~ (p. 290): verifies exactly, but it is the London lecture's light-industry passage, not the cold-flame argument. Out of scope here (§1 scope discipline); it belongs to the light-production material at printed pp. 290-292
- ~~"It would enable us to obtain, by means of currents of very high frequencies, certainly 20 times, if not more, the quantity of light which is obtained in the present incandescent lamp by the same expenditure of energy"~~ (p. 258): verifies exactly, and it is a tempting number, but it is a lamp-economy claim whose whole argument is the incandescence-of-the-gas passage on printed p. 258. A 20x figure quoted without that argument is exactly the kind of overclaim this series exists to catch. If used, quote the argument with it
- ~~"The higher the incandescence, the quicker the mean vibration, the greater is the economy of the light production"~~ (p. 258): verifies, but it is the lamp argument again, and it reads like a thermodynamic law it is not. Not carried
- ~~"a frequency is conceivable - perhaps even obtainable - at"~~ (p. 166): verifies through the dash folding, but it ends on a preposition and the sentence runs onto printed p. 167. The two halves are pinned separately above ('The higher the frequency...' on p. 166; 'which practically the same molecules...' on p. 167)
- ~~"the brush has but an ephemeral existence, and cannot, unfortunately, be indefinitely preserved in its most sensitive state"~~ (p. 226): the ' -has' artefact again, and it is the start of that run. Not quotable; see rejected #6
- ~~"the glow of an incandescent lamp"~~ (p. 145): 'glow' occurs in the volume, but in the editor's introduction (printed p. 145) and about lamps, not about the brush. Do not build a 'glow' motif on it

## Flags for the writer (§3 quote policy, feature-005/t5)

- FOUR TEXTS, FOUR DATES, ONE ARTICLE. Printed pp. 166-171 are chapter XXVI, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF VERY HIGH FREQUENCY'; its footnote verifies exactly as typed - 'A lecture delivered before the American Institute of Electrical Engineers, at Columbia College, N. Y., May 20, 1891.' (printed p. 145; the chapter runs printed pp. 145-197). Printed pp. 226-229, 258-259 and 290-292 are chapter XXVII, 'EXPERIMENTS WITH ALTERNATE CURRENTS OF HIGH POTENTIAL AND HIGH FREQUENCY'; its footnote verifies exactly - 'Lecture delivered before the Institution of Electrical Engineers, London, February, 1892.' (printed p. 198; the chapter runs printed pp. 198-293). Printed p. 322 is chapter XXVIII, 'ON LIGHT AND OTHER HIGH FREQUENCY PHENOMENA', the Philadelphia and St. Louis lecture of February-March 1892 (printed pp. 294-373). Printed pp. 376 and 381 are chapter XXIX, the high-frequency alternator chapter, which is the EDITOR's text in the third person ('In one type of machine of this kind constructed by Mr. Tesla'), not a Tesla paper. Never write 'Tesla wrote in 1894': 1894 is the book, not the writing. Say which lecture a sentence comes from.
- THE STAGE MOMENT IS LONDON, NOT NEW YORK. §9 brief 06 section 1 quotes printed p. 258 and calls it 'the stage moment' without naming the text: it is the Institution of Electrical Engineers, London, February 1892 (ch. XXVII). Most of sections 2 and 3 are the Columbia College lecture, New York, May 20 1891 (ch. XXVI). These are two different papers a year apart; the article must not blend them into one 'Tesla on stage' scene, and each quote carries its own page for a reason.
- THE ALTERNATOR NUMBERS ARE THE BOOK'S, NOT TESLA'S. The 15,000 and 30,000 alternations-per-second figures (printed pp. 376, 381) come from chapter XXIX describing his machines in the third person. Cite them as the 1894 volume's account of the alternator, cross-checked against article 11 (11-tesla-high-frequency-alternator), which is built on that same chapter. Do not put them in his mouth, and do not use them to date the flame claim: the flame passages are 1891 and 1892.
- THE FLAME IS HOT. The §9 title is 'The Flame That Doesn't Burn: Tesla's Cold Fire', but the pinned text says the opposite three times: 'they are veritable flames, for they are hot' (p. 166), 'scorching hot air escapes at the top of the tube' (p. 167), 'Anything held within the brush is, of course, rapidly heated' (p. 167). What he actually claims is that it does not scorch the hand and does not dazzle the eye (p. 258) - cool beside a gas flame, not heatless. The article passes only if a reader comes away understanding that 'cold' is comparative.
- NO COLD FLAME IN THIS BOOK. 'cold flame' and 'cold fire' return 0 exact hits in the whole volume; so do 'corona', 'plasma', 'ioniz-', 'electron' (only fuzzy hits for 'electrode') and 'ultraviolet'. The book's words are 'brush', 'the hot brush' (printed pp. 127, 167), 'streams', 'a veritable flame'. So the title's 'Cold Flame'/'Cold Fire' stays outside quotation marks, and the modern explanation in section 2 is ours: no quotation marks, no page cite. 'ozone' is the one modern-sounding word that is his (printed pp. 127, 158, 171, 322).
- THE BRIEF'S QUOTE TEXT IS NOT THE PRINT'S. §9 brief 06 prints the p. 258 line with 'light;' and a '?', and the p. 167 line with a Unicode ellipsis. The print has 'intense light ;' (a space before the semicolon) and its question marks came out of this scan as '{' or ' ?'; the p. 167 sentence has em dashes, not an ellipsis. Use the forms in this file, not the brief's. The brief's p. 167 quote is also cut mid-sentence: it drops 'we have a possible way of producing' and 'and to accomplish this'.
- EM DASHES, AND THE TWO LEGAL FORMS OF THE p. 167 SENTENCE. The print sets 'by other than chemical means' off with em dashes. qa_page.py forbids em and en dashes in the article body, so the draft has exactly two safe forms: (a) the ASCII ' - ' form pinned here, which verifies exactly because grep_quote.py folds a typed ' - ' to the same normalised text as the print's em dash; or (b) the cut form 'a veritable flame, which would give light and heat without any material being consumed, without any chemical process taking place ... we only need to perfect methods of producing enormous frequencies and potentials', where check_quotes.py splits on the ASCII ' ... ' and each side verifies on printed p. 167. Do not print an em dash and do not print a Unicode ellipsis.
- OCR SPACING, NOT WORDING. The 1894 compositor puts a thin space before ';' and '?' in these passages ('intense light ;', 'fewer collisions ;'). The pinned forms keep that spacing so they pass as exact matches. If the draft prints the clean modern spacing ('light;'), check_quotes.py still passes it, through its space-ignoring index, and reports it as 'whitespace-only difference' - that is allowed, and it is not a licence to change any word. No [sic], no bracketed correction.
- CROSS-PAGE SENTENCES: CITE ONE PAGE, NEVER A RANGE. Three sentences here cross a folio: printed pp. 166->167 (the frequency thought), 213->214 (the verification hedge), 258->259 ('Were there means at hand...'). Where this file pins ONE fragment that straddles the break (pp. 213-214, 258-259), check_quotes.py accepts a citation to either page, so cite the page the sentence starts on. Where the file pins the two halves separately (pp. 166 and 167), each half must be cited to its own page. '(1894, pp. 258-259)' never satisfies check_quotes.py: its citation regex is '\(1894, p{1,2}s?\. ([\d,\s]+?)\)', which cannot read a hyphen.
- NESTED QUOTE MARKS. The print sets " electric light and heat " in double quotes with spaces inside them (printed p. 167). check_quotes.py's scanner splits a quoted run at those inner marks and checks the halves separately, each needing its own citation within 400 characters. Prefer not to quote that sentence (rejected #12). In any quote that does contain inner double quotes, put the citation immediately after the closing mark and put nothing between.
- WHAT HE HEDGES, AND WHAT HE DOES NOT. The pinned set keeps his conditionals in view: 'I have no doubt that if the potential could be made to alternate with sufficient rapidity and power' (p. 167), 'a possible way of producing' (p. 167), 'the experimental verification of the law, whatever it may be, would be exceedingly difficult' (p. 213), 'But as such means are not at disposal' (p. 259). He reports no working cold-flame lamp and no measured gain from one. The article's case - the idea was real, the apparatus was not - is carried by these sentences; no invented claim is needed.
- SAFETY (§4.1). The in-book basis for a caution is that these are coil and machine outputs at 'one or two hundred thousand volts' (p. 168) with 'scorching' air and a strong smell of ozone (pp. 167, 171). Use it for 'do not try this with mains-derived high voltage, and do not breathe the ozone', not for any health claim, and never imply the reader should repeat the experiment at home.
- HIS WORDING, NOT IDIOMATIC ENGLISH. The print reads 'It would, of course, be out of question to transmit...' (printed p. 291), with no 'the'; the modern idiom 'out of the question' is a 0.983 near-match and check_quotes.py FAILS it. The same trap runs through this pin: 'flamelike', 'ozonizing', 'brilliancy', 'rarefy the air in the same', 'such means are not at disposal'. Quote his wording or drop the quotation marks; never modernise a phrase inside them.
- MODERN CLAIMS NEED MODERN SOURCES. Corona rings on high-voltage lines, commercial ozone generators, plasma globes and today's 'cold fire' videos are all outside this volume (rejected #9, #10). If the draft keeps brief 06 sections 5 and 6, each modern sentence needs a cited modern source in the Sources block, kept visibly separate from the 1894 material, or the sentence is cut.
- VOICE RULE (§0.5, enforced by qa_page.py). No em or en dashes, no curly quotes, no Unicode ellipsis in the article body. Every cut in this pin is ASCII ' ... ' for that reason; keep it that way in the draft.

## Notes for the figure task (feature-005/t6)

- the §9 brief 06 figure ids name PRINTED pages, but the files on disk are named by SCAN FILE (printed = scan - 18, §0). The three candidates map to: p247-fig151 -> website/assets/tesla1894/p265-fig1-fig151.webp (scan 265 = printed 247); p228-fig144 -> p246-fig1-fig144.webp, superseded by p228-figs144-145.webp; p179-fig117 -> p197-fig1-fig117.webp, superseded by p179-figs116-117.webp. Use the current filenames.
- TWO OF THE BRIEF'S THREE CANDIDATES ARE ALREADY USED. index.json figures[] read on 2026-10-11: 1894_01 carries p179-figs116-117.webp, and 1894_02 carries p228-figs144-145.webp. §6.6's last rule says never reuse the same engraving on two articles unless the caption differs, and duplicate images across the series look thin. So the brief's p228-fig144 and p179-fig117 are blocked unless a genuinely different crop and caption are made.
- THE THIRD CANDIDATE DOES NOT SHOW A BRUSH. p265-fig1-fig151.webp is free, but the prose that names it is on printed p. 245: 'Fig. 151 illustrates a similar arrangement, with a large tube T protruding into the part of the bulb containing the refractory button' - a bulb construction detail. manifest_qc.csv row for it says 'Caption spans Figs.151-152; the radiant-discharge half is the useful part - split at gutter; dark plate - negate'. It is not a flame and not a brush; brief 06's instruction to 'verify which show brush discharge visually' answers no for this one.
- THE FIGURE THE TEXT ACTUALLY POINTS AT HAS NO CROP. The p. 166 sentence pinned above ends '(Fig. 110)' - 'two powerful brushes several inches long, nearly white at their roots, which in the dark bear a striking resemblance to two flames of a gas escaping under pressure'. That is the article's central image, and there is no p184-* file in website/assets/tesla1894/ and no manifest_qc.csv row for scan file 184: the extractor cut nothing from that page. feature-005/t6 must crop Fig. 110 from books/pdf-pages-tesla-1894/page-184.pdf, view it against the page, and add the manifest row. Caption from the p. 166 prose, never from a caption guess.
- FREE CROPS THAT DO SHOW THE PHENOMENA. (a) p186-fig1.webp (scan 186 = printed p. 168) is unused; the p. 168 prose calls it Fig. 111 - 'the rapid spinning round in a circle of the top of the filament, thus presenting the appearance of a luminous funnel, Fig. Ill' (both the reference and the printed caption OCR as 'Ill' for 111; 'luminous funnel' is 1 hit, printed p. 168). manifest_qc.csv describes the same file as 'a primary coil with a pear-shaped vacuum lamp glowing above it', which is not what the prose describes: verify against books/pdf-pages-tesla-1894/page-186.pdf before use and caption from the prose. (b) p244-fig1-fig141.webp (scan 244 = printed p. 226) and p245-fig1-fig141.webp (scan 245 = printed p. 227) are unused: these are the vacuum bulbs of Figs. 141-142, the apparatus behind the 'brush in high vacuum' passage quoted here, i.e. the plasma-globe ancestor. Both are dark plates; manifest_qc.csv says negate and split at the gutter.
- the book's own description of the brush-stage plates is pinned above: 'Figs. 143, 144 and 145 indicate different forms, or stages, of the brush' (printed p. 227). If 06 needs the plasma-globe look and the p. 228 plates are article 02's, either crop Fig. 143 (printed p. 227, scan file 245) or use a page-scan crop of the p. 228 paragraph ('it is usually sufficient to grasp the globe L with the hand'), which is §6.6 rule 4 - the words are the artefact. Article 03 did a page-scan crop of p. 486 and 05 of p. 394; follow their crop handling and credit line.
- the §6.6 ratio and placement rules apply as everywhere: figure 1 within the first three H2s, figure 2 mid-article, at most one patent plate per two 1894 engravings. This chapter has plenty of its own art (Figs. 110, 111, 141-145), so a patent plate should not be needed; if one is used anyway, confirm the number on patents.google.com and credit it 'US patent NNN,NNN (year), Nikola Tesla.' (§4.2).
- index.json has no row for tid 1894_06 yet (rows exist for hub, 01-05, 07, 09, 11). feature-005/t6 creates it, with figures[] verified:true only after the crop has been viewed against the scan page, and quotes_pages/quotes_note pointing at this file.

## Links (§5.2, for feature-005/t5 and t8)

- out-links per §5.2 row 06 and §9 brief 06: 7-interesting-facts-about-magnets.html, 01 (tesla-lit-lamps-without-wires.html) and 12 (tesla-glowing-tubes-vacuum.html). Checked in website/ on 2026-10-11: 7-interesting-facts-about-magnets.html and tesla-lit-lamps-without-wires.html both exist; tesla-glowing-tubes-vacuum.html does not (it is feature-013 territory, not rendered). So 06 -> 12 cannot be added in t8; record it in index.json the way article 05's pin records its deferred link to 10, and add it when 12 is written.
- in-links required by §5.2 row 06: from 01, from 12 and from the hub. 01 is rendered (feature-001) but cannot link to a page that did not exist when it was written; 12 and the hub are unwritten (feature-013, feature-012). The qa_page.py reciprocal gate ('>= 3 out-links to pages that link back') therefore cannot pass on 06 for any reason to do with 06: nothing on the site links to it yet. Record that in index.json the way article 11's entry records its backlink pass; do not pad 06 with off-map links to make the number.
- the natural bridge for brief 06 section 6 is 7-interesting-facts-about-magnets.html (the §5.2 row 06 target): corona rings, ozone smell and plasma globes are the everyday versions of what the 1894 brush is. Link it where the article turns to 'you have seen this', and do not repeat any product claim from it (§4.1).
- 01 is the right sibling for the 'lamps lit without wires' material: brief 06 section 4's point (the glass envelope was a workaround) is the same apparatus story 01 tells. Link 01 in that paragraph, not in the plasma-globe one.
- when feature-012 renders the hub, the hub card for 06 must not call this 'Tesla's cold flame' as if the phrase were his (see flags): the hub card wording is feature-012's job, and this pin is the record of what the phrase is not.
