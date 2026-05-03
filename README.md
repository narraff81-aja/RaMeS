# RaMeS - Raffaele's Merge & Split - mini PDF editor

**Version:** 0.4.0 - high-performance GUI architecture and the introduction of advanced user interaction features

**Author:** Raffaele N.

## 📝 Description

**RaMeS** is a Python-based PDF manipulation tool. This version marks a transition to a professional, three-module GUI architecture powered by PyQt6.

## 🚀 Key Evolutionary Steps & Architecture

### 🖥️ Modular GUI System
The interface has been refactored into three specialized modules to ensure scalability and clean code:
- **`gui_main_window.py`**: The core dashboard for managing PDF operations.
- **`gui_helper_intervals.py`**: A complete modal dialog dedicated to granular interval editing.
- **`gui_widgets.py`**: A centralized library for custom and enhanced UI components.

### 🏗️ Custom Widget Engine
I developed a base class, **`BaseQTable`** (inheriting from `QTableWidget`), which centralizes the logic for:
- **Row Manipulation**: Integrated methods for moving rows (Top, Up, Down, Bottom), as well as adding, deleting, or duplicating entries.
- **Drag & Drop**: Native support for internal row reordering.
- **Specialized Tables**: `IntervalsQTable`, `SplitQTable`, and `MergeQTable` inherit from this base to implement specific validation logic and support for FileSystem Drop.

### ⚙️ Engine Optimizations
- **Automatic Directory Management:** The `pdf_engine.py` (both Split and Merge functions) now automatically generates the required folder structures if they do not exist, preventing I/O crashes.  

### 🖱️ Advanced UX & Interaction
- **Context-Aware CLI:** The `text_ui.py` now intelligently prompts users if an invalid interval is detected, offering a "full-file no rotation" fallback to streamline the workflow.  
- **Path Management**: The `QLineEdit` in the Split path supports direct **FileSystem Drop** for immediate file loading.
- **Merge Table** and **Split Path**: The `MergeQTable` and `DropQLineEdit` supports **FileSystem Drop** to select PDF files.
- **Visual Handles**: Every table row includes a double-arrow icon serving as a "handle" for internal Drag & Drop.

## 📂 Project Structure
- `intervals.py`: Core logic for page ranges and rotations.
- `pdf_engine.py`: The heartbeat of the app, now with unified check/count logic.
- `text_ui.py`: Command-line interface.
- `gui_main_window.py`: [Refactored] The primary dashboard for Split and Merge operations (Widget-based classes).
- `gui_helper_intervals.py`: [New] A specialized modal dialog for granular interval management. (Widget-based classes).
- `gui_widgets.py`: [New] A dedicated utility library containing enhanced PyQt6 components. (Widget-based classes).
- `tests.py`: Unit tests for the interval parsing engine.
- `assets/`: Folder containing icons and images for the GUIs. 
- `docs/gui_pdf_editor.pdf`: [Link to UI Mockup](./docs/gui_pdf_editor.pdf) (Original design wireframes).

## 🛠 Tech Stack
- **Language**: Python 3.x
- **PDF Core**: pypdf
- **GUI Frameworks**: PyQt6
- **Design**: Professional wireframing (PowerPoint exported to PDF for universal compatibility).

## 📝 Developer Notes
- **Enter points**: Now there are 2 entry point: `tests.py`, `gui_main_window.py`. `main.py` will become the one and only. 
- **Language Policy**: The core documentation remains in English, while all User Interfaces (CLI/GUI) are localized in Italian to meet target user requirements.
- **Dependency Management**: `PyQt6` is now a required dependency for the advanced GUI module.
Install the dependencies with:

`Bash`
```
pip install -r requirements.txt
```

## ⚠️ Known Limitations & 🗺️ Next Implementations
- **Visual Bug (Drag Handles)**: During rapid "internal moves" in the tables, the drag-handle icon might disappear. The row movement logic and data integrity remain fully functional. This visual artifact will be addressed in v.0.5.
- **Execution Binding**: The UI is fully reactive to user inputs and validation, but the final PDF processing (Split/Merge) will be linked to the GUI buttons in **v.0.5**.
- **Work in Progress**: Full i18n is planned for *post-v1.0 releases*.