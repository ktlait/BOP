import psycopg2

try:
    connect_str = "dbname='bopdb' user='postgres' host='localhost'" + \
                  "password='cs163278*cs'"
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM name_table""")
    rows = cursor.fetchall()
    print(rows)
    conn.commit()
    cursor.close()
    connc.close()

except Exception as e:
    print("Uh Oh, can't connect.")
    print(e)
