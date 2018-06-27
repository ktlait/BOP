import psycopg2
import re
from math import floor

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
        if percent > 0.5:
           cur = Colour(colours[line], percent)
           percentages.append(cur)
    return percentages

def show_colours(percentages):
        for var in percentages:
            print("| " + str(var.colour) + " | " + str(var.percentage) + " | ")

try:
    connect_str = "dbname='bopdb' user='postgres' host='localhost'" + \
                 "password='cs163278*cs'"
    conn = psycopg2.connect(connect_str)
    print("Connecting to database ...")
    cursor = conn.cursor()
    print("Connected")
    cursor.execute("""SELECT filepath FROM user_input_images""")
    print("Images discovered:")
    for row in cursor:
        str_row = str(row)
        str_row = re.split('[/ , ) \' .]', str_row)
        file_name = str(str_row[2])
        print(file_name)
    user_input = input("Enter image name to analyse:")
    query = "SELECT image_id FROM user_input_images WHERE filepath= \'images/" + str(user_input) + ".jpg\'"
    cursor.execute(query)
    for row in cursor:
        id = int(row[0])
    query = "SELECT * FROM analysed_images WHERE image_id = " + str(id)
    cursor.execute(query)
    percentages = []
    for row in cursor:
        percentages = calculate_percentage(row[1], row[2])
    show_colours(percentages)
    conn.close()
    cursor.close()
except Exception as e:
    print(e)
