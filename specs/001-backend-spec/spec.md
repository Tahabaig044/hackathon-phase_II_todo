# Backend Specification: Hackathon Todo Application

**Feature Branch**: `001-backend-spec`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "SPECIFY THE COMPLETE BACKEND for Phase II of the Hackathon Todo application."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secure Task Management (Priority: P1)

As a registered user of the Hackathon Todo application, I want to securely create, read, update, and delete my personal tasks through the backend API so that I can manage my productivity while ensuring my data remains private and isolated from other users.

**Why this priority**: This is the core functionality of the application - users must be able to manage their tasks securely with proper authentication and authorization.

**Independent Test**: Can be fully tested by authenticating with a JWT token and performing CRUD operations on tasks, verifying that only the authenticated user's tasks are accessible.

**Acceptance Scenarios**:

1. **Given** I am an authenticated user with a valid JWT token, **When** I make requests to task endpoints, **Then** I can only access, modify, or delete tasks that belong to my user account.
2. **Given** I am an unauthenticated user or have an invalid JWT token, **When** I attempt to access task endpoints, **Then** I receive a 401 Unauthorized response.
3. **Given** I am an authenticated user attempting to access another user's task, **When** I make a request with valid authentication, **Then** I receive a 403 Forbidden response.

---

### User Story 2 - JWT-Based Authentication Integration (Priority: P1)

As a user of the Hackathon Todo application, I want the backend to verify my JWT tokens issued by Better Auth so that I can seamlessly access protected resources with confidence that my identity is properly validated.

**Why this priority**: Authentication is fundamental to user data security and proper multi-tenancy isolation.

**Independent Test**: Can be fully tested by sending requests with valid and invalid JWT tokens to protected endpoints and verifying appropriate responses.

**Acceptance Scenarios**:

1. **Given** I have a valid JWT token from Better Auth, **When** I make requests to protected endpoints, **Then** the backend successfully verifies my token and grants access based on my user identity.
2. **Given** I have an expired or invalid JWT token, **When** I make requests to protected endpoints, **Then** the backend rejects the request with a 401 Unauthorized response.
3. **Given** I make a request without an Authorization header, **When** I access protected endpoints, **Then** the backend returns a 401 Unauthorized response.

---

### User Story 3 - Consistent API Integration (Priority: P2)

As a frontend developer working with the Hackathon Todo application, I want the backend to provide consistent REST API responses so that I can reliably integrate with the API and handle responses predictably.

**Why this priority**: Consistent API behavior is essential for reliable frontend integration and good user experience.

**Independent Test**: Can be fully tested by making various API requests and verifying response formats, status codes, and error handling are consistent.

**Acceptance Scenarios**:

1. **Given** I make valid API requests to backend endpoints, **When** the requests are processed successfully, **Then** I receive consistent JSON responses with appropriate status codes.
2. **Given** I make API requests that result in errors, **When** errors occur, **Then** I receive predictable error responses in a consistent JSON format.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST verify JWT tokens from the Authorization header using the BETTER_AUTH_SECRET environment variable
- **FR-002**: System MUST extract user_id from verified JWT claims and use it as the authoritative user identifier
- **FR-003**: System MUST filter all task queries by the authenticated user_id to ensure data isolation
- **FR-004**: System MUST reject requests without valid JWT tokens with a 401 Unauthorized response
- **FR-005**: System MUST reject requests attempting to access resources belonging to other users with a 403 Forbidden response
- **FR-006**: System MUST provide REST endpoints for task CRUD operations (GET /tasks, POST /tasks, GET /tasks/{id}, PUT /tasks/{id}, DELETE /tasks/{id})
- **FR-007**: System MUST connect to Neon Serverless PostgreSQL using DATABASE_URL environment variable
- **FR-008**: System MUST use SQLModel ORM for database operations
- **FR-009**: System MUST store task data with user_id foreign key relationship (derived from JWT)
- **FR-010**: System MUST handle JWT expiration and validation errors appropriately
- **FR-011**: System MUST provide consistent JSON error responses for all error conditions
- **FR-012**: System MUST implement proper CORS configuration to allow frontend integration
- **FR-013**: System MUST validate request payloads and return 422 validation errors for invalid data
- **FR-014**: System MUST implement connection pooling for database connections
- **FR-015**: System MUST timestamp all task records with created_at and updated_at fields

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with fields: id, title, description, completed status, priority, due_date, user_id (from JWT), timestamps
- **JWT Token**: Authentication token containing user identity claims (user_id, email) issued by Better Auth

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints properly authenticate and authorize users based on JWT tokens without exposing other users' data
- **SC-002**: Database operations consistently filter by authenticated user_id to maintain data isolation
- **SC-003**: API responses follow consistent JSON format with appropriate HTTP status codes
- **SC-004**: Error conditions return predictable responses in standard format
- **SC-005**: Backend successfully integrates with Better Auth JWT verification system
- **SC-006**: System connects to Neon Serverless PostgreSQL using environment configuration
- **SC-007**: All protected endpoints reject unauthorized access attempts appropriately

## Environment Configuration

The backend application MUST use the following environment variables (no fallback values allowed):
- `DATABASE_URL`: Neon Serverless PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT verification secret key
- `BETTER_AUTH_URL`: Frontend authentication origin URL

The application MUST fail loudly if any required environment variables are missing.

## Application Structure

The backend MUST follow this folder structure:

```
backend/
├── main.py                 # FastAPI application entry point
├── core/                   # Core application configuration
│   ├── config.py           # Environment configuration
│   └── security.py         # JWT verification utilities
├── db/                     # Database connection layer
│   ├── session.py          # Database session management
│   └── base.py             # Base model configuration
├── models/                 # SQLModel database models
│   └── task.py             # Task model definition
├── api/                    # API route definitions
│   ├── deps.py             # Dependency injection utilities
│   └── v1/                 # API version 1 routes
│       └── tasks.py        # Task-related endpoints
└── utils/                  # Utility functions
    └── auth.py             # Authentication helpers
```

Each file has specific responsibilities:
- `main.py`: Initializes FastAPI app and includes API routes
- `core/config.py`: Manages environment variables and app settings
- `core/security.py`: Handles JWT token verification logic
- `db/session.py`: Manages database sessions and connection pooling
- `db/base.py`: Defines base SQLModel configuration
- `models/task.py`: Defines the Task SQLModel with proper relationships
- `api/deps.py`: Contains dependency injection functions for authentication
- `api/v1/tasks.py`: Implements task CRUD endpoints with proper authentication
- `utils/auth.py`: Helper functions for authentication workflows

## Database Specification

Using SQLModel, the backend MUST implement:

**Task Model:**
- `id`: UUID primary key with default generation
- `title`: String (not nullable, max length 255)
- `description`: Text field (optional)
- `completed`: Boolean with default False
- `priority`: String enum ('low', 'medium', 'high') with default 'medium'
- `due_date`: DateTime (optional)
- `user_id`: String (not nullable, represents user from JWT - indexed)
- `created_at`: DateTime with timezone and default now
- `updated_at`: DateTime with timezone, nullable, updated on change

**Indexing Strategy:**
- Index on `user_id` for efficient user-based queries
- Composite index on `user_id` and `completed` for filtered queries
- Index on `due_date` for date-based queries

**Constraints:**
- All task queries MUST be filtered by `user_id` from authenticated JWT
- Foreign key constraint NOT required since user_id comes from JWT, not database users table

## Authentication & JWT Verification

The backend MUST implement:

**JWT Extraction:**
- Extract JWT from Authorization header with "Bearer " prefix
- Use `jose` library for token decoding and verification

**Token Verification:**
- Verify signature using BETTER_AUTH_SECRET environment variable
- Validate token expiration (exp claim)
- Extract user_id and email from token claims

**Claims Required:**
- `user_id`: Primary identifier for user isolation
- `email`: Additional user information (optional verification)
- `exp`: Token expiration timestamp

**Error Handling:**
- Missing token: Return 401 Unauthorized
- Invalid token format: Return 401 Unauthorized
- Expired token: Return 401 Unauthorized
- Invalid signature: Return 401 Unauthorized

## Authorization & User Isolation

The backend MUST enforce:

**Request Processing:**
- Each protected request extracts authenticated user_id from JWT
- All task queries include WHERE clause filtering by user_id
- Cross-user access attempts return 403 Forbidden

**Enforcement Rules:**
- Every task endpoint (except creation) verifies resource belongs to authenticated user
- Bulk operations (listing, filtering) only return user's own tasks
- Update and delete operations verify resource ownership before execution

**Response Codes:**
- Missing authentication: 401 Unauthorized
- Failed authorization (cross-user access): 403 Forbidden

## REST API Specification (Backend View)

**Authentication Required:** All endpoints except health check require valid JWT in Authorization header

**Base Path:** `/api/v1`

**Endpoints:**

1. **GET /tasks**
   - Authentication: Required
   - Query Parameters: `completed` (optional, true/false), `limit` (optional), `offset` (optional)
   - Response: 200 OK with array of task objects
   - Error: 401 Unauthorized, 500 Internal Server Error

2. **POST /tasks**
   - Authentication: Required
   - Request Body: JSON with `title` (required), `description`, `priority`, `due_date`
   - Response: 201 Created with created task object
   - Error: 401 Unauthorized, 422 Validation Error, 500 Internal Server Error

3. **GET /tasks/{task_id}**
   - Authentication: Required
   - Path Parameter: `task_id` (UUID string)
   - Response: 200 OK with task object or 404 Not Found
   - Error: 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error

4. **PUT /tasks/{task_id}**
   - Authentication: Required
   - Path Parameter: `task_id` (UUID string)
   - Request Body: JSON with updatable fields
   - Response: 200 OK with updated task object
   - Error: 401 Unauthorized, 403 Forbidden, 404 Not Found, 422 Validation Error, 500 Internal Server Error

5. **DELETE /tasks/{task_id}**
   - Authentication: Required
   - Path Parameter: `task_id` (UUID string)
   - Response: 204 No Content
   - Error: 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error

6. **PATCH /tasks/{task_id}/toggle**
   - Authentication: Required
   - Path Parameter: `task_id` (UUID string)
   - Request Body: Empty or JSON with completion status
   - Response: 200 OK with updated task object
   - Error: 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error

## Frontend Integration Contract

**Expected Request Headers:**
- `Authorization: Bearer <jwt_token>` for all protected endpoints
- `Content-Type: application/json` for POST/PUT/PATCH requests

**JWT Propagation:**
- Frontend stores JWT from Better Auth in secure storage
- Frontend attaches JWT to Authorization header for all API requests
- Backend treats JWT user_id as authoritative for user identification

**CORS Behavior:**
- Backend allows requests from BETTER_AUTH_URL origin
- Backend allows Authorization header in requests
- Backend enables credentials for proper cookie handling if needed

**Response Consistency:**
- Successful responses return appropriate HTTP status codes (200, 201, 204)
- Error responses return JSON with `detail` field explaining the error
- All responses use consistent data structures

## Error Handling

Standardized error responses:

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden:**
```json
{
  "detail": "Access forbidden"
}
```

**404 Not Found:**
```json
{
  "detail": "Resource not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Internal server error"
}
```

All errors MUST be returned as JSON with consistent structure.

## Performance & Scalability

**Connection Pooling:**
- Backend MUST use SQLModel's built-in connection pooling
- Configure appropriate pool size for Neon Serverless PostgreSQL
- Implement proper session disposal to avoid connection leaks

**Performance Considerations:**
- Index database queries by user_id for efficient filtering
- Use pagination for list endpoints to handle large datasets
- Optimize JWT verification with caching if needed for high-volume scenarios

**Scalability:**
- Design supports multi-user isolation at database level
- Stateless authentication allows horizontal scaling
- Connection pooling configured for optimal performance
