#!/usr/bin/env python3
"""
Core Migration Framework for Wagtail 2.14 to 6.4.2 Data Migration
Provides base classes and utilities for data migration operations
"""

import os
import sys
import logging
import logging.config
import psycopg2
import subprocess
from datetime import datetime
from contextlib import contextmanager
from typing import Dict, List, Optional, Any
import json

from migration_config import (
    PRODUCTION_DB_CONFIG, TARGET_DB_CONFIG, BACKUP_DB_CONFIG,
    LOGGING_CONFIG, ERROR_HANDLING, PERFORMANCE_SETTINGS,
    get_timestamp, ensure_directories
)

# Setup logging
ensure_directories()
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('migration')

class MigrationError(Exception):
    """Custom exception for migration errors"""
    pass

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, config: Dict[str, str]):
        self.config = config
        self.connection = None
        
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        try:
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
            self.connection.autocommit = False
            yield self.connection
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logger.error(f"Database connection error: {e}")
            raise MigrationError(f"Database connection failed: {e}")
        finally:
            if self.connection:
                self.connection.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[tuple]:
        """Execute a query and return results"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
                return []
    
    def execute_script(self, script_path: str) -> bool:
        """Execute a SQL script file"""
        try:
            cmd = [
                'psql',
                '-h', self.config['host'],
                '-p', self.config['port'],
                '-U', self.config['user'],
                '-d', self.config['database'],
                '-f', script_path
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.config['password']
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            logger.info(f"Successfully executed script: {script_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Script execution failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            return False
    
    def create_database(self, db_name: str) -> bool:
        """Create a new database"""
        try:
            # Connect to postgres database to create new database
            temp_config = self.config.copy()
            temp_config['database'] = 'postgres'

            conn = psycopg2.connect(**temp_config)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.close()
            conn.close()

            logger.info(f"Created database: {db_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create database {db_name}: {e}")
            return False

    def drop_database(self, db_name: str) -> bool:
        """Drop a database"""
        try:
            temp_config = self.config.copy()
            temp_config['database'] = 'postgres'

            conn = psycopg2.connect(**temp_config)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.close()
            conn.close()

            logger.info(f"Dropped database: {db_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to drop database {db_name}: {e}")
            return False

class BackupManager:
    """Manages database backups and restoration"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.backup_dir = 'backups'
        ensure_directories()
    
    def create_backup(self, backup_name: str = None) -> str:
        """Create a database backup"""
        if not backup_name:
            backup_name = f"migration_backup_{get_timestamp()}.sql"
        
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            cmd = [
                'pg_dump',
                '-h', self.db_manager.config['host'],
                '-p', self.db_manager.config['port'],
                '-U', self.db_manager.config['user'],
                '-d', self.db_manager.config['database'],
                '-f', backup_path,
                '--verbose'
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_manager.config['password']
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup creation failed: {e}")
            raise MigrationError(f"Backup failed: {e}")
    
    def restore_backup(self, backup_path: str, target_db: str = None) -> bool:
        """Restore a database from backup"""
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        db_name = target_db or self.db_manager.config['database']
        
        try:
            cmd = [
                'psql',
                '-h', self.db_manager.config['host'],
                '-p', self.db_manager.config['port'],
                '-U', self.db_manager.config['user'],
                '-d', db_name,
                '-f', backup_path
            ]
            
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_manager.config['password']
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            logger.info(f"Restored backup to {db_name}: {backup_path}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup restoration failed: {e}")
            return False

class MigrationState:
    """Tracks migration state and progress"""
    
    def __init__(self, state_file: str = 'migration_state.json'):
        self.state_file = state_file
        self.state = self.load_state()
    
    def load_state(self) -> Dict[str, Any]:
        """Load migration state from file"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load state file: {e}")
        
        return {
            'started_at': None,
            'completed_tables': [],
            'failed_tables': [],
            'current_phase': 'not_started',
            'backup_created': False,
            'rollback_available': False
        }
    
    def save_state(self):
        """Save current state to file"""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Could not save state: {e}")
    
    def mark_table_completed(self, table_name: str):
        """Mark a table as successfully migrated"""
        if table_name not in self.state['completed_tables']:
            self.state['completed_tables'].append(table_name)
        self.save_state()
    
    def mark_table_failed(self, table_name: str, error: str):
        """Mark a table as failed migration"""
        self.state['failed_tables'].append({
            'table': table_name,
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        })
        self.save_state()
    
    def set_phase(self, phase: str):
        """Set current migration phase"""
        self.state['current_phase'] = phase
        if phase == 'started' and not self.state['started_at']:
            self.state['started_at'] = datetime.now().isoformat()
        self.save_state()

class MigrationValidator:
    """Validates migration results"""
    
    def __init__(self, source_db: DatabaseManager, target_db: DatabaseManager):
        self.source_db = source_db
        self.target_db = target_db
    
    def validate_table_counts(self, table_name: str) -> bool:
        """Validate that table row counts match"""
        try:
            source_count = self.source_db.execute_query(f"SELECT COUNT(*) FROM {table_name}")[0][0]
            target_count = self.target_db.execute_query(f"SELECT COUNT(*) FROM {table_name}")[0][0]
            
            if source_count == target_count:
                logger.info(f"✓ {table_name}: {source_count} rows migrated successfully")
                return True
            else:
                logger.error(f"✗ {table_name}: Count mismatch - Source: {source_count}, Target: {target_count}")
                return False
        except Exception as e:
            logger.error(f"Validation error for {table_name}: {e}")
            return False
    
    def validate_data_integrity(self, table_name: str, sample_size: int = 10) -> bool:
        """Validate data integrity by comparing sample records"""
        try:
            # Get sample records from both databases
            source_query = f"SELECT * FROM {table_name} ORDER BY id LIMIT {sample_size}"
            target_query = f"SELECT * FROM {table_name} ORDER BY id LIMIT {sample_size}"
            
            source_data = self.source_db.execute_query(source_query)
            target_data = self.target_db.execute_query(target_query)
            
            if len(source_data) == len(target_data):
                logger.info(f"✓ {table_name}: Sample data integrity check passed")
                return True
            else:
                logger.error(f"✗ {table_name}: Sample data mismatch")
                return False
        except Exception as e:
            logger.error(f"Data integrity check failed for {table_name}: {e}")
            return False

# Utility functions
def setup_migration_environment():
    """Setup the migration environment"""
    ensure_directories()
    logger.info("Migration environment setup complete")

def cleanup_migration_environment():
    """Cleanup temporary files and connections"""
    logger.info("Migration environment cleanup complete")
