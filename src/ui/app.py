from pathlib import Path
from typing import Iterable
from rich.text import Text
from textual import work
from textual.worker import Worker, get_current_worker
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, HorizontalGroup
from textual.widgets import Header, Footer, Log, RichLog, Static, Button
from textual.events import Resize
from toascii import Video, ColorConverter, GrayscaleConverter, ConverterOptions, gradients, FrameClearStrategy

from models.video_queue import VideoQueue
from models.video_configuration import VideoConfiguration

class VideoApp(App):

    CSS_PATH='app.tcss'
    COMMANDS = App.COMMANDS
    
    SCROLL_BINDING_GROUP=Binding.Group(description='scroll')
    BINDINGS = [
        Binding(key='j,up', action='next_video', description='navigates to the next video',
                group=SCROLL_BINDING_GROUP),
        Binding(key='k,down', action='previous_video', description='navigates to the next video',
                group=SCROLL_BINDING_GROUP),
        Binding(key='c', action='toggle_color', description='enable or disable color')
    ]

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
            and self.__queue is not None
            and self.video_widget is not None):

            self.__video_configuration.path = self.__queue.video 
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
                    yield Button(label='Previous Video', id="PreviousVideo", action="previous_video")
                    yield Button(label='Next Video', id="NextVideo", action="next_video")
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
        
        worker = get_current_worker()
        
        for f in self.__video_configuration.video.get_ascii_frames():
            if worker.is_cancelled:
                break
            self.call_from_thread(self.video_widget.update, Text.from_ansi(f))
            
    def action_next_video(self) -> None:
        # self.notify('next video')
        self.__queue.forward()
        self.__refresh_video()
    
    def action_previous_video(self) -> None:
        # self.notify('previous video')
        self.__queue.backward()
        self.__refresh_video()
        
    def action_toggle_color(self) -> None:
        self.__video_configuration.color = not self.__video_configuration.color
        self.__refresh_video()

