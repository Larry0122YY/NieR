import os.path

import TOOLS_COMMON as common
import matplotlib.pyplot as plt


def main():
    print("请拖入一个视频文件：")
    video_path = common.input_file()
    print("请输入输出的png的名字，默认放在和video同一个路径下，直接回车名字和video一样：")
    select_filename = input()
    if select_filename == "":
        output_file_path = common.switch_ext(video_path, ".png")
    else:
        output_file_path = os.path.join(os.path.dirname(video_path), select_filename + ".png")

    print("output_file_path:"+output_file_path)
    peak_amplitudes = common.get_peak_amplitudes(video_path)

    save_pic_and_show(peak_amplitudes, output_file_path)


def save_pic_and_show(peak_amplitudes, output_file_path):
    # 创建一个图形
    plt.figure()

    # 绘制数据
    plt.plot(peak_amplitudes)

    # 设置标题和轴标签
    plt.title('Peak Amplitudes')
    plt.xlabel('frame')
    plt.ylabel('Amplitude')

    # 保存图形到文件
    plt.savefig(output_file_path, dpi=300)  # dpi指定输出图片的分辨率

    # 显示图形
    plt.show()


if __name__ == '__main__':
    main()
