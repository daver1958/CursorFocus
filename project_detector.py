import os
import json
from config import load_config

# Load project types from config
_config = load_config()
PROJECT_TYPES = _config.get('project_types', {})

def detect_project_type(project_path):
    """Detect project type based on file presence using configurable rules."""
    for project_type, rules in PROJECT_TYPES.items():
        # Check for indicator files (any of these files indicate this project type)
        if any(os.path.exists(os.path.join(project_path, f)) for f in rules.get('indicators', [])):
            return project_type
            
        # Check for required files (all of these files must exist)
        if rules.get('required_files') and all(os.path.exists(os.path.join(project_path, f)) for f in rules['required_files']):
            return project_type
            
    return 'generic'

def get_project_description(project_path):
    """Get project description and key features using standardized approach."""
    try:
        project_type = detect_project_type(project_path)
        
        if project_type == 'chrome_extension':
            manifest_path = os.path.join(project_path, 'manifest.json')
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r') as f:
                    manifest_data = json.load(f)
                    return {
                        "name": manifest_data.get('name', 'Chrome Extension'),
                        "description": manifest_data.get('description', 'No description available'),
                        "key_features": [
                            f"Version: {manifest_data.get('version', 'unknown')}",
                            f"Type: {PROJECT_TYPES[project_type]['description']}",
                            *[f"Permission: {perm}" for perm in manifest_data.get('permissions', [])[:3]]
                        ]
                    }
                    
        elif project_type == 'node_js':
            package_path = os.path.join(project_path, 'package.json')
            if os.path.exists(package_path):
                with open(package_path, 'r') as f:
                    package_data = json.load(f)
                    return {
                        "name": package_data.get('name', 'Node.js Project'),
                        "description": package_data.get('description', 'No description available'),
                        "key_features": [
                            f"Version: {package_data.get('version', 'unknown')}",
                            f"Type: {PROJECT_TYPES[project_type]['description']}",
                            *[f"Dependency: {dep}" for dep in list(package_data.get('dependencies', {}).keys())[:3]]
                        ]
                    }
        
        # Generic Project or other types
        return {
            "name": os.path.basename(project_path),
            "description": "Project directory structure and information",
            "key_features": [
                f"Type: {PROJECT_TYPES.get(project_type, {'description': 'Generic Project'})['description']}",
                "File and directory tracking",
                "Automatic updates"
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