---
name: design-system-unification
description: Unifies design tokens, theming, and component styling across the application for consistency and accessibility.
version: "0.1.0"
type: component
requires_hitl: false
cultural_sensitivity: low
tags: [design, ui, theme, consistency, accessibility]
---

# Design System Unification

## Overview
This skill ensures visual and structural consistency across the application by enforcing consistent use of design tokens, color palettes, typography, and component styling. It addresses issues like conflicting design systems, incorrect heading colors, and inconsistent theming between pages.

## When to Use
- When pages or components have inconsistent styling or color schemes.
- When fixing issues with headings, cards, heroes, or overall visual hierarchy.
- When unifying light and dark mode experiences.
- When standardizing brand colors and component appearance across the app.

## Instructions

### 1. Audit Current Design Inconsistencies
- Identify conflicting design systems (e.g. one part of the app using a dark theme while others use light).
- Check for incorrect application of Tailwind tokens (e.g. `text-primary` or `bg-background` not matching the actual theme).
- Look for global CSS rules that override intended component styles (e.g. headings forced to near-white).

### 2. Establish Consistent Design Tokens
- Use the application's defined brand colors (e.g. Indigo as primary, Cyan as secondary).
- Ensure all heroes, CTAs, links, and focus states follow the same color tokens.
- Apply scoped classes (e.g. `.dark-space`) only where intentionally dark experiences are needed (such as the Whanau Hub section).

### 3. Fix Common Issues
- **Heading visibility**: Ensure headings use dark text on light backgrounds and light text only on intentionally dark sections.
- **Component consistency**: Standardize card, button, and form styling across pages.
- **Dark mode handling**: Use `color-scheme: light` or scoped dark classes to prevent half-applied dark mode bugs.

### 4. Accessibility Considerations
- Maintain sufficient color contrast (minimum 4.5:1 for normal text).
- Ensure consistent focus states and interactive element styling.
- Avoid relying solely on color to convey meaning.

### 5. Documentation
- Document the chosen design tokens and when to use scoped dark classes.
- Update component examples to reflect the unified system.

## Guardrails & Constraints
- Do not create new design systems or introduce new brand colors without approval.
- Respect existing design tokens defined in the Tailwind config and globals.
- Avoid forcing dark mode globally unless it is part of the intentional experience (e.g. the Whanau Hub section).

## Input / Output

**Input**: A description of current design inconsistencies or a specific page/component to fix. 
**Output**: A unified, consistent design approach with clear token usage and minimal visual fragmentation.

## Examples

**Before**: Multiple hero sections using different background and text colors (blue, purple, emerald), causing the app to feel like multiple disconnected products.

**After**: All primary surfaces use the same Indigo hero band and Cyan accent, with consistent card and button styling across home, directory, portals, and admin pages.

## References
- Tailwind configuration and design tokens
- Existing component library (shadcn/ui)
- Previous design unification commits in the project history
