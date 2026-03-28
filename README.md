# RaMeS - Raffaele's Merge & Split - mini PDF editor

**Version:** 0.3.0 - UI Integration & Refactored Engine

**Author:** Raffaele N.

## 📝 Description

RaMeS is a Python-based PDF manipulation tool. This version is evolving into a full-featured desktop application. This version focuses on bridging the gap between the core PDF engine and multiple user interfaces (CLI and GUI).

## 🚀 Key Evolutionary Steps & Architecture
- **Unified PDF Engine**: Replaced standalone validation and counting functions with a single, atomic `pagesCountAndCheck()` method.
- **Hybrid Error Handling**: The engine uses structured Dictionaries for predictable states (validation, page counting), while still leveraging Python Exceptions for critical runtime errors or type mismatches during `pagesCountAndCheck()`, `split()` and `merge()` operations.
- **Multi-UI Architecture**: 
    - `text_ui.py`: A robust CLI for terminal-based operations.
    - `gui_pyqt6.py`: Advanced GUI implementation using the PyQt6 framework.
    - `gui_tkinter.py`: Lightweight GUI alternative using Python's standard library.
- **Type Hinting & Validation**: Maintained 100% type hint coverage for improved maintainability and IDE integration.

## 📂 Project Structure
- `intervals.py`: Core logic for page ranges and rotations.
- `pdf_engine.py`: [Refactored] The heartbeat of the app, now with unified check/count logic.
- `text_ui.py`: [New] Command-line interface.
- `gui_pyqt6.py` / `gui_tkinter.py`: [New] GUI prototypes (Widget-based classes).
- `tests.py`: Unit tests for the interval parsing engine.
- `assets/`: Folder containing icons and images for the GUIs. 
- `docs/gui_pdf_editor.pdf`: [Link to UI Mockup](./docs/gui_pdf_editor.pdf) (Original design wireframes).

## 🛠 Tech Stack
- **Language**: Python 3.x
- **PDF Core**: pypdf
- **GUI Frameworks**: PyQt6, Tkinter
- **Design**: Professional wireframing (PowerPoint exported to PDF for universal compatibility).

## 📝 Developer Notes
- **Enter points**: Now there are 3 entry point: `tests.py`, `gui_pyqt6.py`, `gui_tkinter.py`. `main.py` will become the one and only. 
- **Language Policy**: The core documentation remains in English, while all User Interfaces (CLI/GUI) are localized in Italian to meet target user requirements.
- **Dependency Management**: `PyQt6` is now a required dependency for the advanced GUI module.
Install the dependencies with:

`Bash`
```
pip install -r requirements.txt
```

## ⚠️ Known Limitations & 🗺️ Next Implementations
- **Work in Progress**: Final choice of GUI framework (Tkinter or PyQt6) and ongoing implementation of the same GUI.
- **Work in Progress**: Full i18n is planned for *post-v1.0 releases*.
