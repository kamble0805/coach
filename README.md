# Coaching Class Admission & Fee Management System – In Progress 🚧

This project is a **Django-based web application** designed for **coaching institutes** to efficiently manage **student admissions**, **class-wise and board-wise fee structures (SSC/CBSE)**, and **payment tracking**. It supports role-based features for administrators and teaching staff and is engineered to scale with institute requirements.

---

## 🔑 Key Features

- 📝 **Student Admission System** (Class 1–10)
- 🧾 **Board-wise (SSC/CBSE) Fee Structure Management**
- 💵 **Payment Recording** (Full & Partial Support)
- 📊 **Payment Receipts and Installment Tracking**
- 🔍 **Search & Filter Student Records**
- 🧑‍💼 **Admin Panel for Oversight & Updates**
- 🖼️ **Bootstrap-Powered UI (Customizable)**
- 📤 **Future-Ready for Online Payments, SMS Alerts, and Analytics**

---

## 🧰 Technologies Used

- **Python 3.13.1**
- **Django 5.2**
- **PostgreSQL** *(Development supports SQLite3)*
- **HTML5 + CSS3 + Bootstrap 5**
- **QR Code Integration** (Optional via `qrcode` library)
- **Static & Media Handling** via Django config

---

## ⚙️ Local Development Setup

### 📋 Prerequisites

- Python 3.10 or later
- Git
- pip (Python package manager)
- Virtualenv *(optional but recommended)*

### 🧪 Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/kamble0805/coach.git
cd coach

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create superuser for admin access
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then, open `http://127.0.0.1:8000/` in your browser.

---

## 📁 Project Structure

```
coach/
├── admissions/               # Student admission, payments, fee logic
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/admissions/
│       ├── register_student.html
│       ├── view_students.html
│       ├── register_payment.html
│       └── update_fee_structure.html
├── accounts/                 # (Optional: User management or roles)
├── coach/                    # Core Django settings and URLs
├── static/                   # Bootstrap, JS, CSS (to be customized)
├── templates/                # Global templates if any
├── manage.py
└── requirements.txt
```

---

## 🚧 Future Roadmap

- ✅ Class-based fee management
- ✅ Installment-based payment logging
- 🔄 Stripe / Razorpay integration (Online Payments)
- 📧 Email/SMS fee due reminders
- 📁 Export reports to PDF/Excel
- 🧑‍🏫 Role-based access (Admin / Teacher)
- 📈 Dashboard with analytics for admissions and payments

---

## 🙋‍♂️ Maintainer

**Shubham Kamble**  
*Full Stack Developer – Django | Python | Web Technologies*  
📧 Email: your.email@example.com  
🔗 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
