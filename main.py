import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

name=''
def get_html_data(url):
    data = requests.get(url)
    return data

def get_covid_detail_bd():
    url = "https://worldometers.info/coronavirus/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail = ""

    for i in range(3):
        text = info_div[i].find("h1", class_=None).get_text()

        count = info_div[i].find("span", class_=None).get_text()

        all_detail = all_detail + text + " " + count + "\n"

    return all_detail

def get_country_data():
    name= textfield.get()
    n=name
    url="https://worldometers.info/coronavirus/country/"+name
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail = ""

    for i in range(3):
        text = info_div[i].find("h1", class_=None).get_text()

        count = info_div[i].find("span", class_=None).get_text()

        all_detail = all_detail + text + " " + count + "\n"


    mainlabel['text']=all_detail

    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',

                     parse_dates=['Date'])

    c = name
    countries = [c]
    df = df[df['Country'].isin(countries)]

    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)

    df = df.pivot(index='Date', columns='Country', values='Cases')
    countries = list(df.columns)
    covid = df.reset_index('Date')
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    colors = {c: '#DC3977'}
    plt.style.use('fivethirtyeight')

    plot = covid.plot(figsize=(7, 4), color=list(colors.values()), linewidth=3, legend=False)
    plot.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plot.grid(color='#d4d4d4')
    plot.set_xlabel('Date')
    plot.set_ylabel('# of Cases')

    for country in list(colors.keys()):
        plot.text(x=covid.index[-1], y=covid[country].max(), color=colors[country], s=country, weight='bold')

    plot.text(x=covid.index[1], y=int(covid.max().max()) + 45000, s="COVID-19 Cases by Country", fontsize=20,
              weight='bold', alpha=.75)
    plot.text(x=covid.index[1], y=int(covid.max().max()) + 15000, s="", fontsize=16, alpha=.75)
    plt.show()



def reload():
    new_data = get_covid_detail_bd()
    mainlabel['text']=new_data


root = tk.Tk()
root.geometry("700x500")
root.title("Covid19 update ")
f = ("poppins", 25, "bold")
banner = tk.PhotoImage(file="covid.png")
bannerlabel = tk.Label(root, image=banner)
bannerlabel.pack()

textfield=tk.Entry(root, width= 50)
textfield.pack()

mainlabel = tk.Label(root, text= get_covid_detail_bd(), font=f)
mainlabel.pack()

gbtn = tk.Button(root, text="Get data", font=f, relief='solid', command=get_country_data)
gbtn.pack()

rbtn = tk.Button(root, text="Reload", font=f, relief='solid', command=reload)
rbtn.pack()

root.mainloop()


