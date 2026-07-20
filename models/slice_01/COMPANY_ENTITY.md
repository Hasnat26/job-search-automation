# COMPANY_ENTITY

## Purpose

The Company entity defines the canonical representation of a business organization within the domain model.

It serves as the first approved shared/reference entity in Slice 01 and provides a normalized identity for company-related information referenced across multiple domain entities.

This entity represents organizational identity only. It does not model employment relationships, organizational hierarchy, physical facilities, or business operations.

---

## Scope

The Company entity defines the canonical business identity of an organization.

It includes:

- company identity;
- company naming;
- business status;
- external reference identifiers;
- basic descriptive metadata.

It does not define:

- employee relationships;
- customer or supplier relationships;
- organizational structure;
- office or facility locations;
- legal ownership structures;
- project participation.

These concerns belong to other domain entities or future relationship models.

---

## Domain Definition

A Company represents a unique business organization recognized as a reusable reference throughout the domain model.

Company exists independently of any individual person, employment record, project, or certification.

A Company may be referenced by multiple domain entities while maintaining a single canonical identity.

---

## Ownership

Company is a shared/reference entity.

It owns only its own canonical organizational information.

Other entities may reference Company but shall not duplicate or redefine Company identity.

---

## Business Rules

### BR-COMP-001

Each Company represents one canonical business organization.

---

### BR-COMP-002

Company identity shall remain independent of Employment, Project, Education, Certification, or Person entities.

---

### BR-COMP-003

Multiple domain entities may reference the same Company.

---

### BR-COMP-004

Company shall not contain employment-specific information.

---

### BR-COMP-005

Company shall not represent educational institutions or certification authorities.

Those concepts remain outside the scope of this entity under DDR-001.

---

### BR-COMP-006

Company normalization shall follow the governance rules defined by DDR-001.

---

## Attribute Inventory

| Attribute | Description |
|----------|-------------|
| company_id | Unique identifier of the company. |
| legal_name | Official legal business name. |
| display_name | Commonly used business name, if different from the legal name. |
| company_status | Operational status of the company. |
| website | Official company website, if available. |
| country | Country associated with the company headquarters or primary registration. |
| notes | Optional administrative notes. |
---

## Attribute Specification

| Attribute | Required | Type | Description |
|----------|----------|------|-------------|
| company_id | Yes | UUID | Unique identifier assigned to the company. |
| legal_name | Yes | String | Official legal business name. |
| display_name | No | String | Commonly used or commercial business name. |
| company_status | Yes | Enumeration | Current operational status of the company. |
| website | No | URL | Official company website. |
| country | No | String | Country associated with the company's primary registration or headquarters. This remains a transitional factual attribute until geographic normalization is introduced. |
| notes | No | String | Optional administrative notes. |

---

## Validation Rules

### BR-COMP-007

`company_id` shall be unique across all Company records.

---

### BR-COMP-008

`legal_name` shall not be empty.

---

### BR-COMP-009

`display_name`, when provided, may differ from `legal_name`.

---

### BR-COMP-010

`company_status` shall contain only approved enumeration values.

Recommended values include:

- Active
- Inactive
- Merged
- Acquired
- Dissolved

Implementations may extend this enumeration while preserving semantic compatibility.

---

### BR-COMP-011

`website`, when present, shall represent a valid HTTPS or HTTP URL.

---

### BR-COMP-012

`country` remains a factual descriptive attribute in Slice 01.

It shall not be interpreted as a foreign key or normalized reference to a future geographic entity.

---

## Lifecycle

Company exists independently of all person-owned entities.

Its lifecycle is determined by organizational existence rather than employment, projects, education, certifications, or evidence.

Company records may continue to exist even when no active references remain.

---

## Relationships (Deferred)

Version 1 stores Company independently of other supported domain entities.

Future versions may introduce explicit references or relationship structures connecting Company with:

- Employment
- Project
- Evidence
- Future geographic reference entities

Relationship modeling is intentionally deferred beyond the current Slice 01 baseline.

---

## Normalization Strategy

Company is the first approved shared/reference normalization target defined by DDR-001.

Existing transitional string fields, including company names stored within other entities, remain valid during Slice 01.

Future migration may progressively replace transitional organization name fields with canonical Company references while preserving backward compatibility.

This entity does not introduce or require a generic Organization abstraction.

---

## Future Evolution

Future versions may introduce additional capabilities, including:

- canonical business identifiers;
- industry classification;
- registration information;
- headquarters relationships;
- geographic normalization;
- relationship entities;
- external registry integration.

Such additions shall remain consistent with DDR-001 or any approved successor decision.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Approved Baseline | First approved baseline specification for Slice 01. |