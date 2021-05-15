import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Product } from 'src/app/shared/models/model';
import { environment } from 'src/environments/environment';
import {Cart} from 'src/app/shared/models/model';
import { BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';
import { ThrowStmt } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class ProductApiService {
  public products: Product[];
  public tempProduct:Product;
  private currentSlug="";
  //public array:any[];
 
  baseUrl = `http://127.0.0.1:8000/`;

  constructor(private http: HttpClient) { 
    this.products = [];
    //this.array=[];
    this.tempProduct={
      id:0,
      title:'',
      description:'',
      price:0,
      quantity:0,
      slug:'',
      image:'',


    }
    console.log("constructor gets refreshed");
   // this.currentSlug=JSON.parse(localStorage.getItem('product'));
  }

 
  public getAllProducts(): Observable<any> {

      return this.http.get<any>(`${this.baseUrl}products`).pipe(map(data=>{
        console.log("og data")
        this.products=[]
      console.log(data.products)
      for (let i = 0; i < data.products.length; i++) {
        
        this.tempProduct={
          id:0,
          title:'',
          description:'',
          price:0,
          quantity:0,
          slug:'',
          image:'',
    
    
        }
        this.tempProduct.id=data.products[i]['product'].id
     
      this.tempProduct.title=data.products[i]['product'].title
      
      this.tempProduct.description=data.products[i]['product'].description
      this.tempProduct.price=data.products[i]['stock'].price
      this.tempProduct.quantity=data.products[i]['stock'].quantity
      this.tempProduct.slug=data.products[i]['product'].slug
      this.tempProduct.image=data.products[i]['product'].image
      console.log("here is shit")
      console.log(this.tempProduct)
      console.log(this.products)
      this.products.push(this.tempProduct);
    }      
    return this.products;
      }));
  }

  public setSlug(slug: string) {
    this.currentSlug=slug;
    console.log(this.currentSlug);
    
  }

  public getDetailProducts():Observable<any>{
    let tempSlug;
   // console.log(this.currentSlug);
    if(this.currentSlug===""){
       tempSlug=localStorage.getItem('product');
    }else{
       tempSlug=this.currentSlug;
    }
    return this.http.get<any>(`${this.baseUrl}products/${tempSlug}/`).pipe(map(data=>{
      console.log("here we have data logged")
      console.log(data)
      this.tempProduct.id=data.product.id
      this.tempProduct.title=data.product.title
      this.tempProduct.description=data.product.description
      this.tempProduct.price=data.stock.price
      this.tempProduct.quantity=data.stock.quantity
      this.tempProduct.slug=data.product.slug
      this.tempProduct.image=data.product.image
      //this.products.push(this.tempProduct);
      return this.tempProduct;
    }));
  }

public  getDetailById(id:number):Observable<any>{

return this.http.get<any>(`${this.baseUrl}products/get_id/${id}/`).pipe(map(data=>{
      console.log("here we have data logged")
      console.log(data)
      this.tempProduct.id=data.product.id
      this.tempProduct.title=data.product.title
      this.tempProduct.description=data.product.description
      this.tempProduct.price=data.stock.price
      this.tempProduct.quantity=data.stock.quantity
      this.tempProduct.slug=data.product.slug
      this.tempProduct.image=data.product.image
      //this.products.push(this.tempProduct);
      console.log("data before becoming promise")
      console.log(this.tempProduct);
      return this.tempProduct;
     
    }));
  }

  // public detailIdPromise(id:number){
  //   let promise = new Promise(resolve => {
     
  //     resolve(this.getDetailById(id));
  //   });
  //   console.log("data after becoming promise")
  //     console.log(promise);
  //     return promise;
  // }

}