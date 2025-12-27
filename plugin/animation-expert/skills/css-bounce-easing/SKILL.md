---
name: css-bounce-easing
description: Use when generating CSS bounce animations using the linear() easing function. Activates when user needs bounce effects for UI elements, dropdown menus, modals, or any interface requiring lively motion.
version: 1.0.0
---

Use this skill when the user needs to create bounce animations in CSS.

## About Bounce Easing

Bounce animations add life and playfulness to UI elements. The bounce effect is generated using the CSS `linear()` easing function, which creates precise keyframe-like easing curves.

### When to Use

- Dropdown menus appearing/disappearing
- Modal dialog animations
- Toast notifications entering/leaving
- Button press feedback
- Card hover effects
- Loading indicators
- Success/error state animations

### Duration Guidelines

Bounce animations typically look best with:
- **1 second** - Default, works for most cases
- **0.8 seconds** - Slightly snappier, good for UI feedback
- **1.2 seconds** - More dramatic, good for attention-grabbing elements

**Note:** Longer durations feel like gravity is lower or the UI is lighter. Shorter durations feel like gravity is higher or the UI is heavier.

## Usage Pattern

When implementing bounce animations:

1. **Call the MCP tool** to get the easing function:
   ```
   Use mcp__motion__generate-css-bounce-easing with duration parameter
   ```

2. **Apply to CSS**:
   ```css
   .element {
     transition: transform 1s linear, opacity 1s linear;
     /* The MCP tool provides the easing function value */
   }
   ```

3. **Coordinate with other animations**:
   ```css
   /* For multiple properties, use the same easing */
   .modal {
     transition:
       transform 1s linear,
       opacity 1s linear,
       scale 1s linear;
   }
   ```

## Common Animation Patterns

### Dropdown Menu
```css
.dropdown-menu {
  transform: translateY(-10px) scale(0.95);
  opacity: 0;
  transition: all 1s linear;
}

.dropdown-menu.active {
  transform: translateY(0) scale(1);
  opacity: 1;
}
```

### Modal Appearance
```css
.modal-overlay {
  opacity: 0;
  transition: opacity 1s linear;
}

.modal-content {
  transform: scale(0.8) translateY(20px);
  transition: transform 1s linear;
}
```

### Toast Notification
```css
.toast {
  transform: translateX(100%);
  transition: transform 1s linear;
}

.toast.show {
  transform: translateX(0);
}
```

## Best Practices

1. **Keep it subtle**: Bounce should enhance, not distract
2. **Test on targets**: Same bounce feels different on different element sizes
3. **Consider accessibility**: Respect `prefers-reduced-motion`
4. **Coordinate timings**: Multiple animated elements should share easing
5. **Platform awareness**: Test bounce feel across different devices

## Accessibility

Always respect user motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: none;
  }
}
```

## MCP Tool Reference

The motion MCP server provides:
- **Tool**: `mcp__motion__generate-css-bounce-easing`
- **Parameter**: `duration` (number, default 1.0) - Duration in seconds
- **Returns**: CSS easing function value for use in transitions
