import os.path
import shutil

import cv2
from docx2pdf import convert

import TOOLS_COMMON as common
from moviepy.editor import *
import romkan


def main():
    text_rom = "arigatou"
    rom_to_hira = romkan.to_hiragana(text_rom)
    rom_to_kata = romkan.to_katakana(text_rom)
    print("rom_to_hira:", rom_to_hira)
    print("rom_to_kata:", rom_to_kata)

    print("=====================")
    text_hinagara = "しょうじょう"
    text_katagara = "エンヤ"
    hira_to_rom = romkan.to_roma(text_hinagara)
    kata_to_rom = romkan.to_roma(text_katagara)
    print("hira_to_rom:",hira_to_rom)
    print("kata_to_rom:",kata_to_rom)

    pass


def search():
    path = "F:\\animeAV"
    keyword = " セクフレ幼馴染～処女と童貞は恥ずかしいってみんなが言うから"
    temp = os.walk(path)
    for i in temp:
        for file in i[2]:
            if keyword in file:
                file_path = os.path.join(i[0], file)
                print(file_path)


def get_all_frames_from_1video_exe(video_path, output_folder):
    video_cap = cv2.VideoCapture(video_path)

    frame_number = 0
    print("当前这个视频一共有" + str(video_cap.get(cv2.CAP_PROP_FRAME_COUNT)) + "帧")

    while True:
        ret, frame = video_cap.read()
        if ret:
            frame_number += 1
            img_path = os.path.join(output_folder, str(frame_number) + ".png")
            print("img_path:", str(img_path))
            cv2.imwrite(img_path, frame)
        else:
            break
    print("解析完成！")
    print("我们这次只解析了前" + str(frame_number) + "帧的图片")

    video_cap.release()

    cv2.destroyAllWindows()


def make_audio_file(video_path, audio_name_no_ext):
    if audio_name_no_ext == "":
        audio_name = os.path.splitext(os.path.basename(video_path))[0] + ".wav"
    else:
        audio_name = audio_name_no_ext + ".wav"

    # 拿到video文件的父路径
    work_space = os.path.dirname(video_path)
    # 在和video的同路径下，拿到新的音频文件全路径对象audio_path
    audio_path = os.path.join(work_space, audio_name)

    print("audio_path:", audio_path)

    # 创建video对象
    video = VideoFileClip(video_path)
    # 通个video对象，获取audio对象
    audio = video.audio
    # 写出audio的音频
    audio.write_audiofile(audio_path)


# 音频文件同名txt文件
def make_txt(audio_folder):
    for file in os.listdir(audio_folder):
        if file.endswith("wav"):
            cur_full_path_file = os.path.join(audio_folder, os.path.splitext(file)[0] + ".txt")
            new_file = open(cur_full_path_file, "w")
            print(new_file)


# 将pictures放入一个文件夹中
def put_pic_to_folder():
    path = "D:\\download\\h"
    for file in os.listdir(path):
        if file.endswith("jpg"):
            cur_file = os.path.join(path, file)
            folder = os.path.join(path, "jpg")
            shutil.move(cur_file, folder)


# 将以前的excel里的01A之类的给去掉，变成单纯的serif
def extract_to_pure_serif(path):
    # path = "C:\\Users\\Administrator\\Desktop\\aaa.txt"
    # out_path = "C:\\Users\\Administrator\\Desktop\\bbb.txt"
    out_path = os.path.join(os.path.dirname(path), os.path.splitext(os.path.basename(path))[0] + "_serif" + ".txt")
    print(out_path)
    out_file = open(out_path, "w", encoding="utf-8")
    out_str = ""

    file = open(path, "r", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        if line != "" and not line[0:2].isdigit() and not line.startswith("\t") and not line.startswith("\n"):
            out_str += line

    print(out_str)
    out_file.write(out_str)


def test():
    path = "C:\\Users\\Administrator\\Desktop\\aaa.txt"
    file = open(path, "r", encoding="utf-8")
    lines = file.readline()
    for line in lines:
        if line.startswith("\n"):
            print("ssssssss")


if __name__ == '__main__':
    main()

# new_ext = ".pdf"


# convert(file_path, out_path)

# folder_path = "C:\\Users\\Administrator\\Desktop\\serif"
#
# for file in os.listdir(folder_path):
#     if file.endswith("txt"):
#         cur_file_full_path = os.path.join(folder_path,file)
#         extract_to_pure_serif(cur_file_full_path)
# put_pic_to_folder()
# test()
# extract_to_pure_serif()
# make_txt(path)
# path = "D:\\OneDrive\\日本語\\EP04"
#
# temp = os.walk(path)
# for i in temp:
#     for file in i[2]:
#         if file == "Original Serif.txt":
#             cur_path = os.path.join(i[0], file)
#             print(cur_path)

# for file in os.listdir(path):
#     if file.endswith(".wav"):
#         cur_full_path = os.path.join(path,file)
#         new_file_path = os.path.join(path,"audio",file)
#         os.rename(cur_full_path,new_file_path)


# video_path = "C:\\Users\\Administrator\\Desktop\\video_test\\01.厨师们想修新建筑.mkv"
# output_path = "C:\\Users\\Administrator\\Desktop\\video_test\\img"

# cap = cv2.VideoCapture(video_path)
# ret,frame = cap.read()
# cv2.imwrite(output_path,frame)
# if not os.path.exists(output_path):
#     os.mkdir(output_path)
# get_all_frames_from_1video_exe(video_path,output_path)


# get_all_frames_from_1video_exe()
