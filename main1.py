import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime

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

    print(all_detail)

def get_country_data():
    name= textfield.get()
    url="https://worldometers.info/coronavirus/country/"+name
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="content-inner").findAll("div", id="maincounter-wrap")
    all_detail = ""

    for i in range(3):
        text = info_div[i].find("h1", class_=None).get_text()

        count = info_div[i].find("span", class_=None).get_text()

        all_detail = all_detail + text + " " + count + "\n"


get_covid_detail_bd()