from re import A
import sys
import os
import io
import music_tag
import PIL
from yh_utils import *


def SettingMusicTags(music_dir, albumart_path, tag_path, tag_names, ext='m4a'):
    #file tags setting
    #https://pypi.org/project/music-tag/
    print('Setting Music Tages')

    list_music_path = get_file_list(music_dir, ext, True)
    text_tags = loadTextFile(tag_path)

    if albumart_path == "":
        albumart_path = "./white.jpg"

    with open(albumart_path, 'rb') as image:
        art = image.read()
        for path, tags in zip(list_music_path, text_tags):
            music = music_tag.load_file(path)
            
            #tag setting
            tag = tags.split('-')
            for name, tag in zip(tag_names, tag):
                music[name] = tag.lstrip().rstrip()

            #album art setting
            # image = PIL.Image.open(albumart_path)
            music['artwork'] = art
            # art.first.thumbnail([100,100])

            music.save()

if __name__ == '__main__' :

    music_dir = "C:/Users/Younghyun/Music/녹음/22뮤"
    albumart_path = "C:/Users/Younghyun/Music/westernstory.jpg"
    tag_path = "C:/Users/Younghyun/Music/태그/웨스턴통태그.txt"
    tag_names = ["tracknumber", "tracktitle", "album", "genre", "artist"]

    SettingMusicTags(music_dir, albumart_path, tag_path, tag_names)
