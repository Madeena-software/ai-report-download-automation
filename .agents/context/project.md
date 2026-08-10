---
title: Repository Context Template
document_id: AGENT-CONTEXT-001
version: 1.1
status: approved-template
language: en-US
last_updated: 2026-08-10
scope:
  - repository-level AI orientation
  - repository authority mapping
  - delivery-state orientation
  - scoped-context routing
authority_note: This file is supporting, refreshable repository context. Approved repository authority governs intended behavior. Observed repository evidence governs claims about current implementation reality. Neither silently overrides the other, and this context replaces neither.
---

# Repository Context

This file is the repository-level context entrypoint for AI-assisted software delivery.

It provides a verified orientation map of the repository, identifies where authoritative information lives, summarizes the current delivery state, and routes agents to additional scoped context when needed.

It is not a replacement for authoritative repository artifacts.

Keep this file concise enough to serve as an orientation layer. Prefer references to authoritative documents over duplicating their full contents.

## Repository identity

**Name:**  
`<repository-name>`

**Repository type:**  
`<application | service | library | monorepo | data pipeline | documentation repository | internal tool | other>`

**Primary responsibility:**  
`<short description of the outcome or system responsibility owned by this repository>`

## Purpose

Describe why this repository exists and what outcome it is responsible for.

Focus on repository-level purpose rather than implementation details.

`<repository-purpose>`

## Current repository state

Describe the repository's current delivery condition.

Examples include:

- greenfield;
- early implementation;
- active development;
- mature;
- legacy;
- migration or modernization;
- maintenance;
- another repository-specific state.

Record only information that materially affects planning, execution, review, or release decisions.

**Current state:**  
`<state>`

**Relevant summary:**  
`<verified summary of the current repository condition>`

Existing repositories MUST reuse valid artifacts and implementation evidence rather than recreating workflow artifacts solely to conform to this template.

## Intended authority map

Map the intended-authority responsibilities defined by `.agents/software-workflow.md` to the actual approved sources used by this repository.

Physical file locations and artifact structure are repository-defined.

### Business sources and decisions

- `<path, URL reference, issue, decision record, contract, policy, or other approved source>`

### Product / PRD authority

- `<authoritative product or PRD source>`

### Requirements and matrices

- `<requirement registry, specification, traceability source, dependency source, or equivalent>`

### Architecture and repository policy

- `<architecture specification, ADR location, repository instructions, policy, or equivalent>`

### Delivery planning

- `<implementation plan, roadmap, Work Package plan, MVP plan, gap register, or equivalent>`

### Release policy

- `<release procedure, deployment policy, operational gate, or equivalent>`

### Other authority

- `<additional repository-specific authoritative sources>`

Do not duplicate authoritative artifacts when references are sufficient.

If an authority-bearing artifact does not yet exist, record that absence rather than silently substituting agent-generated assumptions.

## Observed implementation evidence map

Map the repository evidence used to establish what currently exists, what changed, and what has actually been verified.

Relevant evidence MAY include:

### Source and configuration

- `<source roots, configuration, generated-code boundaries, or other implementation references>`

### Data and migrations

- `<migration locations, schema sources, persistence definitions, or equivalent>`

### Tests and verification

- `<test locations, verification commands, fixtures, integration evidence, or equivalent>`

### Version control and CI

- `<Git repository/history reference, CI workflows, status checks, or equivalent>`

### Runtime and operational evidence

- `<runtime observations, logs, deployed-state evidence, external-system evidence, or equivalent when applicable>`

Observed evidence MUST NOT be treated as intended authority merely because it reflects current behavior.

Approved intended authority MUST NOT be treated as proof that observed implementation already conforms.

## Top-level architecture and boundaries

Summarize only the repository-wide boundaries that an agent should understand before loading more detailed context.

Relevant topics MAY include:

- deployable boundaries;
- module, service, domain, or package boundaries;
- data ownership and source-of-truth boundaries;
- trust and security boundaries;
- major external systems;
- major runtime topology;
- repository-to-repository boundaries;
- materially important architectural constraints.

`<concise repository-wide architecture and boundary summary>`

Detailed architecture SHOULD remain in its authoritative repository location when one exists.

## Scoped context

Additional context MAY exist below `.agents/context/` for repository-defined scopes such as:

- modules;
- services;
- domains;
- packages;
- integrations;
- applications;
- infrastructure areas;
- other meaningful repository boundaries.

Load only the scoped context materially relevant to the current work.

### Available scoped context

- `<scope>` → `<relative-context-path>`
- `<scope>` → `<relative-context-path>`

Examples:

```text
Member module       → modules/member/project.md
Image Gateway       → modules/image-gateway/project.md
Billing service     → services/billing/project.md
External PACS       → integrations/pacs/project.md
```

The hierarchy under `.agents/context/` is repository-defined.

A deeper scoped context file does not implicitly override repository-level context or authoritative repository sources.

Material contradictions MUST be verified against repository authority before use.

## Delivery state

Record the currently verified software-delivery state.

This section is an orientation summary, not a replacement for authoritative delivery-planning artifacts.

### Current delivery objective

`<MVP-oriented objective | Work-Package-oriented objective | maintenance objective | other>`

### Current Work Package / MVP / delivery slice

`<identifier or description, if applicable>`

### Quality-gate state

Record only gates that have been verified from repository evidence.

Use the canonical gate states from `.agents/software-workflow.md`:

`pending`, `in_review`, `blocked`, `passed`, `reopened`, or `not_applicable` with recorded rationale.

If a gate has not yet been reliably assessed, record that fact outside the canonical gate-state value rather than inventing a new gate state.

| Gate | Status | Evidence / authority |
|---|---|---|
| B0 — Business Framing | `<pending | in_review | blocked | passed | reopened | not_applicable>` | `<reference or rationale>` |
| P1 — Product Definition | `<status>` | `<reference or rationale>` |
| R2 — Requirements Traceability | `<status>` | `<reference or rationale>` |
| A3 — Architecture Clarity | `<status>` | `<reference or rationale>` |
| D4 — Delivery Readiness | `<status>` | `<reference or rationale>` |
| T5 — Task Readiness | `<status>` | `<reference or rationale>` |
| E6 — Execution Verification | `<status>` | `<reference or rationale>` |
| V7 — Implementation Review | `<status>` | `<reference or rationale>` |
| R8 — Remediation Closure | `<status>` | `<reference or rationale>` |
| A9 — Baseline Acceptance | `<status>` | `<reference or rationale>` |
| G10 — Release Approval | `<status>` | `<reference or rationale>` |

**Earliest unmet or materially unreliable gate:**  
`<gate-id and reason>`

### Active task(s)

For Draft planning work, the immutable publication revision MAY still be unresolved.

Any task recorded as `Validated/Published`, `In Execution`, `Review Required`, or `Remediation Required` MUST identify the exact immutable governing task revision.

Preferred Git-backed identity:

```text
<task path> @ <full Git commit SHA containing the governing task content>
```

- `<task identity, lifecycle state, and governing immutable revision when required>`

### Blocking items

- `<blocking dependency, decision, approval, or gap>`

Non-blocking items should remain visible only when they materially affect downstream planning or execution.

## Accepted baseline

Record the current accepted immutable repository revision.

For Git repositories, prefer the full commit SHA.

If no accepted baseline can be reliably established, record `unknown` explicitly and treat the uncertainty according to its delivery impact. Do not invent or infer an accepted baseline from the current branch tip alone.

**Accepted baseline:**  
`<immutable repository revision>`

**Accepted scope:**  
`<short description of what this baseline is known to satisfy>`

**Evidence reference:**  
`<review, CI, acceptance record, or other supporting evidence>`

Branch names, tags, or labels MAY be recorded for convenience but MUST NOT replace the immutable revision used for execution and review.

## Known gaps and open decisions

Record only unresolved items that materially affect repository orientation or delivery.

Detailed gap registers, ADRs, requirement matrices, or decision logs SHOULD remain in their authoritative repository locations when they already exist.

### Blocking

- `<item>`
  - owner: `<owner>`
  - impact: `<impact>`
  - resolution trigger: `<trigger>`

### Non-blocking

- `<item>`
  - owner: `<owner>`
  - impact: `<impact>`
  - resolution trigger: `<trigger or latest stage by which it must be resolved>`

Do not convert unresolved decisions into implementation assumptions.

## Repository conventions

Record repository-specific conventions and constraints that materially affect planning, execution, review, or release.

Examples MAY include:

- repository structure conventions;
- module ownership rules;
- testing expectations;
- migration constraints;
- generated-code boundaries;
- dependency policies;
- API compatibility constraints;
- deployment restrictions;
- security or privacy constraints;
- prohibited operational practices.

`<repository-specific conventions>`

Do not reproduce generic software-engineering methodology here.

## Context verification

This context is supporting, refreshable repository knowledge.

Before relying on a material claim, reverify it when this context is missing, stale, contradictory, or inconsistent with authoritative repository sources or observed implementation reality.

**Last verified:**  
`<date-time or date>`

**Verified against repository revision:**  
`<immutable revision when applicable>`

**Verified sources:**  

- `<source>`
- `<source>`

**Known verification limitations:**  

- `<limitation or "None known">`
