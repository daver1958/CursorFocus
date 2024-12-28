import os
from datetime import datetime
from analyzers import analyze_file_content, should_ignore_file, is_binary_file
from project_detector import detect_project_type, get_project_description, get_file_type_info
from config import get_file_length_limit

def generate_focus_content(project_path, config):
    """Generate the Focus file content."""
    project_type = detect_project_type(project_path)
    project_info = get_project_description(project_path)
    
    content = [
        f"# Project Focus: {project_info['name']}",
        "",
        f"**Current Goal:** {project_info['description']}",
        "",
        "**Key Components:**"
    ]
    
    # Add directory structure
    structure = get_directory_structure(project_path, config['max_depth'])
    content.extend(structure_to_tree(structure))
    
    content.extend([
        "",
        "**Project Context:**",
        f"Type: {project_info['key_features'][1].replace('Type: ', '')}",
        f"Target Users: Users of {project_info['name']}",
        f"Main Functionality: {project_info['description']}",
        "Key Requirements:",
        *[f"- {feature}" for feature in project_info['key_features']],
        "",
        "**Development Guidelines:**",
        "- Keep code modular and reusable",
        "- Follow best practices for the project type",
        "- Maintain clean separation of concerns",
        "",
        "# File Analysis"
    ])
    
    # Analyze each file
    first_file = True
    for root, _, files in os.walk(project_path):
        if any(ignored in root.split(os.path.sep) for ignored in config['ignored_directories']):
            continue
            
        for file in files:
            if any(file.endswith(ignored.replace('*', '')) for ignored in config['ignored_files']):
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, project_path)
            
            if is_binary_file(file_path):
                continue
            
            functions, line_count = analyze_file_content(file_path)
            if functions or line_count > 0:
                if not first_file:
                    content.append("")
                else:
                    first_file = False
                
                file_type, file_desc = get_file_type_info(file)
                content.append(f"`{rel_path}` ({line_count} lines)")
                content.append(f"**Main Responsibilities:** {file_desc}")
                
                if functions:
                    content.append("**Key Functions:**")
                    for func_name, description in functions:
                        content.append(f"<{func_name}>: {description}")
                
                # Get file-specific length limit
                length_limit = get_file_length_limit(file_path)
                if line_count > length_limit:
                    content.append(f"**📄 Long-file Alert: File exceeds the recommended {length_limit} lines for {os.path.splitext(file)[1]} files ({line_count} lines)**")
    
    content.extend([
        "",
        f"Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    ])
    
    return '\n'.join(content)

def get_directory_structure(project_path, max_depth=3, current_depth=0):
    """Get the directory structure."""
    if current_depth > max_depth:
        return {}
    
    structure = {}
    try:
        for item in os.listdir(project_path):
            if should_ignore_file(item):
                continue
                
            item_path = os.path.join(project_path, item)
            
            if os.path.isdir(item_path):
                substructure = get_directory_structure(item_path, max_depth, current_depth + 1)
                if substructure:
                    structure[item] = substructure
            else:
                structure[item] = None
    except Exception as e:
        print(f"Error scanning directory {project_path}: {e}")
    
    return structure

def structure_to_tree(structure, prefix=''):
    """Convert directory structure to tree format."""
    lines = []
    items = sorted(list(structure.items()), key=lambda x: (x[1] is not None, x[0]))
    
    for i, (name, substructure) in enumerate(items):
        is_last = i == len(items) - 1
        connector = '└─ ' if is_last else '├─ '
        
        if substructure is None:
            icon = '📄 '
            lines.append(f"{prefix}{connector}{icon}{name}")
        else:
            icon = '📁 '
            lines.append(f"{prefix}{connector}{icon}{name}")
            extension = '   ' if is_last else '│  '
            lines.extend(structure_to_tree(substructure, prefix + extension))
    
    return lines 