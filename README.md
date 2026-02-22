# -Project-1-Password-Analyzer-

A CLI-based Password Strength Analyzer that simulates realistic attacker strategies using layered detection logic instead of relying only on entropy.

---

## Features

- Entropy calculation (Shannon approximation)
- Dictionary attack simulation
- Structural pattern detection
- Leet normalization detection
- Sequential and repetition pattern detection
- Mask attack simulation (word + 4 digits)
- Brute-force crack time estimation
- Batch password analysis
- Optional SHA-256 hashing

---

## Project Architecture

- `main.py` → CLI interface and execution flow
- `checker.py` → Core analysis engine
- `common_passwords.txt` → Dictionary dataset

---

## How It Works

The analyzer evaluates passwords in layered phases:

1. Exact dictionary match
2. Structured pattern detection
3. Year detection
4. Dictionary substring detection
5. Leet transformation detection
6. Repetition & sequence detection
7. Entropy threshold evaluation
8. Brute-force fallback estimation

This models realistic attacker behavior instead of naive length-based scoring.

---
