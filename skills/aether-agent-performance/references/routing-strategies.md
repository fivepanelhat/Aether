# Routing Strategies Summary

See the companion skill `aether-agent-routing` for full patterns, design rules, and CAT-specific escalation ladders.

Key empirical takeaway (Arize / Fireworks, July 2026, 2,400 runs):

- Oracle routing: highest coverage at lowest cost-per-successful-task.
- Practical escalation (cheap → mid → frontier, stop on first pass) recovers most of the oracle gain while remaining deployable.
- Naive escalation through every available model is often worse than no routing.

Always evaluate routing changes on cost-per-successful-task, not average cost per attempt.
