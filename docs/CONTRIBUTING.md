# Contributing to Crypto Vibeness

Thank you for your interest in contributing to this pedagogical cryptography project!

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize education and learning

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/BTP_B2/crypto_vibe.git
   cd cryptographie_vibe
   ```

2. **Set up your environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Verify setup**
   ```bash
   make test
   ```

## Development Workflow

### Before Making Changes
- Create a new branch: `git checkout -b feature/your-feature-name`
- Keep changes focused and atomic

### Code Style
- Use Black for formatting: `make format`
- Follow PEP 8 guidelines
- Run linter: `make lint`
- Max line length: 120 characters

### Testing
- Run full test suite: `make test`
- Run specific tests: `make test-jour1p1`, `make test-jour2p2`, etc.
- All tests must pass before submitting PR
- Add tests for new features

### Commit Messages
Include the `Co-authored-by` trailer:
```
Commit message describing the change

Co-authored-by: Your Name <email@example.com>
```

## Pull Request Process

1. Update `PROJECT_STATE.md` with your changes
2. Ensure all tests pass: `make test`
3. Ensure code is formatted: `make format`
4. Create descriptive commit messages
5. Push to your branch and create a PR
6. Link related issues using `Closes #issue-number`

## Documentation

- Update relevant `.md` files (JOUR1_PARTIE1.md, etc.)
- Keep README.md current
- Document new cryptographic modules thoroughly

## Cryptography Standards

This project implements specific cryptographic standards:

- **Password Hashing**: Bcrypt (auto-upgrade from MD5)
- **Key Derivation**: PBKDF2-HMAC-SHA256 (100k iterations)
- **Symmetric Encryption**: AES-256-CBC with random IVs
- **Asymmetric Encryption**: RSA-2048 with OAEP
- **Digital Signatures**: RSA-PSS with SHA256

Do not modify these without understanding the security implications.

## Reporting Issues

- Use GitHub Issues for bug reports
- Include steps to reproduce
- Specify cryptography stage affected (JOUR1_PARTIE1, etc.)
- Attach validation test output if applicable

## Questions?

- Check documentation in `.md` files
- Review existing code examples in `src/`
- Look at tests in `tests/`

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing!** 🚀
