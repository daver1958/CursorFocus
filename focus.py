import os
import json
import time
from datetime import datetime
import re

# Define file type and basic description
type_descriptions = {
    # Web Development
    '.jsx': {
        'type': 'React Component',
        'description': 'React component file containing UI and logic'
    },
    '.tsx': {
        'type': 'React TypeScript',
        'description': 'React component with TypeScript type definitions'
    },
    '.vue': {
        'type': 'Vue Component',
        'description': 'Vue.js component file with template, script, and style'
    },
    '.svelte': {
        'type': 'Svelte Component',
        'description': 'Svelte component file with reactive UI logic'
    },
    
    # Styling
    '.scss': {
        'type': 'SCSS',
        'description': 'Sass stylesheet with extended CSS functionality'
    },
    '.sass': {
        'type': 'Sass',
        'description': 'Sass stylesheet with indented syntax'
    },
    '.less': {
        'type': 'Less',
        'description': 'Less stylesheet preprocessor file'
    },
    '.styl': {
        'type': 'Stylus',
        'description': 'Stylus stylesheet with expressive language'
    },
    
    # Data & Config
    '.yaml': {
        'type': 'YAML',
        'description': 'YAML configuration or data file'
    },
    '.yml': {
        'type': 'YAML',
        'description': 'YAML configuration or data file'
    },
    '.toml': {
        'type': 'TOML',
        'description': 'TOML configuration file'
    },
    '.env': {
        'type': 'Environment',
        'description': 'Environment variables configuration'
    },
    
    # Documentation
    '.mdx': {
        'type': 'MDX',
        'description': 'Markdown with JSX support for interactive docs'
    },
    '.rst': {
        'type': 'reStructuredText',
        'description': 'Python documentation format'
    },
    
    # Testing
    '.test.js': {
        'type': 'Jest Test',
        'description': 'JavaScript test file using Jest'
    },
    '.test.jsx': {
        'type': 'React Test',
        'description': 'React component test file'
    },
    '.spec.js': {
        'type': 'Test Spec',
        'description': 'JavaScript test specification file'
    },
    
    # Build & Deploy
    '.dockerignore': {
        'type': 'Docker Config',
        'description': 'Docker build exclusion patterns'
    },
    '.nvmrc': {
        'type': 'Node Version',
        'description': 'Node.js version specification'
    },
    '.babelrc': {
        'type': 'Babel Config',
        'description': 'Babel JavaScript transpiler configuration'
    },
    
    # Existing types
    '.py': {
        'type': 'Python Source',
        'description': 'Python script containing project logic and functionality'
    },
    '.js': {
        'type': 'JavaScript Source',
        'description': 'JavaScript file for client-side functionality'
    },
    '.html': {
        'type': 'HTML',
        'description': 'Web page template or interface'
    },
    '.css': {
        'type': 'CSS',
        'description': 'Stylesheet for visual styling'
    },
    '.md': {
        'type': 'Markdown',
        'description': 'Documentation and project information'
    },
    '.txt': {
        'type': 'Text',
        'description': 'Plain text file containing project information'
    },
    '.json': {
        'type': 'JSON',
        'description': 'Configuration or data storage file'
    },
    '.plist': {
        'type': 'Property List',
        'description': 'macOS service configuration file'
    },
    '.log': {
        'type': 'Log',
        'description': 'Application log file for debugging and monitoring'
    }
}

def load_config():
    """Load configuration from config.json."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, 'config.json')
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
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
                "build"
            ],
            "ignored_files": [
                ".DS_Store",
                "*.pyc",
                "*.pyo"
            ]
        }
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def get_project_description(project_path):
    """Get project description and key features."""
    try:
        # Check for different project types
        manifest_path = os.path.join(project_path, 'manifest.json')
        package_path = os.path.join(project_path, 'package.json')
        pyproject_path = os.path.join(project_path, 'pyproject.toml')
        setup_path = os.path.join(project_path, 'setup.py')
        
        if os.path.exists(manifest_path):
            # Chrome Extension
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)
                return {
                    "name": manifest_data.get('name', 'Chrome Extension'),
                    "description": manifest_data.get('description', 'No description available'),
                    "key_features": [
                        f"Version: {manifest_data.get('version', 'unknown')}",
                        f"Type: Chrome Extension",
                        *[f"Permission: {perm}" for perm in manifest_data.get('permissions', [])[:3]]
                    ]
                }
        elif os.path.exists(package_path):
            # Node.js Project
            with open(package_path, 'r') as f:
                package_data = json.load(f)
                return {
                    "name": package_data.get('name', 'Node.js Project'),
                    "description": package_data.get('description', 'No description available'),
                    "key_features": [
                        f"Version: {package_data.get('version', 'unknown')}",
                        f"Type: Node.js",
                        *[f"Dependency: {dep}" for dep in list(package_data.get('dependencies', {}).keys())[:3]]
                    ]
                }
        elif os.path.exists(pyproject_path) or os.path.exists(setup_path):
            # Python Project
            return {
                "name": os.path.basename(project_path),
                "description": "Python project with package configuration",
                "key_features": [
                    "Type: Python Project",
                    "Contains setup.py or pyproject.toml",
                    "Python package structure"
                ]
            }
        
        # Generic Project
        return {
            "name": os.path.basename(project_path),
            "description": "Project directory structure and information",
            "key_features": [
                "File and directory tracking",
                "Automatic updates",
                "Project overview"
            ]
        }
    except Exception as e:
        print(f"Error getting project description: {e}")
        return {
            "name": os.path.basename(project_path),
            "description": "Error reading project information",
            "key_features": [
                "File and directory tracking",
                "Automatic updates",
                "Project overview"
            ]
        }

def analyze_file(file_path):
    """Generate a description for a file based on its extension and content."""
    file_info = {
        'type': 'unknown',
        'description': 'No description available',
        'functions': []
    }
    
    filename = os.path.basename(file_path)
    
    # Special handling for Chrome extension files
    if filename == 'manifest.json':
        file_info.update({
            'type': 'Chrome Extension Manifest',
            'description': 'Configuration file defining extension metadata, permissions, and resources'
        })
    elif filename == 'content.js':
        file_info.update({
            'type': 'Content Script',
            'description': 'JavaScript that runs in the context of web pages, handles image detection and icon overlay'
        })
    elif filename == 'options.html':
        file_info.update({
            'type': 'Options Page',
            'description': 'Settings interface for the Chrome extension'
        })
    elif filename == 'options.js':
        file_info.update({
            'type': 'Options Script',
            'description': 'Handles the logic for extension settings and preferences'
        })
    elif filename == 'styles.css':
        file_info.update({
            'type': 'Stylesheet',
            'description': 'Defines the visual appearance of the extension elements'
        })
    else:
        ext = os.path.splitext(file_path)[1].lower()
        # Use the existing type_descriptions dictionary for other files
        if ext in type_descriptions:
            file_info.update(type_descriptions[ext])
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Extract functions and their descriptions
            if filename.endswith('.js'):
                # JavaScript function pattern
                func_pattern = r'(?:\/\*\*([^*]*)\*\/\s*)?(?:async\s+)?(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s+)?function|\b(\w+)\s*:\s*(?:async\s+)?function)'
                matches = re.finditer(func_pattern, content)
                for match in matches:
                    comment = match.group(1)
                    func_name = match.group(2) or match.group(3) or match.group(4)
                    if func_name:
                        if comment:
                            comment = comment.strip().replace('\n', ' ').replace('*', '').strip()
                            file_info['functions'].append(f"{func_name}() - {comment}")
                        else:
                            file_info['functions'].append(f"{func_name}()")
            
            elif filename.endswith('.py'):
                # Python function pattern
                func_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\):\s*(?:"""([^"]*)""")?'
                matches = re.finditer(func_pattern, content)
                for match in matches:
                    func_name = match.group(1)
                    desc = match.group(2)
                    if desc:
                        desc = desc.strip().replace('\n', ' ')
                        file_info['functions'].append(f"{func_name}() - {desc}")
                    else:
                        file_info['functions'].append(f"{func_name}()")
                
    except Exception as e:
        file_info['description'] = f'Error analyzing file: {str(e)}'
    
    return file_info

def get_directory_structure(path, level=0, max_depth=3, exclude_dir=None):
    """Scan directory and create structure with descriptions."""
    if level >= max_depth:
        return {}
    
    structure = {}
    try:
        items = os.listdir(path)
        for item in items:
            # Skip hidden files and ignored directories
            ignored_dirs = {
                '__pycache__',  # Python cache
                'node_modules', # Node.js modules
                'venv',        # Python virtual environment
                '.git',        # Git directory
                '.idea',       # IDE settings
                '.vscode',     # VSCode settings
                'dist',        # Build output
                'build'        # Build output
            }
            
            # Add the exclude_dir to ignored_dirs if specified
            if exclude_dir:
                ignored_dirs.add(exclude_dir)
            
            if item.startswith('.') or item in ignored_dirs:
                continue
                
            item_path = os.path.join(path, item)
            
            if os.path.isdir(item_path):
                structure[item] = {
                    'type': 'directory',
                    'description': get_directory_description(item),
                    'contents': get_directory_structure(item_path, level + 1, max_depth, exclude_dir)
                }
            else:
                file_info = analyze_file(item_path)
                structure[item] = file_info
    except Exception as e:
        print(f"Error scanning directory {path}: {e}")
    
    return structure

def get_directory_description(dirname):
    """Get a meaningful description for specific directories."""
    descriptions = {
        'icons': 'Contains extension icon assets in various sizes',
        'src': 'Source code files for the extension',
        'dist': 'Distribution files for deployment',
        'test': 'Test files and test utilities',
        'docs': 'Project documentation files',
        'styles': 'CSS and styling related files',
        'scripts': 'JavaScript utility scripts',
        'assets': 'Static assets like images and fonts',
        'lib': 'Third-party libraries and dependencies',
        'config': 'Configuration files for various tools'
    }
    return descriptions.get(dirname, f'Contains {dirname.lower()}-related files and resources')

def get_environment_variables():
    """Get relevant environment variables (excluding sensitive ones)."""
    env_vars = {}
    sensitive_terms = ['key', 'secret', 'password', 'token']
    
    for key, value in os.environ.items():
        # Skip sensitive variables
        if not any(term in key.lower() for term in sensitive_terms):
            env_vars[key] = value
    
    return env_vars

def generate_focus_content():
    """Generate the complete focus file content."""
    content = {
        "timestamp": datetime.now().isoformat(),
        "project": get_project_description(),
        "structure": get_directory_structure(),
        "environment": get_environment_variables()
    }
    
    return content

def write_focus_file(content, focus_file):
    """Write the focus content to file in a readable format."""
    with open(focus_file, 'w') as f:
        # Project Description
        f.write("# Project Overview\n\n")
        f.write(f"## {content['project']['name']}\n")
        f.write(f"{content['project']['description']}\n\n")
        
        f.write("## Key Features\n")
        for feature in content['project']['key_features']:
            f.write(f"- {feature}\n")
        f.write("\n")
        
        # Directory Structure
        f.write("# Project Structure\n\n")
        def write_structure(struct, level=0):
            items = sorted(struct.items(), key=lambda x: (not isinstance(x[1], dict) or x[1].get('type') != 'directory', x[0]))
            for name, info in items:
                # Skip the CursorFocus directory
                if name == 'CursorFocus':
                    continue
                    
                indent = "  " * level
                if isinstance(info, dict) and info.get('type') == 'directory':
                    f.write(f"{indent}📁 {name}/\n")
                    f.write(f"{indent}   ├─ Description: {info['description']}\n")
                    if 'contents' in info:
                        write_structure(info['contents'], level + 1)
                else:
                    f.write(f"{indent}📄 {name}\n")
                    f.write(f"{indent}   ├─ Type: {info.get('type', 'unknown')}\n")
                    f.write(f"{indent}   ├─ Description: {info.get('description', 'No description')}\n")
                    if info.get('functions'):
                        f.write(f"{indent}   └─ Functions:\n")
                        for func in info['functions']:
                            f.write(f"{indent}      • {func}\n")
                    else:
                        f.write(f"{indent}   └─ No functions found\n")
        
        write_structure(content['structure'])
        f.write("\n")
        
        # Environment Variables
        f.write("# Environment Variables\n\n")
        for key, value in content['environment'].items():
            f.write(f"- {key}={value}\n")
        
        # Update Timestamp
        f.write(f"\nLast updated: {content['timestamp']}")

def main():
    """Main function to run the focus file generation."""
    try:
        # Load configuration
        config = load_config()
        if not config:
            raise Exception("Failed to load configuration")
        
        # Get the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Determine project directory
        project_dir = config["project_path"] if config["project_path"] else os.path.dirname(script_dir)
        
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(script_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        # Save current directory
        original_dir = os.getcwd()
        
        try:
            # Change to project directory for scanning
            os.chdir(project_dir)
            
            # Generate content
            content = {
                'project': get_project_description(project_dir),
                'structure': get_directory_structure('.', exclude_dir='CursorFocus', max_depth=config["max_depth"]),
                'environment': get_environment_variables(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Write to file (using absolute paths)
            focus_file = os.path.join(script_dir, 'Focus')
            write_focus_file(content, focus_file)
            
        finally:
            # Always restore original directory
            os.chdir(original_dir)
        
    except Exception as e:
        print(f"Error in main: {e}")
        error_log = os.path.join(script_dir, 'logs', 'cursorfocus.error.log')
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()}: {str(e)}\n")

if __name__ == '__main__':
    # Load configuration
    config = load_config()
    if not config:
        print("❌ Failed to load configuration")
        exit(1)
    
    # Get the project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = config["project_path"] if config["project_path"] else os.path.dirname(script_dir)
    
    print(f"🔍 CursorFocus is monitoring: {project_dir}")
    print("📝 Press Ctrl+C to stop")
    
    while True:
        main()
        time.sleep(config["update_interval"])  # Use configured update interval 