# Exploring Codebases

Understand unfamiliar code before making changes.

## Workflow

1. **Discover repos**: read_file `gitnexus://repos` to find indexed repos
2. **Get overview**: read_file `gitnexus://repo/{name}/context` for codebase stats and staleness
3. **Query flows**: `gitnexus_query({query: "<concept>"})` to find related execution flows
4. **Dive into symbols**: `gitnexus_context({name: "<symbol>"})` for 360-degree symbol view
5. **Trace full flows**: read_file `gitnexus://repo/{name}/process/{name}` for step-by-step traces

## Resources

| Resource | What you get |
|----------|-------------|
| `gitnexus://repo/{name}/context` | Stats, staleness warning (~150 tokens) |
| `gitnexus://repo/{name}/clusters` | All functional areas with cohesion scores |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace |

If index is stale: `npx gitnexus analyze`
