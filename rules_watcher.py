import os
import time
from typing import Dict, Any
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from rules_generator import RulesGenerator
from project_detector import detect_project_type

class RulesWatcher(FileSystemEventHandler):
    def __init__(self, project_path: str, project_id: str):
        self.project_path = project_path
        self.project_id = project_id
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
            
            # Generate new rules only if there are changes
            rules_file = self.rules_generator.generate_rules_file(project_info)
            if rules_file:  # Only log if file was actually updated
                print(f"Updated .cursorrules for project {self.project_id} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error updating .cursorrules for project {self.project_id}: {e}")

class ProjectWatcherManager:
    def __init__(self):
        self.observers: Dict[str, Any] = {}
        self.watchers: Dict[str, RulesWatcher] = {}

    def add_project(self, project_path: str, project_id: str = None) -> str:
        """Add a new project to watch.
        
        Args:
            project_path: Path to the project directory
            project_id: Optional unique identifier for the project. If not provided,
                       the absolute path will be used as the ID.
                       
        Returns:
            The project ID used for the watcher
        """
        if not os.path.exists(project_path):
            raise ValueError(f"Project path does not exist: {project_path}")
            
        project_id = project_id or os.path.abspath(project_path)
        
        if project_id in self.observers:
            print(f"Project {project_id} is already being watched")
            return project_id
            
        event_handler = RulesWatcher(project_path, project_id)
        observer = Observer()
        observer.schedule(event_handler, project_path, recursive=True)
        observer.start()
        
        self.observers[project_id] = observer
        self.watchers[project_id] = event_handler
        
        print(f"Started watching project {project_id}")
        return project_id

    def remove_project(self, project_id: str):
        """Stop watching a project."""
        if project_id not in self.observers:
            print(f"Project {project_id} is not being watched")
            return
            
        observer = self.observers[project_id]
        observer.stop()
        observer.join()
        
        del self.observers[project_id]
        del self.watchers[project_id]
        
        print(f"Stopped watching project {project_id}")

    def list_projects(self) -> Dict[str, str]:
        """Return a dictionary of watched projects and their paths."""
        return {pid: watcher.project_path for pid, watcher in self.watchers.items()}

    def stop_all(self):
        """Stop watching all projects."""
        for project_id in list(self.observers.keys()):
            self.remove_project(project_id)

def start_watching(project_paths: str | list[str]):
    """Start watching one or multiple project directories for changes.
    
    Args:
        project_paths: A single project path or list of project paths to watch
    """
    manager = ProjectWatcherManager()
    
    if isinstance(project_paths, str):
        project_paths = [project_paths]
        
    for path in project_paths:
        manager.add_project(path)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop_all() 