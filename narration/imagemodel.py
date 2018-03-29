from main import imager
#from imagedownloader import Downloader
#downloader = Downloader()
from bing_test import Download







#urls = downloader.download(['Shiva', 'Rahul Gandhi', 'Narendra Modi'])

#downloader.get_images(urls, 'photos')
	
		


class textToImage(object):
	"""docstring for textToImage"""

	def getTags(self, para_list, get_urls = False, download = False):
		tags = []
		urls = []
		for i, para in enumerate(para_list):
			#print(para)
			para_tags = self.getParaTags(para = para, para_position = i+1, get_urls = get_urls, download = download)
			tags.append(para_tags)
		if get_urls == True:
			return tags, urls
		else:
			return tags


	def getParaTags(self, para, download = False , para_position = 0, get_urls = False):
		entities = self.getEntities(para)
		if entities is not None:
			Download(keywords = entities)
		return entities

	def getEntities(self, para):
		sentences = para.split('. ')
		entities = []
		for i, sentence in enumerate(sentences):
			#sentences[i] = sentence.split(' ')
			temp_ent = ' '.join(imager(sentences[i]))
			#Stemp_ent = temp_ent[:-1]	
			if temp_ent != '':
				entities.append(temp_ent)
		return entities		


'''para_list = ['Spider Man can beat Iron Man. Narendra Modi is prime minister of India. Sanjay is Racist.', 'Dakshit studies Computer Science at IIT Roorkee. Shiva Plays table tennis. Hardy Sandhu Sings Punjabi Songs']
tt = textToImage()
tags = tt.getTags(para_list, download = True)
print(tags)'''
