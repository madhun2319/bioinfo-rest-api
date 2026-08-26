# Contributing to BioInfo REST API

Thank you for considering contributing! ??

## How to Get Started

1. **Fork the repository** and clone it locally.
2. Create a new branch for your change:
   `ash
   git checkout -b my-feature
   `
3. Install the development dependencies:
   `ash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt  # optional, includes testing tools
   `
4. Make your changes. Please keep the code style consistent:
   - Run lack . and uff . before committing.
   - Add type hints where appropriate.
5. Write or update tests in the 	ests/ directory.
6. Ensure all tests pass:
   `ash
   pytest
   `
7. Commit with a clear, concise message and push:
   `ash
   git push origin my-feature
   `
8. Open a Pull Request against the master branch.

## Reporting Issues

- Use **GitHub Issues**.
- Include a clear title, description, and steps to reproduce.
- Tag the issue with the appropriate label (ug, enhancement, etc.).

## Pull Request Guidelines

- Keep PRs small and focused on a single concept.
- Ensure the CI pipeline passes (tests, linting, type checking).
- Reference related issues using #<issue-number>.
- Include a brief description of what the PR does and why.

## Code of Conduct

By contributing you agree to follow the project's [Code of Conduct](CODE_OF_CONDUCT.md).

---

Happy coding! ??
