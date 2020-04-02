import os
import imageio
import numpy as np
import moviepy.editor as mp



DIR = "/Users/arpj/Documents/princeton/coursework/spring_2020/cee_546/assignments/02/puerto_rico/gif/curv_white"
IN_NAME = 'movie.gif'
OUT_NAME = 'curvature.mp4'
FPS = 6
CODEC = 'mpeg4'

IN = os.path.join(DIR, IN_NAME)
OUT = os.path.join(DIR, OUT_NAME)

clip = mp.VideoFileClip(IN)
clip.write_videofile(OUT, fps=FPS, codec=CODEC, audio=False)
clip.close()
