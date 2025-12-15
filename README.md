# Batch Rename v2.0

**Batch Rename** is a simple, visual-focused desktop tool designed to make renaming collections of images easier and more convenient. Unlike standard text-based renamers, this tool shows **thumbnails** alongside filenames, so you can always see exactly which image you are renaming and keep track of your workflow.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

## Inspiration

This tool takes me back to my early days learning Python and Tkinter. Building a GUI that is both functional and visually appealing was a challenge—especially managing rows and columns. But it was also when I realized the coding world allows me to create solutions for even the smallest problems that no one else would tackle.

Working with large collections of images quickly exposes the limitations of Windows Explorer and even many professional software solutions.

### Real-World Problems
- Large collections of images, whether downloaded from the web, received from multiple sources, captured with cameras, or collected over many years, often come with inconsistent, messy filenames.  
- Managing these files with varying formats, names, and sources becomes tedious, error-prone, and difficult to track.  
- Standard tools do not provide a way to rename files based on a custom list while preserving the intended order and visual reference.

### Windows Explorer Limitations
- Basic renaming and sorting only.  
- Changing the filename of a file immediately triggers Explorer’s automatic sorting (by name, date, size, etc.), which **rearranges the files visually**.  
- As a result, when renaming hundreds or thousands of files, you **lose track of the file sequence** and cannot tell which image you are currently editing without manually searching.  
- Even though Explorer can display thumbnails, there is **no way to rename files visually in a stable, controlled order**, making bulk renaming tedious and error-prone.

### Limitations of Professional Software
- Most paid or professional solutions focus on libraries, catalogs, or simple batch renaming.  
- Few provide **real-time thumbnail visualization combined with bulk renaming**.  
- Very few tools allow you to paste a sequence of names from Excel or Notepad while keeping a stable workflow.

### Solution
This inspired me to create **Batch Rename**: a visual, stable, and intuitive tool that gives you **full control over your image filenames**.  
It might seem simple or quirky, but it perfectly fits my workflow and solves a real-world problem that other tools simply don’t handle.

## Features

*   **Visual Interface:** Automatically loads and displays thumbnails for image files (`.jpg`, `.png`, `.webp`, etc.), making it perfect for organizing photo albums or datasets.
*   **High Performance:** Built with **multi-threading**, allowing the tool to load thousands of images instantly without freezing or lagging the UI.
*   **Smart Validation:**
    *   **Real-time Error Checking:** Detects invalid Windows characters (`\ / : * ? " < > |`) as you type.
    *   **Duplicate Prevention:** Checks for duplicate names within your input list and existing files in the directory to prevent accidental overwrites.
*   **Fast Navigation:** Use `Enter` or `Arrow Keys` to jump between input fields rapidly (Excel-style navigation).
*   **Clipboard Support:** "Paste List" feature allows you to copy a list of names from Excel/Notepad and paste them directly into the tool to map them to images sequentially.
*   **UI:** Clean, centered layout with precise column alignment and color-coded status indicators.

## Download Executable (.exe)

**No Python installed? No problem!**  

You can download the standalone executable (`.exe`) directly from the **Releases** page. It runs instantly on Windows without requiring any installation.

**[Download BatchRename v2.0 Here](https://github.com/e6pure/BatchRename/releases)**

## Installation (Source Code)

If you are a developer and want to run the script using Python, follow these steps:

### Prerequisites
*   Python 3.x
*   Library: `Pillow`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/e6pure/BatchRename.git
    cd BatchRename
    ```

2.  **Install dependencies:**
    ```bash
    pip install Pillow
    ```

3.  **Run the script:**
    ```bash
    python BatchRename.py
    ```

## How to Use

1.  **Select Folder:** Click **📂 Select Folder** and choose the directory containing your images. The tool will load thumbnails immediately.
2.  **Enter New Names:**
    *   **Manual:** Type the new name in the "NEW NAME" column.
    *   **Paste:** Copy a list of text lines from Excel or Notepad, then click **📋 Paste List** to fill the fields automatically.
3.  **Check Status:** Look at the **STATUS** column.
    *   *Empty/Black:* Ready.
    *   *Red Text:* Invalid character or file already exists.
4.  **Rename:** Click **▶ START RENAME**. The tool will process valid entries and skip errors.

### Tip for "Paste List" Feature

When you load a folder, the tool **reads and displays images according to the current sort order in the folder view**.  
To use the "Paste List" feature effectively:

1. Prepare a list of new names in a text editor (Notepad, Excel, etc.), **one name per line**.  
2. Ensure the order of names matches the **current visual order of files in the folder**.  
3. Copy the list and click **📋 Paste List** in the tool. The names will be assigned **sequentially according to the displayed file order**, allowing you to rename images in a controlled and predictable way.  

This way, you can maintain proper sequence while renaming even large collections of images.

## Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| **Enter** | Move focus to the next row (below). |
| **Down Arrow** | Move focus to the next row (below). |
| **Up Arrow** | Move focus to the previous row (above). |

## Disclaimer

**Warning:** This tool modifies image filenames in bulk and **does not provide any undo mechanism or history of changes**.  
Once a rename operation is performed, you cannot revert the changes automatically. Make sure you **fully understand the operation and have backups if needed** before executing a batch rename.

## Contributing

Contributions are welcome! Please submit issues or pull requests for bug fixes, improvements, or new features.

## Contact / Support

GitHub: https://github.com/e6pure
Email: e6pure42@gmail.com

## License

This project is open-source and available under the **MIT License**.

---
*Developed with Python & Tkinter.*
