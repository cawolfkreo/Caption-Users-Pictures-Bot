'''
A big part of the code displayed here is based of
code from this guide: https://blog.lipsumarium.com/caption-memes-in-python/
article. A big thanks to @lipsumar. You can also find
his complete solution here:
https://github.com/lipsumar/meme-caption
'''
from os import path
from PIL import Image, ImageFont, ImageDraw, ImageOps
import textwrap

_fontPath = "src/font/OpenSans-SemiBold.ttf"
_font = ImageFont.truetype(_fontPath, 30)

def createImage(fileToOpen):
    return Image.open(fileToOpen)

def drawTextWithOutline(draw: ImageDraw, text, x, y):
    draw.text((x-1, y-1), text,(0,0,0),font=_font)
    draw.text((x+1, y-1), text,(0,0,0),font=_font)
    draw.text((x+1, y+1), text,(0,0,0),font=_font)
    draw.text((x-1, y+1), text,(0,0,0),font=_font)
    draw.text((x, y), text, (255,255,255), font=_font)

def addTextToProfilePicture(profilePic: Image, textToAdd, heightOffset=0):
    draw = ImageDraw.Draw(profilePic)
    _, _, w, h = draw.textbbox((0,0), textToAdd, _font)         #measure the size the text will take in the picture.

    charSize = round(w/len(textToAdd))                          #the size in pixels of a single character
    charsPerLine = round(profilePic.width / charSize) - 2       #the amount of characters that can be draw on a single line.
                                                                #There is a padding of 1 characters on each side (that's why there is -2 instead of -1)

    wrapper = textwrap.TextWrapper(width=charsPerLine)
    textLines = wrapper.wrap(text=textToAdd)                    #wrap the text in an arrey of "lines" to make sure it won't overflow the image.

    heightOffset *= profilePic.height 

    for i in range(0, len(textLines)):
        #w, h = draw.textsize(textLines[i], _font)
        _, _, w, h = draw.textbbox((0,0), textLines[i], _font)
        drawTextWithOutline(draw, textLines[i], 0.5*(profilePic.width - w), (i * h) + heightOffset)

def addTextToInverseProfilePicture(profilePic: Image, textToAdd: str, name="paco"):
    inverted = ImageOps.invert(profilePic.convert("RGB"))
    baseMessage = f"Evil {name} be like:"
    addTextToProfilePicture(inverted, baseMessage)

    try:
        addTextToProfilePicture(inverted, textToAdd, 0.7)
    finally:
        pass

    return inverted

if __name__ == "__main__":
    # t1
    img = createImage("data/test.jpg")
    addTextToProfilePicture(img, "These are tests that I hope accomplishes to show the image can be created correctly with text on the right position")
    img.save("data/test-out.png")
    # t2
    img = createImage("data/t2.jpg")
    addTextToProfilePicture(img, "These are tests that I hope accomplishes to show the image can be created correctly with text on the right position")
    img.save("data/t2-out.png")
    img = createImage("data/t2.jpg")
    img = addTextToInverseProfilePicture(img, "These are tests that I hope accomplishes to show the image can be created correctly with text on the right position")
    img.save("data/t2-inv-out.png")
    # T3
    img = createImage("data/t3.png")
    addTextToProfilePicture(img, "These are tests that I hope accomplishes to show the image can be created correctly with text on the right position")
    img.save("data/t3-out.png")
    img = createImage("data/t3.png")
    img = addTextToInverseProfilePicture(img, "These are tests that I hope accomplishes to show the image can be created correctly with text on the right position")
    img.save("data/t3-inv-out.png")