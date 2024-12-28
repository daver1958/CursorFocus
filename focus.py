import os
import time
from datetime import datetime
from config import load_config
from content_generator import generate_focus_content

def main():
    """Main function to generate and update the focus file."""
    config = load_config()
    if not config:
        print("Error: Could not load configuration")
        return

    project_path = config['project_path']
    if not project_path:
        print("Error: Project path not set in config.json")
        return

    print(f"🔍 CursorFocus is monitoring: {project_path}")
    print("📝 Press Ctrl+C to stop")

    # Create Focus.md in the project root directory
    focus_file = os.path.join(project_path, 'Focus.md')
    last_content = None
    last_update = 0

    try:
        while True:
            current_time = time.time()
            
            # Only check for updates every update_interval seconds
            if current_time - last_update < config['update_interval']:
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