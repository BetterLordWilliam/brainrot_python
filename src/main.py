from sys import stdout
from pathlib import Path
from argparse import *
from threading import Thread, ThreadError
from queue import Queue
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Log, RichLog, Static
from toascii import Video, ColorConverter, GrayscaleConverter, ConverterOptions, gradients, FrameClearStrategy

TEST_VIDEO_PATH = 'example_video/fisch.mp4'


class VideoConfig():
    def __init__(self, path: Path):
        self._video_path = path
        self._video_path_str = path.absolute().as_uri()
        self._conv_opts = ConverterOptions(
            gradient=gradients.LOW,
            width=150,
            height=70
        )
        self._conv = GrayscaleConverter(self._conv_opts)


class VideoApp(App):

    def __init__(self, engine: VideoConfig):
        super().__init__()
        self.__ve = engine
        self.title = 'brainrot'

    def compose(self) -> ComposeResult:
        with Container(id="VideoAppMain"):
            yield Header()
            with Container(id="VideoAppLogContainer"):
                yield Static(id="VideoAppLog")
            yield Footer()

    def on_mount(self):
        self.log_widget = self.query_one("#VideoAppLog", Static)
        self.run_worker(self.process_video, thread=True)

    def process_video(self):
        v = Video(
            source=self.__ve._video_path_str,
            converter=self.__ve._conv,
            fps=30,
            loop=False,
            frame_clear_strategy=FrameClearStrategy.ANSI_CURSOR_POS
        )
        vg = v.get_ascii_frames()
        for f in vg:
            self.call_from_thread(self.log_widget.update, f)


if __name__ == '__main__':
    """
    spin up a seperate thread to process the video

    make it call a method in that clears the log & flushes the
    frame to the log via write lines

    actually there are built-in textual workers that can be used for this purpose...

    TODO :    

    Questions that need answering
    - scale the video while it is being procesed (like per frame of the generators execution)?
    - streaming video from insta reels into the converter
    - the rest of the interface, reels copy but in the terminal

    """

    args = ArgumentParser(
        prog='brainrot',
        description='this program lets you scroll brainrot in the terminal'
    )
    args.add_argument('-v', '--video-path',
        help="video path, ex. \'/my/dir/video.mp4\'",
        required=True
    )
    pargs = args.parse_args()

    video_path = Path(pargs.video_path)

    print(video_path)

    engine = VideoConfig(video_path)
    app = VideoApp(engine)
    app.run()
