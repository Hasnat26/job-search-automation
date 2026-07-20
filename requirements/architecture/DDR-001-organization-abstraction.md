# DDR-001: Organization Abstraction Strategy

## Status

Approved

---

## Date

2026-07-20

---

## Scope

This DDR governs normalization decisions for Slice 01 domain modeling.

It defines:

- when shared/reference entities may be introduced;
- when transitional string fields remain acceptable;
- when abstraction shall be deferred.

This DDR does not define:

- relationship modeling;
- persistence strategy;
- generated artifacts.

---

## Context

Slice 01 establishes the canonical domain model for the Job Search Automation platform.

Several approved entity specifications contain organization-related attributes represented as transitional string fields, including company names, educational institutions, and certification issuers.

As the domain model evolves, these attributes create opportunities for normalization into shared/reference entities. However, introducing abstraction prematurely increases architectural complexity and risks coupling unrelated domain concepts before sufficient business evidence exists.

A governing architectural decision is therefore required to define normalization boundaries for Slice 01.

---

## Decision Summary

Approved.

Slice 01 shall not introduce a generic `Organization` entity.

`Company` is the first shared/reference normalization target.

`Institution` and `Certification Authority` remain deferred.

---

## Decision

Slice 01 shall not introduce a generic `Organization` entity.

Shared/reference entities shall be introduced only when supported by demonstrated independent lifecycle and sufficient cross-domain reuse.

The first approved shared/reference normalization target for Slice 01 is `Company`.

`Institution` shall remain represented by transitional string attributes until future normalization is justified.

`Certification Authority` shall remain factual metadata until independent lifecycle or reuse requirements emerge.

All Slice 01 entity specifications shall remain consistent with this decision.

---

## Rationale

The objective of this decision is to establish clear normalization boundaries during Slice 01 domain modeling while avoiding premature abstraction.

Current analysis demonstrates asymmetric normalization pressure across organization-related concepts.

`Company` is referenced by multiple present and anticipated domain entities, including Employment, Project, and future business-facing reference models. This indicates an independent lifecycle and sufficient reuse to justify canonical representation.

`Institution` is currently referenced only within the Education domain. Although future normalization may become beneficial, present business requirements do not justify introducing a dedicated shared/reference entity.

`Certification Authority` is currently represented solely as factual issuer metadata. No independent lifecycle, governance requirements, or cross-domain reuse have emerged.

Introducing a generic `Organization` abstraction at this stage would increase architectural complexity without corresponding business value.

This decision therefore follows the architectural principle:

> Normalize only when multiple independent lifecycles emerge.

---

## Trade-offs

### Benefits

- Reduces premature abstraction.
- Preserves a simple and understandable domain model.
- Establishes evidence-driven normalization.
- Provides a stable governance boundary for Slice 01.
- Minimizes unnecessary migration and refactoring effort.

### Costs

- Transitional string fields remain in several approved entities.
- Canonical organization identity is deferred.
- Some duplicate organization names may temporarily exist.
- Future normalization will require controlled migration.

These trade-offs are accepted because they preserve architectural simplicity while maintaining a clear future evolution path.

---

## Governance Rules

This DDR governs normalization decisions for all Slice 01 entity specifications.

Under this decision:

- Generic `Organization` entities shall not be introduced.
- `Company` is the only approved shared/reference normalization target.
- Transitional string fields remain intentional architectural representations.
- Entity specifications shall not contradict this DDR.
- Architectural exceptions are not permitted.
- Any modification to this decision requires approval through a subsequent DDR.

---

## Review Triggers

This DDR shall be reviewed when one or more of the following conditions occur:

- Canonical organization identity is required across multiple domains.
- Organization metadata becomes independently managed.
- Cross-domain relationships require organizational abstraction.
- Multiple entity types duplicate organization semantics.
- Business requirements demonstrate sufficient reuse to justify additional shared/reference entities.

---

## Supersession

This decision remains in force until explicitly superseded by a later approved DDR.

Partial deviation from this DDR is not permitted.

Superseding decisions shall document the architectural rationale for replacing this governance contract.

---

## Consequences

### Immediate Consequences

- Slice 01 proceeds with `Company` as the first shared/reference entity.
- `Institution` remains intentionally represented as a transitional string field.
- `Certification Authority` remains factual metadata.
- Generic `Organization` abstraction is deferred.

### Downstream Impact

This decision governs normalization boundaries for:

- EMPLOYMENT_ENTITY.md
- EDUCATION_ENTITY.md
- CERTIFICATION_ENTITY.md
- COMPANY_ENTITY.md
- LOCATION_ENTITY.md
- Future INSTITUTION_ENTITY.md

Relationship modeling introduced in Slice 02 shall remain consistent with this decision until superseded.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Approved | Initial governing decision establishing the Slice 01 organization abstraction strategy. |