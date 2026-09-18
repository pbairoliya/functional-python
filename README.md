# Higher-Order Functions in Python

Coursework from **NC State University, Spring 2024**. (Published to GitHub later — the
commit dates here are the publication date, not the original work.)

Implements the functional-programming building blocks by hand rather than reaching for
`filter`/`map`: predicate-driven list filtering, mapping, and folds, written with full
type annotations (`Callable`, `List`) so the higher-order signatures are explicit.

The dataset alongside it — `social_network.txt` and `movies.txt` — is a modernized port of
the SWI-Prolog `movies.pl` example: ten users, their friendships, and the films they liked,
used to exercise the traversal and query exercises.

## Running

```bash
python3 pythonScript.py
```

## Files

| File | Purpose |
|---|---|
| `pythonScript.py` | Higher-order function implementations and their drivers |
| `social_network.txt` | Ten users, their friend lists, and liked movies |
| `movies.txt` | Films 2010–2015 sourced from IMDB, with a merged `starred` predicate |
