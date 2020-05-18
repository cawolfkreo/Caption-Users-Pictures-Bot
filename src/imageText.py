'''
A big part of the code displayed here is based
on code from this: https://blog.lipsumarium.com/caption-memes-in-python/
article. A big thanks to @lipsumar. You can also find
the full code of his solution here:
https://github.com/lipsumar/meme-caption
'''
from os import path
from PIL import Image, ImageFont, ImageDraw

def createFontPath(fontRelativePath):
    currentDir = path.dirname(__file__)
    return path.join(currentDir, fontRelativePath)

fontPath = createFontPath("font\OpenSans-SemiBold.ttf")
font = ImageFont.truetype(fontPath, 26)


def createImage(fileToOpen):
    return Image.open(fileToOpen)

def drawTextWithOutline(draw, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)

def addTextToProfilePicture(image, textToAdd):
    textX = 10
    textY = 7

    draw = ImageDraw.Draw(image)
    w, h = draw.textsize(textToAdd, font) # measure the size the text will take
    drawTextWithOutline(draw, textToAdd, image.width/2 - w/2, textY)

if __name__ == "__main__":
    img = createImage("data/t2.jpg")
    addTextToProfilePicture(img, "hola")
    img.save("data/t2-out.jpg")
    img = createImage("data/t0.jpg")
    addTextToProfilePicture(img, "hola")
    img.save("data/t0-out.jpg")