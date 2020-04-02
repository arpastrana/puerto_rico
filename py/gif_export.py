import os
import imageio
from pygifsicle import optimize


DIR = "/Users/arpj/Documents/princeton/coursework/spring_2020/cee_546/assignments/02/puerto_rico/gif/q_all"
OUT_NAME = 'qall2.gif'
SUFFIX = ".bmp"
LOOP = 0
FPS = 3
COLORS = 64


filenames = os.listdir(DIR)
OUT = os.path.join(DIR, OUT_NAME)

images = []
filenames = sorted([filename for filename in filenames if filename.endswith(SUFFIX)])
for filename in filenames:
	file_path = os.path.join(DIR, filename)
	images.append(imageio.imread(file_path))


print('baking...')
imageio.mimsave(OUT, images, loop=LOOP, fps=FPS)
print('baked!')
print('optimizing gif...')
optimize(OUT, colors=COLORS)
print('done!')

