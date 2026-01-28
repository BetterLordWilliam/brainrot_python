from pathlib import Path
from rich.text import Text
from textual import work
from textual.worker import Worker, get_current_worker
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Log, RichLog, Static
from textual.events import Resize
from toascii import Video, ColorConverter, GrayscaleConverter, ConverterOptions, gradients, FrameClearStrategy


class VideoApp(App):

    CSS_PATH='app.tcss'

    def __init__(self, path: Path):
        super().__init__()
        self._path = path
        self.title = 'brainrot'

    def compose(self) -> ComposeResult:
        with Container(id="VideoAppMain"):
            yield Header()
            with Container(id="VideoAppLogContainer"):
                yield Static(id="VideoAppRender")
                yield Log(id="VideoAppLog")
            yield Footer()

    def on_mount(self):
        self.video_widget = self.query_one("#VideoAppRender", Static)
        self.log_widget = self.query_one("#VideoAppLog", Log)
        self.process_video()

    def on_resize(self, event: Resize):
        try:
            self.workers.cancel_all()
            self.process_video()
        except:
            pass

    @work(exclusive=True, thread=True)
    def process_video(self):
        worker = get_current_worker()
        video_path_str = self._path.absolute().as_uri()
        conv_opts = ConverterOptions(
            gradient=gradients.LOW,
            width=self.video_widget.size.width,
            height=self.video_widget.size.height
        )
        conv = GrayscaleConverter(conv_opts)
        v = Video(
            source=video_path_str,
            converter=conv,
            frame_clear_strategy=FrameClearStrategy.ANSI_CURSOR_POS
        )
        vg = v.get_ascii_frames()
        for f in vg:
            self.call_from_thread(self.video_widget.update, Text.from_ansi(f))
            if worker.is_cancelled:
                break
