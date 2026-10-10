#!/usr/bin/env python3
"""Regenerate quotes.md for this article (feature-004/t0).

Run: python3 new_content/1894-series/02-tesla-one-wire-power/gen_quotes.py

Every entry is re-grepped through books/tools/grep_quote.py at generation time:
if a quote does not verify on its stated printed page the script fails and
writes nothing. That is the whole point of the file (SERIES-PLAN-1894.md §8
step 2, §0 non-negotiable 2): the draft is written from this, not from memory.
"""
import re
import sys
from pathlib import Path

TOOLS = Path("/home/matt/projects/other/tesla-generator/books/tools")
sys.path.insert(0, str(TOOLS))
import grep_quote as gq  # noqa: E402

TXT = TOOLS.parent / "extracted" / "tesla-1894-plain.txt"
OUT = Path("/home/matt/projects/other/tesla-generator/new_content/1894-series/"
           "02-tesla-one-wire-power/quotes.md")

# (quote as it will be printed, printed page, brief section, why it is in the piece)
QUOTES = [
    ("A most curious feature of alternate currents of high frequencies and potentials "
     "is that they enable us to perform many experiments by the use of one wire only",
     232, "2. His statement",
     "the H1 promise, quoted in full and at the top of the second H2"),
    ("this motor rotates with one single connection between it and the generator",
     234, "3. What he actually did with it",
     "the demo he chose for the lecture: a coil, a copper disc, one wire. "
     "OCR glues 'itand'; see flags below"),
    ("the other terminals of motor and generator being insulated in space",
     234, "3. What he actually did with it",
     "the part people leave out: the second terminal is not missing, it is open"),
    ("To produce rotation it is generally (but not absolutely) necessary to connect "
     "the free end of the motor coil to an insulated body of some size",
     234, "4. Why it is not magic",
     "the size of the missing conductor is a design variable. OCR has a stray "
     "space inside '(but not absolutely )'; see flags below"),
    ("The experimenter's body is more than sufficient",
     234, "3. What he actually did with it",
     "one-line bridge to article 01 (lamps in hand), which is the same trick"),
    ("If an exhausted tube is put in series with the coil, the tube lights brilliantly, "
     "showing the passage of a strong current",
     234, "3. What he actually did with it",
     "the proof it is not a static effect: a real current flows through one wire"),
    ("the plate acts as a condenser in series with the coil",
     234, "4. Why it is not magic",
     "Tesla's own mechanism, in his words: series capacitance, not magic"),
    ("It counteracts the self-induction of the latter and allows a strong current to pass",
     234, "4. Why it is not magic",
     "why he picked a single-coil motor for the demo (high self-induction)"),
    ("it is not necessary to have even a single connection between the motor and generator, "
     "except, perhaps, through the ground",
     235, "4. Why it is not magic",
     "he pushes it to zero wires, and names the alternative path himself"),
    ("not only is an insulated plate capable of giving off energy into space, "
     "but it is likewise capable of deriving it from an alternating electrostatic field",
     235, "4. Why it is not magic",
     "the receive half of the same statement"),
    ("such \" no wire \" motors, as they might be called",
     235, "1. The rule you were taught",
     "his own label for it, quoted with the 1894 spacing inside the marks "
     "(see flags)"),
    ("Alternate currents, especially of high frequencies, pass with astonishing freedom "
     "through even slightly rarefied gases",
     235, "6. What the internet gets wrong",
     "the rarefied-air path he actually considered, before he drops the idea"),
    ("But such schemes are mentioned merely as possibilities",
     235, "6. What the internet gets wrong",
     "the sentence that kills the 'Tesla said no wires needed' version"),
    ("We shall have no need to transmit power at all",
     235, "6. What the internet gets wrong",
     "the sentence that gets quoted as prophecy; here it is with the sentence before it"),
    ("We may connect an insulated line to a source of such currents, we may pass an "
     "inappreciable current over the line, and on any point of the same we are able to "
     "obtain a heavy current, capable of fusing a thick copper wire",
     236, "3. What he actually did with it",
     "the one-wire distribution claim, with the inappreciable line current attached"),
    ("decompose a solution in any electrolytic cell by connecting only one pole of the "
     "cell to the line or source of energy",
     236, "3. What he actually did with it",
     "single-pole electrolysis, the second of the three demos"),
    ("Or we may, by attaching to the line, or only bringing into its vicinity, light up "
     "an incandescent lamp, an exhausted tube, or a phosphorescent bulb",
     236, "3. What he actually did with it",
     "the third demo, and the one the site's readers picture"),
    ("However impracticable this plan of working may appear in many cases, it certainly "
     "seems practicable, and even recommendable, in the production of light",
     236, "5. Tesla's own economic case",
     "where he thought one-wire was actually worth it: lighting, not power"),
    ("A perfected lamp would require but little energy, and if wires were used at all we "
     "ought to be able to supply that energy without a return wire",
     236, "5. Tesla's own economic case",
     "he admits the return wire and argues for dropping it, in the same breath"),
    ("It is now a fact that a body may be rendered incandescent or phosphorescent by "
     "bringing it either in single contact or merely in the vicinity of a source of "
     "electric impulses of the proper character",
     236, "3. What he actually did with it",
     "what he claims is settled, and how carefully he words it"),
    ("the most inefficient machine ever invented",
     236, "6. What the internet gets wrong",
     "the free-energy beat, one clause only; the full quote belongs to article 10"),
    ("the total energy lost must be proportionate to the product of the frequency and "
     "the square of the electric density",
     267, "6. What the internet gets wrong",
     "the loss law, and he flags it himself as unconfirmed"),
    ("currents of very high frequencies involve considerable waste when transmitted "
     "through conductors",
     267, "5. Tesla's own economic case",
     "the reason one wire can be cheaper: the copper is where the loss is"),
    ("it follows that, on the whole, it is better to employ one wire than two",
     267, "5. Tesla's own economic case",
     "the engineering conclusion, not a vision statement"),
    ("economical reasons will make it advisable to use only one wire, especially if the "
     "distances are great",
     267, "5. Tesla's own economic case",
     "the sentence the brief asks for, in full"),
    ("To reduce the dissipation, it is necessary to work with a small electric density",
     267, "4. Why it is not magic",
     "the cost side: high frequency is not free, it is traded against potential"),
    ("In all cases the insulated body serves to give off the energy into the surrounding "
     "space, and is equivalent to a return wire",
     184, "4. Why it is not magic",
     "the sentence that ends the 'no return path' reading; from the 1891 lecture"),
    ("a coil wound upon an iron core and traversed by an alternating current creates a "
     "moving field of force, capable of setting an armature in rotation",
     233, "3. What he actually did with it",
     "why the demo motor needs only one coil, and the honest 'must remain an open "
     "question' about why"),
]

# Quotes that were considered and must NOT be carried into the draft.
REJECTED = [
    ("In many respects this feature is of great interest", 232,
     "the OCR of the same line reads 'this feat, ure is of great interest' "
     "(ratio 0.882). The comma is an artefact of the scan, but §3 only allows "
     "silent normalisation of long-s and S-for-8, so do not print this fragment"),
    ("we may take another tube and it might not light", 288,
     "no match as typed. The real line is 'But I may take another tube and it "
     "might not light' (p. 288, ratio 1.0), which is the Philadelphia/St. Louis "
     "lecture and article 01's material, not this chapter. Exactly the kind of "
     "half-remembered quote §0 forbids: not used here"),
    ("the current might be converted to low tension and used to operate a motor or "
     "other device", 138,
     "verifies on p. 138, but that is the 1891 earth-return passage and belongs to "
     "article 04 (wireless power 1893). Link to 04 instead of quoting it here"),
]

FLAGS = [
    "p. 234 'between it and the generator': the OCR glues the words "
    "('itand'). grep_quote.py matches it fuzzily (ratio 0.954) and "
    "check_quotes.py will pass it as a space-normalised match. The printed "
    "page has the space; print it with the space.",
    "p. 234 '(but not absolutely)': the OCR carries a stray space before the "
    "closing bracket ('absolutely )', ratio 0.979). Same handling: print the "
    "clean form, the scan shows no gap.",
    "p. 236 'A perfected lamp would require but little energy': the capital A is "
    "genuine, it starts a sentence in the print. Quote it as it stands.",
    "p. 236 'the most inefficient machine ever invented': the print puts a space "
    "before the exclamation mark ('invented !'). Quote the words only and end "
    "the sentence outside the quotation marks. The full 'wheelwork of nature' "
    "passage is article 10's; here take the one clause and link to 10.",
    "p. 235 'such \" no wire \" motors': the 1894 text sets the phrase in spaced "
    "double quotes. Inside our own quotation marks use single quotes for the "
    "term and drop the 1894 spacing; do not add [sic].",
    "p. 267 the loss law: he adds 'but this law needs experimental "
    "confirmation' in the same sentence. Quote the law and keep that clause; "
    "it is the honest version.",
]

FIGURE_NOTES = [
    "the diagram the text calls Fig. 146 is the one-wire motor: 'Here, then, is "
    "a motor (diagrammatically illustrated in Fig. 146)' (printed p. 233), and "
    "the plate itself sits on printed p. 234 (scan file 252). The §9 brief 02 "
    "figure list names fig144 / fig151 / fig153 instead; Fig. 146 is the one "
    "that shows the experiment this article describes.",
    "the extractor crop for that plate is website/assets/tesla1894/p252-fig1.webp "
    "and carries no figure number in its name. Read the number off the scan "
    "before using it (the OCR of the printed caption reads 'PIG. 146.').",
    "brief 02's figure names are printed pages, the asset filenames are scan "
    "files: fig144 = printed p. 228 = p246-fig1-fig144.webp, fig151 = printed "
    "p. 247 = p265-fig1-fig151.webp, fig153 = printed p. 263 = "
    "p281-fig1-fig153.webp. All three are lamp sections, not one-wire circuits.",
]


def raw_window(body: str, quote: str, span: int = 220) -> str:
    """Show the scan's own text around a quote.

    grep_quote.py's raw_context anchors on the quote's first word, which lands
    on an earlier 'but'/'the' in a long page. Here the anchor is the longest
    literal run of the quote that the raw page really contains, so the printed
    fragment always sits inside the window.
    """
    words = quote.split()
    tries = [words] + [words[:n] for n in range(len(words) - 1, 2, -1)] \
        + [words[i:i + 4] for i in range(len(words) - 3)]
    for seq in tries:
        pat = re.compile(r"\s*".join(re.escape(w) for w in seq))
        m = pat.search(body)
        if m:
            a = max(0, m.start() - span)
            b = min(len(body), m.end() + span)
            return ("..." if a > 0 else "") + " ".join(body[a:b].split()) + \
                   ("..." if b < len(body) else "")
    return "(not located in the raw page text; see grep_quote.py context)"


def main():
    pages = gq.load_pages(TXT)
    index = gq.build_index(pages)
    raw_by_page = {fp: body for fp, pp, itext, body, _ in pages}
    rows, problems = [], []
    ntext = index[0]
    nospace = re.sub(r"\s+", "", ntext)
    for quote, page, section, why in QUOTES:
        needle = gq.normalise(quote)
        hits = gq.find_hits(index, needle)
        exact = [h for h in hits if h["ratio"] == 1.0]
        # A quote that matches only once whitespace is ignored is the same case
        # check_quotes.py allows and flags: the scan glues words together at line
        # ends where the printed page has the space. Record it as flagged, not failed.
        space_only = bool(re.sub(r"\s+", "", needle) in nospace)
        if not exact and not space_only:
            problems.append((quote, page, [(h["printed_page"], h["ratio"]) for h in hits[:3]]))
            continue
        pool = exact or [h for h in hits if h["printed_page"] == page] or hits
        hit = next((h for h in pool if h["printed_page"] == page), pool[0])
        if hit["printed_page"] != page:
            problems.append((quote, page, [("stated", page),
                                           ("found", hit["printed_page"])]))
            continue
        rows.append((quote, hit["printed_page"], hit["file_page"], section, why,
                     raw_window(raw_by_page[hit["file_page"]], quote),
                     "exact match, ratio 1.0" if exact else
                     "whitespace-only difference: the OCR spacing is not the "
                     "print's (words glued, or a stray space). Print the clean "
                     "form; check_quotes.py flags it the same way"))
    if problems:
        for q, p, h in problems:
            print(f"FAIL p.{p} {q!r} -> {h}", file=sys.stderr)
        sys.exit(1)

    by_page = {}
    for r in rows:
        by_page.setdefault(r[1], []).append(r)

    out = ["# Article 02 quote pin: tesla-one-wire-power.html",
           "",
           "SERIES-PLAN-1894.md §8 step 2. Every quote below was re-grepped from "
           "`books/extracted/tesla-1894-plain.txt` with `books/tools/grep_quote.py` "
           "on 2026-10-10 and is pinned to the printed page it was found on "
           "(printed page = scan file page - 18, §0). `article.md` for this page is "
           "written from this file; a quote that is not here does not go in the draft.",
           "",
           "Source: Martin (ed.), *The Inventions, Researches and Writings of Nikola "
           "Tesla*, D. Van Nostrand, 1894, archive.org item `inventionsresear00martiala`. "
           "The relevant text is chapter XXVII, 'Experiments of Alternate Currents of "
           "High Potential and Frequency' (London lecture, Feb 3 1892), printed pp. 232-237 "
           "and 267, plus one sentence from chapter XXVI (New York lecture, May 20 1891), "
           "printed p. 184.",
           "",
           f"Verified: {len(rows)} quotes, 0 failures. To re-check any single quote: "
           "`python3 books/tools/grep_quote.py \"<quote>\" --page <lo>-<hi>`, or regenerate "
           "this whole file: `python3 new_content/1894-series/02-tesla-one-wire-power/gen_quotes.py`.",
           ""]
    for page in sorted(by_page):
        rows_p = by_page[page]
        out += [f"## Printed p. {page} (scan file {rows_p[0][2]})", ""]
        for quote, _p, _fp, section, why, raw, how in rows_p:
            out += [f"### {section}", "",
                    f"> \"{quote}\"", "",
                    f"- cited as: `(1894, p. {page})`",
                    f"- why: {why}",
                    f"- grep_quote.py: {how}, printed p. {page}",
                    f"- raw OCR line: `{raw}`", ""]
    out += ["## Rejected: considered and not carried forward", ""]
    for quote, page, why in REJECTED:
        out += [f"- ~~\"{quote}\"~~ (p. {page}): {why}"]
    out += ["", "## Flags for the writer (§3 quote policy)", ""]
    out += [f"- {f}" for f in FLAGS]
    out += ["", "## Notes for the figure task (t2)", ""]
    out += [f"- {f}" for f in FIGURE_NOTES]
    out += ["", "## Links (§5.2, for t1 and t4)", "",
            "Out per the map: `diy-magnetic-generator.html`, "
            "`can-we-use-magnets-to-generate-electricity-a-magnetic-marvel.html`, "
            "`tesla-high-frequency-alternator.html` (11), and the hub when it exists. "
            "In per the map: 01, 04, 11, hub. None of those link to 02 yet, because 02 "
            "does not exist yet.", "",
            "The reciprocal gate (qa_page.py: >= 3 out-links to pages that link back) "
            "cannot pass on 02 from the §5.2 out-list alone: 11 links out to 02, so "
            "02 <-> 11 is one pair; 04 links out to 02 (feature-004/t5), so 02 -> 04 "
            "makes a second; 01 is listed as a required in-link for 02 but 01's own "
            "out-list does not name 02, so 01 needs an added out-link to 02 and 02 an "
            "out-link to 01 to make the third. That re-render of 01 and 11 is "
            "feature-009/t2's job; record it in index.json when 02 ships.", ""]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out))
    print(f"wrote {OUT} ({len(rows)} quotes across {len(by_page)} printed pages)")


if __name__ == "__main__":
    main()
