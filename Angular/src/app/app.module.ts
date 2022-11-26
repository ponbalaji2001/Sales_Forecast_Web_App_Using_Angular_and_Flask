import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { DatasetUploadComponent } from './dataset-upload/dataset-upload.component';
import { ChartsModule } from 'ng2-charts';
import { MychartComponent } from './mychart/mychart.component';
import {UserNameService} from './services/userNameService.service';
import { ChartDataService } from './services/chartDataService.service';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    DatasetUploadComponent,
    MychartComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule,
    FormsModule,
    ChartsModule,
  ],
  providers: [UserNameService,
              ChartDataService],
  bootstrap: [AppComponent],
})
export class AppModule {}
