# 🎓 EduManage — College Management System

A full-featured Django college management system with **Admin**, **Teacher**, and **Student** roles.

---

## 📦 Features

| Module       | Admin                              | Teacher                        | Student                   |
|--------------|-----------------------------------|-------------------------------|---------------------------|
| **Users**    | Create/Edit/Delete all users       | View profile                  | View/Edit own profile     |
| **Courses**  | Create, assign teacher & students  | View assigned courses         | View enrolled courses     |
| **Classes**  | Create, assign teacher & students  | View own classes              | View enrolled classes     |
| **Attendance**| View all sessions & reports       | Take/Edit attendance per class| View own attendance %     |
| **Assignments**| View all, manage              | Create/Edit/Grade per class   | View, Submit, see grades  |
| **Fees**     | Create fees, view all payments     | —                             | View fees, make payments  |

---

##  Quick Setup

### 1. Prerequisites
- Python 3.10+ installed

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations users
python manage.py makemigrations courses classes attendance assignments fees
python manage.py migrate
```

### 5. Seed demo data (recommended)
```bash
python seed_data.py
```

This creates all demo users, courses, classes, attendance, assignments, and fee records.

### 6. Start the server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000/
```

---

## 🔑 Demo Login Credentials

| Role     | Username   | Password     |
|----------|-----------|--------------|
| Admin    | admin     | admin123     |
| Teacher  | teacher1  | teacher123   |
| Teacher  | teacher2  | teacher123   |
| Student  | student1  | student123   |
| Student  | student2  | student123   |
| Student  | student3  | student123   |
| Student  | student4  | student123   |

---

## 📁 Project Structure

```
cms/
├── manage.py
├── requirements.txt
├── seed_data.py              ← Run this to load demo data
├── college_management/       ← Django project settings
│   ├── settings.py
│   └── urls.py
├── core/                     ← Dashboard & base views
├── users/                    ← Custom user model (admin/teacher/student)
├── courses/                  ← Course management
├── classes/                  ← Classroom management
├── attendance/               ← Attendance sessions & records
├── assignments/              ← Assignments & submissions & grading
├── fees/                     ← Fee records & payments
├── static/
│   ├── css/main.css          ← Full custom CSS
│   └── js/main.js            ← Frontend JS
└── templates/
    └── base.html             ← Shared layout with sidebar
```

---

## 🔄 Workflow

### Admin Flow
1. Login → Dashboard with stats
2. **Users** → Add teachers and students
3. **Courses** → Create course, assign teacher + students
4. **Classes** → Create class, assign course + teacher + students
5. **Fees** → Add fee records to students
6. Monitor attendance reports and assignment submissions

### Teacher Flow
1. Login → See assigned classes & recent assignments
2. **Classes** → Click ✅ Take Attendance for any class
3. **Assignments** → Create assignments for classes, grade submissions
4. **Attendance** → View session history & student reports

### Student Flow
1. Login → See attendance %, pending fees, recent assignments
2. **Assignments** → Submit files or text answers
3. **Fees** → View fee records, make payments
4. **Attendance** → View report (attendance %)

---

## 🛠 Manual Admin (Django Admin Panel)
```
http://127.0.0.1:8000/django-admin/
```
Create a superuser if needed:
```bash
python manage.py createsuperuser
```

---

## 📝 Notes
- SQLite database (db.sqlite3) — no external DB needed
- File uploads stored in `media/` folder
- Change `SECRET_KEY` in `settings.py` before production
- Set `DEBUG = False` and configure `ALLOWED_HOSTS` for production
