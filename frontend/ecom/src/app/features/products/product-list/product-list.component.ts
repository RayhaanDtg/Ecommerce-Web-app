import { Component, OnInit } from '@angular/core';
import { Product } from 'src/app/shared/models/model';
import { Cart } from 'src/app/shared/models/model';
import { ProductApiService } from '../services/product.api.service';

@Component({
  selector: 'app-product-list',
  templateUrl: './product-list.component.html',
  styleUrls: ['./product-list.component.css']
})
export class ProductListComponent implements OnInit {

  public products: Product[];
  public tempProduct:Product;
  //public cart: Cart;
  constructor(
    private productApiService: ProductApiService
  ) {
    this.products = [];
    this.tempProduct={
      id:0,
      title:'',
      description:'',
      price:0,
      quantity:0,
      slug:'',
      image:'',


    }
    
  }

  ngOnInit(): void {
    this.productApiService.getAllProducts().subscribe(data => {
      this.products=data;
      
     

     
    })
    
  }

  // public addProductToCart(product: Product): void {
  //   if(!product.existInCart){
  //     this.cart.products.push(product);
  //     console.log(this.cart.products);
  //   product.existInCart=true;

  //   } else{
  //     console.log("already in cart!!");
  //   }
  // }

  // public removeFromCart(product:Product):void{
  //   if(product.existInCart){

  //     this.cart.products.forEach((productinCart,index)=>{
  //       if(productinCart.id===product.id){
  //         this.cart.products.splice(index,1);
  //         product.existInCart=false;
  //       }
  //     });
  //     console.log(this.cart.products);
   

  //   } 
  // }

 public changeSlug(slug:string):void{
   this.productApiService.setSlug(slug);
 }

 

  

}
