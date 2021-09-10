import { Component, OnInit } from '@angular/core';
import { CartService } from 'src/app/features/cart/cart.service'
import {Cart} from 'src/app/shared/models/model';
import {CartItem} from 'src/app/shared/models/model';
import { UserService } from 'src/app/features/auth/services/user.service';
import { UserData } from 'src/app/shared/models/model';
// import {Product} from 'src/app/shared/models/model';
// import { ProductApiService } from 'src/app/features/products/services/product.api.service';
@Component({
  selector: 'app-cart',
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.css']
})
export class CartComponent implements OnInit {
public cartItems:CartItem[];
public user: UserData;
public cart:Cart;
displayedColumns: string[] = ['product',  'qty', 'subtotal','remove'];
// public products: Product[];

  constructor(private cartService:CartService,private authenticationService: UserService) { 
    this.cartItems=this.cartService.cartItems;
    this.cart=this.cartService.cart;
    this.user=this.authenticationService.user;
    //this.products=productApiService.products;
  }

  ngOnInit(): void {
    if (this.isAuth()){
      this.cartService.getCart(this.user.email).subscribe(
        data=>{
          this.cartItems=[];
          this.cart=this.cartService.cart;
          this.cartItems=data
          console.log("here is logged in")
          console.log(this.cartItems);
        }
      );
    }else{
      this.cartItems=[];
      console.log("here is logged out")
      console.log(this.cartItems);
    }
   
  }
public deleteFromCart(id:number):void{
  console.log("here in the delete");
console.log(id);
this.cartService.cartDelete(id, this.cart.id).subscribe(data=>{
  this.cartItems=[];
  this.cart=this.cartService.cart;
  this.cartItems=data
  console.log("delete list")
  console.log(this.cartItems);
});
}
  public isAuth():Boolean{
    //console.log(this.authenticationService.isAuthenticated());
    return (this.authenticationService.isAuthenticated() && this.authenticationService.validateRefresh());
  }

}
