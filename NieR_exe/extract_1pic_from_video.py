import os.path

import cv2

import TOOLS_COMMON as common


def main():
    print("请输入一个video的全路径：")
    video_path = common.input_file()
    print("请输入，想取第几帧的图片？")
    frame_num = common.input_digital_and_none()
    if frame_num == "":
        frame_no = 1
    else:
        frame_no = int(frame_num)

    extract_1_pic(video_path, frame_no)


# 抽出video某帧的图片，下面3个参数分别表示：目标video的全路径；第几帧？；这帧输出的路径
def extract_1_pic(video_path, frame_no):
    # 用和视频同path的png格式的形式，当作此帧的输出路径，名字为帧号
    output_png_file = os.path.join(os.path.dirname(video_path), str(frame_no) + ".png")
    print("output_png_file:", output_png_file)

    # 读取视频文件
    cap = cv2.VideoCapture(video_path)

    # 设置帧号(视频的帧数是从0开始算起的，所以，你想要第100帧，这里需要输入100-1)
    cap.set(1, frame_no - 1)

    # 开始读这一帧
    ret, frame = cap.read()

    # 如果这帧存在
    if ret:
        # 写出照片
        cv2.imwrite(output_png_file, frame)
        print("图片生成完成！")
    else:
        print("输入的帧号不存在")

    # 关闭视频文件流
    cap.release()


if __name__ == '__main__':
    main()
