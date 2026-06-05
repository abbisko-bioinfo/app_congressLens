# Design Style Guide

本文件仅记录 web app 的视觉风格、色彩搭配、排版、组件外观和自适应布局规则。不包含具体业务内容、页面栏目、文案或信息架构设定。

## 1. Visual Direction

整体风格应保持清晰、专业、克制、现代。界面重点是信息可读性、层级清楚和长期使用的稳定感，避免强装饰、复杂渐变和过度卡片化。

视觉关键词：

- Clean
- Professional
- Scientific
- Trustworthy
- Structured
- Responsive

## 2. Color System

### Primary Colors

| Token | RGB | HEX | Suggested Usage |
| --- | --- | --- | --- |
| `--brand-magenta` | `166, 30, 99` | `#A61E63` | Primary CTA, active highlight, key visual accent |
| `--brand-blue` | `59, 91, 162` | `#3B5BA2` | Headings, navigation active state, main UI structure |

### Accent Colors

| Token | RGB | HEX | Suggested Usage |
| --- | --- | --- | --- |
| `--accent-cyan` | `47, 175, 225` | `#2FAFE1` | Secondary highlight, charts, info states |
| `--accent-rose` | `184, 25, 93` | `#B8195D` | Strong emphasis, selected state, alert accent |
| `--neutral-steel` | `159, 166, 167` | `#9FA6A7` | Borders, muted text, disabled states |
| `--accent-deep-blue` | `31, 113, 178` | `#1F71B2` | Dark button variant, deep background, secondary active state |

### Neutral Colors

| Token | HEX | Suggested Usage |
| --- | --- | --- |
| `--bg-page` | `#F6F8FB` | App/page background |
| `--bg-surface` | `#FFFFFF` | Panels, tables, cards, forms |
| `--bg-muted` | `#EEF3F8` | Subtle section background |
| `--text-primary` | `#172033` | Main text |
| `--text-secondary` | `#5E6A78` | Secondary text |
| `--text-muted` | `#8A94A3` | Hints, captions, metadata |
| `--border-subtle` | `#DDE4EC` | Default border |
| `--border-strong` | `#B9C3D0` | Strong divider |

### Color Ratio

- Use white and light neutral backgrounds for 60% to 70% of the interface.
- Use `--brand-blue` as the main structural color for headings, selected navigation and important UI anchors.
- Use `--brand-magenta` sparingly for primary actions and strongest emphasis.
- Use cyan and deep blue as supporting colors for secondary states, charts and hover feedback.
- Avoid building whole screens from one hue family. The interface should not read as all-blue, all-purple or all-gray.

### State Colors

| Token | HEX | Usage |
| --- | --- | --- |
| `--success` | `#1F9D67` | Success, completed, valid |
| `--warning` | `#D98B1E` | Warning, pending, attention |
| `--danger` | `#C9354D` | Error, destructive, failed |
| `--info` | `#2FAFE1` | Information, neutral notice |

## 3. Typography

### Font Stack

```css
font-family: Inter, "Noto Sans SC", "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
```

Use one shared sans-serif system for the app. Avoid decorative fonts. Avoid using monospace fonts except for code-like identifiers.

### Type Scale

| Token | Desktop | Tablet | Mobile | Usage |
| --- | ---: | ---: | ---: | --- |
| `--font-display` | `48px / 56px` | `40px / 48px` | `32px / 40px` | Large page intro only |
| `--font-h1` | `40px / 48px` | `34px / 42px` | `28px / 36px` | Page title |
| `--font-h2` | `30px / 38px` | `26px / 34px` | `22px / 30px` | Section title |
| `--font-h3` | `22px / 30px` | `21px / 29px` | `20px / 28px` | Panel or card title |
| `--font-body` | `16px / 26px` | `16px / 25px` | `15px / 24px` | Body text |
| `--font-small` | `14px / 22px` | `14px / 22px` | `13px / 20px` | Supporting text |
| `--font-caption` | `12px / 18px` | `12px / 18px` | `12px / 18px` | Captions and compact labels |

### Typography Rules

- Letter spacing should remain `0`.
- Do not scale font size with viewport width.
- Headings should be concise and visually calm.
- Use `--brand-blue` for main headings and `--text-primary` for dense content.
- Use `--brand-magenta` only for selected words, numbers or active emphasis.
- Body text should maintain comfortable line height and never be squeezed into narrow columns.

## 4. Responsive Layout

### Breakpoints

| Token | Width |
| --- | ---: |
| `--bp-mobile` | `< 640px` |
| `--bp-tablet` | `640px - 1023px` |
| `--bp-desktop` | `1024px - 1439px` |
| `--bp-wide` | `>= 1440px` |

### Page Width

| Viewport | Content Width | Horizontal Padding |
| --- | --- | ---: |
| Mobile | `100%` | `20px` |
| Tablet | `100%` | `32px` |
| Desktop | `min(100%, 1200px)` | `40px` |
| Wide | `min(100%, 1360px)` | `64px` |

### Grid

| Viewport | Columns | Gutter |
| --- | ---: | ---: |
| Mobile | 4 | `16px` |
| Tablet | 8 | `20px` |
| Desktop | 12 | `24px` |
| Wide | 12 | `24px` |

### Adaptive Rules

- Layouts should reflow, not shrink unreadably.
- Multi-column content collapses from 4 columns to 2 columns to 1 column.
- Dense tables or fixed-width content may use horizontal scrolling inside their own container.
- Toolbars should wrap into multiple rows or collapse into compact controls on mobile.
- Avoid absolute positioning for primary content.
- Use `minmax()`, `clamp()` for spacing or widths, and container-aware grids where possible.
- All text must remain inside its parent container at every viewport width.

## 5. Spacing

| Token | Value |
| --- | ---: |
| `--space-1` | `4px` |
| `--space-2` | `8px` |
| `--space-3` | `12px` |
| `--space-4` | `16px` |
| `--space-5` | `24px` |
| `--space-6` | `32px` |
| `--space-7` | `48px` |
| `--space-8` | `64px` |
| `--space-9` | `96px` |

Spacing should be consistent and predictable. Use larger spacing between page sections, medium spacing between panels, and compact spacing inside controls.

## 6. Radius, Border, Shadow

### Radius

| Token | Value | Usage |
| --- | ---: | --- |
| `--radius-xs` | `4px` | Small tags, compact controls |
| `--radius-sm` | `6px` | Buttons, inputs |
| `--radius-md` | `8px` | Cards, panels |
| `--radius-pill` | `999px` | Pills, status badges |

Cards and panels should not exceed `8px` radius unless a specific component requires a pill shape.

### Border

- Default border: `1px solid var(--border-subtle)`
- Strong divider: `1px solid var(--border-strong)`
- Focus border: `1px solid var(--brand-blue)`

### Shadow

Use shadows sparingly.

```css
--shadow-soft: 0 10px 30px rgba(23, 32, 51, 0.08);
--shadow-popover: 0 16px 40px rgba(23, 32, 51, 0.14);
```

## 7. Components

### Buttons

| Type | Background | Text | Border |
| --- | --- | --- | --- |
| Primary | `--brand-magenta` | `#FFFFFF` | none |
| Secondary | `--brand-blue` | `#FFFFFF` | none |
| Outline | transparent | `--brand-blue` | `--border-strong` |
| Ghost | transparent | `--text-secondary` | transparent |

Button sizes:

| Size | Height | Padding | Font |
| --- | ---: | --- | --- |
| Small | `32px` | `0 12px` | `13px` |
| Medium | `40px` | `0 16px` | `14px` |
| Large | `48px` | `0 20px` | `16px` |

Rules:

- Buttons should have `6px` radius.
- Icon-only buttons should use square dimensions.
- Button text should not wrap unless the button spans full width on mobile.
- Primary buttons should be limited to one or two per view.

### Inputs

| Element | Height | Radius | Border |
| --- | ---: | ---: | --- |
| Text input | `44px` | `6px` | `--border-subtle` |
| Select | `44px` | `6px` | `--border-subtle` |
| Textarea | `min-height: 96px` | `6px` | `--border-subtle` |

Input states:

- Default: white background, subtle border.
- Hover: slightly stronger border.
- Focus: brand-blue border and cyan focus ring.
- Disabled: muted background and muted text.
- Error: danger border and concise helper text.

### Cards

Cards are for repeated items or compact grouped information. Avoid nesting cards inside cards.

Card style:

- Background: `--bg-surface`
- Border: `1px solid var(--border-subtle)`
- Radius: `8px`
- Padding: `20px` to `24px`
- Hover: optional soft shadow and `translateY(-2px)`

### Tables

Table style:

- Header background: `--bg-muted`
- Header text: `--brand-blue`
- Body background: `--bg-surface`
- Row height: `56px` to `64px`
- Row divider: `--border-subtle`
- Hover background: `#F6F8FB`

Responsive tables:

- On desktop, show full columns when space allows.
- On tablet and mobile, allow horizontal scroll or convert rows into stacked cards.
- Sticky headers may be used for long tables.

### Tabs

Tabs should be compact and scan-friendly.

- Active text: `--brand-blue`
- Active indicator: `2px solid var(--brand-magenta)`
- Inactive text: `--text-secondary`
- Hover text: `--brand-blue`

### Badges

Badge style:

- Height: `24px` to `28px`
- Radius: `999px`
- Padding: `0 10px`
- Font size: `12px`
- Default background: `#EEF3F8`
- Default text: `--brand-blue`

Use filled magenta or blue badges only for strong emphasis.

### Navigation

Navigation should feel stable and understated.

- Top navigation height: `64px` to `72px`
- Sidebar width: `220px` to `260px`
- Active item: brand-blue text with subtle tinted background
- Hover item: light muted background
- Mobile navigation: drawer, sheet or compact menu

## 8. Interaction States

### Hover

- Links: `--brand-blue` to `--brand-magenta`
- Cards: optional `translateY(-2px)` and `--shadow-soft`
- Table rows: `#F6F8FB`
- Buttons: slightly darker or more saturated background

### Focus

All interactive elements must have visible focus.

```css
box-shadow: 0 0 0 3px rgba(47, 175, 225, 0.24);
```

### Disabled

- Background: `#EEF3F8`
- Text: `--text-muted`
- Border: `--border-subtle`
- Cursor: `not-allowed`

### Loading

- Use skeleton blocks for content regions.
- Use spinner only for small inline waits.
- Avoid strong animation loops.

## 9. Data Visualization Style

### Chart Palette

1. `#3B5BA2`
2. `#A61E63`
3. `#2FAFE1`
4. `#1F71B2`
5. `#9FA6A7`
6. `#B8195D`

### Chart Rules

- Chart backgrounds should be white or transparent.
- Grid lines should use `#E7EDF4`.
- Axis labels should use `--text-muted`.
- Legends should be visible and compact.
- Do not rely on color alone; use labels, patterns or position when needed.
- Avoid glossy gradients and 3D chart effects.

## 10. Imagery And Surfaces

Images should be sharp, bright and relevant to the product context. Avoid dark, blurry or purely decorative images.

Surface rules:

- Use full-width background bands for major page sections.
- Use cards only for individual repeated items, tools, popovers or modals.
- Do not place UI cards inside larger decorative cards.
- Avoid decorative blobs, random gradients or abstract ornaments.

## 11. CSS Token Example

```css
:root {
  --brand-magenta: #A61E63;
  --brand-blue: #3B5BA2;
  --accent-cyan: #2FAFE1;
  --accent-rose: #B8195D;
  --neutral-steel: #9FA6A7;
  --accent-deep-blue: #1F71B2;

  --success: #1F9D67;
  --warning: #D98B1E;
  --danger: #C9354D;
  --info: #2FAFE1;

  --bg-page: #F6F8FB;
  --bg-surface: #FFFFFF;
  --bg-muted: #EEF3F8;

  --text-primary: #172033;
  --text-secondary: #5E6A78;
  --text-muted: #8A94A3;

  --border-subtle: #DDE4EC;
  --border-strong: #B9C3D0;

  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-pill: 999px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --space-6: 32px;
  --space-7: 48px;
  --space-8: 64px;
  --space-9: 96px;

  --shadow-soft: 0 10px 30px rgba(23, 32, 51, 0.08);
  --shadow-popover: 0 16px 40px rgba(23, 32, 51, 0.14);
}
```

## 12. Implementation Checklist

- Layout adapts cleanly across mobile, tablet, desktop and wide screens.
- Text never overflows buttons, cards, tabs or table cells.
- Primary color usage is restrained and consistent.
- Magenta is reserved for the strongest emphasis and primary actions.
- Components include hover, focus, disabled and loading states.
- Tables and dense content remain readable on small screens.
- Cards are not nested inside other cards.
- Images and visual surfaces support the interface instead of overpowering it.
