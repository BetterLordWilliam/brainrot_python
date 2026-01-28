from pathlib import Path
from toascii import gradients, FrameClearStrategy

class VideoConfiguration:
    def __init__(self):
        self.__gradient = gradients.LOW
        self.__frame_clear_strategy = FrameClearStrategy.ANSI_CURSOR_POS
        self.__fps = 30
        self.__width = 0
        self.__height = 0
        self.__path = Path()

    @property
    def gradient(self) -> str:
        return self.__gradient
    
    @property
    def frame_clear_strategy(self) -> FrameClearStrategy:
        return self.__frame_clear_strategy
    
    @property
    def fps(self) -> int:
        return self.__fps
    
    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width
    
    @property
    def height(self) -> int:
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height

    @property
    def path(self) -> Path:
        return self.__path
    
    @property
    def path_str(self) -> str:
        return self.__path.absolute().as_uri()
    
    @property
    def path_posix(self) -> str:
        return self.__path.absolute().as_posix()

    @path.setter
    def path(self, path: Path) -> None:
        self.__path = path
