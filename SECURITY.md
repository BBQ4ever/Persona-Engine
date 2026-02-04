# Security Policy

## Supported Versions

We only provide security updates for the latest stable version of Persona Engine.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

As an AI infrastructure project, we take security seriously. We categorize vulnerabilities into two types:

### 1. Technical Vulnerabilities
Traditional code exploits, buffer overflows, or dependency vulnerabilities.

### 2. Behavioral Vulnerabilities (AI Safety)
- **Prompt Leakage**: Methods to bypass the L0/L1 gatekeepers to reveal the raw L2 Genome instructions.
- **Logic Jailbreaking**: Attacks that force the Persona into a "Hallucination Trap" by bypassing the L0 Strict Mode.

**Please do not report security vulnerabilities via public GitHub issues.** Instead, please send them to the project maintainers directly (or via the email listed in your GitHub profile).

We will acknowledge your report within 48 hours and provide a timeline for a fix.
