# PERSON_CERTIFICATION_RELATIONSHIP

## Purpose

Defines the association between Person and Certification entities.

The relationship stores person-specific certification ownership and association metadata while owning neither referenced entity.

---

## Scope

This relationship defines:

- associations between Person and Certification;
- person-specific certification ownership;
- certification acquisition details;
- relationship-specific metadata.

This relationship does **not** define:

- Person entities;
- Certification entities;
- certification definitions;
- certification issuer definitions.

---

## Domain Definition

Each Person Certification Relationship shall reference exactly one Person entity and one Certification entity.

A Person may be be associated with multiple Certification records.

A Certification entity may be associated with multiple Person entities.

The Person Certification Relationship stores person-specific certification information while maintaining references to the canonical Person and Certification entities.

The relationship cannot exist without valid referenced Person and Certification entities.

---

## Ownership

The Person Certification Relationship owns only person-specific certification metadata.

Ownership of Person remains with the Person entity.

Ownership of Certification definition remains with the Certification entity.

---

## Business Rules

### BR-PCR-001

Each relationship shall reference exactly one Person entity.

---

### BR-PCR-002

Each relationship shall reference exactly one Certification entity.

---

### BR-PCR-003

A Person may be associated with multiple Certification entities.

---

### BR-PCR-004

A Certification entity may be associated with multiple Person entities.

---

### BR-PCR-005

Relationship metadata shall not modify or redefine the canonical Person entity.

---

### BR-PCR-006

Relationship metadata shall not modify or redefine the canonical Certification entity.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| relationship_id | Unique identifier of the relationship. |
| person_id | Reference to the associated Person entity. |
| certification_id | Reference to the associated Certification entity. |
| issue_date | Date the certification was issued to the Person. |
| expiry_date | Certification expiration date for the Person, when applicable. |
| credential_id | Credential or certificate identifier assigned to the Person. |
| verification_status | Verification state of the person's certification. |
| notes | Optional relationship-specific notes. |

---

## Attribute Specification

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| relationship_id | Yes | UUID | Unique identifier assigned to the relationship. |
| person_id | Yes | UUID | Reference to the associated Person entity. |
| certification_id | Yes | UUID | Reference to the associated Certification entity. |
| issue_date | No | Date | Date the certification was issued. |
| expiry_date | No | Date | Expiration date of the certification, if applicable. |
| credential_id | No | String | Person-specific credential or certificate identifier. |
| verification_status | No | Enumeration | Verification state of the certification. |
| notes | No | String | Optional relationship-specific notes. |

---

## Validation Rules

### BR-PCR-007

`relationship_id` shall be unique across all Person Certification Relationship records.

---

### BR-PCR-008

`person_id` shall reference an existing Person entity.

---

### BR-PCR-009

`certification_id` shall reference an existing Certification entity.

---

### BR-PCR-010

The combination of `person_id`, `certification_id`, and `credential_id` shall be unique.

---

### BR-PCR-011

`verification_status`, when provided, shall contain only approved enumeration values.

Recommended values include:

- Pending
- Verified
- Expired
- Revoked

Implementations may extend this enumeration while preserving semantic compatibility.

---

### BR-PCR-012

If both `issue_date` and `expiry_date` are provided, `expiry_date` shall not be earlier than `issue_date`.

---

### BR-PCR-013

`notes`, when provided, shall contain only relationship-specific contextual information.

It shall not duplicate or redefine canonical Person or Certification information.

---

## Lifecycle

The Person Certification Relationship maintains its own relationship-specific metadata.

However, it cannot exist without valid referenced Person and Certification entities.

Changes to the lifecycle of either referenced entity may require the relationship to be archived or removed according to implementation policy.

---

## Relationship Constraints

This entity owns only person-specific certification metadata.

It shall not:

- duplicate Person attributes;
- duplicate Certification definition attributes;
- redefine canonical entity information;
- establish ownership over Person or Certification.

---

## Future Evolution

Future versions may introduce additional capabilities, including:

- renewal history;
- continuing education credits;
- digital badge references;
- certification attachments;
- audit history.

Such additions shall preserve the canonical ownership boundaries established by the Person and Certification entities.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Baseline Pending Validation | First review-ready specification for Slice 02. |