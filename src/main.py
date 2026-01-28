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
        self._video_path_bytes = path.read_bytes()
        self._conv_opts = ConverterOptions(
            gradient=gradients.LOW,
            width=100,
            height=100
        )
        self._conv = GrayscaleConverter(self._conv_opts)
        self._video = Video(
            source=self._video_path_bytes,
            converter=self._conv,
            fps=30,
            loop=True,
            frame_clear_strategy=FrameClearStrategy.ANSI_CURSOR_POS
        )


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
        vg = self.__ve._video.get_ascii_frames()
        for f in vg:
            self.call_from_thread(self.log_widget.update, f)


if __name__ == '__main__':
    # main()

    """
    spin up a seperate thread to process the video

    make it call a method in that clears the log & flushes the
    frame to the log via write lines

    """

    args = ArgumentParser(
        prog='brainrot',
        description='this program lets you scroll brainrot in the terminal'
    )
    args.add_argument('-v', '--video-path',
        help="video path, ex. \'/my/dir/video.p4\'",
        required=True
    )

    pargs = args.parse_args()

    video_path = Path(pargs.video_path)

    print(video_path)

    engine = VideoConfig(video_path)
    app = VideoApp(engine)
    app.run()
