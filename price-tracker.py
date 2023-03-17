import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secretss import user_email, user_password


import requests
from bs4 import BeautifulSoup

user = user_email
password = user_password
url = 'https://www.amazon.in/Crucial-500GB-NAND-NVMe-PCIe/dp/B086BGWNY8/ref=asc_df_B086BGWNY8/?tag=googleshopdes-21&linkCode=df0&hvadid=397081015634&hvpos=&hvnetw=g&hvrand=9352131983268838655&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=20460&hvtargid=pla-973021540717&psc=1&ext_vrnc=hi'


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
           'accept': '*/*',
           'referer': 'https://www.amazon.in/Crucial-500GB-NAND-NVMe-PCIe/dp/B086BGWNY8/ref=asc_df_B086BGWNY8/?tag=googleshopdes-21&linkCode=df0&hvadid=397081015634&hvpos=&hvnetw=g&hvrand=9352131983268838655&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=20460&hvtargid=pla-973021540717&ext_vrnc=hi&th=1',
           'Origin': 'https://www.amazon.in'
          }

def get_price(url, headers):

    with requests.Session() as s:
        response = s.get(url, headers=headers)
        html = response.text
        print(html)

        bs = BeautifulSoup(html, 'html.parser')

        price_span = bs.find_all(attrs={'class': 'a-offscreen'})
        price = price_span[0].string[1:].replace(',', '')
        print("price: %s" % price)

        p = float(price)
        print(p)

        return p


def send_email(price):
    global user, password

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = user
    msg['Subject'] = "Amazon price alert !"
    body = 'Price dropped! Current price is: %s' % price
    msg.attach(MIMEText(body, 'plain'))


    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, user, msg.as_string())
        server.quit()
        print("Sent Email Successfully")

while True:
    price = get_price(url, headers)
    if price <= 3600:
        send_email(price)

    time.sleep(60 * 30)













