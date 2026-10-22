# 💼 Job Portal - Full Stack Web Application

A full-stack, production-ready **Job Portal** platform designed to connect **Job Seekers** with **Recruiters**. Recruiters can create and manage job vacancies, while job seekers can search, filter, view openings, and submit their resumes.

---

## 🛠️ Tech Stack

This project is built using modern full-stack web technologies:

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | **React.js** / Modern UI | Interactive Single Page Application (SPA), component-driven UI, responsive layout |
| **Backend** | **Python / Django** | Robust backend MVC/MVT architecture, ORM, secure authentication, role-based access control |
| **Database** | **PostgreSQL** | Relational SQL database for ACID compliance, scalable query performance, data integrity |
| **Media & Storage** | **Django File Storage** | Secure resume file uploads (`.pdf`, `.doc`, `.docx`) with validation |
| **Styling** | **Bootstrap 5 / CSS3** | Clean, mobile-first responsive design |

---

## ✨ Key Features

### 👤 Role-Based Authentication & Authorization
- **Job Seeker**:
  - Register as a candidate.
  - Search and filter jobs by keywords, company, location, and job type.
  - View full job descriptions, salary brackets, and recruiter info.
  - Apply with resume upload (supports PDF, DOC, DOCX; required size: 50 KB to 1 MB).
  - Built-in duplicate application prevention.
- **Recruiter**:
  - Register as an employer / recruiter.
  - Post new job openings with title, company name, location, salary, job type, and detailed description.
  - Manage and track job postings.
- **Admin**:
  - Django Admin dashboard for full user, job, and application management.

### 🔍 Advanced Job Search & Filters
- Real-time keyword search (title, company, skills, description, city).
- Filter by Job Type: *Full Time, Part Time, Internship, Remote, Contract*.
- Instant filter reset.

### 📁 Resume Upload & Document Validation
- Server-side file validation (checks extension and maximum size limit).
- Organized media root handling for uploaded CVs.

---

## 📁 Project Structure

```text
job_portal/
├── accounts/               # User Authentication & Profiles App
│   ├── models.py           # Custom User model with Role (Seeker / Recruiter / Admin)
│   ├── forms.py            # Registration Form with role selection
│   ├── views.py            # Auth views (Register, Login, Logout)
│   ├── urls.py             # Auth URL routing
│   └── tests.py            # Unit tests for authentication & roles
│
├── jobs/                   # Jobs & Applications App
│   ├── models.py           # Job & Application models with constraints
│   ├── forms.py            # JobForm & ApplicationForm with resume validation
│   ├── views.py            # Job listing, search, detail, post job, apply job
│   ├── urls.py             # Jobs URL routing
│   └── tests.py            # Unit tests for jobs, application & duplicate checks
│
├── config/                 # Project Configuration
│   ├── settings.py         # Django settings (PostgreSQL, Media, Apps)
│   ├── urls.py             # Main routing configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── templates/              # HTML Templates (Bootstrap 5 UI)
│   ├── base.html           # Main layout, Navbar with role badges, messages
│   ├── home.html           # Landing page with search & recent openings
│   ├── login.html          # Clean sign-in card
│   ├── register.html       # Role-based sign-up card
│   ├── job_list.html       # Search, filter, and job cards
│   ├── job_detail.html     # Dedicated job description page
│   ├── post_job.html       # Recruiter job posting form
│   └── apply_job.html      # Seeker resume upload form
│
├── media/                  # Uploaded resumes and assets
├── manage.py
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started (Installation & Setup)

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python** (v3.10 or higher)
- **PostgreSQL** (v14 or higher)
- **Node.js & npm** (v18 or higher) - *for React frontend*
- **Git**

---

### 2. Database Configuration (PostgreSQL)

1. Open your PostgreSQL prompt or pgAdmin:
   ```bash
   sudo -u postgres psql
   ```
2. Create database and user:
   ```sql
   CREATE DATABASE job_portal_db;
   CREATE USER job_user WITH PASSWORD 'your_secure_password';
   ALTER ROLE job_user SET client_encoding TO 'utf8';
   ALTER ROLE job_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE job_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE job_portal_db TO job_user;
   \q
   ```

3. In `config/settings.py`, configure the PostgreSQL database:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'job_portal_db',
           'USER': 'job_user',
           'PASSWORD': 'your_secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

---

### 3. Backend Setup (Django)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/job_portal.git
   cd job_portal
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django psycopg2-binary
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The backend server will start at: `http://127.0.0.1:8000/`

---

### 4. Frontend Setup (React.js)

To run the React client application:

1. Navigate to the frontend directory (e.g., `frontend/`):
   ```bash
   cd frontend
   ```
2. Install frontend dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm start
   ```
   The React application will run at: `http://localhost:3000/`

---

## 🧪 Running Automated Tests

Run the full suite of unit and integration tests:

```bash
python manage.py test
```

Expected output:
```text
Found 9 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 9 tests in 4.826s

OK
Destroying test database for alias 'default'...
```

---

## 🔒 Security & Best Practices

- **Role Authorization:** Protected views using `@login_required` and strict role verification.
- **CSRF Protection:** Secure CSRF tokens on all POST/mutating requests.
- **File Upload Safety:** Extension whitelist (`.pdf`, `.doc`, `.docx`) and file size validation (required between 50 KB and 1 MB).
- **Secure Logout:** Implements HTTP POST logout to prevent cross-site logout vulnerabilities.
- **Data Integrity:** Database-level `UniqueConstraint` on `(job, seeker)` to prevent duplicate applications.

---

## 🛣️ API / URL Routes Reference

| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Public | Home / Landing Page with search & recent openings |
| `/jobs/` | `GET` | Public | Browse all jobs with search and type filters |
| `/jobs/<id>/` | `GET` | Public | Job details view |
| `/jobs/post/` | `GET, POST` | Recruiter | Post a new job vacancy |
| `/jobs/apply/<id>/` | `GET, POST` | Seeker | Upload resume and apply for a job |
| `/jobs/my-applications/` | `GET` | Seeker | View candidate's applied jobs & status tracker |
| `/jobs/my-jobs/` | `GET` | Recruiter | Manage recruiter's posted openings & applicant stats |
| `/jobs/<id>/applicants/` | `GET` | Recruiter | View all applicants, download CVs & filter status |
| `/jobs/application/<id>/status/<status>/` | `GET, POST` | Recruiter | Update applicant status (Shortlist / Reject) |
| `/jobs/<id>/edit/` | `GET, POST` | Recruiter | Update job listing specifications |
| `/jobs/<id>/delete/` | `GET, POST` | Recruiter | Delete job listing |
| `/accounts/profile/` | `GET, POST` | Authenticated | Manage user profile, avatar, skills, or company info |
| `/accounts/register/` | `GET, POST` | Public | Register as Seeker or Recruiter |
| `/accounts/login/` | `GET, POST` | Public | Login to account |
| `/accounts/logout/` | `POST` | Authenticated | Logout securely |
| `/admin/` | `GET, POST` | Admin | Django administration panel |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

