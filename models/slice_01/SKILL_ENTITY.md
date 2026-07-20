# Skill Entity

**Status:** Approved Baseline
**Version:** 1.0
**Scope:** Slice 01
**Level:** Entity Specification

---

## Purpose

The Skill entity represents one distinct professional skill owned by a single Person within the Career Operating System.

Each Skill record preserves one authoritative skill fact independently of resumes, CVs, generated profiles, Employment records, Project records, or other presentation artifacts.

The Skill entity stores only authoritative skill facts. It does not store inferred proficiency, competency assessments, calculated experience metrics, recommendation scores, or other derived information.

---

## Responsibilities

The Skill entity is responsible for:

- Recording factual professional skills.
- Maintaining the canonical skill inventory for one Person.
- Representing one distinct skill per record.
- Recording skill ownership.
- Recording skill classification.
- Recording the canonical name of each skill.
- Recording optional factual descriptions.
- Maintaining authoritative skill information.

The Skill entity is NOT responsible for:

- Maintaining the Person profile.
- Maintaining Employment records.
- Maintaining Project records.
- Maintaining Company master data.
- Maintaining Evidence artifacts.
- Maintaining generated career artifacts.
- Recording where or when a skill was demonstrated.
- Storing derived competency indicators.

---

## Ownership Principle

Skill owns skill facts.

Each Skill record belongs to exactly one Person through `person_id`.

Person owns professional identity.

Employment owns employment facts.

Project owns project facts.

Employment and Project may reference Skill usage but shall never own or duplicate Skill facts.

Generated outputs may reference, summarize, or transform Skill information but shall never become the authoritative source of Skill facts.

---

## Attributes

The Skill entity defines the canonical professional skill inventory owned by one Person.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| skill_id | Unique identifier for the Skill record. |
| person_id | Reference to the owning Person entity. |
| skill_name | Canonical professional skill name. |
| skill_category | Controlled classification of the skill. |
| description | Optional factual description of the skill. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| skill_id | Yes | UUID | System-generated unique identifier. |
| person_id | Yes | UUID | Reference to the owning Person entity. |
| skill_name | Yes | String | Canonical professional skill name. |
| skill_category | Yes | Reference Value (Controlled Vocabulary) | Skill classification selected from an approved controlled vocabulary. |
| description | No | Text | Optional factual description of the skill. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-SKILL-001

Each Skill record shall belong to exactly one Person.

---

### BR-SKILL-002

Each Skill record shall represent one distinct professional skill.

---

### BR-SKILL-003

Skill shall be the authoritative source of skill facts.

Skill facts shall not be duplicated within the Person entity, Employment entity, Project entity, or generated career artifacts.

---

### BR-SKILL-004

Skill shall not store generated or derived information.

Derived competency assessments, proficiency calculations, experience duration, recommendation scores, and other calculated information shall be produced by application services rather than stored within the Skill entity.

---

### BR-SKILL-005

Employment and Project may reference Skill records as evidence that a Skill was demonstrated.

Neither Employment nor Project shall own or duplicate Skill facts.

---

### BR-SKILL-006

Multiple Employment records and multiple Project records may reference the same Skill.

Version 1 intentionally does not implement explicit relationship entities for these references.

---

### BR-SKILL-007

`skill_category` shall be selected from an approved controlled vocabulary.

Free-text skill classifications shall not be permitted.

---

### BR-SKILL-008

Skill records shall preserve factual professional skill information.

Historical skill information shall not be modified to reflect changing market terminology, vendor naming, or technology trends unless correcting factual errors.

---

## Validation Rules

### VR-SKILL-001

`skill_id` shall be system-generated and immutable after record creation.

---

### VR-SKILL-002

`person_id` shall reference a valid Person record.

---

### VR-SKILL-003

`skill_name` is mandatory and shall not be empty.

---

### VR-SKILL-004

The combination of `person_id` and the canonical `skill_name` shall be unique.

Duplicate Skill records for the same Person shall not be created.

---

### VR-SKILL-005

`skill_category` shall be selected from the approved controlled vocabulary.

---

### VR-SKILL-006

`created_at` shall be assigned only once during record creation.

---

### VR-SKILL-007

`updated_at` shall be updated whenever the Skill record is modified.

---

### VR-SKILL-008

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-SKILL-009

Validation rules shall preserve the integrity of skill facts without introducing derived or inferred information.

---

## Relationships

The Skill entity is an independent domain entity owned by exactly one Person.

### Primary Relationships

Each Skill record shall reference exactly one Person through `person_id`.

A Person may own zero or more Skill records.

Employment records may reference zero or more Skill records as evidence that a Skill was demonstrated during an employment engagement.

Project records may reference zero or more Skill records as evidence that a Skill was demonstrated during a project.

Version 1 intentionally does not implement explicit relationship entities between Skill and Employment or between Skill and Project.

Skill records remain independently identifiable regardless of where the Skill was demonstrated.

---

### Planned Downstream Relationships

Future slices are expected to introduce relationships between Skill and the following domains:

- Employment
- Project
- Evidence
- Certification
- Generated Artifacts

These relationships represent architectural intent only and do not imply implemented foreign-key structures within Version 1.

---

### Transitional Relationship Strategy

Version 1 stores Skill as an independent entity owned by one Person.

Employment and Project preserve only their own factual information.

Future versions may introduce explicit relationship entities linking Skill to Employment and Project while preserving backward compatibility.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1.

### DD-SKILL-001

A dedicated Skill Category reference entity is deferred.

Version 1 assumes a controlled vocabulary without requiring a dedicated reference entity.

---

### DD-SKILL-002

Explicit Skill-to-Employment relationship entities are deferred.

Version 1 preserves skill facts without implementing many-to-many relationship structures.

---

### DD-SKILL-003

Explicit Skill-to-Project relationship entities are deferred.

Version 1 preserves skill facts without implementing many-to-many relationship structures.

---

### DD-SKILL-004

Skill proficiency, competency level, experience duration, endorsements, assessments, and rankings remain outside the scope of Slice 01.

---

### DD-SKILL-005

Evidence demonstrating Skill usage remains outside the Skill entity.

Future versions may introduce structured evidence linkage through dedicated relationship entities.

---

### DD-SKILL-006

Certification linkage is deferred until Certification becomes an independent domain entity.

---

## Future Extension Points

The Skill entity is intentionally designed for long-term extensibility.

### FEP-SKILL-001

Introduce a dedicated Skill Category reference entity.

---

### FEP-SKILL-002

Introduce explicit Skill-to-Employment relationship entities.

---

### FEP-SKILL-003

Introduce explicit Skill-to-Project relationship entities.

---

### FEP-SKILL-004

Support structured competency and proficiency frameworks.

---

### FEP-SKILL-005

Support certification linkage between Skill and Certification entities.

---

### FEP-SKILL-006

Support evidence linkage documenting where and how a Skill was demonstrated.

---

## Design Principles

The Skill entity shall remain:

- The canonical source of Skill facts.
- Owned by exactly one Person.
- Independent from Employment and Project lifecycle entities.
- Independent from generated career artifacts.
- Free from derived attributes.
- Extensible without requiring breaking schema changes.

Skill shall preserve factual professional knowledge while allowing future relationship expansion without duplicating domain truth.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |