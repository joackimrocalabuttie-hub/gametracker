#!/bin/bash
set -e
echo "=== LANCEMENT PIPELINE ==="
./scripts/wait-for-db.sh
echo "[SQL] Initialisation..."
mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < scripts/init-db.sql
echo "[PYTHON] Exécution ETL..."
python src/main.py
echo "=== TERMINÉ (Voir output/rapport.txt) ==="