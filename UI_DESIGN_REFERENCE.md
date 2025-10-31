# Analysis UI Design Reference

## Two-Column Layout with Monochromatic Dark Theme

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYSIS CONTAINER                           │
├──────────────────────────────┬──────────────────────────────────┤
│  LEFT COLUMN (50%)           │  RIGHT COLUMN (50%)              │
│  ┌────────────────────────┐  │  ┌────────────────────────────┐ │
│  │  📸 Component Analysis │  │  │  🔍 Component Identification│ │
│  ├────────────────────────┤  │  ├────────────────────────────┤ │
│  │                        │  │  │  ✅ CONFIRMED COMPONENTS   │ │
│  │   [Annotated Image]    │  │  │  ┌──────────────────────┐ │ │
│  │                        │  │  │  │ ✓ Battery            │ │ │
│  │                        │  │  │  │   Confirmed.         │ │ │
│  │                        │  │  │  └──────────────────────┘ │ │
│  │                        │  │  │  ┌──────────────────────┐ │ │
│  │                        │  │  │  │ ✓ Fan                │ │ │
│  │                        │  │  │  │   Confirmed.         │ │ │
│  └────────────────────────┘  │  │  └──────────────────────┘ │ │
│                               │  │                            │ │
│                               │  │  ⚠️ NOT VISIBLE/OBSCURED  │ │
│                               │  │  ┌──────────────────────┐ │ │
│                               │  │  │ ◯ CMOS Battery       │ │ │
│                               │  │  │   Not visible        │ │ │
│                               │  │  └──────────────────────┘ │ │
│                               │  └────────────────────────────┘ │
│                               │  ┌────────────────────────────┐ │
│                               │  │  📄 View Raw Analysis ▼    │ │
│                               │  └────────────────────────────┘ │
└──────────────────────────────┴──────────────────────────────────┘
```

### Color Scheme - Monochromatic Dark Shades

#### Base Colors
- **Background**: `#1a1a1a` to `#252525` (gradient)
- **Cards**: `linear-gradient(145deg, #1a1a1a, #252525)`
- **Borders**: `#333333`, `#404040`
- **Text Primary**: `#e0e0e0`, `#f0f0f0`
- **Text Secondary**: `#999999`, `#aaa`

#### Component-Specific Tints
1. **Confirmed Components** (Green Tint)
   - Background: `linear-gradient(135deg, #1a2a1a, #1f2f1f)`
   - Border: `#4CAF50`
   - Icon Color: `#4CAF50`

2. **Not Visible/Obscured** (Orange Tint)
   - Background: `linear-gradient(135deg, #2a2218, #2f271d)`
   - Border: `#FF9800`
   - Icon Color: `#FF9800`

3. **Notes/Additional** (Blue Tint)
   - Background: `linear-gradient(135deg, #1a1f2a, #1f242f)`
   - Border: `#2196F3`
   - Icon Color: `#2196F3`

### Component Parsing Logic

#### Input Format (from LLM)
```markdown
**1. Component Identification Confirmation:**

*   **Battery:** Confirmed.
*   **Fan:** Confirmed.
*   **Heat Pipe:** Likely present, though obscured by the fan.
*   **CMOS Battery:** Not explicitly visible in the image.
```

#### Parsed Output Structure
```typescript
{
  confirmed: [
    { name: "Battery", status: "Confirmed." },
    { name: "Fan", status: "Confirmed." }
  ],
  notVisible: [
    { name: "Heat Pipe", status: "Likely present, though obscured by the fan." },
    { name: "CMOS Battery", status: "Not explicitly visible in the image." }
  ],
  notes: []
}
```

### UI Elements

#### 1. Dark Card
- Rounded corners: `12px`
- Padding: `24px`
- Box shadow: Multiple layers for depth
- Inset highlight: `rgba(255, 255, 255, 0.05)`

#### 2. Card Title
- Font size: `18px`
- Font weight: `600`
- Color: `#e0e0e0`
- Bottom border: `2px solid #404040`
- Letter spacing: `0.5px`

#### 3. Section Header
- Font size: `13px`
- Font weight: `600`
- Color: `#b0b0b0`
- Text transform: `uppercase`
- Letter spacing: `1px`

#### 4. Component Item
- Display: `flex`
- Padding: `14px 16px`
- Border radius: `8px`
- Left border: `3px` (color varies by type)
- Hover effect: `translateX(4px)` + slight background

#### 5. Component Icon
- Size: `32px × 32px`
- Font size: `18px`
- Symbols:
  - Confirmed: `✓` (check mark)
  - Not Visible: `◯` (circle)
  - Notes: `•` (bullet)

#### 6. Component Name
- Font size: `15px`
- Font weight: `600`
- Color: `#f0f0f0`
- Letter spacing: `0.3px`

#### 7. Component Status
- Font size: `13px`
- Color: `#999`
- Font style: `italic`
- Line height: `1.5`

### Responsive Design

```css
@media (max-width: 1024px) {
  .analysis-grid {
    grid-template-columns: 1fr; /* Stack vertically on tablets */
  }
}
```

### Dark Theme Scrollbar
- Width: `8px`
- Track: `#1a1a1a`
- Thumb: `#404040` (hover: `#505050`)

### Raw Analysis Toggle
- Collapsible `<details>` element
- Summary text: `#888` (hover: `#b0b0b0`)
- Content background: `#0a0a0a`
- Border: `1px solid #2a2a2a`
- Monospace font for raw text

## Visual Hierarchy

1. **Primary Focus**: Left column image (visual evidence)
2. **Secondary Focus**: Confirmed components (green section)
3. **Tertiary Focus**: Not visible/obscured (orange section)
4. **Reference**: Raw analysis (collapsed by default)

## Accessibility Features

- High contrast text on dark backgrounds
- Color-coded categories with both color AND icons
- Hover effects for interactive elements
- Smooth transitions (0.2s ease)
- Readable font sizes (13px minimum)

## Example Usage

### User uploads laptop internals image
1. **Left Column** shows annotated image with component overlay
2. **Right Column** shows:
   - ✅ **Confirmed**: Battery, Fan, Motherboard, SSD, SSD Shielding
   - ⚠️ **Not Visible**: Heat Pipe (obscured), CMOS Battery (not visible)
3. **Raw Analysis** available in collapsed section

### Benefits
✅ Clean, organized presentation
✅ Easy to scan confirmed vs. not visible
✅ Dark theme reduces eye strain
✅ Two-column layout maximizes screen space
✅ Color-coded categories for quick recognition
✅ Hover effects provide interactivity
✅ Responsive design works on all screens
