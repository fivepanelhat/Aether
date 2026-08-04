# Performance Half-Life & ROI Forecasting

## Why Half-Life Matters

Observed agent performance in real environments follows an exponential decay pattern. An agent that achieves a high success rate on day 1 or on a static benchmark will typically see that rate decline as:

- Interfaces change
- Data distributions shift
- Edge cases accumulate
- Instructions or context drift
- Downstream systems evolve

The **performance half-life** is the point (measured in runs, calendar days, or environmental change events) at which the success rate falls to 50% of its measured baseline. Measuring half-life turns a one-time benchmark into a forecasting tool.

## Practical Measurement

1. Establish a clear baseline success rate under controlled but realistic conditions (minimum recommended sample: 20–30 tasks).
2. Continue measuring the same task distribution over time or under controlled variation.
3. Fit a simple decay curve or simply track the run/day at which success rate first drops below 50% of baseline.
4. Record the dominant failure modes that drove the decay.

Even a rough half-life estimate is more useful for planning than a single peak number.

## ROI Implications

- High initial success with short half-life → high ongoing maintenance cost (constant re-tuning, monitoring, human intervention).
- Moderate initial success with long half-life → often better unit economics.
- Cost-per-successful-task must be calculated only on the verified successful completions; failed runs still consume tokens and time.

When forecasting ROI for a new agent workflow:

1. Measure or estimate baseline success rate.
2. Estimate half-life under expected production conditions.
3. Project the cumulative successful completions over the desired time horizon.
4. Subtract expected human oversight and re-tuning cost.
5. Compare against the value of the completed work.

## CAT / Aether Usage Notes

- Surface half-life and cost-per-success in Night Cycle Morning Briefs for any production or pilot agent that has accumulated enough runs.
- Prefer skills and agents that demonstrate longer half-lives under the kinds of change expected in sovereign edge, farm, or Hub environments.
- When a measured half-life is unacceptably short, the first response should be decomposition + hybrid human checkpoints, not simply “use a bigger model”.
