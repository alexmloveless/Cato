# /done

Mark an item as complete. Quick shortcut for `/update <id> -S done`.

## Usage

```
/done <id>
```

## Arguments

- `id` (required) - The item ID to mark as complete

## Examples

```
/done 1                         # Mark item #001 as done
/done 42                        # Mark item #042 as done
```

## Notes

- This is a convenience command equivalent to `/update <id> -S done`
- Completed items are hidden by default in `/list` output
- Use `/list -S all` or `/list -S done` to see completed items

## Aliases

- `/complete`
- `/finish`

## Related Commands

- `/list` - Display items with IDs
- `/update` - Update other item fields
- `/remove` - Delete item permanently
- `/clear` - Clear multiple done items
