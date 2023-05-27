import yt_dlp
import ffmpeg
import os

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []
    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information

filename_collector = FilenameCollectorPP()

def download(URL):
	ydl_opts={
		'outtmpl': '%(id)s.%(ext)s'
	}
	global video_title

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.add_post_processor(filename_collector)
		info_dict=ydl.extract_info(URL, download=True)
	video_title=info_dict.get("webpage_url", None).split('/')[5]

	for f_name in filename_collector.filenames:
		list_f=open(video_title+".txt", "a")
		list_f.write("file '"+f_name+"'\n")
		list_f.close()

	ffmpeg.input(video_title+".txt", format='concat', safe=0).output(video_title+".mp4", c='copy').run()

print("South Park Downloader # ver 0.1")
print("Downloads from the official site(www.southparkstudios.com)")

while 1:
	URL=input()
	download(URL)

	for f_name in filename_collector.filenames:
		os.remove(f_name)
	os.remove(video_title+".txt")

	print("Successfully Downloaded! (Saved as \""+video_title+".mp4"+"\".)")