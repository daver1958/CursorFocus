import os
import json

def detect_project_type(project_path):
    """Detect project type based on file presence."""
    if os.path.exists(os.path.join(project_path, 'manifest.json')):
        return 'chrome_extension'
    elif os.path.exists(os.path.join(project_path, 'package.json')):
        return 'node_js'
    elif any(os.path.exists(os.path.join(project_path, f)) for f in ['setup.py', 'pyproject.toml']):
        return 'python'
    elif all(os.path.exists(os.path.join(project_path, f)) for f in ['src/App.js', 'src/index.js']):
        return 'react'
    return 'generic'

def get_project_description(project_path):
    """Get project description and key features."""
    try:
        project_type = detect_project_type(project_path)
        
        if project_type == 'chrome_extension':
            with open(os.path.join(project_path, 'manifest.json'), 'r') as f:
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
        elif project_type == 'node_js':
            with open(os.path.join(project_path, 'package.json'), 'r') as f:
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
            "key_features": ["File and directory tracking"]
        }

def get_file_type_info(filename):
    """Get file type information."""
    ext = os.path.splitext(filename)[1].lower()
    
    type_map = {
        '.py': ('Python Source', 'Python script containing project logic'),
        '.js': ('JavaScript', 'JavaScript file for client-side functionality'),
        '.jsx': ('React Component', 'React component file'),
        '.ts': ('TypeScript', 'TypeScript source file'),
        '.tsx': ('React TypeScript', 'React component with TypeScript'),
        '.html': ('HTML', 'Web page template'),
        '.css': ('CSS', 'Stylesheet for visual styling'),
        '.md': ('Markdown', 'Documentation file'),
        '.json': ('JSON', 'Configuration or data file')
    }
    
    return type_map.get(ext, ('Generic', 'Project file')) 