import { Component, Input, OnInit } from '@angular/core';
import {UserData} from  'src/app/shared/models/model';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs';

declare let $: any;
@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  //  userModel :UserData;
  // loginForm:FormGroup;
  // registerForm:FormGroup;


  constructor(private fb:FormBuilder) {
    // this.userModel = {
    //   email:'',
    //   first_name:'',
    //   lastname:'',
    //   password:''
    // }
    // this.loginForm=this.createFormBuilder(this.fb,2);
    // this.registerForm=this.createFormBuilder(this.fb,1);
    
   }

  ngOnInit(): void {
    
  }
  // private createFormGroup(){
  //   return new FormGroup({
  //     email:new FormControl(),
  //     firstname:new FormControl(),
  //     lastname:new FormControl()
  //   });
  // }
  

  
  
  
}
