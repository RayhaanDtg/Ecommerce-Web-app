import { Injectable } from '@angular/core';
import { UserService } from 'src/app/features/auth/services/user.service'
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { CartService } from 'src/app/features/cart/cart.service'
import { Cart } from '../models/model';

@Injectable({
  providedIn: 'root'
})
export class AuthguardService implements CanActivate {

  constructor(
    private router: Router,
    private userService: UserService,
   // private cartService:CartService
    
  ) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    //const user = this.userService.user;
    if (this.userService.isAuthenticated()) {
      //  let cart:any;
      //  cart=this.cartService.getCart(this.userService.user.email)
        return true;
    } else {
        // not logged in so redirect to login page with the return url
        this.router.navigate(['/login'], { queryParams: { returnUrl: state.url } });
        return false;
    }
}
}
