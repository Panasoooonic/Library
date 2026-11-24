# Library Loan Manager

A small Python 3.12 program that tracks library books and members, checks books out and in, and calculates loan fees by membership tier.

- Language: Python 3.12
- Test framework: pytest 8.3.4 with pytest-cov 6.0.0
- Baseline version: v1.0.0

## Run the tests

```bash
pip install -r requirements.txt
pytest --cov=. --cov-report=xml:coverage.xml --cov-report=term
```
