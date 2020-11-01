#!/usr/bin/env bash

set -e

[ ! -z "$1" ] && DATABASE="$1" || (echo "database filename must be specified"; exit 1 )

rm -f "${DATABASE}"
rm -f "*dump.gz"

sqlite3 "${DATABASE}" <<'END_SQL'
CREATE TABLE IF NOT EXISTS employees
  (
      [EmployeeId] INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
      [LastName] NVARCHAR(20)  NOT NULL,
      [FirstName] NVARCHAR(20)  NOT NULL,
      [Title] NVARCHAR(30),
      [BirthDate] DATETIME,
      [HireDate] DATETIME,
      [Address] NVARCHAR(70),
      [City] NVARCHAR(40),
      [State] NVARCHAR(40),
      [Country] NVARCHAR(40),
      [PostalCode] NVARCHAR(10),
      [Phone] NVARCHAR(24),
      [Fax] NVARCHAR(24),
      [Email] NVARCHAR(60)
  );
END_SQL

echo "Database \"${DATABASE}\" was created successfully!"