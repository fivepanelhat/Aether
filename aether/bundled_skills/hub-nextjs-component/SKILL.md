---
name: hub-nextjs-component
description: Use when building or modifying UI components for the Whanau Preterm Support Hub. Provides production-ready patterns for accessible shadcn/ui + Tailwind components, WCAG 2.2 AA compliance, mobile-first design, Te Tiriti-aligned considerations, and proper handling of health-related disclaimers.
version: "0.2.0"
type: component
requires_hitl: false
cultural_sensitivity: medium
---

# Hub Next.js Component Authoring

This skill encodes the standards and patterns for creating high-quality, accessible, and culturally considerate UI components for the Whanau Preterm Support Hub NZ.

## Overview

Provides production-ready patterns for building components using Next.js 15, TypeScript, Tailwind, and shadcn/ui / Radix primitives, with strong emphasis on accessibility (WCAG 2.2 AA), mobile-first design, and cultural safety.

## When to Use

- Creating new pages, cards, forms, modals, or interactive elements for the Hub.
- Refactoring or improving existing UI components.
- Ensuring consistency with accessibility and cultural standards across the application.

## Instructions

### Core Requirements

- Use **Next.js 15 App Router** + **TypeScript** + **Tailwind** + **shadcn/ui**.
- Achieve **WCAG 2.2 AA** compliance by default.
- Be **mobile-first** and responsive.
- Include clear **disclaimers** when the component surfaces health, funding, or support-related information.
- Be easy for cultural reviewers to understand and extend.

### Component Structure

Follow this general structure:

```tsx
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ResourceCardProps {
 title: string;
 description: string;
 category: string;
}

export function ResourceCard({ title, description, category }: ResourceCardProps) {
 return (
 <Card>
 <CardHeader>
 <CardTitle>{title}</CardTitle>
 </CardHeader>
 <CardContent>
 <p>{description}</p>
 </CardContent>
 </Card>
 );
}
```
