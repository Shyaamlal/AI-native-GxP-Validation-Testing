# Project Context

**Purpose:** This folder contains all context needed for AI-assisted validation work. Every validation session should reference these files to ensure consistent, context-aware documentation.

---

## What is Context Management?

Context management means giving AI tools comprehensive knowledge about:
- The application being validated
- The validation methodology being used
- Patterns and lessons learned from previous work
- Historical decisions and rationale

**Result:** AI generates validation documentation that is specific to Sambhava and compliant with GxP standards, rather than generic templates.

---

## Files in This Folder

### Core Context Documents

**`Methodology.md`**
- Validation approach (GAMP 5 retrospective validation)
- Workflow steps (Observation → Requirements → Testing)
- AI tool usage guidelines
- Standards and compliance requirements

**`Sambhava_Application_Context.md`**
- Application overview and business purpose
- User workflows and personas
- Technical architecture and data models
- Business rules and risk context
- **Most important file for accurate AI assistance**

---

### Accumulated Knowledge

**`Skills/`**
- Decision frameworks and patterns learned from validation work
- Domain-specific guidance for AI tools
- Updated after each feature when new patterns emerge

Example: `feature_boundary_skill.md` - How to define feature scope

---

### Historical Context

**`Thread_Summaries/`**
- What happened in each validation session
- Key decisions and rationale
- Outcomes and next steps
- Created at end of each session

**`Learning_Journals/`**
- Personal reflections and insights
- Process observations and improvements
- Optional documentation for deeper reflection

---

### Reusable Assets

**`Templates/`**
- Document templates for validation artifacts
- Starter prompts for AI tools
- Reusable structures and formats

---

## How to Use This Folder

### Starting a Validation Session

**With Claude Code (or any AI tool):**
```
Working directory: C:\Users\motic\sambhava-validation-portfolio

Read 00_Project_Context\ for full context.

Starting [Feature Name] validation...
```

**What the AI reads:**
1. `Methodology.md` - Understands validation approach
2. `Sambhava_Application_Context.md` - Understands application
3. `Skills/` - Applies learned patterns
4. `Thread_Summaries/` - Knows historical decisions

---

### Ending a Validation Session

**Ask the AI tool:**
```
Session complete. Based on today's work, what should I update in 00_Project_Context/?
```

**The AI will suggest:**
- Create Thread Summary for this session
- Update Skills if new patterns emerged
- Update Application Context if new facts discovered

This ensures you don't forget important updates.

---

## Why Context Matters

### Without Context (Generic Output):
```
Requirement: System shall validate email format
Test: Enter valid email, enter invalid email
```

**Problem:** Could be any application

---

### With Context (Sambhava-Specific Output):
```
Requirement: System shall validate email format for client records

Context: Clients are HR professionals receiving assessment reports
Risk: Invalid email = client cannot access purchased assessment
Impact: MEDIUM

Test: 
- Valid corporate email → Client created, welcome email sent
- Invalid email → Error with clear guidance
- Edge case: Check if disposable emails should be blocked
```

**Result:** Specific to Sambhava, considers business impact, asks relevant questions

---

## Updating Context

### After Validating a Feature:

**1. Always Create Thread Summary** (5 minutes)
- Document what you validated
- Record key decisions made
- Note what's next
- File: `Thread_Summaries/YYYY-MM-DD_Feature_Complete.md`

**2. Update Skills When You Learn Patterns** (5-10 minutes)
- Example: "CRUD operations should be separate features"
- Add to relevant skill file
- Only when you think "I should remember this for next time"

**3. Update Application Context When You Discover Facts** (as needed)
- Example: "Email uniqueness is enforced at database level"
- Add to appropriate section
- Only when you learn something new about the application

**Not rigid rules - just document when it makes sense!**

---

## Context Layers

This folder organizes context in layers:

**Layer 1: Methodology** (rarely changes)
- How validation works
- Standards and compliance
- AI tool usage approach

**Layer 2: Application** (updates when understanding deepens)
- Business purpose and workflows
- Technical architecture
- Business rules and constraints

**Layer 3: Skills** (grows over time)
- Patterns learned from validation work
- Decision frameworks
- Accumulated expertise

**Layer 4: History** (grows with each session)
- What happened in past sessions
- Decisions made and why
- Learnings and observations

---

## Why This Approach Works

### Alignment with Industry Context Practices:

Major tech companies (GitHub, Microsoft, Netflix) use similar context management:
- **GitHub Copilot Spaces** - Project context for AI coding
- **Microsoft WorkIQ** - Organizational memory
- **Netflix Global Catalog** - Knowledge infrastructure

**Key insight:** Context quality matters more than AI model choice.

Good context + basic AI = excellent results  
Poor context + advanced AI = mediocre results

---

## Quick Start for New Users

**Understanding this repository:**

1. Read `Methodology.md` (10 min) - Validation approach
2. Skim `Sambhava_Application_Context.md` (5 min) - Application basics
3. Review `01_Login/` folder (15 min) - See methodology applied
4. Check `Skills/` (5 min) - See learned patterns

**Total: 35 minutes to understand the framework**

---

## Workflow with AI Tools

### Starting Work:
```
Read 00_Project_Context\ for full context.
Starting [Feature] validation...
```

### During Work:
- AI has context, just work normally
- AI responses will be Sambhava-specific

### Ending Work:
```
What should I update in 00_Project_Context based on today's work?
```

### AI Suggests Updates:
- Thread Summary needed? Yes/No
- Skills to update? Which ones and why
- Application Context changes? What facts discovered

**Let the AI help you remember what needs updating!**

---

## Maintenance Tips

**Don't overthink it:**
- Thread Summary = Always do (quick end-of-session doc)
- Skills update = Only when you learned a reusable pattern
- Application Context = Only when you discovered new facts
- Learning Journal = Optional, for personal reflection

**Quality over completeness:**
- Better to have accurate, focused context
- Than exhaustive but outdated context
- Update when it makes sense, not on a schedule

---

## Questions?

- **"How do I start?"** → Read Methodology.md and Sambhava_Application_Context.md
- **"What if context gets too large?"** → Archive old thread summaries, keep skills updated
- **"Do I need all of this?"** → Methodology and Application Context are essential, rest is optional
- **"How often should I update?"** → After each feature, let AI suggest what needs updating

---

## What This Folder Is Not

- This is not a feature backlog
- This does not replace validation artifacts
- This is not a substitute for human review or approval


*This folder is the foundation for context-aware AI validation. With it, AI tools understand Sambhava specifically and generate accurate, compliant documentation.*