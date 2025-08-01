# REVISED UPGRADE STRATEGY: Continue Wagtail Upgrade Path

## Key Insight
Instead of trying to fix dependencies for Wagtail 3.0, we should **continue upgrading Wagtail** to higher versions where these packages have official support.

**Date**: 2025-07-27  
**Current State**: Wagtail 3.0, Django 3.2.5  
**Revised Strategy**: Upgrade to Wagtail 5.x/6.x where packages are officially supported

## Research Findings

### ✅ Packages with Newer Versions Available

#### wagtail-birdsong (Newsletter System)
- **Current**: 0.2.0 (disabled)
- **Latest**: 2.0.0 (May 10, 2024)
- **Status**: Actively maintained, supports modern Wagtail
- **Action**: Upgrade Wagtail to compatible version, then use wagtail-birdsong 2.0.0

#### wagtailstreamforms (Form Builder)
- **Current**: 4.0.x (disabled)
- **Latest**: 4.1.0 (Dec 1, 2023)
- **Status**: Very actively maintained (58 releases)
- **Action**: Upgrade Wagtail to compatible version, then use latest wagtailstreamforms

#### wagtailnews (News System)
- **Current**: 2.7.1 (disabled)
- **Latest**: Supports "Wagtail 5.2 and upwards"
- **Status**: Updated for modern Wagtail
- **Action**: Upgrade to Wagtail 5.2+, then re-enable wagtailnews

## Revised Upgrade Path

### Phase 1: Continue Wagtail Upgrades (PRIORITY)
Instead of fixing dependencies for Wagtail 3.0, continue upgrading:

1. **Wagtail 3.0 → 3.1 → 3.2** (incremental)
2. **Wagtail 3.2 → 4.0** (major version)
3. **Wagtail 4.0 → 4.1 → 4.2** (incremental)
4. **Wagtail 4.2 → 5.0** (major version)
5. **Wagtail 5.0 → 5.1 → 5.2** (target for wagtailnews)
6. **Wagtail 5.2 → 6.0** (latest major)

### Phase 2: Django Alignment
Upgrade Django to match Wagtail requirements:
- **Django 3.2.5 → 4.0** (when required by Wagtail 4.x)
- **Django 4.0 → 4.1 → 4.2** (incremental)
- **Django 4.2 → 5.0** (when required by Wagtail 5.x+)

### Phase 3: Re-enable Dependencies
At appropriate Wagtail versions, re-enable packages:

#### At Wagtail 4.x:
- wagtailstreamforms 4.1.0
- Research other packages for 4.x compatibility

#### At Wagtail 5.2+:
- wagtail-birdsong 2.0.0
- wagtailnews (latest)

#### At Wagtail 6.x:
- All remaining packages with latest versions

## Benefits of This Approach

### ✅ Advantages
1. **Official Support**: Use officially maintained packages instead of forks
2. **Latest Features**: Get newest features and security updates
3. **Long-term Stability**: Packages are actively maintained
4. **Less Technical Debt**: No custom forks to maintain
5. **Better Performance**: Newer versions often have performance improvements
6. **Security**: Latest versions have security patches

### ⚠️ Considerations
1. **More Upgrade Steps**: Need to upgrade Wagtail through multiple versions
2. **Testing Required**: Each upgrade step needs thorough testing
3. **Breaking Changes**: May encounter breaking changes in newer Wagtail versions
4. **Time Investment**: More upgrade steps = more time

## Immediate Action Plan

### Step 1: Research Compatibility Matrix
Create a detailed matrix showing which package versions work with which Wagtail versions:

```
Wagtail Version | wagtail-birdsong | wagtailstreamforms | wagtailnews
3.0             | Not compatible  | Research needed    | Not compatible
4.0             | Research needed  | 4.1.0 likely      | Research needed
4.2             | Research needed  | 4.1.0 likely      | Research needed
5.0             | Research needed  | 4.1.0 likely      | Research needed
5.2             | 2.0.0           | 4.1.0 likely      | Latest
6.0             | 2.0.0           | 4.1.0 likely      | Latest
```

### Step 2: Continue Wagtail 3.x Series
- Wagtail 3.0 → 3.1
- Wagtail 3.1 → 3.2
- Test at each step with current working functionality

### Step 3: Research Package Compatibility
For each target Wagtail version, research:
- Which packages have compatible versions
- What breaking changes to expect
- Migration requirements

### Step 4: Plan Re-enablement Points
Identify specific Wagtail versions where we can re-enable each package:
- Create testing checklist for each re-enablement
- Plan rollback procedures

## Current State Management

### Keep Application Functional
While upgrading, maintain current functionality:
- Keep placeholder models for disabled packages
- Maintain current workarounds (CharBlock replacements)
- Ensure no functionality loss during upgrades

### Gradual Re-enablement
As we reach compatible Wagtail versions:
1. Test package compatibility
2. Update requirements
3. Remove workarounds
4. Restore full functionality
5. Test thoroughly

## Success Metrics

### Short-term (Wagtail 4.x)
- [ ] Wagtail 4.2 running successfully
- [ ] wagtailstreamforms re-enabled
- [ ] Form functionality restored
- [ ] No critical functionality lost

### Medium-term (Wagtail 5.x)
- [ ] Wagtail 5.2 running successfully
- [ ] wagtail-birdsong 2.0.0 enabled
- [ ] wagtailnews re-enabled
- [ ] Newsletter functionality restored
- [ ] News system fully functional

### Long-term (Wagtail 6.x)
- [ ] Latest Wagtail version
- [ ] All packages using latest versions
- [ ] No disabled dependencies
- [ ] Full functionality restored
- [ ] Modern, maintainable codebase

## Risk Mitigation

### Backup Strategy
- Database backup before each upgrade step
- Git branches for each upgrade milestone
- Rollback procedures documented

### Testing Strategy
- Comprehensive testing at each Wagtail version
- Functionality verification before proceeding
- User acceptance testing for critical features

### Fallback Options
- If packages still incompatible at higher versions, then consider forking
- Alternative packages as last resort
- Custom implementations only if no other options

## Conclusion

This revised strategy is **more sustainable and future-proof** than trying to fix dependencies for Wagtail 3.0. By continuing the upgrade path, we:

1. **Leverage official package support** instead of creating technical debt
2. **Get modern features and security updates**
3. **Align with the Wagtail ecosystem's direction**
4. **Reduce long-term maintenance burden**

The trade-off is more upgrade steps, but each step is smaller and more manageable than trying to fork and maintain multiple packages.

---

**Next Action**: Research specific package compatibility for Wagtail 4.x and create detailed upgrade timeline.
