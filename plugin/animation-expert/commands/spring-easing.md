---
name: spring-easing
description: Generate CSS spring easing function using the motion MCP server for natural, physics-based animations
arguments:
  - name: bounce
    description: Spring bounce amount (0-1, default 0.2). Higher = more bounce
    required: false
  - name: duration
    description: Perceptual duration in seconds (0.2-1.0, default 0.4)
    required: false
  - name: context
    description: Animation context (toggle, card, sheet, button, swipe, general)
    required: false
    default: general
---

Generate a CSS spring easing function using the motion MCP server.

## How It Works

This command uses the `mcp__motion__generate-css-spring` tool to create a physics-based spring animation as a `linear()` easing function. Springs simulate real-world physics with bounce and momentum for organic, natural motion.

## Input Parameters

### Bounce (0 to 1)
Controls how bouncy the spring is:

| Value | Feel | Best For |
|-------|------|----------|
| 0.0 | Smooth, dead | Professional transitions |
| 0.1-0.2 | Subtle, natural | Cards, panels, general UI |
| 0.3 | Snappy | Buttons, toggles |
| 0.5 | Playful | Success states, toasts |
| 0.7+ | Very bouncy | Pull-to-refresh, special effects |

### Duration (seconds)
The perceptual duration (how long it appears to take):

| Value | Feel | Best For |
|-------|------|----------|
| 0.2 | Quick, snappy | Toggles, buttons |
| 0.3-0.4 | Normal (default) | General UI motion |
| 0.5-0.6 | Relaxed | Large cards, sheets |
| 0.8+ | Slow | Dramatic effects |

**Note**: The actual duration returned may be longer than specified to allow the spring to settle.

## Output

1. **CSS easing string** with duration and easing function
2. **Complete CSS example** showing proper usage
3. **Parameter explanation** for the chosen bounce/duration
4. **Property coordination guide** for multi-property animations
5. **Accessibility note** for reduced motion preferences

## Usage

```css
/* The MCP tool returns: "0.4s linear(<easing-function>)" */
.your-element {
  transition: transform 0.4s linear(<generated-easing>);
}

/* Multiple properties use same easing */
.element {
  transition:
    transform 0.4s linear(<easing>),
    opacity 0.4s linear(<easing>),
    box-shadow 0.4s linear(<easing>);
}
```

## Examples

- `/spring-easing` - Generate standard spring (bounce: 0.2, duration: 0.4)
- `/spring-easing 0.3 0.2 toggle` - Snappy bounce for toggle switch
- `/spring-easing 0.1 0.5 card` - Gentle spring for card hover
- `/spring-easing 0.6 0.5 swipe` - Bouncy spring for swipe gesture
- `/spring-easing 0 0.3 modal` - Smooth spring with no bounce

## Best Use Cases

- Pull-to-refresh interactions
- Draggable interface elements
- Card swipe gestures
- Bottom sheet/modal dismissals
- Tab switching animations
- Toggle switches
- Natural-feeling UI motion

## Property Coordination

When animating multiple properties, use the same spring value:

```css
.card {
  transition:
    transform <spring-value>,
    opacity <spring-value>,
    box-shadow <spring-value>;
}
```

For layered effects, use different springs per property:

```css
.complex {
  transition:
    transform <snappy-spring>,
    opacity <gentle-spring>;
}
```

## Accessibility Reminder

Always include reduced motion support:

```css
@media (prefers-reduced-motion: reduce) {
  .element {
    transition: transform 0.2s ease-out;
  }
}
```

## Spring vs Bounce Easing

- **Spring**: Physics-based, configurable bounce/duration, natural feel, great for gestures
- **Bounce**: Pre-defined curve, single duration, predictable, great for UI state changes

Use `/bounce-easing` for modal enter/exit, dropdowns.
Use `/spring-easing` for draggable interfaces, toggles, cards.
