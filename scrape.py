import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def scrape():
    req = requests.get('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield')
    content = req.text
    soup = BeautifulSoup(content, "lxml")
    
    treasury_table= soup.find("table", attrs={"class": "t-chart"})
    treasury_data = treasury_table.find_all("tr")
    
    
    header =["Date", "1Mo", "2Mo", "3Mo", "6Mo", "1Yr", "2Yr", "3Yr", "5Yr", "7Yr", "10Yr", "20Yr", "30Yr"]

    treasury_table= soup.find("table", attrs={"class": "t-chart"})
    

    trs = treasury_table.find_all("tr")

    data = []
    for tr in trs:
        tds = tr.findAll("td")
        row_empty=[]
        for td in tds:
            td_text = td.text.strip()
            row_empty.append(td_text)
        data.append(row_empty)
    final_data = data[1:]
    data_frame = pd.DataFrame(final_data, columns = header)
    data_frame[["1Mo", "2Mo", "3Mo", "6Mo", "1Yr", "2Yr", "3Yr", "5Yr", "7Yr", "10Yr", "20Yr", "30Yr"]] = data_frame[["1Mo", "2Mo", "3Mo", "6Mo", "1Yr", "2Yr", "3Yr", "5Yr", "7Yr", "10Yr", "20Yr", "30Yr"]].apply(pd.to_numeric)
    return data_frame



def creating_chart():
    df = scrape()
    try:
        plt.plot(df["Date"], df["1Mo"], data=df, color ="red", label = "1Mo")
        plt.plot(df["Date"], df["2Mo"], data=df, color ="blue", label = "2Mo")
        plt.plot(df["Date"], df["3Mo"], data=df, color ="orange", label = "3Mo")
        plt.legend()

        #savingplot
        plt.show()
        plt.savefig('charts/Treasury_yield.png')
    except:
        return "saving Uncesseccful"

if __name__ == '__main__':
    creating_chart()