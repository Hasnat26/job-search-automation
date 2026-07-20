# Career OS Domain Model

## Purpose

Defines the core business entities, domain boundaries, architectural principles, and relationships for the Career Operating System.

---

# M2.2 Domain Boundary

## Core Source-of-Truth Domains

These domains contain the canonical business truth of the Career Operating System.

- Career Profile
- Professional Experience
- Projects
- Skills & Competencies
- Education & Certifications
- Evidence Repository
- Job Search / Career Targeting

---

## Derived Artifact Area

Generated artifacts are produced from canonical business data but never become the authoritative source.

- Generated Outputs

Examples:

- CV Version
- Cover Letter Version
- LinkedIn Snapshot
- Interview Preparation Package

---

# Architecture Principles

## AP-001
Never store derived data.

---

## AP-002
Domains hold truth; outputs consume truth.

---

## AP-003
Generated artifacts are persisted snapshots, not authoritative data.

---

## AP-004
Model today's needs, preserve tomorrow's extension points.

---

## AP-005
Normalize only when multiple independent lifecycles emerge.

Normalization is justified only when an object:

- has its own lifecycle
- is shared by multiple parent entities
- has its own business rules
- requires independent querying or updating

---

## AP-006
Separate Core (Canonical), Reference / Shared, and Operational entities.

---

# Entity Classification

## Core (Canonical) Entities

Authoritative, person-centered business records.

Examples:

- Person
- Employment
- Project
- Skill
- Education
- Certification
- EvidenceItem

---

## Reference / Shared Entities

Reusable supporting entities shared across multiple domains.

Examples:

- Company
- Institution
- SkillCategory
- Country
- Industry
- Technology

---

## Operational Entities

Workflow, tracking, assessment, and generated artifact records.

Examples:

- JobOpportunity
- Application
- MatchAssessment
- CVVersion
- CoverLetterVersion
- LinkedInSnapshot

Operational entities may persist snapshots or analysis results, but they never become source-of-truth.

---

# M2.3 Preparation

## Career Profile (v1)

### Canonical Entity

- Person

---

### Embedded Profile Attributes

- Full Name
- Professional Headline
- Professional Summary
- Primary Email
- Primary Phone
- LinkedIn URL
- GitHub URL
- Portfolio URL
- Current Location
- Preferred Location
- Work Authorization

These attributes remain embedded within the `Person` entity for MVP (v1).

---

### Deferred Entities

The following concepts are intentionally deferred until independent lifecycles justify normalization.

- ContactMethod
- Language
- Nationality
- SecurityClearance
- MobilityPreference

---

# Next Milestone

## M2.4 — Person Entity Attribute Design

The next step is to define the Person entity at the attribute level, including:

- Required vs Optional attributes
- Data types
- Business rules
- Validation rules
- Future extensibility
- Relationships with other domains