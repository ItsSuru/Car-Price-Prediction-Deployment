'''from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

"""
@app.route('/success/<output>')
def success(output):
   return jsonify(output)"""

@app.route('/query-example', methods=['POST','GET'])
def query_example():
    l1 = request.args.get('l1')
    l2 = request.args.get('l2')
    l3 = request.args.get('l3')
    l4 = request.args.get('l4')
    l5 = request.args.get('l5')
    l6 = request.args.get('l6')
    l7 = request.args.get('l7')
    l8 = request.args.get('l8')
    prediction = model.predict([[int(l1), np.log(int(l2)), int(l3), int(l4), int(l5), int(l6), int(l7), int(l8)]])
    output = round(prediction[0], 2)
    data={}
    data={
        "result":output
    }
    data=json.dumps(data)
    if output < 0:
        #return 0
        return data
    else:
        #return str(output)
        return data
if __name__ == '__main__':
    app.run(debug=True,port=4040)'''

from flask import Flask, render_template, request, url_for
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        Year=2020-Year
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('result.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('result.html',prediction_text="You Can Sell The Car at {} lacks".format(output))
    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True, port=3000)
