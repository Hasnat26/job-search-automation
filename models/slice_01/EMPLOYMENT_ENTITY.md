# Employment Entity

**Status:** Approved Baseline
**Version:** 1.0
**Scope:** Slice 01
**Level:** Entity Specification

---

## Purpose

The Employment entity represents one professional employment engagement within the Career Operating System.

It records one factual employment engagement within an individual's professional history.

Employment is a lifecycle entity. Each record represents one distinct employment engagement and preserves its historical integrity regardless of subsequent career changes.

The Employment entity stores only authoritative employment facts. It does not store generated content, profile summaries, or derived information.

---

## Responsibilities

The Employment entity is responsible for:

- Recording factual employment engagements.
- Preserving employment history.
- Representing one employment engagement per record.
- Maintaining authoritative employment information.
- Recording employer identification for the employment engagement.
- Recording employment dates.
- Recording professional responsibilities performed during the engagement.
- Recording significant achievements accomplished during the engagement.
- Recording technologies, platforms, systems, and tools materially associated with the engagement.

The Employment entity is NOT responsible for:

- Maintaining the Person profile.
- Managing Company master data.
- Managing Project records.
- Managing Skill records.
- Managing Education records.
- Managing Certification records.
- Managing Evidence artifacts.
- Managing generated career artifacts.
- Storing derived employment indicators.

---

## Ownership Principle

Employment owns employment facts.

The Person entity may reference employment context but shall never duplicate employment facts.

Generated outputs may present, summarize, transform, or format employment facts but shall never become the authoritative source of those facts.

---

## Attributes

The Employment entity defines the canonical employment history associated with a single Person.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| employment_id | Unique identifier for the Employment record. |
| person_id | Reference to the owning Person entity. |
| company_name | Canonical employer identifier in Version 1. This is an intentional transitional modeling decision pending introduction of a dedicated Company entity. |
| job_title | Official position held during the employment. |
| department | Organizational department or business unit. |
| employment_type | Controlled classification of the employment relationship. |
| start_date | Employment commencement date. |
| end_date | Employment completion date when applicable. |
| location | Primary work location. |
| responsibilities | Principal responsibilities performed during the employment. |
| achievements | Significant accomplishments achieved during the employment. |
| technologies_used | Technologies, systems, platforms, frameworks, and tools materially associated with the employment. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| employment_id | Yes | UUID | System-generated unique identifier. |
| person_id | Yes | UUID | Reference to the owning Person entity. |
| company_name | Yes | String | Canonical employer identifier used in Version 1. |
| job_title | Yes | String | Official employment title. |
| department | No | String | Organizational department or business unit. |
| employment_type | Yes | Reference Value (Controlled Vocabulary) | Employment classification selected from an approved controlled vocabulary. |
| start_date | Yes | Date | Employment commencement date. |
| end_date | No | Date | Employment completion date. `NULL` indicates an ongoing employment engagement unless otherwise explicitly specified. |
| location | No | String | Primary employment location. |
| responsibilities | No | Text | Principal responsibilities performed during the employment. |
| achievements | No | Text | Significant accomplishments achieved during the employment. |
| technologies_used | No | Logical List<String> | Technologies, systems, platforms, frameworks, or tools materially associated with the employment. Physical storage is implementation-specific. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-EMP-001

Each Employment record shall belong to exactly one Person.

---

### BR-EMP-002

Each Employment record shall represent one distinct employment engagement.

---

### BR-EMP-003

Employment shall be the authoritative source of employment facts.

Employment facts shall not be duplicated within the Person entity or within generated career artifacts.

---

### BR-EMP-004

Employment shall not store generated or derived information.

Derived profile indicators shall be computed by application services rather than stored within the Employment entity.

---

### BR-EMP-005

Employment periods may overlap when they represent legitimately concurrent roles, including part-time work, consulting engagements, contract assignments, advisory roles, or other concurrent employment arrangements.

The system shall not assume that overlapping Employment records are invalid by default.

Validation of employment overlap shall be governed by business rules rather than date comparisons alone.

---

### BR-EMP-006

An Employment record is considered active when `end_date` is `NULL` or otherwise explicitly indicates an ongoing engagement.

A Person may have more than one active Employment record when concurrent employment is permitted by applicable business rules.

---

### BR-EMP-007

`employment_type` shall be selected from an approved controlled vocabulary.

Free-text employment classifications shall not be permitted.

---

### BR-EMP-008

Version 1 uses `company_name` as the canonical employer identifier.

This is an intentional transitional modeling decision.

No additional employer-identification attributes shall be introduced before migration to a dedicated Company entity.

---

### BR-EMP-009

Future versions may replace `company_name` with a reference to a dedicated Company entity (`company_id`).

The migration shall preserve backward compatibility while maintaining a single canonical employer identifier throughout the transition.

---

### BR-EMP-010

Employment records shall preserve historical facts.

Historical employment information shall not be modified to reflect subsequent organizational restructuring, company renaming, title standardization, or other later events unless correcting factual errors.

---

## Validation Rules

### VR-EMP-001

`employment_id` shall be system-generated and immutable after record creation.

---

### VR-EMP-002

`person_id` shall reference a valid Person record.

---

### VR-EMP-003

`company_name` is mandatory in Version 1 and shall not be empty.

---

### VR-EMP-004

`job_title` is mandatory and shall not be empty.

---

### VR-EMP-005

`employment_type` shall be selected from the approved controlled vocabulary.

---

### VR-EMP-006

`start_date` shall be provided for every Employment record.

---

### VR-EMP-007

If `end_date` is provided, it shall not precede `start_date`.

---

### VR-EMP-008

`created_at` shall be assigned only once during record creation.

---

### VR-EMP-009

`updated_at` shall be updated whenever the Employment record is modified.

---

### VR-EMP-010

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-EMP-011

Validation rules shall preserve the integrity of employment facts without introducing derived or inferred information.

---

## Relationships

The Employment entity is a lifecycle entity owned by a single Person.

### Primary Relationships

Each Employment record shall reference exactly one Person.

A Person may own zero or more Employment records.

---

### Planned Downstream Relationships

Future slices are expected to introduce relationships between Employment and the following domains:

- Company
- Project
- Skill
- Evidence
- Generated Artifacts

These relationships represent architectural intent only and do not imply implemented foreign-key structures within Version 1.

---

### Transitional Employer Reference

Version 1 identifies employers using `company_name`.

This is an intentional transitional modeling decision.

Future versions may replace `company_name` with a reference to a dedicated Company entity while preserving backward compatibility.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1.

### DD-EMP-001

A dedicated Company entity is deferred until employer information requires independent lifecycle management.

---

### DD-EMP-002

Employment Type reference management is deferred.

Version 1 assumes a controlled vocabulary without requiring a dedicated reference entity.

---

### DD-EMP-003

Responsibilities remain embedded narrative content.

They may become structured records only when independent lifecycle requirements emerge.

---

### DD-EMP-004

Achievements remain embedded narrative content.

Separate Achievement entities are deferred until justified by future business requirements.

---

### DD-EMP-005

Technologies Used remain embedded within Employment.

Future versions may introduce structured Technology references shared across Employment and Project entities.

---

### DD-EMP-006

Employment verification, employer references, and supporting evidence remain outside the scope of Slice 01.

---

## Future Extension Points

The Employment entity is intentionally designed for long-term extensibility.

### FEP-EMP-001

Introduce a dedicated Company entity referenced through `company_id`.

---

### FEP-EMP-002

Introduce a controlled Employment Type reference entity.

---

### FEP-EMP-003

Support structured Responsibilities linked to competency frameworks.

---

### FEP-EMP-004

Support structured Achievement records with measurable outcomes.

---

### FEP-EMP-005

Support shared Technology references reusable across Employment and Project entities.

---

### FEP-EMP-006

Support employment verification, employer references, evidence linkage, and externally verifiable employment credentials.

---

## Design Principles

The Employment entity shall remain:

- The canonical source of employment facts.
- A lifecycle entity owned by exactly one Person.
- Independent from generated career artifacts.
- Free from derived attributes.
- Extensible without requiring breaking schema changes.

Employment shall preserve historical accuracy while supporting future architectural evolution.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |