# MVP Progress

## Project status

Vue 3 + Vuetify + Pinia client (`client/`) and FastAPI + SQLAlchemy server (`server/`). Stages 1 and 2 are written. The auth/routing flow, dashboard overview, project pages, taskboard and task pages, and the sidebar are functional. Calendar, documents, gantt, notifications and settings are still stubs. **No tests, builds or dev tools were run in either stage, so none of the code has been executed.**

## Completed in Stage 1

- `GET /api/v1/dashboard` plus a real-data `OverviewPage.vue`: metrics, upcoming deadlines, recent activity (recently updated tasks), task progress, taskboards, shortcuts, with loading/error/empty states.
- Routing fixes: `/` and `/dashboard` land on `overview`. Completed users can reach the onboarding taskboard step. `NewProject` awaits the user refresh. The skip handler no longer double-pushes. Login honours a safe `redirect` query. Session loss on a protected route redirects to login.

## Completed in Stage 2

**Active project switching**
- Backend: `PATCH /users/me` with `{active_project_public_id}`, checked for ownership and soft-deletion.
- Frontend: `authStore.setActiveProject`; `ProjectList` wires the card's "Set as active" action to it, and `ProjectOverview` has a "Set as active" button. A project card now only navigates to its overview; the "Set as active" menu item switches the project. The dead Rename/Duplicate/Delete menu items were replaced by "Project settings".

**Project pagination**
- Backend: the hard-coded `limit(5)` is gone. `GET /projects` takes `cursor` and `limit` (default 20, max 100) and returns `next_cursor`, using the same keyset scheme as tasks.
- Frontend: `projects.store` has `nextCursor` and `loadMore`, and new projects are prepended. `ProjectList` has a "Load more" button, a skeleton, and an error state with retry.

**ProjectOverview and ProjectSettings**
- Backend: `GET /projects/{id}/summary` returns task stats and taskboards for that project. It reuses `get_task_stats` from the dashboard service and `list_taskboards`.
- `ProjectOverview` shows the project header, task metrics, details (status, dates, timezone, agent) and taskboards.
- `ProjectSettings` edits the project with the existing `ProjectForm` (now honouring `submitLabel`) and has a delete section with a confirmation dialog. The active project can't be deleted.
- `DashboardMetrics` now uses an auto-fit grid so it works with any number of metrics.

**Taskboard and task pages**
- `TaskBoard.vue`:
  - search and status/priority filters, both driven by the toolbar (the status/priority filters are stored in the route query);
  - loading and error states with retry;
  - "Load more tasks" using the existing cursor;
  - board edit (reusing `CreateTaskBoardModel`, which now supports editing) and delete;
  - task delete and "mark complete" from the card menu.
- Drag-and-drop now only highlights and accepts valid target columns. Status change errors show a toast.
- Removed dead or fake UI: the hard-coded 67% progress bar on task cards, Snooze/Duplicate actions, Share/Invite/"Private" in the board header, Sort/View buttons, the fake ⌘S hint, and the inert column menu and resize handle.
- `TaskPage`:
  - reacts to route id changes and no longer shows a stale task;
  - shows a loading skeleton;
  - the task menu can delete the task;
  - `useTaskEditor` now reports save/status/priority errors through toasts, and takes just the task ref.
- Backend: `update_task` rejects marking an unapproved agent-created task as done with a validation error. Before, this would have hit a database constraint and returned a 500.

**Reset stores on logout**
- `authStore.clearSession` (called on logout and on any lost session) calls `resetSessionData`, which resets every Pinia store except `auth` and clears the request cache.

**Sidebar**
- The rail toggle works: `Dashboard.vue` owns the `isRail` state and passes it to `Sidebar`, which collapses labels, the brand and sub-items.
- The notification badge is not done: no notifications backend exists, so the Sidebar's `unreadNotifications` prop is still unused.

## Files modified

Backend:
- `server/app/features/users/{schemas,services,router}.py`
- `server/app/features/projects/{schemas,services,router}.py`
- `server/app/features/dashboard/services.py`
- `server/app/features/tasks/services.py`
- plus the Stage 1 files: `dashboard/*` and `main.py`

Frontend:
- Stores and utils: `stores/{auth,cache,projects.store,tasks.store}.js`, `utils/sessionReset.js` (new)
- API and types: `api/projects.api.js`, `types/project.js`
- Views: `views/{ProjectList,ProjectOverview,ProjectSettings,TaskBoard,TaskPage,Dashboard}.vue`
- Components: `components/common/ConfirmDialog.vue` (new), `components/projects/{ProjectCard,ProjectForm}.vue`, `components/taskboards/{BoardHeader,BoardToolbar,CreateTaskBoardModel}.vue`, `components/tasks/{TaskCard,TaskColumn,TaskPageHeader}.vue`, `components/dashboard/DashboardMetrics.vue`, `components/layout/Sidebar.vue`
- Composables: `composables/useTaskEditor.js`

## Existing architecture

- Server: `features/<name>/{router,schemas,services,dependencies,exceptions}.py`. Routers are mounted under `/api/v1` in `main.py`. `get_db` commits per request. Ownership is enforced through `get_current_user` and `get_owned_*` dependencies. Entities are soft-deleted via `deleted_at`. Relationships default to `lazy="raise"`, so aggregate endpoints select columns directly. Lists use keyset cursors from `utils/pagination.py`.
- Client: `views` for pages, `components/<area>`, a Pinia store per area (`*.store.js`) using `cachedRequest` and status/error maps, an `api/*.api.js` layer on `apiFetch` and `parseJson`, JSDoc typedefs in `types/`, and constants in `constants/`.
- Auth: the access token lives in memory and the refresh cookie is httpOnly. `authStore.initialize()` runs before the router is installed. Onboarding is complete when `currentUser.active_project_public_id` is set. Task and taskboard listing is scoped to the **active project** by the backend, so switching the active project changes what those pages show.
- Status changes: any task status can be set from any other status. `TASK_STATUS_TRANSITIONS` and `Task.can_transition_to` exist on the backend but are deliberately not enforced.
- Styling: Vuetify theme variables (`rgb(var(--v-theme-...))`), 0.75rem radius outlined surfaces, rem units.

## Database restrictions

No migrations were created, modified or deleted, and no tables, columns or relationships were added or changed in either stage. Everything uses existing tables.

## Known issues

- The notification badge and Notifications page have no backend. The Sidebar's `unreadNotifications` prop is never fed.
- "Recent activity" is derived from `tasks.updated_at`. There is no event table.
- `ProjectHeader` still shows a "Project members" button that does nothing.
- Task page: the Subtask panel, tags and details components were not reviewed in Stage 2.
- The sidebar taskboard task counts don't update after tasks are created or deleted on a board. The counts refresh on reload or when the project is switched.
- Board delete and edit only appear once the taskboard list has loaded in the sidebar.
- Login page: the "Forgot password" and "Create an account" buttons do nothing.
- `resetSessionData` relies on Pinia's internal `_s` store map.
- Nothing has been run or tested.

## Remaining work

**Stage 3**
1. Calendar and Gantt, using task `start_date`/`due_date` and task edges.
2. Documents, notifications (backend needed) and settings, using whatever the existing schema supports.
3. Review of the Subtask panel and the other task detail components; refresh sidebar board task counts after task changes.
4. Decide whether to enforce task status transitions.
5. Tests, and restricting the CORS origins.
