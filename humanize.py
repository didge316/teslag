#!/usr/bin/env python3
"""
Humanize Phase 1 articles using the Humanizer skill rules.
Focus: remove em dashes, AI vocabulary, promotional language, filler patterns.
"""

import re
from pathlib import Path

BASE = Path("/home/matt/projects/other/tesla-generator/new_content/phases/phase-1-foundation")

# AI vocabulary to replace
AI_WORDS = {
    "crucial": "important",
    "delve": "look into",
    "delving": "looking into",
    "showcase": "show",
    "showcasing": "showing",
    "tapestry": "",
    "testament": "proof",
    "testament to": "proof of",
    "underscores": "shows",
    "underscore": "shows",
    "underscoring": "showing",
    "highlights": "shows",
    "highlight": "shows",
    "highlighting": "showing",
    "emphasizes": "stresses",
    "emphasize": "stress",
    "emphasizing": "stressing",
    "enhance": "improve",
    "enhancing": "improving",
    "fostering": "building",
    "cultivating": "growing",
    "garner": "get",
    "garnered": "got",
    "pivotal": "key",
    "pivotal moment": "key moment",
    "landscape": "situation",
    "intricate": "complex",
    "intricacies": "details",
    "valuable": "useful",
    "vibrant": "active",
    "enduring": "lasting",
    "additional": "more",
    "additionally": "also",
    "align with": "match",
    "key role": "main role",
    "key factor": "main factor",
    "key takeaway": "main point",
    "game-changer": "big difference",
    "deep dive": "detailed look",
    "at the end of the day": "overall",
    "when it comes to": "for",
    "in a world where": "",
    "moving forward": "going forward",
    "navigate": "handle",
    "unpack": "break down",
    "straightforward": "simple",
    "make no mistake": "",
    "let me be clear": "",
    "lean into": "use",
    "double down": "focus on",
    "circle back": "return to",
    "on the same page": "in agreement",
    "it turns out": "actually",
    "stand as": "are",
    "serves as": "is",
    "boasts": "has",
    "features": "has",
    "represents": "is",
    "marks": "is",
    "reflects": "shows",
    "symbolizing": "which means",
    "contributing to": "adding to",
    "ensuring": "making sure",
    "encompassing": "including",
    "exemplifies": "shows",
    "commitment to": "focus on",
}

# Filler phrases to remove/shorten
FILLER_PHRASES = {
    "In order to": "To",
    "Due to the fact that": "Because",
    "At this point in time": "Now",
    "In the event that": "If",
    "The system has the ability to": "The system can",
    "It is important to note that": "",
    "It is worth noting that": "",
    "It should be noted that": "",
    "For the purpose of": "For",
    "In terms of": "In",
    "With regard to": "About",
    "As far as ... is concerned": "",
    "From a ... perspective": "From the ... point of view",
    "A total of": "",
    "The majority of": "Most",
    "A number of": "Several",
    "A wide range of": "Many",
    "A variety of": "Different",
    "It can be seen that": "",
    "It is clear that": "",
    "It is evident that": "",
    "One can see that": "",
    "There is no doubt that": "",
    "It is widely believed that": "",
    "Studies show that": "Research shows",
    "Experts agree that": "Most experts say",
    "It is often said that": "",
    "As a matter of fact": "",
    "In fact": "Actually",
    "In other words": "Put simply",
    "That is to say": "Which means",
    "For example": "Like",
    "For instance": "Like",
    "Namely": "Such as",
    "To put it simply": "Simply",
    "To begin with": "First",
    "Last but not least": "Finally",
    "On the one hand": "One side",
    "On the other hand": "The other",
    "In conclusion": "",
    "To summarize": "In short",
    "In summary": "In short",
    "Overall, it can be said": "",
    "In general": "Generally",
    "As a whole": "Overall",
    "By and large": "Mostly",
    "For the most part": "Mostly",
    "More or less": "About",
    "Roughly speaking": "About",
    "At present": "Now",
    "At the moment": "Now",
    "So far": "Up to now",
    "Up until now": "Until now",
    "In recent years": "Lately",
    "Over the years": "Over time",
    "Over the past few years": "Recently",
    "In the near future": "Soon",
    "In the near term": "Soon",
}

# Signposting phrases to remove
SIGNPOSTS = [
    "Let's dive in",
    "Let's explore",
    "Let's break this down",
    "Here's what you need to know",
    "Now let's look at",
    "Without further ado",
    "Let's take a look",
    "Let me tell you",
    "Here's the thing",
    "Here's how it works",
    "Here's why",
    "Here's what happens",
    "Here's the deal",
    "Let's get into it",
]

# Reassurance kickers to remove
REASSURANCE = [
    "And that's okay.",
    "And that's fine.",
    "There's nothing wrong with that.",
    "No shame in...",
    "You're not alone",
    "It's completely normal",
]

# Sentence opener tics
OPENER_TICS = [
    "So, ",
    "Look, ",
]

# Adverb openers
ADVERB_OPENERS = [
    "Interestingly, ",
    "Importantly, ",
    "Notably, ",
    "Crucially, ",
    "Essentially, ",
    "Ultimately, ",
    "Surprisingly, ",
    "Remarkably, ",
    "Significantly, ",
    "Fundamentally, ",
]

def humanize_text(text):
    """Apply humanization rules to text."""
    result = text
    
    # 1. Remove em dashes — replace with commas or periods
    # Replace em dashes with commas first, then clean up double commas
    result = re.sub(r'\s*—\s*', ', ', result)
    result = re.sub(r',\s*,', ', ', result)
    # Replace remaining em dashes
    result = result.replace('—', ',')
    result = result.replace('–', '-')
    
    # 2. Remove AI vocabulary
    for word, replacement in AI_WORDS.items():
        pattern = r'\b' + re.escape(word) + r'\b'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # 3. Remove filler phrases (case-insensitive, whole phrase)
    for phrase, replacement in FILLER_PHRASES.items():
        pattern = r'\b' + re.escape(phrase) + r'\b'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # 4. Remove signposting phrases (case-insensitive)
    for phrase in SIGNPOSTS:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    
    # 5. Remove reassurance kickers
    for phrase in REASSURANCE:
        pattern = r'\b' + re.escape(phrase) + r'\b'
        result = re.sub(pattern, '', result, flags=re.IGNORECASE)
    
    # 6. Remove sentence opener tics
    for tic in OPENER_TICS:
        result = re.sub(r'(^|\n\s*)' + re.escape(tic), r'\1', result)
    
    # 7. Remove adverb openers
    for opener in ADVERB_OPENERS:
        result = re.sub(r'(^|\n\s*)' + re.escape(opener), r'\1', result)
    
    # 8. Remove excessive hedging
    result = re.sub(r'could potentially', '', result)
    result = re.sub(r'potentially', '', result)
    result = re.sub(r'it could be argued that', '', result)
    result = re.sub(r'it may be', 'it is', result)
    result = re.sub(r'it might be', 'it is', result)
    result = re.sub(r'arguably', '', result)
    result = re.sub(r'perhaps', '', result)
    result = re.sub(r'maybe', '', result)
    
    # 9. Remove generic positive conclusions
    result = re.sub(r'The future looks bright', '', result)
    result = re.sub(r'Exciting times lie ahead', '', result)
    result = re.sub(r'This represents a major step', '', result)
    result = re.sub(r'a major step', '', result)
    result = re.sub(r'a significant step', '', result)
    
    # 10. Remove rhetorical questions answered immediately
    # Pattern: "What is X? It is..." -> "X is..."
    result = re.sub(r'What (is|are|does|do|can|will|would) (.*?)\? \1 \2', r'\2', result, flags=re.IGNORECASE)
    
    # 11. Remove "It is worth mentioning" type phrases
    result = re.sub(r'It is worth mentioning that ', '', result)
    result = re.sub(r'One thing worth noting is that ', '', result)
    result = re.sub(r'Another important point is that ', '', result)
    
    # 12. Remove "In today's ..." phrases
    result = re.sub(r"In today's .*? landscape, ", '', result)
    result = re.sub(r"In today's .*? world, ", '', result)
    
    # 13. Clean up double spaces and spaces before punctuation
    result = re.sub(r'  +', ' ', result)
    result = re.sub(r' \.', '.', result)
    result = re.sub(r' ,', ',', result)
    result = re.sub(r' !', '!', result)
    result = re.sub(r' \?', '?', result)
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)
    
    # 14. Remove "Additionally" at start of sentences
    result = re.sub(r'\nAdditionally, ', '\nAlso, ', result)
    
    # 15. Remove "In conclusion" at start
    result = re.sub(r'\nIn conclusion, ', '\n', result)
    
    # 16. Remove "Overall" at start of sentences (when used as filler)
    result = re.sub(r'\nOverall, ', '\n', result)
    
    # 17. Remove "In short" at start
    result = re.sub(r'\nIn short, ', '\n', result)
    
    # 18. Remove "Put simply" at start
    result = re.sub(r'\nPut simply, ', '\n', result)
    
    # 19. Remove "Actually" at start
    result = re.sub(r'\nActually, ', '\n', result)
    
    # 20. Remove "Also," at start of sentences (when redundant)
    result = re.sub(r'\nAlso, ', '\n', result)
    
    # 21. Remove "Simply" at start
    result = re.sub(r'\nSimply, ', '\n', result)
    
    # 22. Remove "Generally" at start
    result = re.sub(r'\nGenerally, ', '\n', result)
    
    # 23. Remove "Mostly" at start
    result = re.sub(r'\nMostly, ', '\n', result)
    
    # 24. Remove "About" at start of sentences
    result = re.sub(r'\nAbout ', '\n', result)
    
    # 25. Remove "Like" at start of sentences
    result = re.sub(r'\nLike ', '\n', result)
    
    # 26. Remove "Which means" when it starts a sentence
    result = re.sub(r'\nWhich means ', '\n', result)
    
    # 27. Remove "Also" at start
    result = re.sub(r'\nAlso ', '\n', result)
    
    # 28. Remove "Also," at start
    result = re.sub(r'\nAlso, ', '\n', result)
    
    return result

def humanize_article(folder_name):
    """Humanize a single article."""
    article_path = BASE / folder_name / "article.md"
    if not article_path.exists():
        return False
    
    with open(article_path, 'r') as f:
        content = f.read()
    
    new_content = humanize_text(content)
    
    with open(article_path, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    folders = [d.name for d in BASE.iterdir() if d.is_dir()]
    print(f"Humanizing {len(folders)} articles...\n")
    
    for folder in folders:
        if humanize_article(folder):
            # Count words after humanizing
            article_path = BASE / folder / "article.md"
            with open(article_path, 'r') as f:
                words = len(f.read().split())
            print(f"  ✅ {folder}: {words} words")
        else:
            print(f"  ⏭️ {folder}: no article.md")

if __name__ == "__main__":
    main()
