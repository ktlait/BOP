from PIL import Image
import glob
import time
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient

import psycopg2
image_list = []
try:
    # connect to database using credientals
    connect_str = "dbname='bopdb' user='postgres' host='localhost' " +\
                  "password='cs163278*cs'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    # run a SELECT statement - no data in there, but we can try it
    cursor.execute("""SELECT * from user_input_images""")
    rows = cursor.fetchall()
    google_maps = GoogleMaps(api_key = 'AIzaSyDVCz85jlq7W29UXHNh_K2HZ4gl4-ST8t0')
    query = "INSERT INTO user_input_images (filepath, img_date, img_time, geolocation)" + \
            " VALUES (%s, %s, %s, %s);"
    address = "Dublin, Ireland"
    # search google maps for the address
    location = google_maps.search(location=address)
    location = location.first()
    location = str( location.lat) + "," + str(location.lng)
    print(location)

    for filename in glob.iglob('images/*.jpg'):
        image_list.append(filename)
        cursor.execute(query, (filename, str(time.strftime("%x")),
                  str(time.strftime("%X")), location))

    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)

