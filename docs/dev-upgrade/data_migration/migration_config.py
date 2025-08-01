#!/usr/bin/env python3
"""
Migration Configuration for Wagtail 2.14 to 6.4.2 Data Migration
Contains database configurations, table mappings, and migration settings
"""

import os
from datetime import datetime

# Database Configurations
PRODUCTION_DB_CONFIG = {
    'host': 'localhost',
    'port': '5434',
    'user': 'django',
    'password': 'postgres',
    'database': 'strafrecht_production_temp'  # Temporary DB for production data
}

TARGET_DB_CONFIG = {
    'host': 'localhost',
    'port': '5434',
    'user': 'django',
    'password': 'postgres',
    'database': 'strafrecht_migration_test'  # Current upgraded database
}

BACKUP_DB_CONFIG = {
    'host': 'localhost',
    'port': '5434',
    'user': 'django',
    'password': 'postgres',
    'database': 'strafrecht_migration_backup'  # Backup before migration
}

# File Paths
PRODUCTION_BACKUP_FILE = '../backup.sql'
MIGRATION_LOG_DIR = 'logs'
BACKUP_DIR = 'backups'

# Migration Settings
MIGRATION_BATCH_SIZE = 1000
MAX_RETRY_ATTEMPTS = 3
VALIDATION_SAMPLE_SIZE = 100

# Table Migration Priority
# Order matters - dependencies must be migrated first
MIGRATION_ORDER = [
    # Core Django tables - content types must come first for foreign key dependencies
    'django_content_type',
    'auth_user',
    'auth_group',
    'auth_permission',
    'auth_user_groups',
    'auth_user_user_permissions',
    'django_site',

    # Wagtail core tables (dependency order) - revisions must come before pages
    'wagtailcore_locale',
    'wagtailcore_collection',
    'wagtailcore_site',
    'wagtailcore_revision',
    'wagtailcore_page',
    'wagtailcore_pagerevision',
    
    # User profiles and permissions
    'wagtailusers_userprofile',
    'wagtailcore_grouppagepermission',
    'wagtailcore_groupcollectionpermission',
    
    # Media and documents
    'wagtailimages_image',
    'wagtailimages_rendition',
    'wagtaildocs_document',
    
    # Content and forms
    'wagtailforms_formsubmission',
    'wagtailstreamforms_form',
    'wagtailstreamforms_formsubmission',
    
    # Navigation and menus
    'wagtailmenus_mainmenu',
    'wagtailmenus_mainmenuitem',
    'wagtailmenus_flatmenu',
    'wagtailmenus_flatmenuitem',
    
    # Newsletter system
    'birdsong_campaign',
    'birdsong_contact',
    'birdsong_receipt',
    
    # Custom application tables
    'pages_homepage',
    'pages_contentpage',
    'pages_eventpage',
    'pages_sessionpage',
    'quiz_quiz',
    'quiz_question',
    'quiz_answer',
    'casetraining_case',
    'flashcards_deck',
    'flashcards_card',
]

# Tables to exclude from migration (deprecated or problematic)
EXCLUDED_TABLES = [
    'wagtailsearch_editorspick',
    'wagtailsearch_query',
    'wagtailsearch_querydailyhits',
    'wagtaildocs_uploadeddocument',
    'wagtailimages_uploadedimage',
    'django_migrations',  # Will be handled separately
    'django_session',     # Temporary data
    'django_admin_log',   # Can be regenerated
]

# Schema mapping for tables with significant changes
SCHEMA_MAPPINGS = {
    'wagtailcore_page': {
        'required_defaults': {
            'translation_key': 'gen_random_uuid()',  # Use gen_random_uuid() instead of uuid_generate_v4()
            'locale_id': '1',  # Default locale
            'alias_of_id': 'NULL',
            'latest_revision_id': 'NULL',
            'live_revision_id': 'NULL',
            'first_published_at': 'NULL',
            'last_published_at': 'NULL',
            'draft_title': "''",
            'has_unpublished_changes': 'false',
            'show_in_menus_default': 'false',
            'search_description': "''",
            'seo_title': "''",
            'locked_at': 'NULL',
            'locked_by_id': 'NULL',
            'workflow_in_progress': 'false',
        }
    },
    'wagtailimages_image': {
        'required_defaults': {
            'collection_id': '1',  # Root collection
            'focal_point_x': 'NULL',
            'focal_point_y': 'NULL',
            'focal_point_width': 'NULL',
            'focal_point_height': 'NULL',
            'description': "''",  # Empty string for required description field
            'focal_point_y': 'NULL',
            'focal_point_width': 'NULL',
            'focal_point_height': 'NULL',
            'file_size': 'NULL',
            'file_hash': "''",
        }
    },
    'wagtailusers_userprofile': {
        'required_defaults': {
            'submitted_notifications': 'true',
            'approved_notifications': 'true',
            'rejected_notifications': 'true',
            'updated_comments_notifications': 'true',
            'preferred_language': "''",
            'current_time_zone': "''",
            'avatar': "''",
            'dismissibles': '{}',
            'theme': "'system'",  # Default theme
            'density': "'default'",  # Default density
            'guide_tour_status': "'{}'",  # Empty JSON object
        }
    }
}

# Validation rules for migrated data
VALIDATION_RULES = {
    'auth_user': {
        'count_check': True,
        'required_fields': ['username', 'email'],
        'unique_fields': ['username', 'email']
    },
    'wagtailcore_page': {
        'count_check': True,
        'required_fields': ['title', 'slug', 'content_type_id'],
        'hierarchy_check': True
    },
    'wagtailimages_image': {
        'count_check': True,
        'file_existence_check': True,
        'required_fields': ['title', 'file']
    },
    'wagtaildocs_document': {
        'count_check': True,
        'file_existence_check': True,
        'required_fields': ['title', 'file']
    }
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f'{MIGRATION_LOG_DIR}/migration_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            'formatter': 'detailed'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'migration': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Error handling configuration
ERROR_HANDLING = {
    'continue_on_non_critical_errors': True,
    'critical_tables': [
        'auth_user',
        'wagtailcore_page',
        'wagtailcore_site',
        'wagtailimages_image'
    ],
    'max_errors_per_table': 10,
    'rollback_on_critical_failure': True
}

# Performance settings
PERFORMANCE_SETTINGS = {
    'use_bulk_insert': True,
    'disable_foreign_key_checks': True,
    'use_transactions': True,
    'commit_frequency': 1000,
    'parallel_processing': False  # Set to True for large datasets
}

def get_timestamp():
    """Get current timestamp for logging and backups"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_directories():
    """Ensure required directories exist"""
    os.makedirs(MIGRATION_LOG_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)

def get_migration_tables():
    """Get list of tables to migrate in correct order"""
    return [table for table in MIGRATION_ORDER if table not in EXCLUDED_TABLES]
