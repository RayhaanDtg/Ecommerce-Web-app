import { Injectable } from '@angular/core';
import { UserData } from 'src/app/shared/models/model';

import { UserService } from 'src/app/features/auth/services/user.service'
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import {Address} from 'src/app/shared/models/model';


@Injectable({
  providedIn: 'root'
})
export class AccountServiceService {
  baseUrl = `http://127.0.0.1:8000/Address/`;
  public user:UserData;
  public address:Address

  //private address:Address;

  constructor(private userService:UserService,private http: HttpClient) {
    this.user=userService.user;
    this.address={
      address_line_1:"",
      address_line_2:"",
      city:"",
      state:"",
      phone_number:0,
      billing_profile:0,
      id:0
    }
   }

   public get_address(): Observable<any> {
    let parameter = new HttpParams().set("email",this.userService.user.email)
    console.log("Trying to get address and printing param")
    console.log(parameter)
    return this.http.get<any>(`${this.baseUrl}`,{ params: parameter } ).pipe(map(data => {
     
      console.log(data.address)
      this.address.address_line_1=data.address.address_line_1
      this.address.address_line_2=data.address.address_line_2
      this.address.city=data.address.city
      this.address.state=data.address.state
      this.address.phone_number=data.address.phone_number
      this.address.billing_profile=data.address.billing_profile
      this.address.id=data.address.id
      console.log("This is address details")
      console.log(data.address_line_1)
      return this.address;
      
      //localStorage.setItem("currentUser",data);
    }

    ))
  }

  public saveData(): Observable<Address> {
 console.log("this is details being sent to backend")
    console.log(this.address)
    return this.http.post<Address>(`${this.baseUrl}save/`,this.address);
  }
}
