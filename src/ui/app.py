from pathlib import Path
from typing import Iterable
from rich.text import Text
from textual import work
from textual.worker import Worker, get_current_worker
from textual.app import App, ComposeResult
from textual.containers import Container, Grid, HorizontalGroup
from textual.widgets import Header, Footer, Log, RichLog, Static, Button
from textual.events import Resize
from toascii import Video, ColorConverter, GrayscaleConverter, ConverterOptions, gradients, FrameClearStrategy

from models.video_queue import VideoQueue
from models.video_configuration import VideoConfiguration

class VideoApp(App):

    CSS_PATH='app.tcss'
    COMMANDS = App.COMMANDS

    def __init__(self, queue: VideoQueue, conf: VideoConfiguration):
        super().__init__()
        self.__queue = queue
        self.__video_configuration = conf
        self.title = 'brainrot'

    def __video_ready_state(self) -> bool:
        video_configuration = self.__video_configuration
        return bool(
            video_configuration is not None
            and video_configuration.path
            and ( video_configuration.fps > 0
                and video_configuration.width > 0
                and video_configuration.height > 0 ) )

    def __update_configuration(self) -> None:
        if (self.__video_configuration is not None
            and self.video_widget is not None):

            self.__video_configuration.width    = self.video_widget.size.width
            self.__video_configuration.height   = self.video_widget.size.height
           
    def __refresh_video(self) -> None:
        self.__update_configuration()
        
        self.workers.cancel_all()
        self.process_video()
            
    def compose(self) -> ComposeResult:
        with Container(id="VideoAppMain"):
            yield Header()
            with Container(id="VideoAppOuterContainer"):
                with Container(id='VideoAppInnerContainer'):
                    yield Static(id="VideoAppRender")
                with Container(id='VideoButtonContainer'):
                    yield Button('Previous Video', id="PreviousVideo")
                    yield Button('Next Video', id="NextVideo")
                # yield Log(id="VideoAppLog")
            yield Footer()

    def on_mount(self):
        self.video_widget = self.query_one("#VideoAppRender", Static)
        # self.log_widget = self.query_one("#VideoAppLog", Log)
        
    def on_ready(self):
        try:
            self.__refresh_video()
        except:
            pass
        
    def on_resize(self, event: Resize):
        try:
            self.__refresh_video()
        except:
            pass

    @work(exclusive=True, thread=True)
    def process_audio(self):
        pass

    @work(exclusive=True, thread=True)
    def process_video(self):
        video_queue = self.__queue
        video_configuration = self.__video_configuration
        
        worker = get_current_worker()
        
        conv_opts = ConverterOptions(
            gradient=video_configuration.gradient,
            width=video_configuration.width,
            height=video_configuration.height
        )
        conv = GrayscaleConverter(conv_opts)
        v = Video(
            converter=conv,
            source=video_queue.video_str,
            fps=video_configuration.fps,
            frame_clear_strategy=video_configuration.frame_clear_strategy
        )
        
        vg = v.get_ascii_frames()
        for f in vg:
            self.call_from_thread(self.video_widget.update, Text.from_ansi(f))
            if worker.is_cancelled:
                break
            

