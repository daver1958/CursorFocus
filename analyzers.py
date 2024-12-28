import os
import re
from config import BINARY_EXTENSIONS, IGNORED_NAMES

def is_binary_file(filename):
    """Check if a file is binary based on its extension."""
    return os.path.splitext(filename)[1].lower() in BINARY_EXTENSIONS

def should_ignore_file(name):
    """Check if a file or directory should be ignored."""
    return name in IGNORED_NAMES or name.startswith('.')

def find_duplicate_functions(content, filename):
    """Find duplicate functions in a file and their line numbers."""
    duplicates = {}
    function_lines = {}
    
    # JavaScript/TypeScript pattern
    js_pattern = r'(?:^|\s+)(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?function|\b(\w+)\s*:\s*(?:async\s*)?function)'
    
    # Find all function declarations
    for i, line in enumerate(content.split('\n'), 1):
        matches = re.finditer(js_pattern, line)
        for match in matches:
            func_name = next(filter(None, match.groups()))
            if func_name not in function_lines:
                function_lines[func_name] = []
            function_lines[func_name].append(i)
    
    # Identify duplicates
    for func_name, lines in function_lines.items():
        if len(lines) > 1:
            duplicates[func_name] = lines
    
    return duplicates

def analyze_file_content(file_path):
    """Analyze file content for functions and their descriptions."""
    try:
        if is_binary_file(file_path):
            return [], 0
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        functions = []
        duplicates = find_duplicate_functions(content, file_path)
        
        # JavaScript/TypeScript pattern for function with comments
        js_pattern = r'(?:\/\*\*(?:[^*]|\*(?!\/))*\*\/\s*|\/\/[^\n]*\s*)*(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?function|\b(\w+)\s*:\s*(?:async\s*)?function)'
        
        matches = re.finditer(js_pattern, content, re.MULTILINE | re.DOTALL)
        for match in matches:
            func_name = next(filter(None, match.groups()))
            
            # Get comment block before function
            start = match.start()
            comment_block = content[:start].strip().split('\n')[-10:]  # Get up to 10 lines before function
            description = []
            
            # Look for multi-line comment
            in_comment_block = False
            for line in reversed(comment_block):
                line = line.strip()
                
                # Handle JSDoc style comments
                if line.startswith('/**'):
                    in_comment_block = True
                    continue
                elif line.startswith('*/'):
                    continue
                elif in_comment_block and line.startswith('*'):
                    cleaned_line = line.lstrip('* ').strip()
                    if cleaned_line and not cleaned_line.startswith('@'):
                        description.insert(0, cleaned_line)
                # Handle single line comments
                elif line.startswith('//'):
                    cleaned_line = line.lstrip('/ ').strip()
                    if cleaned_line:
                        description.insert(0, cleaned_line)
                # Stop if we hit code
                elif line and not line.startswith('/*') and not in_comment_block:
                    break
            
            # If no comment found, analyze function name and context
            if not description:
                # Get function context from surrounding code
                context_start = max(0, start - 500)
                context = content[context_start:start].strip()
                
                # Analyze function name parts
                name_parts = re.findall('[A-Z][a-z]*|[a-z]+', func_name)
                verb = name_parts[0].lower() if name_parts else ''
                subject = ' '.join(name_parts[1:]).lower() if len(name_parts) > 1 else ''
                
                # Generate meaningful description based on naming pattern
                if verb in ['is', 'has', 'should', 'can', 'will']:
                    description = [f"Checks if {subject} meets specific criteria. Used for validation and state verification."]
                elif verb in ['get', 'fetch', 'retrieve']:
                    description = [f"Retrieves and processes {subject} data. Essential for data access and manipulation."]
                elif verb in ['set', 'update', 'modify']:
                    description = [f"Updates or configures {subject} in the system. Manages state and settings."]
                elif verb in ['calc', 'compute', 'calculate']:
                    description = [f"Performs calculations related to {subject}. Handles complex computations and scoring."]
                elif verb in ['handle', 'process']:
                    description = [f"Processes and manages {subject} operations. Core handler for business logic."]
                elif verb in ['validate', 'verify']:
                    description = [f"Validates {subject} against defined rules. Ensures data integrity and correctness."]
                elif verb in ['create', 'init', 'initialize']:
                    description = [f"Creates and initializes {subject}. Responsible for object creation and setup."]
                elif verb in ['sort', 'order']:
                    description = [f"Sorts {subject} based on specific criteria. Handles data organization and ranking."]
                else:
                    description = [f"Manages {' '.join(name_parts).lower()} operations. Part of core functionality."]
            
            final_description = ' '.join(description)
            
            # Add duplicate alert if needed
            if func_name in duplicates:
                lines = duplicates[func_name]
                final_description += f" **🔄 Duplicate Alert: Function appears twice (lines {' and '.join(map(str, lines))})**"
            
            functions.append((func_name, final_description))
        
        return functions, len(content.split('\n'))
    except Exception as e:
        print(f"Error analyzing file {file_path}: {e}")
        return [], 0 