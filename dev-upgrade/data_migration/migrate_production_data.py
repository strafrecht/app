#!/usr/bin/env python3
"""
Main Migration Script for Wagtail 2.14 to 6.4.2 Data Migration
Orchestrates the complete migration process with error handling and rollback capabilities
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from migration_framework import (
    DatabaseManager, BackupManager, MigrationState, MigrationValidator,
    MigrationError, setup_migration_environment, cleanup_migration_environment
)
from migration_config import (
    PRODUCTION_DB_CONFIG, TARGET_DB_CONFIG, BACKUP_DB_CONFIG,
    PRODUCTION_BACKUP_FILE, get_migration_tables, SCHEMA_MAPPINGS,
    VALIDATION_RULES, ERROR_HANDLING
)

logger = logging.getLogger('migration')

class ProductionDataMigrator:
    """Main class for orchestrating production data migration"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.state = MigrationState()
        self.target_db = DatabaseManager(TARGET_DB_CONFIG)
        self.backup_manager = BackupManager(self.target_db)
        self.production_db = None
        self.validator = None
        self.content_type_mapping = {}

        logger.info(f"Initialized migrator (dry_run={dry_run})")
    
    def setup_production_database(self) -> bool:
        """Setup temporary database with production data"""
        logger.info("Setting up production database from backup...")
        
        try:
            # Create temporary database for production data
            temp_db_name = PRODUCTION_DB_CONFIG['database']
            
            # Drop existing temp database if it exists
            self.target_db.drop_database(temp_db_name)
            
            # Create new temp database
            if not self.target_db.create_database(temp_db_name):
                raise MigrationError("Failed to create temporary production database")
            
            # Initialize production database manager
            self.production_db = DatabaseManager(PRODUCTION_DB_CONFIG)
            
            # Restore production backup to temp database
            if not self.backup_manager.restore_backup(PRODUCTION_BACKUP_FILE, temp_db_name):
                raise MigrationError("Failed to restore production backup")
            
            # Initialize validator
            self.validator = MigrationValidator(self.production_db, self.target_db)
            
            logger.info("Production database setup complete")
            return True
            
        except Exception as e:
            logger.error(f"Production database setup failed: {e}")
            return False
    
    def create_migration_backup(self) -> bool:
        """Create backup of current target database before migration"""
        logger.info("Creating pre-migration backup...")

        try:
            # Check if target database exists first
            target_db_name = TARGET_DB_CONFIG['database']

            # Try to connect to see if database exists
            try:
                test_conn = self.target_db.get_connection()
                test_conn.close()
                database_exists = True
                logger.info(f"Target database {target_db_name} exists - creating backup")
            except:
                database_exists = False
                logger.info(f"Target database {target_db_name} doesn't exist yet - will skip backup")

            if database_exists:
                # Check if database has any tables (is it empty?)
                try:
                    tables = self.target_db.execute_query(
                        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
                    )
                    table_count = tables[0][0] if tables else 0

                    if table_count > 0:
                        backup_path = self.backup_manager.create_backup(f"pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")
                        self.state.state['backup_created'] = True
                        self.state.state['backup_path'] = backup_path
                        self.state.state['rollback_available'] = True
                        logger.info(f"Pre-migration backup created: {backup_path}")
                    else:
                        logger.info("Target database is empty - skipping backup")
                        self.state.state['backup_created'] = False
                        self.state.state['backup_path'] = None
                        self.state.state['rollback_available'] = False
                except Exception as e:
                    logger.warning(f"Could not check table count: {e} - proceeding without backup")
                    self.state.state['backup_created'] = False
                    self.state.state['backup_path'] = None
                    self.state.state['rollback_available'] = False
            else:
                # Database doesn't exist - this is fine, we'll create it during migration
                logger.info("Target database doesn't exist - will be created during migration")
                self.state.state['backup_created'] = False
                self.state.state['backup_path'] = None
                self.state.state['rollback_available'] = False

            self.state.save_state()

            return True

        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False

    def create_target_schema(self) -> bool:
        """Create Wagtail 6.4.2 schema in target database"""
        logger.info("Creating target database schema...")

        try:
            # Change to project directory and run Django migrations
            import subprocess
            import os

            project_dir = '/root/strafrecht-online'

            # Set environment variables for Django
            env = os.environ.copy()
            env['DJANGO_SETTINGS_MODULE'] = 'strafrecht.settings.dev'
            env['PGPASSWORD'] = 'postgres'

            # Run Django migrations to create the schema
            cmd = [
                'python3', 'manage.py', 'migrate',
                '--database', 'default',
                '--run-syncdb'
            ]

            result = subprocess.run(
                cmd,
                cwd=project_dir,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )

            logger.info("✓ Target database schema created successfully")
            if result.stdout:
                logger.debug(f"Migration output: {result.stdout}")

            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create target schema: {e}")
            if e.stderr:
                logger.error(f"Error output: {e.stderr}")
            if e.stdout:
                logger.error(f"Standard output: {e.stdout}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error creating target schema: {e}")
            return False

    def build_content_type_mapping(self) -> dict:
        """Build mapping of content type IDs from production to test database"""
        try:
            # Get content types from production database
            prod_content_types = self.production_db.execute_query(
                "SELECT id, app_label, model FROM django_content_type ORDER BY app_label, model"
            )
            prod_ct_dict = {(row[1], row[2]): row[0] for row in prod_content_types}

            # Get content types from test database
            test_content_types = self.target_db.execute_query(
                "SELECT id, app_label, model FROM django_content_type ORDER BY app_label, model"
            )
            test_ct_dict = {(row[1], row[2]): row[0] for row in test_content_types}

            # Build mapping
            content_type_mapping = {}
            for (app_label, model), prod_id in prod_ct_dict.items():
                if (app_label, model) in test_ct_dict:
                    test_id = test_ct_dict[(app_label, model)]
                    if prod_id != test_id:
                        content_type_mapping[prod_id] = test_id
                        logger.info(f"Content type mapping: {app_label}.{model} {prod_id} -> {test_id}")
                else:
                    logger.warning(f"Content type {app_label}.{model} (ID {prod_id}) not found in test database")

            self.content_type_mapping = content_type_mapping
            return content_type_mapping

        except Exception as e:
            logger.error(f"Failed to build content type mapping: {e}")
            return {}

    def migrate_table_data(self, table_name: str) -> bool:
        """Migrate data for a specific table"""
        logger.info(f"Migrating table: {table_name}")
        
        if self.dry_run:
            logger.info(f"DRY RUN: Would migrate {table_name}")
            return True
        
        try:
            # Check if table exists in production database
            prod_exists = self.production_db.execute_query(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
                (table_name,)
            )[0][0]
            
            if not prod_exists:
                logger.warning(f"Table {table_name} does not exist in production database")
                return True
            
            # Check if table exists in target database
            target_exists = self.target_db.execute_query(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
                (table_name,)
            )[0][0]
            
            if not target_exists:
                logger.warning(f"Table {table_name} does not exist in target database")
                return True
            
            # Get production data
            prod_data = self.production_db.execute_query(f"SELECT * FROM {table_name}")
            
            if not prod_data:
                logger.info(f"No data to migrate for {table_name}")
                return True
            
            # Clear existing data in target table (if any), but preserve default records for certain tables
            preserve_defaults_tables = [
                'wagtailcore_locale', 'wagtailcore_collection', 'wagtailcore_site', 'django_site',
                'auth_group', 'auth_permission', 'django_content_type', 'wagtailcore_page'
            ]

            if table_name in preserve_defaults_tables:
                # For these tables, only clear non-default records or use UPSERT logic
                if table_name in ['wagtailcore_locale', 'wagtailcore_collection', 'wagtailcore_site', 'django_site', 'wagtailcore_page']:
                    # Clear records with ID > 1
                    self.target_db.execute_query(f"DELETE FROM {table_name} WHERE id > 1")
                elif table_name == 'auth_user':
                    # For auth_user, clear all users except superuser (ID=1)
                    self.target_db.execute_query(f"DELETE FROM {table_name} WHERE id > 1")
                else:
                    # For auth and content type tables, we'll handle conflicts in insertion
                    pass
            else:
                # For other tables, clear all data
                self.target_db.execute_query(f"DELETE FROM {table_name}")
            
            # Filter out conflicting default records for certain tables
            skip_default_records_tables = [
                'wagtailcore_locale', 'wagtailcore_collection', 'wagtailcore_site', 'django_site', 'wagtailcore_page', 'auth_user'
            ]

            if table_name in skip_default_records_tables:
                # Skip records with ID 1 (default records) for these tables
                prod_data = [row for row in prod_data if row[0] != 1]

            # Prepare insert statement
            if table_name in SCHEMA_MAPPINGS:
                # Handle tables with schema changes
                success = self._migrate_table_with_schema_mapping(table_name, prod_data)
            else:
                # Direct migration for unchanged tables
                success = self._migrate_table_direct(table_name, prod_data)
            
            if success:
                self.state.mark_table_completed(table_name)
                logger.info(f"✓ Successfully migrated {table_name} ({len(prod_data)} rows)")
            else:
                self.state.mark_table_failed(table_name, "Migration failed")
                logger.error(f"✗ Failed to migrate {table_name}")
            
            return success
            
        except Exception as e:
            error_msg = f"Error migrating {table_name}: {e}"
            logger.error(error_msg)
            self.state.mark_table_failed(table_name, str(e))
            
            # Check if this is a critical table
            if table_name in ERROR_HANDLING['critical_tables']:
                raise MigrationError(f"Critical table migration failed: {table_name}")
            
            return False
    
    def _migrate_table_direct(self, table_name: str, data: list) -> bool:
        """Direct migration for tables without schema changes"""
        try:
            if not data:
                return True
            
            # Get column names
            columns = self.target_db.execute_query(
                "SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position",
                (table_name,)
            )
            column_names = [col[0] for col in columns]
            
            # Prepare insert statement with conflict handling for certain tables
            placeholders = ','.join(['%s'] * len(column_names))

            conflict_handling_tables = [
                'auth_group', 'auth_permission', 'django_content_type', 'auth_user',
                'auth_user_groups', 'wagtailcore_collection', 'wagtailcore_groupcollectionpermission'
            ]

            if table_name in conflict_handling_tables:
                # Use INSERT ... ON CONFLICT DO NOTHING for tables that might have conflicts
                insert_query = f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
            else:
                insert_query = f"INSERT INTO {table_name} ({','.join(column_names)}) VALUES ({placeholders})"

            # Insert data in batches
            with self.target_db.get_connection() as conn:
                with conn.cursor() as cursor:
                    for row in data:
                        # Ensure row has correct number of columns
                        if len(row) == len(column_names):
                            # Transform content type IDs if needed
                            transformed_row = list(row)
                            if 'content_type_id' in column_names and self.content_type_mapping:
                                content_type_idx = column_names.index('content_type_id')
                                old_ct_id = transformed_row[content_type_idx]
                                if old_ct_id in self.content_type_mapping:
                                    transformed_row[content_type_idx] = self.content_type_mapping[old_ct_id]
                                    logger.debug(f"Transformed content_type_id {old_ct_id} -> {self.content_type_mapping[old_ct_id]} for {table_name}")

                            cursor.execute(insert_query, transformed_row)
                        else:
                            logger.warning(f"Row length mismatch for {table_name}: expected {len(column_names)}, got {len(row)}")
                    conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Direct migration failed for {table_name}: {e}")
            return False
    
    def _migrate_table_with_schema_mapping(self, table_name: str, data: list) -> bool:
        """Migration for tables with schema changes"""
        try:
            if not data:
                return True
            
            mapping = SCHEMA_MAPPINGS[table_name]
            
            # Get current target schema
            target_columns = self.target_db.execute_query(
                "SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position",
                (table_name,)
            )
            target_column_names = [col[0] for col in target_columns]
            
            # Get production schema
            prod_columns = self.production_db.execute_query(
                "SELECT column_name FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position",
                (table_name,)
            )
            prod_column_names = [col[0] for col in prod_columns]
            
            # Map data with defaults for new columns
            with self.target_db.get_connection() as conn:
                with conn.cursor() as cursor:
                    for row in data:
                        # Create row dict from production data
                        row_dict = dict(zip(prod_column_names, row))
                        
                        # Build target row with defaults for missing columns
                        target_values = []
                        value_placeholders = []
                        for col_name in target_column_names:
                            # Check if we have a forced default for this column
                            if col_name in mapping.get('required_defaults', {}):
                                default_value = mapping['required_defaults'][col_name]
                                if default_value == 'NULL':
                                    target_values.append(None)
                                    value_placeholders.append('%s')
                                elif default_value.startswith("'") and default_value.endswith("'"):
                                    target_values.append(default_value[1:-1])
                                    value_placeholders.append('%s')
                                elif default_value.endswith('()'):  # SQL function call
                                    value_placeholders.append(default_value)
                                    # Don't add to target_values as it's a SQL function
                                else:
                                    target_values.append(default_value)
                                    value_placeholders.append('%s')
                            elif col_name in row_dict:
                                target_values.append(row_dict[col_name])
                                value_placeholders.append('%s')
                            else:
                                target_values.append(None)
                                value_placeholders.append('%s')

                        # Insert row
                        insert_query = f"INSERT INTO {table_name} ({','.join(target_column_names)}) VALUES ({','.join(value_placeholders)})"
                        cursor.execute(insert_query, target_values)
                    
                    conn.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Schema mapping migration failed for {table_name}: {e}")
            return False
    
    def validate_migration(self) -> bool:
        """Validate the migration results"""
        logger.info("Validating migration results...")
        
        validation_passed = True
        tables_to_validate = [table for table in get_migration_tables() if table in VALIDATION_RULES]
        
        for table_name in tables_to_validate:
            try:
                rules = VALIDATION_RULES[table_name]
                
                if rules.get('count_check', False):
                    if not self.validator.validate_table_counts(table_name):
                        validation_passed = False
                
                if rules.get('data_integrity_check', False):
                    if not self.validator.validate_data_integrity(table_name):
                        validation_passed = False
                        
            except Exception as e:
                logger.error(f"Validation error for {table_name}: {e}")
                validation_passed = False
        
        if validation_passed:
            logger.info("✓ Migration validation passed")
        else:
            logger.error("✗ Migration validation failed")
        
        return validation_passed
    
    def rollback_migration(self) -> bool:
        """Rollback migration using pre-migration backup"""
        logger.info("Rolling back migration...")
        
        if not self.state.state.get('rollback_available', False):
            logger.error("No rollback backup available")
            return False
        
        backup_path = self.state.state.get('backup_path')
        if not backup_path or not os.path.exists(backup_path):
            logger.error("Rollback backup file not found")
            return False
        
        try:
            # Restore from backup
            if self.backup_manager.restore_backup(backup_path):
                logger.info("✓ Migration rollback completed successfully")
                self.state.set_phase('rolled_back')
                return True
            else:
                logger.error("✗ Migration rollback failed")
                return False
                
        except Exception as e:
            logger.error(f"Rollback error: {e}")
            return False
    
    def run_migration(self) -> bool:
        """Run the complete migration process"""
        logger.info("Starting production data migration...")
        
        try:
            self.state.set_phase('started')
            
            # Setup environment
            setup_migration_environment()
            
            # Create backup
            if not self.create_migration_backup():
                raise MigrationError("Failed to create pre-migration backup")
            
            # Setup production database
            if not self.setup_production_database():
                raise MigrationError("Failed to setup production database")

            # Create target database if it doesn't exist
            target_db_name = TARGET_DB_CONFIG['database']
            try:
                # Try to connect to target database
                test_conn = self.target_db.get_connection()
                test_conn.close()
                logger.info(f"Target database {target_db_name} already exists")
            except:
                # Database doesn't exist, create it
                logger.info(f"Creating target database: {target_db_name}")
                if not self.target_db.create_database(target_db_name):
                    raise MigrationError(f"Failed to create target database {target_db_name}")
                logger.info(f"✓ Created target database: {target_db_name}")

            # Create Wagtail 6.4.2 schema in target database
            logger.info("Creating Wagtail 6.4.2 schema in target database...")
            if not self.create_target_schema():
                raise MigrationError("Failed to create target database schema")

            # Build content type mapping
            self.build_content_type_mapping()

            # Migrate tables
            self.state.set_phase('migrating_data')
            migration_tables = get_migration_tables()
            
            for table_name in migration_tables:
                if not self.migrate_table_data(table_name):
                    if table_name in ERROR_HANDLING['critical_tables']:
                        raise MigrationError(f"Critical table migration failed: {table_name}")
                    else:
                        logger.warning(f"Non-critical table migration failed: {table_name}")
            
            # Validate migration
            self.state.set_phase('validating')
            if not self.validate_migration():
                if ERROR_HANDLING.get('rollback_on_critical_failure', True):
                    logger.error("Validation failed, rolling back...")
                    self.rollback_migration()
                    return False
            
            # Complete migration
            self.state.set_phase('completed')
            logger.info("✓ Production data migration completed successfully")
            
            # Cleanup
            cleanup_migration_environment()
            
            return True
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self.state.set_phase('failed')
            
            if ERROR_HANDLING.get('rollback_on_critical_failure', True):
                logger.info("Attempting automatic rollback...")
                self.rollback_migration()
            
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Migrate production data from Wagtail 2.14 to 6.4.2')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without actual migration')
    parser.add_argument('--rollback', action='store_true', help='Rollback the last migration')
    parser.add_argument('--validate-only', action='store_true', help='Only run validation checks')
    
    args = parser.parse_args()
    
    migrator = ProductionDataMigrator(dry_run=args.dry_run)
    
    if args.rollback:
        success = migrator.rollback_migration()
    elif args.validate_only:
        if not migrator.setup_production_database():
            logger.error("Failed to setup production database for validation")
            sys.exit(1)
        success = migrator.validate_migration()
    else:
        success = migrator.run_migration()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
