import vuba
import glob
from natsort import natsorted, ns

# Parameters --------
folder = '/path/to/videos'
output_file = '/path/to/output.avi'

# -------------------

files = natsorted(glob.glob(f'{folder}/*.avi'), alg=ns.IGNORECASE)

video = vuba.Video(files[0])

main_writer = vuba.Writer(output_file, video)

video.close()

for file in files:
	print(f'Processing: {file}')	

	video = vuba.Video(file)

	for frame in video.read(0, len(video), grayscale=False):
		writer.write(frame)

	video.close()

main_writer.close()