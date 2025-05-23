# Context Facts

## Context Commands
- `create`: Make a new context file of a given type.
- `edit`: Open a context file in the default editor.
- `view`: Display the contents of a context file.
- `list`: Show files by type.
- `delete`: Remove a context file.
- Validation ensures only known types are allowed.

## Context Types
- `facts/`: Key concepts and reusable knowledge
- `decisions/`: Documented choices
- `goals/`: Project intentions and criteria
- `instructions/`: Style/formatting guides
- `summaries/`: Session summaries
- `archives/`: Full logs
- `personas/`: Perspective modifiers
- `timeline/`: Log of updates/events

## Context Workflow
1. Initialize a project with `context init [project]`
2. Add context using `create`, `edit`, or `summarize`
3. Load active context with `context load`
4. Maintain context with `update`, `archive`, or `clear`


Created on 2025-05-22T21:38:26.268301
