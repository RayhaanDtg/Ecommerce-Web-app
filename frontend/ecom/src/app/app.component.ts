import { Component } from '@angular/core';
import { UserService } from 'src/app/features/auth/services/user.service';
import { UserData } from 'src/app/shared/models/model';
import { Router } from '@angular/router';
import { CartService } from 'src/app/features/cart/cart.service'

import { Cart } from 'src/app/shared/models/model';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  public user: UserData;
  title = 'ecom';
  constructor(private authenticationService: UserService, private router: Router,private cartService:CartService) {
    this.user=this.authenticationService.user;
    console.log(this.user);

}

public isAuth():Boolean{
  //console.log(this.authenticationService.isAuthenticated());
  return (this.authenticationService.isAuthenticated() && this.authenticationService.validateRefresh());
}
public logOut(){
  this.authenticationService.logout();
  this.router.navigate(['/login']);
}
public getCart(){
  console.log("port of entry for cart shit");
  
  console.log(this.user.email)
 this.cartService.getCart(this.user.email).subscribe(
  data=>{
    console.log("function of cart successful")
  }
);
  console.log("port of exit for cart shit");
}
}
