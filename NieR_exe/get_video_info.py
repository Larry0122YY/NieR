import TOOLS_COMMON as common


def main():
    print("请拖入一个视频文件,将给出这个视频的fps,resolution,frames的信息：")
    video_path = common.input_file()
    fps,resolution,frames = common.get_fps_resolution_allFrames(video_path)
    print("=========================")
    print("fps:"+str(fps))
    print("resolution:"+str(resolution))
    print("frames:"+str(frames))
    print("=========================")

if __name__ == '__main__':
    main()