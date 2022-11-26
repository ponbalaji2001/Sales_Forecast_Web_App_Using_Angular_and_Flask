import { Injectable } from '@angular/core';

@Injectable()
export class ChartDataService {
  _date: any;
  predict: any;
  forecastVal: any;
  forecastUp: any;
  forecastDown: any;
  actual: any;
  horizon: any;
  rmse: any;
  mse: any;
  mae: any;

  ChartData(d:any, p:any, f:any, fu:any, fd:any, a:any, h:any, r:any, ms:any, ma:any) {
    this._date = d;
    this.predict = p;
    this.forecastVal = f;
    this.forecastUp = fu;
    this.forecastDown = fd;
    this.actual = a;
    this.horizon = h;
    this.rmse = r;
    this.mse = ms;
    this.mae = ma;
  }

  constructor() {}
}
