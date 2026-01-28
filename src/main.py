from sys import stdout
from pathlib import Path
from argparse import *
from threading import Thread, ThreadError
from queue import Queue
from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Log, RichLog, Static
from textual.events import Resize
from toascii import Video, ColorConverter, GrayscaleConverter, ConverterOptions, gradients, FrameClearStrategy


class VideoApp(App):

    CSS="""
#VideoAppLogContainer {
    height: 100%; width: 100%;
}
#VideoAppRender {
    height: 90%;
}
#VideoAppLog {
    height: 10%;
}
"""

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

        self.run_worker(self.process_video, thread=True, exclusive=True)

    def on_resize(self, event: Resize):
        try:
            self.log_widget.write_line('resize has occured')
            # self.workers.cancel_all()
            self.log_widget.write_line(f'{self.workers.__len__}')
        except:
            print('not logging widget')

    def process_video(self):
        video_path = self._path
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
            self.call_from_thread(self.video_widget.update, Text.from_ansi(f, no_wrap=True))


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

    app = VideoApp(video_path)
    app.run()
