# Database Setup

## Create the database

Run `schema.sql` against your MySQL server. It creates the `integrated_cybersecurity` database and all required tables.

Windows/MySQL client:

```powershell
mysql -u root -p < database/schema.sql
```

Linux/macOS:

```bash
mysql -u root -p < database/schema.sql
```

You can also open `schema.sql` in MySQL Workbench and execute it.

## Sample data

`sample_data.sql` is optional. It is intended for demonstrations only and assumes that a compatible user record already exists. Do not use sample data as production credentials.
