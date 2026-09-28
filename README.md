# MyWellbeing — Cross-Platform Fitness & Telemetry Platform

A cross-platform health and fitness telemetry client built with Python and [Flet](https://flet.dev) (Flutter runtime for Python), backed by a relational PostgreSQL database. The application aggregates user activity metrics via the Strava API, dispatches automated event notifications via the Resend API, and supports automated cross-platform UI validation via Appium and GitHub Actions CI/CD.

---

## Architecture & Integration Overview

```text
       [ External Services ]                    [ Client Application (Flet / Flutter) ]
┌─────────────────────────────────┐           ┌─────────────────────────────────────────┐
│ Strava API (Activity Telemetry) │ ◄───────► │ - Cross-Platform UI (Desktop & Mobile)  │
│ Resend API (Transactional Mail) │ ◄───────► │ - Local State & Telemetry Aggregation   │
└─────────────────────────────────┘           └────────────────────┬────────────────────┘
                                                                   │
                                                                   ▼
                                                     [ Relational Persistence Layer ]
                                                     ┌───────────────────────────────┐
                                                     │ PostgreSQL Database Engine    │
                                                     │ - User Accounts & Profiles    │
                                                     │ - Activity Logs & Analytics   │
                                                     └───────────────────────────────┘