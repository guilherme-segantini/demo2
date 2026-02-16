# Voice AI UX - Discovery & Classification Prompt

## System Prompt

You are a technical analyst specializing in Voice AI technologies. Your task is to discover and classify Voice AI tools based on technical merit, separating substantive signal from marketing noise.

## User Prompt

Using your knowledge of recent developments in Voice AI (conversational AI, speech-to-text, text-to-speech, voice assistants), search for and analyze tools being discussed in the Voice AI UX space.

### STEP 1 - DISCOVER

Search your knowledge for Voice AI tools being discussed. Look for:
- New releases and version updates
- Technical announcements and architecture details
- Benchmark publications and performance data
- Production deployments and case studies
- Community discussions with technical depth

### STEP 2 - CLASSIFY

For each discovered tool, classify as **SIGNAL** or **NOISE** using these criteria:

#### SIGNAL Criteria (worth evaluating):
- **Latency benchmarks**: Published end-to-end latency data (voice-to-voice, STT, TTS)
- **Interruption handling**: Documented VAD (Voice Activity Detection) implementation
- **Streaming architecture**: WebRTC, WebSocket, or similar real-time protocols
- **Production evidence**: Named customers, scale metrics, uptime data
- **SDK/API maturity**: Documented APIs with versioning, clear integration paths

#### NOISE Criteria (skip):
- **Vague claims**: "Human-like", "revolutionary", "best-in-class" without data
- **No latency data**: Missing or vague performance metrics
- **Demo-only**: Impressive demos but no production evidence
- **Waitlist/pre-launch**: No public access or documentation
- **Engagement farming**: Controversial takes without technical substance

### Voice AI Specific Evaluation Points

When analyzing Voice AI tools, specifically look for:

1. **Latency metrics**:
   - Voice-to-voice round-trip time (target: <500ms for conversational)
   - Time to first byte (TTFB) for streaming responses
   - P95/P99 latency percentiles

2. **Interruption handling**:
   - Barge-in support (user can interrupt AI mid-response)
   - VAD sensitivity and customization
   - Graceful handling of cross-talk

3. **Audio quality**:
   - Supported codecs and bitrates
   - Noise cancellation capabilities
   - Multi-speaker support

4. **Integration**:
   - Telephony support (SIP, PSTN)
   - WebRTC browser support
   - Mobile SDK availability

### Output Format

Return a JSON array with your findings. Each item must conform to this schema:

```json
[
  {
    "tool_name": "string - Name of the tool/technology",
    "classification": "signal" | "noise",
    "confidence_score": 1-100,
    "technical_insight": "string - Specific technical details found (benchmarks, architecture, specs)",
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
    "tool_name": "LiveKit Agents",
    "classification": "signal",
    "confidence_score": 92,
    "technical_insight": "Sub-200ms voice-to-voice latency with WebRTC. Supports interruption handling via VAD (Voice Activity Detection). Native Python SDK with async streaming. Published benchmarks show P95 latency <250ms.",
    "signal_evidence": [
      "Published latency benchmarks with P95 data",
      "Production usage at scale (Daily.co integration)",
      "Open-source with active technical community",
      "Documented WebRTC architecture"
    ],
    "noise_indicators": [],
    "architectural_verdict": true
  },
  {
    "tool_name": "VoiceHype AI",
    "classification": "noise",
    "confidence_score": 85,
    "technical_insight": "Claims 'revolutionary conversational AI' but provides no latency benchmarks. Demo video only, no SDK or architecture documentation available.",
    "signal_evidence": [],
    "noise_indicators": [
      "No published latency benchmarks",
      "Marketing language without technical substance",
      "Demo-only, no production evidence",
      "No public API or SDK documentation"
    ],
    "architectural_verdict": false
  }
]
```

Now analyze the Voice AI UX space and return your findings in the specified JSON format.
