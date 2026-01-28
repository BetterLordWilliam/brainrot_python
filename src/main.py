from sys import stdout
from pathlib import Path
from argparse import *

from models.video_configuration import VideoConfiguration
from models.video_queue import VideoQueue
from ui.app import VideoApp

if __name__ == '__main__':
    """
    spin up a seperate thread to process the video

    make it call a method in that clears the log & flushes the
    frame to the log via write lines

    actually there are built-in textual workers that can be used for this purpose...

    TODO :    

    Questions that need answering
    - [X] scale the video while it is being procesed (like per frame of the generators execution)?
        sort of 
        
    - streaming video from insta reels into the converter
        find some API that will let us take video from the internet that are memes
        meme api
    - [X] the rest of the interface, reels copy but in the terminal
        sort of 
        
    - [ ] feed the application a set of videos and be able to navigate forwards and backwards through them
    - [ ] make the video player its own separate widget
    - [ ] instead of loading video from a file on the file system, internet download and stream the downloaded video converted frames into the widget

    """

    args = ArgumentParser(
        prog='brainrot',
        description='this program lets you scroll brainrot in the terminal'
    )
    args.add_argument('-v', '--video-path',
        help="video path, ex. \'/my/dir/video.mp4\'",
        nargs='+',
        required=True
    )
    pargs = args.parse_args()

    video_queue = VideoQueue(pargs.video_path)
    video_configuration = VideoConfiguration()
    
    # video_configuration.path = Path(pargs.video_path)

    app = VideoApp(video_queue, video_configuration)
    app.run()
