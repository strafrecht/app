# Frontend Upgrade Log

## Project Overview
- **Project**: Strafrecht Online Frontend (Webpack + Vue.js Application)
- **Current State**: Webpack 5.36.1, Vue.js 2.6.12, Node.js dependencies from 2021-2022
- **Target State**: Latest stable versions with modern tooling
- **Upgrade Start Date**: 2025-07-27
- **Upgrade Strategy**: Systematic incremental upgrades aligned with backend modernization

## Current Frontend Technology Stack Analysis

### Core Build Tools
- **Webpack**: 5.36.1 (Released: April 2021)
- **Webpack CLI**: 4.6.0 (April 2021)
- **Webpack Dev Server**: 3.11.2 (March 2021)
- **Webpack Merge**: 5.7.3 (March 2021)

### JavaScript Framework & Runtime
- **Vue.js**: 2.6.12 (October 2020) - **MAJOR VERSION BEHIND** (Vue 3.x is current)
- **Vue Loader**: 15.9.6 (February 2021)
- **Vue Template Compiler**: 2.6.11 (March 2020)
- **Babel Core**: 7.13.16 (April 2021)
- **Node.js**: Version not pinned (needs analysis)

### CSS & Styling
- **Sass Loader**: 10.1.1 (February 2021)
- **Node Sass**: 5.0.0 (October 2020) - **DEPRECATED** (should use Dart Sass)
- **CSS Loader**: 5.2.4 (April 2021)
- **PostCSS Loader**: 4.2.0 (April 2021)
- **Mini CSS Extract Plugin**: 1.5.1 (April 2021)

### UI Framework & Components
- **Vuetify**: 2.4.7 (March 2021) - **MAJOR VERSION BEHIND** (Vuetify 3.x is current)
- **Bootstrap**: 4.6.0 (February 2021) - **MAJOR VERSION BEHIND** (Bootstrap 5.x is current)
- **Vue Select**: 3.20.0 (February 2022)
- **Vue Treeselect**: 0.4.0 (October 2020)

### Development Tools & Linting
- **ESLint**: 6.7.2 (November 2019) - **SEVERELY OUTDATED**
- **Stylelint**: 13.13.0 (April 2021)
- **Babel ESLint**: 10.0.3 (December 2019) - **DEPRECATED**

### Key Dependencies Analysis
- **Axios**: 1.1.3 (October 2022) - Relatively recent
- **jQuery**: 3.6.0 (March 2021) - Should consider removal in favor of modern approaches
- **Moment.js**: 2.29.1 (January 2021) - **DEPRECATED** (should migrate to Day.js or date-fns)
- **Chart.js (Chartist)**: 0.11.4 (May 2018) - **VERY OUTDATED**

## Critical Upgrade Requirements

### 1. Vue.js 2 → 3 Migration (MAJOR BREAKING CHANGE)
- **Impact**: Complete rewrite of Vue components required
- **Breaking Changes**: Composition API, new reactivity system, template syntax changes
- **Components Affected**: 
  - `frontend/src/scripts/vue/flashcards/Deck.vue`
  - `frontend/src/scripts/vue/casetraining/Case.vue`
  - All Vue components in unused/ directory
- **Vuetify Migration**: Requires Vuetify 2 → 3 migration alongside Vue upgrade

### 2. Webpack 5 → 6 Migration
- **Current**: Webpack 5.36.1 (April 2021)
- **Target**: Latest Webpack 6.x (when stable) or latest 5.x
- **Breaking Changes**: Module federation updates, asset modules changes

### 3. Node.js Version Management
- **Current**: No version pinning detected
- **Required**: Establish Node.js version requirements (.nvmrc file)
- **Recommendation**: Node.js 18 LTS or 20 LTS for modern tooling support

### 4. Deprecated Dependencies Replacement
- **Node Sass → Dart Sass**: Critical for future compatibility
- **Moment.js → Day.js**: Performance and bundle size improvements
- **Babel ESLint → @babel/eslint-parser**: Modern ESLint integration
- **ESLint 6 → 8+**: Security and feature updates

## Frontend-Backend Integration Points

### 1. Django Static Files Integration
- **Location**: Django settings.py STATICFILES configuration
- **Webpack Output**: `frontend/build/` directory
- **Integration**: Django collectstatic process
- **Risk Level**: Medium - Changes to webpack output structure could break Django integration

### 2. Wagtail Admin Interface Integration
- **Vue Components**: Embedded in Wagtail admin pages
- **Global Variables**: Vue components exposed via `global.DeckApp`, `global.CaseApp`
- **Risk Level**: High - Wagtail 6.x admin interface changes may conflict with Vue components

### 3. API Endpoints
- **Axios Configuration**: Frontend API calls to Django REST endpoints
- **CSRF Integration**: Django CSRF token handling in Vue components
- **Risk Level**: Medium - API structure changes could break frontend functionality

### 4. Asset Management
- **Fonts**: @fontsource packages for typography
- **Icons**: FontAwesome, Bootstrap Icons, MDI integration
- **Images**: Static asset handling through webpack file-loader
- **Risk Level**: Low - Asset handling is generally stable

## Upgrade Risk Assessment

### High Risk Areas
1. **Vue 2 → 3 Migration**: Complete component rewrite required
2. **Vuetify 2 → 3 Migration**: UI framework breaking changes
3. **Webpack Configuration**: Build process modifications
4. **ESLint Configuration**: Linting rule updates and parser changes

### Medium Risk Areas
1. **CSS Processing**: Sass/PostCSS loader updates
2. **Asset Loading**: File loader and asset module changes
3. **Development Server**: Webpack dev server configuration updates

### Low Risk Areas
1. **Package Updates**: Minor version bumps for stable packages
2. **Font Loading**: @fontsource package updates
3. **Utility Libraries**: Axios, utility function updates

## Recommended Upgrade Strategy

### Phase 1: Foundation Stabilization (Weeks 1-2)
1. **Node.js Version Pinning**: Create .nvmrc file, establish Node 18 LTS
2. **Package Audit**: Run npm audit and fix security vulnerabilities
3. **Webpack 5 Latest**: Update to latest Webpack 5.x (avoid 6.x initially)
4. **Development Tools**: Update ESLint, Stylelint, Babel to latest compatible versions

### Phase 2: Dependency Modernization (Weeks 3-4)
1. **Sass Migration**: Node Sass → Dart Sass
2. **Moment.js Replacement**: Migrate to Day.js
3. **Bootstrap 4 → 5**: Update Bootstrap with breaking change analysis
4. **Chart Library**: Evaluate Chartist replacement (Chart.js, D3.js alternatives)

### Phase 3: Vue.js Ecosystem Upgrade (Weeks 5-8)
1. **Vue 2.7**: Intermediate upgrade to Vue 2.7 (Composition API backport)
2. **Component Analysis**: Audit all Vue components for Vue 3 compatibility
3. **Vuetify Planning**: Research Vuetify 2 → 3 migration requirements
4. **Testing Setup**: Establish Vue component testing framework

### Phase 4: Major Framework Migration (Weeks 9-12)
1. **Vue 3 Migration**: Systematic component-by-component migration
2. **Vuetify 3 Migration**: UI framework upgrade with design system updates
3. **Integration Testing**: Comprehensive frontend-backend integration validation
4. **Performance Optimization**: Bundle analysis and optimization

## Success Criteria

### Technical Metrics
- [ ] All frontend builds complete without errors
- [ ] Vue components render correctly in Wagtail admin
- [ ] Frontend-backend API integration functional
- [ ] Static file collection works with Django
- [ ] Development server starts and hot-reloads properly
- [ ] Production builds generate optimized assets

### Performance Metrics
- [ ] Bundle size maintained or reduced
- [ ] Page load times improved or maintained
- [ ] Development build times acceptable (<30 seconds)
- [ ] Hot reload performance maintained

### Code Quality Metrics
- [ ] ESLint passes with zero errors
- [ ] Stylelint passes with zero errors
- [ ] No deprecated dependency warnings
- [ ] TypeScript integration (future consideration)

## Emergency Rollback Procedures

### Immediate Rollback Triggers
- Frontend build failures preventing deployment
- Vue components not rendering in production
- Django static file collection failures
- Critical functionality broken (flashcards, case training)

### Rollback Steps
1. **Git Revert**: Return to last known working commit
2. **Node Modules**: Clear and reinstall from package-lock.json
3. **Django Collectstatic**: Re-run static file collection
4. **Cache Clear**: Clear browser and CDN caches
5. **Verification**: Test critical user journeys

## Next Steps

1. **Create Node.js Version File**: Establish .nvmrc for version consistency
2. **Security Audit**: Run npm audit and address vulnerabilities
3. **Backup Current State**: Create git tag for current working state
4. **Development Environment**: Set up isolated frontend development environment
5. **Testing Framework**: Establish Vue component testing capabilities

---

**Last Updated**: 2025-07-27  
**Next Review**: Weekly during upgrade process  
**Responsible**: Frontend Development Team  
**Escalation**: Backend team for integration issues
