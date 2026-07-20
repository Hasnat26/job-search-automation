# Project Entity

**Status:** Approved Baseline
**Version:** 1.0
**Scope:** Slice 01
**Level:** Entity Specification

---

## Purpose

The Project entity represents one distinct professional project or major work engagement completed or significantly contributed to by a Person during the individual's professional career.

Each Project record preserves one factual project engagement independently of resumes, CVs, generated profiles, or other presentation artifacts.

The Project entity stores only authoritative project facts. It does not store generated summaries, inferred competencies, calculated metrics, or derived information.

---

## Responsibilities

The Project entity is responsible for:

- Recording factual project information.
- Preserving project history.
- Representing one distinct project per record.
- Recording project scope and objectives.
- Recording the individual's role within the project.
- Recording project responsibilities.
- Recording measurable project achievements when available.
- Recording technologies, systems, platforms, frameworks, and tools materially associated with the project.
- Maintaining authoritative project information.

The Project entity is NOT responsible for:

- Maintaining the Person profile.
- Maintaining Employment records.
- Maintaining Company master data.
- Maintaining Skill records.
- Maintaining Evidence artifacts.
- Maintaining generated career artifacts.
- Storing derived project indicators.

---

## Ownership Principle

Project owns project facts.

Person owns professional identity.

Employment owns employment facts.

Generated outputs may reference, summarize, or transform project information but shall never become the authoritative source of project facts.

---

## Attributes

The Project entity defines the canonical project history associated with an individual's professional career.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| project_id | Unique identifier for the Project record. |
| project_name | Official or commonly recognized project name. |
| project_type | Controlled classification of the project. |
| client_name | Client, owner, or end customer when applicable. |
| organization_name | Organization responsible for project execution in Version 1. |
| role | Primary role performed within the project. |
| description | Objective factual description of the project. |
| start_date | Project commencement date. |
| end_date | Project completion date when applicable. |
| location | Primary project location. |
| responsibilities | Principal responsibilities performed within the project. |
| achievements | Significant measurable project achievements. |
| technologies_used | Technologies, systems, platforms, frameworks, and tools materially associated with the project. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| project_id | Yes | UUID | System-generated unique identifier. |
| project_name | Yes | String | Official or commonly recognized project name. |
| project_type | Yes | Reference Value (Controlled Vocabulary) | Project classification selected from an approved controlled vocabulary. |
| client_name | No | String | Client, owner, or end customer. |
| organization_name | No | String | Executing organization in Version 1. |
| role | Yes | String | Primary role performed within the project. |
| description | No | Text | Objective factual project description. |
| start_date | No | Date | Project commencement date. |
| end_date | No | Date | Project completion date. |
| location | No | String | Primary project location. |
| responsibilities | No | Text | Principal responsibilities performed. |
| achievements | No | Text | Significant measurable project achievements. |
| technologies_used | No | Logical List<String> | Technologies, systems, platforms, frameworks, and tools materially associated with the project. Physical storage is implementation-specific. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-PROJ-001

Each Project record shall represent one distinct project.

---

### BR-PROJ-002

Project shall be the authoritative source of project facts.

Project facts shall not be duplicated within the Person entity, Employment entity, or generated career artifacts.

---

### BR-PROJ-003

Project shall not store generated or derived information.

Derived metrics, competency assessments, portfolio summaries, and other calculated information shall be produced by application services rather than stored within the Project entity.

---

### BR-PROJ-004

A Project may span multiple Employment engagements throughout an individual's professional history.

The Project entity remains independent of Employment lifecycle boundaries.

---

### BR-PROJ-005

Multiple Persons may participate in the same real-world project.

Version 1 models projects from the perspective of a single career repository and does not attempt to represent cross-person collaboration.

---

### BR-PROJ-006

`project_type` shall be selected from an approved controlled vocabulary.

Free-text project classifications shall not be permitted.

---

### BR-PROJ-007

Project records shall preserve factual historical information.

Historical project information shall not be modified to reflect subsequent organizational restructuring, client renaming, technology upgrades, or later business events unless correcting factual errors.

---

### BR-PROJ-008

Version 1 stores `organization_name` as the canonical organization identifier.

This is an intentional transitional modeling decision.

Future versions may replace `organization_name` with a reference to a dedicated Company entity (`company_id`) while preserving backward compatibility.

---

## Validation Rules

### VR-PROJ-001

`project_id` shall be system-generated and immutable after record creation.

---

### VR-PROJ-002

`project_name` is mandatory and shall not be empty.

---

### VR-PROJ-003

`project_type` shall be selected from the approved controlled vocabulary.

---

### VR-PROJ-004

`role` is mandatory and shall not be empty.

---

### VR-PROJ-005

If both `start_date` and `end_date` are provided, `end_date` shall not precede `start_date`.

---

### VR-PROJ-006

`created_at` shall be assigned only once during record creation.

---

### VR-PROJ-007

`updated_at` shall be updated whenever the Project record is modified.

---

### VR-PROJ-008

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-PROJ-009

Validation rules shall preserve the integrity of project facts without introducing derived or inferred information.

---

## Relationships

The Project entity is a lifecycle entity representing one distinct professional project within a Person's career history.

### Primary Relationships

A Person may own zero or more Project records.

A Project may be associated with zero, one, or multiple Employment engagements during an individual's career.

Version 1 intentionally does not implement explicit relationship entities between Project and Employment.

Project records remain independently identifiable regardless of Employment associations.

---

### Planned Downstream Relationships

Future slices are expected to introduce relationships between Project and the following domains:

- Person
- Employment
- Company
- Skill
- Evidence
- Generated Artifacts

These relationships represent architectural intent only and do not imply implemented foreign-key structures within Version 1.

---

### Transitional Organization Reference

Version 1 identifies the executing organization using `organization_name`.

This is the canonical organization identifier for Version 1 and remains intentionally independent of any future Company entity.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1.

### DD-PROJ-001

A dedicated Company entity is deferred until organizations require independent lifecycle management.

---

### DD-PROJ-002

Project Type reference management is deferred.

Version 1 assumes a controlled vocabulary without requiring a dedicated reference entity.

---

### DD-PROJ-003

Explicit Project-to-Employment relationship entities are deferred.

Version 1 preserves project facts without implementing many-to-many relationship structures.

---

### DD-PROJ-004

Responsibilities remain embedded narrative content.

They may become structured records only when independent lifecycle requirements emerge.

---

### DD-PROJ-005

Achievements remain embedded narrative content.

Separate Achievement entities are deferred until justified by future business requirements.

---

### DD-PROJ-006

Technologies Used remain embedded within Project.

Future versions may introduce structured Technology references shared across Project and Employment entities.

---

### DD-PROJ-007

Project evidence, deliverables, verification records, and supporting documentation remain outside the scope of Slice 01.

---

## Future Extension Points

The Project entity is intentionally designed for long-term extensibility.

### FEP-PROJ-001

Introduce a dedicated Company entity referenced through `company_id`.

---

### FEP-PROJ-002

Introduce a controlled Project Type reference entity.

---

### FEP-PROJ-003

Introduce explicit Project-to-Employment relationship entities.

---

### FEP-PROJ-004

Support structured Responsibilities linked to competency frameworks.

---

### FEP-PROJ-005

Support structured Achievement records with measurable outcomes.

---

### FEP-PROJ-006

Support shared Technology references reusable across Project and Employment entities.

---

### FEP-PROJ-007

Support project evidence, deliverables, verification records, and traceable supporting documentation.

---

## Design Principles

The Project entity shall remain:

- The canonical source of project facts.
- Independent from Employment lifecycle boundaries.
- Independent from generated career artifacts.
- Free from derived attributes.
- Extensible without requiring breaking schema changes.

Project shall preserve historical accuracy while supporting future architectural evolution.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |