---
name: motion-dev-expert
description: Use when working specifically with Motion.dev (formerly Framer Motion) including variants, AnimatePresence, layout animations, useScroll, useTransform, and React animation patterns. Integrates with motion MCP server for CSS easing and spring physics.
version: 1.0.0
---

Use this skill when the user is working with Motion.dev or React animation patterns.

## Motion.dev Core Knowledge

### Basic Animations
- `motion.div`, `motion.span`, etc.
- `initial`, `animate`, `transition` props
- `whileHover`, `whileTap`, `whileDrag`
- `variants` for reusable animations

### Transition Types
- Spring physics (stiffness, damping, mass)
- Tween animations (duration, ease)
- Inertia for drag-based motion
- Custom cubic bezier
- **CSS easing functions via MCP server** (linear() bounce/spring)

## MCP Integration for Motion.dev

The motion MCP server provides CSS easing functions that can be used with Motion.dev's `transition` prop:

### Using MCP Bounce Easing

```jsx
// Get bounce easing from MCP server
// Tool: mcp__motion__generate-css-bounce-easing
// Parameter: duration (default 1.0)

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  // Use the returned easing value in transition
  transition={{ ease: "<returned-easing-value>", duration: 1 }}
/>
```

### Using MCP Spring Easing

```jsx
// Get spring easing from MCP server
// Tool: mcp__motion__generate-css-spring
// Parameters: bounce (0-1, default 0.2), duration (default 0.4)

<motion.div
  initial={{ scale: 0.8 }}
  animate={{ scale: 1 }}
  // Use the returned easing value
  transition={{
    ease: "<returned-easing-value>",
    duration: <returned-duration>
  }}
/>
```

## Component Patterns

### Basic Animation

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: "easeOut" }}
/>

// With MCP bounce easing
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ ease: "<mcp-bounce-easing>", duration: 1 }}
/>
```

### Interactive States

```jsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  whileDrag={{ scale: 1.1 }}
/>

// With MCP spring easing for natural feel
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ ease: "<mcp-spring-bounce-0.2-duration-0.2>" }}
/>
```

### Variants for Orchestration

```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { x: -20, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    // Use MCP spring for natural stagger
    transition: { ease: "<mcp-spring>" }
  }
};

<motion.ul variants={containerVariants}>
  {items.map(item => (
    <motion.li key={item} variants={itemVariants}>
      {item}
    </motion.li>
  ))}
</motion.ul>
```

## Advanced Features

### AnimatePresence (Entry/Exit)

```jsx
<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      transition={{ ease: "<mcp-bounce-easing>" }}
    />
  )}
</AnimatePresence>

// With mode for sequential animations
<AnimatePresence mode="wait">
  {isVisible && <Component />}
</AnimatePresence>
```

### Layout Animations

```jsx
// Automatic layout projection
<motion.div layout>
  {/* Animates to new position */}
</motion.div>

// Shared element transitions
<motion.div layoutId="shared-card">
  Content that morphs between positions
</motion.div>

// With MCP spring for natural layout motion
<motion.div
  layout
  transition={{ ease: "<mcp-spring-bounce-0.1-duration-0.4>" }}
/>
```

### Scroll-Linked Animations

```jsx
const { scrollYProgress } = useScroll();
const scale = useTransform(scrollYProgress, [0, 1], [0.5, 1.5]);
const opacity = useTransform(scrollY, [0, 300], [1, 0]);

// With spring smoothing
const smoothProgress = useSpring(scrollYProgress, {
  damping: 20,
  stiffness: 100
});

<motion.div style={{ scale, opacity }} />
```

### Reorder Component

```jsx
<Reorder.Group axis="y" values={items} onReorder={setItems}>
  {items.map(item => (
    <Reorder.Item
      key={item}
      value={item}
      // Use MCP spring for natural drag feel
      transition={{ ease: "<mcp-spring-bounce-0.3-duration-0.3>" }}
    >
      {item}
    </Reorder.Item>
  ))}
</Reorder.Group>
```

## Spring Physics Configuration

### Motion.dev Built-in Springs

```jsx
// Simple spring
transition={{ type: "spring", stiffness: 100, damping: 10 }}

// Quick snappy
transition={{ type: "spring", stiffness: 300, damping: 30 }}

// Slow bouncy
transition={{ type: "spring", stiffness: 50, damping: 5 }}

// Mass effect (heavier elements)
transition={{ type: "spring", stiffness: 100, damping: 10, mass: 2 }}
```

### MCP Spring vs Motion.dev Spring

| MCP Spring | Motion.dev Spring |
|------------|-------------------|
| CSS easing function | JavaScript physics simulation |
| Works with any CSS transition | Motion.dev only |
| Pre-calculated curve | Real-time physics |
| Predictable output | Responsive to interaction |
| Use for: entry/exit, hover | Use for: drag, gesture, scroll |

**Recommendation**: Use MCP spring for predictable state changes, Motion.dev spring for interactive gestures.

## Performance Optimization

- Memoize variant objects with `useMemo`
- Use `layout="position"` for simpler transitions
- Avoid `AnimatePresence` with large lists
- Virtualize animated list items
- Clean up `useMotionValue` references
- Prefer MCP-generated easing for static animations
- Use Motion.dev springs for interactive elements only

## When to Use This Skill

- User mentions Motion.dev or Framer Motion
- Working with React components and animations
- Implementing entry/exit animations
- Building layout transitions
- Creating scroll-linked effects
- Using variants for animation orchestration
- Needing gesture-based interactions
- Generating CSS easing for Motion.dev transitions

## Motion.dev vs GSAP Context

Use Motion.dev when:
- Building React applications
- Need declarative animation syntax
- Entry/exit animations are required
- Rapid prototyping is priority
- Layout animations are needed
- Gesture interactions are common

Consider GSAP instead when:
- Complex timeline control needed
- Non-React project
- Advanced plugins required (MorphSVG)
- Maximum performance control needed
- Precise frame-by-frame control needed

## MCP Tool Quick Reference

| Tool | Parameters | Best For |
|------|------------|----------|
| `mcp__motion__generate-css-bounce-easing` | duration (default 1.0) | Modal enter/exit, dropdowns, toasts |
| `mcp__motion__generate-css-spring` | bounce (0-1, default 0.2), duration (default 0.4) | Cards, buttons, natural motion, toggles |
