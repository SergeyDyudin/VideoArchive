import os
import subprocess

"""Для вычисление битрейта и длительности файла, необходимо, чтобы был установлен MediaInfo_CLI в Program Files.
"""


def audio_bitrate(file_name):
    command = ''"C:\Program Files\MediaInfo_CLI\MediaInfo.exe " "--Inform=Audio;%%BitRate%% " "%s"'' %(file_name)
    audio_bit = subprocess.check_output(command)
    if audio_bit == b'\r\n':
        audio_bit = 'None'
    else:
        audio_bit = int(audio_bit.decode())
        audio_bit = int(audio_bit/1000)
    return audio_bit


def video_bitrate(file_name):
    command = ''"C:\Program Files\MediaInfo_CLI\MediaInfo.exe " "--Inform=Video;%%BitRate%% " "%s"'' % (file_name)
    video_bit = subprocess.check_output(command)
    if video_bit == b'\r\n':
        video_bit = 'None'
    else:
        video_bit = int(video_bit.decode())
        video_bit = int(video_bit/1000)
    return video_bit


def duration(file_name):
    command = ''"C:\Program Files\MediaInfo_CLI\MediaInfo.exe " "--Inform=General;%%Duration%% " "%s"'' % (file_name)
    d = subprocess.check_output(command)
    if d == b'\r\n':
        d = 'None'
    else:
        d = int(d.decode())
        d = int(d/60000)
    return d


if __name__ == '__main__':
    for adress, dirs, files in os.walk(r'D:\Test—copy'):
        os.chdir(adress)
        for f in files:
            print("="*30)
            print('File name     = %s' %(f))
            print('Video bitrate = %s kb/sec' % (video_bitrate(f)))
            print('Audio bitrate = %s kb/sec' % (audio_bitrate(f)))
            print('Длительность файла %s минут' % duration(f))
