from sys import stdout
from pathlib import Path
from argparse import *

from models.video_configuration import VideoConfiguration
from ui.app import VideoApp

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

    video_configuration = VideoConfiguration()
    video_configuration.path = Path(pargs.video_path)

    app = VideoApp(video_configuration)
    app.run()
