---
name: bounce-easing
description: Generate CSS bounce easing function using the motion MCP server for lively, playful animations
arguments:
  - name: duration
    description: Animation duration in seconds (0.5-2.0, default 1.0)
    required: false
  - name: context
    description: Animation context (dropdown, modal, toast, button, card, general)
    required: false
    default: general
---

Generate a CSS bounce easing function using the motion MCP server.

## How It Works

This command uses the `mcp__motion__generate-css-bounce-easing` tool to create a precise `linear()` easing function that produces realistic bounce animations in CSS.

## Input Parameters

- **Duration**: Animation duration in seconds (default: 1.0)
  - Shorter (0.5-0.8): Snappier, more urgent feel
  - Default (1.0): Balanced bounce for most use cases
  - Longer (1.2-2.0): Floatier, more dramatic

- **Context**: Helps tailor recommendations (dropdown, modal, toast, button, card, general)

## Output

1. **CSS easing function** ready to use in `transition` properties
2. **Complete CSS example** showing proper usage
3. **Duration recommendation** based on context
4. **Accessibility note** for reduced motion preferences
5. **Variation suggestions** for tweaking the effect

## Usage

```css
/* The generated easing function */
.your-element {
  transition: transform 1s linear(<generated-easing>);
}
```

## Examples

- `/bounce-easing` - Generate standard 1-second bounce easing
- `/bounce-easing 0.8 dropdown` - Snappy bounce for dropdown menu
- `/bounce-easing 1.5 modal` - Dramatic bounce for modal appearance
- `/bounce-easing 0.6 button` - Quick bounce for button press feedback

## Best Use Cases

- Dropdown menus appearing/disappearing
- Modal dialog entry/exit
- Toast notifications
- Button press feedback
- Card hover effects
- Loading indicators

## Accessibility Reminder

Always include reduced motion support:

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
  }
}
```
