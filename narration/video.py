import os
from moviepy.editor import *
from PIL import Image 
import subprocess

_dir = os.getcwd()
_FPS = 1

def format_text(string): 
	words=string.split()
	output=''
	buffer_string=''
	for w in words:
		if(len(buffer_string)<65):
			buffer_string+=w+' '
		else:
			output+=buffer_string+'\n'
			buffer_string=w+' '
	output+=buffer_string   
	return output

def video_generator(sentences,keywords):
	text_list = []
	video_list = []
	audio_list = []
	_images = os.listdir(_dir + '/narration/photos/')

	u = 0
	if len(keywords[0]) == 0:
	    lastpath = _dir + '/temp/basic.jpg'

	for i in range(0, len(sentences)):
		_title = 'audio_file_' + str(i+1)
		temp_audio = AudioFileClip(_dir + '/narration/audio/' + _title + '.wav')
		audio_list.append(temp_audio)
		temp_text = TextClip(format_text(sentences[i]),font='Time',fontsize=50,color='yellow',bg_color='black',stroke_width=30).set_pos('bottom').set_duration(temp_audio.duration).resize(width=700)
		text_list.append(temp_text)
		if len(keywords[i]) != 0:
			for j in range(0, len(keywords[i])):
				path = _dir + '/narration/photos/' + keywords[i][j] + '.jpg'
				if os.path.isfile(path):
					temp_video=ImageClip(path).set_duration(temp_audio.duration/len(keywords[i])).set_position('top').set_fps(_FPS).crossfadein(0.5)
					video_list.append(temp_video)
				lastpath = path
		else:
			temp_video=ImageClip(lastpath).set_duration(temp_audio.duration).set_position('top').set_fps(_FPS).crossfadein(0.5)
			video_list.append(temp_video)
	audio_clip = concatenate_audioclips(audio_list)
	txt_clip = concatenate_videoclips(text_list, method='compose').set_position('bottom')
	video_clip = concatenate_videoclips(video_list, method='compose').set_position('center')
	result=CompositeVideoClip([video_clip, txt_clip])
	result_with_audio=result.set_audio(audio_clip)
	result_with_audio.write_videofile('temp/hello.mp4', fps=2)


