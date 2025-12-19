<h1 align="center" style="color:#D4AF37;">
  🎓 Student Counseling Web Application
</h1>

<h3 align="center" style="color:#B8860B;">
  Secure Admissions · Percentage-Based Seat Allocation · Fee Verification · Email Automation
</h3>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&pause=1000&color=D4AF37&center=true&vCenter=true&width=750&lines=Automating+Student+Admissions;Seat+Allocation+Based+on+Percentage;Fee+Verification+Workflow;PDF+Offer+Letter+Generation;Built+with+Django+and+Tailwind" />
</p>

---

## Project Overview

The **Student Counseling Web Application** is a full-stack Django-based system designed to digitize and automate the **student counseling and admission workflow**.

It provides a structured process for:
- Student registration
- Percentage-based seat allocation
- Fee receipt verification
- Email-based communication
- PDF offer letter generation

The application is optimized for **local development** and **Render free-tier deployment**.

---

## Key Features

### Authentication & Security
- Email-based authentication
- Secure password reset via email (token-based)
- Role-based access for **Admin** and **Students**

---

### Student Panel
- Student registration and login
- Submission of personal and academic details
- Upload **fee receipt image**
- View fee status (Paid / Not Paid)
- View **seat allocation result**
- Download **offer letter (PDF)**
- Password reset via email

---

###  Admin Panel
- Dedicated admin dashboard
- **Search students by name and percentage only**
- View complete student profiles
- Review uploaded fee receipt images
- Mark fees as **Paid / Not Paid**
- **Seat allocation based on percentage cut-off**
- Generate and issue **PDF offer letters**
- Centralized student record management

---

## Email System

### Gmail SMTP (Localhost)
- Used during development
- Fully functional in local environment

### SendGrid SMTP (Production)
- Integrated to support **Render free-tier deployment**
- Used due to Gmail SMTP limitations on free cloud hosting
- Handles password reset and system notifications reliably

---

## File Upload & Verification
- Secure upload of fee receipt images
- Admin-side preview before verification
- Controlled media handling

---

## PDF Generation
- Automatic offer letter generation
- Triggered after seat allocation
- Downloadable by students
- Professional document structure

---

## Tech Stack

<p>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/TailwindCSS-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/SendGrid-0080FF?style=for-the-badge&logo=sendgrid&logoColor=white" />
  <img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white" />
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black" />
</p>

---

### Authentication
- Login Page  
- Password Reset via Email


---

## Deployment (Render)

- Gunicorn used as production server
- Application binds automatically to `$PORT`

### Environment Variables

```env
# SECURITY WARNING: keep the secret key used in production secret
SECRET_KEY=

DEBUG=

DOMAIN=
PROTOCOL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

SENDGRID_API_KEY=
```
## 📄 License

This project is developed for academic and learning purposes.


<hr style="border: none; height: 1px; background: linear-gradient(to right, transparent, #D4AF37, transparent);" />

<p align="center" style="color:#8B8000;">
  <em>Built with care · Designed for real-world academic workflows</em>
</p>


