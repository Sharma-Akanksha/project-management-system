Mini Project Management System

A simplified multi-tenant project management system built as part of a software engineering screening task.
The application demonstrates backend API design using Django + GraphQL and a frontend dashboard using React + TypeScript + Apollo Client.

Tech Stack
Backend


Python 3.10+


Django 4.x


Graphene-Django (GraphQL)


PostgreSQL (recommended) / SQLite (local)


Django ORM


Frontend


React 18+


TypeScript


Apollo Client


TailwindCSS



Features Implemented
Backend


Multi-tenant data model with organization-based isolation


GraphQL API for:


Listing projects by organization


Creating projects and tasks


Computing project statistics:


Total tasks


Completed tasks


Completion rate






Clean relational models:


Organization


Project


Task


TaskComment




Frontend


Project dashboard listing projects with:


Status


Task count


Completed tasks


Completion rate




Apollo Client integration


TypeScript interfaces for strong typing


Loading and error states



Project Structure
project-root/
│
├── backend/
│   ├── core/
│   │   ├── models.py
│   │   ├── schema.py
│   │   └── mutations.py
│   ├── project/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── graphql/
│   │   │   ├── queries.ts
│   │   │   └── mutations.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
│
├── screenshots/
│   └── dashboard.png
│
├── README.md
└── TECHNICAL_SUMMARY.md


Setup Instructions
Prerequisites


Node.js 18+


Python 3.10+


Git


PostgreSQL (optional — SQLite works for local)



Backend Setup (Django + GraphQL)
cd backend

1. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

2. Install dependencies
pip install -r requirements.txt

3. Database setup
By default, SQLite is used for simplicity.
(Optional) Configure PostgreSQL in settings.py if required.
4. Run migrations
python manage.py makemigrations
python manage.py migrate

5. Create superuser (optional)
python manage.py createsuperuser

6. Start backend server
python manage.py runserver

Backend will run at:
http://localhost:8000/

GraphQL Playground:
http://localhost:8000/graphql/


Frontend Setup (React + Apollo)
cd frontend

1. Install dependencies
npm install

2. Start frontend server
npm start

Frontend will run at:
http://localhost:3000/


GraphQL Usage Examples
Query: List Projects for an Organization
query {
  projects(organizationSlug: "test-org") {
    id
    name
    taskCount
    completedTasks
    completionRate
  }
}


Mutation: Create Task
mutation {
  createTask(
    projectId: "1"
    organizationSlug: "test-org"
    title: "Complete interview task"
    status: "DONE"
  ) {
    task {
      id
      title
      status
    }
  }
}


Organization-Based Multi-Tenancy


All queries and mutations require an organizationSlug


