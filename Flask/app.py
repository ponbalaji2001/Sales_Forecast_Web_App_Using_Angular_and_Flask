from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from prediction import Forecast

app = Flask(__name__)
CORS(app)

#Get the file from Angular and store it locally
app.config['UPLOAD_FOLDER'] = 'static'
@app.route('/upload', methods=['GET', 'POST'])
def upload_dataset():
    global fileName
    file = request.files['file']
    fileName = secure_filename(file.filename)
    print(fileName)
    file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], fileName))
    return jsonify({'Flask': 'File uploaded'})

#Get the forecast range and value from Angular
@app.route('/input', methods=['GET', 'POST'])
def input_data():
    j = request.get_json()
    rang = j['rang']
    val = j['val']
    print(rang, val)

    #call the prophet function based on the forecast range for forecasting
    if (rang == "Year"):
        #d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, (12*val)) -----> Monthly data
        d, p, a, f, u, l, h, r, ms, ma =Forecast(fileName,(365*val))

    elif (rang == "Month"):
        #d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, (val)) -----> Monthly data
        d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, (30*val))

    #In contrast to daily data, monthly data is inadequate for forecasting weeks and days.
    elif (rang == "Week"):
        d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, (7*val))

    elif (rang == "Day"):
        d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, val)
    
    #sent a response to Angular
    return jsonify({'predictDate': list(d), 'predictVal': list(p), 'actualVal': list(a), 'forecastVal':list(f), 'forecastUp': list(u), 'forecastDown': list(l),  'horizon': list(h), 'rmse': list(r), 'mse': list(ms), 'mae': list(ma)})

if __name__ == '__main__':
    app.run(debug=True)
