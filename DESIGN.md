---
name: Premium Digital Butler
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bccbb9'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#869585'
  outline-variant: '#3d4a3d'
  surface-tint: '#4ae176'
  primary: '#4be277'
  on-primary: '#003915'
  primary-container: '#22c55e'
  on-primary-container: '#004b1e'
  inverse-primary: '#006e2f'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#ffba61'
  on-tertiary: '#472a00'
  tertiary-container: '#ef9900'
  on-tertiary-container: '#5c3800'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6bff8f'
  primary-fixed-dim: '#4ae176'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#005321'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Hanken Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Hanken Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  headline-md-mobile:
    fontFamily: Hanken Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding: 24px
  gutter: 16px
  stack-sm: 12px
  stack-md: 24px
  max-width: 1200px
---

## Brand & Style
The design system embodies the persona of a high-end digital butler: efficient, sophisticated, and always ready to serve. It leverages a **Premium Dark** aesthetic, combining deep, ink-like charcoals with royal accents to evoke a sense of exclusivity and reliability.

The personality is "Attentive Professionalism." It avoids the coldness of typical utility apps by using soft shapes and organic depth, ensuring the user feels their media library is being curated by a personal assistant rather than just a script. The visual language is a blend of **Minimalism** and **Modern Corporate**, focusing on extreme clarity, high-quality typography, and a refined sense of order.

## Colors
The palette is built on a foundation of "Midnight Navy" and "Obsidian" to provide a more luxurious depth than pure black.

- **Primary (Vibrant Green):** Reserved for "Active" and "Connected" states, signaling health and motion.
- **Secondary (Royal Purple):** Used for primary actions and brand highlights, nodding to the "Prince" butler theme.
- **Tertiary (Gold):** Used sparingly for premium features or "Completed" success states.
- **Neutral (Slate):** Various shades of slate and charcoal define the structural hierarchy, ensuring a low-strain experience during late-night usage.

## Typography
The typography system uses **Hanken Grotesk** for a sharp, contemporary display feel and **Inter** for maximum legibility in data-dense lists. 

**JetBrains Mono** is introduced for status labels and technical metadata (file sizes, speeds, percentages) to provide a "precise" technical feel that contrasts beautifully with the rounded brand fonts. All headings use a tighter letter-spacing to maintain a sophisticated, editorial look.

## Layout & Spacing
This design system utilizes a **Fixed Grid** approach for the central content area on desktop to maintain the "organized butler" aesthetic.

- **Desktop:** 12-column grid, 1200px max-width, 24px gutters.
- **Tablet:** 8-column grid, fluid margins.
- **Mobile:** 4-column grid, 16px margins.

The vertical rhythm is strictly 8px-based. Card content should use generous internal padding (24px) to ensure the UI feels "premium" and uncrowded. Media lists are stacked with 12px gaps to balance density with scannability.

## Elevation & Depth
Depth is created through **Tonal Layers** rather than heavy shadows. The background is the darkest layer (`#020617`), with cards and containers using a slightly lighter surface (`#1E293B`).

For interactive elements, use **Ambient Shadows**:
- **Resting:** No shadow, thin 1px border (`#334155`).
- **Hover/Active:** A soft, 12px blur shadow tinted with the primary or secondary color at 15% opacity to create a subtle "glow" effect, suggesting the element is powered on.
- **Glassmorphism:** Use a 20px backdrop blur on top-level navigation bars and modal overlays to maintain a sense of space.

## Shapes
The shape language is "Friendly Professional." Everything uses a standard **0.5rem (8px)** corner radius for standard cards and inputs. Larger containers or hero sections may use **1rem (16px)** to emphasize the "soft" nature of the personal assistant persona. Buttons and progress indicators should use fully rounded (pill-shaped) caps to differentiate them from the structural containers.

## Components

### Buttons
- **Primary:** Royal purple background, white text, pill-shaped. On hover, apply a subtle violet glow.
- **Secondary/Ghost:** 1px border in slate-400, no background.

### Progress Indicators
- **Track:** Deep slate (`#0F172A`) with a subtle inner shadow.
- **Fill:** Gradient from Primary Green to a slightly lighter mint green. 
- **Animation:** A subtle "shimmer" effect moving across the fill color while a download is active.

### Cards (Media Items)
- Each download is housed in a card with a 1px border.
- Include a high-contrast icon (Video/Music) in the top left using the secondary purple color.
- Status badges (e.g., "Downloading") use pill shapes with 10% opacity backgrounds of their respective status color.

### Input Fields
- Dark backgrounds (`#0F172A`) with focus states that transition the border color to the secondary purple.
- Use mono-fonts for URL inputs to help users spot errors in links.

### Media Icons
- Use thick-stroke (2px) custom icons for Video, Music, and Archive types. Icons should be encased in a soft-rounded square with a subtle gradient background.