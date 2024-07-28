import argparse
import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MoveHandler(FileSystemEventHandler):
    def __init__(self, source_path, target_path):
        self.source_path = source_path
        self.target_path = target_path
        self.stable_timeout = 1
    
    def on_modified(self, event):
        if event.is_directory:
            return None
        else:
            self.validate_file(event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return None
        else:
            self.validate_file(event.src_path)

    def validate_file(self, source_file_path):
        if not os.path.isfile(source_file_path):
            return

        stable = False
        initial_size = os.path.getsize(source_file_path)

        while not stable:
            time.sleep(self.stable_timeout)
            current_size = os.path.getsize(source_file_path)

            if current_size == initial_size:
                stable = True
            else:
                initial_size = current_size
        
        self.move_file(source_file_path)

    def move_file(self, source_file_path):
        relative_path = os.path.relpath(source_file_path, self.source_path)
        target_file_path = os.path.join(self.target_path, relative_path)

        target_path = os.path.dirname(target_file_path)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        try:
            shutil.move(source_file_path, target_file_path)
            print(f"Moved {source_file_path} to {target_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print(f"Failed to move {source_file_path} to {target_file_path}")

def main(source_path, target_path):
    event_handler = MoveHandler(source_path, target_path)

    observer = Observer()
    observer.schedule(event_handler, path=source_path, recursive=True)

    observer.start()
    print(f"Observing {source_path} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor a directory and move its contents to another directory")

    parser.add_argument("source", type=str, help="Path to the source directory to observe")
    parser.add_argument("target", type=str, help="Path to the target directory to move the contents to")

    args = parser.parse_args()

    main(args.source, args.target)