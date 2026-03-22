# RaMeS - Raffaele's Merge & Split - mini PDF editor

**Version:** 0.2.0 - Core Consolidation

**Author:** Raffaele N.

## Description

RaMeS is a Python-based PDF manipulation tool. This version marks the transition from experimental scripts to a structured, modular codebase.

## Key Features & Architecture
- **Hybrid Logic**: The project uses a robust Object-Oriented approach for `interval` parsing (`Interval` class in `intervals.py`) combined with a functional engine for PDF processing.
- **Resilient PDF Engine**: The `pdf_engine.py` now features a "Validation Loop". It doesn't just execute; it verifies file integrity and page counts before any operation, handling errors via Python exceptions.
- **Development Strategy (Shadowing)**: * Functions like `_split_()` and `_merge_()` handle real File System I/O.
  - Standard `split()` and `merge()` functions are used for testing and console output simulation.
- **Runtime Type Hinting**: The codebase extensively uses Python type hints to ensure data integrity and improve IDE autocompletion. This reduces type-related bugs during the development of the `Interval` logic and `pdf_engine` utilities.

## Language Policy
- **Documentation & Docstrings**: Written in English to comply with professional coding standards.
- **User Interface & Internal Comments**: The console messages (prints) are in Italian, as the primary target audience for the initial release is Italian-speaking. Full i18n is planned for *post-v1.0 releases*.

## Project Structure
- `intervals.py`: [Core] Finalized logic for page ranges and rotations (absolute/relative).
- `pdf_engine.py`: [Core] Utilities for PDF editing.
- `intervalli.py`: [Legacy] Original procedural logic, kept for reference (to be removed in v0.3).
- `pdf_esempi.py`: [Legacy] Early-stage PDF manipulation experiments (to be removed in v0.3).
- `tests.py`: Unit tests for the interval parsing engine.

## Installation

Make sure you have Python 3.x installed. Install the dependencies with:

`Bash`
```
pip install -r requirements.txt
```

## Known Limitations & Next Implementations
- **Work in Progress**: Integration between the `text_ui` and the refined `pdf_engine` is currently being finalized.

