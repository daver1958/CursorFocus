# CursorFocus

A lightweight tool that maintains a focused view of your project structure and environment. CursorFocus automatically tracks your project files, functions, and environment variables, updating every 60 seconds to keep you informed of changes.

## Features

- 🔄 Real-time project structure tracking
- 📝 Automatic file and function documentation
- 🌳 Hierarchical directory visualization
- ⚙️ Environment variable monitoring
- 🎯 Project-specific information detection
- 🔍 Smart project type detection (Chrome Extension, Node.js, Python)

## Setup

1. Clone or copy the CursorFocus directory to your project:
   ```bash
   git clone https://github.com/yourusername/cursorfocus.git CursorFocus
   ```

2. Install dependencies:
   ```bash
   cd CursorFocus
   pip install -r requirements.txt
   ```

3. Configure CursorFocus for your project:
   ```bash
   python3 setup.py --project /path/to/your/project
   ```

   Options:
   - `--project` or `-p`: Path to the project to monitor (default: parent directory)
   - `--interval` or `-i`: Update interval in seconds (default: 60)
   - `--depth` or `-d`: Maximum directory depth to scan (default: 3)

4. Start monitoring:
   ```bash
   python3 focus.py
   ```

## Output

CursorFocus generates a `Focus` file in the CursorFocus directory with:

1. Project Overview
   - Project name and description
   - Key features and version
   - Project type detection

2. Project Structure
   - Directory hierarchy
   - File descriptions
   - Function listings with descriptions
   - File type detection

3. Environment Variables
   - System environment variables
   - Project-specific variables

## Configuration

Edit `config.json` to customize:

```json
{
    "project_path": "/path/to/your/project",
    "update_interval": 60,
    "max_depth": 3,
    "ignored_directories": [
        "__pycache__",
        "node_modules",
        "venv",
        ".git"
    ],
    "ignored_files": [
        ".DS_Store",
        "*.pyc"
    ]
}
```

## Supported Project Types

CursorFocus automatically detects and provides specialized information for:

- Chrome Extensions (manifest.json)
- Node.js Projects (package.json)
- Python Projects (setup.py, pyproject.toml)
- Generic Projects (basic structure) 