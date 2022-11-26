import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';


@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent implements OnInit {
  constructor(private http: HttpClient, private router: Router) {}

  fullName = '';
  email = '';
  password = '';
  confirmPassword = '';

  @ViewChild('myForm') form: NgForm;

  showpassword = false;
  showConfirmPassword = false;

  ngOnInit(): void {}

  //Add a user to the JSON server
  AddUser() {
    this.http
      .post('http://localhost:3000/UserData', {
        Name: this.fullName,
        Email: this.email,
        Password: this.password,
      })
      .subscribe(
        (res: any) => {
          console.log(res);
          alert('Account created successfully');
          this.router.navigate(['login']);
        },
        (error: any) => {
          console.log(error);
        }
      );
  }

  onsubmit() {
    console.log(this.form);
  }

  passwordShow() {
    this.showpassword = !this.showpassword;
  }

  confirmPasswordShow() {
    this.showConfirmPassword = !this.showConfirmPassword;
  }
}
  


