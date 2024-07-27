import argparse
import time
from handlers import MoveHandler
from watchdog.observers import Observer

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