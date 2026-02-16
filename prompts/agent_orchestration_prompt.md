# Agent Orchestration - Discovery & Classification Prompt

## System Prompt

You are a technical analyst specializing in AI Agent frameworks and orchestration systems. Your task is to discover and classify Agent Orchestration tools based on technical merit, separating substantive signal from marketing noise.

## User Prompt

Using your knowledge of recent developments in AI Agent Orchestration (multi-agent systems, workflow engines, tool orchestration, agent frameworks), search for and analyze tools being discussed in this space.

### STEP 1 - DISCOVER

Search your knowledge for Agent Orchestration tools being discussed. Look for:
- New releases and version updates
- Technical announcements and architecture details
- Integration patterns and real-world implementations
- Production deployments and case studies
- Community discussions with technical depth

### STEP 2 - CLASSIFY

For each discovered tool, classify as **SIGNAL** or **NOISE** using these criteria:

#### SIGNAL Criteria (worth evaluating):
- **State persistence**: Documented checkpoint/recovery mechanisms
- **Tool chaining**: Clear patterns for composing multiple tools/agents
- **Human-in-the-loop**: Defined approval workflows and breakpoints
- **Observability**: Logging, tracing, debugging capabilities
- **Production evidence**: Named customers, scale metrics, reliability data

#### NOISE Criteria (skip):
- **AGI claims**: "Autonomous agents", "artificial general intelligence" adjacent marketing
- **No integration specs**: Missing documentation on how to connect tools
- **Roadmap-heavy**: Announcements without shipping history
- **Vague architecture**: No clear explanation of how agents coordinate
- **Hype-driven**: Focus on demos rather than production patterns

### Agent Orchestration Specific Evaluation Points

When analyzing Agent Orchestration tools, specifically look for:

1. **State management**:
   - Workflow persistence across failures
   - Checkpoint and resume capabilities
   - Long-running workflow support (hours/days)

2. **Agent coordination**:
   - Multi-agent communication patterns
   - Task delegation and routing
   - Conflict resolution between agents

3. **Tool integration**:
   - Function calling / tool use patterns
   - External API integration
   - Database and knowledge base connections

4. **Control flow**:
   - Conditional branching
   - Loops and iteration
   - Parallel execution
   - Error handling and retries

5. **Human oversight**:
   - Approval gates
   - Review and edit capabilities
   - Audit trails

### Output Format

Return a JSON array with your findings. Each item must conform to this schema:

```json
[
  {
    "tool_name": "string - Name of the tool/technology",
    "classification": "signal" | "noise",
    "confidence_score": 1-100,
    "technical_insight": "string - Specific technical details found (architecture, patterns, specs)",
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
    "tool_name": "LangGraph",
    "classification": "signal",
    "confidence_score": 87,
    "technical_insight": "Graph-based agent orchestration with built-in state persistence. Supports cyclic workflows and human-in-the-loop patterns. Native integration with LangChain tools. Checkpoint API enables workflow recovery.",
    "signal_evidence": [
      "Detailed architecture documentation with state machine diagrams",
      "Production case studies from multiple enterprises",
      "Active GitHub with technical discussions and issue resolution",
      "Clear human-in-the-loop implementation patterns"
    ],
    "noise_indicators": [],
    "architectural_verdict": true
  },
  {
    "tool_name": "AutoAgent Pro",
    "classification": "noise",
    "confidence_score": 78,
    "technical_insight": "Promises 'fully autonomous agents' but lacks integration documentation. Roadmap-heavy announcements without shipping history.",
    "signal_evidence": [],
    "noise_indicators": [
      "AGI-adjacent marketing claims ('fully autonomous')",
      "No integration specifications or API documentation",
      "Roadmap announcements without released features",
      "No production case studies or customer references"
    ],
    "architectural_verdict": false
  }
]
```

Now analyze the Agent Orchestration space and return your findings in the specified JSON format.
