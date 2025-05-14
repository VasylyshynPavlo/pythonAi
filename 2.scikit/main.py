import requests
import pandas as pd
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

rates = []
dates = []
today = datetime.date.today()
#тут змінити 100 на число днів за якими треба прости навчання
for i in range(100, 0, -1):
    day = today - datetime.timedelta(days=i)
    date_str = day.strftime("%Y%m%d")
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={date_str}&json"
    r = requests.get(url)
    if r.status_code == 200 and r.json():
        data = r.json()[0]
        rates.append(data["rate"])
        dates.append(day)
    else:
        print(f"Failed to fetch data for {day}")

df = pd.DataFrame({"date": dates, "rate": rates})
df["day_num"] = np.arange(len(df))

model = LinearRegression()
X = df[["day_num"]]
y = df["rate"]

model.fit(X, y)

future_days = np.arange(len(df), len(df) + 10).reshape(-1, 1)
future_rates = model.predict(future_days)

print("\nNBU USD Exchange Rate Forecast for the Next 10 Days:")
for i in range(10):
    day = today + datetime.timedelta(days=i + 1)
    print(f"{day}: {future_rates[i]:.2f} UAH")
