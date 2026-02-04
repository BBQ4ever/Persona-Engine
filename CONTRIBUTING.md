# Contributing to Persona Engine

Thank you for your interest in the Persona Engine! We welcome contributions from the community, whether they are bug reports, feature requests, or code improvements.

## Development Principles
1.  **Layer Integrity**: Changes must respect the L0-L3 abstraction layers.
2.  **Deterministic Testing**: Any change to the `SeededSampler` must pass seeding regression tests.
3.  **Bilingual Documentation**: Please provide updates to both English and Chinese documentation where applicable.

## How to Contribute
1.  **Fork the repository**.
2.  **Create a feature branch** (`git checkout -b feat/amazing-feature`).
3.  **Commit your changes** (`git commit -m 'feat: Add amazing feature'`).
4.  **Reference the GECCE Kernel**: If your changes affect the core substrate, ensure compatibility with the GECCE specification.
5.  **Submit a Pull Request**.

## Code of Conduct
By participating in this project, you agree to abide by our ethical standards (see `docs/ETHICS.md`). We reserve the right to reject contributions that promote harmful AI behaviors or violate the 4-layer substrate integrity.
