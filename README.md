## Overview
Clippy is a lightweight command-line tool for Ubuntu that simplifies clipboard operations. It allows users to copy file paths or file contents to the clipboard and paste clipboard content (or CopyQ history) to a file. Built with Python, it integrates with <mark>xclip</mark> for basic clipboard functionality and optionally with <mark>CopyQ</mark> for accessing clipboard history.

## Features
- **Copy file paths**: Copy the absolute paths of one or more files to the clipboard.
- **Copy file content**: Copy the text content of a single file to the clipboard.
- **Paste clipboard content**: Append or overwrite clipboard content to a specified file.
- **CopyQ integration**: Paste specific items from CopyQ's clipboard history using an index.
- **Piped input support**: Copy content piped from another command (e.g., curl output).
- **Verbose mode**: Display detailed output for operations.
- **Error handling**: Robust error messages for missing dependencies or invalid inputs.

## Requirements

- Python 3.x
- <mark>xclip</mark>: Required for basic clipboard operations (`sudo apt install xclip`).
- <mark>CopyQ</mark>: Optional for clipboard history access (`sudo apt install copyq`).

## Installation

1. Clone the repository:
  ```
  git clone https://github.com/NightBird78/clippy.git
  cd clippy
  ```


2. Ensure <mark>xclip</mark> (and optionally <mark>CopyQ</mark>) is installed:
  ```
  sudo apt update
  sudo apt install xclip copyq
  ```




3. Make the script executable:
  ```
  chmod +x clippy.py
  ```

4. Optionally, move the script to a directory in your PATH (e.g., /usr/local/bin):
  ```
  sudo mv clippy.py /usr/local/bin/clippy
  ```


## Usage
Run clippy with the desired arguments. Below are some example commands:

### Copy file path(s) to clipboard
  ```
  clippy file1.txt file2.txt
  ```

### Copy file content as text
  ```
  clippy -t file.txt
  ```

### Paste current clipboard to a file (append by default)
  ```
  clippy --paste output.txt
  ```

### Paste the 2nd item from CopyQ history to a file, overwriting
```
clippy --paste -i 1 -w output.txt
```

### Copy piped input to clipboard
```
curl https://jsonplaceholder.typicode.com/users | clippy
```

### Show help
```
clippy --help
```

## Arguments

| Option | Description |
|---|---|
| `files` | Files to copy as paths or paste to (with `--paste`). |
| `-v`, `--verbose` | Show verbose output. |
| `-t`, `--text` | Copy file content as text instead of path. |
| `--paste` | Paste clipboard content to the specified file. |
| `-i`, `--index <n>` | <mark>CopyQ</mark> history index to paste (0 for current, 1 for previous, etc.). |
| `-w`, `--write` | Overwrite the output file instead of appending. |


## Notes

- If <mark>CopyQ</mark> is not installed, the tool falls back to xclip and ignores the `--index`.
- The `-1`, `-2`, etc., shorthands are automatically converted to `--index 1`, `--index 2`, etc.
- Ensure the output file path is valid when using `--paste` to avoid errors.
