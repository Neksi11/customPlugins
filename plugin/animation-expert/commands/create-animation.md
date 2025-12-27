---
name: create-animation
description: Create animation code using GSAP or Motion.dev for UI components, transitions, and effects. Integrates with motion MCP server for CSS easing functions.
arguments:
  - name: component
    description: The UI component or element to animate
    required: true
  - name: library
    description: Animation library to use (gsap, motion, or css)
    required: false
    default: gsap
  - name: type
    description: Animation type (hover, click, scroll, entry, exit, stagger, timeline, bounce, spring)
    required: false
    default: hover
---

Create an animation implementation for the specified component using the animation expert's knowledge.

## Input Parameters

- **Component**: Describe the element(s) you want to animate (button, card, modal, list, etc.)
- **Library**:
  - `gsap` - GSAP with full plugin ecosystem (default)
  - `motion` - Motion.dev/Framer Motion for React
  - `css` - Pure CSS with MCP-generated easing functions
- **Type**: hover, click, scroll, entry, exit, stagger, timeline, bounce, spring, 3d, parallax, gesture, svg

## Output

Provide complete, production-ready animation code including:

1. **Animation code** with proper setup and configuration
2. **Easing selection** with rationale - uses MCP server for bounce/spring easing when appropriate
3. **Duration guidelines** based on animation type
4. **Performance notes** about GPU acceleration and optimization
5. **Accessibility considerations** (prefers-reduced-motion)
6. **Integration instructions** for React/vanilla JS projects

## MCP Integration

For CSS-based animations or Motion.dev transitions, this command will automatically use the motion MCP server to generate optimal easing functions:

- **Bounce animations**: Uses `mcp__motion__generate-css-bounce-easing` for entry/exit effects
- **Spring animations**: Uses `mcp__motion__generate-css-spring` for natural, physics-based motion

## Examples

- `/create-animation button hover` - Button hover animation
- `/create-animation modal entry motion` - Modal entry with Motion.dev bounce easing
- `/create-animation card tap css spring` - Card tap effect with CSS spring easing
- `/create-animation list stagger gsap` - List items with staggered animation
- `/create-animation dropdown exit css bounce` - Dropdown exit with bounce easing

## Style

- Production-ready code you can copy-paste
- Include comments explaining key decisions
- Provide variant patterns for flexibility
- Mention any licensing requirements (e.g., GSAP Club plugins)
- When appropriate, use MCP-generated easing values
