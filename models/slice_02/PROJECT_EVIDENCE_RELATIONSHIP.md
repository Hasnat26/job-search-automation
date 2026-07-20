# PROJECT_EVIDENCE_RELATIONSHIP

## Purpose

Defines the association between Project and Evidence entities.

The relationship stores only association-specific metadata and owns neither referenced entity.

---

## Scope

This relationship defines:

- associations between Project and Evidence;
- project evidence usage;
- relationship-specific metadata;
- project evidence context.

This relationship does **not** define:

- Project entities;
- Evidence entities;
- Person entities;
- evidence storage or content.

---

## Domain Definition

Each Project Evidence Relationship shall reference exactly one Project entity and one Evidence entity.

A Project may be associated with multiple Evidence records.

An Evidence record may be associated with multiple Project entities.

The Project Evidence Relationship maintains its own association metadata but cannot exist without valid referenced Project and Evidence entities.

---

## Ownership

The Project Evidence Relationship owns only relationship-specific metadata.

Ownership of Project and Evidence remains with their respective canonical entities.

---

## Business Rules

### BR-PjER-001

Each relationship shall reference exactly one Project entity.

---

### BR-PjER-002

Each relationship shall reference exactly one Evidence entity.

---

### BR-PjER-003

A Project may be associated with multiple Evidence records.

---

### BR-PjER-004

An Evidence record may be associated with multiple Project entities.

---

### BR-PjER-005

Relationship metadata shall not modify or redefine the canonical Evidence entity.

---

### BR-PjER-006

Relationship metadata shall not modify or redefine the canonical Project entity.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| relationship_id | Unique identifier of the relationship. |
| project_id | Reference to the associated Project entity. |
| evidence_id | Reference to the associated Evidence entity. |
| relationship_type | Optional classification describing how the Evidence relates to the Project. |
| notes | Optional relationship-specific notes. |

---

## Attribute Specification

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| relationship_id | Yes | UUID | Unique identifier assigned to the relationship. |
| project_id | Yes | UUID | Reference to the associated Project entity. |
| evidence_id | Yes | UUID | Reference to the associated Evidence entity. |
| relationship_type | No | Enumeration | Optional classification describing the relationship between the Project and Evidence entities. |
| notes | No | String | Optional relationship-specific notes. |

---

## Validation Rules

### BR-PjER-007

`relationship_id` shall be unique across all Project Evidence Relationship records.

---

### BR-PjER-008

`project_id` shall reference an existing Project entity.

---

### BR-PjER-009

`evidence_id` shall reference an existing Evidence entity.

---

### BR-PjER-010

The combination of `project_id` and `evidence_id` shall be unique.

Duplicate relationships between the same Project and Evidence are not permitted.

---

### BR-PjER-011

`relationship_type`, when provided, shall contain only approved enumeration values.

The relationship type represents the nature of the association between the Project and Evidence entities.

It does not modify or redefine the canonical Evidence entity.

Recommended values include:

- Primary
- Supporting
- Verification
- Contextual

Implementations may extend this enumeration while preserving semantic compatibility.

---

### BR-PjER-012

`notes`, when provided, shall contain only relationship-specific contextual information.

It shall not duplicate or redefine canonical Project or Evidence information.

---

## Lifecycle

The Project Evidence Relationship maintains its own relationship-specific metadata.

However, it cannot exist without valid referenced Project and Evidence entities.

Changes to the lifecycle of either referenced entity may require the relationship to be archived or removed according to implementation policy.

---

## Relationship Constraints

This entity owns only relationship-specific metadata.

It shall not:

- duplicate Project attributes;
- duplicate Evidence attributes;
- redefine canonical entity information;
- establish ownership over Project or Evidence.

---

## Future Evolution

Future versions may introduce additional capabilities, including:

- evidence validity periods;
- evidence verification status;
- confidence or trust indicators;
- reviewer annotations;
- evidence sequencing or prioritization.

Such additions shall preserve the canonical ownership boundaries established by the Project and Evidence entities.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Baseline Pending Validation | First review-ready specification for Slice 02. |