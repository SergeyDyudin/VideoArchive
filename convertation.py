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
    dur = subprocess.check_output(command)
    if dur == b'\r\n':
        dur = 'None'
    else:
        dur = int(dur.decode())
        dur = int(dur/60000)
    return dur

if __name__ == '__main__':
    os.chdir(r'D:\Test—copy')
    for adress, dirs, files in os.walk(os.getcwd()):
        os.chdir(adress)
        for f in files:
            audio_bit = audio_bitrate(f)
            video_bit = video_bitrate(f)
            dur = duration(f)
            print("="*30)
            print('File name     = %s' %(f))
            print('Video bitrate = %s kb/sec' %(video_bit))
            print('Audio bitrate = %s kb/sec' %(audio_bit))
            print('Длительность файла %s минут' % dur)
