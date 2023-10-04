import logging
import os
from pathlib import Path

from flask import Flask, Response
from flask_socketio import SocketIO
from watchdog.events import FileSystemEvent, RegexMatchingEventHandler
from watchdog.observers import Observer

from utilities.jemdoc_mediator import (
    WORKING_DIR,
    compile_all_jemdoc_files,
    compile_jemdoc_file,
    copy_default_css_file,
)

app = Flask(__name__)
socketio = SocketIO(app)

# Configuration
SERVER_PORT = int(os.environ.get("SERVER_PORT", 5000))


class JemdocHandler(RegexMatchingEventHandler):
    def __init__(self):
        # Only react to .jemdoc files.
        super().__init__(regexes=[r".*\.jemdoc$"])

    def on_modified(self, event: FileSystemEvent):
        logging.info(event.src_path)
        compile_jemdoc_file(Path(event.src_path))
        socketio.emit("reload")

    def on_created(self, event: FileSystemEvent):
        logging.info(event.src_path)
        compile_jemdoc_file(Path(event.src_path))
        socketio.emit("reload")


@app.route("/")
def home() -> Response:
    return _send_file_with_injected_reloading("index.html")


@app.route("/<path:path>")
def send_jemdoc(path: str) -> Response:
    return _send_file_with_injected_reloading(path)


def _send_file_with_injected_reloading(filename: str):
    with open(os.path.join(WORKING_DIR, filename), "r", encoding="utf-8") as f:
        content = f.read()

    if filename.endswith(".html"):
        # Insert JavaScript for live-reload before </body>
        modified_content = content.replace(
            "</body>",
            """
            <script src='http://127.0.0.1:5000/4.7.2_socket.io.min.js'></script>
            <script>
                var socket = io.connect('http://' + document.domain + ':' + location.port);
                socket.on('reload', function() {
                    location.reload();
                });
            </script>
        </body>""",
        )

        return Response(modified_content, content_type="text/html")
    return content


if __name__ == "__main__":
    WORKING_DIR.mkdir(exist_ok=True)
    copy_default_css_file()
    compile_all_jemdoc_files()
    event_handler = JemdocHandler()
    observer: Observer = Observer()
    logging.info(f"Watching directory {WORKING_DIR}")
    observer.schedule(event_handler, str(WORKING_DIR), recursive=False)
    observer.start()

    logging.info(f"Starting server on port {SERVER_PORT}...")
    try:
        socketio.run(app, debug=True, host="127.0.0.1")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
