#!/bin/bash
# Cleanup script for migration test

export PGPASSWORD="postgres"

echo "Cleaning up migration test environment..."

# Restore original migration config
if [ -f migration_config_backup.py ]; then
    mv migration_config_backup.py migration_config.py
    echo "✓ Migration configuration restored"
fi

# Drop test database
psql -h "localhost" -p "5434" -U "django" -d postgres -c "DROP DATABASE IF EXISTS strafrecht_migration_test;"
echo "✓ Test database 'strafrecht_migration_test' dropped"

# Remove migration state files
rm -f migration_state.json
rm -f migration_test_report_*.md

echo "✓ Migration test cleanup complete"
