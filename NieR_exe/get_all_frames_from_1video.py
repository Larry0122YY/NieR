import os.path
import TOOLS_COMMON as common

import cv2


def main():
    print("请将一个视频file拖进来:")
    video_file = common.input_file()
    print("请输入一个folder名，默认和video file在同一路径下，如果直接回车，则默认folder名为img：")
    select_folder_name = input()
    if select_folder_name == "":
        folder_name = "img"
    else:
        folder_name = select_folder_name

    output_folder_path = os.path.join(os.path.dirname(video_file), folder_name)
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    print("video_file:",video_file)
    print("output_folder_path:",output_folder_path)
    get_all_frames_from_1video_exe(video_path=video_file, output_folder=output_folder_path)


def get_all_frames_from_1video_exe(video_path, output_folder):
    video_cap = cv2.VideoCapture(video_path)

    frame_number = 0
    print("当前这个视频一共有" + str(video_cap.get(cv2.CAP_PROP_FRAME_COUNT)) + "帧")

    while True:
        ret, frame = video_cap.read()
        if ret:
            frame_number += 1
            img_path = os.path.join(output_folder, str(frame_number) + ".png")
            cv2.imwrite(img_path, frame)
        else:
            break
    print("解析完成！")
    print("我们这次只解析了前" + str(frame_number) + "帧的图片")

    video_cap.release()

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
