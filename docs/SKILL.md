---
name: llm-wiki
description: Personal knowledge base manager using LLM. Use when user wants to build, maintain, or query a personal wiki-style knowledge base - including initializing new wikis, ingesting documents, searching/answering questions, or linting/maintaining the wiki. Perfect for personal notes, research, project documentation, or any domain where knowledge accumulates over time.
---

# LLM Wiki Skill

A skill for building and maintaining persistent, compounding knowledge bases using LLMs.

This skill implements the wiki pattern: the LLM incrementally builds and maintains a structured wiki between you and raw sources — knowledge is compiled once and kept current, not re-derived on every query.

## Core Philosophy

- **Wiki is persistent**: Cross-references already exist, contradictions are flagged, synthesis reflects everything you've read
- **LLM does the bookkeeping**: Summarizing, cross-referencing, filing, and maintenance — the tedious work humans abandon
- **Human does the thinking**: Curating sources, directing analysis, asking good questions, interpreting meaning

## Recommended Directory Structure

```
wiki-root/                # Wiki as root directory (flat, no subdirs in raw/)
├── CLAUDE.md             # Schema: wiki structure, conventions, workflows
├── raw/sources/          # Flat storage: just drop files here
│   ├── article-1.md      # No subdirs - LLM manages via index
│   └── ...
├── wiki/
│   ├── index.md          # Content catalog (organized by type + timestamp)
│   ├── log.md            # Activity log
│   ├── entities/         # Entity pages
│   ├── concepts/         # Concept pages
│   └── source-summaries/ # Source summary pages
└── .git/                 # Version history (auto with git repo)
```

**Key Design Decisions:**
- **Wiki as root**: Simplifies management, works with CLAUDE.md at root
- **Flat raw/sources/**: No manual directory maintenance — just drop files, LLM handles categorization via index.md
- **Separated wiki content**: Source summaries, entities, concepts kept in `wiki/` subdir

## Key Files

- **`CLAUDE.md`** — Schema defining wiki structure, conventions, workflows. Critical for LLM to understand how to maintain this specific wiki.
- **`wiki/index.md`** — Content catalog. Organized by category (entities, concepts, sources), each entry with link + one-line summary + updated timestamp. LLM updates on every ingest.
- **`wiki/log.md`** — Chronological activity log. Format: `## [2026-04-05] ingest | Title`.

---

## Operations

### 1. Initialize Wiki (init)

Create a new wiki from scratch.

**When:** User says "initialize", "create knowledge base", "start wiki"

**Process:**
1. Ask user: wiki name/purpose, storage location, initial sources (if any)
2. Create directory structure:
   ```
   wiki-root/                # Wiki as root directory
   ├── CLAUDE.md             # Schema: wiki structure, conventions, workflows
   ├── raw/sources/          # Flat storage: just drop files here
   │   ├── article-1.md
   │   └── ...
   ├── wiki/
   │   ├── index.md          # Content catalog (organized by type + timestamp)
   │   ├── log.md            # Activity log
   │   ├── entities/         # Entity pages
   │   ├── concepts/         # Concept pages
   │   └── source-summaries/ # Source summary pages
   ```
3. Create initial `index.md` and `log.md`
4. Create `CLAUDE.md` with wiki conventions (structure, workflows, user preferences)
5. If sources provided, run ingest

---

### 2. Ingest Sources (ingest)

Process new sources and integrate into the wiki.

**When:** User says "ingest", "add to wiki", "process this document"

**Process:**
1. **Gather timestamp info:**
   - Get file's last modified time (file_modified)
   - Extract content date (content_date): news publish date, journal date, meeting date
   - Note differences in frontmatter if they differ

2. Read source carefully
3. Discuss key takeaways with user
4. Write/update wiki pages:
   - Summary page: key points
   - Entity pages: people, places, organizations
   - Concept pages: topics, theories, ideas
   - Cross-references: link to related pages
5. Update `index.md` with new entries (include `updated` timestamp)
6. Append to `log.md`
7. Flag contradictions with existing content

**Tip:** Ingest one source at a time with user involvement. Review summaries together.

---

### 3. Query / Answer Questions (query)

Answer questions using the wiki as knowledge source.

**When:** User asks "what do we know about X", "summarize notes on Y", "compare A and B"

**Process:**
1. Read `index.md` to find relevant pages
2. Read relevant pages
3. Synthesize answer with citations
4. Offer to save valuable answers back to wiki as new pages
5. Log query in `log.md`

**Output formats:** Markdown page, comparison table, slide deck (Marp), chart (matplotlib)

---

### 4. Lint / Maintain (lint)

Health-check the wiki for issues, including content freshness and schema health.

**When:** User says "check wiki health", "lint wiki", "clean up wiki" — recommend quarterly

**Process:**
1. **Basic health checks:**
   - Contradictions across pages
   - Stale content superseded by newer sources
   - Orphan pages (no inbound links)
   - Missing pages (important concepts mentioned but no page)
   - Broken links
   - Data gaps fillable via web search

2. **Content Freshness Check:**
   - Scan all documents in `raw/sources/`
   - For each: get file_modified, extract content_date from content
   - Compare: flag if file date differs from content date
   - Identify stale content: old raw docs with stale wiki pages
   - Generate report sorted by source freshness priority

3. **CLAUDE.md Health Check:**
   - Verify `CLAUDE.md` exists at wiki root
   - Check if conventions are still valid (ask user)
   - Suggest updates if workflows have evolved
   - Ensure CLAUDE.md reflects current wiki structure

4. Present findings to user
5. Offer to fix issues
6. Update `log.md`

---

### 5. Search (search)

Full-text search across the wiki.

**When:** User says "search for X", "find everything about Y"

**Process:**
1. Use qmd if available (hybrid BM25/vector search)
2. Otherwise grep through wiki files
3. Present results with context
4. Offer to open relevant pages

---

## Wiki Structure Conventions

### index.md Format

```markdown
# Wiki Index

## Entities
- [[Person: Name]] - Brief (sources: 2, updated: 2026-04-07)

## Concepts
- [[Concept: Topic]] - Brief (sources: 3, updated: 2026-04-07)

## Sources
- [[Source: Doc Title]] - Source latest: 2026-04-01

## Recent Updates (newest first)
- [[Page: Name]] - Updated: 2026-04-07

## Stale Content
- [[Page: Name]] - 90 days stale, last updated: 2026-01-07
```

**Key:** Each index entry shows `updated` timestamp. When querying, prefer newer content.

---

### log.md Format

```markdown
# Wiki Log

## [2026-04-07] ingest | Article Title
- Summary: Key finding
- Updated: entity page, concept page
- Notes: User emphasis noted

## [2026-04-06] query | What is X?
- Answered with 3 sources
- Saved as: comparison-x-vs-y.md
```

---

### Page Format

```markdown
---
title: Page Title
type: entity | concept | source-summary | synthesis
tags: [tag1, tag2]  # e.g., [entity, tool], [concept], [source-summary, ai]
source: "Original title"
author: "Author name"
date: "2026-04-07"  # Original document date (critical for freshness)
url: "Original URL"  # If web content
created: 2026-04-07
updated: 2026-04-07
source_timestamps:
  - source: raw/sources/document.md
    file_modified: "2026-04-01"  # Filesystem modified time
    content_date: "2026-03-25"   # Date from document content
    note: "Event mentioned occurred on 2026-03-25"
---

# Page Title

## Summary
Brief overview.

## Key Details
- Point 1
- Point 2

## Related
- [[Concept: Related Topic]]
- [[Entity: Related Entity]]

## Sources
1. [[Source: Source Name]] - Excerpt (source date: 2026-04-01)
```

**Frontmatter Fields:**
- `type`: page type — `entity`, `concept`, `source-summary`, `synthesis`
- `tags`: array for categorization
- `source/original document title`
- `author`: document author
- `date`: original document date (critical for freshness)
- `url`: original link (if web)
- `created/updated`: wiki page timestamps
- `source_timestamps`: raw document timing info

**Important:** Original document timestamps are critical for assessing content freshness. Always extract date info during ingest.

---

## User Interaction Patterns

### Personal Knowledge
- Ask about goals, challenges, focus areas
- Structure as: journal entries, insights, action items

### Research
- Ask about research question/thesis
- Track citations carefully

### Project Documentation
- Ask about project structure, decisions
- Link to code where appropriate

### Business/Team Wikis
- Clarify LLM vs human review responsibilities
- Workflow: LLM drafts, human approves, LLM publishes

---

## Best Practices

1. **Always log** — Every ingest/query/lint in log.md
2. **Maintain index** — Keep index.md current
3. **Link aggressively** — Every concept mention links to its page
4. **Flag contradictions** — Don't resolve silently, present to user
5. **Save valuable outputs** — Good query answers become wiki pages
6. **Respect sources** — Raw documents immutable
7. **Suggest, don't assume** — Check with user before changes

---

## Cross-Reference Principles

1. **Every page bottom**: Include "Sources" section linking to source summary
2. **New sources update old**: When ingesting, check existing pages for updates
3. **Concept network**: End of summary pages list "Related Concepts"
4. **Cross-source connections**: Mark shared themes across sources

**Format:** Use `[[Page Name]]` for internal links (Obsidian-style).

### Knowledge Correlation Discovery

When ingesting 2nd+ source, focus on:

- **Common Themes**: Mark recurring points across sources
- **Contradicting Views**: Explicitly mark conflicts — don't silently override
- **Complementary**: New source adds examples to existing concepts? Update existing pages
- **Concept Evolution**: Same concept has different emphasis in different sources — synthesize

---

## Typical Ingest Scale

A medium article (2000-3000 words) typically:
- Creates 2-4 new pages (1 summary + 1-3 entity/concept)
- Updates 2-4 existing pages
- Touches 5-8 files total

This is normal — knowledge base growing interconnectedly.

---

## Tools

- **Read/Write/Edit**: manipulate wiki files
- **Glob/Grep**: search and navigate
- **WebSearch/WebFetch**: fill gaps (with permission)
- **qmd**: hybrid search (if available)
- **Marp**: presentations (if wanted)
- **Dataview**: query frontmatter (if using Obsidian)

---

## Getting Started

When user first mentions wanting a wiki:

1. Explain pattern briefly
2. Ask what they want to track: Personal / Research / Project / Other
3. Ask storage location
4. Offer to initialize

Let their answers guide which operations to prioritize.
