# 🎓 E-Learning Platform API

A robust and scalable **E-Learning Platform API** developed with Django and Django REST Framework. This backend system facilitates the creation, management, and delivery of online courses, supporting features akin to platforms like Udemy or Skillshare.

---

## 🚀 Features

- **User Management**: JWT-based authentication with roles for Students, Instructors, and Admins.
- **Course Management**: Instructors can create, update, and delete courses with detailed metadata.
- **Lecture Content**: Structured course content with sections and lectures, supporting various media types.
- **Enrollment & Payments**: Secure enrollment processes with Stripe integration for paid courses.
- **Access Control**: Role-based permissions ensuring appropriate content access.
- **Reviews & Ratings**: Students can provide feedback, influencing course ratings.
- **Certificate Generation**: Automated PDF certificates upon course completion.
- **Admin Dashboard**: Comprehensive analytics and management tools for administrators.

---

## 🧱 Modules Overview

### 1. User Module
- JWT Registration/Login
- User roles: Student, Instructor, Admin
- Profile management: name, bio, profile picture, social links

### 2. Course Module
- CRUD operations for courses
- Course attributes: Title, Description, Price, Category, Tags, Level
- Media uploads: Thumbnails and videos via AWS S3 or Cloudinary
- Course listing with search, filter, and pagination

### 3. Lecture Module
- Structured course content with sections and lectures
- Lecture details: Video, Title, Notes (Markdown), Resources (PDF, ZIP)
- Tracking lecture completion per student

### 4. Enrollment & Payment
- Enrollment in free or paid courses
- Stripe integration for secure payments
- Payment history and invoice generation using Celery

### 5. Access Control
- Content access restricted to enrolled users
- Instructors can view their course statistics
- Admins have full access to all data

### 6. Reviews & Ratings
- Students can rate and review courses
- Calculation of average ratings per course
- Sorting courses based on ratings

### 7. Certificate Generator (Bonus)
- Automatic certificate generation upon 100% course completion
- PDF certificates delivered via Celery
- Downloadable certificate links for students

### 8. Admin Dashboard (Optional API)
- Analytics: Total users, instructors, revenue (daily/monthly)
- Insights: Most popular courses, top instructors

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **Media Storage**: AWS S3 or Cloudinary
- **Asynchronous Tasks**: Celery with Redis
- **Payments**: Razorpay/Stripe API 
