---
title: "Tesla's One-Wire Power: The Experiment Textbooks Skip"
slug: tesla-one-wire-power.html
pretty_slug: /tesla-one-wire-power
description: "Tesla's 1894 book prints a motor, a cell and a lamp worked from one wire. Here is what he claimed, what he measured, and what he said about the cost."
keywords: [one wire circuit, does electricity need a return path, tesla single wire, power a lamp with one wire, tesla one wire experiment]
date_published: "2026-10-20"
date_modified: "2026-10-20"
series_no: 2
primary_query: one wire circuit
tid: "1894_02"
og_image: assets/og/tesla-one-wire-power.webp
card_image: assets/tesla1894/p252-fig1.webp
card_alt: "1894 photograph, Fig. 146: a single coil on a long iron core between two stands, a copper disc on a pillar at one end, a lead to a transformer above, and a square plate suspended at the other side"
standfirst: "Tesla told the Institution of Electrical Engineers in 1892 that high-frequency currents let him work with one wire only, and the 1894 book prints the apparatus: a motor, a cell and a lamp, each on a single connection. It also prints his reason, and the reason is an engineering one."
figures:
  # Fig. 146 is the plate the text points to: 'Here, then, is a motor (diagrammatically
  # illustrated in Fig. 146)' (printed p. 233); the plate itself sits on printed p. 234.
  # The extractor file carries no figure number (p252-fig1.webp); the number was read off the
  # printed page per §6.6. The printed caption 'FIG. 146' sits in the text column, not in this
  # crop, and the plate is dark: t2 should test a negate/auto-level pass and re-check dims.
  - src: /assets/tesla1894/p252-fig1.webp
    alt: "1894 photograph, Fig. 146, printed p. 234: a single coil wound on a long iron core carried on two stands, a copper disc on a small pillar at the left end of the core, a lead from the coil up to a transformer at upper left, and a square metal plate suspended at the right"
    width: 725
    height: 627
    caption: "NOT YET VISUALLY VERIFIED (figure task t2). Fig. 146, printed p. 234: the motor described on pp. 233 to 235, photographed with the book's own labels for the transformer, the rotating disc, the iron core and the suspended plate. The plate is the insulated body the text says is wanted to produce rotation (1894, p. 234). Public domain."
  # Brief 02 lists fig144 / fig151 / fig153; all three are lamp sections (see quotes.md notes).
  # Figs. 144 and 145 are the pair whose text describes a bulb excited from one terminal, so
  # they carry the lighting passage. The crop holds both figures in one band; t2 may split it
  # at the whitespace gutter. Third figure candidate for t2: single-conductor transmission
  # patent, US 454,622 / 464,666 per §6.3, number not yet verified on patents.google.com.
  - src: /assets/tesla1894/p246-fig1-fig144.webp
    alt: "1894 photographs, Figs. 144 and 145, printed p. 228: two sections of an exhausted bulb hanging from a single lead, each showing a brush of luminous rays spreading through the globe from the terminal"
    width: 942
    height: 629
    caption: "NOT YET VISUALLY VERIFIED (figure task t2). Figs. 144 and 145, printed p. 228: the same class of exhausted bulb at two stages of being worked, the luminous brush changing shape as the current is passed. The text beside them says such a bulb is excited by grasping the globe with the hand (1894, p. 228). Public domain."
cta:
  text: "A one-wire circuit is a lesson in high-voltage engineering, not a way past the return conductor. If you are wiring a home generator instead, the plans we recommend come with a parts list and a straight answer about output."
  href_suffix: "1894_02"
pages_used: [184, 228, 232, 233, 234, 235, 236, 267]
faq:
  - q: "Does electricity need a return path?"
    a: "Always: a current needs a circuit, not necessarily two wires. At 50 or 60 Hz the second side of that circuit is a conductor, which is why house wiring has a neutral. At high frequency and high potential the second side can be the capacitance of a plate, a person, or the room. Tesla states it in the 1891 lecture: 'In all cases the insulated body serves to give off the energy into the surrounding space, and is equivalent to a return wire' (1894, p. 184). The return is there; it is simply not copper."
  - q: "Can you light a lamp from one wire?"
    a: "Yes, with a source of the right kind. The 1892 lecture lists it among the things one wire will do: 'Or we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent lamp, an exhausted tube, or a phosphorescent bulb' (1894, p. 236). In the motor demonstration of the same chapter, a tube put in series with a single-connected coil 'lights brilliantly, showing the passage of a strong current' (1894, p. 234). None of this works from a mains supply at 50 or 60 Hz."
  - q: "Did Tesla invent single-wire power transmission?"
    a: "He described systems worked from one conductor and argued for them on cost, not on mystery. In the 1894 book his case is arithmetic about loss: 'currents of very high frequencies involve considerable waste when transmitted through conductors', so 'it follows that, on the whole, it is better to employ one wire than two' (1894, p. 267). He is equally plain about working devices at a distance through air: 'But such schemes are mentioned merely as possibilities' (1894, p. 235)."
  - q: "Why does nobody distribute power on one wire today?"
    a: "Because the effect depends on frequency. The return current through the capacitance of a line and its surroundings is tiny at power frequencies, and Tesla's own reason for preferring one conductor was that high frequencies waste energy in the copper: 'the total energy lost must be proportionate to the product of the frequency and the square of the electric density' (1894, p. 267). He flagged that law himself as unproven, and the chapter that shows the motor turning on one wire is the same chapter that works out what the arrangement costs."
sources:
  - text: "Chapter XXVII, 'Experiments of Alternate Currents of High Potential and High Frequency', a lecture delivered before the Institution of Electrical Engineers, London, February 1892. The one-wire passages are printed pp. 232 to 237 of the 1894 edition; the passage on loss in transmission and the case for one conductor is printed p. 267"
  - text: "Chapter XXVI, 'Experiments with Alternate Currents of Very High Frequency and Their Application to Methods of Artificial Illumination', a lecture delivered before the American Institute of Electrical Engineers at Columbia College, N. Y., May 20, 1891. The sentence on the insulated body as a return path is printed p. 184"
  - text: "The chapter's account of an exhausted bulb worked from one terminal, with Figs. 144 and 145, printed p. 228"
  - text: "Every quote here was re-grepped from the text layer of our scan and pinned to its printed page before drafting; the register is new_content/1894-series/02-tesla-one-wire-power/quotes.md, re-runnable with books/tools/grep_quote.py"
---

**Standfirst.** Nikola Tesla told the Institution of Electrical Engineers in February 1892
that currents of high frequency and high potential "enable us to perform many experiments by
the use of one wire only" (1894, p. 232). The 1894 book prints what he meant: a motor, an
electrolytic cell and a lamp, each worked from a single connection. It also prints his reason
for doing it, and the reason is an engineering one.

## The rule, and the exception he found

Every reader was taught the same rule. Current goes out and comes back: a source, a load, and
two conductors between them. At 50 or 60 Hz, in a house or a distribution line, that is not a
convention. It is what makes the circuit close.

Tesla does not argue against the rule. He argues that at high frequency and high potential the
second conductor stops being a piece of copper, and that this is worth knowing because of what
it lets you build.

He also keeps the parts of the argument in order. First the demonstrations, with the apparatus
described and the currents described. Then a calculation about whether any of it is worth the
cost. The second part is the part most retellings drop.

## What he did with a single conductor

"A most curious feature of alternate currents of high frequencies and potentials is that they
enable us to perform many experiments by the use of one wire only." (1894, p. 232)

Then he lists the experiments, and the first is a line.

"We may connect an insulated line to a source of such currents, we may pass an inappreciable
current over the line, and on any point of the same we are able to obtain a heavy current,
capable of fusing a thick copper wire." (1894, p. 236)

That is a measurement claim, not a stage trick. The current travelling along the line is too
small to matter. The current you can draw from any point on it will melt a thick copper wire.
The line is not carrying the load; it is holding a high alternating potential, and the load
completes itself through the surroundings.

The second is chemistry, and he allows for an artifice in it. A solution can be decomposed in
an electrolytic cell "by connecting only one pole of the cell to the line or source of energy"
(1894, p. 236). The third is light: "Or
we may, by attaching to the line, or only bringing into its vicinity, light up an incandescent
lamp, an exhausted tube, or a phosphorescent bulb." (1894, p. 236)

He marks exactly which part of this he calls settled. "It is now a fact that a body may be
rendered incandescent or phosphorescent by bringing it either in single contact or merely in
the vicinity of a source of electric impulses of the proper character" (1894, p. 236). That is
a claim about lamps, worded as a claim about lamps, and it is the only one of the three he
puts in that form.

## The motor with one connection

The demonstration he chose for the lecture was a motor, and he picked its type on purpose. It
is the simplest thing that will turn: a coil on an iron core, a copper disc near it, and
nothing else in motion.

He is candid about not knowing why it works. Whether the effect comes from a true time lag in
the magnetisation of the core, or from eddy currents circulating in minute paths, he writes,
"must remain an open question" (1894, p. 233).

What he will assert is the result: "a coil wound upon an iron core and traversed by an
alternating current creates a moving field of force, capable of setting an armature in
rotation." (1894, p. 233)

![1894 photograph, Fig. 146, printed p. 234: a single coil wound on a long iron core carried on two stands, a copper disc on a small pillar at the left end of the core, a lead from the coil up to a transformer at upper left, and a square metal plate suspended at the right](/assets/tesla1894/p252-fig1.webp "NOT YET VISUALLY VERIFIED (figure task t2). Fig. 146, printed p. 234: the motor described on pp. 233 to 235, photographed with the book's own labels for the transformer, the rotating disc, the iron core and the suspended plate. The plate is the insulated body the text says is wanted to produce rotation (1894, p. 234). Public domain.")

Then the reason he chose this motor, which is the point of the passage. "this motor rotates
with one single connection between it and the generator", one terminal of the motor to one
terminal of a high-tension coil, "the other terminals of motor and generator being insulated in
space." (1894, p. 234)

One wire, and the disc turns. To make it turn reliably he adds one condition: "To produce
rotation it is generally (but not absolutely) necessary to connect the free end of the motor
coil to an insulated body of some size" (1894, p. 234).

And then: "The experimenter's body is more than sufficient." (1894, p. 234) That is the same
fact as the lamp held in a hand, and it is why the two demonstrations sit in the same chapter.

The proof that a real current is moving, rather than a field sitting there, is in the same
paragraph: "If an exhausted tube is put in series with the coil, the tube lights brilliantly,
showing the passage of a strong current." (1894, p. 234)

## Why it is not magic

Tesla supplies the mechanism himself, and it is a condenser. Instead of the experimenter, a
small sheet of metal hung on a cord does the same job: "the plate acts as a condenser in
series with the coil. It counteracts the self-induction of the latter and allows a strong
current to pass." (1894, p. 234)

That is a design trade, stated as one. A coil of high self-induction needs a smaller plate,
which is why a single coil on an iron core was chosen: it has a great deal of self-induction.
Add a closed secondary round that core and the trick gets harder, because the secondary cuts
off the primary's lines and lets only a minute current through.

The two sentences that end the mystery are in the 1891 lecture, four chapters earlier. "In all
cases the insulated body serves to give off the energy into the surrounding space, and is
equivalent to a return wire." (1894, p. 184)

Then he removes the last wire. With the motor standing in an alternating electrostatic field,
"it is not necessary to have even a single connection between the motor and generator, except,
perhaps, through the ground" (1894, p. 235).

The reason is the same property in reverse: "not only is an insulated plate capable of giving
off energy into space, but it is likewise capable of deriving it from an alternating
electrostatic field" (1894, p. 235). The catch is in the same sentence: "though in the latter
case the available energy is much smaller" (1894, p. 235).

## His own case for one wire

The argument for one conductor is not that copper is precious. It is that at high frequency the
copper is where the energy goes.

He builds a model of the loss from the bombardment of molecules at the surface of an
electrified body. His conclusion: "the total energy lost must be proportionate to the product
of the frequency and the square of the electric density" (1894, p. 267).

He adds, in the same sentence, that "this law needs experimental confirmation" (1894, p. 267).
Then the working rule: "To reduce the dissipation, it is necessary to work with a small
electric density" (1894, p. 267), the smaller the higher the frequency.

From that he draws the conclusion the series is named for. Since "currents of very high
frequencies involve considerable waste when transmitted through conductors", he writes, "it
follows that, on the whole, it is better to employ one wire than two" (1894, p. 267). And the
sentence the retellings skip: "economical reasons will make it advisable to use only one wire,
especially if the distances are great." (1894, p. 267)

One wire because two cost more, not because the second is unnecessary. That is an engineer's
case, and it is the opposite of the version in which the return path is simply waved away.

Where he thought it would actually pay is lighting. "However impracticable this plan of working
may appear in many cases, it certainly seems practicable, and even recommendable, in the
production of light." (1894, p. 236) A finished lamp would need very little energy, and "if
wires were used at all we ought to be able to supply that energy without a return wire."
(1894, p. 236)

![1894 photographs, Figs. 144 and 145, printed p. 228: two sections of an exhausted bulb hanging from a single lead, each showing a brush of luminous rays spreading through the globe from the terminal](/assets/tesla1894/p246-fig1-fig144.webp "NOT YET VISUALLY VERIFIED (figure task t2). Figs. 144 and 145, printed p. 228: the same class of exhausted bulb at two stages of being worked, the luminous brush changing shape as the current is passed. The text beside them says such a bulb is excited by grasping the globe with the hand (1894, p. 228). Public domain.")

## What the internet gets wrong

**That Tesla proposed power without wires and was ignored.** He raises the idea and closes it
himself. He allows that motors of this class might be worked at a distance, since "Alternate
currents, especially of high frequencies, pass with astonishing freedom through even slightly
rarefied gases" (1894, p. 235), and the upper strata of the air are rarefied.

Then, in the next sentence: "But such schemes are mentioned merely as possibilities."
(1894, p. 235)

The sentence that gets quoted on posters comes two lines later, and in the book it sits behind
that refusal: "We shall have no need to transmit power at all." (1894, p. 235) He is talking
about drawing energy from the environment, not about the one-wire circuit, and the paragraph
that follows is about Crookes's radiometer, the machine he rates "the most inefficient machine
ever invented" (1894, p. 236).

**That a one-wire circuit is a free-energy circuit.** It is a circuit with a harder supply, not
a source of something for nothing. The same chapter that shows the motor turning on one wire
also works out what the arrangement costs, in copper and in the air around the apparatus.

**That the return path is missing.** It is there. It is the capacitance of a plate, a person,
the room and, often, the earth. Tesla's own words for it are "equivalent to a return wire"
(1894, p. 184). An air return is a poor conductor. It is not no conductor.

## What this means for a home wiring project

None of this transfers to a house at 50 or 60 Hz. The capacitance that carries a return at tens
of thousands of alternations a second is far too small to carry an ampere at sixty.

That is why a generator, an inverter and a load are connected the ordinary way, with a neutral
and a protective conductor. [How a home generator system is actually wired](diy-magnetic-generator.html)
is the practical version of that sentence.

What the 1894 chapters do change is how the rule should be worded. The rule is not "current
needs two wires". It is that current needs a circuit, and the impedance of the second side of
that circuit is a design variable. At power frequencies the only good answer is a second
conductor; at high frequencies the room becomes a usable one.

For the machine that made these effects available, see
[Tesla's high-frequency alternators](tesla-high-frequency-alternator.html), with the pole counts
and the speeds.

For the same single-conductor trick done with a lamp in the hand instead of a motor on a bench,
see [Tesla's lamps lit without wires](tesla-lit-lamps-without-wires.html). For the honest
answer on what magnets can and cannot do in a generator you build, see
[can we use magnets to generate electricity](can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html).

{{FAQ}}

{{CTA}}

{{SOURCES}}
