---
name: gsap-expert
description: Use when specifically working with GSAP (GreenSock Animation Platform) including timelines, ScrollTrigger, Flip, Draggable, or any GSAP plugins
version: 1.0.0
---

Use this skill when the user is working with GSAP or needs GSAP-specific expertise.

## GSAP Core Knowledge

### Basic Animations
- `gsap.to()`, `gsap.from()`, `gsap.fromTo()`
- Property sets (x, y, scale, rotation, opacity)
- Duration and easing configuration

### Timeline Control
- `gsap.timeline()` creation and nesting
- Positioning parameters (`<`, `+=`, `-=`, labels)
- Playback controls (play, pause, reverse, restart)
- Progress/time manipulation

### Performance Optimization
- Animate only transform and opacity
- `gsap.context()` for React cleanup
- `will-change` usage
- Batch DOM operations

## GSAP Plugins

### ScrollTrigger
- Scroll-triggered animations
- Pinning elements
- Scrubbing with scroll position
- Parallax effects
- Horizontal scroll sections

### Flip
- Layout animation between states
- Element reordering
- Grid to list transitions
- Absolute positioning for smooth transitions

### Draggable
- Drag interactions with inertia
- Bounds and edge resistance
- Drag events and callbacks
- Throw and catch behavior

### MotionPath
- Animate along SVG paths
- Bezier curve animation
- Auto-rotate along path

### Inertia
- Physics-based scrolling
- Momentum-based animations
- Custom spring physics

## Common Patterns

```javascript
// Basic animation
gsap.to(element, { x: 100, duration: 0.5, ease: "power2.out" });

// Timeline with positioning
const tl = gsap.timeline();
tl.to(el1, { opacity: 1 })
  .to(el2, { opacity: 1 }, "-=0.2")
  .to(el3, { opacity: 1 }, "+=0.3");

// ScrollTrigger
gsap.to(element, {
  x: 500,
  scrollTrigger: {
    trigger: triggerEl,
    start: "top 80%",
    end: "bottom 20%",
    scrub: 1
  }
});

// Flip animation
const state = Flip.getState(elements);
// DOM changes...
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut"
});

// React cleanup
useEffect(() => {
  let ctx = gsap.context(() => {
    gsap.to(ref.current, { x: 100 });
  }, ref);
  return () => ctx.revert();
}, []);
```

## When to Use This Skill

- User mentions GSAP specifically
- Working with timeline-based animations
- Implementing scroll-triggered effects
- Needing Flip/Draggable functionality
- Building complex animation sequences
- Converting from CSS to GSAP

## Licensing Notes

- Core GSAP: Free for most use cases
- Club GSAP (MorphSVG, Inertia, etc.): Paid license required for commercial use
- Always mention licensing for premium plugins
