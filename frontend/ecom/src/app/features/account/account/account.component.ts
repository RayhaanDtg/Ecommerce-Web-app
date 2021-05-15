import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import { Observable } from 'rxjs';
import { AccountServiceService } from 'src/app/features/account/account-service.service'
import {Address} from 'src/app/shared/models/model';
import {UserData} from 'src/app/shared/models/model';
import { UserService } from 'src/app/features/auth/services/user.service'
import { Router, ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
public userForm:FormGroup;
public shippingForm:FormGroup;
public address:Address
public user:UserData
public isDisabledUser:Boolean;
public isDisabledShip:Boolean;
public returnUrl: string;
 
  constructor(private accountService:AccountServiceService,private userService:UserService,private fb:FormBuilder,
    private route: ActivatedRoute,
    private router: Router){
    this.address={
      address_line_1:"",
      address_line_2:"",
      city:"",
      state:"",
      phone_number:0,
      billing_profile:0,
      id:0
      
    }
    this.user=userService.user
    this.userForm=this.createFormBuilderUser(this.fb);
    this.shippingForm=this.createFormBuilderShipping(this.fb);
    //this.enabled=false;
    this.isDisabledUser=true;
    this.isDisabledShip=true;
    this.returnUrl='';
    // this.userForm.disable();
    // this.shippingForm.disable();
  }

  ngOnInit(): void {
    this.getUserAddress()
    
      this.userForm.valueChanges.subscribe(val => {
        this.address.phone_number=val.phone_number
        console.log("trying to get the phone number")
        console.log(val.phone_number)
        console.log(this.address.phone_number)
       
   });
   this.shippingForm.valueChanges.subscribe(val => {
    this.address.address_line_1=val.address_line_1
    console.log("trying to get the address for form")
        console.log(val.address_line_1)
        console.log(this.address.address_line_1)
    this.address.address_line_2=val.address_line_2
    this.address.city=val.city
    this.address.state=val.state
   
  });
    
   

  this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
  
  }


  private createFormBuilderShipping(formBuilder:FormBuilder){
    return  formBuilder.group({
      address_line_1:[''],
      address_line_2:[''],
      city:[''],
      state:['']
    });
   
  }
  private createFormBuilderUser(formBuilder:FormBuilder){
    return  formBuilder.group({
      
      phone_number:['']

    });
   
  }
  get phone_number(){
    return this.userForm.get('phone_number')
  }
  get address_line_1(){
    return this.shippingForm.get('address_line_1')
  }
  get address_line_2(){
    return this.shippingForm.get('address_line_2')
  }

  get city(){
    return this.shippingForm.get('city')
  }
  get state(){
    return this.shippingForm.get('state')
  }
  private getUserAddress(){
  this.accountService.get_address().subscribe(
    data=>{
      this.address=data
      console.log(this.address)
    }
  )
  }

 public  editShipping():void{
    this.isDisabledShip=false;
  }
  public  editUser():void{
    this.isDisabledUser=false;
  }
  private setAddress(){
    console.log(this.address.id)
    this.accountService.address=this.address
  }

public saveData(){
this.setAddress();
this.accountService.saveData().subscribe(data=>{
console.log(data)
this.router.navigate([this.returnUrl]);

},
error=>console.log(error)
);
}
 
}
