#!/usr/bin/env python3
import os
import json
import argparse

def create_launch_agent(project_path, python_path='/usr/local/bin/python3'):
    """Create and install the LaunchAgent plist file."""
    # Get user's home directory
    home = os.path.expanduser('~')
    launch_agents_dir = os.path.join(home, 'Library/LaunchAgents')
    plist_path = os.path.join(launch_agents_dir, 'com.cursorfocus.plist')
    
    # Create LaunchAgents directory if it doesn't exist
    os.makedirs(launch_agents_dir, exist_ok=True)
    
    plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cursorfocus</string>
    <key>ProgramArguments</key>
    <array>
        <string>{python_path}</string>
        <string>{os.path.join(project_path, 'focus.py')}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{project_path}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{os.path.join(project_path, 'cursorfocus.log')}</string>
    <key>StandardErrorPath</key>
    <string>{os.path.join(project_path, 'cursorfocus.error.log')}</string>
</dict>
</plist>'''

    # Write the plist file
    with open(plist_path, 'w') as f:
        f.write(plist_content)
    
    # Set proper permissions
    os.chmod(plist_path, 0o644)
    
    # Load the launch agent
    os.system(f'launchctl load {plist_path}')
    
    return plist_path

def setup_cursorfocus():
    """Set up CursorFocus for a project."""
    parser = argparse.ArgumentParser(description='Set up CursorFocus for your project')
    parser.add_argument('--project', '-p', help='Path to the project to monitor (default: parent directory)')
    parser.add_argument('--interval', '-i', type=int, help='Update interval in seconds (default: 60)')
    parser.add_argument('--depth', '-d', type=int, help='Maximum directory depth to scan (default: 3)')
    parser.add_argument('--install-agent', '-a', action='store_true', help='Install LaunchAgent for automatic startup')
    parser.add_argument('--python-path', help='Path to Python interpreter (default: /usr/local/bin/python3)')
    
    args = parser.parse_args()
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')
    
    # Load existing config if it exists
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {
            "project_path": "",
            "update_interval": 60,
            "max_depth": 3,
            "ignored_directories": [
                "__pycache__",
                "node_modules",
                "venv",
                ".git",
                ".idea",
                ".vscode",
                "dist",
                "build"
            ],
            "ignored_files": [
                ".DS_Store",
                "*.pyc",
                "*.pyo"
            ]
        }
    
    # Update config with command line arguments
    if args.project:
        config["project_path"] = os.path.abspath(args.project)
    if args.interval:
        config["update_interval"] = args.interval
    if args.depth:
        config["max_depth"] = args.depth
    
    # Save the config
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    # Install LaunchAgent if requested
    if args.install_agent:
        try:
            if not os.path.exists('/usr/local/bin/python3'):
                print("⚠️  Warning: Default Python path not found. Please specify with --python-path")
                return
            
            python_path = args.python_path or '/usr/local/bin/python3'
            plist_path = create_launch_agent(os.path.dirname(os.path.abspath(__file__)), python_path)
            print(f"\n✅ LaunchAgent installed at: {plist_path}")
            print("CursorFocus will now start automatically at login")
            print("\nTo start now:")
            print(f"$ launchctl load {plist_path}")
            print("\nTo stop:")
            print(f"$ launchctl unload {plist_path}")
        except Exception as e:
            print(f"\n❌ Error installing LaunchAgent: {e}")
            print("Please check permissions and try again")
    
    print("\n✅ CursorFocus configuration updated!")
    print(f"📁 Project path: {config['project_path'] or 'Parent directory'}")
    print(f"⏱️  Update interval: {config['update_interval']} seconds")
    print(f"🔍 Max depth: {config['max_depth']} levels")
    print("\nTo start monitoring, run:")
    print(f"python3 {os.path.join(script_dir, 'focus.py')}")

if __name__ == '__main__':
    setup_cursorfocus() 