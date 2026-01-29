from pathlib import Path

class VideoQueue:
    def __init__(self, videos: list[str]):
        self.__pos = 0
        self.__videos = [Path(p) for p in videos]
    
    def backward(self) -> None:
        self.__pos += 1
        if self.__pos == len(self.__videos):
            self.__pos = 0
    
    def forward(self) -> None:
        self.__pos -= 1
        if self.__pos < 0:
            self.__pos = len(self.__videos) - 1
            
    @property
    def video(self) -> Path:
        return self.__videos[self.__pos]
    
    @property 
    def video_str(self) -> Path:
        return self.__videos[self.__pos].absolute().as_uri()
    
    @property
    def video_posix(self) -> Path:
        return self.__videos[self.__pos].absolute().as_uri()

