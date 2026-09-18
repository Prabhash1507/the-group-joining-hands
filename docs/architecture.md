# The Group of Joining Hands - Enterprise Architecture

## 1. System Overview
**The Group of Joining Hands** is an enterprise-grade community ecosystem featuring:
- **Pure White Landing Page**: High-resolution sacred bull hero photo (`static/images/hero.jpg`), bold typography, slogan `"Together Forever"`, and dual portal ecosystem cards.
- **ProConnect Network**: Professional social network portal with feed timeline, image attachments, real-time messaging, connections manager, events RSVP, saved items bookmarks, and settings center.
- **GramConnect Visual Portal**: Full-screen photo lightbox gallery and visual storytelling.
- **Administration & Quality Assurance**: In-app workflow status board, bug quality tracker, and comprehensive Admin Control Panel.

## 2. Directory Architecture Breakdown
```
project-root/
├── app/                  # Application Modules
│   ├── config/           # Configuration & constants
│   ├── database/         # SQLite Connection & Initialization
│   ├── helpers/          # Security & hashing helpers
│   ├── routes/           # REST API endpoints
│   ├── controllers/      # Business logic handlers
│   ├── services/         # Application services
│   ├── middleware/       # Rate limiting & security headers
│   ├── models/           # Data schemas
│   ├── utilities/        # Utility helpers
│   └── validators/       # Input validators
├── static/               # Web Application Assets
│   ├── css/              # Design System Stylesheet (styles.css)
│   ├── js/               # Frontend Client Logic (script.js)
│   ├── images/           # Static photo assets (hero.jpg, k3.png)
│   └── uploads/          # User photo uploads & avatars
├── templates/            # Single Page Application Templates (index.html)
├── database/             # Relational Database Storage
│   ├── database.db       # Primary SQLite database
│   └── backups/          # Timestamped automated backups
├── docs/                 # Documentation & Specification Logs
├── tests/                # Automated Test Suites
├── logs/                 # Operational Log Output
├── scripts/              # Maintenance Automation Scripts
├── server.py             # Enterprise Root Entry Point
├── requirements.txt      # Python Manifest
└── README.md             # Enterprise Documentation
```

## 3. Data Integrity & Security Standards
- **Zero Cloud Cost**: 100% standard library Python + local disk uploads.
- **Data Backup**: Timestamped SQLite backups saved to `database/backups/`.
- **Sanitization**: SQL Injection protection via parameterized queries & HTML XSS escaping.
