import os

# 获取当前路径
curpath = os.getcwd()
input_dir = os.path.join(curpath, "input")
input_video_list = os.listdir(input_dir)

# 生成文件列表
file = open('filelist.txt', "r+")
file.truncate()
file = open('filelist.txt', 'w')
num = 0
for each_video in input_video_list:
    line = 'file "{}{}{}"\n'.format(input_dir, os.sep, each_video)
    print(line)
    file.write(line)
    if num:
        suffix = each_video.split(".")[1]
    num += 1
file.close()

# 执行合并
if len(input_video_list) == 0:
    print('文件夹为空')
else:
    ffmpegCommand = ("ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.{}".format(suffix))
    os.system(ffmpegCommand)
os.system('pause')
