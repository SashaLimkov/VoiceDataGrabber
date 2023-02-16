# from pydub import AudioSegment
# AudioSegment.from_file("file.ogg").export("new_file.mp3", format="mp3")
import mutagen
audio_info = mutagen.File('file.ogg').info
print(dir(audio_info), audio_info.length)