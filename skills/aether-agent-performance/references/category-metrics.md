# Category-Specific Metrics & Observations

Source synthesis from AIMultiple benchmarks (nearly 70 agents, >1,000 tasks across 12 studies, updated June 2026) plus CAT operational priorities. Use these as starting points when designing evaluations for a specific domain. Always re-measure under your own conditions.

## Browser / Computer-Use Agents

**Primary metrics**
- Task completion rate (form filling, booking, multi-step navigation)
- Navigation accuracy
- Time to complete
- Stability under UI change (most important production signal)

**Key findings**
- Visual perception is the dominant failure mode, not planning.
- Top models can reach ~90% on simple static tasks; many others stay below 45%.
- Capability is not a simple function of model size.
- Small UI changes frequently break workflows.
- Prefer stability-under-change over peak benchmark score when selecting for production.

## Remote Browser / Hosted Browser Agents

**Primary metrics**
- Task completion rate
- Latency
- Session stability / failure rate across repeated runs

**Key findings**
- Strong on repetitive, rule-based tasks.
- Sensitive to layout changes and dynamic elements.
- Higher latency due to rendering and interaction layers.
- Selection criterion should emphasise stability, not peak success.

## Search & Information Retrieval / Agentic Search / Deep Research

**Primary metrics**
- Answer accuracy
- Source grounding (claims linked to evidence)
- Hallucination rate
- Report accuracy vs latency / cost (for deep research agents)

**Key findings**
- Strong on simple lookups; degrades sharply on complex or multi-source questions.
- Best agentic search engines still only return correct data ~57% of the time on harder queries.
- More searches / longer reports / higher cost do not reliably improve accuracy.
- Tools that carefully read primary sources outperform broad searchers.
- Treat all outputs as starting points that require verification for high-stakes use.

## Mobile Agents

**Primary metrics**
- Task success rate on realistic device flows
- Cost per successful task

**Key findings**
- Category is still pre-production. Best observed success rates remain very low (single-digit percentages in recent tests).
- Environments are highly unpredictable.
- Cloud round-trips add latency.
- Improvements will come more from better scaffolding than from larger base models.

## Finance Agents & Spreadsheet / Excel Tools

**Primary metrics**
- Theory knowledge score (useful baseline only)
- Applied task success (analysis, interpretation, risk identification, multi-step calculations)
- Accuracy on workbook structure and dependencies

**Key findings**
- High theory scores do not predict applied performance.
- Multi-step calculations and understanding of workbook context remain weak points.
- Human validation is essential for complex financial modelling.
- Weight applied execution success far more heavily than knowledge benchmarks.

## Developer / Agentic CLI & Coding Agents

**Primary metrics**
- Code-generation accuracy
- Debugging success
- Command-execution reliability
- Tool-selection and planning quality
- Overall task success on realistic backend/frontend work

**Key findings**
- Higher token usage or slower speed does not guarantee better results.
- No current tool completes every realistic task.
- Cost and “newest model” status are poor predictors of strength.
- Verification of every non-trivial output remains mandatory.

## Cross-Cutting Observations

- Agents perform best in structured, relatively stable environments.
- Performance declines predictably with task complexity and environmental change.
- Human oversight remains necessary for high-stakes or open-ended work.
- The most useful production metric is often cost (or time) per successful, verified outcome — not raw success rate on a static test set.
