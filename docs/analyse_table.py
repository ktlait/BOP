from PIL import Image
import psycopg2
image_list = []

try:
    # connect to database with owner creditentials
    connect_str = "dbname= 'bopdb' user= 'postgres' host= 'localhost'" + \
    "password= 'cs163278*cs'"
    # use these values to establish connection through psycopg2 module
    conn = psycopg2.connect(connect_str)
    # cursor is an object that will execute queries
    cursor = conn.cursor()
    # create a table that will store analysis of images
    cursor.execute("""SELECT image_id, filepath FROM user_input_images""")
    # rows = cursor.fetchall()
    # print(rows)
    image_id_list = []
    big_daddy_colour_list = []
    big_daddy_percentage_list = []
    for row in cursor:
        image_id_list.append(row[0])
        colours_list = []
        percentage_list = []
        im = Image.open(row[1])
        colors = im.getcolors(256*256*256)
        print(row[1])
        for var in colors:
           # insert into arrays and then into table (x, (y, z, w))
           colours_list.append(var[1])
           percentage_list.append(var[0])
        big_daddy_colour_list.append(colours_list)
        big_daddy_percentage_list.append(percentage_list)
    for var in range(len(big_daddy_colour_list)):
        query ="""INSERT INTO analysed_images (image_id, colours_found, pixel_presence)
             VALUES (%s, %s, %s)"""
        cursor.execute(query,(image_id_list[var], big_daddy_colour_list[var], big_daddy_percentage_list[var]))
    print(big_daddy_colour_list)
    # query ="INSERT INTO analysed_images (image_id, colours_found, pixel_presence)
             #VALUES (%s, %s, %s)"""
    # cursor.execute(query, (row[0], colours_list, percentage_list))
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print("Uh oh, there has been an error.")
    print(e)

