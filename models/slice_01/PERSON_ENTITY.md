# Person Entity

**Status:** Approved Baseline  
**Version:** 1.0  
**Scope:** Slice 01  
**Level:** Entity Specification

---

## Purpose

The Person entity represents the canonical professional identity within the Career Operating System.

It serves as the primary source-of-truth for an individual's professional profile and acts as the root entity for all person-centered career information.

The Person entity stores only authoritative profile information. It does not store derived or generated content. Instead, it provides canonical data consumed by downstream domains and application services.

---

## Responsibilities

The Person entity is responsible for:

- Representing the canonical professional identity of the individual.
- Maintaining stable professional profile information.
- Acting as the root entity for all person-centered relationships.
- Providing canonical profile data consumed by application services.
- Providing authoritative information for CV generation, Cover Letter generation, LinkedIn profile generation, and other career artifacts.
- Maintaining references to related career records without duplicating their business data.

The Person entity is NOT responsible for:

- Managing employment history.
- Managing project information.
- Managing skills or competency records.
- Managing education records.
- Managing certification records.
- Managing evidence artifacts.
- Managing target roles.
- Managing job opportunities.
- Managing job applications.
- Storing generated content such as CVs, Cover Letters, LinkedIn summaries, or any other derived artifacts.

---

## Attributes

The Person entity defines the canonical professional profile of an individual.

### Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| person_id | Unique identifier for the person. |
| full_name | Official professional name. |
| professional_headline | Primary professional headline used across career platforms. |
| professional_summary | Canonical professional profile summary maintained by the user. |
| primary_email | Primary professional email address. |
| primary_phone | Primary contact number. |
| linkedin_url | LinkedIn profile URL. |
| github_url | GitHub profile URL. |
| portfolio_url | Personal portfolio or website URL. |
| current_location | Current city/country of residence. |
| preferred_location | Preferred work location(s). |
| work_authorization | Current work authorization or eligibility status. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| person_id | Yes | UUID | System-generated unique identifier. |
| full_name | Yes | String | Official professional name. |
| professional_headline | No | String | Primary professional headline. |
| professional_summary | No | Text | Canonical professional profile summary maintained by the user. |
| primary_email | No | String | Primary professional email address. |
| primary_phone | No | String | Primary contact number. |
| linkedin_url | No | URL | LinkedIn profile URL. |
| github_url | No | URL | GitHub profile URL. |
| portfolio_url | No | URL | Personal portfolio or website. |
| current_location | No | String | Current place of residence. |
| preferred_location | No | String | Preferred work location(s). |
| work_authorization | No | String | Current work authorization status. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-PER-001

There shall be exactly one canonical Person record for each Career Operating System profile.

---

### BR-PER-002

The Person entity shall be the authoritative source of professional identity information.

---

### BR-PER-003

The Person entity shall not contain employment, project, skill, education, certification, evidence, target role, job opportunity, or job application data.

---

### BR-PER-004

The Person entity shall not store generated or derived content.

Generated artifacts such as CV Versions, Cover Letter Versions, LinkedIn Snapshots, and similar outputs shall reference the Person entity but shall never replace it as the source-of-truth.

---

### BR-PER-005

Each Person shall be uniquely identifiable by its `person_id`.

---

### BR-PER-006

`primary_email` is optional.

If provided, it shall be unique within the Career Operating System.

---

### BR-PER-007

The Person entity may be referenced by multiple downstream entities while remaining the single authoritative professional profile.

---

### BR-PER-008

Profile information may evolve over time while preserving a single canonical identity.

---

## Validation Rules

### VR-PER-001

`person_id` shall be system-generated and immutable after creation.

---

### VR-PER-002

`full_name` is mandatory and shall not be empty.

---

### VR-PER-003

`primary_email` is optional.

If provided, it shall conform to a valid email format.

---

### VR-PER-004

`linkedin_url`, `github_url`, and `portfolio_url`, when provided, shall be valid URLs.

---

### VR-PER-005

`created_at` shall be assigned only once during record creation.

---

### VR-PER-006

`updated_at` shall be updated whenever the Person record is modified.

---

### VR-PER-007

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-PER-008

Validation rules shall preserve the integrity of the canonical Person profile without introducing derived data.

---

## Relationships

The Person entity acts as the root entity of the Career Operating System.

### Planned Downstream Relationships

Future slices are expected to introduce relationships between the Person entity and the following domains:

- Employment Records
- Project Records
- Skill Records
- Education Records
- Certification Records
- Evidence Items
- Target Roles
- Job Opportunities
- Job Applications
- Generated Artifacts

These relationships represent architectural intent for future slices. They do not imply implemented foreign-key structures within the current specification.

### Embedded Profile References (v1)

The following profile attributes remain embedded within the Person entity in Version 1:

- Current Location
- Preferred Location
- Work Authorization

These attributes may be extracted into dedicated shared or reference entities in future versions if independent lifecycle management becomes necessary.

### Relationship Principle

All downstream entities shall reference the Person entity through `person_id`.

The Person entity shall never duplicate business data owned by downstream entities.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1 to avoid premature modeling.

### DD-PER-001

Contact methods remain embedded within the Person entity.

A dedicated `ContactMethod` entity will only be introduced when multiple contact channels, verification status, communication preferences, or communication history require independent lifecycle management.

---

### DD-PER-002

Language preferences are intentionally deferred.

A dedicated `Language` entity may be introduced when multilingual profile support becomes a business requirement.

---

### DD-PER-003

Nationality is intentionally deferred.

It shall only become a first-class entity attribute when required by business, regulatory, or immigration workflows.

---

### DD-PER-004

Security clearance information is deferred until supported by a concrete business requirement.

---

### DD-PER-005

Mobility preferences, including relocation willingness, travel availability, remote work preference, hybrid work preference, and preferred countries, are deferred until the Career Targeting domain requires them.

---

### DD-PER-006

Profile versioning and audit history remain outside the scope of Slice 01.

---

## Future Extension Points

The Person entity is intentionally designed for long-term extensibility without requiring structural redesign.

### FEP-PER-001

Introduce a dedicated `ContactMethod` entity supporting:

- Multiple email addresses
- Multiple phone numbers
- Verification status
- Preferred communication channel
- Contact visibility settings

---

### FEP-PER-002

Introduce a dedicated `Language` entity supporting:

- Multiple languages
- Proficiency levels
- Reading, writing, listening, and speaking competencies

---

### FEP-PER-003

Introduce structured mobility preferences supporting:

- Relocation willingness
- Travel availability
- Remote work preference
- Hybrid work preference
- Preferred countries
- Preferred regions

---

### FEP-PER-004

Support profile versioning and complete audit history.

---

### FEP-PER-005

Support profile completeness scoring and AI-assisted profile quality assessment.

---

### FEP-PER-006

Support additional professional profile capabilities as future business requirements emerge while preserving backward compatibility.

---

## Design Principles

The Person entity shall remain:

- The canonical source of professional identity.
- Independent from downstream business domains.
- Free from generated or derived content.
- Stable across application versions.
- Extensible without requiring breaking schema changes.

The integrity of the Person entity shall always take precedence over convenience or duplication.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |