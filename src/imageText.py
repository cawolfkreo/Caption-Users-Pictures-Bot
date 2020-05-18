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
    currentDir = path.dirname(__file__)
    return path.join(currentDir, fontRelativePath)

fontPath = createFontPath("font\OpenSans-SemiBold.ttf")
font = ImageFont.truetype(fontPath, 28)


def createImage(fileToOpen):
    return Image.open(fileToOpen)

def drawTextWithOutline(draw, text, x, y):
    draw.multiline_text((x-2, y-2), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x-2, y-3), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x+2, y-2), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x+2, y+2), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x+2, y+3), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x-2, y+2), text,(0,0,0),font=font, align="center")
    draw.multiline_text((x, y), text, (255,255,255), font=font, align="center")

def addTextToProfilePicture(profilePic, textToAdd):
    textX = 10
    textY = 7

    draw = ImageDraw.Draw(profilePic)
    w, h = draw.textsize(textToAdd, font)                   #measure the size the text will take in the picture.
    
    lineCount = 1
    if (w > profilePic.width):
        lineCount = w / profilePic.width
    charsPerLine = int(round((len(textToAdd) / lineCount) + 1))
    wrapper = textwrap.TextWrapper(width=charsPerLine)
    textLines = wrapper.wrap(text=textToAdd)                #wrap the text in an arrey of "lines" to make sure it won't overflow the image.

    singleLineW, singleLineH = draw.textsize(textLines[0], font) #calculates the w of a single line
    multiLineText = "\n".join(textLines)                    #Makes a new string with the "\n" in between the lines of the string
    drawTextWithOutline(draw, multiLineText, profilePic.width/2 - singleLineW/2, textY)

if __name__ == "__main__":
    img = createImage("data/t2.jpg")
    addTextToProfilePicture(img, "Esta es una prueba más que espero logre demostrar que la imágen se puedee crear de forma correcta y con el texto en la posición correcta, no entiendo porqué rayos quedó así.")
    img.save("data/t2-out.jpg")
    img.save("data/t2-out.png", "PNG")