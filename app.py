from pytube import Playlist
from string import Template
from os import listdir, rename, remove
import subprocess
import sys

playlist = Playlist(sys.argv[1])
path = Template("/home/helio/Downloads/playlist_downloader/$title/")
path = path.substitute(title=playlist.title.replace(" ", "_").replace("/", "-"))
print("Iniciando o download da playlist "+playlist.title+"\n")
print("Essa playlist contém ", len(playlist.videos), " vídeos\n\n")
# Download the videos
for index, video in enumerate(playlist.videos):
    print("Fazendo download do arquivo #", index+1, '\n')
    mp4_videos = video.streams.filter(file_extension='mp4')
    if(len(mp4_videos)>0):
        mp4_videos[-1].download(path)
    else:
        print("Falha no download do arquivo #", index+1, "\n")

#rename files for better use in FFMPEG
print("Arquivos baixados, trocando espaços para underlines\n")
for file in listdir(path):
    rename(path+file, path+file.replace(" ", "_"))
# Convert  to mp3 and delete video
file_to_convert = Template("ffmpeg -hide_banner -loglevel error -i '$path/$file' '$path/$output'")
for file in listdir(path):
    print("Convertendo o arquivo "+file+" para "+file.replace("mp4", "mp3"))
    subprocess.run(file_to_convert.substitute(path=path, file=file, output = file.replace("mp4", "mp3")), shell=True)
    remove(path+file)

print("Arquivos em ~/Downloads/playlist_downloader/"+playlist.title+"\n")
