# EMPLOYMENT_SKILL_RELATIONSHIP

## Purpose

The Employment Skill Relationship defines the association between an Employment record and a Skill within the domain model.

It represents how a specific skill is applied, demonstrated, or required during a particular employment period.

This relationship does not own Employment or Skill information. It exists solely to describe the association between the two canonical entities.

---

## Scope

This relationship defines:

- associations between Employment and Skill;
- skill usage within a specific employment record;
- optional proficiency and experience metadata;
- relationship-specific descriptive information.

It does not define:

- Skill attributes;
- Employment attributes;
- Person identity;
- skill taxonomy;
- certification information.

These concerns belong to their respective canonical entities.

---

## Domain Definition

An Employment Skill Relationship links one Employment record to one Skill.

A single Employment record may reference multiple skills.

A single Skill may be associated with multiple Employment records.

The relationship maintains its own association metadata but cannot exist without valid referenced Employment and Skill entities.

---

## Ownership

This is a relationship entity.

It owns only relationship-specific information.

It shall not duplicate or redefine attributes owned by Employment or Skill.

---

## Business Rules

### BR-ESR-001

Each relationship shall reference exactly one Employment entity.

---

### BR-ESR-002

Each relationship shall reference exactly one Skill entity.

---

### BR-ESR-003

Multiple skills may be associated with a single Employment record.

---

### BR-ESR-004

The same Skill may be associated with multiple Employment records.

---

### BR-ESR-005

Relationship-specific metadata shall not modify or override canonical Skill information.

---

### BR-ESR-006

Relationship-specific metadata shall not modify or override canonical Employment information.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| relationship_id | Unique identifier of the relationship. |
| employment_id | Reference to the Employment entity. |
| skill_id | Reference to the Skill entity. |
| proficiency_level | Optional proficiency demonstrated during this employment. |
| years_used | Optional duration the skill was applied in this employment. |
| notes | Optional relationship-specific notes. |
---

## Attribute Specification

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| relationship_id | Yes | UUID | Unique identifier assigned to the relationship. |
| employment_id | Yes | UUID | Reference to the associated Employment entity. |
| skill_id | Yes | UUID | Reference to the associated Skill entity. |
| proficiency_level | No | Enumeration | Optional proficiency demonstrated during the employment period. |
| years_used | No | Decimal | Approximate duration the skill was applied within the employment period. |
| notes | No | String | Optional relationship-specific notes. |

---

## Validation Rules

### BR-ESR-007

`relationship_id` shall be unique across all Employment Skill Relationship records.

---

### BR-ESR-008

`employment_id` shall reference an existing Employment entity.

---

### BR-ESR-009

`skill_id` shall reference an existing Skill entity.

---

### BR-ESR-010

The combination of `employment_id` and `skill_id` shall be unique.

Duplicate relationships between the same Employment and Skill are not permitted.

---

### BR-ESR-011

`proficiency_level`, when provided, shall contain only approved enumeration values.

The proficiency level represents skill proficiency demonstrated within the associated Employment Skill Relationship.

It does not modify or redefine the canonical Skill entity.

Recommended values include:

- Beginner
- Intermediate
- Advanced
- Expert

Implementations may extend this enumeration while preserving semantic compatibility.

---

### BR-ESR-012

`years_used`, when provided, shall be greater than or equal to zero.

---

### BR-ESR-013

When both employment duration and `years_used` are available, `years_used` shall not exceed the duration of the associated Employment record.

---

## Lifecycle

The Employment Skill Relationship maintains its own relationship-specific metadata.

However, it cannot exist without valid referenced Employment and Skill entities.

Changes to the lifecycle of either referenced entity may require the relationship to be archived or removed according to implementation policy.

---

## Relationship Constraints

This entity owns only relationship-specific metadata.

It shall not:

- duplicate Employment attributes;
- duplicate Skill attributes;
- redefine canonical entity information;
- establish ownership over Employment or Skill.

---

## Future Evolution

Future versions may introduce additional capabilities, including:

- skill importance or weighting;
- evidence references supporting skill usage;
- project-specific skill associations;
- proficiency assessment history;
- relationship validity periods.

Such additions shall preserve the canonical ownership boundaries established by the Employment and Skill entities.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Approved Baseline | First approved baseline specification for Slice 02. |