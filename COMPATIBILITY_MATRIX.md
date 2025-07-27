# Dependency Compatibility Matrix

## Overview
This matrix tracks compatibility of all dependencies across the planned Wagtail/Django upgrade path.

**Legend**:
- ✅ **Compatible**: Confirmed working
- ⚠️ **Needs Testing**: Likely compatible but requires validation
- ❌ **Incompatible**: Known incompatibility
- 🔄 **Needs Update**: Requires version update
- 🚫 **Deprecated**: Package deprecated/abandoned
- 📝 **Custom Fork**: Requires custom fork/modification

## Core Framework Compatibility

| Package | Current | Wagtail 2.14 | Wagtail 2.15 | Wagtail 3.0 | Wagtail 4.0 | Wagtail 5.0 | Wagtail 6.0 | Latest |
|---------|---------|--------------|--------------|-------------|-------------|-------------|-------------|---------|
| **Django** | 3.2.5 | ✅ 3.2.x | ✅ 3.2.x | 🔄 4.0+ | 🔄 4.1+ | 🔄 4.2+ | 🔄 5.0+ | 🔄 5.1+ |
| **wagtail** | 2.13 | 🔄 2.14 | 🔄 2.15 | 🔄 3.0 | 🔄 4.0 | 🔄 5.0 | 🔄 6.0 | 🔄 Latest |
| **djangorestframework** | 3.12.4 | ✅ | ✅ | ⚠️ | ⚠️ | 🔄 | 🔄 | 🔄 |

## Wagtail Extensions Compatibility

| Package | Current | 2.14 | 2.15 | 3.0 | 4.0 | 5.0 | 6.0 | Latest | Notes |
|---------|---------|------|------|-----|-----|-----|-----|---------|-------|
| **wagtail-birdsong** | 0.2.0 | ⚠️ | ⚠️ | ❌ | ❌ | 🔄 2.0.0 | ✅ 2.0.0 | ✅ 2.0.0 | Newsletter system - upgrade to 2.0.0 at Wagtail 5.2+ |
| **wagtailmenus** | 3.0.2 | ✅ | ✅ | ⚠️ | 🔄 | 🔄 | 🔄 | 🔄 | Navigation - critical functionality |
| **wagtailnews** | 2.7.1 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | News system - may need replacement |
| **wagtail-autocomplete** | 0.6.3 | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | May need modern alternative |
| **wagtail-color-panel** | 1.2.0 | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | Color picker functionality |
| **wagtail-markdown** | 0.7.0 | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | Markdown support |
| **wagtail-modelchooser** | 2.13.1 | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | Model selection widget |
| **wagtailfontawesome** | 1.2.1 | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | FontAwesome integration |
| **wagtailstreamforms** | 3.15 | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | Form builder |
| **wagtail-treemodeladmin** | 1.5.0 | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ | Tree model admin |

## Django Extensions Compatibility

| Package | Current | Django 3.2 | Django 4.0 | Django 4.1 | Django 4.2 | Django 5.0 | Django 5.1 | Notes |
|---------|---------|-------------|-------------|-------------|-------------|-------------|-------------|-------|
| **django-wiki** | 0.7.10 | ✅ | 🔄 0.11.x | 🔄 0.11.x | 🔄 0.11.x | 🔄 0.12.0 | ✅ 0.12.0 | Wiki - upgrade path available |
| **channels** | 3.0.3 | ✅ | 🔄 | 🔄 | 🔄 | 🔄 | 🔄 | WebSocket support |
| **django-admin-interface** | 0.16.3 | ✅ | ⚠️ | ⚠️ | ⚠️ | 🔄 | 🔄 | Admin theming |
| **django-comments-xtd** | 2.9.1 | ✅ | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | Comment system |
| **django-cors-headers** | 3.7.0 | ✅ | ✅ | ✅ | 🔄 | 🔄 | 🔄 | CORS handling |
| **django-crispy-forms** | 1.14.0 | ✅ | ✅ | ✅ | ✅ | 🔄 | 🔄 | Form rendering |
| **django-debug-toolbar** | 3.2.1 | ✅ | ✅ | ✅ | 🔄 | 🔄 | 🔄 | Debug tools |

## Database & Infrastructure

| Package | Current | Compatibility | Upgrade Path | Notes |
|---------|---------|---------------|--------------|-------|
| **psycopg2-binary** | 2.8.6 | ✅ All versions | 🔄 Latest | PostgreSQL adapter |
| **aioredis** | 1.3.1 | ⚠️ Older version | 🔄 2.x+ | Redis async client |
| **channels-redis** | 3.2.0 | ✅ Most versions | 🔄 Latest | Channels Redis backend |
| **hiredis** | 2.0.0 | ✅ All versions | ✅ Current | Redis parser |

## Frontend Dependencies (Node.js)

| Package | Current Issue | Required Action | Notes |
|---------|---------------|-----------------|-------|
| **Node.js** | v22.17.1 | 🔄 Downgrade to v16 | Frontend build compatibility |
| **Webpack** | Unknown | 📝 Analysis needed | Build system |
| **Vue.js** | Unknown | 📝 Analysis needed | Frontend framework |

## Risk Assessment by Upgrade Phase

### Phase 1: Wagtail 2.13 → 2.15 (LOW RISK)
- Most dependencies should remain compatible
- Focus on testing Wagtail extensions
- No Django upgrade required

### Phase 2: Wagtail 2.15 → 3.0 (HIGH RISK)
- Major version jump with breaking changes
- Many Wagtail extensions likely incompatible
- Requires Django 4.0+ upgrade
- **Critical packages needing attention**:
  - wagtail-birdsong (newsletter system)
  - django-wiki (wiki functionality)
  - wagtail-autocomplete
  - wagtail-markdown

### Phase 3: Django 3.2 → 4.0 (MEDIUM RISK)
- URL pattern changes (url() → path())
- Deprecated settings removal
- ASGI configuration updates
- **Critical packages needing attention**:
  - django-wiki (major compatibility issues)
  - django-comments-xtd
  - channels configuration

### Phase 4: Wagtail 4.0+ (MEDIUM RISK)
- StreamField API changes
- Admin interface modifications
- Search backend changes
- Image/document handling updates

### Phase 5: Wagtail 5.0+ (HIGH RISK)
- Major API overhauls
- Many legacy extensions incompatible
- Performance improvements but breaking changes

## Action Plan for Incompatible Dependencies

### Packages with Upgrade Paths Available ✅
1. **wagtail-birdsong**: 0.2.0 → 2.0.0 (supports Wagtail 5.2+)
2. **django-wiki**: 0.7.10 → 0.12.0 (supports Django 4.0+ and 5.x)

### Immediate Forks Required
1. **wagtail-autocomplete**: Admin interface dependency

### Alternative Packages to Research
1. **wagtail-birdsong** → Modern newsletter solution
2. **wagtailnews** → Built-in Wagtail news features
3. **wagtail-markdown** → Native Wagtail markdown support
4. **django-comments-xtd** → Modern comment system

### Custom Development Required
1. **wagtail-color-panel** → Custom color picker implementation
2. **wagtail-treemodeladmin** → Custom tree admin interface
3. **wagtailfontawesome** → Direct FontAwesome integration

## Testing Strategy per Phase

### Pre-Upgrade Testing
- [ ] Full test suite execution
- [ ] Admin interface functionality
- [ ] Newsletter system testing
- [ ] Wiki functionality testing
- [ ] Frontend build testing

### Post-Upgrade Validation
- [ ] All tests pass
- [ ] No deprecation warnings
- [ ] Performance benchmarking
- [ ] User acceptance testing
- [ ] Security audit

---

*This matrix will be updated as we progress through each upgrade phase with actual compatibility results and solutions implemented.*
