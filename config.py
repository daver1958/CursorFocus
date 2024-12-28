import os
import json

def load_config():
    """Load configuration from config.json."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        return get_default_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def get_default_config():
    """Get default configuration settings."""
    return {
        "project_path": "",
        "update_interval": 60,
        "max_depth": 3,
        "ignored_directories": [
            "__pycache__",
            "node_modules",
            "venv",
            ".git",
            ".idea",
            ".vscode",
            "dist",
            "build",
            "coverage"
        ],
        "ignored_files": [
            ".DS_Store",
            "Thumbs.db",
            "*.pyc",
            "*.pyo",
            "package-lock.json",
            "yarn.lock"
        ]
    }

# Constants
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.exe', '.bin'}
IGNORED_NAMES = {'.git', '__pycache__', 'node_modules', '.DS_Store', 'venv', 'env'}

# File length standards by file type
FILE_LENGTH_STANDARDS = {
    # JavaScript/TypeScript
    '.js': 300,
    '.jsx': 250,  # React components
    '.ts': 300,
    '.tsx': 250,  # React components with TypeScript
    
    # Python
    '.py': 400,
    
    # Styles
    '.css': 400,
    '.scss': 400,
    '.less': 400,
    '.sass': 400,
    
    # Templates
    '.html': 300,
    '.vue': 250,  # Vue components
    '.svelte': 250,  # Svelte components
    
    # Configuration
    '.json': 100,
    '.yaml': 100,
    '.yml': 100,
    '.toml': 100,
    
    # Documentation
    '.md': 500,
    '.rst': 500,
    
    # Default
    'default': 300
}

def get_file_length_limit(file_path):
    """Get the recommended line limit for a given file type."""
    ext = os.path.splitext(file_path)[1].lower()
    return FILE_LENGTH_STANDARDS.get(ext, FILE_LENGTH_STANDARDS['default']) 