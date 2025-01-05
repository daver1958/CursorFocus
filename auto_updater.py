import os
import requests
import json
import shutil
from datetime import datetime, timezone
import logging
from typing import Optional, Dict, Any
import tempfile
import zipfile

class AutoUpdater:
    def __init__(self, repo_url: str = "https://github.com/RenjiYuusei/CursorFocus"):
        self.repo_url = repo_url
        self.api_url = repo_url.replace("github.com", "api.github.com/repos")
        self.last_check_file = os.path.join(os.path.dirname(__file__), '.last_update_check')
        self.update_interval = 24 * 60 * 60  # 24 hours in seconds

    def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Check update from latest update"""
        try:
            if not self._should_check_updates():
                last_check = self._get_last_check_time()
                print(f"Last check: {last_check}")
                return None

            response = requests.get(f"{self.api_url}/commits/main")
            if response.status_code == 404:  
                response = requests.get(f"{self.api_url}/commits/master")
            
            if response.status_code != 200:
                return None

            latest_commit = response.json()
            current_commit = self._get_current_commit()
            
            if latest_commit['sha'] != current_commit:
                # Convert UTC time to local time
                utc_date = datetime.strptime(
                    latest_commit['commit']['author']['date'], 
                    "%Y-%m-%dT%H:%M:%SZ"
                )
                local_date = utc_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
                formatted_date = local_date.strftime("%B %d, %Y at %I:%M %p")
                
                return {
                    'sha': latest_commit['sha'],
                    'message': latest_commit['commit']['message'],
                    'date': formatted_date,
                    'author': latest_commit['commit']['author']['name'],
                    'download_url': f"{self.repo_url}/archive/refs/heads/main.zip"
                }
            
            return None

        except Exception as e:
            logging.error(f"Error checking for updates: {e}")
            return None

    def _get_current_commit(self) -> str:
        """Get the SHA of the current commit."""
        try:
            version_file = os.path.join(os.path.dirname(__file__), '.current_commit')
            if os.path.exists(version_file):
                with open(version_file, 'r') as f:
                    return f.read().strip()
            return ''
        except:
            return ''

    def update(self, update_info: Dict[str, Any]) -> bool:
        """Update from latest commit."""
        try:
            # Download zip file of branch
            response = requests.get(update_info['download_url'])
            if response.status_code != 200:
                return False

            # Save zip file temporarily
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, 'update.zip')
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            # Unzip and update
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get root directory name in zip
                root_dir = zip_ref.namelist()[0].split('/')[0]
                zip_ref.extractall(temp_dir)

                # Copy new files
                src_dir = os.path.join(temp_dir, root_dir)
                dst_dir = os.path.dirname(__file__)
                
                for item in os.listdir(src_dir):
                    s = os.path.join(src_dir, item)
                    d = os.path.join(dst_dir, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                    elif os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)

            # Save SHA of new commit
            with open(os.path.join(dst_dir, '.current_commit'), 'w') as f:
                f.write(update_info['sha'])

            # Clean up
            shutil.rmtree(temp_dir)
            return True

        except Exception as e:
            logging.error(f"Error updating: {e}")
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

    def _get_last_check_time(self) -> str:
        """Get the last update check time in human readable format."""
        try:
            with open(self.last_check_file, 'r') as f:
                return f.read().strip()
        except:
            return "Never" 