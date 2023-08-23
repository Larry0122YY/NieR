import numpy

import TOOLS_COMMON as common


def main():
    print("请拖入一个视频文件：")
    video_path = common.input_file()
    peak_amplitudes = common.get_peak_amplitudes(video_path)
    max_amplitudes_frame = numpy.argmax(peak_amplitudes)
    print("最大振幅点对应的那一个frame是第" + str(max_amplitudes_frame) + "帧")


if __name__ == '__main__':
    main()
