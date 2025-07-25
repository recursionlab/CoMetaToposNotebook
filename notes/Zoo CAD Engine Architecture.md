[https://zoo.dev/research/zoo-cad-engine-overview#21-cad-as-a-service](https://zoo.dev/research/zoo-cad-engine-overview#21-cad-as-a-service)

---

I'll fetch the content from that Zoo.dev research page about their CAD engine overview.

This is an excellent technical overview of Zoo's CAD engine architecture and design philosophy. The document provides deep insights into their approach to building a modern CAD system from the ground up. Here are the key takeaways:

## Core Design Philosophy

**CAD-as-a-Service Architecture**: Zoo has designed their CAD engine to be natively API-first, rather than retrofitting an existing desktop application with web APIs. This ensures that third-party developers have access to exactly the same functionality as Zoo's internal teams - no "secret fast mode" for first-party applications.

**GPU-First Approach**: Unlike traditional CAD systems built in the pre-GPU era, Zoo leverages modern GPU computing throughout both their geometry engine and rendering pipeline. They draw inspiration from game engine development, which has pushed 3D graphics and GPU computing forward while CAD software has lagged behind.

## Technical Innovations

**Minimal Geometric Primitives**: Rather than supporting multiple representation formats (polygons, NURBS, subdivision surfaces, etc.), Zoo maintains a minimal set focused on B-splines. This avoids the "combinatorial curse" where every operation needs multiple implementations for different primitive combinations.

**GPU-Accelerated Surface-Surface Intersection**: They've developed a patented algorithm that uses brute-force parallel processing to sample surface point clouds and identify intersections through distance filtering. This is fundamentally different from traditional "marching" methods that are sequential and CPU-bound.

**Smart Performance Optimizations**: Features like geometry instancing for patterns, batch processing capabilities, and level-of-detail approaches for complex operations.

## Key Technical Sections

The document includes detailed explanations of:

- Sweep operations and their mathematical foundations
- Pattern/duplication systems with GPU instancing
- A comprehensive case study on their GPU-accelerated surface-surface intersection algorithm

The SSI case study is particularly impressive - it shows how they transform a traditionally sequential, CPU-bound operation into a massively parallel GPU operation using point cloud sampling, medial axis transforms, and sophisticated curve reconstruction techniques.

This represents a genuinely modern approach to CAD engine design that addresses many of the performance and architectural limitations of legacy CAD systems. The API-first design combined with GPU acceleration could be particularly compelling for modern cloud-based CAD workflows.

---

Try to help me come up with system prompts or an organizational flow

It basically starts with core shapes like a square and then adds shapes and removes them until it gets the finished product. So the hard part is orienting the llms specially with natural language context

---

Based on Zoo's CAD engine overview, I can help you design system prompts and organizational flow for natural language CAD operations. The key challenge is translating conversational descriptions into precise geometric operations while maintaining spatial reasoning.

This system architecture breaks down the complex problem of natural language CAD into specialized agents that can work together effectively. Here are the key insights:

## Critical Success Factors

1. **Spatial Context is King**: The biggest challenge you mentioned is orientation/spatial reasoning. The dedicated Spatial Reasoning Agent maintains coordinate systems and resolves ambiguous positioning throughout the entire process.
2. **Graceful Ambiguity Handling**: Instead of failing on unclear descriptions, the system asks specific clarifying questions while maintaining conversation flow.
3. **Primitive-First Approach**: Like Zoo's philosophy, start with basic shapes and build complexity through Boolean operations.
4. **Multi-Agent Coordination**: Each agent has a specific expertise area but they communicate through a central coordinator that maintains overall context.

## Implementation Priorities

1. **Start with the Spatial Reasoning Agent** - this is your biggest technical challenge
2. **Build robust Parameter Extraction** - handling "small hole" vs "M6 clearance" is crucial
3. **Create a strong Operation Sequencer** - the logic of what order to do things matters enormously
4. **Implement iterative clarification loops** - users rarely give complete specs upfront

The system is designed to be conversational and forgiving while still producing precise geometric operations. Would you like me to elaborate on any specific agent or create example dialogs for particular use cases?