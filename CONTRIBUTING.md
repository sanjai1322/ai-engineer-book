# Contributing

Thank you for considering a contribution.

## What belongs here

This repo is companion code for the book. Every file matches printed code, so
changes fall into a few categories:

1. **Bug fixes** — if a script does not run on a clean install, that is a bug.
   Open an issue with the error output and which file you ran.
2. **Typos and formatting** — small fixes to READMEs or comments.
3. **Missing error handling** — if a failure produces a stack trace instead of a
   helpful message, that counts.

## What does not belong here

- Refactoring the code into classes, frameworks, or different patterns. The
  book teaches the primitives deliberately.
- Adding LangChain, LlamaIndex, or any abstraction layer.
- Rewriting examples to use a different model or provider.
- Adding type hints, linters, or formatters not shown in the book.

## How to contribute

1. Fork the repo
2. Create a branch (`fix/week-05-sort-error`)
3. Make your change
4. Test it: `python <file>.py` should run cleanly with a valid API key
5. Open a pull request with a clear description of what broke and how you fixed it

## Style

Match the book: plain English, no hype, no emoji in code comments.
Explain *why* when it is not obvious. Say nothing when it is.

## Security

Never commit API keys, even partial ones. If you see one in the history,
open an issue immediately.
