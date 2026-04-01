# Research: .tasks-* Files in Graph View

## Config File Path
- **Location:** `.workgraph/config.toml`
- **Relevant section:** None for path filtering — viz filtering is handled in code, not config

## Pattern Matching Rules

### How Tasks Are Filtered in Graph View

The graph view filtering is implemented in `/home/erik/workgraph/src/commands/viz/mod.rs`:

1. **`is_system_task()`** (graph.rs:373-375): Returns `true` if task ID starts with `.`
   ```rust
   pub fn is_system_task(task_id: &str) -> bool {
       task_id.starts_with('.')
   }
   ```

2. **`is_internal_task()`** (viz/mod.rs:158-171): Returns `true` for tasks that are:
   - NOT coordinator/compact/user-board tasks (those are exempt)
   - AND either `is_system_task()` OR have `assignment`/`evaluation` tags
   
3. **`system_task_parent_id()`** (viz/mod.rs:203-222): Extracts parent ID from system task prefixes:
   ```rust
   ".assign-" | ".evaluate-" | ".verify-" | ".flip-" | ".respond-to-" | ".place-"
   "assign-" | "evaluate-" | "verify-" | "flip-" | "respond-to-"
   ```

4. **`filter_internal_tasks()`** (viz/mod.rs:229-269): Removes internal tasks and computes phase annotations

5. **`filter_internal_tasks_running_only()`** (viz/mod.rs:273-315): Keeps running internal tasks visible

### Key Observation: No `.tasks-*` Pattern Exists

The original task question mentions `.tasks-*` files appearing in graph view. After reviewing the codebase:

- **No `.tasks-*` pattern exists** in the workgraph filtering logic
- Tasks starting with `.` ARE system tasks (e.g., `.assign-foo`, `.evaluate-bar`)
- These ARE filtered out by default unless `--show-internal` is used

If `.tasks-*` files are appearing in the graph view, they would only show if:
1. They have task IDs that don't start with `.`
2. Or `--show-internal` flag is being used

## How to Modify Display Filters

### Option 1: Use CLI Flags
```bash
# Show all tasks including internal
wg viz --show-internal

# Show only running internal tasks
wg viz --show-internal-running-only

# Show all tasks in all states
wg viz --all

# Filter by status
wg viz --status in-progress
```

### Option 2: Modify Tags
In task definitions, add/remove tags to control visibility:
```toml
# Internal tasks have "assignment" or "evaluation" tags
tags = ["assignment"]  # Will be hidden in default viz
tags = ["my-task"]     # Will be visible
```

### Option 3: Modify System Task Prefixes (Code Change)
To change which patterns are treated as internal, edit `viz/mod.rs`:

```rust
// Current prefixes at line 204-215:
for prefix in &[
    ".assign-",
    ".evaluate-",
    ".verify-",
    ".flip-",
    ".respond-to-",
    ".place-",
    "assign-",
    "evaluate-",
    "verify-",
    "flip-",
    "respond-to-",
] {
    if let Some(rest) = id.strip_prefix(prefix) {
        return Some(rest.to_string());
    }
}
```

To add a new prefix (e.g., `.tasks-*`):
```rust
".tasks-",  // Add this line
```

### Option 4: Filter by Tags (Code Change)
In `viz/mod.rs`, the `VizOptions.tags` field supports AND semantics:

```rust
// Line 518-519 in viz/mod.rs
.filter(|t| options.tags.iter().all(|tag| t.tags.contains(tag)))
```

## Examples

### Example 1: Debug why a task is hidden
```bash
# Check if task is system task
wg show <task-id>

# Check if task has assignment/evaluation tags
# If task ID starts with . → hidden by default
```

### Example 2: Make internal tasks visible
```bash
# Temporarily show all internal tasks
wg viz --show-internal

# Or show only running ones
wg viz --show-internal-running-only
```

### Example 3: Filter to specific tag combinations
```bash
# Show only tasks with both "bug" and "urgent" tags
wg viz --tags bug --tags urgent
```

## Summary

- **Config file:** `.workgraph/config.toml` (no viz filtering settings)
- **Pattern matching:** Task ID prefix `.` or tags `assignment`/`evaluation`
- **Display filter examples:** Use `--show-internal`, `--all`, `--status`, `--tags`
- **Code changes:** Edit `viz/mod.rs:system_task_parent_id()` to add new patterns

## Related Source Files
- `/home/erik/workgraph/src/graph.rs` - `is_system_task()` (line 373)
- `/home/erik/workgraph/src/commands/viz/mod.rs` - filtering logic (lines 158-315)
- `/home/erik/workgraph/src/commands/viz/dot.rs` - DOT/Mermaid generation
- `/home/erik/workgraph/src/commands/viz/ascii.rs` - ASCII graph rendering
