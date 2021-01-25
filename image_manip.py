"""
Project 4:    Image Manipulation

Author(s):    Noah Bridgeman

Due Date:     10:00 p.m., Sunday, November 15

Description:  Image Manipulation Tools: Pixelate an image, interlace two images, or smear an image
"""

from PIL import Image, ImageDraw
import random

MENU_OPTIONS = "BCDKLSXPIMQ"

def menu():
    """Displays menu of options and gets user's input."""
    choice = "No choice"
    while choice not in MENU_OPTIONS:
        print()
        print("B - Transform image A into black and white")
        print("C - Copy image A to image B")
        print("D - Display image A")
        print("K - Catenate image B to image A")
        print("L - Load image from file into image A")
        print("S - Save image A to file")
        print("X - Exchange image A and B")
        print("P - Pixelate image A")
        print("I - Interlace image A and B")
        print("M - Smear image A")
        print("Q - Quit")
        choice = input("Please select an option from the menu: ").upper()
        print()
        if choice not in MENU_OPTIONS:
            print("Sorry,", choice, "is not one of the options, please try again.")
               
    return choice


def catenate(left, right):
    """Catenates two images together.
    This function only works for images of the same height!"""

    result = Image.new("RGB", (left.width + right.width, left.height))
    
    for x in range(left.width):
        for y in range(left.height):
            pixel = left.getpixel((x, y))
            result.putpixel((x, y), pixel)
            
    for x in range(right.width):
        for y in range(right.height):            
            pixel = right.getpixel((x, y))
            result.putpixel((left.width + x, y), pixel)

    return result


def luminance(rgb):
    """Finds the average of r, g, and b components to determine how
    bright a pixel is."""
    
    (r, g, b) = rgb
    return (r + g + b) // 3


def black_and_white(image):
    """Takes an image and makes it black and white."""
    
    for x in range(image.width):
        for y in range(image.height):
            rgb = image.getpixel((x, y))
            avg = luminance(rgb)
            
            if avg < 128:
                image.putpixel((x, y), (0, 0, 0))
            else:
                image.putpixel((x, y), (255, 255, 255))
                
def average(x, y, image, scaleX, scaleY):
    rSum = 0
    gSum = 0
    bSum = 0
    for i in range(scaleX):
        for j in range(scaleY):
            r, g, b = image.getpixel((x + i, y + j))
            rSum += r
            gSum += g
            bSum += b
    rAvg = rSum // (scaleX * scaleY)
    gAvg = gSum // (scaleX * scaleY)
    bAvg = bSum // (scaleX * scaleY)
    
    return rAvg, gAvg, bAvg

def pixelate(image, amount = 16):
    scaleX = image.width // amount
    scaleY = image.height // amount
    newImage = image.resize((amount * scaleX, amount * scaleY))
    
    for x in range(0, newImage.width - 1, scaleX):
        for y in range(0, newImage.height - 1, scaleY):
            color = average(x, y, newImage, scaleX, scaleY)
            for i in range(scaleX):
                for j in range(scaleY):
                    newImage.putpixel((x + i, y + j), color)
    
    return newImage

def interlace(imageA, imageB):
    if imageA.width > imageB.width:
        width = (imageB.width // 2) * 2
    else:
        width = (imageA.width // 2) * 2
    if imageA.height > imageB.height:
        height = (imageB.height // 2) * 2
    else:
        height = (imageA.height // 2) * 2
        
    imageA.resize((width, height))
    imageB.resize((width, height))
    newImage = Image.new("RGB", (width, height))
        
    for x in range(0, width - 1, 2):
        for y in range(0, height):
            color = imageA.getpixel((x, y))
            newImage.putpixel((x, y), color)
            color = imageB.getpixel((x + 1, y))
            newImage.putpixel((x + 1, y), color)
            
    return newImage

def circle(draw, center, radius, color):
    lowX, lowY = center[0] - radius, center[1] - radius
    highX, highY = center[0] + radius, center[1] + radius
    
    draw.ellipse((lowX, lowY, highX, highY), color)

def smear(image):
    blank = Image.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(blank, "RGBA")
    
    for _ in range((image.width * image.height) // 2):
        x = random.randrange(0, image.width)
        y = random.randrange(0, image.height)
        
        r, g, b = image.getpixel((x, y))
        
        for i in range(random.randrange(10, 30)):
            circle(draw, (x + i, y + i), random.randrange(2, 4), (r, g, b, random.randrange(25, 175)))
    
    return blank
    
        
def main():
    choice = menu()
    imageA = Image.new("RGB", (100, 100))
    imageB = Image.new("RGB", (100, 100))
    
    while choice != "Q":
        if choice == "B":
            black_and_white(imageA)
            
        elif choice == "C":
            imageB = imageA.copy()
            
        elif choice == "D":
            print("Displaying image...")
            imageA.show()

        elif choice == "K":
            imageA = catenate(imageA, imageB)
            
        elif choice == "L":
            print("Loading file...")
            name = input("Enter the name of the file: ")
            imageA = Image.open(name)

        elif choice == "S":
            name = input("Enter the name of the file: ")
            imageA.save(name)
            
        elif choice == "P":
            print("Pixelating image...")
            imageA = pixelate(imageA)

        elif choice == "X":
            tmp = imageB
            imageB = imageA
            imageA = tmp
            
        elif choice == "I":
            print("Interlacing images...")
            imageA = interlace(imageA, imageB)
            
        elif choice == "M":
            print("Smearing image...")
            imageA = smear(imageA)

        choice = menu()

if __name__ == "__main__":
    main()
