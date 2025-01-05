import os
import requests
import json
import shutil
from datetime import datetime
import logging
from typing import Optional, Dict, Any

class AutoUpdater:
    def __init__(self, repo_url: str = "https://github.com/RenjiYuusei/CursorFocus"):
        self.repo_url = repo_url
        self.api_url = repo_url.replace("github.com", "api.github.com/repos")
        self.last_check_file = os.path.join(os.path.dirname(__file__), '.last_update_check')
        self.update_interval = 24 * 60 * 60  # 24 hours in seconds

    def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Check if updates are available."""
        try:
            # Check time from last check
            if not self._should_check_updates():
                last_check = self._get_last_check_time()
                print(f"Last update check was at: {last_check}")
                return None

            # Get the latest release information
            response = requests.get(f"{self.api_url}/releases/latest")
            if response.status_code != 200:
                return None

            latest_release = response.json()
            current_version = self._get_current_version()
            
            if self._is_newer_version(latest_release['tag_name'], current_version):
                return latest_release
            
            return None

        except Exception as e:
            logging.error(f"Error checking for updates: {e}")
            return None

    def update(self, release_info: Dict[str, Any]) -> bool:
        """Download and install update."""
        try:
            # Download and extract update
            download_url = release_info['zipball_url']
            response = requests.get(download_url)
            
            if response.status_code != 200:
                return False
                
            # Save zip file
            update_zip = os.path.join(os.path.dirname(__file__), 'update.zip')
            with open(update_zip, 'wb') as f:
                f.write(response.content)
                
            # Extract and update files
            self._extract_and_update(update_zip)
            
            # Delete zip file
            os.remove(update_zip)
            
            # Update version
            self._update_version(release_info['tag_name'])
            
            return True

        except Exception as e:
            logging.error(f"Error during update: {e}")
            return False

    def _should_check_updates(self) -> bool:
        """Check if enough time has passed since last update check."""
        current_time = datetime.now()
        
        if not os.path.exists(self.last_check_file):
            self._save_last_check_time(current_time)
            return True
        
        try:
            with open(self.last_check_file, 'r') as f:
                last_check_str = f.read().strip()
                last_check = datetime.strptime(last_check_str, "%Y-%m-%d %H:%M:%S")
            
            time_diff = current_time - last_check
            should_check = time_diff.total_seconds() >= self.update_interval
            
            if should_check:
                self._save_last_check_time(current_time)
            
            return should_check
            
        except Exception as e:
            logging.error(f"Error reading last check time: {e}")
            self._save_last_check_time(current_time)
            return True

    def _save_last_check_time(self, check_time: datetime):
        """Save the last update check time in human readable format."""
        try:
            with open(self.last_check_file, 'w') as f:
                f.write(check_time.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            logging.error(f"Error saving last check time: {e}")

    def _get_current_version(self) -> str:
        """Get current installed version."""
        version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                return f.read().strip()
        return "0.0.0"

    def _is_newer_version(self, latest: str, current: str) -> bool:
        """Compare version numbers."""
        latest = latest.lstrip('v').split('.')
        current = current.split('.')
        
        for l, c in zip(latest, current):
            if int(l) > int(c):
                return True
            elif int(l) < int(c):
                return False
        return len(latest) > len(current)

    def _extract_and_update(self, zip_path: str):
        """Extract and update files from zip."""
        import zipfile
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            zip_ref.extractall(temp_dir)
            
            # Copy new files
            extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            for item in os.listdir(extracted_dir):
                src = os.path.join(extracted_dir, item)
                dst = os.path.join(os.path.dirname(__file__), item)
                
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                else:
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    
            shutil.rmtree(temp_dir)

    def _update_version(self, version: str):
        """Update stored version number."""
        with open(os.path.join(os.path.dirname(__file__), 'version.txt'), 'w') as f:
            f.write(version.lstrip('v')) 

    def _get_last_check_time(self) -> str:
        """Get the last update check time in human readable format."""
        try:
            with open(self.last_check_file, 'r') as f:
                return f.read().strip()
        except:
            return "Never" 