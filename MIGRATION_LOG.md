# Database Migration Log

## Overview
This log tracks all database migrations during the Wagtail/Django upgrade process, including backup procedures, migration testing, and rollback information.

## Database Information
- **Database**: PostgreSQL 13.x
- **Host**: localhost:5434
- **Database Name**: strafrecht
- **User**: django
- **Current Tables**: 138 tables (confirmed working)

## Backup Strategy

### Pre-Upgrade Backup Locations
- **Original Backup**: `/root/backup.sql` (baseline - working state)
- **Pre-Upgrade Backups**: `/root/backups/upgrade_YYYYMMDD_HHMMSS.sql`

### Backup Commands
```bash
# Create timestamped backup
pg_dump -h localhost -p 5434 -U django strafrecht > /root/backups/upgrade_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup
psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/backup_file.sql
```

## Current Migration Status (Baseline)

### Django Apps Migration Status
```bash
# Run: python manage.py showmigrations
```

**Status as of 2025-07-27**:
- ✅ **admin**: All migrations applied
- ✅ **auth**: All migrations applied  
- ✅ **contenttypes**: All migrations applied
- ✅ **sessions**: All migrations applied
- ⚠️ **Some apps**: Pending migrations detected during baseline

### Wagtail Apps Migration Status
- ✅ **wagtailcore**: Compatible with Wagtail 2.13
- ✅ **wagtailimages**: Compatible with Wagtail 2.13
- ✅ **wagtaildocs**: Compatible with Wagtail 2.13
- ✅ **wagtailadmin**: Compatible with Wagtail 2.13
- ✅ **wagtailsearch**: Compatible with Wagtail 2.13

## Migration Plan by Upgrade Phase

### Phase 1: Wagtail 2.13 → 2.14
**Expected Changes**:
- Minor Wagtail core migrations
- No Django migrations required
- Wagtail extension compatibility checks

**Pre-Migration Checklist**:
- [ ] Create backup: `upgrade_wagtail_2_14_pre.sql`
- [ ] Test migrations on database copy
- [ ] Review migration SQL with `sqlmigrate`
- [ ] Prepare rollback procedure

**Migration Commands**:
```bash
# Dry run first
python manage.py migrate --dry-run

# Apply migrations
python manage.py migrate

# Verify migration status
python manage.py showmigrations
```

### Phase 2: Wagtail 2.14 → 2.15
**Expected Changes**:
- Final 2.x series migrations
- Preparation for 3.0 compatibility
- Extension compatibility validation

### Phase 3: Wagtail 2.15 → 3.0 (HIGH RISK)
**Expected Changes**:
- **MAJOR VERSION MIGRATIONS**
- StreamField schema changes
- Image/document model updates
- Search backend modifications
- Admin interface database changes

**Special Precautions**:
- Multiple backup points during migration
- Test on complete database copy first
- Prepare detailed rollback procedure
- Extended testing period before proceeding

### Phase 4: Django 3.2 → 4.0 (HIGH RISK)
**Expected Changes**:
- **MAJOR DJANGO MIGRATIONS**
- Auth system updates
- Content types modifications
- Session handling changes
- Admin interface database updates

**Critical Considerations**:
- Django 4.0 has significant migration changes
- Some third-party apps may have migration conflicts
- Custom migrations may need updates

### Phase 5: Subsequent Upgrades
- Incremental migrations for each version
- Continuous validation and testing
- Performance impact monitoring

## Migration Testing Procedure

### Pre-Migration Testing
1. **Create Test Database Copy**:
   ```bash
   createdb -h localhost -p 5434 -U django strafrecht_test
   psql -h localhost -p 5434 -U django -d strafrecht_test < /root/backup.sql
   ```

2. **Test Migrations on Copy**:
   ```bash
   # Update settings to use test database
   python manage.py migrate --database=test
   ```

3. **Validate Test Results**:
   - Check migration completion
   - Verify data integrity
   - Test application functionality
   - Performance benchmarking

### Post-Migration Validation
1. **Data Integrity Checks**:
   - Row counts match expectations
   - Foreign key constraints intact
   - Index performance maintained
   - No orphaned records

2. **Application Functionality**:
   - Admin interface accessible
   - Content creation/editing works
   - Search functionality operational
   - User authentication working

3. **Performance Validation**:
   - Query performance maintained
   - Page load times acceptable
   - Database connection pooling working

## Rollback Procedures

### Immediate Rollback (Migration Failure)
1. **Stop Application**:
   ```bash
   # Stop Django development server
   pkill -f "python manage.py runserver"
   ```

2. **Restore Database**:
   ```bash
   # Drop current database
   dropdb -h localhost -p 5434 -U django strafrecht
   
   # Recreate database
   createdb -h localhost -p 5434 -U django strafrecht
   
   # Restore from backup
   psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/[backup_file].sql
   ```

3. **Revert Code Changes**:
   ```bash
   git checkout [previous_working_commit]
   ```

### Planned Rollback (Post-Migration Issues)
1. **Document Issues**: Record specific problems in this log
2. **Analyze Root Cause**: Determine if fixable or requires rollback
3. **Execute Rollback**: Follow immediate rollback procedure
4. **Plan Alternative Approach**: Modify upgrade strategy

## Migration Log Entries

### 2025-07-27: Baseline Migration Status
**Status**: ✅ DOCUMENTED
**Actions Taken**:
- Confirmed 138 tables in working database
- Verified Django/Wagtail migrations are current for version 2.13
- Identified some pending migrations in baseline
- Established backup and testing procedures

**Database State**:
- All core Django apps: Migrations current
- All core Wagtail apps: Migrations current
- Third-party apps: Some pending migrations detected
- Custom apps: Status to be verified

**Next Steps**:
- Create fresh pre-upgrade backup
- Resolve any pending migrations in baseline
- Test migration procedures on database copy

---

### Template for Future Entries

### YYYY-MM-DD: [Upgrade Phase] Migration
**Status**: [PLANNED/IN_PROGRESS/COMPLETED/FAILED/ROLLED_BACK]
**Wagtail Version**: [From] → [To]
**Django Version**: [From] → [To]

**Pre-Migration State**:
- Backup Created: [filename]
- Migration Count: [number]
- Database Size: [size]

**Migration Process**:
- Start Time: [timestamp]
- End Time: [timestamp]
- Duration: [time]
- Migrations Applied: [count]

**Issues Encountered**:
- [List any issues]

**Resolution**:
- [How issues were resolved]

**Post-Migration Validation**:
- [ ] Data integrity verified
- [ ] Application functionality tested
- [ ] Performance benchmarked
- [ ] No deprecation warnings

**Rollback Information**:
- Rollback Required: [Yes/No]
- Rollback Reason: [If applicable]
- Rollback Procedure Used: [If applicable]

---

## Migration Performance Tracking

| Phase | Duration | Migrations Applied | Issues | Rollback Required |
|-------|----------|-------------------|---------|-------------------|
| Baseline | N/A | Current | Pending migrations | No |
| 2.13→2.14 | TBD | TBD | TBD | TBD |
| 2.14→2.15 | TBD | TBD | TBD | TBD |
| 2.15→3.0 | TBD | TBD | TBD | TBD |
| Django 3.2→4.0 | TBD | TBD | TBD | TBD |

## Critical Migration Checkpoints

### Before Each Major Upgrade
- [ ] Fresh database backup created
- [ ] Migration tested on database copy
- [ ] Rollback procedure verified
- [ ] Application functionality baseline established

### After Each Migration
- [ ] Migration completion verified
- [ ] Data integrity validated
- [ ] Application functionality tested
- [ ] Performance impact assessed
- [ ] Documentation updated

---

*This log will be updated with detailed information for each migration performed during the upgrade process.*
