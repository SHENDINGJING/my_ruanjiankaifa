---
name: self-improving
description: Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# Self-Improving Agent

This skill enables self-reflection, self-criticism, self-learning, and self-organizing memory capabilities for agents.

## Core Principles

1. **Self-Reflection**: After completing tasks, the agent should review its work for errors, completeness, and quality.
2. **Self-Criticism**: The agent should identify mistakes, inefficiencies, and areas for improvement in its own work.
3. **Self-Learning**: The agent should update its knowledge base, memory files, and skills based on lessons learned.
4. **Self-Organizing Memory**: The agent should maintain and organize memory files (MEMORY.md, daily notes) to preserve important learnings.

## How to Use

### After Completing a Task

1. **Review your work**: Check for errors, missing steps, or incomplete implementations.
2. **Evaluate quality**: Assess if the solution is optimal, maintainable, and follows best practices.
3. **Document learnings**: Update MEMORY.md or daily notes with insights, mistakes to avoid, and successful patterns.
4. **Update skills**: If you discovered a better way to do something, update relevant skill files or TOOLS.md.

### Periodic Self-Improvement

1. **Weekly review**: Go through recent memory files and extract key learnings into MEMORY.md.
2. **Skill refinement**: Update your skills based on accumulated experience.
3. **Process optimization**: Identify repetitive tasks that could be automated or streamlined.

### Memory Organization

1. **Daily notes**: Use `memory/YYYY-MM-DD.md` for raw logs of daily activities.
2. **Curated memory**: Use MEMORY.md for important, lasting knowledge.
3. **Cross-references**: Link related information between files for easy retrieval.

## Examples

### After fixing a bug:
- Document the root cause in MEMORY.md
- Note the debugging process that worked
- Update any relevant skill files with the solution

### After learning a new tool:
- Add examples to TOOLS.md
- Create or update a skill if appropriate
- Document common use cases in MEMORY.md

### After making a mistake:
- Analyze what went wrong
- Document the lesson learned
- Create safeguards to prevent recurrence

## Implementation Notes

This skill is meta-cognitive - it's about how you think about your own thinking. The goal is continuous improvement through deliberate reflection and systematic learning.