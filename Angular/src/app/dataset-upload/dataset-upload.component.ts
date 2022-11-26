import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { UserNameService } from '../services/userNameService.service';
import { ChartDataService } from '../services/chartDataService.service';

@Component({
  selector: 'app-dataset-upload',
  templateUrl: './dataset-upload.component.html',
  styleUrls: ['./dataset-upload.component.css'],
})
export class DatasetUploadComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private router: Router,
    private userName: UserNameService,
    private chartDataServ: ChartDataService
  ) {}

  @ViewChild('myForm') form: NgForm;
  rang: string;
  val: string;
  show: boolean = false;
  name: any;
  filename: any;

  ngOnInit(): void {
    
    //get the user name from the userName service
    this.name = this.userName.user_name;
    console.log(this.name);
  }

  //uploading the file to the Flask
  uploadFile(file: any) {
    var formData = new FormData();
    formData.append('file', file.files[0]);
    console.log(file.files[0]);
    const headers = new HttpHeaders({
      'Access-Control-Allow-Origin': 'http://localhost:4200',
      'Access-Control-Allow-Methods': 'POST',
      'Access-Control-Allow-Headers': 'multipart/form-data',
    });

    this.http
      .post('http://127.0.0.1:5000/upload', formData, { headers: headers })
      .subscribe(
        (res: any) => {
          console.log(res);
          alert('File uploaded successfully');
        },
        (error: any) => {
          console.log(error);
        }
      );
  }

  submitData() {
    this.show = !this.show;
    const headers = new HttpHeaders({
      'Access-Control-Allow-Origin': 'http://localhost:4200',
      'Access-Control-Allow-Methods': 'POST',
      'Access-Control-Allow-Headers': 'application/json',
      'Content-Type': 'application/json',
    });

    //sent the forecast range and value to the Flask
    this.http
      .post(
        'http://127.0.0.1:5000/input',
        { rang: this.rang, val: this.val },
        { headers: headers }
      )
      .subscribe(
        (res: any) => {
          console.log(res);
          console.log('submitted successfully');
          alert('Forecast Done');

          //Send the response data to Chart Service
          this.chartDataServ.ChartData(
            res['predictDate'],
            res['predictVal'],
            res['forecastVal'],
            res['forecastUp'],
            res['forecastDown'],
            res['actualVal'],
            res['horizon'],
            res['rmse'],
            res['mse'],
            res['mae']
          );
          this.router.navigate(['chart']);
        },
        (error: any) => {
          console.log(error);
        }
      );
  }

  onsubmit() {
    console.log(this.form);
  }

  logout() {
    this.router.navigate(['login']);
  }
}


