from pathlib import Path

class VideoQueue:
    def __init__(self, videos: list[str]):
        self.__pos = 0
        self.__videos = [Path(p) for p in videos]
    
    def backward(self) -> Path:
        self.__pos += 1
        if self.__pos == len(self.__videos):
            self.__pos = 0
    
    def forward(self):
        self.__pos -= 1
        if self.__pos < 0:
            self.__pos = len(self.__videos) - 1
            
    @property
    def video(self):
        return self.__videos[self.__pos]
    
    @property 
    def video_str(self):
        return self.__videos[self.__pos].absolute().as_uri()
    
    @property
    def video_posix(self):
        return self.__videos[self.__pos].absolute().as_uri()