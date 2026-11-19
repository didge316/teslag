"""One definition of two malformed-markup defects, shared by the checker and the
fixer. Both tests/img-alt/inventory.py (the assertion) and tests/img-alt/
space-fix.py (the repair) import it, because two definitions of a defect class is
how a fix ships believing the class is empty.

It has been that way twice, and the second time is the reason this file is a
tokenizer and not a regex.

The first version of the shared definition was a regex:

    ("[^"]*"|'[^']*')(?=[a-zA-Z_:][-a-zA-Z0-9_:.]*=)

which reads as "a quoted value immediately followed by attribute-name=". It
counted 250 of them on ad559e9 and the repair inserted 250 spaces, and 52 of those
were inventions. The alternative `"[^"]*"` is free to start a "value" at the
*closing* quote of the previous attribute, so in

    <meta name="viewport" content="width=device-width, initial-scale=1" />

it happily matches `" content="` - a span that begins at the close of `viewport`
and ends at the open of `width`, with `width=` as the lookahead - and the repair
inserts a space inside the next attribute's value:

    <meta name="viewport" content=" width=device-width, initial-scale=1" />

Fifty-three pages shipped that in the working tree, in the `viewport` meta, and the
proof this repo was written to trust - "every rewritten file has an identical
non-whitespace byte sequence" - cannot see it, because a space inside a value is a
whitespace byte. The proof is not wrong; it is answering a different question. What
caught this was parsing the same two trees into (tag, attribute, value) triples and
comparing the triples, which is a different instrument and the one that asks the
question that matters here: *did the meaning of any attribute change*.

So: a quoted span only counts as a value when an `=` put it there. Everything below
follows from that one sentence, and the two numbers it produces on a clean checkout
of ad559e9 are 198 separators and 4 malformed quotations - not 250, which was the
number a bad definition reported and which is now only interesting as a fact about
bad definitions.

What the two defects are:

  count() / fix()      a quoted attribute value with no space before the next
                       attribute: `alt="Close-up of a permanent magnet"width="754"`
                       and `style="max-width: 30%;"alt="Blueprint"` are the same
                       mistake. The ticket named only the first pair, and a check
                       aimed at that pair cannot see the second.

  quote_defects()      an attribute value containing an unescaped `"`, which ends
                       the value where the browser thinks it ends and leaves bare
                       words inside the tag. Four of them are on this site, in the
                       og:title / twitter:title of the two "Massage" articles, and
                       they are reported, NOT repaired: an escaping fixer working
                       on a tag it cannot parse is a tool that invents content, and
                       the whole point of this module is that it knows the
                       difference between what it can prove and what it is guessing.

A start tag is read up to the first `>`, so a tag whose attribute value contains a
literal `>` is truncated here. That is also what the browser's tokenizer does with
these malformed tags, and neither count nor repair depends on seeing past it.
"""
import re

# A start tag.
TAG = re.compile(r"<[a-zA-Z][\w:-]*\b[^>]*>")
# One attribute: a name, optionally `=` and a value, where a quoted value is only
# recognised in the position a quoted value can legally occupy (this is the whole
# correction described in the docstring, and it is the only place the grammar of an
# HTML start tag is written down in this repo).
ATTR = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)(\s*=\s*("[^"]*"|'[^']*'|[^\s"'<>]+))?""")
_GAP = " \t\n\r"
_AFTER = " \t\n\r/>"


def _walk(body):
    """Yield (name, has_value, index_of_char_before_the_name) for each attribute
    the grammar recognises, walking a start tag in order. The bareword-with-no-value
    case is what both malformed classes look like from here, and the character
    before the name separates them: `width="754"` glued on after a closing quote is
    a missing separator, and `Massage` with nothing after it is a value that ended
    where an unescaped quote was."""
    i, n = 0, len(body)
    while i < n:
        while i < n and (body[i] in _GAP or body[i] in "/>"):
            i += 1
        if i >= n:
            break
        start = i
        m = ATTR.match(body, i)
        if not m or m.end() == i:
            j = re.search(r"[\s/]", body[i + 1:])
            i = n if not j else i + 1 + j.end()
            continue
        yield m.group(1), m.group(2) is not None, (body[start - 1] if start else "")
        i = m.end()
        if i < n and body[i] not in _AFTER:
            yield None, None, i          # marker: a separator is missing here


def _positions(body):
    """Offsets inside a start tag where a separator between attributes is missing.

    The walk consumes attributes in order; a violation is reported where one
    attribute ends and the next begins with no space between them. An unparseable
    fragment is skipped to the next boundary rather than cascading a false positive
    across the rest of the tag, and `quote_defects()` is what makes those cases
    visible instead of them being silently walked past.
    """
    return [x[2] for x in _walk(body) if x[0] is None]


def count(text):
    """Missing separators, counted inside start tags only: a quote in prose
    followed by `x=` is somebody's sentence, not markup."""
    return sum(len(_positions(m.group(0))) for m in TAG.finditer(text))


def fix(text):
    """Insert the missing separators. Returns (new_text, n_repairs).

    Repair positions are computed against the original text and applied back-to-
    front, so inserting one space never invalidates the offset of the next - and
    every position came out of `_positions()`, which can only land between two
    attributes it has parsed, which is what keeps this out of other people's
    attribute values.
    """
    total = 0

    def one(m):
        nonlocal total
        body = m.group(0)
        # A tag whose quotes are already broken cannot be repaired by inserting
        # spaces: the walk does not know where its values actually begin and end,
        # so a repair there is a guess about content. Those tags are counted and
        # left alone, and quote_defects() is what reports them.
        if any(name is not None and not has_value and before == '"'
               for name, has_value, before in _walk(body)):
            return body          # left for quote_defects() to report
        pos = _positions(body)
        if not pos:
            return body
        total += len(pos)
        for p in sorted(pos, reverse=True):
            body = body[:p] + " " + body[p:]
        return body

    return TAG.sub(one, text), total


def quote_defects(text):
    """Start tags whose quoted values contain an unescaped `"`.

    Detected from the walk: an attribute that came out with no value while the
    character before its name is a closing quote. `content="Tesla's High-Frequency "
    Massage" Cure of 1891"` reads to the parser as `content="Tesla's High-Frequency "
    ` followed by the valueless attribute `Massage` followed by a floating `" Cure of
    1891"`, so the page's og:title is truncated mid-word and everything after it in
    the tag is guesswork. A genuinely valueless attribute (`disabled`, `itemscope`)
    is preceded by whitespace and is therefore not flagged, and the missing-separator
    class is not flagged either because its bareword does carry a value - which is
    the whole reason both classes can be told apart from the same walk.

    Reported rather than repaired: see the module docstring.
    """
    out = []
    for m in TAG.finditer(text):
        hits = [name for name, has_value, before in _walk(m.group(0))
                if name is not None and not has_value and before == '"']
        if hits:
            out.append((m.group(0)[:200], hits))
    return out


def attrs(text):
    """The (tag, attribute, value) triples of a document, in order.

    This is the instrument that caught the bad definition: two trees can have
    identical non-whitespace bytes and identical `<img>` counts while an attribute
    *value* changed underneath them, and comparing triples is what asks the
    question that matters - did the meaning of any attribute change.
    """
    out = []
    for m in TAG.finditer(text):
        body = m.group(0)
        tag = re.match(r"<([\w:-]+)", body).group(1)
        i, n = body.index(tag) + len(tag), len(body)
        while i < n:
            if body[i].isspace():
                i += 1
                continue
            if body[i] in "/>":
                break
            m2 = ATTR.match(body, i)
            if not m2 or m2.end() == i:
                i += 1
                continue
            out.append((tag, m2.group(1), (m2.group(3) or "").strip()))
            i = m2.end()
    return out


_NAME_START = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*["']""")


def escape_inner_quotes(text):
    """Escape the unescaped `"` inside a malformed attribute value. Returns
    (new_text, n_tags_changed).

    Narrow on purpose, and it knows it. It handles exactly the shape
    `quote_defects()` detects: it finds the attribute whose opening quote precedes
    the offending bareword, takes the value to run from that quote to the *last*
    quote before the tag closes (which is where the author meant it to end), and
    escapes the inner quotes as `&quot;`. It is not an HTML escaper and would be
    wrong on a tag with two malformed values, which is why `count()` and
    `quote_defects()` must both be zero after it runs - the caller asserts that,
    and this site has exactly two such tags, both the og:title / twitter:title of
    tesla-high-frequency-massage.html, so "the assertion holds" is a fact about two
    tags rather than a hope about a general algorithm.

    Why repair this at all, when the module docstring says report-only: the
    consequence here is not theoretical and it is not invisible. Measured in a
    browser, that page's og:title and twitter:title both came through as
    `Tesla's High-Frequency ` - every social card for the article was truncated
    mid-phrase - while the <title> element was intact, because element text is not
    an attribute. A fix that is provably whitespace or provably escaping is fine;
    a fix that guesses at structure is not, and this one is checked by unescaping
    the result and requiring it to be the text that was there before.
    """
    changed = 0

    def one(m):
        nonlocal changed
        tag = m.group(0)
        defects = [name for name, has_value, before in _walk(tag)
                   if name is not None and not has_value and before == '"']
        if not defects:
            return tag
        bare = tag.index(defects[0])
        starts = [s for s in _NAME_START.finditer(tag) if s.end() < bare]
        if not starts:
            return tag
        attr = starts[-1]
        open_q = tag[attr.end() - 1]
        close = tag.rfind(open_q, 0, len(tag) - tag.rstrip().endswith(">") and len(tag.rstrip(" />")) or len(tag))
        close = tag.rfind(open_q, bare)
        if close < 0:
            return tag
        inner = tag[attr.end():close]
        if '"' not in inner and open_q == '"':
            return tag
        new_tag = (tag[:attr.end()] + inner.replace('"', "&quot;") + open_q + tag[close + 1:])
        changed += 1
        return new_tag

    return TAG.sub(one, text), changed


# ---------------------------------------------------------------------------
# The neighbours of the glued-attribute class.
#
# Item 5 is "fix the class, not the instance", and the class is *malformed start
# tags*. Stopping at the two shapes that were reported would be the same mistake
# that made this branch demote an accessibility bug to a formatting bug: it is the
# scope of the check, not its cleverness, that decides what gets found. So these
# four sit next to count() and quote_defects(), are run by inventory.py on every
# run, and are reported whether or not this branch fixes them. None of them is
# repaired here: a repair needs a reason, and the reason arrives with the finding.
# ---------------------------------------------------------------------------

def duplicate_attrs(text):
    """`<a href="/x" class="a" href="/y">`: the parser keeps the first and discards
    the rest, so a duplicate `href`, `alt` or `class` is content that silently does
    not exist. Same family as a glued attribute - two attributes failing to separate
    themselves properly - and invisible to a reader of the rendered page."""
    out = []
    for m in TAG.finditer(text):
        seen, dupes = {}, []
        for name, has_value, _ in _walk(m.group(0)):
            if name is None:
                continue
            key = name.lower()
            if key in seen:
                dupes.append(key)
            seen[key] = True
        if dupes:
            out.append((m.group(0)[:80], dupes))
    return out


# `unclosed_quotes()` used to live here. It was removed because it could only ever
# print 0: given `<img src="a.jpg alt="A photo">` - the textbook unclosed value - it
# found nothing, because `_walk` reads `a.jpg alt=` as a complete value and the
# function was looking for a value that never closed. A check that cannot fail is not
# a check, and the class it claimed to cover is already covered: quote_defects() fires
# on that exact input (it sees the bareword `A` where an attribute name cannot start),
# fires on the unescaped-inner-quote shape, and does not fire on `title="it's fine"`
# or on clean markup - the four cases in the other direction that make the difference
# between a detector and a decoration.

def duplicate_ids(text):
    """Two elements with the same `id` in one document. Only the first is reachable
    by `#anchor`, `label for=` or `aria-labelledby`, so the second one's label can
    end up on the wrong control and a jump link can land somewhere else entirely.
    Returns [(id, n, referenced_from_label_or_aria)]."""
    ids = {}
    for m in TAG.finditer(text):
        for name, has_value, _ in _walk(m.group(0)):
            if name and name.lower() == "id" and has_value:
                pass
    # values are not surfaced by _walk (it yields names only), so pull them directly
    got = re.findall(r"""\sid\s*=\s*"([^"]*)"|\sid\s*=\s*'([^']*)'""", text)
    for a, b in got:
        i = a or b
        if i:
            ids[i] = ids.get(i, 0) + 1
    dupes = {i: n for i, n in ids.items() if n > 1}
    hits = []
    for i, n in dupes.items():
        ref = bool(re.search(r"(?:for|aria-labelledby|aria-describedby|href)=[\"']#?" +
                             re.escape(i) + r"[\"']", text))
        hits.append((i, n, ref))
    return sorted(hits)


def unknown_entities(text):
    """`&copy` with no semicolon, or `&thing;` that is not an entity: the parser
    prints it literally, so this is text the author did not write. Only ampersands
    inside attribute values and text are looked at; `&#...;` numeric references are
    considered known."""
    known = ("amp", "lt", "gt", "quot", "apos", "nbsp", "mdash", "ndash", "copy",
             "reg", "trade", "hellip", "rsquo", "lsquo", "rdquo", "ldquo", "middot",
             "deg", "plusmn", "times", "divide", "laquo", "raquo", "sect", "para",
             "bull", "dagger", "larr", "rarr", "harr", "eacute", "egrave", "agrave",
             "ccedil", "uuml", "ouml", "auml", "ocirc", "ucirc", "icirc", "nbsp")
    bad, seen = [], set()
    for m in re.finditer(r"&([a-zA-Z][a-zA-Z0-9]{1,10})(;?)", text):
        name, semi = m.group(1), m.group(2)
        if name.lower() in known and semi:
            continue
        if not semi and name.lower() in known:
            # `&copy` without the semicolon resolves in HTML5 only in some contexts;
            # flag it, because the two renderings differ and the author meant one.
            key = name + " (no semicolon)"
        else:
            key = name + ";"
        if key in seen:
            continue
        seen.add(key)
        bad.append(key)
    return sorted(bad)
