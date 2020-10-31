from __future__ import annotations
import youtube_dl

class YoutubeDL(youtube_dl.YoutubeDL):
	def get_playlist(self, url: str, verbose: bool = True):
		"""Small extension to youtube_dl library class YoutubeDL that let's you extract raw playlist data."""
		self.params.setdefault('skip_download', True)
		self.params.setdefault('extract_flat', True)
		self.params.setdefault('quiet', not verbose)
		res = self.extract_info(url, download=False)
		try:
			return res['entries']
		except Exception:
			raise NotImplementedError('Failed to parse yt response due to lack of proper implementation of received response from method "YoutubeDL.extract_info"')
    
	def _extract_titles(self, playlist) -> List[str]:
		res = []
		for video in playlist:
			try:
				res.append(video['title'])
			except Exception:
				try:
					import jsonpickle
					raise ValueError('Failed to parse response, no element "title" in dictionary playlist.entries, video as json=' + jsonpickle.encode(video))
				except ValueError as ex:
					raise ex
				except Exception as e:
					raise ValueError('Failed to parse response, no element "title" in dictionary playlist.entries, failed to print details: ' + str(e))
		return res
    
	def get_playlist_titles(self, url: str, verbose: bool = True):
		_playlist = self.get_playlist(url, verbose)
		return self._extract_titles(_playlist)



if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		link = sys.argv[1]
	else:
		link = 'https://www.youtube.com/watch?v=4Uc9IhBSW6k&list=PLy6N_9yB8Qwy6LL0J7zLUyW8XNX-BPeDl'
	print(f"Running playlist test, download playlist in video '{link}")
	print('\n'.join(YoutubeDL().get_playlist_titles(link)))
