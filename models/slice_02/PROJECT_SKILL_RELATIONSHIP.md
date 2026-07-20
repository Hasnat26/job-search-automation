# PROJECT_SKILL_RELATIONSHIP

## Purpose

The Project Skill Relationship defines the association between a Project record and a Skill within the domain model.

It represents how a specific skill is applied, demonstrated, or required during the execution of a project.

This relationship does not own Project or Skill information. It exists solely to describe the association between the two canonical entities.

---

## Scope

This relationship defines:

- associations between Project and Skill;
- skill usage within a specific project;
- optional proficiency and utilization metadata;
- relationship-specific descriptive information.

It does not define:

- Project attributes;
- Skill attributes;
- Person identity;
- project ownership;
- certification information.

These concerns belong to their respective canonical entities.

---

## Domain Definition

A Project Skill Relationship links one Project record to one Skill.

A single Project may reference multiple skills.

A single Skill may be associated with multiple projects.

The Project Skill Relationship maintains its own association metadata but cannot exist without valid referenced Project and Skill entities.

---

## Ownership

This is a relationship entity.

It owns only relationship-specific information.

It shall not duplicate or redefine attributes owned by Project or Skill.

---

## Business Rules

### BR-PSR-001

Each relationship shall reference exactly one Project entity.

---

### BR-PSR-002

Each relationship shall reference exactly one Skill entity.

---

### BR-PSR-003

Multiple skills may be associated with a single Project.

---

### BR-PSR-004

The same Skill may be associated with multiple Projects.

---

### BR-PSR-005

Relationship-specific metadata shall not modify or override canonical Skill information.

---

### BR-PSR-006

Relationship-specific metadata shall not modify or override canonical Project information.

---

## Attribute Inventory

| Attribute | Description |
|-----------|-------------|
| relationship_id | Unique identifier of the relationship. |
| project_id | Reference to the Project entity. |
| skill_id | Reference to the Skill entity. |
| proficiency_level | Optional proficiency demonstrated during the project. |
| importance | Optional indication of the significance of the skill within the project. |
| notes | Optional relationship-specific notes. |

---

## Attribute Specification

| Attribute | Required | Type | Description |
|-----------|----------|------|-------------|
| relationship_id | Yes | UUID | Unique identifier assigned to the relationship. |
| project_id | Yes | UUID | Reference to the associated Project entity. |
| skill_id | Yes | UUID | Reference to the associated Skill entity. |
| proficiency_level | No | Enumeration | Optional proficiency demonstrated during the project. |
| importance | No | Enumeration | Optional indication of the significance of the skill within the project. |
| notes | No | String | Optional relationship-specific notes. |

---

## Validation Rules

### BR-PSR-007

`relationship_id` shall be unique across all Project Skill Relationship records.

---

### BR-PSR-008

`project_id` shall reference an existing Project entity.

---

### BR-PSR-009

`skill_id` shall reference an existing Skill entity.

---

### BR-PSR-010

The combination of `project_id` and `skill_id` shall be unique.

Duplicate relationships between the same Project and Skill are not permitted.

---

### BR-PSR-011

`proficiency_level`, when provided, shall contain only approved enumeration values.

The proficiency level represents skill proficiency demonstrated within the associated Project Skill Relationship.

It does not modify or redefine the canonical Skill entity.

Recommended values include:
- Beginner
- Intermediate
- Advanced
- Expert

Implementations may extend this enumeration while preserving semantic compatibility.

---

### BR-PSR-012

`importance`, when provided, shall contain only approved enumeration values.

Recommended values include:

- Low
- Medium
- High
- Critical

Implementations may extend this enumeration while preserving semantic compatibility.

---

## Lifecycle

The Project Skill Relationship maintains its own relationship-specific metadata.

However, it cannot exist without valid referenced Project and Skill entities.

Changes to the lifecycle of either referenced entity may require the relationship to be archived or removed according to implementation policy.

---

## Relationship Constraints

This entity owns only relationship-specific metadata.

It shall not:

- duplicate Project attributes;
- duplicate Skill attributes;
- redefine canonical entity information;
- establish ownership over Project or Skill.

---

## Future Evolution

Future versions may introduce additional capabilities, including:

- evidence references supporting skill usage;
- project role or responsibility associations;
- skill utilization metrics;
- proficiency assessment history;
- relationship validity periods.

Such additions shall preserve the canonical ownership boundaries established by the Project and Skill entities.

---

## Revision History

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Approved Baseline | First approved baseline specification for Slice 02. |