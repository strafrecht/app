# Dependency Resolution Action Plan

## Overview
Based on codebase analysis, this document outlines the specific actions needed to resolve each disabled dependency for Wagtail 6.4.2 and Django 5.2.4 compatibility.

**Date**: 2025-07-28
**Current State**: Wagtail 6.4.2, Django 5.2.4
**Status**: Fork management approach established - systematic implementation in progress

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

### 2. wagtailstreamforms (Form Builder) - NEXT PRIORITY
**Status**: 🔴 DISABLED - Form functionality missing
**Impact**: StreamField-based form building unavailable
**Original Version**: Last working with older Wagtail versions
**Fork Strategy**: Clone → Update for Wagtail 6.x → Test → Deploy
**Timeline**: 1-2 days
**Risk**: Medium - StreamField API changes may require updates

### 3. wagtailfontawesome (FontAwesome Integration) - HIGH PRIORITY
**Status**: 🔴 DISABLED - Icon functionality missing
**Impact**: FontAwesome icons not available in admin/frontend
**Original Issue**: Uses deprecated `wagtail.core` imports
**Fork Strategy**: Simple import updates for Wagtail 6.x
**Timeline**: 1 day
**Risk**: Low - straightforward import fixes

### 4. comments-wagtail-xtd (Wagtail Comments) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Comment integration missing
**Impact**: Wagtail-specific comment functionality unavailable
**Dependencies**: Requires django-comments-xtd to be re-enabled first
**Fork Strategy**: Update imports + test integration
**Timeline**: 2-3 days
**Risk**: Medium - depends on django-comments-xtd compatibility

### 5. wagtail-markdown (Markdown Support) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Markdown functionality missing
**Impact**: Markdown fields not available
**Original Issue**: bleach dependency conflicts
**Fork Strategy**: Update dependencies + resolve conflicts
**Timeline**: 2-3 days
**Risk**: Medium - dependency resolution required

### 2. wagtail-treemodeladmin (Tree Admin Interface) - HIGH PRIORITY
**Status**: 🔴 DISABLED - Admin interface degraded  
**Impact**: Flashcard deck management using basic ModelAdmin  
**Usage Found**:
- `flashcards/wagtail_hooks.py` - DeckAdmin changed from TreeModelAdmin to ModelAdmin
- Comments indicate child_field and child_model_admin disabled

**Resolution Strategy**: Research and Update
- **Action**: Check if newer version supports Wagtail 3.0
- **Alternative**: Implement custom tree interface or use native Wagtail features
- **Timeline**: 2-3 days
- **Risk**: Medium - may need custom implementation

### 3. wagtailstreamforms (Form Builder) - HIGH PRIORITY  
**Status**: 🔴 DISABLED - Form functionality missing  
**Impact**: StreamField-based form building unavailable  
**Usage Found**:
- Previously upgraded to 3.17 during Wagtail 2.15 upgrade
- Disabled for Wagtail 3.0 due to StreamField API changes

**Resolution Strategy**: Version Research
- **Action**: Research wagtailstreamforms versions compatible with Wagtail 3.0
- **Alternative**: Use wagtail.contrib.forms for basic form functionality
- **Timeline**: 1-2 days
- **Risk**: Low - likely has compatible version

## Priority 2: Important Dependencies (Address Soon)

### 4. wagtail-modelchooser (Model Selection Widgets) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Admin widgets degraded  
**Impact**: Model chooser panels replaced with CharBlock workarounds  
**Usage Found**:
- Mentioned in upgrade log as replaced with CharBlock for poll selection
- Used for model selection in admin interface

**Resolution Strategy**: Native Wagtail Alternative
- **Action**: Replace with native Wagtail chooser panels where possible
- **Research**: Check if Wagtail 3.0 has built-in model choosers
- **Timeline**: 2-3 days
- **Risk**: Low - likely replaceable with native features

### 5. wagtail-color-panel (Color Picker) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Color picker unavailable  
**Impact**: Color selection replaced with CharBlock workarounds  
**Usage Found**:
- Mentioned in upgrade log as replaced with CharBlock for color fields
- `django-colorfield` already installed as alternative

**Resolution Strategy**: Replace with django-colorfield
- **Action**: Update models to use ColorField from django-colorfield
- **Changes**: Replace wagtail_color_panel usage with django-colorfield
- **Timeline**: 1 day
- **Risk**: Very Low - direct replacement available

### 6. wagtail-autocomplete (Autocomplete Widgets) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Autocomplete functionality missing  
**Impact**: Admin interface autocomplete widgets unavailable  

**Resolution Strategy**: Native Wagtail Features
- **Action**: Check if Wagtail 3.0 has built-in autocomplete features
- **Alternative**: Use standard Django autocomplete widgets
- **Timeline**: 1-2 days
- **Risk**: Low - likely replaceable

## Priority 3: Lower Priority Dependencies

### 7. wagtailfontawesome (FontAwesome Integration) - LOW PRIORITY
**Status**: 🔴 DISABLED - Icon integration missing  
**Impact**: FontAwesome icons not available in admin  

**Resolution Strategy**: Direct Integration
- **Action**: Include FontAwesome CSS/JS directly in templates
- **Remove**: wagtailfontawesome dependency entirely
- **Timeline**: 1 day
- **Risk**: Very Low - simple CSS/JS inclusion

### 8. wagtail-markdown (Markdown Support) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Markdown editing unavailable  
**Impact**: Markdown fields not available  

**Resolution Strategy**: Evaluate Necessity
- **Action**: Check if RichTextField can replace markdown fields
- **Alternative**: Use django-markdownify (already installed)
- **Timeline**: 1-2 days
- **Risk**: Low - alternatives available

### 9. comments-wagtail-xtd (Comments Integration) - MEDIUM PRIORITY
**Status**: 🔴 DISABLED - Wagtail-specific comment features missing  
**Impact**: django-comments-xtd still works, but no Wagtail integration  

**Resolution Strategy**: Evaluate Necessity
- **Action**: Check if Wagtail-specific features are needed
- **Keep**: django-comments-xtd (already working)
- **Timeline**: 1 day
- **Risk**: Very Low - base functionality preserved

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
3. **Day 3**: Research and fix wagtailstreamforms compatibility

### Week 1 (Days 4-5)
4. **Day 4**: Replace wagtail-color-panel with django-colorfield
5. **Day 5**: Research wagtail-treemodeladmin alternatives

### Week 2 (Days 6-10)
6. **Days 6-7**: Implement treemodeladmin solution
7. **Days 8-9**: Replace wagtail-modelchooser with native alternatives
8. **Day 10**: Clean up remaining low-priority dependencies

## Success Criteria

### Phase 1 Complete (Critical Dependencies)
- [ ] Newsletter system fully functional
- [ ] Form building capabilities restored
- [ ] Tree admin interface working for flashcards
- [ ] No critical functionality missing

### Phase 2 Complete (All Dependencies)
- [ ] All admin interface features working
- [ ] Color picker functionality restored
- [ ] Autocomplete features working
- [ ] No disabled dependencies remaining

### Final Validation
- [ ] All tests passing
- [ ] Admin interface fully functional
- [ ] Newsletter sending working
- [ ] Form creation working
- [ ] No deprecation warnings
- [ ] Performance maintained

## Risk Mitigation

### High-Risk Items
1. **wagtail-birdsong fork** - Create comprehensive tests before deployment
2. **wagtail-treemodeladmin** - Have fallback to basic ModelAdmin

### Rollback Plan
- Keep current working state as backup
- Test each change individually
- Document all changes for easy rollback

---

**Next Steps**: Begin with wagtail-birdsong fork as highest priority item.
