from pathlib import Path
from toascii import gradients, FrameClearStrategy, ConverterOptions, Video, GrayscaleConverter, ColorConverter, HtmlColorConverter

class VideoConfiguration:
    def __init__(self):
        self.__frame_clear_strategy = FrameClearStrategy.ANSI_CURSOR_POS
        self.__fps = 30
        self.__path = Path()
        self.__loop = False
        self.__color = False # this is slower than grayscale noticeably
        self.__conv_opts = ConverterOptions(
            gradient=gradients.LOW, # unchanging for now
            width = 1,
            height = 1,
        )
        self.__gr_conv = GrayscaleConverter(self.__conv_opts)
        self.__cl_conv = ColorConverter(self.__conv_opts)

    @property
    def frame_clear_strategy(self) -> FrameClearStrategy:
        return self.__frame_clear_strategy
    
    @frame_clear_strategy.setter
    def frame_clear_strategy(self, fcs: FrameClearStrategy) -> None:
        self.__frame_clear_strategy = fcs
    
    @property
    def fps(self) -> int:
        return self.__fps
    
    @property
    def width(self) -> int:
        return self.__conv_opts.width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__conv_opts.width = width
    
    @property
    def height(self) -> int:
        return self.__conv_opts.height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__conv_opts.height = height

    @property
    def path(self) -> Path:
        return self.__path
    
    @path.setter
    def path(self, path: Path) -> None:
        self.__path = path
    
    @property
    def path_str(self) -> str:
        return self.__path.absolute().as_uri()
    
    @property
    def path_posix(self) -> str:
        return self.__path.absolute().as_posix()

    @path.setter
    def path(self, path: Path) -> None:
        self.__path = path
        
    @property
    def color(self) -> bool:
        return self.__color
    
    @color.setter
    def color(self, color: bool) -> bool:
        self.__color = color
        
    @property
    def video(self) -> Video:
        converter = self.__gr_conv if not self.__color else self.__cl_conv
        return Video(
            source=self.path_str,
            converter=converter,
            fps=self.__fps,
            loop=self.__loop
        )
        
