import os
import shutil
import time
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