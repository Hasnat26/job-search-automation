# Evidence Entity

**Status:** Approved Baseline
**Version:** 1.0
**Scope:** Slice 01
**Level:** Entity Specification

---

## Purpose

The Evidence entity represents one authoritative piece of supporting evidence associated with a single Person within the Career Operating System.

Evidence supports the credibility and traceability of domain facts without becoming the source of those facts.

The Evidence entity stores only factual metadata describing evidence artifacts. It does not store domain facts, generated summaries, competency assessments, or derived information.

---

## Responsibilities

The Evidence entity is responsible for:

- Recording evidence metadata.
- Maintaining evidence ownership.
- Representing one evidence artifact per record.
- Recording evidence type.
- Recording evidence source information.
- Recording evidence location.
- Recording evidence integrity metadata.
- Maintaining authoritative evidence information.

The Evidence entity is NOT responsible for:

- Maintaining the Person profile.
- Maintaining Employment records.
- Maintaining Project records.
- Maintaining Skill records.
- Maintaining Company master data.
- Owning domain facts.
- Maintaining generated career artifacts.
- Storing derived credibility indicators.

---

## Ownership Principle

Evidence owns evidence metadata.

Each Evidence record belongs to exactly one Person through `person_id`.

Person owns professional identity.

Employment, Project, Skill, Certification, Education, and other domain entities may reference Evidence but shall never own evidence artifacts.

Generated outputs may reference Evidence but shall never become the authoritative source of evidence metadata.

---

## Attributes

The Evidence entity defines the canonical evidence inventory owned by one Person.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| evidence_id | Unique identifier for the Evidence record. |
| person_id | Reference to the owning Person entity. |
| evidence_type | Controlled classification of the evidence artifact. |
| title | Human-readable evidence title. |
| description | Optional factual description of the evidence. |
| source | Origin of the evidence artifact. |
| storage_location | Canonical storage reference or location. |
| issue_date | Date associated with the evidence when applicable. |
| created_at | Record creation timestamp. |
| updated_at | Last modification timestamp. |

---

## Attribute Specification

| Attribute | Mandatory | Type | Description |
|-----------|:---------:|------|-------------|
| evidence_id | Yes | UUID | System-generated unique identifier. |
| person_id | Yes | UUID | Reference to the owning Person entity. |
| evidence_type | Yes | Reference Value (Controlled Vocabulary) | Evidence classification selected from an approved controlled vocabulary. |
| title | Yes | String | Human-readable evidence title. |
| description | No | Text | Optional factual description of the evidence. |
| source | No | String | Origin of the evidence artifact. |
| storage_location | Yes | String | Canonical storage reference or location. |
| issue_date | No | Date | Date associated with the evidence when applicable. |
| created_at | Yes | Timestamp | Record creation timestamp. |
| updated_at | Yes | Timestamp | Last modification timestamp. |

---

## Business Rules

### BR-EVID-001

Each Evidence record shall belong to exactly one Person.

---

### BR-EVID-002

Each Evidence record shall represent one distinct evidence artifact.

---

### BR-EVID-003

Evidence shall be the authoritative source of evidence metadata.

Evidence metadata shall not be duplicated within Person, Employment, Project, Skill, or generated career artifacts.

---

### BR-EVID-004

Evidence shall not store generated or derived information.

Derived credibility assessments, confidence scores, verification outcomes, or other calculated information shall be produced by application services rather than stored within the Evidence entity.

---

### BR-EVID-005

Evidence may support one or more domain entities.

Version 1 does not structurally represent support relationships within the data model.

Version 1 stores only independent evidence metadata and ownership through `person_id`.

Explicit relationship entities linking Evidence to Employment, Project, Skill, Education, Certification, or other supported domains are intentionally deferred to future versions.

---

### BR-EVID-006

`evidence_type` shall be selected from an approved controlled vocabulary.

Free-text evidence classifications shall not be permitted.

---

### BR-EVID-007

Evidence records shall preserve factual evidence metadata.

Historical evidence metadata shall not be modified except to correct factual errors or update storage references when required.

---

### BR-EVID-008

Version 1 stores evidence independently of the entities it may support.

Future versions may introduce explicit relationship entities linking Evidence to Employment, Project, Skill, Certification, Education, and other supported domains while preserving backward compatibility.

---
## Validation Rules

### VR-EVID-001

`evidence_id` shall be system-generated and immutable after record creation.

---

### VR-EVID-002

`person_id` shall reference a valid Person record.

---

### VR-EVID-003

`evidence_type` shall be selected from the approved controlled vocabulary.

---

### VR-EVID-004

`title` is mandatory and shall not be empty.

---

### VR-EVID-005

`storage_location` is mandatory and shall not be empty.

---

### VR-EVID-006

`created_at` shall be assigned only once during record creation.

---

### VR-EVID-007

`updated_at` shall be updated whenever the Evidence record is modified.

---

### VR-EVID-008

Unknown or unavailable optional attributes shall be stored as `NULL` rather than placeholder values.

---

### VR-EVID-009

Validation rules shall preserve the integrity of evidence metadata without introducing derived or inferred information.

---

## Relationships

The Evidence entity is an independent domain entity owned by exactly one Person.

### Primary Relationships

Each Evidence record shall reference exactly one Person through `person_id`.

A Person may own zero or more Evidence records.

Version 1 does not structurally represent relationships between Evidence and supported domain entities.

Evidence records remain independently identifiable regardless of where they may later be referenced.

Support relationships are architectural intent only and are intentionally deferred beyond Version 1.

---

### Planned Downstream Relationships

Future slices are expected to introduce relationships between Evidence and the following domains:

- Employment
- Project
- Skill
- Education
- Certification
- Company
- Generated Artifacts

These relationships represent architectural intent only and do not imply implemented foreign-key structures within Version 1.

---

### Transitional Relationship Strategy

Version 1 stores Evidence independently from all supported domain entities.

Employment, Project, Skill, Education, Certification, and other entities preserve only their own factual information.

Future versions may introduce explicit relationship entities linking Evidence to supported domains while preserving backward compatibility.

---

## Deferred Design Decisions

The following design decisions are intentionally deferred beyond Version 1.

### DD-EVID-001

A dedicated Evidence Type reference entity is deferred.

Version 1 assumes a controlled vocabulary without requiring a dedicated reference entity.

---

### DD-EVID-002

Explicit relationship entities between Evidence and supported domain entities are deferred.

Version 1 preserves evidence metadata without implementing many-to-many relationship structures.

---

### DD-EVID-003

Evidence verification workflows are deferred.

Verification status, reviewer information, approval history, and audit workflows remain outside the scope of Slice 01.

---

### DD-EVID-004

Evidence versioning is deferred.

Version 1 manages a single canonical metadata record for each evidence artifact.

---

### DD-EVID-005

Cryptographic integrity validation, digital signatures, checksums, and immutable audit capabilities are deferred.

---

### DD-EVID-006

Physical file lifecycle management remains outside the scope of Slice 01.

Version 1 stores only canonical metadata and storage references.

---

## Future Extension Points

The Evidence entity is intentionally designed for long-term extensibility.

### FEP-EVID-001

Introduce a dedicated Evidence Type reference entity.

---

### FEP-EVID-002

Introduce explicit relationship entities linking Evidence to Employment, Project, Skill, Education, Certification, Company, and other supported domains.

---

### FEP-EVID-003

Support evidence verification workflows and approval history.

---

### FEP-EVID-004

Support evidence versioning and lifecycle management.

---

### FEP-EVID-005

Support cryptographic integrity verification, digital signatures, and immutable audit records.

---

### FEP-EVID-006

Support external document repositories and object-storage providers while preserving canonical metadata ownership.

---

## Design Principles

The Evidence entity shall remain:

- The canonical source of evidence metadata.
- Owned by exactly one Person.
- Independent from the lifecycle of all supported domain entities.
- Independent from generated career artifacts.
- Free from derived attributes.
- Extensible without requiring breaking schema changes.

Evidence shall preserve authoritative proof metadata while allowing future relationship expansion without duplicating evidence across domain entities.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 0.1 | Working Draft | Initial working specification. |
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |