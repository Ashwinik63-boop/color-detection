import pandas as pd
import cv2

imageUrl = 'colors.jpeg'
clicked = False
redValue = 0
greenValue = 0
blueValue = 0
xPosition = 0
yPosition = 0

# Load the color data
colorNameDataFrame = pd.read_csv('colordetection.csv')
# Print columns to debug
print(colorNameDataFrame.columns)

# If columns have spaces or incorrect names, clean them
colorNameDataFrame.columns = colorNameDataFrame.columns.str.strip()

# Rename columns if they match exactly
colorNameDataFrame.rename(columns={'Hex (24 bit)': 'Hex', 
                                   'Red (8 bit)': 'Red', 
                                   'Green (8 bit)': 'Green', 
                                   'Blue (8 bit)': 'Blue'}, inplace=True)

# Print renamed columns to verify
print(colorNameDataFrame.columns)

#colorNameDataFrame.drop(colorNameDataFrame.iloc[:, 5:8], inplace=True, axis=1)
#colorNameDataFrame.rename(columns={'Hex (24 bit)': 'Hex', 'Red (8 bit)': 'Red', 'Green (8 bit)': 'Green', 'Blue (8 bit)': 'Blue'}, inplace=True)

# Load the image
image = cv2.imread(imageUrl)
if image is None:
    print("Error: Unable to load image")
    exit()

def getColorName(red, green, blue):
    minimumValue = 10000
    colorName = "Unknown"
    for i in range(len(colorNameDataFrame)):
        rgbValue = abs(red - int(colorNameDataFrame.loc[i, "Red"])) + abs(green - int(colorNameDataFrame.loc[i, "Green"])) + abs(blue - int(colorNameDataFrame.loc[i, "Blue"]))
        if (rgbValue <= minimumValue):
            minimumValue = rgbValue
            colorName = colorNameDataFrame.loc[i, "Name"]
    print(f"Detected color: {colorName}")  # Debug print
    return colorName

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Single click instead of double click
        global blueValue, greenValue, redValue, xPosition, yPosition, clicked
        clicked = True
        xPosition = x
        yPosition = y
        blueValue, greenValue, redValue = image[yPosition, xPosition]
        blueValue = int(blueValue)
        greenValue = int(greenValue)
        redValue = int(redValue)

if __name__ == '__main__':
    cv2.namedWindow('Color Name')
    cv2.setMouseCallback('Color Name', draw_function)

    while (1):
        if clicked:
            print(f"Clicked at ({xPosition}, {yPosition}) - RGB: ({redValue}, {greenValue}, {blueValue})")
            cv2.rectangle(image, (20, 20), (750, 60), (blueValue, greenValue, redValue), -1)
            colorName = 'Selected color name is: ' + getColorName(redValue, greenValue, blueValue)
            textColor = (255, 255, 255) if redValue + greenValue + blueValue < 600 else (0, 0, 0)
            cv2.putText(image, colorName, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, textColor, 1, cv2.LINE_AA)
            clicked = False

        cv2.imshow("Color Name", image)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
