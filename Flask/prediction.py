import pandas as pd
import prophet
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics

def Forecast(fileName,value):
    print(fileName)
    #read the dataset
    df = pd.read_csv("./static/"+fileName)
    
    #To use the prophet model, change column names to "ds" and "y"
    df.columns = ['ds', 'y']

    #change the "ds" column to datetime format
    df['ds'] = pd.to_datetime(df['ds'])

    #fit the dataframe into the prophet model
    model = Prophet()
    model.fit(df)
    df.dropna(axis=0, inplace=True)
    r, c = df.shape

    #Make future dates for forecastig
    future_dates = model.make_future_dataframe(periods=value)
    #future_dates = model.make_future_dataframe(periods=value, freq='MS') -----> Monthly data

    #Forecasting 
    predictFuture = model.predict(future_dates)

    #slice predictFuture dataframe to obtain predicted and forecast value separetely
    df2 = predictFuture[:r]
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
    prediction.to_csv('C:/datasets/Power BI/Predicted.csv', index=False)

    #Determine Performance Metrics
    df_cv = cross_validation(model, initial='200 days',period='180 days', horizon='365 days')
    #df_cv = cross_validation(model, initial='730 days',period='180 days', horizon='365 days') -----> monthly data
    df_p = performance_metrics(df_cv)

    horizon = df_p['horizon'].astype('str')
    rmse =df_p['rmse']
    mse=df_p['mse']
    mae=df_p['mae']
    
    return  predictDate, predictValue, actualValue, forecastVal, forecastUpper, forecastLower, horizon, rmse, mse, mae

       
