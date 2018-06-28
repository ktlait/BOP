from PIL import Image
import psycopg2
from matplotlib.colors import rgb2hex
import re

class Colour():
    colour = ""
    percentage = 0
    def __init__(self, colour, percentage):
        self.colour = colour
        self.percentage = percentage

def calculate_percentage(colours, counts):
    percentages = []
    points = 0
    size = len(counts)
    for line in counts:
        points = points+line
    for line in range(len(counts)):
        percent = (counts[line]/points)*100
        if percent > 0.05:
           cur = Colour(colours[line], percent)
           percentages.append(cur)
    return percentages

def show_colours(percentages):
    for var in percentages:
        print("| " + str(var.colour) + " | " + str(var.percentage) + " | ")



try:
    connect_str = "dbname='bopdb' user='postgres' host='localhost' " + \
                  "password='cs163278*cs'"
    connection = psycopg2.connect(connect_str)
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM analysed_images""")
    all_percentages = []
    for row in cursor:
        print("Image ID: " + str(row[0]))
        percentages = calculate_percentage(row[1], row[2])
        # show_colours(percentages)
        all_percentages.append(percentages)
    # prompt user to add colour names
    query = "INSERT INTO name_table (colour_hex, name) " + \
            "VALUES (%s, %s)"
    s = []
    for line in all_percentages:
        for cur in line:
            rgb = re.split('[( , )]', str(cur.colour))
            rgb2 = rgb[1:4]
            r = int(rgb[1])
            g = int(rgb[2])
            b = int(rgb[3])
            rgb_to_hex = lambda r, g, b: '%02x%02x%02x' %(r,g,b)
            in_hex = rgb_to_hex(r, g, b)
            s.append(in_hex)
            siz1 = len(s)
            s = list(set(s))
            siz2 = len(s)
            print(str(siz1) + " - " + str(siz2))
            if siz1==siz2:
                cursor.execute(query, (in_hex, "temp"))
                print("Entered into table")
            else:
                print("Sorry already exists in table")
    connection.commit()
    connection.close()
    cursor.close()

except Exception as e:
    print(e)

