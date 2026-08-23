# Integrated Cybersecurity System

A transferable Flask + MySQL academic prototype implementing the documented objectives of a web-based integrated cybersecurity system for phishing detection, intrusion monitoring, and OTP-based multi-factor authentication.

## 1. Project scope

The application implements:

- Username/password registration and authentication
- Secure password hashing
- OTP-based MFA with on-screen OTP simulation for academic/demo use
- Rule-based heuristic phishing URL detection
- Application-level intrusion monitoring based on repeated failed logins
- Security alerts
- User dashboard
- Activity logs
- Phishing scan history
- Protected sessions and secure logout
- Responsive Bootstrap 5 interface

The implementation intentionally stays within the project paper's scope: phishing detection is rule-based and intrusion monitoring is limited to application-level login activity. It does not introduce machine-learning phishing detection or network packet analysis.

## 2. Transferability

This project is designed to be copied to another Windows or Linux computer without changing the source code.

Machine-specific values are kept in `.env`, which is intentionally **not** distributed. Use `.env.example` as the configuration template.

The following are not included in the project package because they are machine-specific or generated automatically:

- `.env`
- `venv/` or `.venv/`
- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`

The Python environment can always be recreated from `requirements.txt`, and the MySQL database can be recreated from `database/schema.sql`.

## 3. Requirements

Install the following on the destination computer:

- Python 3.11 or newer
- MySQL Server 8.x (or a compatible MySQL installation)
- A modern web browser
- Visual Studio Code (recommended development environment)

Internet access is only required to install Python packages from `requirements.txt` if they are not already cached locally.

## 4. Installation on Windows

### Step 1: Open the project

Extract the ZIP and open the `integrated_cybersecurity_system` folder in Visual Studio Code.

### Step 2: Create a virtual environment

Open the VS Code terminal and run:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure MySQL

Copy `.env.example` to `.env` and edit the values:

```env
SECRET_KEY=replace-with-a-long-random-secret
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=integrated_cybersecurity
FLASK_DEBUG=0
SESSION_LIFETIME=1800
SESSION_COOKIE_SECURE=0
```

Do not commit or share the real `.env` file.

### Step 5: Create the database

From the project directory, use MySQL Workbench or the MySQL client to run:

```sql
SOURCE database/schema.sql;
```

Alternatively, from a terminal with the MySQL client available:

```powershell
mysql -u root -p < database/schema.sql
```

### Step 6: Start the application

```powershell
python app.py
```

Open:

`http://127.0.0.1:5000/`

## 5. Installation on Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `.env` from `.env.example`, configure MySQL, then run:

```bash
mysql -u root -p < database/schema.sql
python app.py
```

Open `http://127.0.0.1:5000/` in a browser.

## 6. Database

The schema creates the database and these tables:

- `users`
- `otp_codes`
- `login_logs`
- `phishing_scans`
- `activity_logs`
- `security_alerts`

`database/sample_data.sql` is optional and should only be used for demonstrations where sample records are desired.

## 7. Demo workflow

1. Register a user.
2. Log in using the username and password.
3. The application generates an OTP and displays it on the OTP page because external email/SMS delivery is not configured.
4. Enter the displayed OTP.
5. Open the dashboard.
6. Scan a safe URL and a suspicious URL.
7. Attempt three incorrect logins to demonstrate the intrusion alert threshold.
8. Review Activity Logs and Security Alerts.
9. Log out and confirm that protected pages require authentication again.

## 8. Testing

Run the automated tests from the project root:

```bash
pytest
```

The automated tests currently focus on the rule-based phishing classifier. Full browser/integration testing requires a configured MySQL instance.

## 9. Moving the project to another computer

1. Copy/extract the project ZIP.
2. Install Python and MySQL on the new computer.
3. Create a new `.venv`.
4. Install `requirements.txt`.
5. Create a new `.env` using `.env.example`.
6. Run `database/schema.sql` against the new MySQL server.
7. Start `python app.py`.

No source-code path changes should be necessary.

## 10. Security notes

This is an academic prototype. Before production deployment, add HTTPS, production-grade CSRF handling, rate limiting, stronger account lockout controls, external OTP delivery, centralized secret management, audit retention policies, secure reverse-proxy deployment, and additional security monitoring.

Never place real passwords, API keys, or production secrets in source files or SQL scripts.

## If the server appears to stop after Register

The registration form writes to MySQL. If MySQL is stopped, the database does not exist, or the credentials in `.env` are incorrect, registration cannot be completed.

Check that:

1. MySQL Server is running.
2. `database/schema.sql` has been executed.
3. `.env` contains the correct `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
4. The terminal running `python app.py` shows no database error.

The application now catches database errors during registration and displays a user-friendly message instead of allowing the registration request to terminate unexpectedly.
