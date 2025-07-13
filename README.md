# About
Simple script for moving files from a directory to another, but has following features:
- The files will be only move to the another directory if
    - the parent directories exist in the destination directory
    - if the files are allowed in the destination directory
    - if the files isn't existed in the destination directory
- Produce reports, indicating the paths and reason why the files isn't move

It's good for situation where strict directory structure is needed.

# Requirements
- Windows 10 or newer
- Microsoft Excel
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- powershell


# Setup
```powershell
PS C:\> cd path\to\project
PS C:\> uv sync
```


# Usage
1. add/change `DirInfo` object/s at `_generate_dir_infos` function
2. execute `uv run -m app` using powershell