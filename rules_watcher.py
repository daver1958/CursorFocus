import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rules_generator import RulesGenerator
from project_detector import detect_project_type

class RulesWatcher(FileSystemEventHandler):
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.rules_generator = RulesGenerator(project_path)
        self.last_update = 0
        self.update_delay = 5  # Seconds to wait before updating to avoid multiple updates

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only process Focus.md changes or project configuration files
        if not self._should_process_file(event.src_path):
            return
            
        current_time = time.time()
        if current_time - self.last_update < self.update_delay:
            return
            
        self.last_update = current_time
        self._update_rules()

    def _should_process_file(self, file_path: str) -> bool:
        """Check if the file change should trigger a rules update."""
        filename = os.path.basename(file_path)
        
        # List of files that should trigger an update
        trigger_files = [
            'Focus.md',
            'package.json',
            'requirements.txt',
            'CMakeLists.txt',
            '.csproj',
            'composer.json',
            'build.gradle',
            'pom.xml'
        ]
        
        return filename in trigger_files or any(file_path.endswith(ext) for ext in ['.csproj'])

    def _update_rules(self):
        """Update the .cursorrules file."""
        try:
            # Re-detect project type
            project_info = detect_project_type(self.project_path)
            
            # Generate new rules
            self.rules_generator.generate_rules_file(project_info)
            print(f"Updated .cursorrules at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error updating .cursorrules: {e}")

def start_watching(project_path: str):
    """Start watching the project directory for changes."""
    event_handler = RulesWatcher(project_path)
    observer = Observer()
    observer.schedule(event_handler, project_path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 