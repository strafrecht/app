# Rollback Procedures

## Overview
This document provides step-by-step procedures for rolling back from any point in the Wagtail/Django upgrade process. Each rollback procedure is designed to restore the system to a known working state with minimal data loss.

## Emergency Contact Information
- **System Administrator**: [To be filled]
- **Database Administrator**: [To be filled]
- **Emergency Escalation**: [To be filled]

## Rollback Triggers

### Immediate Rollback Required
- **Database corruption or data loss**
- **Application completely non-functional**
- **Security vulnerabilities introduced**
- **Critical functionality broken (newsletter, wiki, admin)**
- **Performance degradation > 50%**

### Planned Rollback Scenarios
- **Test failures after upgrade**
- **Compatibility issues discovered**
- **User acceptance testing failures**
- **Performance degradation 20-50%**
- **Non-critical functionality broken**

## Pre-Rollback Checklist

### Before Any Rollback
1. **Document the Issue**:
   - Record exact error messages
   - Note what functionality is broken
   - Capture screenshots/logs
   - Document steps that led to the issue

2. **Assess Impact**:
   - Determine if issue is critical or can be fixed
   - Evaluate data loss risk
   - Consider user impact
   - Estimate fix time vs rollback time

3. **Notify Stakeholders**:
   - Inform users of potential downtime
   - Alert development team
   - Document rollback decision

## Rollback Procedures by Upgrade Phase

### Phase 1: Wagtail 2.13 → 2.14 Rollback

#### Quick Rollback (< 30 minutes)
```bash
# 1. Stop the application
pkill -f "python manage.py runserver"

# 2. Switch to backup branch
git checkout wagtail-2.13-baseline

# 3. Restore virtual environment
pip install -r requirements/common.txt

# 4. Restore database (if migrations were applied)
dropdb -h localhost -p 5434 -U django strafrecht
createdb -h localhost -p 5434 -U django strafrecht
psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/pre_wagtail_2_14.sql

# 5. Restart application
python manage.py runserver 0.0.0.0:8000
```

#### Verification Steps
- [ ] Application starts without errors
- [ ] Admin interface accessible
- [ ] Newsletter system functional
- [ ] Wiki system functional
- [ ] No data loss confirmed

### Phase 2: Wagtail 2.15 → 3.0 Rollback (HIGH RISK)

#### Emergency Rollback Procedure
```bash
# 1. IMMEDIATE STOP
pkill -f "python manage.py runserver"
pkill -f "daphne"

# 2. Restore code to last known good state
git checkout wagtail-2.15-stable

# 3. Restore Python environment
pip install -r requirements/common.txt --force-reinstall

# 4. Database restoration (CRITICAL)
# Create backup of current state first (for analysis)
pg_dump -h localhost -p 5434 -U django strafrecht > /root/backups/failed_wagtail_3_0_$(date +%Y%m%d_%H%M%S).sql

# Restore from pre-upgrade backup
dropdb -h localhost -p 5434 -U django strafrecht
createdb -h localhost -p 5434 -U django strafrecht
psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/pre_wagtail_3_0.sql

# 5. Verify migrations are correct
python manage.py showmigrations

# 6. Restart services
python manage.py runserver 0.0.0.0:8000
```

#### Extended Verification
- [ ] All 138 tables present
- [ ] User accounts functional
- [ ] Content accessible
- [ ] Admin interface fully functional
- [ ] Newsletter campaigns intact
- [ ] Wiki articles accessible
- [ ] File uploads working
- [ ] Search functionality operational

### Phase 3: Django 3.2 → 4.0 Rollback

#### Critical Django Rollback
```bash
# 1. Stop all Django processes
pkill -f "python manage.py"
pkill -f "daphne"
pkill -f "channels"

# 2. Code rollback
git checkout django-3.2-stable

# 3. Environment restoration
pip install -r requirements/common.txt --force-reinstall

# 4. Database rollback (Django migrations are complex)
# Restore from pre-Django-4.0 backup
dropdb -h localhost -p 5434 -U django strafrecht
createdb -h localhost -p 5434 -U django strafrecht
psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/pre_django_4_0.sql

# 5. Configuration restoration
cp app/settings/development.py.backup app/settings/development.py
cp app/urls.py.backup app/urls.py

# 6. Restart with Django 3.2
python manage.py runserver 0.0.0.0:8000
```

### Phase 4: Custom Code Rollback

#### Forked Dependencies Rollback
```bash
# 1. Remove forked packages
pip uninstall wagtail-birdsong-custom
pip uninstall django-wiki-custom

# 2. Reinstall original packages
pip install wagtail-birdsong==0.2.0
pip install django-wiki==0.7.10

# 3. Restore original code
git checkout custom-changes-baseline

# 4. Database schema rollback
python manage.py migrate [app] [migration_number]

# 5. Test functionality
python manage.py test
```

## Data Recovery Procedures

### Database Recovery Levels

#### Level 1: Configuration Rollback Only
- No database changes required
- Code and package rollback sufficient
- Fastest recovery (< 15 minutes)

#### Level 2: Migration Rollback
- Reverse specific migrations
- Preserve most data
- Medium recovery time (15-60 minutes)

```bash
# Reverse specific migrations
python manage.py migrate wagtailcore 0001 --fake
python manage.py migrate [app] [previous_migration]
```

#### Level 3: Full Database Restore
- Complete database replacement
- Potential data loss since backup
- Longest recovery time (30-120 minutes)

```bash
# Full restoration procedure
dropdb -h localhost -p 5434 -U django strafrecht
createdb -h localhost -p 5434 -U django strafrecht
psql -h localhost -p 5434 -U django -d strafrecht < /root/backups/[backup_file].sql
```

### Data Loss Mitigation

#### Before Rollback
1. **Create Current State Backup**:
   ```bash
   pg_dump -h localhost -p 5434 -U django strafrecht > /root/backups/pre_rollback_$(date +%Y%m%d_%H%M%S).sql
   ```

2. **Export Critical Data**:
   ```bash
   # Export user-generated content
   python manage.py dumpdata wagtailcore.Page > pages_backup.json
   python manage.py dumpdata auth.User > users_backup.json
   ```

#### After Rollback
1. **Assess Data Loss**:
   - Compare record counts
   - Verify critical content exists
   - Check user accounts

2. **Selective Data Recovery**:
   ```bash
   # Import specific data if needed
   python manage.py loaddata pages_backup.json
   ```

## Rollback Validation Checklist

### Immediate Validation (< 5 minutes)
- [ ] Application starts without errors
- [ ] Database connection successful
- [ ] Admin login functional
- [ ] Homepage loads correctly

### Functional Validation (< 30 minutes)
- [ ] User authentication working
- [ ] Content creation/editing functional
- [ ] Newsletter system operational
- [ ] Wiki system accessible
- [ ] File upload/download working
- [ ] Search functionality operational

### Extended Validation (< 2 hours)
- [ ] All user workflows tested
- [ ] Performance benchmarking
- [ ] Data integrity verification
- [ ] Security settings validated
- [ ] Email functionality tested
- [ ] Frontend build successful

## Communication Procedures

### During Rollback
1. **Status Updates**:
   - Initial rollback notification
   - Progress updates every 15 minutes
   - Completion notification

2. **User Communication**:
   - Maintenance mode message
   - Expected downtime duration
   - Functionality restoration updates

### Post-Rollback
1. **Incident Report**:
   - Root cause analysis
   - Timeline of events
   - Lessons learned
   - Prevention measures

2. **Stakeholder Notification**:
   - System restoration confirmation
   - Any data loss impact
   - Next steps planning

## Rollback Testing

### Regular Rollback Drills
- **Frequency**: Before each major upgrade
- **Scope**: Full rollback procedure
- **Documentation**: Update procedures based on results
- **Training**: Ensure team familiarity

### Rollback Validation
```bash
# Test rollback procedure on copy
createdb -h localhost -p 5434 -U django strafrecht_rollback_test
# ... perform rollback test ...
dropdb -h localhost -p 5434 -U django strafrecht_rollback_test
```

## Emergency Contacts and Escalation

### Technical Escalation
1. **Level 1**: Development Team Lead
2. **Level 2**: System Administrator
3. **Level 3**: External Consultant

### Business Escalation
1. **Level 1**: Project Manager
2. **Level 2**: Department Head
3. **Level 3**: Executive Team

## Rollback Decision Matrix

| Issue Severity | Data Loss Risk | User Impact | Decision |
|---------------|----------------|-------------|----------|
| Critical | High | High | Immediate Rollback |
| Critical | Low | High | Immediate Rollback |
| Major | High | Medium | Planned Rollback |
| Major | Low | Medium | Attempt Fix First |
| Minor | Any | Low | Attempt Fix First |

## Post-Rollback Actions

### Immediate (< 24 hours)
- [ ] Root cause analysis
- [ ] Issue documentation
- [ ] Stakeholder communication
- [ ] System monitoring

### Short-term (< 1 week)
- [ ] Alternative upgrade strategy
- [ ] Additional testing procedures
- [ ] Team training updates
- [ ] Process improvements

### Long-term (< 1 month)
- [ ] Upgrade plan revision
- [ ] Infrastructure improvements
- [ ] Documentation updates
- [ ] Preventive measures implementation

---

## Rollback Log

### Template for Rollback Events

#### YYYY-MM-DD: [Rollback Event]
**Trigger**: [What caused the rollback]
**Severity**: [Critical/Major/Minor]
**Rollback Type**: [Emergency/Planned]
**Duration**: [Total downtime]

**Actions Taken**:
- [Step-by-step actions]

**Data Loss**:
- [Any data loss and impact]

**Lessons Learned**:
- [What was learned from this rollback]

**Prevention Measures**:
- [Steps to prevent similar issues]

---

*This document will be updated after each rollback event with lessons learned and procedure improvements.*
