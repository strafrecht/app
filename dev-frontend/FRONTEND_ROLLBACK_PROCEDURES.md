# Frontend Rollback Procedures

## Overview
Emergency rollback procedures for frontend upgrades when critical issues are encountered during the upgrade process.

**Last Updated**: 2025-07-27  
**Emergency Contact**: Frontend Development Team  
**Escalation Path**: Backend Team → Infrastructure Team  
**Maximum Rollback Time**: 30 minutes for critical issues

## Rollback Triggers

### Immediate Rollback Required
- [ ] **Build Failures**: Frontend build process completely broken
- [ ] **Critical Functionality Lost**: Flashcards or case training components non-functional
- [ ] **Django Integration Broken**: Static file collection fails
- [ ] **Wagtail Admin Broken**: Vue components crash Wagtail admin interface
- [ ] **Security Vulnerabilities**: New security issues introduced
- [ ] **Performance Degradation**: >50% performance regression

### Rollback Consideration
- [ ] **Minor UI Issues**: Non-critical visual problems
- [ ] **Development Tool Issues**: Linting or development server problems
- [ ] **Non-Critical Features**: Secondary functionality affected
- [ ] **Performance Issues**: <20% performance regression

## Pre-Rollback Checklist

### 1. Issue Assessment (5 minutes)
- [ ] **Document Issue**: Record exact error messages and symptoms
- [ ] **Identify Scope**: Determine if issue affects development, staging, or production
- [ ] **Check Recent Changes**: Identify which upgrade step caused the issue
- [ ] **Assess Impact**: Evaluate user impact and business criticality
- [ ] **Notify Team**: Alert relevant team members of rollback decision

### 2. Backup Current State (5 minutes)
- [ ] **Git Status**: Check current git status and uncommitted changes
- [ ] **Package State**: Backup current package.json and package-lock.json
- [ ] **Build Artifacts**: Backup current build output if needed
- [ ] **Configuration Files**: Backup webpack and other config files
- [ ] **Database State**: Note any database changes (if applicable)

## Rollback Procedures by Phase

### Phase 1 Rollback: Foundation Issues

#### Node.js Version Rollback
```bash
# 1. Remove .nvmrc if it was added
rm -f frontend/.nvmrc

# 2. Switch to previous Node.js version
nvm use 16  # or whatever was previously used

# 3. Clear npm cache
npm cache clean --force

# 4. Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Security Updates Rollback
```bash
# 1. Revert to previous package.json
cd frontend
git checkout HEAD~1 -- package.json package-lock.json

# 2. Reinstall previous dependencies
rm -rf node_modules
npm install

# 3. Verify build works
npm run build
```

#### ESLint Rollback
```bash
# 1. Revert ESLint configuration
git checkout HEAD~1 -- frontend/.eslintrc.js frontend/package.json

# 2. Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# 3. Test linting
npm run lint:scripts
```

### Phase 2 Rollback: Build Tools Issues

#### Webpack Rollback
```bash
# 1. Revert webpack configuration and packages
cd frontend
git checkout HEAD~1 -- webpack/ package.json package-lock.json

# 2. Clear build cache
rm -rf node_modules build .cache

# 3. Reinstall and rebuild
npm install
npm run build
npm start  # Test dev server
```

#### CSS Processing Rollback
```bash
# 1. Revert Sass-related packages
git checkout HEAD~1 -- frontend/package.json frontend/package-lock.json

# 2. Reinstall Node Sass if needed
cd frontend
rm -rf node_modules
npm install

# 3. Test style compilation
npm run build
```

### Phase 3 Rollback: Framework Preparation Issues

#### Bootstrap Rollback
```bash
# 1. Revert Bootstrap and related packages
cd frontend
git checkout HEAD~1 -- package.json package-lock.json src/styles/

# 2. Reinstall dependencies
rm -rf node_modules
npm install

# 3. Rebuild and test
npm run build
```

#### Moment.js Rollback
```bash
# 1. Revert date library changes
git checkout HEAD~1 -- frontend/src/scripts/ frontend/package.json

# 2. Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# 3. Test date functionality
npm run build
```

### Phase 4 Rollback: Vue.js Migration Issues

#### Vue 3 Rollback (Critical)
```bash
# 1. Revert all Vue-related changes
cd frontend
git checkout HEAD~1 -- src/scripts/vue/ package.json package-lock.json

# 2. Clear all caches
rm -rf node_modules build .cache

# 3. Reinstall Vue 2 dependencies
npm install

# 4. Rebuild and test components
npm run build
npm start
```

#### Vuetify Rollback
```bash
# 1. Revert Vuetify and component changes
git checkout HEAD~1 -- frontend/src/scripts/vue/ frontend/package.json

# 2. Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install

# 3. Test UI components
npm run build
```

## Django Integration Rollback

### Static Files Rollback
```bash
# 1. Clear Django static files
cd /root/strafrecht-online
python manage.py collectstatic --clear --noinput

# 2. Rebuild frontend with previous version
cd frontend
npm run build

# 3. Recollect static files
cd ..
python manage.py collectstatic --noinput

# 4. Restart Django server
python manage.py runserver
```

### Wagtail Admin Integration Rollback
```bash
# 1. Revert Vue component integration
git checkout HEAD~1 -- frontend/src/scripts/index.js

# 2. Rebuild frontend
cd frontend
npm run build

# 3. Collect static files
cd ..
python manage.py collectstatic --noinput

# 4. Test Wagtail admin
python manage.py runserver
```

## Complete System Rollback

### Full Git Rollback
```bash
# 1. Identify last known good commit
git log --oneline -10

# 2. Create backup branch of current state
git checkout -b rollback-backup-$(date +%Y%m%d-%H%M%S)
git checkout main  # or your main branch

# 3. Hard reset to last known good commit
git reset --hard <LAST_GOOD_COMMIT_HASH>

# 4. Force push if needed (DANGEROUS - use with caution)
# git push --force-with-lease origin main
```

### Environment Restoration
```bash
# 1. Clear all caches and builds
cd frontend
rm -rf node_modules package-lock.json build .cache

# 2. Reinstall dependencies from git state
npm install

# 3. Rebuild frontend
npm run build

# 4. Django static file collection
cd ..
python manage.py collectstatic --noinput

# 5. Restart all services
python manage.py runserver
```

## Post-Rollback Verification

### 1. Build System Check (5 minutes)
- [ ] **Development Build**: `npm start` works without errors
- [ ] **Production Build**: `npm run build` completes successfully
- [ ] **Build Time**: Build times return to baseline
- [ ] **Asset Generation**: All assets generate correctly

### 2. Functionality Check (10 minutes)
- [ ] **Vue Components**: Flashcards and case training work
- [ ] **Django Integration**: Static files serve correctly
- [ ] **Wagtail Admin**: Admin interface functions properly
- [ ] **API Calls**: Frontend-backend communication works
- [ ] **User Interface**: All UI elements render correctly

### 3. Performance Check (5 minutes)
- [ ] **Page Load**: Page load times return to baseline
- [ ] **Bundle Size**: Bundle sizes return to previous state
- [ ] **Memory Usage**: No memory leaks detected
- [ ] **Hot Reload**: Development server performance restored

## Communication Procedures

### Internal Communication
1. **Immediate Notification**: Slack/Teams message to development team
2. **Issue Documentation**: Create detailed issue report in project management system
3. **Stakeholder Update**: Notify product owner and QA team
4. **Post-Mortem**: Schedule post-mortem meeting within 24 hours

### External Communication (if applicable)
1. **User Notification**: If production is affected, notify users
2. **Status Page**: Update system status page if applicable
3. **Support Team**: Brief support team on any user-facing issues

## Prevention Measures

### Before Next Attempt
- [ ] **Root Cause Analysis**: Identify why rollback was needed
- [ ] **Testing Enhancement**: Improve testing procedures
- [ ] **Staging Validation**: Ensure thorough staging environment testing
- [ ] **Backup Verification**: Verify all backup procedures work
- [ ] **Team Training**: Brief team on lessons learned

### Improved Procedures
- [ ] **Smaller Steps**: Break upgrade into smaller, more manageable steps
- [ ] **Better Testing**: Enhance automated testing coverage
- [ ] **Monitoring**: Implement better monitoring and alerting
- [ ] **Documentation**: Update procedures based on lessons learned

## Emergency Contacts

### Primary Contacts
- **Frontend Lead**: [Contact Information]
- **Backend Lead**: [Contact Information]
- **DevOps Lead**: [Contact Information]

### Escalation Path
1. Frontend Development Team
2. Backend Development Team
3. Infrastructure Team
4. Technical Leadership

---

**Review Schedule**: After each rollback incident  
**Update Frequency**: Monthly or after significant changes  
**Training**: All team members should be familiar with these procedures
