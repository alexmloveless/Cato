# /writejson

Export the full conversation to a JSON file.

## Usage
- `/writejson <file>`

## Aliases
- `/wjson`

## Output
The JSON contains:
- `conversation`: message list (including the system prompt if present)
- `config`: minimal model settings (model, temperature, max_tokens)

## Examples
- `/writejson conversation.json`
- `/writejson exports:conversation.json`