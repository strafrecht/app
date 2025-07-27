---
type: "always_apply"
---

# Wagtail Legacy Application Upgrade Rules

## Project Context
This is a legacy Wagtail Django application requiring systematic upgrade from Wagtail 2.13/Django 3.2 to latest versions. The application includes:
- Custom Wagtail plugins and third-party dependencies
- Webpack-based frontend with Vue.js components  
- PostgreSQL database with complex schema
- Production deployment considerations

## Core Upgrade Principles

### 1. SYSTEMATIC VERSION PROGRESSION
- **NEVER** jump directly to latest versions
- Follow incremental upgrade path: Wagtail 2.13 -> 3.0 → 3.0.1  → 3.0.2 → 3.0.3 → 4.0 → 4.1 → 4.2 → 5.0 → 5.1 → 5.2 → 6.0 → latest
- Django upgrades must align: 3.2 → 4.0 → 4.1 → 4.2 → 5.0 → latest
- Test thoroughly at each intermediate version before proceeding

### 2. PRE-UPGRADE REQUIREMENTS
Before ANY version upgrade:
- Create full database backup: `pg_dump -h localhost -p 5434 -U django strafrecht > backup_$(date +%Y%m%d_%H%M%S).sql`
- Document current working state in UPGRADE_LOG.md
- Create git branch for the specific upgrade step: `upgrade-wagtail-X.Y`
- Run full test suite and document results
- Backup media files and static assets

### 3. DEPENDENCY COMPATIBILITY ANALYSIS
Before upgrading core packages:
- Check each dependency in requirements/common.txt for compatibility with target versions
- Use `pip-check-reqs` and `pipdeptree` to analyze dependency conflicts
- Research breaking changes in release notes for ALL dependencies
- Create compatibility matrix in COMPATIBILITY_MATRIX.md
- Identify dependencies that need forking or replacement

### 4. DATABASE MIGRATION SAFETY
- **ALWAYS** test migrations on database copy first
- Use `--dry-run` flag when available
- Create migration rollback scripts before applying
- Document schema changes in MIGRATION_LOG.md
- Never run migrations directly on production without staging validation
- Use `python manage.py sqlmigrate` to review SQL before applying
- Backup database you can find here: /root/backup.sql

### 5. FRONTEND COMPATIBILITY REQUIREMENTS
- Test webpack build after each backend upgrade
- Verify Vue.js component functionality
- Check for breaking changes in:
  - Django static file handling
  - Wagtail admin interface integration
  - API endpoints used by frontend
- Update frontend dependencies in coordination with backend changes
- Maintain separate frontend testing environment

## Specific Technical Guidelines

### Wagtail-Specific Upgrade Rules
- Check Wagtail release notes for breaking changes in:
  - StreamField API changes
  - Admin interface modifications  
  - Search backend changes
  - Image/document handling updates
- Update custom Wagtail hooks and panels
- Verify wagtail-birdsong newsletter functionality
- Test wagtailmenus and wagtailnews compatibility

### Django Upgrade Considerations
- Update URL patterns for Django 4.0+ (path() vs url())
- Check for deprecated settings and middleware
- Update ASGI configuration if needed
- Verify django-wiki compatibility with newer Django versions
- Test django-channels WebSocket functionality

### Third-Party Plugin Management
- For incompatible plugins, create forks in separate repositories
- Document all custom modifications in CUSTOM_CHANGES.md
- Maintain version pins for forked dependencies
- Consider alternative plugins if maintenance becomes unsustainable

### Code Quality and Testing
- Run `python manage.py check --deploy` after each upgrade
- Use `python manage.py test` for full test suite
- Add integration tests for critical user journeys
- Test admin interface functionality thoroughly
- Verify email newsletter system (birdsong) works correctly

## File and Documentation Requirements

### Required Documentation Files
- `UPGRADE_LOG.md` - Detailed log of each upgrade step
- `COMPATIBILITY_MATRIX.md` - Dependency compatibility analysis
- `MIGRATION_LOG.md` - Database migration tracking
- `CUSTOM_CHANGES.md` - Documentation of all custom modifications
- `ROLLBACK_PROCEDURES.md` - Step-by-step rollback instructions
- `TESTING_CHECKLIST.md` - Comprehensive testing procedures

### Backup and Recovery
- Maintain at least 3 database backups before major upgrades
- Store backups with timestamps and version information
- Test backup restoration procedures
- Document exact restoration steps in ROLLBACK_PROCEDURES.md

### Version Control Strategy
- Create feature branch for each upgrade milestone
- Use descriptive commit messages with version information
- Tag successful upgrade milestones
- Never merge to main without full testing completion

## Error Handling and Rollback

### When Upgrades Fail
- Immediately stop upgrade process
- Document exact error and context in UPGRADE_LOG.md
- Restore from most recent backup
- Analyze root cause before attempting retry
- Consider alternative upgrade paths or dependency replacements

### Rollback Triggers
- Any test failures after upgrade
- Performance degradation > 20%
- Critical functionality broken
- Database migration errors
- Frontend build failures

## Success Criteria for Each Upgrade Step
- All existing tests pass
- No new deprecation warnings
- Frontend builds and functions correctly
- Admin interface fully functional
- Newsletter system operational
- Wiki functionality intact
- Performance maintained or improved
- No security vulnerabilities introduced

## Final Validation Requirements
- Full user acceptance testing
- Performance benchmarking
- Security audit
- Documentation completeness review
- Deployment procedure validation
- Monitoring and alerting setup

## Specific Upgrade Roadmap

### Phase 1: Current State Analysis (Wagtail 4.0, Django 3.2)
- Document all custom code and modifications
- Create comprehensive test coverage for existing functionality
- Identify all third-party dependencies and their versions
- Establish baseline performance metrics

### Phase 2: Django 4.0 Upgrade
- Upgrade Django 3.2 → 4.0
- Update URL patterns and deprecated features
- Test all functionality thoroughly
- Update requirements files

### Phase 3: Wagtail 4.1-4.2 Incremental Upgrades
- Upgrade Wagtail 4.0 → 4.1 → 4.2
- Update Wagtail plugins compatibility
- Test StreamField and admin interface changes
- Verify frontend integration

### Phase 4: Django 4.1-4.2 Alignment
- Upgrade Django to match Wagtail requirements
- Update ASGI configuration
- Test channels and WebSocket functionality

### Phase 5: Wagtail 5.x Series
- Systematic upgrade through Wagtail 5.x versions
- Major API changes handling
- Frontend compatibility verification
- Performance optimization

### Phase 6: Latest Version Migration
- Final upgrade to current stable versions
- Security hardening
- Performance optimization
- Documentation finalization

## Critical Dependencies to Monitor
- wagtail-birdsong (newsletter system)
- django-wiki (wiki functionality)
- wagtailmenus (navigation)
- wagtailnews (news system)
- django-channels (WebSocket)
- Vue.js frontend components

## Emergency Procedures
- Keep production system on stable version during upgrades
- Maintain parallel staging environment for testing
- Have immediate rollback capability ready
- Monitor system health continuously during upgrades

Remember: Patience and systematic approach prevent data loss and system downtime. Each upgrade step should be treated as a separate project with its own planning, execution, and validation phases.
