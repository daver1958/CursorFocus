#!/usr/bin/env python3
import os
import json
import argparse

def setup_cursorfocus():
    """Set up CursorFocus for a project."""
    parser = argparse.ArgumentParser(description='Set up CursorFocus for your project')
    parser.add_argument('--project', '-p', help='Path to the project to monitor (default: parent directory)')
    parser.add_argument('--interval', '-i', type=int, help='Update interval in seconds (default: 60)')
    parser.add_argument('--depth', '-d', type=int, help='Maximum directory depth to scan (default: 3)')
    
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
    
    print("\n✅ CursorFocus configuration updated!")
    print(f"📁 Project path: {config['project_path'] or 'Parent directory'}")
    print(f"⏱️  Update interval: {config['update_interval']} seconds")
    print(f"🔍 Max depth: {config['max_depth']} levels")
    print("\nTo start monitoring, run:")
    print(f"python3 {os.path.join(script_dir, 'focus.py')}")

if __name__ == '__main__':
    setup_cursorfocus() 