import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { UserNameService } from '../services/userNameService.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
  constructor(
    private http: HttpClient,
    private router: Router,
    private userNameServ: UserNameService
  ) {}

  @ViewChild('myForm') form: NgForm;
  email = '';
  password = '';
  fullname = '';
  showpassword = false;

  ngOnInit(): void {}

  //Check if the user data is present in the JSON server
  login() {
    this.http.get<any>('http://localhost:3000/UserData').subscribe((res) => {
      console.log(res);
      const user = res.find((a: any) => {
        this.fullname = a.Name;
        return a.Email === this.email && a.Password === this.password;
      });

      if (user) {
        //Assign the name to userName Service
        this.userNameServ.user_name = this.fullname;
        this.router.navigate(['forecast']);
      } else {
        alert('Invalid Credentials');
      }
    });
  }

  onsubmit() {
    console.log(this.form);
  }

  toggleShow() {
    this.showpassword = !this.showpassword;
  }
}
  
     
    
       

