# Durable Runtime - Discovery & Classification Prompt

## System Prompt

You are a technical analyst specializing in durable execution and workflow runtime systems. Your task is to discover and classify Durable Runtime tools based on technical merit, separating substantive signal from marketing noise.

## User Prompt

Using your knowledge of recent developments in Durable Runtimes (workflow engines, durable execution, fault-tolerant computing, long-running processes), search for and analyze tools being discussed in this space.

### STEP 1 - DISCOVER

Search your knowledge for Durable Runtime tools being discussed. Look for:
- New releases and version updates
- Technical announcements and architecture details
- Benchmark publications and reliability data
- Production deployments and case studies
- Community discussions with technical depth

### STEP 2 - CLASSIFY

For each discovered tool, classify as **SIGNAL** or **NOISE** using these criteria:

#### SIGNAL Criteria (worth evaluating):
- **Durability guarantees**: Published SLAs, exactly-once semantics, consistency models
- **Cold-start benchmarks**: Measured startup latency with methodology
- **Checkpoint/recovery**: Documented state persistence and replay mechanisms
- **Fault tolerance**: Automatic retries, failure handling, dead letter queues
- **Production evidence**: Named customers, scale metrics, reliability data

#### NOISE Criteria (skip):
- **Impossible claims**: "Zero cold starts", "infinite scale", "100% uptime"
- **No SLAs**: Missing durability or availability guarantees
- **Marketing-only**: Impressive claims without technical documentation
- **Waitlist/private beta**: No public access or verifiable benchmarks
- **Vague architecture**: No explanation of how durability is achieved

### Durable Runtime Specific Evaluation Points

When analyzing Durable Runtime tools, specifically look for:

1. **Durability guarantees**:
   - Exactly-once vs at-least-once semantics
   - State consistency model (strong, eventual)
   - Data persistence strategy (event sourcing, snapshots)

2. **Performance characteristics**:
   - Cold-start latency (P50, P95, P99)
   - Warm execution overhead
   - Throughput limits and scaling behavior

3. **Failure handling**:
   - Automatic retry policies
   - Timeout configuration
   - Dead letter queue support
   - Manual intervention capabilities

4. **State management**:
   - Checkpoint frequency and size limits
   - Long-running workflow support (hours/days/weeks)
   - State versioning and migration

5. **Operational concerns**:
   - Monitoring and observability
   - Debugging failed workflows
   - Deployment and versioning strategies

### Output Format

Return a JSON array with your findings. Each item must conform to this schema:

```json
[
  {
    "tool_name": "string - Name of the tool/technology",
    "classification": "signal" | "noise",
    "confidence_score": 1-100,
    "technical_insight": "string - Specific technical details found (benchmarks, SLAs, architecture)",
    "signal_evidence": ["array of strings - concrete evidence supporting signal classification"],
    "noise_indicators": ["array of strings - specific hype patterns or missing data"],
    "architectural_verdict": true | false
  }
]
```

### Rules

1. Only include tools with enough information to make a classification
2. `confidence_score` should reflect the quality and quantity of evidence
3. `technical_insight` must contain specifics, not marketing copy
4. For SIGNAL: `signal_evidence` should have 2-4 concrete items, `noise_indicators` empty
5. For NOISE: `noise_indicators` should have 2-4 specific issues, `signal_evidence` empty
6. `architectural_verdict`: true = recommend for technical evaluation, false = skip

### Example Output

```json
[
  {
    "tool_name": "Temporal.io",
    "classification": "signal",
    "confidence_score": 94,
    "technical_insight": "Workflow durability with automatic retries and state recovery. Cold-start ~50ms for cached workers. Supports long-running workflows (days/weeks) with checkpoint persistence. Published SLAs for cloud offering.",
    "signal_evidence": [
      "Published cold-start benchmarks with P95 data",
      "SLA documentation for durability guarantees (99.99%)",
      "Enterprise production usage (Netflix, Snap, Stripe)",
      "Detailed architecture docs explaining event sourcing model"
    ],
    "noise_indicators": [],
    "architectural_verdict": true
  },
  {
    "tool_name": "InfiniScale Runtime",
    "classification": "noise",
    "confidence_score": 81,
    "technical_insight": "Claims 'infinite scale with zero cold starts' but provides no benchmark data. Private beta with waitlist, no architecture documentation.",
    "signal_evidence": [],
    "noise_indicators": [
      "Impossible claims ('zero cold starts', 'infinite scale')",
      "No published benchmarks or SLAs",
      "Waitlist-only with no public documentation",
      "No explanation of durability mechanism"
    ],
    "architectural_verdict": false
  }
]
```

Now analyze the Durable Runtime space and return your findings in the specified JSON format.
