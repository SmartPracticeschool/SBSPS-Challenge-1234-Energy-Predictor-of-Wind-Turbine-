from flask import Flask,redirect,request,url_for,json_available,render_template
import pickle
import requests
import json
import pandas as pd
import os

port = int(os.getenv('PORT', 8000))

#def mypredic(lat,log)
app = Flask(__name__)


@app.route("/",methods=['GET','POST'])
def home():
    #feature = request.form['u2']
    return render_template('login.html')

@app.route('/pre',methods=['POST'])
def pre():
    values = [request.form['log'],request.form['lat']]
    lat = str(values[0])
    log = str(values[1])
    
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+lat+'&lon='+log+'&%20exclude=houly&appid=2be1dca4896e5b73df449f2570ee7c29'


    model = pickle.load(open('model.pkl','rb'))

    respon = requests.get(url)  

    respon_json = respon.json()

    data = respon_json['hourly']

    df = pd.DataFrame(data)

    test_data = df.loc[:,['wind_speed','wind_deg']]

    pred = model.predict(test_data)
    

    
    dates = pd.to_datetime(df['dt'],unit='s')
    df_2  = pd.DataFrame(dates)
    df_2['Value'] = pred
    Top_10 = df_2.nlargest(10, ['Value'])
    df_main = pd.DataFrame(Top_10)
    list= df_main.values.tolist()
    
     #val = df_main['Value'].tolist()
    return render_template('login.html',list=list,log=log,lat=lat)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)