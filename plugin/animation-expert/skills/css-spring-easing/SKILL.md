---
name: css-spring-easing
description: Use when generating CSS spring animations using the linear() easing function. Activates when user needs physics-based spring motion for UI elements, pull-to-refresh, draggable interfaces, or natural-feeling animations.
version: 1.0.0
---

Use this skill when the user needs to create spring animations in CSS.

## About Spring Easing

Spring animations create natural, physics-based motion that feels organic and responsive. Unlike linear or bezier curves, springs simulate real-world physics with bounce and momentum.

### When to Use

- Pull-to-refresh interactions
- Draggable interface elements
- Card swipe gestures
- Bottom sheet/modal dismissals
- Tab switching animations
- Toggle switches
- Any UI needing natural, organic motion
- Micro-interactions responding to user input

### Spring Parameters

Springs are defined by two key parameters:

#### Bounce (0 to 1)
- **0** = No bounce (smooth decay)
- **0.2** = Subtle bounce (default, good for most UI)
- **0.5** = Moderate bounce (playful but controlled)
- **0.8** = High bounce (dramatic, attention-grabbing)
- **1.0** = Maximum bounce (very bouncy, use sparingly)

#### Duration (seconds)
- **0.2** = Quick/snappy (buttons, toggles)
- **0.3** = Normal (default, general UI)
- **0.4** = Relaxed (cards, panels)
- **0.6+** = Slow/dramatic (special effects)

**Important:** Duration is "perceptual duration" - how long the animation appears to take. The actual returned value may be longer due to spring settling time.

## Usage Pattern

When implementing spring animations:

1. **Call the MCP tool** to get the easing function:
   ```
   Use mcp__motion__generate-css-spring with bounce and duration parameters
   ```

2. **Apply to CSS** - prepend with property name:
   ```css
   .element {
     /* The MCP tool returns: "<duration> <easing-function>" */
     transition: transform <returned-value>;
   }
   ```

3. **Coordinate multiple properties**:
   ```css
   /* Use same spring for all animated properties */
   .card {
     transition:
       transform <spring-value>,
       opacity <spring-value>,
       box-shadow <spring-value>;
   }

   /* Or use different springs per property for layered effects */
   .complex {
     transition:
       transform <snappy-spring>,
       opacity <gentle-spring>;
   }
   ```

## Common Animation Patterns

### Toggle Switch (Snappy)
```css
.toggle-slider {
  transform: translateX(0);
  /* bounce: 0.3, duration: 0.2 - snappy feedback */
  transition: transform <spring-value>;
}

.toggle.active .toggle-slider {
  transform: translateX(24px);
}
```

### Bottom Sheet (Natural)
```css
.bottom-sheet {
  transform: translateY(100%);
  /* bounce: 0.4, duration: 0.4 - natural feel */
  transition: transform <spring-value>;
}

.bottom-sheet.open {
  transform: translateY(0);
}
```

### Card Lift (Subtle)
```css
.card {
  transform: translateY(0) scale(1);
  /* bounce: 0.1, duration: 0.3 - almost no bounce */
  transition: transform <spring-value>;
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
}
```

### Pull to Refresh (Bouncy)
```css
.refresh-indicator {
  transform: scale(0);
  /* bounce: 0.7, duration: 0.5 - very bouncy */
  transition: transform <spring-value>;
}

.refresh-indicator.active {
  transform: scale(1);
}
```

## Spring Character Examples

| Bounce | Duration | Character | Use Case |
|--------|----------|-----------|----------|
| 0.0 | 0.2 | Dead, smooth | Professional transitions |
| 0.1 | 0.3 | Gentle | Hover effects, cards |
| 0.2 | 0.4 | Natural (default) | General UI motion |
| 0.3 | 0.2 | Snappy bounce | Buttons, toggles |
| 0.5 | 0.4 | Playful | Success states, toasts |
| 0.7 | 0.5 | Very bouncy | Pull-to-refresh, loading |
| 1.0 | 0.6 | Maximum | Special effects |

## Coordination with Other Animations

When coordinating springs with other animations:

```css
/* Spring for primary motion, fixed timing for fade */
.element {
  transition:
    transform <spring-value>,  /* Uses spring timing */
    opacity 0.3s ease-out;      /* Uses fixed timing */
}
```

The spring's **perceptual duration** should match your other animation timings. If the spring returns `0.6s` but you specified `0.4s` perceptual duration, use `0.4s` for coordinating animations.

## Best Practices

1. **Test on devices**: Springs feel different on touch vs mouse
2. **Match interaction energy**: Quick swipes = snappy springs, slow drags = gentle springs
3. **Avoid over-bounce**: High bounce values can feel chaotic
4. **Coordinate gestures**: Spring bounce should match gesture feel
5. **Consider content**: Heavy content needs gentler springs

## Accessibility

Respect motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: transform 0.2s ease-out;
  }
}
```

## MCP Tool Reference

The motion MCP server provides:
- **Tool**: `mcp__motion__generate-css-spring`
- **Parameters**:
  - `bounce` (number, 0-1, default 0.2) - Bounciness of the spring
  - `duration` (number, default 0.4) - Perceptual duration in seconds
- **Returns**: `"<duration> <easing-function>"` string for CSS transitions

## Spring vs Bounce Easing

| Spring Easing | Bounce Easing |
|---------------|---------------|
| Physics-based simulation | Pre-defined bounce curve |
| Configurable bounce/duration | Single duration parameter |
| More organic feel | Predictable, repeatable |
| Great for gestures | Great for UI state changes |
| Two parameters | One parameter |
