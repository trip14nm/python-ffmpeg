import os
import yaml

# 读配置
t = open('config.yaml', encoding='utf-8')
config = yaml.safe_load(t)
t.close()
subtitleStyle = config['subtitle']['subtitleStyle']
subtitleStyle_format = "'{}'".format(subtitleStyle)
subtitleSuffix = config['subtitle']['subtitleSuffix']
videoSuffixSet = config['videoSuffixSet']
decode = config['decode']
encode = config['encode']
threads = config['threads']
# 路径设置
curpath = os.getcwd()
inputDir = os.path.join(curpath, "input")
outputDir = os.path.join(curpath, "output")

# 获取视频列表
file_list = os.listdir(inputDir)

# 如果没有 ./output 这个文件夹，则创建这个文件夹
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

# 转码
for each_file in file_list:
    suffix = each_file.rsplit(".", 1)[-1].lower()
    if suffix in videoSuffixSet:
        videoName, _ = os.path.splitext(each_file)
        subtitleName = ("{name}.{suffix}".format(name=videoName, suffix=subtitleSuffix))
        subtitleFile = ('{indir}{sep}{subtitlename}'.format(sep=os.sep, indir=inputDir, subtitlename=subtitleName))
        subtitleName_format = "'{}'".format(subtitleName)
        print(subtitleFile)
        cdCommand = ('cd "{}"'.format(inputDir))
        if os.path.exists(subtitleFile):
            if config['subtitle']['customizeStyle']:
                ffmpegCommand = (
                    'ffmpeg {decode} -i "{filename}" -y -threads {threads} -vf "subtitles={subtitlename}:force_style={subtitlestyle}"'
                    ' {encode} "{outdir}{sep}{name}.mp4"'
                    .format(decode=decode, filename=each_file,
                            subtitlename=subtitleName_format, subtitlestyle=subtitleStyle_format,
                            encode=encode, threads=threads, outdir=outputDir, sep=os.sep, name=videoName))
            else:
                ffmpegCommand = (
                    'ffmpeg {decode} -i "{filename}" -y -threads {threads} -vf "subtitles={subtitlename}"'
                    ' {encode} "{outdir}{sep}{name}.mp4"'
                    .format(decode=decode, filename=each_file, subtitlename=subtitleName_format,
                            encode=encode, threads=threads, outdir=outputDir, sep=os.sep, name=videoName))
        else:
            ffmpegCommand = (
                'ffmpeg {decode} -i "{filename}" -y {encode} -threads {threads} "{outdir}{sep}{name}.mp4"'
                .format(decode=decode, filename=each_file,
                        encode=encode, threads=threads, outdir=outputDir, sep=os.sep, name=videoName))
        command = ('{} && {}'.format(cdCommand, ffmpegCommand))
        print(command)
        os.system(command)
os.system('pause')
