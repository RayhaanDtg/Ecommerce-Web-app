import { HttpClient, HttpHeaders } from '@angular/common/http';
import { stringify } from '@angular/compiler/src/util';
import { Injectable } from '@angular/core';
//import { Observable } from 'rxjs';
import { UserData } from 'src/app/shared/models/model';
import { map } from 'rxjs/operators';
import jwt_decode from 'jwt-decode';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  //private user:UserData;
  private httpOptions: any;
  public accessToken: any;
  public refreshToken: any;
  private refreshTokenTimeout?:any;
 

  public user: UserData;
  //public token:any;
  //public payload:any=[];


  // the username of the logged in user
  //private refreshTokenTimeout:TimeOut;

  // error messages received from the login attempt
  public errors: any = [];
  baseUrl = `http://127.0.0.1:8000/Users/`;
  constructor(private http: HttpClient) {
    this.user = {
      email: '',
      first_name: '',
      last_name: '',
      password: '',

      userId: 0
    }
    
      this.accessToken = localStorage.getItem("currentUserAccess");
    
    
    this.refreshToken = localStorage.getItem("currentUserRefresh");
    this.setUser();
    this.httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };
  }
  changeUser(user: UserData) {
    this.user = user
  }
  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint

  // Refreshes the JWT token, to extend the time the user is logged in

  public loginUser(email: String, password: String): Observable<any> {

    return this.http.post<any>(`${this.baseUrl}login/`, { email, password }, ).pipe(map(data => {
      this.accessToken = data.access
      this.refreshToken = data.refresh
      this.setUser();
      this.checkExpiryToken();
      
      //this.cartService.getCart(this.user.email);
      console.log(this.refreshToken);
      
      return data;
      //localStorage.setItem("currentUser",data);
    }

    ))
  }
  public setUser(){
    let payload = this.getDecodedAccessToken(this.accessToken);
     
      if(payload){
        this.user.first_name = payload.first_name
        this.user.last_name = payload.last_name
        this.user.email = payload.email
        this.user.userId = payload.user_id
      }
      
  }

// checks if the user has a valid refresh token and that the refresh token is not expired
  public validateRefresh():Boolean{
    
    const token = localStorage.getItem('currentUserRefresh');
    if (token){
     if(this.isExpValid(token)){
       return true;
     }
     else{
       return false;
     }
    }
    else{
      return false;
    }
    

  }
  //checks if a user has an access token and is authenticated
  public isAuthenticated():Boolean{
    //let val=false;
    const token = localStorage.getItem('currentUserAccess');
    if (token){
      if(this.isExpValid(token)){
        return true;
      }
      else{
        return false;
      }
     }
     else{
       return false;
     }

  }
  // true if token expired, else false
  private isExpValid(token:any): boolean{
   
    const jwtToken = this.getDecodedAccessToken(token);
    //console.log("here is the jwt token")
    
    const expires = new Date(jwtToken.exp * 1000);
    return expires.getTime() >= Date.now() ;
  }
  //returns the payload of the token
  getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    }
    catch (Error) {
      return null;
    }
  }
  //checks the expiry of the access token and then calls the timer for refreshing the token
  private checkExpiryToken(): void {
    // console.log("here is the access token after refresh")
    // console.log(this.accessToken)
    const jwtToken = this.getDecodedAccessToken(this.accessToken);
    // console.log("here is the jwt token")
    // console.log(jwtToken);
    // console.log(jwtToken.exp);
    const expires = new Date(jwtToken.exp * 1000);
    let timeout = expires.getTime() - Date.now() - (60 * 1000);
    // console.log("Waiting for timeout")
     setTimeout(() => this.refreshTokenFunction().subscribe(), timeout);
    //  console.log("Timeout done")
    //return timeout;
  }

  //retrieves the new access function using the refresh token
 public refreshTokenFunction() {
   let refresh=localStorage.getItem("currentUserRefresh");
  //  console.log("got into the refresh")
  //  console.log(refresh)
    return this.http.post<any>(`${this.baseUrl}refresh/`, {refresh})
        .pipe(map((token) => {
          // console.log("got here for the new acces token after refresh")
          // console.log(token)
            this.accessToken=token.access;
            // console.log(this.accessToken);
            localStorage.setItem("currentUserAccess",JSON.stringify(this.accessToken))
            this.checkExpiryToken();
            //return this.accessToken;
        }));
}
private stopRefreshTokenTimer() {
  clearTimeout(this.refreshTokenTimeout);
}
public logout() {
  //this.http.post<any>(`${environment.apiUrl}/users/revoke-token`, {}, { withCredentials: true }).subscribe();
  this.stopRefreshTokenTimer();
  this.user = {
    email: '',
    first_name: '',
    last_name: '',
    password: '',

    userId: 0
    
  }
  localStorage.removeItem("currentUserAccess");
  localStorage.removeItem("currentUserRefresh");
 this.refreshToken='';
 this.accessToken='';
}
  
  public registerUser(): Observable<UserData> {
    // console.log(this.user)
    return this.http.post<UserData>(`${this.baseUrl}register/`, this.user);
  }
  public getAllUsers(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}`);
  }
}
