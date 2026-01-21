# /writecode

Extract markdown code blocks from the last assistant response and write them to a file.

## Usage
- `/writecode <file>`

## Aliases
- `/wcode`

## Notes
- If the last assistant response contains multiple fenced code blocks, they are concatenated with a blank line between them.
- Supports code fences with metadata on the opening line (e.g. `python path=... start=...`).

## Examples
- `/writecode extracted.py`
- `/writecode docs:snippet.txt`