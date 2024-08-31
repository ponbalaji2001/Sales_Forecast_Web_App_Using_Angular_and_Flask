import pandas as pd
import prophet
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

def Forecast(fileName, datasetType, dateIndex, salesIndex, value):
    print(fileName)
    #read the dataset
    df = pd.read_csv("./static/"+fileName)

    if len(df) > 1000:
        df = df.tail(1000)

    df = df.iloc[:, [dateIndex, salesIndex]]

    #To use the prophet model, change column names to "ds" and "y"
    df.columns = ['ds', 'y']
    
    df = df.dropna(subset=['ds']) # Drop rows where 'ds' is NaN

    date_formats = ['%d-%m-%Y', '%m/%y', '%b-%y', '%Y']  # Add more formats as needed
    for fmt in date_formats:
        try:
            df['ds'] = pd.to_datetime(df['ds'], format=fmt, errors='raise')
            break  # If the conversion is successful, exit the loop
        except ValueError:
            continue  
    df['ds'] = pd.to_datetime(df['ds'], errors='coerce') 
    print(df.head())

    #change the "ds" column to datetime format
    df['ds'] = df['ds'].dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['ds']) # Drop rows where 'ds' is NaN

    df['y'] = pd.to_numeric(df['y'], errors='coerce')
    df['y'] = df['y'].fillna(value=0)  # Replace NaN values in column 'y' with 0

    #fit the dataframe into the prophet model
    model = Prophet(interval_width=0.95)
    model.fit(df)
    df.dropna(axis=0, inplace=True)
    r, c = df.shape

    #Make future dates for forecastig
    if datasetType == "Day":
        future_dates = model.make_future_dataframe(periods=value)
    elif datasetType == "Week":
        future_dates = model.make_future_dataframe(periods=value, freq='W-SUN')
    elif datasetType == "Month":
        future_dates = model.make_future_dataframe(periods=value, freq='MS')
    elif datasetType == "Year":
        future_dates = model.make_future_dataframe(periods=value, freq='YS')

    #Forecasting 
    predictFuture = model.predict(future_dates)

    #slice predictFuture dataframe to obtain predicted and forecast value separetely
    df2 = predictFuture[:r+1]
    df2 = df2[['ds', 'yhat', 'trend']]

    df3 = predictFuture[r:]
    df3 = df3[['ds', 'yhat', 'yhat_upper', 'yhat_lower', 'trend']]

    df4 = pd.concat([df, df3], ignore_index=True)
    df4.fillna('NAN', inplace=True)
  
    predictDate = predictFuture['ds']
    predictValue = df2['yhat']
    actualValue = df['y']
    forecastVal = df4['yhat']
    forecastUpper = df4['yhat_upper']
    forecastLower = df4['yhat_lower']
    
    #saving the forecasted dataframe as a csv file for creating a Power BI dashboard
    prediction = predictFuture[['ds','trend','yhat']]
    prediction = prediction.join(df3[['yhat_upper','yhat_lower']])
    prediction = prediction.join(df['y'])
    prediction.to_csv('./static/result/Forecast_Result.csv', index=False)

    #Determine Performance Metrics
    df_cv = cross_validation(model, initial='365 days', period='180 days', horizon='365 days')
    df_p = performance_metrics(df_cv)

    horizon = df_p['horizon'].astype('str')
    rmse =df_p['rmse']
    mse=df_p['mse']
    mae=df_p['mae']
    
    return  predictDate, predictValue, actualValue, forecastVal, forecastUpper, forecastLower, horizon, rmse, mse, mae

       
