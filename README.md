# 🤝 The Group of Joining Hands — Enterprise Web Ecosystem

> **Full-Stack Community Platform & Professional Network Ecosystem**  
> *Official Motto:* **"Together Forever"**  
> *Zero-Cloud-Cost Architecture ($0.00 Hosting & Storage Overhead)*

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/SQLite3-Hardened%20Db-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="Database" />
  <img src="https://img.shields.io/badge/Security-PBKDF2%20%7C%20OIDC%20%7C%20JWT-DC2626?style=for-the-badge" alt="Security" />
  <img src="https://img.shields.io/badge/Responsive-Mobile%20%7C%20Tablet%20%7C%20Desktop-7C3AED?style=for-the-badge" alt="Responsive" />
</div>

---

## 📑 Interactive Table of Contents

* [⚡ Quick Start Guide (Run in 30 Seconds)](#-quick-start-guide-run-in-30-seconds)
* [🔑 Default Login Accounts & Credentials](#-default-login-accounts--credentials)
* [📂 Repository Directory Structure](#-repository-directory-structure)
* [🗄️ Database Tables Schema Explorer](#%EF%B8%8F-database-tables-schema-explorer)
* [🌐 Core API Endpoints Reference](#-core-api-endpoints-reference)
* [🎨 Visual Identity & Design Tokens](#-visual-identity-&-design-tokens)
* [🧪 Automated Tests runner CLI](#-automated-tests-runner-cli)
* [🚀 Cloud Deployment Guides](#-cloud-deployment-guides)
* [🛠️ Operations & Troubleshooting manual](#%EF%B8%8F-operations--troubleshooting-manual)

---

## ⚡ Quick Start Guide (Run in 30 Seconds)

To get the application up and running on your local machine autonomously, follow these quick steps:

### 1. Setup Environment Configuration
Create a `.env` file in the root folder with your credentials (use `.env.example` as a template):
```bash
PORT=8080
HOST=127.0.0.1
GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

### 2. Start the Server
Run using Python (standard library dependencies, zero configuration needed):
```bash
python server.py
```

### 3. Launch the App
Open your web browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 🔑 Default Login Accounts & Credentials

| Role | Email Address | Password | Description / Access Level |
| :--- | :--- | :--- | :--- |
| **Super Administrator** | `member@joininghands.org` | `demo1234` | Full access to moderation panel, security audit logs, user management, and health checks. |
| **Community Member** | `ramesh@joininghands.org` | `demo1234` | Standard member profile, timeline sharing, messaging, and RSVP rights. |
| **Instant Demo Login** | *One-Click Button* | *Auto* | Click **"One-Click Demo Login"** on the portal login screen for instant access. |

---

## 📂 Repository Directory Structure

Click to expand and inspect the exact file structure of this repository:

<details>
<summary><b>📂 Click to expand Complete Directory Layout</b></summary>

```text
joining-hands/
├── server.py                        # Main REST API entrypoint & Web Server
├── google_credentials.json           # Google Cloud client configuration JSON (git-ignored)
├── .env                             # Active environment configuration settings (git-ignored)
├── .env.example                     # Example environment config template
├── .gitignore                       # Git ignored folders & file formats list
├── README.md                        # Interactive onboarding manual (This file)
├── run_tests.ps1                    # On-demand test runner CLI script
├── requirements.txt                 # Backend Python package dependencies
├── Dockerfile                       # Multi-stage Docker container recipe
├── render.yaml                      # 1-Click Render.com deployment setup
├── Procfile                         # Heroku/Render process script
├── AGENTS.md                        # Execution rules and pre-flight guidelines
├── PROJECT_CONTEXT.txt              # Core project mandates & slogans list
├── walkthrough.md                   # Complete implementation summary report
├── hero.jpg                         # Core fallback avatar & asset
├── app/                             # Core Backend Application Logic
├── docs/                            # Documentation & Presentations
│   ├── presentations/               # Pitch & Investor Decks (.pptx)
│   ├── PROJECT_CONTEXT.txt          # Core project mandates & slogans list
│   └── Credentials.csv              # Test login credentials
├── database/                        # Persistence Layer
│   ├── database.db                  # Active SQLite Database
│   └── backups/                     # Auto-generated SQLite backups
├── static/                          # Frontend Static Assets
│   ├── css/styles.css               # Core Stylesheet
│   └── js/script.js                 # Unified Frontend JavaScript
├── templates/
│   └── index.html                   # Main Single-Page Application View
└── themes/                          # High-Res Looping Video Backgrounds (.mp4)
├── app/                             # Core Backend application codebase
│   ├── config/
│   │   └── config.py                # Environment configs & manual .env parser
│   ├── database/
│   │   └── db.py                    # SQLite connection, schema seeding & backups
│   ├── helpers/
│   │   ├── future_architecture.py   # Future module expansion specifications
│   │   ├── security.py              # PBKDF2 hashing, magic-bytes, escaping filters
│   │   ├── jwt_auth.py              # JWT generation, revocation and blacklists
│   │   └── storage.py               # Media upload file storage management
│   ├── controllers/                 # Placeholder for MVC Controllers (Empty)
│   ├── middleware/                  # Placeholder for MVC Middleware (Empty)
│   ├── models/                      # Placeholder for MVC Models (Empty)
│   ├── routes/                      # Placeholder for MVC Routes (Empty)
│   ├── services/                    # Placeholder for Business Services (Empty)
│   ├── utilities/                   # Placeholder for Utility Helpers (Empty)
│   └── validators/                  # Placeholder for Validation schemas (Empty)
├── backups/                         # Core system backup directory
│   ├── database_20260806_191101.db  # Verified database backups
│   └── database_20260813_185154.db
├── database/                        # Database workspace
│   ├── database.db                  # Local database binary copy
│   └── backups/                     # Autogenerated database backups
├── docs/                            # Internal reference manuals
│   ├── AGENTS.md                    # Pre-flight checklist guidelines
│   ├── architecture.md              # Database structural diagrams
│   ├── conversation.txt             # Initial onboarding chats
│   ├── postman_collection.json      # API test collection
│   ├── PROJECT_CONTEXT.txt          # Slogans & brand limits Context
│   └── test_cases_matrix.csv        # Comprehensive test scenarios matrix
├── logs/                            # Real-Time runtime telemetry logs
│   ├── server.log                   # Server operations & exceptions
│   └── console.log                  # Standard console output redirects
├── scripts/                         # Operational helper tools
│   └── backup.py                    # Standalone manual DB backup script
├── static/                          # Served assets compilation folder
│   ├── css/
│   │   └── styles.css               # Main visual layout stylesheets
│   ├── js/
│   │   └── script.js                # Core frontend scripts & dynamic widgets
│   ├── images/
│   │   ├── hero.jpg                 # Background graphics assets
│   │   └── k3.png
│   └── uploads/                     # User timelines uploaded photos
├── templates/                       # Backend template views
│   └── index.html                   # Global single-page application view
└── tests/                           # Unit, integrations & functional test suites
    ├── __init__.py
    ├── api_test.py                  # API post timeline feed tests
    ├── test_jwt_and_backend_solid.py # Session JWT signature validation tests
    ├── test_production_hardening.py  # DB tables and files upload validations
    ├── test_production_zero_surprise.py # CORS and core security checks
    ├── test_real_google_oauth.py     # OAuth Google verification unit tests
    └── test_six_feature_extensions.py # Mutes, blocks, search, and notification tests
```
</details>

---

## 🗄️ Database Tables Schema Explorer

Click below to expand and view the SQLite database schema tables. The database contains **28 tables** mapped to core system modules:

<details>
<summary><b>🔐 Security, JWT & User Table Columns</b></summary>

* **`users`**: Master user records.
  * Columns: `id`, `email`, `password_hash`, `google_id`, `full_name`, `headline`, `avatar_url`, `bio`, `is_admin`, `status`, `role`, `email_verified`, `location`, `cover_photo_url`, `created_at`.
* **`sessions`**: Active authentication sessions.
  * Columns: `token`, `user_id`, `created_at`.
* **`email_verification_tokens`**: Verification workflow.
  * Columns: `id`, `user_id`, `token_hash`, `expires_at`, `used`, `created_at`.
* **`password_reset_tokens`**: Reset authentication codes.
  * Columns: `id`, `user_id`, `token_hash`, `expires_at`, `used`, `created_at`.
* **`token_blacklist`**: JWT enterprise security revocation log.
  * Columns: `id`, `jti`, `token_hash`, `user_id`, `revoked_at`, `expires_at`, `reason`.
* **`login_history`**: Audit logs for user logins.
  * Columns: `id`, `user_id`, `ip_address`, `status`, `login_time`.
</details>

<details>
<summary><b>👥 Social Network, DMs & Alerts Columns</b></summary>

* **`connections`**: Member network connections.
  * Columns: `id`, `requester_id`, `receiver_id`, `status`, `created_at`.
* **`direct_messages`**: One-to-one text messaging records.
  * Columns: `id`, `sender_id`, `receiver_id`, `message_text`, `is_read`, `created_at`.
* **`notifications`**: User action feeds (mentions, comments, connections).
  * Columns: `id`, `user_id`, `sender_id`, `notif_type`, `title`, `reference_id`, `is_read`, `created_at`.
</details>

<details>
<summary><b>📝 Timeline Feed & Content Columns</b></summary>

* **`posts`**: Timeline post shares.
  * Columns: `id`, `author_id`, `content`, `media_url`, `created_at`.
* **`post_likes`**: Likes composite key map.
  * Columns: `id`, `post_id`, `user_id`, `created_at`.
* **`post_comments`**: Threaded post replies.
  * Columns: `id`, `post_id`, `user_id`, `content`, `parent_id`, `created_at`.
* **`saved_posts`**: Bookmarked post listings.
  * Columns: `id`, `user_id`, `post_id`, `created_at`.
* **`hashtags`**: Search Discovery Hashtags.
  * Columns: `id`, `tag`, `created_at`.
* **`post_hashtags`**: Junction mapping posts to hashtags.
  * Columns: `post_id`, `hashtag_id`, `created_at`.
</details>

<details>
<summary><b>📅 Articles & RSVP Events Hub Columns</b></summary>

* **`articles`**: Public long-form blogs.
  * Columns: `id`, `title`, `author_id`, `content`, `cover_url`, `created_at`.
* **`events`**: Scheduled meetups and workshops.
  * Columns: `id`, `title`, `organizer_name`, `date_str`, `location`, `description`, `banner_url`, `created_at`.
* **`event_rsvps`**: RSVPs indicating attendance.
  * Columns: `id`, `event_id`, `user_id`, `created_at`.
</details>

<details>
<summary><b>🎓 Professional Profile Columns</b></summary>

* **`profile_skills`**: Specific skills tags.
  * Columns: `id`, `user_id`, `skill_name`, `created_at`.
* **`profile_education`**: Academic history.
  * Columns: `id`, `user_id`, `institution`, `degree`, `field_of_study`, `start_year`, `end_year`, `description`, `created_at`.
* **`profile_experience`**: Professional work items.
  * Columns: `id`, `user_id`, `company`, `position`, `location`, `start_date`, `end_date`, `is_current`, `description`, `created_at`.
* **`profile_projects`**: Portfolio showcases.
  * Columns: `id`, `user_id`, `project_name`, `description`, `technologies`, `project_url`, `github_url`, `created_at`.
* **`profile_certifications`**: Certifications issued.
  * Columns: `id`, `user_id`, `cert_name`, `issuing_org`, `issue_date`, `credential_id`, `credential_url`, `created_at`.
</details>

<details>
<summary><b>🛡️ Preferences, Mutes, Blocks & Trackers Columns</b></summary>

* **`reports`**: Flagged content under review.
  * Columns: `id`, `reporter_id`, `target_type`, `target_id`, `reason`, `status`, `created_at`.
* **`blocked_users`**: Restrictions between members.
  * Columns: `id`, `user_id`, `blocked_user_id`, `created_at`.
* **`muted_users`**: Feed visibility filters.
  * Columns: `id`, `user_id`, `muted_user_id`, `created_at`.
* **`user_settings`**: Theme preferences & privacy flags.
  * Columns: `user_id`, `theme`, `language`, `privacy`, `message_privacy`, `connect_privacy`, `notifications_enabled`.
* **`issue_bugs`**: Bug tracker matrix.
  * Columns: `id`, `module`, `title`, `priority`, `status`, `fix_date`, `regression_status`.
</details>

---

## 🌐 Core API Endpoints Reference

Click below to expand and view the core REST API interface reference:

<details>
<summary><b>🔐 Authentication Endpoints</b></summary>

* `POST /api/auth/signup` - Register standard password profile.
* `POST /api/auth/login` - Authenticate standard user and issue session JWT.
* `GET /api/auth/google-client-id` - Retrieve active `GOOGLE_CLIENT_ID` securely.
* `POST /api/auth/google` - Cryptographically verify incoming Google ID Token (`credential`), auto-merge with matching email profiles, and issue session JWT.
* `POST /api/auth/logout` - Revoke JWT and blacklist token.
* `GET /api/auth/me` - Fetch profile metadata for authenticated session.
</details>

<details>
<summary><b>📝 Timeline Feed & Search Endpoints</b></summary>

* `GET /api/posts` - Fetch page-paginated feed posts.
* `POST /api/posts` - Create post with optional image upload (enforces PNG/JPG binary magic-bytes).
* `GET /api/users/search?q={query}` - Unified multi-category search returning matched profiles, posts, and trending hashtags.
</details>

---

## 🔐 UAT & Security Lock Modes

The ecosystem includes two critical lock mechanisms for staging and pre-launch testing:

1. **Visual Platform Lock (UAT Mode)**:
   * **State**: Controlled via `IS_WEBSITE_LOCKED` in `static/js/script.js`.
   * **Behavior**: Blocks the entire 3D ecosystem UI with a "BLOCKED-UAT" screen.
   * **Bypass**: Can be unlocked mid-session by typing `demo1234` in the hidden Admin Password box.
2. **Admin-Only Login Mode**:
   * **State**: Controlled via `ADMIN_ONLY_MODE` in `static/js/script.js`.
   * **Behavior**: The platform remains visually open, but standard users are blocked from logging in (throwing an "Only admin tracking is enabled" error). Only Super Administrators can log in.

## 🔠 Typography Settings

Users can customize the main hero typography on the fly via the Settings Popover:
* **Default**: Pure bold text without glass wrappers. Clean, minimal, readable.
* **Elegant**: Split-word modular icons.
* **Unified**: Uppercase layout using consistent radium-word-icon styles.

## 🎨 Visual Identity & Design Tokens

* **Slogan**: *"Together Forever"* (Bold serif styling with gold-kesari accents).
* **Background Canvas**: Pure white layout canvas.
* **Typography Hierarchy**:
  * Headings & CTA Action buttons: Geometric **Outfit** Google font.
  * Paragraphs & feed body text: **Plus Jakarta Sans** Google font.
* **Infinite Header Marquee**:
  * Glowing Violet-Indigo-Blue gradient background: `linear-gradient(135deg, #7c3aed 0%, #4f46e5 50%, #3b82f6 100%)`.
  * Marquee spacing delimiters: Star icons rendered with brand saffron/kesari tone (`#ff7700`).
* **Interactive App Cards**:
  * Original 3D letter button tiles layout (D, H, I, P, E) centered on landing view.
  * Hover states: Parallax tilt effects and inward click press movements.

---

## 🧪 Automated Tests Runner CLI

The test runner CLI script ([`run_tests.ps1`](run_tests.ps1)) allows running specific modules on-demand without executing the entire suite:

<details>
<summary><b>💻 Click to view Test Suite Commands</b></summary>

* **Run all tests**:
  ```powershell
  .\run_tests.ps1
  ```
* **Run JWT Verification suite**:
  ```powershell
  .\run_tests.ps1 jwt
  ```
* **Run Google OAuth verification suite**:
  ```powershell
  .\run_tests.ps1 google
  ```
* **Run Safe Feature extensions suite**:
  ```powershell
  .\run_tests.ps1 extensions
  ```
* **Run REST API feed suite**:
  ```powershell
  .\run_tests.ps1 api
  ```
</details>

---

## 🚀 Cloud Deployment Guides
### 🚀 Render.com Deployment & Custom Domains
When deploying to a new Render account or configuring `joininghandsgroup.com`:
1. **Environment Variables**: You *must* manually add `GOOGLE_CLIENT_ID` in the Render Environment tab. If this is missing, the "Login with Google" button will automatically hide itself.
2. **Custom Domain (`www`)**: When adding the domain, ensure your DNS provider (e.g., GoDaddy) has a `CNAME` record for `www` pointing to the exact `.onrender.com` address generated by Render.



Click below to expand and view instructions to deploy this platform to the public web for **$0.00 / month**:

<details>
<summary><b>☁️ Deploying on Render.com (1-Click Blueprint)</b></summary>

1. Push this repository to [GitHub](https://github.com).
2. Sign up at [Render.com](https://render.com) (Free Tier).
3. Click **"New +"** ➔ **"Blueprint"** ➔ Select your repository.
4. Render automatically reads [`render.yaml`](render.yaml) and deploy the service.
5. Your platform is deployed live with a free SSL domain!
</details>

<details>
<summary><b>🐋 Deploying with Docker Containers</b></summary>

To run the container locally or push to Railway/Koyeb:
```bash
docker build -t joining-hands .
docker run -p 8080:8080 joining-hands
```
</details>

---

## 🛠️ Operations & Troubleshooting Manual

<details>
<summary><b>1. Port Conflict (`Address already in use`)</b></summary>

If port `8080` is occupied on your computer, set a custom port via environment variable:
* **Windows (PowerShell)**:
  ```powershell
  $env:PORT="9000"; python server.py
  ```
* **macOS / Linux (Bash)**:
  ```bash
  PORT=9000 python server.py
  ```
</details>

<details>
<summary><b>2. Reset Database to Factory State</b></summary>

To wipe all database records and seed fresh factory demo data:
* **Windows (PowerShell)**:
  ```powershell
  Remove-Item database/database.db; python server.py
  ```
* **macOS / Linux (Bash)**:
  ```bash
  rm database/database.db && python server.py
  ```
</details>

---

**Together Forever.** 🤝
