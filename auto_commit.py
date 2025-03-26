import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GitAutoCommitHandler(FileSystemEventHandler):
    def commit_changes(self):
        # Stage all changes
        subprocess.call(["git", "add", "."])
        # Create a commit message with a timestamp
        commit_message = f"Auto commit: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        # Commit changes; if there's nothing to commit, this will fail gracefully
        commit_result = subprocess.call(["git", "commit", "-m", commit_message])
        if commit_result == 0:
            # If commit was successful, push the changes
            subprocess.call(["git", "push", "origin", "main"])
            print(f"{commit_message} - Changes pushed to GitHub.")
        else:
            print("No changes to commit.")

    def on_modified(self, event):
        self.commit_changes()

    def on_created(self, event):
        self.commit_changes()

if __name__ == "__main__":
    path = "."  # Monitor the current directory recursively
    event_handler = GitAutoCommitHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Monitoring for changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
