import os.path
from moviepy.editor import *
import TOOLS_COMMON as common


def main():
    print("请将您想处理的video拖进来：")
    video_path = common.input_path()
    print("输入音频名：(直接回车的话，和video名一样)")
    audio_name = input()

    make_audio_file(video_path, audio_name)


def make_audio_file(video_path, audio_name_no_ext):
    if audio_name_no_ext == "":
        audio_name = os.path.splitext(os.path.basename(video_path))[0] + ".wav"
    else:
        audio_name = audio_name_no_ext + ".wav"

    # 拿到video文件的父路径
    work_space = os.path.dirname(video_path)
    # 在和video的同路径下，拿到新的音频文件全路径对象audio_path
    audio_path = os.path.join(work_space, audio_name)

    print("audio_path:",audio_path)

    # 创建video对象
    video = VideoFileClip(video_path)
    # 通个video对象，获取audio对象
    audio = video.audio
    # 写出audio的音频
    audio.write_audiofile(audio_path)


if __name__ == '__main__':
    main()
