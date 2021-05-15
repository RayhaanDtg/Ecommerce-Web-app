import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { UserData } from 'src/app/shared/models/model';
import { UserService } from 'src/app/features/auth/services/user.service'
import { first } from 'rxjs/operators';
import { stringify } from '@angular/compiler/src/util';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;

  public token:any[];
  public user: UserData;
  public users: UserData[];
  public exists: boolean;
 public returnUrl: string;

  constructor(private fb:FormBuilder, private userService:UserService,private route: ActivatedRoute,
    private router: Router) {
    this.user = {
      email:'',
      first_name:'',
      last_name:'',
      password:'',
      
      userId:0
    }
    this.users=[];
    this.token=[];
  
    this.exists=false;
    this.returnUrl='';
   
    this.loginForm=this.createFormBuilder(this.fb);
    if (this.userService.isAuthenticated()) { 
      this.router.navigate(['/']);
    }
    
   }

  ngOnInit(): void {
    this.loginForm.valueChanges.subscribe(val => {
      this.user.email=val.email
      
      this.user.password=val.password
 });
 this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
 
  }

  private createFormBuilder(formBuilder:FormBuilder){
    return  formBuilder.group({
      email:['', [Validators.required,Validators.pattern("^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$")]],
      password:['']

    });
   
  }

  get email() {
    return this.loginForm.get('email');
  }
  
  get password(){
    return this.loginForm.get('password');
  }

  public onSubmit():void{
    
   this.userService.loginUser(this.user.email,this.user.password).subscribe(
     data=>{
    //  this.user.email=data.email
    //  this.user.first_name=data.first_name
    //  this.user.last_name=data.last_name
    //  this.user.token=data.token
     
     if (data.access && data.refresh){
       

       localStorage.setItem("currentUserAccess",data.access);
      localStorage.setItem("currentUserRefresh",data.refresh);
       
     }
     
     this.router.navigate([this.returnUrl]);
     
     },
     error=>console.log(error)
   )
     
    
   
   
  }
}
