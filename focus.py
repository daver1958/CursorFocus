import os
import time
from datetime import datetime
from config import load_config
from content_generator import generate_focus_content
from rules_analyzer import RulesAnalyzer
from rules_generator import RulesGenerator

def get_default_config():
    """Get default configuration with parent directory as project path."""
    return {
        'project_path': os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        'update_interval': 60,
        'max_depth': 3,
        'ignored_directories': [
            '__pycache__',
            'node_modules',
            'venv',
            '.git',
            '.idea',
            '.vscode',
            'dist',
            'build',
            'CursorFocus'
        ],
        'ignored_files': [
            '.DS_Store',
            '*.pyc',
            '*.pyo'
        ],
        'binary_extensions': [
            '.png',
            '.jpg',
            '.jpeg',
            '.gif',
            '.ico',
            '.pdf',
            '.exe',
            '.bin'
        ],
        'file_length_standards': {
            '.js': 300,
            '.jsx': 250,
            '.ts': 300,
            '.tsx': 250,
            '.py': 400,
            '.css': 400,
            '.scss': 400,
            '.less': 400,
            '.sass': 400,
            '.html': 300,
            '.vue': 250,
            '.svelte': 250,
            '.json': 100,
            '.yaml': 100,
            '.yml': 100,
            '.toml': 100,
            '.md': 500,
            '.rst': 500,
            'default': 300
        },
        'file_length_thresholds': {
            'warning': 1.0,
            'critical': 1.5,
            'severe': 2.0
        },
        'project_types': {
            'chrome_extension': {
                'indicators': ['manifest.json'],
                'required_files': [],
                'description': 'Chrome Extension'
            },
            'node_js': {
                'indicators': ['package.json'],
                'required_files': [],
                'description': 'Node.js Project'
            },
            'python': {
                'indicators': ['setup.py', 'pyproject.toml'],
                'required_files': [],
                'description': 'Python Project'
            },
            'react': {
                'indicators': [],
                'required_files': ['src/App.js', 'src/index.js'],
                'description': 'React Application'
            }
        }
    }

def setup_cursor_focus(project_path):
    """Set up CursorFocus for a project by generating necessary files."""
    try:
        # Generate .cursorrules file
        print(f"Analyzing project: {project_path}")
        analyzer = RulesAnalyzer(project_path)
        project_info = analyzer.analyze_project_for_rules()
        
        rules_generator = RulesGenerator(project_path)
        rules_file = rules_generator.generate_rules_file(project_info)
        print(f"✅ Generated {rules_file}")

        # Generate initial Focus.md with default config
        focus_file = os.path.join(project_path, 'Focus.md')
        default_config = get_default_config()
        content = generate_focus_content(project_path, default_config)
        with open(focus_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Generated {focus_file}")

        print("\n🎉 CursorFocus setup complete!")
        print("Generated files:")
        print(f"- {rules_file}")
        print(f"- {focus_file}")
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        raise

def main():
    """Main function to generate and update the focus file."""
    # Try to load config, use defaults if not found
    config = load_config()
    if not config:
        print("No config.json found, using default configuration")
        config = get_default_config()

    project_path = config['project_path']
    print(f"Project path: {project_path}")

    # If this is the first run, set up the necessary files
    rules_file = os.path.join(project_path, '.cursorrules')
    if not os.path.exists(rules_file):
        setup_cursor_focus(project_path)

    print(f"\n🔍 CursorFocus is monitoring: {project_path}")
    print("📝 Press Ctrl+C to stop")

    # Monitor and update Focus.md
    focus_file = os.path.join(project_path, 'Focus.md')
    last_content = None
    last_update = 0

    try:
        while True:
            current_time = time.time()
            
            # Only check for updates every update_interval seconds
            if current_time - last_update < config.get('update_interval', 60):
                time.sleep(1)  # Sleep for 1 second to prevent CPU overuse
                continue
                
            # Generate new content
            content = generate_focus_content(project_path, config)
            
            # Only write if content has changed
            if content != last_content:
                try:
                    with open(focus_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    last_content = content
                    print(f"✅ Focus.md updated at {datetime.now().strftime('%I:%M:%S %p')}")
                except Exception as e:
                    print(f"❌ Error writing Focus.md: {e}")
            
            last_update = current_time
            
    except KeyboardInterrupt:
        print("\n👋 Stopping CursorFocus")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    main() 