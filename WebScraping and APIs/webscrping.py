#First install necessary library
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
url ="https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films"

db_name="Movies.db"
table_name="top_20"
final_file="extracted_file.csv"

df = pd.DataFrame(columns=["Film","Year","Rotten Tomatoes' Top 100"])
count = 0

html_page=requests.get(url).text
data=BeautifulSoup(html_page, "html.parser")

tables = data.find_all("tbody")
rows = tables[0].find_all("tr")

for row in rows:
    if count < 25:
        col = row.find_all("td")
        if len(col)!=0:
            data_dict={"Film": int(col[1].contents[0]),
                        "Year":int(col[2].contents[0]),
                        "Rotten Tomatoes' Top 100":int(col[3].contents[0])
                        }
            df1 = pd.DataFrame(data_dict, index=[0])
            df = pd.concat([df,df1],ignore_index=True)
            count+=1
        else:
            break
print(df)

df.to_csv(final_file)

conn=sqlite3.connect(db_name)
df.to_sql(table_name, conn, if_exists="replace", index=False)
conn.close()