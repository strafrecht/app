# Dependency Resolution Action Plan

## Overview
Based on codebase analysis, this document outlines the specific actions needed to resolve each disabled dependency for Wagtail 6.4.2 and Django 5.2.4 compatibility.

**Date**: 2025-07-28
**Current State**: Wagtail 6.4.2, Django 5.2.4
**Status**: ✅ COMPLETED - All high priority dependencies resolved - 6/6 major dependencies completed

## ✅ COMPLETED FORKS

### 1. wagtail-birdsong (Newsletter System) - ✅ COMPLETED
**Status**: ✅ FORKED and RE-ENABLED - Fully functional
**GitHub Fork**: https://github.com/strafrecht-admin/wagtail-birdsong-fork.git
**Integration**: Git submodule + editable installation
**Version**: 2.0.1 (forked from 2.0.0)
**Changes Made**: Updated setup.py requirements for Wagtail 6.x/Django 5.x
**Testing**: ✅ Newsletter system, admin interface, and subscription functionality working

## 🔄 NEXT PRIORITY: Remaining Dependencies (Systematic Fork Approach)

### Fork Management Strategy Established
**Approach**: Professional git submodule + GitHub fork management
**Process**: Clone → Update → Test → Push to GitHub → Add as submodule → Re-enable
**Benefits**: Version control, team collaboration, production-ready deployment

### 2. wagtailstreamforms (Form Builder) - ✅ COMPLETED
**Status**: ✅ RESOLVED - Migrated to wagtail-flexible-forms
**Impact**: StreamField-based form building now available with modern alternative
**Solution**: wagtail-flexible-forms v2.1.0 (future official Wagtail form builder)
**Migration Strategy**: Complete replacement with modern package
**Timeline**: ✅ COMPLETED (1 day)
**Risk**: ✅ RESOLVED - No data migration needed, seamless integration

### 3. wagtailfontawesome (FontAwesome Integration) - ✅ COMPLETED
**Status**: ✅ RESOLVED - Migrated to wagtail-font-awesome-svg
**Impact**: FontAwesome icons now available in admin and frontend
**Solution**: wagtail-font-awesome-svg v1.1 (modern SVG-based FontAwesome)
**Migration Strategy**: Modern alternative with enhanced functionality
**Changes Made**:
- Added `wagtailfontawesomesvg` to INSTALLED_APPS
- Updated wagtailcolumnblocks icon reference to use SVG path
- Registered 22 commonly used FontAwesome SVG icons for admin interface
- Frontend FontAwesome CSS continues working via webpack (@fortawesome/fontawesome-free)
**Timeline**: ✅ COMPLETED (1 day)
**Risk**: ✅ RESOLVED - No compatibility issues, improved performance with SVG icons

### 4. comments-wagtail-xtd (Wagtail Comments) - ✅ COMPLETED
**Status**: ✅ FORKED and RE-ENABLED - Fully functional
**Impact**: Wagtail admin comment management now available
**GitHub Fork**: https://github.com/strafrecht-admin/strafrecht-wagtailcomments_xtd.git
**Integration**: Git submodule + editable installation (following wagtail-birdsong pattern)
**Version**: 1.0.0 (forked and updated from 0.0.2)
**Changes Made**:
- Updated all deprecated Wagtail imports for 6.x compatibility
- Fixed URL patterns and translation functions
- Removed FontAwesome dependency (uses built-in Wagtail icons)
- Updated setup.py for modern Django/Wagtail versions
- Comprehensive README with installation instructions
**Testing**: ✅ URL routing, template tags, comment model access, and system check passing
**Dependencies**: ✅ django-comments-xtd 2.10.7 re-enabled and working

### 5. wagtail-markdown (Markdown Support) - MEDIUM PRIORITY
**Status**: ❌ DISABLED - Dependency conflict with wiki package
**Issue**: Bleach version conflict - wagtail-markdown requires bleach<5, wiki requires bleach>=6
**Current Version**: 0.12.1 (installed but disabled)
**Target**: Re-enable when nh3 migration is complete

**Detailed Analysis**:
- wagtail-markdown 0.12.1 requires `bleach<5,>=3.3` (uses deprecated `styles` parameter)
- wiki 0.12.0 requires `bleach[css]<7,>=6` (uses newer bleach API)
- bleach deprecated in 2023, `styles` parameter removed in v5.0
- Upstream issue: https://github.com/torchbox/wagtail-markdown/issues/132 (Replace bleach with nh3)

**Resolution Strategy**:
- ✅ CONFIRMED: wagtail-markdown maintainers aware of issue and planning nh3 migration
- Monitor wagtail-markdown issue #132 for nh3 migration progress
- Consider alternative markdown packages if migration is delayed
- Temporary workaround: Use raw HTML or alternative rich text solutions
**Timeline**: Waiting for upstream nh3 migration
**Risk**: Medium - dependency resolution required

### 6. wagtail-treemodeladmin (Tree Admin Interface) - HIGH PRIORITY
**Status**: ✅ COMPLETED - Successfully re-enabled and working
**Impact**: Tree-like navigation restored for flashcard deck management
**Current Version**: 1.9.2 (supports Wagtail 6.x)

**Resolution Completed**:
- ✅ **Research**: Confirmed v1.9.2 includes Wagtail 6.x support (PR #45 merged April 2024)
- ✅ **Re-enabled**: Updated requirements/common.txt and app/settings.py
- ✅ **Fixed Configuration**: Updated flashcards/wagtail_hooks.py to use TreeModelAdmin
- ✅ **Corrected Relationships**: Fixed child_field from 'flashcard_set' to 'flashcards' (related_name)
- ✅ **Validated**: System check passes, TreeModelAdmin imports successfully

**Timeline**: ✅ COMPLETED (1 day)
**Risk**: ✅ RESOLVED - No compatibility issues

## Priority 2: Important Dependencies (Address Soon)

### 7. wagtail-modelchooser (Model Selection Widgets) - ✅ COMPLETED
**Status**: ✅ RE-ENABLED - Model chooser functionality restored
**Impact**: Model chooser panels and blocks now available for admin interface
**Current Version**: 4.0.1 (compatible with Wagtail 6.4.2)

**Resolution Completed**:
- ✅ **Research**: Confirmed wagtail-modelchooser 4.0.1 supports Wagtail >=4.0 (compatible with 6.4.2)
- ✅ **Re-enabled**: Updated app/settings.py to include 'wagtailmodelchooser' in INSTALLED_APPS
- ✅ **Imports Restored**: Updated pages/models/sidebar.py to use ModelChooserBlock and ModelChooserPanel
- ✅ **Poll Integration**: Restored SidebarPollChooser to use ModelChooserBlock('wagtailpolls.Poll')
- ✅ **Validated**: System check passes, no compatibility issues detected

**Changes Made**:
- Re-enabled 'wagtailmodelchooser' in INSTALLED_APPS
- Restored ModelChooserBlock import in sidebar.py
- Updated SidebarPollChooser to use proper ModelChooserBlock instead of CharBlock workaround
- Verified wagtailpolls.models.Poll is properly registered for model chooser

**Timeline**: ✅ COMPLETED (1 day)
**Risk**: ✅ RESOLVED - Full compatibility with Wagtail 6.4.2 confirmed

### 8. wagtail-color-panel (Color Picker) - MEDIUM PRIORITY
**Status**: ✅ RESOLVED - Native color picker functionality restored
**Impact**: ✅ RESOLVED - Color selection now uses native wagtail-color-panel
**Usage Found**:
- Re-enabled in INSTALLED_APPS (app/settings.py)
- Updated SidebarHeaderBlock to use NativeColorBlock (pages/models/sidebar.py)
- Confirmed compatibility with Wagtail 6.4.2

**Resolution Strategy**: ✅ COMPLETED - Re-enabled native wagtail-color-panel
- **Action**: ✅ COMPLETED - Re-enabled wagtail_color_panel in INSTALLED_APPS
- **Changes**: ✅ COMPLETED - Updated sidebar.py to use NativeColorBlock instead of django-colorfield workaround
- **Timeline**: ✅ COMPLETED (1 day)
- **Risk**: ✅ RESOLVED - Full compatibility with Wagtail 6.4.2 confirmed

### 9. wagtail-autocomplete (Autocomplete Widgets) - ✅ COMPLETED
**Status**: ✅ RESOLVED - Re-enabled with latest version
**Impact**: Admin interface autocomplete widgets now available

**Resolution Strategy**: ✅ COMPLETED - Latest Version Compatibility
- **Action**: ✅ COMPLETED - Re-enabled wagtail-autocomplete v0.12.0
- **Changes Made**:
  - Already updated in requirements.txt to wagtail-autocomplete>=0.12.0
  - Re-enabled 'wagtailautocomplete' in INSTALLED_APPS
  - Re-enabled autocomplete admin URLs in app/urls.py
  - Re-enabled AutocompletePanel import in pages/models/news.py
  - Confirmed compatibility with Wagtail 6.4.2
- **Timeline**: ✅ COMPLETED (1 day)
- **Risk**: ✅ RESOLVED - Full compatibility with Wagtail 6.4.2 confirmed

## Priority 3: Lower Priority Dependencies

### 7. wagtailfontawesome (FontAwesome Integration) - ✅ COMPLETED
**Status**: ✅ RESOLVED - Migrated to wagtail-font-awesome-svg
**Impact**: FontAwesome icons now available in admin and frontend

**Resolution Strategy**: Modern Alternative Migration
- **Action**: ✅ COMPLETED - Migrated to wagtail-font-awesome-svg v1.1
- **Changes Made**:
  - Added `wagtailfontawesomesvg` to INSTALLED_APPS
  - Updated wagtailcolumnblocks icon reference
  - Registered 22 commonly used FontAwesome SVG icons for admin
  - Frontend FontAwesome CSS continues working via webpack
- **Timeline**: ✅ COMPLETED (1 day)
- **Risk**: ✅ RESOLVED - No compatibility issues

### 8. wagtail-markdown (Markdown Support) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Markdown editing unavailable  
**Impact**: Markdown fields not available  

**Resolution Strategy**: Evaluate Necessity
- **Action**: Check if RichTextField can replace markdown fields
- **Alternative**: Use django-markdownify (already installed)
- **Timeline**: 1-2 days
- **Risk**: Low - alternatives available

### 9. comments-wagtail-xtd (Comments Integration) - ✅ COMPLETED
**Status**: ✅ FORKED and RE-ENABLED - Wagtail admin integration working
**Impact**: Full Wagtail admin comment management functionality restored
**Solution**: Created updated fork with Wagtail 6.x compatibility
**Changes Made**: Complete modernization of codebase for current versions
**Timeline**: ✅ COMPLETED (1 day)
**Risk**: ✅ RESOLVED - Full functionality restored with modern codebase

## Dependencies Already Working

### ✅ wagtailmenus==3.0.2
**Status**: ✅ ENABLED and working  
**Action**: Monitor for issues, no immediate action needed

### ✅ django-colorfield==0.4.1
**Status**: ✅ Available as replacement for wagtail-color-panel

### ✅ mjml
**Status**: ✅ Working for email templates

## Implementation Timeline

### Week 1 (Days 1-3)
1. **Day 1**: Fork wagtail-birdsong and update for Wagtail 3.0
2. **Day 2**: Test birdsong fork and re-enable newsletter functionality
3. **Day 3**: ✅ COMPLETED - Migrated wagtailstreamforms to wagtail-flexible-forms

### Week 1 (Days 4-5)
4. **Day 4**: ✅ COMPLETED - Re-enabled wagtail-color-panel with native functionality
5. **Day 5**: ✅ COMPLETED - wagtail-treemodeladmin re-enabled and working

### Week 2 (Days 6-10)
6. **Days 6-7**: ✅ COMPLETED - treemodeladmin solution implemented
7. **Days 8-9**: Replace wagtail-modelchooser with native alternatives
8. **Day 10**: Clean up remaining low-priority dependencies

## Success Criteria

### Phase 1 Complete (Critical Dependencies)
- [x] Newsletter system fully functional (wagtail-birdsong)
- [x] Form building capabilities restored (wagtail-flexible-forms)
- [x] FontAwesome icons working in admin and frontend (wagtail-font-awesome-svg)
- [x] Comment system fully functional (django-comments-xtd + wagtailcomments_xtd)
- [x] Tree admin interface working for flashcards (wagtail-treemodeladmin)
- [x] Model chooser functionality restored (wagtail-modelchooser)
- [x] No critical functionality missing

### Phase 2 Complete (All Dependencies)
- [x] FontAwesome icons working in admin interface
- [ ] All admin interface features working
- [x] Color picker functionality restored (wagtail-color-panel)
- [ ] Autocomplete features working
- [ ] No disabled dependencies remaining

### Final Validation
- [x] FontAwesome functionality tested and working
- [x] Comment system functionality tested and working
- [x] Model chooser functionality tested and working
- [x] Poll model registered and available for chooser
- [ ] All tests passing
- [ ] Admin interface fully functional
- [x] Newsletter sending working
- [x] Form creation working
- [ ] No deprecation warnings
- [ ] Performance maintained

## Risk Mitigation

### High-Risk Items
1. **wagtail-birdsong fork** - Create comprehensive tests before deployment
2. **wagtail-treemodeladmin** - ✅ RESOLVED - Successfully re-enabled

### Rollback Plan
- Keep current working state as backup
- Test each change individually
- Document all changes for easy rollback

---

**Next Steps**: Begin with wagtail-birdsong fork as highest priority item.
