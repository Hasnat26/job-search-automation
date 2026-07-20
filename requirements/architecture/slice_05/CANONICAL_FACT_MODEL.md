# CANONICAL_FACT_MODEL

Title: Canonical Fact Model
Specification ID: KG-002
Version: 1.0
Status: Draft
Document Type: Normative Specification
Owner: Architecture
Approved By:
Depends On:
- DDR-001
- AG-001 (Integrity Rules)
- AG-003 (Referential Integrity Rules)
- AG-004 (Lifecycle Rules)
- AS-001 (Identifier Rules)
- AS-002 (Ownership Rules)
- AS-003 (Enumeration Rules)
- AS-004 (Naming Conventions)
- KG-001 (Knowledge Graph Architecture)
Supersedes:

---

# Purpose

This specification defines the Canonical Fact Model used throughout the Career Knowledge Builder.

A canonical fact represents the authoritative architectural statement describing one aspect of a business object.

Canonical facts are the primary semantic units of knowledge within the architecture.

This specification defines:

- what constitutes a canonical fact;
- fact identity;
- fact ownership;
- fact lifecycle;
- fact relationships;
- fact consistency.

This specification does not define:

- evidence evaluation;
- provenance;
- temporal validity;
- confidence scoring;
- persistence implementation.

Those concerns are defined by dedicated specifications.

---

# Scope

This specification governs all canonical facts represented within the knowledge architecture.

Every architectural specification introducing business knowledge shall conform to this model.

---

# Definitions

## Canonical Fact

The authoritative architectural representation of exactly one business statement.

A canonical fact represents what the architecture recognizes as true within its defined scope.

---

## Business Statement

A statement describing a characteristic, relationship, event, or condition of one or more canonical entities.

---

## Fact Subject

The canonical entity primarily described by the fact.

---

## Fact Predicate

The business property or relationship asserted by the fact.

---

## Fact Value

The business value, entity, relationship, or state asserted by the fact.

---

## Fact Context

The architectural context required to correctly interpret a fact.

Context may include qualifiers such as scope, applicable entity, or business constraints.

---

# Canonical Fact Principles

Canonical facts shall:

- represent one business statement;
- remain semantically unambiguous;
- be technology independent;
- support historical interpretation;
- support evidence attachment;
- support provenance;
- support temporal validity.

---

# Canonical Fact Structure

Every canonical fact consists of:

- Fact Subject
- Fact Predicate
- Fact Value

Optional contextual information may supplement the fact without altering its meaning.

Conceptually:

```
Subject
    │
Predicate
    │
Value
```

Example:

```
Subject
    Employment

Predicate
    employer

Value
    Company
```

---

# Global Canonical Fact Rules

## GCF-001

Every canonical fact shall represent exactly one business statement.

Compound facts are prohibited.

---

## GCF-002

Every canonical fact shall identify exactly one primary fact subject.

---

## GCF-003

Every canonical fact shall define exactly one predicate.

Predicates shall represent one business concept.

---

## GCF-004

Every canonical fact shall define exactly one asserted value.

---

## GCF-005

Canonical facts shall not encode implementation-specific information.

---

## GCF-006

Canonical facts shall remain independent of supporting evidence.

Evidence strengthens confidence but does not define the existence of a canonical fact.

---

## GCF-007

Canonical facts shall remain independent of provenance.

The origin of supporting information shall not alter the semantic meaning of the fact.

---

## GCF-008

Canonical facts shall remain independent of temporal validity.

Time constrains applicability rather than semantic identity.

---

## GCF-009

Canonical facts shall remain stable throughout their architectural lifecycle.

Revisions shall preserve historical interpretation.

---

## GCF-010

Duplicate canonical facts representing the same business statement are prohibited.

---

## GCF-011

Canonical facts shall comply with approved ownership, identifier, and integrity specifications.

---

## GCF-012

Canonical facts shall remain consistent with approved:

- Domain Design Rules (DDR);
- Architecture Governance specifications;
- Architectural Standards;
- Knowledge Graph Architecture.

Conflicting specifications require formal architectural approval.

---

# Fact Relationships

Canonical facts may reference:

- one or more canonical entities;
- one or more canonical relationships;
- zero or more supporting evidence records;
- zero or more provenance records;
- zero or more temporal constraints.

These references do not alter the identity of the canonical fact.

---

# Canonical Fact Lifecycle

A canonical fact may progress through:

- creation;
- validation;
- approval;
- revision;
- archival.

Lifecycle state shall not alter semantic identity.

---

# Canonical Fact Consistency

Canonical facts shall satisfy the following characteristics:

- semantic consistency;
- architectural consistency;
- identifier consistency;
- ownership consistency;
- historical consistency.

Violations require architectural review.

---

# Compliance

Every specification defining business knowledge shall explicitly identify the canonical facts it introduces.

Every canonical fact shall conform to this specification before additional semantics, such as evidence or provenance, are applied.

---

# Future Evolution

Future versions may introduce:

- composite fact patterns;
- inferred facts;
- derived facts;
- fact versioning;
- fact normalization;
- machine-readable fact schemas.

Such extensions shall preserve the architectural principles defined by this specification.

---

# Related Specifications

This specification provides the conceptual foundation for:

- KG-003 Provenance Rules
- KG-004 Temporal Model
- KG-005 Traceability Model
- KG-006 Evidence Confidence Model

---

# Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Initial canonical fact architecture baseline. |