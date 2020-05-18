'''
A big part of the code displayed here is based
on code from this: https://blog.lipsumarium.com/caption-memes-in-python/
article. A big thanks to @lipsumar. You can also find
the full code of his solution here:
https://github.com/lipsumar/meme-caption
'''
from os import path
from PIL import Image, ImageFont, ImageDraw
import textwrap

def createFontPath(fontRelativePath):
    currentDir = "/src/"
    return path.join(currentDir, fontRelativePath)

fontPath = createFontPath("font\OpenSans-SemiBold.ttf")
font = ImageFont.truetype(fontPath, 28)


def createImage(fileToOpen):
    return Image.open(fileToOpen)

def drawTextWithOutline(draw, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=font)
    draw.text((x-2, y-3), text,(0,0,0),font=font)
    draw.text((x+2, y-2), text,(0,0,0),font=font)
    draw.text((x+2, y+2), text,(0,0,0),font=font)
    draw.text((x+2, y+3), text,(0,0,0),font=font)
    draw.text((x-2, y+2), text,(0,0,0),font=font)
    draw.text((x, y), text, (255,255,255), font=font)

def addTextToProfilePicture(profilePic, textToAdd):
    textX = 10
    textY = 7

    draw = ImageDraw.Draw(profilePic)
    w, h = draw.textsize(textToAdd, font)                       #measure the size the text will take in the picture.

    charSize = round((w/len(textToAdd)))                        #the size in pixels of a single character
    charsPerLine = round(profilePic.width / charSize) - 1       #the amount of characters that can be draw on a single line.

    wrapper = textwrap.TextWrapper(width=charsPerLine)
    textLines = wrapper.wrap(text=textToAdd)                    #wrap the text in an arrey of "lines" to make sure it won't overflow the image.

    for i in range(0, len(textLines)):
        w, h = draw.textsize(textLines[i], font)
        drawTextWithOutline(draw, textLines[i], 0.5*(profilePic.width - w), i * h)

if __name__ == "__main__":
    img = createImage("data/test.jpg")
    addTextToProfilePicture(img, "Esta es una prueba más que espero logre demostrar que la imágen se puedee crear de forma correcta y con el texto en la posición correcta, no entiendo porqué rayos quedó así.")
    img.save("data/test-out.jpg")
    img = createImage("data/t2.jpg")
    addTextToProfilePicture(img, "Esta es una prueba más que espero logre demostrar que la imágen se puedee crear de forma correcta y con el texto en la posición correcta, no entiendo porqué rayos quedó así.")
    img.save("data/t2-out.jpg")