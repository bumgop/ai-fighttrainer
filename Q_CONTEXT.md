# Amazon Q Project Context

## Project Summary
This repository contains a solo portfolio project:
An adaptive fighting game training system built in Godot 4 Mono (C#).

The project uses short, WarioWare-style minigames to train fighting game fundamentals and analyze player performance using telemetry and ML-assisted analytics.

This is NOT a full fighting game.

---

## Tooling Roles
- ChatGPT: Architectural authority and planner
- Amazon Q: Code implementer and refactorer
- Git: Source of truth

Amazon Q must not redesign systems or advance development phases independently.

---

## Development Workflow
Development is phase-gated.

Each phase includes:
- Objective
- Deliverables
- Non-goals
- Acceptance criteria

Amazon Q must:
- Work ONLY on the currently active phase
- Ignore future phases unless explicitly instructed
- Ask for clarification if instructions conflict with documentation

---

## Core Constraints
- Engine: Godot 4.x Mono
- Language: C#
- ML is implemented later via Python (file-based exchange)
- Visual style is minimal and abstract
- No multiplayer
- No scope expansion without approval

---

## Execution Rule
When given instructions:
1. Follow them literally
2. Prefer minimal, clear implementations
3. Avoid speculative abstractions
4. Avoid premature optimization
