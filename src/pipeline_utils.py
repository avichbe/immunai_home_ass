import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config

# --- Generic Event Handler ---
class GenericFileEventHandler(FileSystemEventHandler):
    """
    A generic file event handler that triggers a callback when a new file is created.
    """
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.logger = logging.getLogger("GenericFileEventHandler")

    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(config.FILE_EXTENSION):
            self.logger.info(f"Detected new file: {event.src_path}")
            self.callback(event.src_path)

# --- Pipeline Watcher ---
class PipelineWatcher:
    """
    Watches a specified directory and calls a provided callback when new files appear.
    """
    def __init__(self, directory, callback, recursive=False):
        self.directory = directory
        self.callback = callback
        self.recursive = recursive
        self.observer = Observer()
        self.event_handler = GenericFileEventHandler(self.callback)
        self.logger = logging.getLogger("PipelineWatcher")

    def start(self):
        self.observer.schedule(self.event_handler, path=self.directory, recursive=self.recursive)
        self.observer.start()
        self.logger.info(f"Started watching directory: {self.directory}")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.logger.info(f"Stopped watching directory: {self.directory}")

# --- Pipeline Orchestrator ---
class PipelineOrchestrator:
    """
    Orchestrates the entire pipeline by creating watchers for each stage.
    """
    def __init__(self, raw_dir, stage1_dir, stage2_dir,
                 process_raw_callback, process_stage1_callback, process_stage2_callback):
        self.logger = logging.getLogger("PipelineOrchestrator")
        self.watcher_raw = PipelineWatcher(raw_dir, process_raw_callback)
        self.watcher_stage1 = PipelineWatcher(stage1_dir, process_stage1_callback)
        self.watcher_stage2 = PipelineWatcher(stage2_dir, process_stage2_callback)

    def run(self):
        self.logger.info("Starting all pipeline watchers")
        self.watcher_raw.start()
        self.watcher_stage1.start()
        self.watcher_stage2.start()

    def stop_all(self):
        self.logger.info("Stopping all pipeline watchers")
        self.watcher_raw.stop()
        self.watcher_stage1.stop()
        self.watcher_stage2.stop()
