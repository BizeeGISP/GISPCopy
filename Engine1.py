from openpyxl import load_workbook
import dbUtilities

cur = dbUtilities.connectDB()

wb = load_workbook(filename='data/url/url.xlsx', read_only=True)
ws = wb['Sheet1']
i=0
for row in ws.rows:
    for cell in row:
        print(cell.value)
        dbUtilities.executeInsert(cur, """INSERT INTO gisp.url(url, status) VALUES (%s, %s)""", ((cell.value),'new'))
        i+=1
print i



dbUtilities.commit()
