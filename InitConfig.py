import os
REALPATH=os.path.split(os.path.realpath(__file__))[0]
def folderInit(path):
	if not os.path.exists(path):
		os.makedirs(path)
class PATHConfig:
	def __init__(self):
		self.HTLMSPATH=r'htmls\\'[:-1]
		folderInit(self.HTLMSPATH)

		self.IMAGESPATH=r'images\\'[:-1]
		folderInit(self.IMAGESPATH)

		self.CHROMEPATH = r'E:\chromedriver.exe'
		self.HTLMSREPATH = REALPATH+'\\' + self.HTLMSPATH
#
# p=PATHConfig()
# print(p.HTLMSREPATH)
# print(p.HTLMSPATH)
# print(p.CHROMEPATH)
# print(p.IMAGESPATH)

