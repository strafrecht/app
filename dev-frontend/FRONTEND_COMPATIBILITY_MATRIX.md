# Frontend Compatibility Matrix

## Overview
This document tracks compatibility requirements and upgrade paths for all frontend dependencies in the Strafrecht Online project.

**Last Updated**: 2025-07-27  
**Current State**: Pre-upgrade analysis  
**Target**: Modern, secure, and maintainable frontend stack

## Node.js Compatibility Requirements

| Package | Current Version | Node.js Requirement | Latest Version | Node.js Requirement | Upgrade Priority |
|---------|----------------|---------------------|----------------|---------------------|------------------|
| webpack | 5.36.1 | >=10.13.0 | 5.95.0 | >=10.13.0 | HIGH |
| vue | 2.6.12 | >=8.9.0 | 3.5.13 | >=16.0.0 | CRITICAL |
| @babel/core | 7.13.16 | >=6.9.0 | 7.26.0 | >=6.9.0 | HIGH |
| eslint | 6.7.2 | >=6.14.0 | 9.17.0 | >=18.18.0 | HIGH |

**Recommended Node.js Version**: 18.20.5 LTS or 20.18.1 LTS

## Core Framework Compatibility

### Vue.js Ecosystem
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| vue | 2.6.12 | 3.5.13 | MAJOR | HIGH | Complete rewrite required |
| vue-loader | 15.9.6 | 17.4.2 | MAJOR | HIGH | Vue 3 compatibility |
| vue-template-compiler | 2.6.11 | N/A | REMOVED | HIGH | Replaced by @vue/compiler-sfc |
| vuetify | 2.4.7 | 3.7.4 | MAJOR | HIGH | Complete UI redesign |
| vue-select | 3.20.0 | 4.0.0-beta.6 | MAJOR | MEDIUM | API changes |
| @riophae/vue-treeselect | 0.4.0 | 0.4.0 | NONE | LOW | No updates available |

### Build Tools
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| webpack | 5.36.1 | 5.95.0 | MINOR | LOW | Incremental updates |
| webpack-cli | 4.6.0 | 5.1.4 | MAJOR | MEDIUM | Command changes |
| webpack-dev-server | 3.11.2 | 5.1.0 | MAJOR | MEDIUM | Configuration changes |
| webpack-merge | 5.7.3 | 6.0.1 | MAJOR | LOW | API simplification |

### CSS & Styling
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| node-sass | 5.0.0 | DEPRECATED | N/A | MEDIUM | Replace with sass |
| sass | N/A | 1.82.0 | N/A | MEDIUM | Dart Sass replacement |
| sass-loader | 10.1.1 | 16.0.3 | MAJOR | MEDIUM | Webpack 5 compatibility |
| css-loader | 5.2.4 | 7.1.2 | MAJOR | MEDIUM | Asset modules |
| postcss-loader | 4.2.0 | 8.1.1 | MAJOR | MEDIUM | PostCSS 8 compatibility |
| mini-css-extract-plugin | 1.5.1 | 2.9.2 | MAJOR | MEDIUM | Webpack 5 optimizations |

## UI Framework Compatibility

### Bootstrap Ecosystem
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| bootstrap | 4.6.0 | 5.3.3 | MAJOR | HIGH | jQuery removal, utility changes |
| bootstrap-icons | 1.9.1 | 1.11.3 | MINOR | LOW | Icon additions |

### Icon & Font Libraries
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| @fortawesome/fontawesome-free | 5.15.4 | 6.7.2 | MAJOR | MEDIUM | Icon name changes |
| @mdi/font | 4.3.95 | 7.4.47 | MINOR | LOW | Icon additions |
| @fontsource/* | Various | Latest | MINOR | LOW | Font loading updates |

## Development Tools Compatibility

### Linting & Code Quality
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| eslint | 6.7.2 | 9.17.0 | MAJOR | HIGH | Config format changes |
| babel-eslint | 10.0.3 | DEPRECATED | N/A | MEDIUM | Replace with @babel/eslint-parser |
| @babel/eslint-parser | N/A | 7.26.0 | N/A | MEDIUM | Modern ESLint integration |
| eslint-plugin-vue | 6.0.1 | 9.31.0 | MAJOR | HIGH | Vue 3 compatibility |
| stylelint | 13.13.0 | 16.12.0 | MAJOR | MEDIUM | Config format changes |

### Babel Ecosystem
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| @babel/core | 7.13.16 | 7.26.0 | MINOR | LOW | Incremental updates |
| @babel/preset-env | 7.13.15 | 7.26.0 | MINOR | LOW | Browser target updates |
| babel-loader | 8.2.2 | 9.2.1 | MAJOR | MEDIUM | Webpack 5 compatibility |

## Utility Libraries Compatibility

### Date & Time
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| moment | 2.29.1 | DEPRECATED | N/A | HIGH | Replace with day.js or date-fns |
| dayjs | N/A | 1.11.13 | N/A | HIGH | Moment.js replacement |

### HTTP & API
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| axios | 1.1.3 | 1.7.9 | MINOR | LOW | Security updates |

### Charts & Visualization
| Package | Current | Latest | Breaking Changes | Migration Effort | Notes |
|---------|---------|--------|------------------|------------------|-------|
| chartist | 0.11.4 | 1.3.0 | MAJOR | HIGH | API redesign |
| chartist-plugin-fill-donut | 0.1.4 | 0.1.4 | NONE | LOW | No updates |

## Upgrade Roadmap by Priority

### Phase 1: Critical Security & Foundation (Week 1-2)
**Priority**: CRITICAL
- [ ] Node.js version pinning (.nvmrc)
- [ ] npm audit fix (security vulnerabilities)
- [ ] ESLint 6 → 8+ (security updates)
- [ ] Babel ESLint → @babel/eslint-parser
- [ ] Node Sass → Dart Sass

### Phase 2: Build Tools Modernization (Week 3-4)
**Priority**: HIGH
- [ ] Webpack 5.36.1 → 5.95.0
- [ ] Webpack CLI 4 → 5
- [ ] Webpack Dev Server 3 → 5
- [ ] CSS Loader updates
- [ ] PostCSS Loader updates

### Phase 3: Framework Preparation (Week 5-6)
**Priority**: HIGH
- [ ] Vue 2.6.12 → 2.7.x (Composition API backport)
- [ ] Vue component audit for Vue 3 compatibility
- [ ] Bootstrap 4 → 5 migration
- [ ] Moment.js → Day.js migration

### Phase 4: Major Framework Migration (Week 7-10)
**Priority**: CRITICAL
- [ ] Vue 2.7 → 3.5.x
- [ ] Vue Loader 15 → 17
- [ ] Vuetify 2 → 3
- [ ] Vue component rewrite
- [ ] Template syntax updates

### Phase 5: Optimization & Cleanup (Week 11-12)
**Priority**: MEDIUM
- [ ] Bundle analysis and optimization
- [ ] Unused dependency removal
- [ ] Performance testing
- [ ] Documentation updates

## Compatibility Testing Matrix

### Browser Support Requirements
| Browser | Minimum Version | Current Support | Post-Upgrade Support |
|---------|----------------|-----------------|---------------------|
| Chrome | 70+ | ✅ | ✅ |
| Firefox | 65+ | ✅ | ✅ |
| Safari | 12+ | ✅ | ✅ |
| Edge | 79+ | ✅ | ✅ |
| IE 11 | N/A | ❌ | ❌ |

### Node.js Support Matrix
| Node.js Version | Current Compatibility | Post-Upgrade Compatibility |
|----------------|----------------------|---------------------------|
| 14.x | ✅ | ❌ (EOL) |
| 16.x | ✅ | ⚠️ (Maintenance) |
| 18.x | ✅ | ✅ (Recommended) |
| 20.x | ✅ | ✅ (Latest LTS) |
| 22.x | ⚠️ | ✅ (Current) |

## Risk Assessment

### High Risk Dependencies
1. **Vue.js 2 → 3**: Complete component rewrite required
2. **Vuetify 2 → 3**: UI framework breaking changes
3. **Bootstrap 4 → 5**: jQuery removal, utility class changes
4. **ESLint 6 → 9**: Configuration format changes

### Medium Risk Dependencies
1. **Webpack ecosystem**: Build configuration updates
2. **Sass migration**: Node Sass → Dart Sass
3. **Moment.js replacement**: Date handling changes

### Low Risk Dependencies
1. **Font packages**: Generally backward compatible
2. **Axios updates**: Minor API changes
3. **Icon libraries**: Additive changes

## Rollback Compatibility

### Rollback Points
1. **Pre-upgrade state**: Current working configuration
2. **Post-Phase 1**: Security updates applied
3. **Post-Phase 2**: Build tools updated
4. **Post-Phase 3**: Framework preparation complete

### Rollback Requirements
- Git tags for each phase
- Package-lock.json backups
- Build artifact backups
- Database state documentation (if applicable)

---

**Next Review**: After each upgrade phase  
**Escalation Path**: Backend team for integration issues  
**Testing Requirements**: Full regression testing after each phase
