# ShadowGym — Gym Management System

A complete web-based gym administration system built with **Django** and a custom dark UI. Manages members, memberships, payments, and daily attendance tracking with QR codes.

🇪🇸 [Ver en Español](README.md)

---

## Key Features

### 🏋️ Member Management
- Full CRUD: register, edit, and delete members
- Real-time search by name, ID number, or phone
- Attendance filters: All / Checked in today / Pending today
- Membership status with automatic expiry tracking

### 📋 Membership Plans
- Flexible plan duration (days, weeks, months)
- Per-plan pricing with usage statistics
- Automatic link to payment records

### 💳 Payments
- Multi-method payment registration
- Automatic membership date calculation on payment
- Dashboard with monthly and historical revenue

### ✅ Daily Attendance Control
- Check-in by **unique access code** or ID number
- Real-time **QR code scanner** via device camera (html5-qrcode)
- Access validation: blocks entry if membership expired or inactive
- Automatic cleanup of previous day's attendance records
- Live "Today's Attendance" panel

### 📧 QR Code by Email
- Unique QR generated per member (`qrcode` library)
- Email delivery with QR image attached (Gmail SMTP)
- QR preview in modal without leaving the page

### 🔐 Authentication
- Login/logout using Django's built-in auth
- All views protected with `@login_required`
- Automatic redirect to login on app open

### ⚡ No-Reload UX
- Mark attendance without page reload (fetch + row update)
- Edit records in a floating modal
- Send QR with visual response in modal
- Toast notifications for immediate feedback

### 🎨 Interface
- Custom dark theme with yellow accent (#ffde59)
- Fixed sidebar (`position: fixed`)
- Fully static layout — only the table scrolls
- Mobile-responsive design (≤600px)
- Login screen with background video and visual panel

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14 + Django 6 |
| Database | SQLite (development) |
| Frontend | HTML, CSS Grid/Flexbox, JavaScript (Fetch API) |
| QR Generation | `qrcode[pil]` |
| Email | Gmail SMTP via Django Email |
| QR Scanner | `html5-qrcode` (CDN) |
| Version Control | Git + GitHub |

---

## Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/Jhoyder/ShadowGym.git
cd ShadowGym

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install django qrcode[pil]

# 4. Apply migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

Open in browser: `http://127.0.0.1:8000/`

---

## Email Configuration (Gmail)

In `shadowfit/settings.py`:

```python
EMAIL_HOST_USER = 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'  # Google App Password
```

Steps to get an App Password:
1. Enable 2-Step Verification on your Google Account
2. Go to **Security → App Passwords**
3. Generate one for "Mail" and paste it into `EMAIL_HOST_PASSWORD`

---

## Project Structure

```
ShadowGym/
├── members/          # Members, attendance, QR
├── memberships/      # Membership plans
├── payments/         # Payments
├── shadowfit/        # Django settings
├── templates/
│   ├── dashboard/    # Base shell, sidebar partial, modal
│   ├── members/      # Members dashboard + QR register page
│   ├── memberships/  # Plans dashboard
│   ├── payments/     # Payments dashboard
│   └── registration/ # Login
└── static/
    ├── css/          # dashboard.css, login.css
    ├── img/          # Logo
    └── video/        # Login background video
```

---

## Main Views

### members
| URL | View | Description |
|---|---|---|
| `/members/` | `dashboard` | KPI panel and member list |
| `/members/registro/` | `attendance_register` | Dedicated check-in page |
| `/members/attendance/by-code/` | `mark_attendance_by_code` | Code-based check-in |
| `/members/<pk>/attendance/` | `mark_attendance` | Mark attendance (AJAX/JSON) |
| `/members/<pk>/qr/` | `member_qr` | QR image for member |
| `/members/<pk>/send-code/` | `send_member_code_email` | Send QR via email |

### memberships
| URL | View | Description |
|---|---|---|
| `/memberships/` | `dashboard` | Plans overview |

### payments
| URL | View | Description |
|---|---|---|
| `/payments/` | `dashboard` | Payment panel with revenue stats |

---

## What I Built & Learned

- Designed and implemented a full-stack Django application from scratch
- Built a custom dark UI without any CSS framework
- Integrated real-time QR scanning using the device camera via JavaScript
- Implemented partial page updates with the Fetch API (no SPA framework)
- Configured Gmail SMTP for transactional email with QR attachments
- Applied Django signals and model-level logic for automatic data updates
- Structured templates with inheritance and reusable partials

---

## Author

**Jhoyder** — Personal portfolio project.

- GitHub: [@Jhoyder](https://github.com/Jhoyder)

---

## License

Personal and educational use.
