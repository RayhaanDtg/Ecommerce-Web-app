import { Component, OnInit } from '@angular/core';
import { Product } from 'src/app/shared/models/model';
import { Cart } from 'src/app/shared/models/model';
import { ProductApiService } from 'src/app/features/products/services/product.api.service';
import { CartService } from 'src/app/features/cart/cart.service'
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/features/auth/services/user.service';
import { UserData } from 'src/app/shared/models/model';
import {CartItem} from 'src/app/shared/models/model';


@Component({
  selector: 'app-product-detail',
  templateUrl: './product-detail.component.html',
  styleUrls: ['./product-detail.component.css']
})
export class ProductDetailComponent implements OnInit {
  public product: Product;
  public increment: any;
  public cart_items:CartItem[];
  public cart:Cart;
  public user: UserData;
 // public cart: Cart;
  constructor(private productApiService: ProductApiService,private cartService:CartService,private authenticationService: UserService,private router: Router){
    this.product={
      id: 0,
      title: "",
      description: "",
      price: 0,
      slug:"",
      image:"",
      quantity: 0
    };
   
    this.increment=0;
    this.cart_items=this.cartService.cartItems;
    this.cart=this.cartService.cart;
    this.user=this.authenticationService.user;
    //here we call the getcart of the cartservice because it is acting like an Observable from which we want data
    //subscring to it in the constructor will ensure that all value concerning cart will be available the moment components created.
    this.cartService.getCart(this.user.email).subscribe(data=>{
    
        this.cart_items=this.cartService.cartItems;
     
        this.cart=this.cartService.cart;
    });

    
  }

  

  ngOnInit(): void {
    this.productApiService.getDetailProducts().subscribe(data => {
     
       this.product=data
       //this.cart_items=this.cartService.cartItems;

       if(this.inCart()){
        let obj= this.cart_items.find(i=>i.product.slug===this.product.slug)
     
       this.increment=obj?.qty
      
       }
localStorage.setItem('product', this.product.slug);
     
    })
   
    
    
  }
public modify(){
  this.modifyCart(this.increment,this.user.email,this.product.slug);
}
  public modifyCart(qty:number,email:string,slug:string){
    if(this.isAuth()){
      this.cartService.modifyCart(email,qty,slug).subscribe(data=>{
       
        this.cart_items=data;
        this.router.navigate(['/cart']);
      },
      error=>{
        console.log(error);
        
      }
      )
    }
  }
public increase(){
  if(this.increment<10){
    this.increment++;
  }

}
public inCart():boolean{
  let bool:boolean=false;
  this.cartService.cartItems.forEach(value=>{
    
    if(value.product.slug==this.product.slug){
      bool=true;
    }
  })
  
  return bool;
}
public decrease(){
  if(this.increment>1){
    this.increment--;
  }
}

public isAuth():Boolean{
  //console.log(this.authenticationService.isAuthenticated());
  return (this.authenticationService.isAuthenticated() && this.authenticationService.validateRefresh());
}
}
