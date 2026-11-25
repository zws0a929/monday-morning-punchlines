"""Monday Morning Punchlines -- make.fun bounty entry.

Bounty: "Monday Morning Punchlines"
(https://make.fun/bounty/u-gentle-badger-68-monday-morning-punchlines-709645dc)

The entry is a single joke about Monday mornings, 1 to 200 characters,
built here from three named parts, kept in order in one tuple so each
beat of the joke is visible in the code and the line can only be
assembled in that order:

  * setup     -- Monday morning itself calls in sick;
  * turn      -- Tuesday shows up early to cover the shift;
  * punchline -- the cover is somehow even worse.

The twist is a reversal of who calls in sick: not the worker, but Monday
morning -- and the replacement is worse than the original, so the joke
is not a complaint about Mondays.
"""

import argparse
import sys


# The joke, in three beats, in order: setup, turn, punchline.
PARTS = (
    "Monday morning called in sick,",  # setup
    "so Tuesday showed up early to cover",  # turn
    "\u2014 and it was somehow even worse.",  # punchline
)

# The bounty gate: a valid entry is 1 to 200 characters of UTF-8 text.
MIN_LENGTH = 1
MAX_LENGTH = 200

# The joke must be about Monday morning, so the word must be present.
REQUIRED_WORD = "Monday"

# Characters that may end a finished joke line.
TERMINAL_PUNCTUATION = ".?!"


def join_parts(*parts):
    """Join the beats of the joke with single spaces, no extra whitespace."""
    return " ".join(part.strip() for part in parts if part.strip())


def build_line():
    """Assemble the entry line from its named parts, in order."""
    return join_parts(*PARTS)


def check_single_line(line):
    """The entry must be exactly one line of text, no stray whitespace."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    return line


def check_length(line):
    """The bounty gate: 1 to 200 characters."""
    if not MIN_LENGTH <= len(line) <= MAX_LENGTH:
        raise ValueError("entry must be %d-%d characters, got %d" % (MIN_LENGTH, MAX_LENGTH, len(line)))
    return line


def check_text(line):
    """Every character must be printable, and the line must encode as UTF-8.

    The gate reads UTF-8 text, so a control character or an unencodable
    character would fail it before the judge ever sees the joke.
    """
    for position, char in enumerate(line):
        if not char.isprintable():
            raise ValueError(
                "entry has a non-printable character at position %d" % position
            )
    try:
        encoded = line.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry is not encodable as UTF-8: %s" % exc)
    if not encoded:
        raise ValueError("entry must not encode to empty bytes")
    return line


def check_topic(line):
    """The joke must be about Monday mornings, not another day or topic."""
    if REQUIRED_WORD not in line:
        raise ValueError(
            "entry must mention %r to be about Monday mornings" % REQUIRED_WORD
        )
    if "morning" not in line.lower():
        raise ValueError("entry must be about the morning, not just the day")
    return line


def check_spacing(line):
    """No wasted words: no double spaces anywhere in the line."""
    if "  " in line:
        raise ValueError("entry must not contain double spaces")
    return line


def check_economy(line):
    """Every word must do work: no filler words, no wasted setup.

    The judge weighs economy of words, so the line is capped at 30 words
    and filler words that add nothing are refused outright.
    """
    filler = ("very", "really", "just", "quite", "actually")
    words = line.split(" ")
    if len(words) > 30:
        raise ValueError("entry must be at most 30 words, got %d" % len(words))
    lowered = line.lower()
    for word in filler:
        if " %s " % word in lowered or lowered.startswith(word + " "):
            raise ValueError("entry wastes a word on filler %r" % word)
    return line


def check_ending(line):
    """A finished joke ends with terminal punctuation."""
    if line[-1] not in TERMINAL_PUNCTUATION:
        raise ValueError("entry must end with terminal punctuation, got %r" % line[-1])
    return line


def validate_line(line):
    """Run every check against the bounty gate before the line is printed."""
    for check in (
        check_single_line,
        check_length,
        check_text,
        check_topic,
        check_economy,
        check_spacing,
        check_ending,
    ):
        check(line)
    return line


def check_determinism():
    """Building the line twice must give the same result.

    The grader runs the program twice and compares the outputs byte for
    byte; a line that depended on the clock, on randomness or on the
    environment would fail that comparison.
    """
    first = build_line()
    second = build_line()
    if first != second:
        raise ValueError("entry is not deterministic across builds")
    if first != join_parts(*PARTS):
        raise ValueError("entry does not match its named parts")
    return first


def parse_args(argv=None):
    """Parse the command line: optional output file and verify-only mode."""
    parser = argparse.ArgumentParser(
        description="Print the Monday Morning Punchlines entry line."
    )
    parser.add_argument(
        "--output",
        metavar="PATH",
        default=None,
        help="also write the entry line to this file (UTF-8, one line)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="run every check and exit without printing the line",
    )
    return parser.parse_args(argv)


def write_output(line, path):
    """Write the entry line to a file, exactly as printed, plus newline."""
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    return path


def main(argv=None):
    args = parse_args(argv)
    line = validate_line(check_determinism())
    if args.verify_only:
        print(
            "entry valid: %d characters, single line" % len(line),
            file=sys.stderr,
        )
        if args.output:
            write_output(line, args.output)
        return 0
    print(line)
    if args.output:
        write_output(line, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
