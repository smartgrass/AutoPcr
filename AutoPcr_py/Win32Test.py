
from PIL import Image
import pytesseract
import os

curDir = os.path.dirname(__file__)
#图片路径拼接
def GetFullPath(pngName):
	global curDir
	return os.path.join(curDir,pngName)



if __name__ == '__main__':
	print("start")

	try:
		pytesseract.pytesseract.tesseract_cmd = curDir+'/OCR/tesseract.exe'
		text = pytesseract.image_to_string(Image.open('./shop/buyBtn.png'), lang='chi_sim')
	except:
		print("except 错误")
		exit(0)

	# text = pytesseract.image_to_string(Image.open('./main/auto2.png'), lang='chi_sim')

	print("shoot",text)


