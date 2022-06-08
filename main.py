import requests
import pyodbc
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-7TSKHCKF;'
                      'Database=zomato;'
                      'Trusted_Connection=yes;')
conn1 = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-7TSKHCKF;'
                      'Database=zomato;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("SELECT URL FROM [zomato].[stage].[tbl_csv1]")
for row in cursor:
    url = [elem for elem in row]
    response = requests.get(url[0], headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    href_table = []
    for i in soup.find_all("a", href=True):
        href_table.append(i['href'])
    for i in href_table:
        j = i.replace('"', '')
        if 'google.com/maps' in j:
            coords = (j.split('=')[-1])
    query = """INSERT INTO [zomato].[stage].[tbl_coordinates] (URL, COORDINATES) VALUES (?,?)"""
    record = (url[0],coords)
    cursor1 = conn1.cursor()
    cursor1.execute(query,record)
    conn1.commit()
    