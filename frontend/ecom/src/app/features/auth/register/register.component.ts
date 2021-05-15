import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { UserData } from 'src/app/shared/models/model';
import {UserService} from 'src/app/features/auth/services/user.service'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
registerForm:FormGroup;

public user:UserData;
public users: UserData[];
public exists:boolean;


constructor(private fb:FormBuilder, private userService:UserService) {
  this.user = {
    email:'',
    first_name:'',
    last_name:'',
    password:'',
    //token:'',
    userId:0
  }
  this.users=[];

  this.exists=false;
 
  this.registerForm=this.createFormBuilder(this.fb);
  
 }


  ngOnInit(): void {
    this.registerForm.valueChanges.subscribe(val => {
      this.user.email=val.email
      this.user.first_name=val.firstname
      this.user.last_name=val.lastname
      this.user.password=val.password
 });

  }

  private createFormBuilder(formBuilder:FormBuilder){
    return  formBuilder.group({
      email:['', [Validators.required,Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
      firstname:['', [Validators.required, Validators.maxLength(20), Validators.pattern("^[a-zA-Z]+$")]],
      lastname:['', [Validators.required, Validators.maxLength(20), Validators.pattern("^[a-zA-Z]+$")]],
      password:['',[Validators.required]]

    });
   
  }
  public setUser(user:UserData){
    this.userService.changeUser(user)
  }
  get firstname() {
    return this.registerForm.get('firstname');
  }
 
  get lastname() {
    return this.registerForm.get('lastname');
  }
 
  get email() {
    return this.registerForm.get('email');
  }
  
  get password(){
    return this.registerForm.get('password');
  }
  public onSubmit():void{
    this.setUser(this.user)
    console.log(this.user)
    this.userService.registerUser().subscribe(data=>
      {
        alert('user has been registered')
      },
      error=>alert(error.error.email[0])
    
    );
    
   
    
   
   
  }

}
