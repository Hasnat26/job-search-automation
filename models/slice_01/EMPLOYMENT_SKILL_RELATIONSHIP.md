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

The relationship exists independently of the lifecycle of either entity while both referenced entities remain valid.

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

### BR-ESR-013

When both employment duration and `years_used` are available, `years_used` shall not exceed the duration of the associated Employment record.

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

## Lifecycle

An Employment Skill Relationship exists only while both referenced entities remain valid.

If either the referenced Employment or Skill entity is removed from the canonical model, this relationship shall also be removed or archived according to implementation policy.

The lifecycle of this relationship does not alter or govern the lifecycle of either referenced entity.

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