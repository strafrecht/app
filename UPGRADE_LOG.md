# Wagtail/Django Upgrade Log

## Project Overview
- **Project**: Strafrecht Online (Legacy Wagtail Application)
- **Current State**: Wagtail 2.13, Django 3.2.5
- **Target State**: Latest stable Wagtail/Django versions
- **Upgrade Start Date**: 2025-07-27
- **Upgrade Strategy**: Systematic incremental upgrades

## Current Environment Baseline (2025-07-27)

### Versions Confirmed
- **Wagtail**: 2.13 (NOT 4.0+ as initially documented)
- **Django**: 3.2.5
- **Python**: 3.9.2
- **Node.js**: v22.17.1 (incompatible with frontend - needs v16)
- **PostgreSQL**: 13.x
- **Redis**: Available

### Database State
- **Tables**: 138 tables restored from backup
- **Backup File**: `/root/backup.sql` (working backup confirmed)
- **Connection**: ✅ Working (localhost:5434, user: django, db: strafrecht)

### Application State
- **Django Server**: ✅ Running on http://localhost:8000
- **Admin Interface**: ✅ Accessible at /admin/
- **System Check**: ✅ Passes with minor warnings
- **Frontend Build**: ❌ Node.js compatibility issues

### Critical Dependencies Analysis
```
Core Framework:
- wagtail==2.13
- Django==3.2.5
- djangorestframework==3.12.4

Wagtail Extensions:
- wagtail-birdsong==0.2.0 (newsletter system)
- wagtailmenus==3.0.2 (navigation)
- wagtailnews==2.7.1 (news system)
- wagtail-autocomplete==0.6.3
- wagtail-color-panel==1.2.0
- wagtail-markdown==0.7.0
- wagtail-modelchooser==2.13.1
- wagtailfontawesome==1.2.1
- wagtailstreamforms==3.15
- wagtail-treemodeladmin==1.5.0

Django Extensions:
- django-wiki==0.7.10 (wiki functionality)
- channels==3.0.3 (WebSocket)
- django-admin-interface==0.16.3
- django-comments-xtd==2.9.1
- django-cors-headers==3.7.0
- django-crispy-forms==1.14.0
- django-debug-toolbar==3.2.1

Database & Storage:
- psycopg2-binary==2.8.6
- redis via aioredis==1.3.1
- channels-redis==3.2.0
```

## Planned Upgrade Path

### Phase 1: Wagtail 2.x Series (Current)
- [x] **Baseline Established**: Wagtail 2.13, Django 3.2.5
- [ ] **2.13 → 2.14**: First incremental upgrade
- [ ] **2.14 → 2.15**: Final 2.x series upgrade

### Phase 2: Major Version Jump
- [ ] **2.15 → 3.0**: Major version upgrade with breaking changes
- [ ] **Django 3.2 → 4.0**: Align Django with Wagtail 3.x requirements

### Phase 3: Wagtail 3.x Series
- [ ] **3.0 → 3.0.1**: Patch updates
- [ ] **3.0.1 → 3.0.2**: Patch updates
- [ ] **3.0.2 → 3.0.3**: Final 3.0.x series

### Phase 4: Wagtail 4.x Series
- [ ] **3.0.3 → 4.0**: Major version upgrade
- [ ] **4.0 → 4.1**: Minor version upgrade
- [ ] **4.1 → 4.2**: Minor version upgrade
- [ ] **Django 4.0 → 4.1**: Align Django versions
- [ ] **Django 4.1 → 4.2**: Align Django versions

### Phase 5: Wagtail 5.x Series
- [ ] **4.2 → 5.0**: Major version upgrade
- [ ] **5.0 → 5.1**: Minor version upgrade
- [ ] **5.1 → 5.2**: Minor version upgrade
- [ ] **Django 4.2 → 5.0**: Major Django upgrade

### Phase 6: Latest Versions
- [ ] **5.2 → 6.0**: Major version upgrade
- [ ] **6.0 → Latest**: Current stable version

## Pre-Upgrade Checklist

### Documentation Created
- [x] UPGRADE_LOG.md (this file)
- [ ] COMPATIBILITY_MATRIX.md
- [ ] MIGRATION_LOG.md
- [ ] CUSTOM_CHANGES.md
- [ ] ROLLBACK_PROCEDURES.md
- [ ] TESTING_CHECKLIST.md

### Backup Strategy
- [x] Database backup confirmed: `/root/backup.sql`
- [ ] Create fresh pre-upgrade backup
- [ ] Media files backup
- [ ] Static assets backup
- [ ] Git branch created for upgrade work

### Environment Preparation
- [x] Python dependencies installed and working
- [x] Database connection verified
- [x] Application baseline functionality confirmed
- [ ] Frontend compatibility analysis
- [ ] Dependency compatibility matrix completed

## Upgrade Log Entries

### 2025-07-27: Baseline Establishment
**Status**: ✅ COMPLETED
**Actions Taken**:
- Discovered actual Wagtail version is 2.13 (not 4.0+ as documented)
- Restored database from backup (138 tables)
- Confirmed Django application functionality
- Identified frontend Node.js compatibility issues
- Created comprehensive baseline documentation

**Issues Discovered**:
- Setup documentation inaccurate about Wagtail version
- Frontend requires Node.js v16, current system has v22
- Some pending migrations in various apps

**Next Steps**:
- Create complete documentation structure
- Analyze dependency compatibility
- Begin Wagtail 2.13 → 2.14 upgrade

---

## Notes and Observations

### Critical Dependencies to Monitor
1. **wagtail-birdsong**: Newsletter system - check compatibility with each Wagtail version
2. **django-wiki**: Wiki functionality - may need forking for newer Django versions
3. **wagtailmenus**: Navigation system - critical for site functionality
4. **channels**: WebSocket functionality - ensure compatibility with Django upgrades

### Known Risks
1. **Major Version Jumps**: 2.x → 3.0 and 4.x → 5.0 likely have breaking changes
2. **Frontend Dependencies**: Node.js version conflicts may require environment changes
3. **Custom Wagtail Extensions**: May not be compatible with newer versions
4. **Database Migrations**: Complex schema may have migration issues

### Success Criteria for Each Upgrade
- All existing tests pass
- No new deprecation warnings
- Admin interface fully functional
- Newsletter system operational
- Wiki functionality intact
- Frontend builds successfully (when addressed)
- Performance maintained or improved

---

*This log will be updated with each upgrade step, including detailed notes on issues encountered, solutions implemented, and validation results.*
