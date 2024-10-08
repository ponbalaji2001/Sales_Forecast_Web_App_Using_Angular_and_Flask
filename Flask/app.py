from flask import Flask, request, jsonify, send_from_directory
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

#Get forecast data
app.config['DOWNLOAD_FOLDER'] = 'static/result'
@app.route('/download', methods=['GET'])
def download_file():
    try:
        filename = 'Forecast_Result.csv'
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)

        # Check if the file exists
        if os.path.isfile(file_path):
            return send_from_directory(
                directory=app.config['DOWNLOAD_FOLDER'],
                path=filename,
                as_attachment=True
            )
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500


#Get the forecast results
@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    j = request.get_json()
    datasetType = j['datasetType']
    dateIndex = j['dateIndex']
    salesIndex = j['salesIndex']
    forecastPeriod = j['forecastPeriod']
    numberOfPeriod = j['numberOfPeriod']

    #call the prophet function based on the forecast period for forecasting
    if forecastPeriod == "Year":
        if datasetType == "Year":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, numberOfPeriod)
        elif datasetType == "Month":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (12*numberOfPeriod))
        elif datasetType == "Week":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (52*numberOfPeriod))
        elif datasetType == "Day":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (365*numberOfPeriod))

    elif forecastPeriod == "Month":
        if datasetType == "Year":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//12))
        elif datasetType == "Month":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, numberOfPeriod)
        elif datasetType == "Week":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (4*numberOfPeriod))
        elif datasetType == "Day":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (30*numberOfPeriod))

    elif forecastPeriod == "Week":
        if datasetType == "Year":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//52))
        elif datasetType == "Month":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//4))
        elif datasetType == "Week":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, numberOfPeriod)
        elif datasetType == "Day":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (7*numberOfPeriod))

    elif forecastPeriod == "Day":
        if datasetType == "Year":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//365))
        elif datasetType == "Month":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//30))
        elif datasetType == "Week":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, (numberOfPeriod//7))
        elif datasetType == "Day":
            d, p, a, f, u, l, h, r, ms, ma = Forecast(fileName, datasetType, dateIndex, salesIndex, numberOfPeriod)

    #sent a response to Angular
    return jsonify({'predictDate': list(d), 'predictVal': list(p), 'actualVal': list(a), 'forecastVal':list(f), 'forecastUp': list(u), 'forecastDown': list(l),  'horizon': list(h), 'rmse': list(r), 'mse': list(ms), 'mae': list(ma)})

if __name__ == '__main__':
    app.run(debug=True)
