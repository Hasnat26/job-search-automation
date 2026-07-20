# Certification Entity

**Status:** Approved Baseline
**Version:** 1.0
**Scope:** Slice 01
**Level:** Entity Specification

---

## Purpose

The Certification entity represents one professional certification, license, accreditation, or vendor-issued credential associated with a single Person within the Career Operating System.

Certification preserves factual credential history without representing educational history, professional skills, employment history, or generated career artifacts.

The Certification entity stores only factual certification metadata. It does not store competency assessments, generated summaries, verification outcomes, or derived information.

---

## Responsibilities

The Certification entity is responsible for:

- Recording certification history.
- Maintaining certification ownership.
- Representing one certification or credential per record.
- Recording issuing organization information.
- Recording certification details.
- Recording certification validity information.
- Maintaining authoritative certification metadata.

The Certification entity is NOT responsible for:

- Maintaining the Person profile.
- Maintaining Employment records.
- Maintaining Project records.
- Maintaining Skill records.
- Maintaining Education records.
- Maintaining Company master data.
- Owning supporting evidence.
- Maintaining generated career artifacts.
- Storing derived competency information.

---

## Ownership Principle

Certification owns certification metadata.

Each Certification record belongs to exactly one Person through `person_id`.

Person owns professional identity.

Evidence may support Certification but shall never own certification facts.

Generated outputs may reference Certification but shall never become the authoritative source of certification metadata.

---

## Attributes

The Certification entity defines the canonical certification inventory owned by one Person.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| certification_id | Unique identifier for the Certification record. |
| person_id | Reference to the owning Person entity. |
| certification_name | Official name of the certification or credential. |
| issuing_organization | Organization that issued the certification. |
| credential_identifier | Optional credential or certificate identifier. |
| issue_date | Certification issue date. |
| expiration_date | Certification expiration date when applicable. |
| description | Optional factual description of the certification. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| certification_id | Yes | UUID | System-generated unique identifier. |
| person_id | Yes | UUID | Reference to the owning Person entity. |
| certification_name | Yes | String | Official certification or credential name. |
| issuing_organization | Yes | String | Organization that issued the certification. |
| credential_identifier | No | String | Optional credential or certificate identifier. |
| issue_date | No | Date | Certification issue date. |
| expiration_date | No | Date | Certification expiration date when applicable. |
| description | No | Text | Optional factual description. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-CERT-001

Each Certification record shall belong to exactly one Person.

---

### BR-CERT-002

Each Certification record shall represent one distinct professional certification or credential.

---

### BR-CERT-003

Certification shall be the authoritative source of certification metadata.

Certification metadata shall not be duplicated within Person, Employment, Project, Skill, Education, Evidence, or generated career artifacts.

---

### BR-CERT-004

Certification shall not store generated or derived information.

Derived competency assessments, verification outcomes, confidence scores, renewal predictions, or other calculated information shall be produced by application services rather than stored within the Certification entity.

---

### BR-CERT-005

Certification stores only factual certification information.

Version 1 does not structurally represent relationships between Certification and Skill, Education, or Evidence.

Explicit relationship entities are intentionally deferred to future versions.

---

### BR-CERT-006

Issuing organizations shall be stored as factual values.

Version 1 does not require a canonical Organization reference entity.

---

### BR-CERT-007

Certification records shall preserve factual certification history.

Historical certification records shall not be modified except to correct factual errors.

---

### BR-CERT-008

Version 1 stores Certification independently of other supported domain entities.

Future versions may introduce explicit relationship entities linking Certification to Evidence, Skill, Education, Organization, and other supported domains while preserving backward compatibility.

---
## Validation Rules

### VR-CERT-001

`certification_id` shall be system-generated and immutable after record creation.

---

### VR-CERT-002

`person_id` shall reference a valid Person record.

---

### VR-CERT-003

`certification_name` is mandatory and shall not be empty.

---

### VR-CERT-004

`issuing_organization` is mandatory and shall not be empty.

---

### VR-CERT-005

If both `issue_date` and `expiration_date` are present, `issue_date` shall not occur after `expiration_date`.

---

### VR-CERT-006

`created_at` shall be assigned only once during record creation.

---

### VR-CERT-007

`updated_at` shall be updated whenever the Certification record is modified.

---

### VR-CERT-008

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-CERT-009

Validation rules shall preserve the integrity of certification metadata without introducing derived or inferred information.

---

## Relationships

The Certification entity is an independent domain entity owned by exactly one Person.

### Primary Relationships

Each Certification record shall reference exactly one Person through `person_id`.

A Person may own zero or more Certification records.

Version 1 does not structurally represent relationships between Certification and other supported domain entities.

Certification records remain independently identifiable regardless of where they may later be referenced.

Relationships to Evidence, Skill, Education, Organization, or other supported domains are architectural intent only and are intentionally deferred beyond Version 1.

---

### Planned Downstream Relationships

Future slices are expected to introduce relationships between Certification and the following domains:

- Evidence
- Skill
- Education
- Organization
- Generated Artifacts

These relationships represent architectural intent only and do not imply implemented foreign-key structures within Version 1.

---

### Transitional Relationship Strategy

Version 1 stores Certification independently from all supported domain entities.

Evidence, Skill, Education, and other entities preserve only their own factual information.

Future versions may introduce explicit relationship entities linking Certification to supported domains while preserving backward compatibility.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1.

### DD-CERT-001

A dedicated Organization reference entity is deferred.

Version 1 stores issuing organization names as factual values without requiring a canonical Organization entity.

---

### DD-CERT-002

Explicit relationship entities between Certification and supported domain entities are deferred.

Version 1 preserves certification metadata without implementing many-to-many relationship structures.

---

### DD-CERT-003

Certification verification workflows are deferred.

Verification status, reviewer information, approval history, renewal workflows, and audit capabilities remain outside the scope of Slice 01.

---

### DD-CERT-004

Certification versioning is deferred.

Version 1 manages a single canonical metadata record for each certification.

---

### DD-CERT-005

Certification renewal management, continuing education requirements, competency scoring, and credential lifecycle automation remain outside the scope of Slice 01.

---

### DD-CERT-006

Supporting evidence linkage is deferred until explicit relationship entities are introduced.

---

## Future Extension Points

The Certification entity is intentionally designed for long-term extensibility.

### FEP-CERT-001

Introduce a dedicated Organization reference entity.

---

### FEP-CERT-002

Introduce explicit relationship entities linking Certification to Evidence, Skill, Education, Organization, and other supported domains.

---

### FEP-CERT-003

Support certification verification workflows, renewal history, and approval records.

---

### FEP-CERT-004

Support certification versioning and credential lifecycle management.

---

### FEP-CERT-005

Support continuing education requirements, renewal tracking, and structured credential management.

---

### FEP-CERT-006

Support evidence linkage documenting certification issuance, renewal, and verification.

---

## Design Principles

The Certification entity shall remain:

- The canonical source of certification metadata.
- Owned by exactly one Person.
- Independent from the lifecycle of other domain entities.
- Independent from generated career artifacts.
- Free from derived attributes.
- Extensible without requiring breaking schema changes.

Certification shall preserve authoritative credential history while allowing future relationship expansion without duplicating domain truth.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |