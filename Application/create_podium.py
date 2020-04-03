from PIL import Image, ImageDraw
import wget
import os


def create(liste):

	files = os.listdir()
	if not 'img_artists' in files:
		os.mkdir('img_artists')
	
	sizes = []
	locs = []
	for i in range(3):
		sizes.append(len(liste[i]))
		for j in range(len(liste[i])):
			outfile = f"img_artists/{i+1}_{j+1}.png"
			wget.download(liste[i][j], out=outfile)
			locs.append(outfile)
	
	mask_im = Image.new("L", (100,100), 0)
	draw = ImageDraw.Draw(mask_im)
	draw.ellipse((0, 0, 100, 100), fill=255)

	img_big = Image.open('static/images/podium.png', 'r')
	img_w, img_h = img_big.size

	# Positions selon sizes
	posx = [250,90,410]
	posy = [10,60,90]

	for i in range(3):
		infile = f"img_artists/{i+1}_1.png"
		img_small = Image.open(infile, 'r')
		img_small = img_small.resize((100,100))
		img_big.paste(img_small, (posx[i],posy[i]), mask_im)

	actual = os.getcwd()+'/img_artists/'
	files = os.listdir('img_artists/')
	for f in files:
		path = actual+f
		os.remove(path)

	img_big.save('static/images/podium_fin.png')