# 🐾 VetSphere — Pet Care Management System

A full-featured, role-based **Pet Care Management System** built with Django — designed for veterinary clinics and pet care centers to streamline appointments, billing, staff management, and CRM operations.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.0%2B-green?style=flat-square&logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Modules](#-project-modules)
- [User Roles & Permissions](#-user-roles--permissions)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 About the Project

**VetSphere** is a comprehensive Django-based web application built to modernize and automate the day-to-day operations of veterinary clinics and pet care centers. From managing pet records and booking appointments to generating invoices and tracking staff rosters — VetSphere brings everything under one unified platform.

Whether you're a clinic admin managing operations, a staff member updating records, or a pet owner tracking your pet's health history, VetSphere provides a seamless and intuitive experience for all.

---

## ✨ Key Features

- 🐶 **Pet Management** — Register pets with full profiles including breed, age, medical history, and daily health logs.
- 📅 **Booking & Appointments** — Schedule, update, and manage appointments for grooming, checkups, vaccinations, and more.
- 📊 **CRM Dashboard** — Track customer interactions, messages, follow-ups, and overall clinic activity in real time.
- 🧾 **Billing & Invoicing** — Automatically generate PDF invoices and manage payment records for each service.
- 👨‍⚕️ **Staff Roster Management** — Organize staff schedules, shift assignments, and availability efficiently.
- 🔐 **Secure Authentication** — Role-based login and registration system with separate dashboards for Admins and Users.
- 📸 **User Profiles** — Support for custom profile avatars and personal account settings.
- 📱 **Responsive UI** — Fully mobile-friendly interface built with Bootstrap 5 and custom CSS.

---

## 💻 Tech Stack

| Category        | Technology                              |
|-----------------|-----------------------------------------|
| Backend         | Python 3.8+, Django 5.0+               |
| Frontend        | HTML5, CSS3, JavaScript, Bootstrap 5   |
| Database        | SQLite3 (Default)                       |
| PDF Generation  | xhtml2pdf                               |
| Image Handling  | Pillow                                  |
| Testing         | pytest-django                           |
| Version Control | Git & GitHub                            |

---

## 🗂️ Project Modules

| Module       | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| `accounts`   | User authentication, registration, login, and profile management         |
| `pets`       | Pet registration, medical history, and health log management             |
| `bookings`   | Appointment scheduling and management for various pet care services      |
| `crm`        | Customer relationship management — messages, interactions, and follow-ups|
| `billing`    | Invoice generation (PDF), payment tracking, and billing records          |
| `rosters`    | Staff schedule management and shift assignment                           |
| `dashboard`  | Centralized overview dashboard for admin and users                       |

---

## 👥 User Roles & Permissions

### 👑 Admin
- Full access to all modules and data.
- Manage users — create, activate, deactivate accounts.
- Oversee all bookings, billing, and staff rosters.
- Access the CRM dashboard for clinic-wide insights.

### 👤 User (Pet Owner / Staff)
- Register and manage their own pet profiles.
- Book and view appointments.
- View billing history and download invoices.
- Update personal profile and account settings.

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher**
- Git installed on your system
- pip (Python package manager)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/SELVAKUMAR-ANALYST/VetSphere.git
cd VetSphere
```

**2. Set up a Virtual Environment:**
```bash
python -m venv venv
```

**3. Activate the Virtual Environment:**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

**4. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**5. Run Database Migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Create a Superuser (Admin Account):**
```bash
python manage.py createsuperuser
```

**7. Start the Development Server:**
```bash
python manage.py runserver
```

**8.** Open your browser and navigate to 👉 `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
VetSphere/
│
├── accounts/           # User auth, profiles, login/register
├── pets/               # Pet registration and health records
├── bookings/           # Appointment scheduling system
├── crm/                # CRM dashboard and customer interactions
├── billing/            # Invoicing and payment management
├── rosters/            # Staff roster and shift management
├── dashboard/          # Main dashboard views
├── templates/          # HTML templates (base + per-app)
├── static/             # CSS, JS, images, and static assets
├── media/              # Uploaded files (profile pictures, etc.)
├── pet_care_management/ # Django project settings & URLs
├── manage.py           # Django management entry point
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/YourFeatureName`
3. Commit your changes: `git commit -m 'Add YourFeatureName'`
4. Push to the branch: `git push origin feature/YourFeatureName`
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Developed with ❤️ by <strong>Selva Kumar S</strong>
</p>
