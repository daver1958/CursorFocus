import os
import json
from typing import Dict, Any, List
from datetime import datetime
import re
import pathlib

class RulesGenerator:
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates', 'default.cursorrules.json')
        self.focus_template_path = os.path.join(os.path.dirname(__file__), 'templates', 'Focus.md')

    def _get_timestamp(self) -> str:
        """Get current timestamp in standard format."""
        return datetime.now().strftime('%B %d, %Y at %I:%M %p')

    def generate_rules_file(self, project_info: Dict[str, Any]) -> str:
        """Generate rules file with content comparison before writing."""
        rules_file = pathlib.Path(self.project_path) / '.cursorrules'
        
        # Create new content without timestamp
        new_content = self._generate_content(project_info)
        
        try:
            # Check if file exists and compare contents
            if rules_file.exists():
                old_content = self._read_existing_content(rules_file)
                if self._contents_match(old_content, new_content):
                    return None  # Return None if no changes needed
            
            # Only write if there are actual changes
            self._write_rules_file(rules_file, new_content)
            return str(rules_file)
            
        except Exception as e:
            print(f"Error generating rules file: {str(e)}")
            return None

    def _generate_content(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rules content without timestamp."""
        # Load template
        template = self._load_template()
        
        # Customize template
        rules = self._customize_template(template, project_info)
        
        return rules

    def _read_existing_content(self, rules_file: pathlib.Path) -> Dict[str, Any]:
        """Read existing rules file and strip timestamp."""
        try:
            with open(rules_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                # Remove timestamp from comparison
                if 'last_updated' in content:
                    del content['last_updated']
                return content
        except Exception:
            return None

    def _contents_match(self, old_content: Dict[str, Any], new_content: Dict[str, Any]) -> bool:
        """Compare contents ignoring timestamp."""
        if not old_content:
            return False
        
        # Force update if project name doesn't match directory name
        current_dir_name = pathlib.Path(self.project_path).name
        if old_content.get('project', {}).get('name') != current_dir_name:
            return False
        
        # Deep compare contents
        return json.dumps(old_content, sort_keys=True) == json.dumps(new_content, sort_keys=True)

    def _write_rules_file(self, rules_file: pathlib.Path, content: Dict[str, Any]) -> None:
        """Write content to rules file with current timestamp."""
        # Add timestamp only when writing
        content['last_updated'] = datetime.now().isoformat()
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2)

    def _load_template(self) -> Dict[str, Any]:
        """Load the default template."""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading template: {e}")
            return self._get_default_template()

    def _get_default_template(self) -> Dict[str, Any]:
        """Get a default template if the template file cannot be loaded."""
        return {
            "version": "1.0",
            "last_updated": self._get_timestamp(),
            "project": {
                "name": "Unknown Project",
                "version": "1.0.0",
                "language": "javascript",
                "framework": "none",
                "type": "application"
            },
            "ai_behavior": {
                "code_generation": {
                    "style": {
                        "prefer": [],
                        "avoid": [
                            "magic numbers",
                            "nested callbacks",
                            "hard-coded values"
                        ]
                    }
                },
                "testing": {
                    "required": True,
                    "frameworks": ["jest"],
                    "coverage_threshold": 80
                }
            }
        }

    def _customize_template(self, template: Dict[str, Any], project_info: Dict[str, Any]) -> Dict[str, Any]:
        """Customize the template based on project analysis."""
        rules = template.copy()
        
        # Add timestamp first
        rules['last_updated'] = self._get_timestamp()
        
        # Get project name from directory
        project_name = pathlib.Path(self.project_path).name
        
        # Update project info
        rules['project'].update({
            'name': project_name,  # Use directory name as project name
            'type': project_info.get('type', 'generic'),
            'language': project_info.get('language', 'unknown'),
            'framework': project_info.get('framework', 'none'),
            'description': project_info.get('description', f'Python project: {project_name}')
        })
        
        # Add basic AI behavior rules
        rules['ai_behavior'].update({
            'code_review': {
                'focus_areas': [
                    'security vulnerabilities',
                    'performance bottlenecks',
                    'code maintainability',
                    'test coverage'
                ]
            },
            'documentation': {
                'required_sections': [
                    'overview',
                    'installation',
                    'usage',
                    'api reference'
                ]
            }
        })
        
        return rules

    # ... rest of the methods remain the same ... 