<!--• Project Overview • Problem Statement • Features • Technology Stack • Architecture • Database Design, where applicable • API Documentation, where applicable • Installation • Environment Variables • How to Run • Screenshots, where applicable • Challenges Faced • Solutions • Future Improvements -->

# Employee Management Dashboard

An end-to-end full-stack dashboard for managing organizational employee records, computing real-time payroll metrics, and performing multi-parameter search, filtering, sorting, and full CRUD operations.

---

## Project Overview

This application serves as an internal administrative tool to track and manage employee records across departments. It combines a decoupled Express/TypeScript backend serving REST endpoints with a responsive React/TypeScript frontend built on Vite.

---

## Problem Statement

Administrative teams frequently struggle with fragmented employee records, delayed metric calculations (such as average compensation and department distribution), and clunky interfaces for basic HR updates. This project provides a centralized, type-safe interface that executes search, filtering, and metric aggregations with sub-millisecond client-side performance.

---

## Features

* **Key Metrics Bar:** Real-time summary cards displaying Total Employees, Average Salary (localized to INR `₹`), and Distinct Departments derived dynamically via memoized selectors.
* **Multi-Field Search:** Sub-string search matching against First Name, Last Name, Email, and Role simultaneously.
* **Department Filtering:** Dynamic dropdown populated from unique backend departments.
* **Two-Way Sorting:** Field-based sorting (Name, Department, Salary, Join Date) with toggleable Ascending/Descending ordering.
* **Full CRUD Support:**
* **Create:** Modal form with client-side field validation.
* **Read:** Tabular listing and single-record detail inspection modal.
* **Update:** Pre-populated edit modal with ID integrity protection.
* **Delete:** Destruction of records with confirmation safeguards.



---

## Technology Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Frontend** | React 18+, TypeScript | UI components, view state, and local reactivity |
| **Build Tool** | Vite | Module bundling and fast HMR |
| **Styling** | Vanilla CSS (CSS Variables) | Lightweight styling without external UI dependencies |
| **Backend** | Node.js, Express, TypeScript | REST API service and payload validation |
| **Runtime** | `tsx` / Node.js | TypeScript execution without compile-step overhead |
| **Networking** | Fetch API, CORS middleware | Client-server communication |

---

## Architecture

The project is structured as a decoupled monorepo:

```text
day-06/react-app/
├── backend/                  # REST API Layer
│   ├── server.ts             # Express routes, controllers, and in-memory datastore
│   ├── tsconfig.json
│   └── package.json
└── frontend/                 # Client UI Layer
    ├── src/
    │   ├── types/            # Shared TypeScript contracts (Employee, Criteria)
    │   ├── services/         # API abstraction layer (Fetch client)
    │   ├── components/       # Presentational & interactive UI modules
    │   ├── App.tsx           # State orchestration & derived selectors
    │   ├── main.tsx          # React DOM mounting
    │   └── index.css         # Global variables, grid layouts, and modals
    ├── index.html
    ├── tsconfig.json
    └── vite.config.ts

```

---

## Database Design / Data Model

Data is structured around the `Employee` entity:

| Field | Type | Description |
| --- | --- | --- |
| `id` | `string` | Unique identifier (e.g., `emp-1718000000000`) |
| `firstName` | `string` | Employee's given name |
| `lastName` | `string` | Employee's family name |
| `email` | `string` | Unique corporate email address |
| `department` | `string` | Department assignment (Engineering, Product, etc.) |
| `role` | `string` | Organizational title |
| `salary` | `number` | Annual compensation in INR |
| `joinDate` | `string` | ISO Date format (`YYYY-MM-DD`) |

---

## API Documentation

**Base URL:** `http://localhost:5000/api/employees`

| Method | Endpoint | Description | Request Body | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/` | Retrieve all employees | None | `Employee[]` |
| `GET` | `/:id` | Fetch employee by ID | None | `Employee` (or `404`) |
| `POST` | `/` | Create an employee | `Omit<Employee, "id">` | Created `Employee` (`201`) |
| `PUT` | `/:id` | Update an existing record | `Partial<Employee>` | Updated `Employee` (`200`) |
| `DELETE` | `/:id` | Delete employee record | None | Empty (`204`) |

---

## Installation

### Prerequisites

* **Node.js:** v18.0.0 or higher
* **npm:** v9.0.0 or higher

### 1. Setup Backend

```bash
cd backend
npm install

```

### 2. Setup Frontend

```bash
cd ../frontend
npm install

```

---

## How to Run

### Step 1: Start the Backend Service

```bash
cd backend
npx tsx server.ts
# Server will listen on http://localhost:5000

```

### Step 2: Start the Frontend Application

In a separate terminal window:

```bash
cd frontend
npm run dev
# Vite server will start on http://localhost:5173

```

Open `http://localhost:5173` in your browser.

---

## Screenshots

| Dashboard Overview & Metrics | Add/Edit Employee Modal |
| --- | --- |
| ** | ** |

---

## Challenges Faced

1. **Runtime Execution with TypeScript:** Encountered `TypeError: Cannot read properties of undefined (reading 'fileExists')` using `ts-node` due to local resolution mismatches with TypeScript peer dependencies.
2. **Derived Computations vs. Re-render Lag:** Calculating statistics (total count, distinct departments, average salary) along with multi-attribute filtering and sorting on every keystroke risked UI micro-stutters.

---

## Solutions

1. **Switched to `tsx`:** Replaced the legacy `ts-node` execution engine with `tsx` (powered by `esbuild`), eliminating configuration-heavy compilation overhead during development.
2. **Memoized Derivation:** Separated state into raw server entities (`employees`) and UI input parameters (`criteria`). Used React's `useMemo` hooks to isolate filter/sort operations and summary calculations so expensive arrays only recompute when data alters.

---

## Future Improvements

* [ ] **Database Persistence:** Migrate backend in-memory array to an SQLite or PostgreSQL instance using Prisma ORM.
* [ ] **Server-Side Pagination:** Add `?page=1&limit=10` query parameter support on the backend to maintain performance at scale.
* [ ] **Data Export:** Add a CSV/Excel export button for reporting.
* [ ] **Authentication & Roles:** Implement JWT-based auth separating Admin (Read/Write) and Staff (Read-Only) permissions.
