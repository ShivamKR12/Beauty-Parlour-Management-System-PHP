# Beauty Parlour Management System (BPMS)

A web-based Beauty Parlour & Salon Management System built in **PHP / MySQL** with an accompanying **Python (Flask)** API and modern templating bridge.

It provides appointment scheduling, service catalog management, invoice generation, customer history, and an administrative control panel.

## 🌟 Key Features

### 👤 Customer Features
- **Browse Services**: View detailed salon service descriptions, pricing, and timing.
- **Online Appointment Booking**: Select preferred appointment date, time, and service package.
- **Booking & Invoice History**: Track current appointment status (New, Accepted, Rejected) and view printable receipts/invoices.
- **User Authentication**: Secure customer registration, login, profile editing, and password recovery.

### 🛡️ Admin Dashboard (`admin/`)
- **Dashboard Overview**: Metrics for total customers, total appointments, accepted/rejected bookings, and total sales.
- **Appointment Processing**: Review new booking requests, update appointment status, and assign remarks.
- **Service Management**: Add, update, and manage beauty and salon service packages.
- **Invoicing & Billing**: Generate itemized customer invoices for rendered services.
- **Sales & Customer Reports**: Generate date-range sales reports and customer lists.

### 🐍 Python / Flask Backend (`app.py`)
- Modern REST API endpoints (`/api/aboutus`, `/api/appointment/<aptnumber>`) and Jinja2 frontend templates (`templates/`) for appointment tracking.

---

## 🚀 Getting Started

### Prerequisites

- **Web Server**: Apache & MySQL (e.g. XAMPP, WampServer, or LAMP stack).
- **PHP**: 7.4 or 8.x.
- **Python**: 3.8+ (if running the Flask API).

---

### PHP / Apache Setup (XAMPP / WAMP)

1. Clone or copy the project into your web server's root directory:
   ```bash
   git clone https://github.com/ShivamKR12/Beauty-Parlour-Management-System-PHP.git
   ```
   *(e.g., in `C:\xampp\htdocs\bpms`)*

2. Start **Apache** and **MySQL** in your XAMPP/WAMP control panel.

3. Open **phpMyAdmin** (`http://localhost/phpmyadmin/`), create a database named `bpmsdb`, and import [`bpmsdb.sql`](bpmsdb.sql).

4. Verify database connection credentials in:
   - [`includes/dbconnection.php`](includes/dbconnection.php)
   - [`admin/includes/dbconnection.php`](admin/includes/dbconnection.php)

5. Open the web application:
   - **User Portal**: `http://localhost/bpms/`
   - **Admin Portal**: `http://localhost/bpms/admin/`

---

### Python / Flask API Setup (Optional)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the Flask server:
   ```bash
   python app.py
   ```

3. Visit `http://localhost:5000/` in your browser.

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Bootstrap
- **Backend**: PHP 8.x & Python (Flask)
- **Database**: MySQL / MariaDB
