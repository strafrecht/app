# Custom Changes Documentation

## Overview
This document tracks all custom modifications, patches, and workarounds implemented during the Wagtail/Django upgrade process. This includes forked dependencies, custom code modifications, and configuration changes.

**Current Status**: ✅ MAJOR UPGRADE COMPLETED - Wagtail 2.13 → 6.4.2, Django 3.2.5 → 5.2.4
**Last Updated**: 2025-07-27

## ✅ COMPLETED CHANGES (Wagtail 6.4.2 & Django 5.2.4 Upgrade)

### Forked Dependencies for Wagtail 6.x/Django 5.x Compatibility

#### wagtail-birdsong (Newsletter System) - FORKED
- **Original Version**: 2.0.0 (neon-jungle/wagtail-birdsong)
- **GitHub Fork**: https://github.com/strafrecht-admin/wagtail-birdsong-fork.git
- **Fork Version**: 2.0.1
- **Integration**: Git submodule at `wagtail-birdsong-fork/`
- **Installation**: `pip install -e ./wagtail-birdsong-fork`
- **Status**: ✅ COMPLETED and WORKING

**Changes Made**:
1. **Import Fix**: Updated `from wagtail.coreutils import camelcase_to_underscore` (line 10 in models.py)
   - The import was correct - `wagtail.coreutils` still exists in Wagtail 6.x
2. **Dependencies Updated**: Updated setup.py requirements:
   - `wagtail>=6.0` (was `wagtail>=5.2`)
   - Added `Django>=5.0` requirement
3. **Version Bump**: Updated to 2.0.1 to distinguish from original

**Re-enabled Components**:
- ✅ `birdsong` app in INSTALLED_APPS
- ✅ `mjml` app in INSTALLED_APPS (upgraded to django-mjml 1.4)
- ✅ `emails` app in INSTALLED_APPS
- ✅ Newsletter models: `NewsletterEmail`, `LSHNewsletter`
- ✅ Newsletter admin: `LSHNewsletterAdmin`, `ContactAdmin`
- ✅ Birdsong URLs: `/mail/` endpoints
- ✅ Newsletter subscription functionality in core/views.py

**Git Submodule Management**:
- ✅ Added as git submodule: `git submodule add https://github.com/strafrecht-admin/wagtail-birdsong-fork.git wagtail-birdsong-fork`
- ✅ Fork changes pushed to GitHub repository
- ✅ Submodule properly integrated with main project
- ✅ `.gitmodules` file created for submodule tracking

**Testing**: ✅ Application passes `python manage.py check --deploy` with no errors

**Fork Management Benefits**:
- Version control for fork changes
- Easy collaboration and updates
- Production-ready deployment approach
- Clear separation from main project code

## ✅ COMPLETED CHANGES (Previous Wagtail 5.2 Upgrade)

### Wagtail 5.0+ Breaking Changes Fixed
*All changes required for Wagtail 5.0+ compatibility*

#### Wagtail Core Import Updates
- **Files Modified**: 41 Python files across the entire codebase
- **Change**: Updated `wagtail.core.*` imports to `wagtail.*`
- **Script Used**: `dev-upgrade/fix_wagtail_core_imports.py`
- **Examples**:
  - `from wagtail.core.models import Page` → `from wagtail.models import Page`
  - `from wagtail.core.fields import RichTextField` → `from wagtail.fields import RichTextField`
  - `from wagtail.core.blocks import StreamBlock` → `from wagtail.blocks import StreamBlock`
- **Status**: ✅ COMPLETED

#### Panel System Updates (Wagtail 5.0+)
- **Files Modified**: 8 Python files
- **Changes**:
  - Replaced `StreamFieldPanel` with `FieldPanel` (deprecated in Wagtail 5.0)
  - Replaced `FieldRowPanel` with `MultiFieldPanel` (deprecated in Wagtail 5.0)
  - Added missing imports for `TabbedInterface`, `MultiFieldPanel`
- **Script Used**: `dev-upgrade/fix_wagtail_5_panels.py`
- **Status**: ✅ COMPLETED

#### Migration Files Fixed
- **Files Modified**: 23 migration files
- **Change**: Updated old `wagtail.core.*` imports in migration files
- **Script Used**: `dev-upgrade/fix_migration_wagtail_core.py`
- **Status**: ✅ COMPLETED

### Django 4.0+ Compatibility Fixes
*All changes required for Django 4.0+ compatibility*

#### URL Pattern Updates
- **Files Modified**: `quiz/wagtail_hooks.py`, `wagtailpolls/wagtail_hooks.py`
- **Change**: Updated `django.conf.urls.url` to `django.urls.re_path`
- **Reason**: `url()` function removed in Django 4.0
- **Status**: ✅ COMPLETED

#### Translation Function Updates
- **Files Modified**: `wagtailpolls/views/chooser.py`, `wagtailpolls/forms.py`
- **Changes**:
  - `ugettext` → `gettext`
  - `ungettext_lazy` → `ngettext_lazy`
- **Reason**: Old translation functions removed in Django 4.0
- **Status**: ✅ COMPLETED

#### IP Address Detection Updates
- **Files Modified**: `wagtailpolls/forms.py`
- **Change**: Updated django-ipware API usage
- **Old**: `get_real_ip(request) or get_ip(request)`
- **New**: `get_client_ip(request)`
- **Status**: ✅ COMPLETED

### Package Version Updates
*Package updates for Django 4.2/Wagtail 5.2 compatibility*

#### Core Package Updates
- **django-comments-xtd**: 2.9.1 → 2.10.7 (Django 4.2 compatibility)
- **wagtailmenus**: 3.0.2 → 3.1.9 (Wagtail 5.0+ compatibility)
- **django-pipeline**: 2.0.6 → 3.1.0 (Django 4.0+ compatibility)
- **django-pwa**: 1.0.10 → 1.1.0 (Django 4.0+ compatibility)
- **django-filter**: 22.1 → 23.5 (Wagtail 5.2 requirement)
- **Status**: ✅ COMPLETED

#### Additional Dependencies Installed
- **wrapt**: 1.17.2 (required by wiki_patch.py)
- **html2text**: 2025.4.15 (required by core.views)
- **wget**: 3.2 (required by core.seed)
- **django-ipware**: 7.0.1 (updated API)
- **Status**: ✅ COMPLETED

#### Pillow Version Management
- **Issue**: Pillow 10.4.0 incompatible with django-avatar (Image.ANTIALIAS removed)
- **Solution**: Downgraded to Pillow 9.5.0
- **Removed**: pillow-heif (dependency conflict)
- **Status**: ✅ COMPLETED

### Database Migration Handling
*Special handling for problematic migrations*

#### Wagtail Log Entry Migrations
- **Migrations**: wagtailcore.0088, wagtailcore.0089
- **Issue**: Column `wagtailcore_pagelogentry.data` does not exist
- **Solution**: Faked migrations (log entries can be regenerated)
- **Command**: `python manage.py migrate wagtailcore 0088 --fake`
- **Status**: ✅ COMPLETED

## Custom Modifications Tracking

### Forked Dependencies
*Dependencies that required custom forks due to incompatibility with newer versions*

#### wagtail-birdsong (Newsletter System)
- **Original Version**: 0.2.0
- **Fork Status**: TBD
- **Reason**: Incompatible with Wagtail 3.0+
- **Repository**: TBD
- **Modifications**: TBD
- **Maintenance Plan**: TBD

#### django-wiki (Wiki Functionality)  
- **Original Version**: 0.7.10
- **Fork Status**: TBD
- **Reason**: Incompatible with Django 4.0+
- **Repository**: TBD
- **Modifications**: TBD
- **Maintenance Plan**: TBD

#### wagtail-autocomplete
- **Original Version**: 0.6.3
- **Fork Status**: TBD
- **Reason**: Incompatible with Wagtail 3.0+
- **Repository**: TBD
- **Modifications**: TBD
- **Maintenance Plan**: TBD

### Custom Code Patches
*Direct modifications to application code for compatibility*

#### URL Pattern Updates (Django 4.0+)
- **File**: `urls.py` files throughout project
- **Change**: Convert `url()` to `path()` patterns
- **Reason**: Django 4.0 deprecated `url()` function
- **Status**: TBD

#### Settings Configuration Updates
- **File**: `app/settings/*.py`
- **Changes**: 
  - Remove deprecated settings
  - Update middleware configuration
  - ASGI configuration updates
- **Status**: TBD

#### Wagtail StreamField Updates
- **Files**: Models using StreamField
- **Changes**: Update StreamField API usage for Wagtail 3.0+
- **Reason**: StreamField API changes in Wagtail 3.0
- **Status**: TBD

### Configuration Workarounds
*Temporary configuration changes to maintain compatibility*

#### Frontend Build Compatibility
- **Issue**: Node.js v22 incompatible with legacy frontend dependencies
- **Workaround**: TBD (likely Node.js version downgrade)
- **Files Affected**: `package.json`, webpack configuration
- **Permanent Solution**: Update frontend dependencies

#### Database Connection Settings
- **Issue**: PostgreSQL connection configuration
- **Current**: localhost:5434 with custom user
- **Modifications**: None required currently
- **Notes**: Monitor for Django 4.0+ connection changes

### Replacement Packages
*Third-party packages replaced with alternatives*

#### Planned Replacements

**wagtail-color-panel** → Custom Implementation
- **Reason**: No longer maintained for newer Wagtail versions
- **Replacement**: Custom color picker field
- **Implementation Status**: TBD

**wagtail-treemodeladmin** → Native Wagtail Admin
- **Reason**: Incompatible with newer Wagtail versions
- **Replacement**: Native Wagtail admin with custom tree functionality
- **Implementation Status**: TBD

**django-comments-xtd** → Modern Comment System
- **Reason**: Incompatible with Django 4.0+
- **Replacement**: TBD (research modern alternatives)
- **Implementation Status**: TBD

## Custom Development Required

### Newsletter System (wagtail-birdsong replacement)
**Priority**: HIGH - Critical functionality

**Requirements**:
- Email template management
- Subscriber management
- Campaign tracking
- Integration with Wagtail admin
- MJML template support

**Implementation Plan**:
1. Analyze current wagtail-birdsong usage
2. Design replacement architecture
3. Implement core functionality
4. Migrate existing data
5. Test thoroughly

**Files to Create/Modify**:
- `newsletter/` app directory
- Models for campaigns, subscribers, templates
- Admin interface integration
- Email sending functionality
- Migration scripts for data transfer

### Wiki System (django-wiki replacement)
**Priority**: HIGH - Critical functionality

**Requirements**:
- Article creation and editing
- Version history
- User permissions
- Search functionality
- Integration with main site

**Implementation Options**:
1. Fork and update django-wiki for Django 4.0+
2. Replace with modern wiki solution
3. Custom implementation

**Decision**: TBD based on complexity analysis

### Color Picker Functionality
**Priority**: MEDIUM

**Requirements**:
- Color field for Wagtail admin
- Color picker widget
- Hex/RGB value support

**Implementation**:
- Custom Wagtail field
- JavaScript color picker widget
- Admin interface integration

### Tree Model Admin
**Priority**: MEDIUM

**Requirements**:
- Hierarchical model display
- Drag-and-drop reordering
- Wagtail admin integration

**Implementation**:
- Custom admin views
- JavaScript tree interface
- Model ordering functionality

## Code Quality Standards

### Custom Code Requirements
- **Documentation**: All custom code must be thoroughly documented
- **Testing**: Unit tests required for all custom functionality
- **Code Style**: Follow Django/Wagtail coding standards
- **Version Control**: All changes tracked in git with descriptive commits

### Fork Maintenance Strategy
- **Repository Naming**: `strafrecht-[package-name]`
- **Branching**: Maintain upgrade branches for each version
- **Documentation**: README with modification details
- **Testing**: Automated testing for custom modifications
- **Updates**: Regular updates from upstream when possible

## Migration Strategy for Custom Changes

### Phase 1: Analysis and Planning
- [ ] Catalog all custom modifications in current codebase
- [ ] Identify dependencies requiring forks
- [ ] Plan replacement implementations
- [ ] Create development timeline

### Phase 2: Fork Creation
- [ ] Create forks for critical dependencies
- [ ] Implement compatibility updates
- [ ] Test forked packages thoroughly
- [ ] Document all modifications

### Phase 3: Custom Development
- [ ] Implement replacement functionality
- [ ] Create migration scripts for data transfer
- [ ] Develop comprehensive tests
- [ ] Update documentation

### Phase 4: Integration and Testing
- [ ] Integrate custom solutions
- [ ] Perform end-to-end testing
- [ ] Validate all functionality
- [ ] Performance testing

## Rollback Procedures for Custom Changes

### Fork Rollback
1. **Revert to Original Package**:
   ```bash
   pip uninstall [forked-package]
   pip install [original-package]==version
   ```

2. **Update Requirements**:
   - Remove fork references
   - Restore original package versions

3. **Code Rollback**:
   - Revert custom modifications
   - Restore original functionality

### Custom Code Rollback
1. **Git Revert**:
   ```bash
   git revert [commit-hash]
   ```

2. **Database Rollback**:
   - Restore from pre-modification backup
   - Run reverse migrations if available

3. **Configuration Rollback**:
   - Restore original settings
   - Revert URL patterns
   - Reset middleware configuration

## Testing Strategy for Custom Changes

### Unit Testing
- Test all custom functionality
- Mock external dependencies
- Validate edge cases
- Performance testing

### Integration Testing
- Test with upgraded frameworks
- Validate admin interface integration
- Test data migration scripts
- End-to-end functionality testing

### Regression Testing
- Ensure existing functionality unchanged
- Validate all user workflows
- Performance benchmarking
- Security testing

## Documentation Requirements

### For Each Custom Change
- **Purpose**: Why the change was necessary
- **Implementation**: How it was implemented
- **Testing**: How it was tested
- **Maintenance**: How to maintain/update
- **Rollback**: How to revert if needed

### Code Documentation
- Inline comments for complex logic
- Docstrings for all functions/classes
- README files for custom packages
- API documentation for custom interfaces

## Change Log Template

### YYYY-MM-DD: [Change Description]
**Type**: [Fork/Patch/Replacement/Configuration]
**Priority**: [HIGH/MEDIUM/LOW]
**Status**: [PLANNED/IN_PROGRESS/COMPLETED/TESTED]

**Reason for Change**:
[Detailed explanation of why change was necessary]

**Implementation Details**:
[How the change was implemented]

**Files Modified**:
- [List of files changed]

**Testing Performed**:
- [List of tests performed]

**Rollback Procedure**:
[Steps to revert this change]

**Maintenance Notes**:
[Any ongoing maintenance requirements]

---

## Current Custom Changes Log

### 2025-07-27: Baseline Documentation
**Type**: Documentation
**Status**: COMPLETED

**Action**: Created custom changes tracking framework
**Files Created**: CUSTOM_CHANGES.md
**Next Steps**: Begin analysis of current codebase for existing custom modifications

---

*This document will be updated with each custom modification made during the upgrade process.*
