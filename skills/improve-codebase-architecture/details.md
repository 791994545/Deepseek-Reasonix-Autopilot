# Improve Codebase Architecture

Surface architectural friction and propose deepening opportunities.

## Key Concepts

- **Module** - anything with an interface and implementation
- **Depth** - leverage at the interface: lots of behavior behind a small interface
- **Seam** - where an interface lives; a place behavior can be altered without editing in place
- **Deletion test** - imagine deleting the module. If complexity vanishes, it was a pass-through

## Process

1. **Explore** - walk the codebase, note where you experience friction
2. **Present candidates** - numbered list of deepening opportunities with problem/solution/benefits
3. **Grilling loop** - walk the design tree with the user
