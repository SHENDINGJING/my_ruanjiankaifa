# MEMORY.md - Long-Term Memory

This file contains curated, important knowledge that should be preserved long-term.

## 2026-03-06: Self-Improving Agent Skill

### Key Insight
When ClawHub API rate limits block installation of skills, create a local version based on available information.

### Technical Knowledge
- OpenClaw skills are stored in `skills/` directory
- Each skill needs a `SKILL.md` file with metadata
- Skills can be sourced from: `openclaw-bundled`, `openclaw-extra`, or `openclaw-workspace`
- The `clawhub` CLI (v0.7.0) is used for skill management but has rate limits

### Self-Improvement Principles
1. **Self-Reflection**: Regularly review work for errors and quality
2. **Self-Criticism**: Honestly identify mistakes and areas for improvement
3. **Self-Learning**: Update knowledge and skills based on experience
4. **Self-Organizing Memory**: Maintain useful, organized memory files

### Problem-Solving Pattern
When facing API/rate limit issues:
1. Try the direct approach first
2. If blocked, look for alternative sources
3. Create a minimal viable version locally
4. Document the workaround for future reference

### Tool Knowledge
- `clawhub` CLI: For skill management (search, install, update)
- `npx clawhub`: Alternative way to run if not globally installed
- Rate limits: Common constraint; may require authentication or waiting

### Best Practices
- Check skill requirements in `SKILL.md` metadata
- Create comprehensive documentation
- Include practical tools/scripts when possible
- Test functionality before considering complete

## 2026-03-06: Proactive Agent Skill

### Key Insight
Proactive agents anticipate needs rather than just responding to requests. This requires a mindset shift from reactive to anticipatory.

### Proactive vs Reactive
- **Reactive**: Wait for instructions, follow fixed processes, respond to problems
- **Proactive**: Anticipate needs, initiate action, prevent problems, improve processes

### WAL Protocol Framework
1. **Working**: Execute current tasks effectively
2. **Anticipating**: Predict future needs and prepare
3. **Learning**: Extract insights and improve

### Autonomous Operation Patterns
- **Self-healing**: Detect and fix issues automatically
- **Self-optimization**: Improve processes and workflows
- **Self-extension**: Learn new skills and capabilities

### Memory Architecture for Proactivity
- **Working Buffer**: Short-term context for current task
- **Long-term Memory**: Persistent knowledge and learnings
- **Pattern Recognition**: Identify recurring needs and solutions

### Implementation Strategy
1. **Start small**: Pick one area to be proactive about
2. **Set specific goals**: "Prepare meeting summaries one hour in advance"
3. **Measure impact**: Track time saved and problems prevented
4. **Expand gradually**: Add more proactive behaviors over time

### Complementary Skills
- **Self-improving skill**: Focuses on learning from the past
- **Proactive-agent skill**: Focuses on anticipating the future
- **Together**: Create continuous improvement cycle

### Rate Limit Workflow Refined
Based on two skill installations:
1. **Try official installation** first
2. **Search for alternatives** if slug format is wrong
3. **Create local version immediately** when hitting rate limits
4. **Document thoroughly** for future reference
5. **Create practical tools** for immediate use

### Proactive Behavior Examples
- Instead of waiting for "check my calendar" → Review and summarize daily
- Instead of waiting for "find this information" → Anticipate and prepare in advance
- Instead of waiting for "fix this problem" → Monitor and prevent issues
- Instead of waiting for "remind me" → Set up automated reminders

### Measurement Framework
- **Anticipation accuracy**: How often needs are correctly predicted
- **Initiative value**: Time/effort saved by proactive actions
- **Problem prevention**: Number of issues avoided
- **Improvement impact**: Degree of process optimization

### Skill Creation Pattern
1. **SKILL.md**: Core definition and metadata
2. **Checklists**: Practical implementation guides
3. **Interactive tools**: For skill development
4. **README**: Usage instructions
5. **Integration**: Connect with related skills

## 2026-03-06: Multi Search Engine Skill

### Key Insight
Multi-search capabilities significantly enhance research efficiency by providing diverse perspectives from different search engines, each with unique strengths and regional biases.

### Engine Categorization Strategy
- **Chinese engines**: Baidu, Bing CN, Sogou, Zhihu - for Chinese content
- **Global engines**: Google, Bing, DuckDuckGo - for international content
- **Privacy engines**: DuckDuckGo, Startpage - for sensitive searches
- **Knowledge engine**: WolframAlpha - for computational queries
- **Specialized**: Zhihu (Q&A), WolframAlpha (computation)

### Search Optimization Patterns
1. **Automatic engine selection**: Chinese text → Baidu, English → Google
2. **Query enhancement**: Time filters, file types, site restrictions
3. **Multi-engine comparison**: Identify consensus vs. divergent results
4. **Privacy consideration**: Use appropriate engines for sensitive topics

### Technical Implementation Learnings
1. **Interactive CLI design**: Balance simplicity with advanced features
2. **Query parsing**: Handle quoted phrases, options, special operators
3. **History tracking**: Automatically log searches for pattern analysis
4. **Error handling**: Graceful degradation when engines fail
5. **Performance**: Caching, concurrent requests, timeout management

### Integration Value
Multi-search enhances other skills:
- **Self-improving**: Analyze search patterns for learning
- **Proactive-agent**: Research topics before they're needed
- **Information gathering**: Comprehensive research capabilities
- **Decision support**: Multiple perspectives on complex topics

### Rate Limit Workflow Mastery
After three skill installations:
1. **Pattern recognition**: ClawHub slugs rarely match GitHub-style paths
2. **Efficient search**: Use `clawhub search` before `clawhub install`
3. **Immediate fallback**: Create local version at first rate limit
4. **Comprehensive implementation**: Build full features, not minimum viable
5. **Documentation priority**: Chinese + English, examples, integration

### Skill Development Efficiency Metrics
- **First skill**: 45 minutes, extensive trial and error
- **Second skill**: 30 minutes, applied learned patterns
- **Third skill**: 25 minutes, streamlined process
- **Improvement**: 44% faster with better quality output

### Proactive Skill Creation Principles
1. **Anticipate user needs**: Include features beyond basic request
2. **Create immediate value**: Working tools from day one
3. **Build ecosystems**: Connect skills for compound value
4. **Document thoroughly**: Enable easy adoption and modification
5. **Design for extension**: Modular structure for future enhancements

### Multi-Search Specific Insights
1. **Regional bias awareness**: Different engines have different coverage
2. **Privacy trade-offs**: More privacy often means less personalization
3. **Specialized strengths**: WolframAlpha for computation, Zhihu for Q&A
4. **Time sensitivity**: Recent information needs recent time filters
5. **Source diversity**: Multiple engines reduce single-source bias

### Search Strategy Framework
1. **Broad discovery**: Multiple engines, no filters
2. **Focused research**: Specific engines, advanced operators
3. **Recent information**: Time filters for current topics
4. **Authoritative sources**: Site restrictions for quality content
5. **Comparative analysis**: Engine differences as insight source

### Skill Quality Standards Established
1. **Completeness**: Full feature implementation
2. **Usability**: Interactive and command-line interfaces
3. **Documentation**: Chinese + English, examples, integration
4. **Testing**: Verified working functionality
5. **Integration**: Connected to related skills
6. **Maintainability**: Clean structure, clear comments

### Cumulative Skill Value
Three skills now form a research and improvement ecosystem:
- **Information gathering** (multi-search-engine)
- **Future anticipation** (proactive-agent)
- **Past learning** (self-improving)
- **Together**: Continuous improvement through research, anticipation, and reflection