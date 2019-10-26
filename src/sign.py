from PIL import Image, ImageDraw, ImageFont, ImageChops
import sys

from config import config

font_file = 'FRAMDCN.TTF'
fonts = [None] + [ImageFont.truetype(font_file, size) for size in config['signgen']['geometry']['font_sizes']]
y_offset = [None] + config['signgen']['geometry']['y_offset']

im_template = Image.open(config['signgen']['template']).convert('RGBA')
im_template_mask = Image.open(config['signgen']['template_mask']).convert('L').resize(im_template.size)

def create_sign_sticker(text, filename, rotation=9, h_scale=.8, text_color=(165, 50, 0, 255),
                        outline_color=(0, 0, 0, 255), sign_bg_color=(253, 221, 145, 255)):
	n_lines = len(text.split('\n'))
	if n_lines > 5:
		raise Exception('Cannot do more than 5 lines :(')
	font = fonts[n_lines]

	im_text = Image.new('RGBA', im_template.size, sign_bg_color)
	d = ImageDraw.Draw(im_text)
	w, h = d.multiline_textsize(text, font=font)
	pos = (
		im_text.size[0]//2 - w//2,
		im_text.size[1]//2 - h//2 + y_offset[n_lines]
	)

	# render text outline
	kwargs = {'font': font, 'align': 'center', 'fill': outline_color, 'spacing': -6}
	d.text((pos[0] - 1, pos[1] - 1), text, **kwargs)
	d.text((pos[0] + 1, pos[1] - 1), text, **kwargs)
	d.text((pos[0] - 1, pos[1] + 1), text, **kwargs)
	d.text((pos[0] + 1, pos[1] + 1), text, **kwargs)

	# render text
	kwargs['fill'] = text_color
	d.text(pos, text, **kwargs)

	# squeeze
	im_text3 = im_text.resize((int(im_text.size[0]*h_scale), im_text.size[1]), resample=Image.BICUBIC)
	im_text2 = Image.new('RGBA', im_template.size, sign_bg_color)
	im_text2.paste(im_text3, (int(im_text.size[0]*(1-h_scale)*.5), 0))
	im_text = im_text2

	# offset and rotate
	im_text = ImageChops.offset(im_text, 63,85)
	im_text = im_text.rotate(rotation, resample=Image.BICUBIC)

	# now save
	result = Image.composite(im_text, im_template, im_template_mask)
	result.save(filename)

def main():
	if len(sys.argv) >= 2:
		create_sign_sticker(sys.argv[1].replace('\\n', '\n'), 'out.png')
		print('Saved to out.png')
	else:
		print('Usage: python {} sign-text'.format(sys.argv[0]))

if __name__ == '__main__':
	main()
