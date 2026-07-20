# NAMING_CONVENTIONS

Title: Naming Conventions
Specification ID: AS-004
Version: 1.0
Status: Draft
Document Type: Normative Specification
Owner: Architecture
Approved By:
Depends On:
- DDR-001
- AG-001 (Integrity Rules)
- AS-001 (Identifier Rules)
- AS-002 (Ownership Rules)
- AS-003 (Enumeration Rules)
Supersedes:

---

# Purpose

This specification defines the architectural naming conventions used throughout the canonical domain model.

Consistent naming improves readability, traceability, interoperability, and long-term maintainability.

This specification governs architectural names only.

It does not define:

- programming language naming conventions;
- database naming conventions;
- API naming conventions;
- user interface labels;
- localization.

---

# Scope

This specification defines naming conventions for:

- canonical entities;
- relationship entities;
- attributes;
- enumerations;
- specifications;
- architectural rules;
- identifiers.

This specification does not define implementation-specific naming.

---

# Definitions

## Architectural Name

A standardized name assigned to an architectural concept.

---

## Canonical Entity Name

The approved architectural name of a canonical business object.

---

## Relationship Name

The approved architectural name of an association between canonical entities.

---

## Attribute Name

The approved architectural name of a business property belonging to a canonical entity.

---

# Naming Principles

Architectural names shall be:

- clear;
- unambiguous;
- consistent;
- technology independent;
- business-oriented.

Names shall prioritize meaning over brevity.

---

# Global Naming Rules

## GNR-001

Every architectural element shall have exactly one approved canonical name.

Aliases may exist for documentation purposes but shall not replace the canonical name.

---

## GNR-002

Names shall describe business meaning rather than implementation details.

Implementation terminology shall not appear in canonical architectural names.

---

## GNR-003

Canonical entity names shall use singular nouns.

Examples:

- Person
- Employment
- Project
- Company

---

## GNR-004

Relationship entity names shall describe the participating business concepts.

Relationship names shall remain concise and unambiguous.

---

## GNR-005

Attribute names shall describe a single business concept.

Compound or ambiguous attribute names are prohibited.

---

## GNR-006

Enumeration names shall describe the architectural concept represented by the enumeration.

Enumeration values shall use consistent naming conventions within the enumeration.

---

## GNR-007

Specification titles shall remain stable after approval.

Specification identifiers shall remain authoritative even if titles evolve.

---

## GNR-008

Rule identifiers shall remain globally unique within their owning specification.

Rule identifiers shall never be reused.

---

## GNR-009

Architectural names shall not include implementation technology.

Examples of prohibited technology-specific terminology include:

- SQL
- JSON
- Neo4j
- REST
- API

unless the specification explicitly concerns implementation mapping.

---

## GNR-010

Abbreviations shall be avoided unless they represent widely accepted industry terminology.

Where abbreviations are used, their meaning shall be defined in the Glossary.

---

## GNR-011

Renaming an approved architectural element shall require formal architectural review.

Historical traceability shall be preserved following approved renaming.

---

## GNR-012

Naming conventions shall remain consistent with approved:

- Domain Design Rules (DDR);
- Integrity Rules;
- Identifier Rules;
- Ownership Rules;
- Enumeration Rules;
- Glossary.

Conflicting specifications require formal architectural approval before adoption.

---

# Naming Patterns

## Canonical Entities

Use:

```
SingularNoun
```

Examples:

```
Person
Employment
Certification
Project
Company
Evidence
```

---

## Relationship Entities

Use:

```
PrimaryConcept_SecondaryConcept_Relationship
```

Examples:

```
Employment_Skill_Relationship
Project_Evidence_Relationship
```

---

## Attributes

Use:

```
lower_snake_case
```

Examples:

```
start_date
end_date
company_name
person_id
```

---

## Specifications

Use:

```
UPPER_SNAKE_CASE
```

Examples:

```
IDENTIFIER_RULES.md
OWNERSHIP_RULES.md
CANONICAL_FACT_MODEL.md
```

---

## Rule Identifiers

Use document-specific prefixes.

Examples:

```
GIR-001
GVR-001
RIR-001
LCR-001

GID-001
GOR-001
GER-001
GNR-001
```

Rule identifiers shall remain stable throughout the lifecycle of the specification.

---

## Specification Identifiers

Use stable specification identifiers independent of repository structure.

Examples:

```
AG-001
AG-002

AS-001
AS-002
AS-003
AS-004

KG-001
KG-002

KQ-001

IM-001
```

Specification identifiers shall never encode slice numbers or repository paths.

---

# Compliance

Every architectural specification shall comply with these naming conventions.

Implementation-specific naming standards may extend these requirements but shall not weaken the architectural consistency defined herein.

---

# Future Evolution

Future versions may introduce:

- automated naming validation;
- multilingual naming guidance;
- repository-wide naming audits;
- controlled abbreviation catalogs;
- specification naming registries.

Such extensions shall remain fully consistent with approved architectural governance.

---

# Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Initial architectural naming standard. |