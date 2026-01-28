from toascii import Video, ColorConverter, ConverterOptions, gradients

TEST_VIDEO_PATH = '../example_video/fisch.mp4'

def main():
    # TODO : Determine the host size & use that in the options
    converter_opts = ConverterOptions(
        gradient=gradients.HIGH,
        width=100,
        height=100
    )
    converter = ColorConverter(converter_opts)
    video = Video(source=TEST_VIDEO_PATH,
                  converter=converter,
                  fps=30,
                  loop=False)
    video.view()

if __name__ == '__main__':
    main()
