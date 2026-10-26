# Corridor fixtures

| Corridor | Illustrative FX rate | Example route types |
|---|---:|---|
| EUR → BRL | 5.45 | Bank, EVM, Solana, hybrid |
| USD → BRL | 5.62 | Bank, Solana, hybrid |
| USD → MXN | 17.10 | Bank, Solana |

These fixed numbers are synthetic fixtures, not current FX, liquidity, provider availability or corridor coverage claims. Route data lives in `src/payflow/domain.py` to keep the initial implementation dependency-light and directly reviewable.
