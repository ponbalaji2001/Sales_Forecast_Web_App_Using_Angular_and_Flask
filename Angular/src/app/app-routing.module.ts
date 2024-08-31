import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DatasetUploadComponent } from './dataset-upload/dataset-upload.component';
import { LoginComponent } from './login/login.component';
import { MychartComponent } from './mychart/mychart.component';
import { SignupComponent } from './signup/signup.component';

const routes: Routes = [
  {path:'', redirectTo:'login',pathMatch:'full'},
  {path:'login', component:LoginComponent},
  {path:'signup', component:SignupComponent},
  {path:'forecast',component:DatasetUploadComponent},
  {path:'chart', component:MychartComponent}


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
