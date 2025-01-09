import os
import time
from datetime import datetime
from config import load_config
from content_generator import generate_focus_content
from rules_analyzer import RulesAnalyzer
from rules_generator import RulesGenerator
from rules_watcher import ProjectWatcherManager
import logging
from auto_updater import AutoUpdater
import pathlib
import re

def get_default_config():
    """Get default configuration with parent directory as project path."""
    return {
        'project_path': os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
        'update_interval': 300,
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
            '.php': 400,
            '.phtml': 300,
            '.ctp': 300,
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
            },
            'php': {
                'indicators': ['composer.json', 'index.php'],
                'required_files': [],
                'description': 'PHP Project'
            },
            'laravel': {
                'indicators': ['artisan'],
                'required_files': [],
                'description': 'Laravel Project'
            },
            'wordpress': {
                'indicators': ['wp-config.php'],
                'required_files': [],
                'description': 'WordPress Project'
            }
        }
    }

def setup_cursor_focus(project_path):
    """Set up CursorFocus for a project by generating necessary files."""
    try:
        # Convert to Path object for better path handling
        project_path = pathlib.Path(project_path)
        print(f"Analyzing project: {project_path}")
        
        analyzer = RulesAnalyzer(str(project_path))
        project_info = analyzer.analyze_project_for_rules()
        
        rules_generator = RulesGenerator(str(project_path))
        rules_file = rules_generator.generate_rules_file(project_info)
        print(f"✅ Generated {rules_file}")

        # Generate initial Focus.md with default config
        focus_file = project_path / 'Focus.md'
        default_config = get_default_config()
        content = generate_focus_content(str(project_path), default_config)
        # Ensure parent directory exists
        focus_file.parent.mkdir(parents=True, exist_ok=True)
        focus_file.write_text(content, encoding='utf-8')
        print(f"✅ Generated {focus_file}")

        print("\n🎉 CursorFocus setup complete!")
        print("Generated files:")
        print(f"- {rules_file}")
        print(f"- {focus_file}")
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        raise

def monitor_project(project_config, global_config):
    """Monitor a single project."""
    # Convert to Path object
    project_path = pathlib.Path(project_config['project_path'])
    print(f"\n🔍 Monitoring project: {project_config['name']} at {project_path}")
    
    # Merge project config with global config
    config = {**global_config, **project_config}
    
    focus_file = project_path / 'Focus.md'
    last_content = None
    last_update = 0

    # Start rules watcher for this project
    watcher = ProjectWatcherManager()
    watcher.add_project(str(project_path), project_config['name'])

    while True:
        current_time = time.time()
        
        if current_time - last_update < config.get('update_interval', 300):
            time.sleep(1)
            continue
            
        content = generate_focus_content(str(project_path), config)
        
        # Compare content ignoring timestamp lines
        if _content_changed(last_content, content):
            try:
                # Ensure parent directory exists
                focus_file.parent.mkdir(parents=True, exist_ok=True)
                focus_file.write_text(content, encoding='utf-8')
                last_content = content
                print(f"✅ {project_config['name']} Focus.md updated at {datetime.now().strftime('%I:%M:%S %p')}")
            except Exception as e:
                print(f"❌ Error writing Focus.md for {project_config['name']}: {str(e)}")
        
        last_update = current_time

def _content_changed(old_content: str, new_content: str) -> bool:
    """Compare Focus.md content ignoring timestamp lines."""
    if old_content is None:
        return True
        
    # Split content into lines
    old_lines = old_lines = [line for line in old_content.splitlines() 
                            if not _is_timestamp_line(line)]
    new_lines = [line for line in new_content.splitlines() 
                 if not _is_timestamp_line(line)]
    
    return old_lines != new_lines

def _is_timestamp_line(line: str) -> bool:
    """Check if a line contains timestamp information."""
    timestamp_patterns = [
        "Last Updated:",
        "Generated on:",
        "Last Analyzed:",
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",  # yyyy-mm-dd hh:mm:ss
        r"\w+ \d{1,2}, \d{4} at \d{1,2}:\d{2} [AP]M"  # Month DD, YYYY at HH:MM AM/PM
    ]
    
    return any(pattern in line or re.search(pattern, line) 
              for pattern in timestamp_patterns)

def main():
    """Main function to monitor multiple projects."""
    # Setup logging
    logging.basicConfig(
        level=logging.WARNING,
        format='%(levelname)s: %(message)s'
    )

    config = load_config()
    if not config:
        print("No config.json found, using default configuration")
        config = get_default_config()

    # Only check for updates if auto_update is True
    if config.get('auto_update', False):
        print("\n🔄 Checking for updates...")
        updater = AutoUpdater()
        update_info = updater.check_for_updates()
        
        if update_info:
            print(f"\n📦 New updates available")
            print(f"Commit: {update_info['message']}")
            print(f"Author: {update_info['author']}")
            print(f"Date: {update_info['date']}")
            
            if input("\nDo you want to update? (y/n): ").lower() == 'y':
                print("\n⏳ Downloading and installing update...")
                if updater.update(update_info):
                    print("✅ Update successful! Please restart the application.")
                    return
                else:
                    print("❌ Update failed. Continuing with current version.")
        else:
            print("✅ You are using the latest version.")

    if 'projects' not in config:
        # Handle single project config for backward compatibility
        config['projects'] = [{
            'name': 'Default Project',
            'project_path': config['project_path'],
            'update_interval': config.get('update_interval', 300),
            'max_depth': config.get('max_depth', 3)
        }]

    # Create threads for each project
    from threading import Thread
    threads = []
    
    try:
        for project in config['projects']:
            # Convert project path to Path object
            project_path = pathlib.Path(project['project_path'])
            
            try:
                # Verify directory exists and is accessible
                if not project_path.exists():
                    print(f"⚠️ Warning: Project path does not exist: {project_path}")
                    continue
                
                # Try to create a test file to check write permissions
                test_file = project_path / '.cursor_test'
                try:
                    test_file.touch()
                    test_file.unlink()  # Remove test file
                except PermissionError:
                    print(f"⚠️ Warning: No write permission for: {project_path}")
                    continue

                # Setup project if needed
                rules_file = project_path / '.cursorrules'
                if not rules_file.exists():
                    try:
                        setup_cursor_focus(project_path)
                    except Exception as e:
                        print(f"❌ Error setting up project {project['name']}: {str(e)}")
                        continue

                # Start monitoring thread
                thread = Thread(
                    target=monitor_project,
                    args=(project, config),
                    daemon=True,
                    name=f"Monitor-{project['name']}"
                )
                thread.start()
                threads.append(thread)
                print(f"✅ Started monitoring: {project['name']}")

            except Exception as e:
                print(f"❌ Error initializing project {project['name']}: {str(e)}")
                continue

        if not threads:
            print("\n❌ No projects could be monitored. Check permissions and paths.")
            return

        print(f"\n✅ Monitoring {len(threads)} projects")
        print("📝 Press Ctrl+C to stop all monitors")
        
        # Keep main thread alive and monitor thread health
        while True:
            alive_threads = [t for t in threads if t.is_alive()]
            if len(alive_threads) < len(threads):
                print(f"⚠️ Warning: Some monitoring threads have stopped. Active: {len(alive_threads)}/{len(threads)}")
                threads = alive_threads
            if not threads:
                print("❌ All monitoring threads have stopped. Exiting...")
                break
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n👋 Stopping all CursorFocus monitors")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == '__main__':
    main() 