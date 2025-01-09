import os
import json

def load_config():
    """Load configuration from config.json."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        # Add auto_update setting to config if not present
        if 'auto_update' not in config:
            config['auto_update'] = False
            
        return config
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
        ],
        "binary_extensions": [
            ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".exe", ".bin"
        ],
        "file_length_standards": {
            ".js": 300,
            ".jsx": 250,
            ".ts": 300,
            ".tsx": 250,
            ".py": 400,
            ".css": 400,
            ".scss": 400,
            ".less": 400,
            ".sass": 400,
            ".html": 300,
            ".vue": 250,
            ".svelte": 250,
            ".json": 100,
            ".yaml": 100,
            ".yml": 100,
            ".toml": 100,
            ".md": 500,
            ".rst": 500,
            "default": 300,
            ".swift": 400,
            ".kt": 300,
            ".kts": 200
        }
    }

# Load configuration once at module level
_config = load_config()

# Binary file extensions that should be ignored
BINARY_EXTENSIONS = set(_config.get('binary_extensions', []))

# Documentation and text files that shouldn't be analyzed for functions
NON_CODE_EXTENSIONS = {
    '.md', '.txt', '.log', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
    '.conf', '.config', '.markdown', '.rst', '.rdoc', '.csv', '.tsv'
}

# Extensions that should be analyzed for code
CODE_EXTENSIONS = {
    '.js', '.jsx', '.ts', '.tsx', '.py', '.java', '.cpp', '.c', '.h', 
    '.hpp', '.cs', '.go', '.rb', '.php', '.phtml', '.ctp',
    '.swift', '.kt', '.kts', '.lua'
}

# Regex patterns for function detection
FUNCTION_PATTERNS = {
    'standard': r'(?:^|\s+)(?:function\s+([a-zA-Z_]\w*)|(?:const|let|var)\s+([a-zA-Z_]\w*)\s*=\s*(?:async\s*)?function)',
    'arrow': r'(?:^|\s+)(?:const|let|var)\s+([a-zA-Z_]\w*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[^=])\s*=>',
    'method': r'\b([a-zA-Z_]\w*)\s*:\s*(?:async\s*)?function',
    'class_method': r'(?:^|\s+)(?:async\s+)?([a-zA-Z_]\w*)\s*\([^)]*\)\s*{',
    'object_property': r'([a-zA-Z_]\w*)\s*:\s*(?:\([^)]*\)|[^=])\s*=>',
    'php_function': r'(?:public\s+|private\s+|protected\s+)?function\s+([a-zA-Z_]\w*)\s*\(',
    'php_class_method': r'(?:public\s+|private\s+|protected\s+)function\s+([a-zA-Z_]\w*)\s*\(',
    'cpp_function': r'(?:virtual\s+)?(?:static\s+)?(?:inline\s+)?(?:const\s+)?(?:\w+(?:::\w+)*\s+)?([a-zA-Z_]\w*)\s*\([^)]*\)(?:\s*const)?(?:\s*noexcept)?(?:\s*override)?(?:\s*final)?(?:\s*=\s*0)?(?:\s*=\s*default)?(?:\s*=\s*delete)?(?:{|;)',
    'csharp_method': r'(?:public|private|protected|internal|static|virtual|override|abstract|sealed|async)\s+(?:\w+(?:<[^>]+>)?)\s+([a-zA-Z_]\w*)\s*\([^)]*\)',
    'c_function': r'(?:static\s+)?(?:inline\s+)?(?:const\s+)?(?:\w+(?:\s*\*)*\s+)?([a-zA-Z_]\w*)\s*\([^)]*\)(?:\s*{|;)',
    'kotlin_function': r'(?:fun\s+)?([a-zA-Z_]\w*)\s*(?:<[^>]+>)?\s*\([^)]*\)(?:\s*:\s*[^{]+)?\s*{',
    'kotlin_property': r'(?:val|var)\s+([a-zA-Z_]\w*)\s*(?::\s*[^=]+)?\s*=\s*{',
    'swift_function': r'(?:func\s+)([a-zA-Z_]\w*)\s*(?:<[^>]+>)?\s*\([^)]*\)(?:\s*->\s*[^{]+)?\s*{',
    'swift_property': r'(?:var|let)\s+([a-zA-Z_]\w*)\s*:\s*[^{]+\s*{\s*(?:get|set|willSet|didSet)',
    'go_function': r'func\s+([a-zA-Z_]\w*)\s*\([^)]*\)(?:\s*\([^)]*\))?\s*{',
    'go_method': r'func\s*\([^)]*\)\s*([a-zA-Z_]\w*)\s*\([^)]*\)(?:\s*\([^)]*\))?\s*{',
    'lua_function': r'(?:local\s+)?function\s+([a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)\s*\([^)]*\)',
    'lua_method': r'function\s+[a-zA-Z_]\w*:([a-zA-Z_]\w*)\s*\([^)]*\)'
}

# Keywords that should not be treated as function names
IGNORED_KEYWORDS = {
    'if', 'switch', 'while', 'for', 'catch', 'finally', 'else', 'return',
    'break', 'continue', 'case', 'default', 'to', 'from', 'import', 'as',
    'try', 'except', 'raise', 'with', 'async', 'await', 'yield', 'assert',
    'pass', 'del', 'print', 'in', 'is', 'not', 'and', 'or', 'lambda',
    'global', 'nonlocal', 'class', 'def', 'n', 'lines', 'directly'
}

# Names of files and directories that should be ignored
IGNORED_NAMES = set(_config.get('ignored_directories', []))

FILE_LENGTH_STANDARDS = _config.get('file_length_standards', {})

def get_file_length_limit(file_path):
    """Get the recommended line limit for a given file type."""
    ext = os.path.splitext(file_path)[1].lower()
    return FILE_LENGTH_STANDARDS.get(ext, FILE_LENGTH_STANDARDS.get('default', 300)) 