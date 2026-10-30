# MVP Progress

## Project status

Vue 3 + Vuetify + Pinia client (`client/`) and FastAPI + SQLAlchemy server (`server/`). After Stage 1 the auth/routing flow is reliable and the Overview dashboard is backed by real data. Most other dashboard pages (project overview, calendar, documents, gantt, notifications, settings) are still stubs. No tests or dev tools were run in this stage; none of the changes have been executed.

## Completed in Stage 1

**Backend**
- New `GET /api/v1/dashboard` (authenticated, scoped to the current user's non-deleted projects and tasks). Returns:
  - project totals (total, active)
  - task stats (total, completed, pending, overdue, count by status)
  - 5 upcoming deadlines (non-terminal tasks with a due date, soonest first, overdue included)
  - 5 recently updated tasks, used as "Recent activity"
  - taskboard summaries for the active project, reusing `taskboards.services.list_taskboards`
- Pending means every task that is neither done nor cancelled. Overdue means past due and not done or cancelled.

**Frontend**
- `OverviewPage.vue` now shows metric cards, upcoming deadlines, recent activity, task progress with a status breakdown, taskboards and shortcuts. It has loading, error (with retry) and empty states, and a refresh button.
- New components in `components/dashboard/`: `DashboardSection`, `DashboardTaskList`; `DashboardMetrics` is now implemented.
- `dashboard.store.js`, `dashboard.api.js`, `types/dashboard.js` and `constants/dashboard.js` are implemented. The API now calls `/dashboard` (no scope id).
- `Dashboard.vue` no longer leaves taskboard fetch failures unhandled.

**Auth and routing fixes**
- `/dashboard` redirects to `overview`, and `/` redirects to `dashboard`. The guard sends users who haven't onboarded to onboarding.
- Completed users could never reach the onboarding taskboard step, because every onboarding route redirected them to the dashboard. Only the `project` step now redirects them.
- `NewProject` now awaits `refreshCurrentUser` before moving on. Previously this raced with the route guard.
- `Onboarding.vue` skip handler no longer pushes twice or crashes on the last step.
- Login honours the `redirect` query, accepting only internal paths, and falls back to the dashboard.
- `authStore.login` throws if the user can't be loaded, instead of silently bouncing back to the login page.
- `App.vue` redirects to login (keeping the redirect target) when the session is lost on a protected route, for example after refresh-token failure.

## Files modified

Backend:
- `server/app/features/dashboard/{__init__,router,schemas,services}.py` (new)
- `server/app/main.py`

Frontend:
- `client/src/router/index.js`
- `client/src/App.vue`
- `client/src/stores/auth.js`
- `client/src/stores/dashboard.store.js`
- `client/src/api/dashboard.api.js`
- `client/src/types/dashboard.js`
- `client/src/constants/dashboard.js`
- `client/src/views/{OverviewPage,Dashboard,LoginPage,Onboarding}.vue`
- `client/src/components/dashboard/*`
- `client/src/components/onboarding/NewProject.vue`

## Existing architecture

- Server: `features/<name>/{router,schemas,services,dependencies,exceptions}.py`. Routers are mounted under `/api/v1` in `main.py`. `get_db` commits per request. Ownership is enforced through `get_current_user` and `get_owned_*` dependencies. Entities are soft-deleted via `deleted_at`. Relationships default to `lazy="raise"`, so aggregate endpoints select columns directly.
- Client: `views` for pages, `components/<area>`, a Pinia store per area (`*.store.js`) using `cachedRequest` and status/error maps, an `api/*.api.js` layer on `apiFetch` and `parseJson`, JSDoc typedefs in `types/`, and constants in `constants/`.
- Auth: the access token lives in memory and the refresh cookie is httpOnly. `authStore.initialize()` runs before the router is installed, so the guard never sees a half-initialised state. Onboarding is complete when `currentUser.active_project_public_id` is set.
- Styling: Vuetify theme variables (`rgb(var(--v-theme-...))`), 0.75rem radius outlined surfaces, rem units.

## Database restrictions

No migrations were created, modified or deleted, and no tables, columns or relationships were added or changed. The dashboard only reads existing tables.

## Known issues

- "Recent activity" is derived from `tasks.updated_at`. There is no activity-event table, and `agent_activity_log` has no documented structure, so the dashboard doesn't show a real event stream.
- Project and task stats cover all of the user's projects, but the taskboard summary covers only the active project.
- `projects.services.list_projects` hard-codes `limit(5)`, so the project list never shows more than 5 projects. The dashboard counts are not affected.
- The Projects page "switch project" handler is empty, and `update_project` has a TODO for setting the active project.
- The Sidebar never receives `unreadNotifications`. Its `toggle-rail` event has no handler.
- The login page's "Forgot password" and "Create an account" buttons do nothing.
- `ProjectOverview`, `ProjectSettings`, `Calendar`, `Documents`, `Gantt`, `Notifications` and `Settings` are stubs or incomplete.
- Pinia stores aren't reset on logout, so data from a previous user could appear after a different user logs in.
- Nothing has been run or tested, as required for this stage.

## Remaining work

**Stage 2**
1. Make the active project switchable, and lift the project list limit with pagination.
2. Build out `ProjectOverview` and `ProjectSettings`.
3. Finish the taskboard and task pages, including status changes.
4. Reset stores on logout.

**Stage 3**
1. Calendar and Gantt, using task `start_date`/`due_date` and task edges.
2. Documents, notifications and settings, using whatever the existing schema supports.
3. Sidebar polish: rail toggle and the notification badge.
4. Tests, and restricting the CORS origins.
