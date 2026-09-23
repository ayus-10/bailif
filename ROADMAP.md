# Taskboard Feature Roadmap

## Goal

Complete the missing taskboard and project functionality using the existing functional backend and data model. This roadmap intentionally focuses on the missing features only and orders them by dependency and implementation value.

---

## Phase 1 — Project Context & Ownership

These features establish the active project context that the rest of the application depends on.

### 1. Create Project
Allow users to create a new project and make it available in the project list.

### 2. Switch Active Project
Allow users to switch between existing projects and update the application context to the selected project.

### 3. Enforce Single Active Project
Ensure only one project can be active at a time so every taskboard and task has an unambiguous project context.

### 4. Active Project Owns the Hierarchy
Ensure tasks, sub-tasks, taskboards, and other hierarchy elements are consistently associated with the active project.

### 5. Project-Specific Settings
Add project-level settings that can provide defaults to the taskboards and tasks belonging to that project.

### 6. Settings Flow Down as Defaults
Define how project settings are inherited by descendants while still allowing more specific settings or values to override the defaults.

---

## Phase 2 — Task Hierarchy

Establish the complete root-task/sub-task behavior before building actions that may operate on either level.

### 7. Sub-task Functionality
Allow root tasks to contain sub-tasks while preserving the existing task entity and `parent_public_id` relationship.

### 8. Sub-task Lifecycle
Support creating, viewing, updating, moving/re-parenting where required, and deleting sub-tasks while preserving valid hierarchy relationships.

---

## Phase 3 — Core Task Actions

Implement the direct actions users perform on individual task cards.

### 9. Mark Complete
Allow a task to transition to the completed state through the existing task status lifecycle.

### 10. Delete
Allow users to delete tasks and define how deletion affects any sub-tasks belonging to the deleted task.

### 11. Duplicate
Allow users to create a new task from an existing task while generating a new identity and timestamps.

### 12. Snooze
Allow users to temporarily defer a task according to a clearly defined snooze behavior without unintentionally changing its normal task data.

---

## Phase 4 — Taskboard Querying

Once task data and actions are stable, add the mechanisms for finding and organizing tasks.

### 13. Search
Allow users to search the current taskboard using relevant task fields such as title, description, and tags.

### 14. Filter
Allow users to narrow visible tasks using existing properties such as status, priority, type, tags, and dates.

### 15. Sort
Allow users to order visible tasks using supported task properties such as position, priority, due date, creation date, or title.

### 16. Combine Search, Filter, and Sort
Make search, filters, and sorting work together so users can progressively narrow and organize the same task set.

---

## Phase 5 — Taskboard Interaction

Add the controls that change how users interact with the board itself.

### 17. View
Allow users to switch between the supported taskboard presentation modes without changing the underlying task data.

### 18. Column Context Menu
Provide useful actions for individual static columns, such as collapsing a column or applying supported column-level task operations.

### 19. Taskboard Settings
Allow users to configure taskboard-level behavior and defaults that apply to the board.

---

## Phase 6 — Integration & Consistency

Tie the completed features together and verify that project context, hierarchy, actions, and board controls behave consistently.

### 20. Project Context Integration
Verify that changing the active project correctly updates the taskboard and prevents tasks from another project from appearing in the active hierarchy.

### 21. Settings Inheritance Integration
Verify that project settings correctly flow into taskboards and tasks as defaults without unexpectedly overriding explicit values.

### 22. Hierarchy Integration
Verify that root tasks and sub-tasks behave consistently across task actions, searching, filtering, sorting, and views.

### 23. Task Action Integration
Verify that completing, snoozing, duplicating, and deleting tasks correctly update the taskboard without leaving stale or invalid UI state.

### 24. Querying Integration
Verify that search, filters, sorting, and views can be combined without producing inconsistent task results.

---

## Recommended Implementation Order

```text
PROJECT CONTEXT
    │
    ├── Create Project
    ├── Switch Active Project
    ├── Single Active Project
    ├── Project Owns Hierarchy
    ├── Project Settings
    └── Settings → Defaults
            │
            ▼
TASK HIERARCHY
    │
    ├── Sub-task Creation / Retrieval
    ├── Sub-task Updates
    ├── Sub-task Re-parenting (if required)
    └── Sub-task Deletion
            │
            ▼
CORE TASK ACTIONS
    │
    ├── Mark Complete
    ├── Delete
    ├── Duplicate
    └── Snooze
            │
            ▼
TASKBOARD QUERYING
    │
    ├── Search
    ├── Filter
    ├── Sort
    └── Combine Query Controls
            │
            ▼
TASKBOARD INTERACTION
    │
    ├── View
    ├── Column Context Menu
    └── Taskboard Settings
            │
            ▼
INTEGRATION
    │
    ├── Project Context
    ├── Settings Inheritance
    ├── Hierarchy
    ├── Task Actions
    └── Querying
```

## Guiding Principle

Do not redesign or rebuild the existing backend. For each roadmap item, first identify the smallest backend/API change required to support the missing behavior, then implement the corresponding frontend behavior and integration.
