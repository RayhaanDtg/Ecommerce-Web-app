import { Injectable } from '@angular/core';
import { Cart } from 'src/app/shared/models/model';
import { Product } from 'src/app/shared/models/model';
import { CartItem } from 'src/app/shared/models/model';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { UserService } from 'src/app/features/auth/services/user.service';
import { UserData } from 'src/app/shared/models/model';
import { ProductApiService } from 'src/app/features/products/services/product.api.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  public cart: Cart;
  public cartItems: CartItem[];
  baseUrl = `http://127.0.0.1:8000/Cart/`;
  public user: UserData;
  public tempProduct: Product;
  public tempItem: CartItem;
 
  constructor(private http: HttpClient, private authenticationService: UserService, private productApiService: ProductApiService) {
    this.cart = {
      id: 0,
      total: 0,
      isActive: false,
      user: 0

    };

    this.cartItems = [];
    this.user = this.authenticationService.user;
    this.tempProduct = {

      id: 0,
      title: '',
      description: '',
      price: 0,
      quantity: 0,
      slug: '',
      image: ''

    }
  
    this.tempItem = {
      id: 0,
      isActive: false,
      product: {
        id: 0,
        title: '',
        description: '',
        price: 0,
        quantity: 0,
        slug: '',
        image: ''
      },
      subtotal: 0,
      qty: 0,
      cart: 0

    }
    
  }
  public isAuth(): Boolean {

    return (this.authenticationService.isAuthenticated() && this.authenticationService.validateRefresh());
  }
  public getCart(email: string): Observable<any> {


    let parameter = new HttpParams().set("email", email)

    return this.http.get<any>(`${this.baseUrl}`, { params: parameter }).pipe(map(data => {
      this.cartItems = [];


      this.cartSetter(data['cart']);


      for (let i = 0; i < data['cart_items_list'].length; i++) {
       
        for (let j = 0; j < data['product_items_list'].length; j++) {


          if (data['product_items_list'][j]['product_item'].id === data['cart_items_list'][i]['cart_item'].product) {
         
            this.cartItems.push(this.cartItemSetter(data['cart_items_list'][i]['cart_item'], data['product_items_list'][j]['product_item']));
          }
        }


      }

   

      return this.cartItems;
    }
    ))
  }
  public modifyCart(email: string, qty: number, slug: string): Observable<any> {
   
    return this.http.post<any>(`${this.baseUrl}modify/`, { email, qty, slug }).pipe(map(data => {
      this.cartItems = [];

      this.cartSetter(data['cart']);


      for (let i = 0; i < data['cart_items_list'].length; i++) {

        for (let j = 0; j < data['product_items_list'].length; j++) {


          if (data['product_items_list'][j]['product_item'].id === data['cart_items_list'][i]['cart_item'].product) {

            this.cartItems.push(this.cartItemSetter(data['cart_items_list'][i]['cart_item'], data['product_items_list'][j]['product_item']));
          }
        }


      }




      return this.cartItems;

    }))
  }

  public cartDelete(cart_item:number,cart:number):Observable<any>{
    
    return this.http.post<any>(`${this.baseUrl}delete/`, { cart,cart_item }).pipe(map(data => {
      this.cartItems = [];

      this.cartSetter(data['cart']);


      for (let i = 0; i < data['cart_items_list'].length; i++) {

        for (let j = 0; j < data['product_items_list'].length; j++) {


          if (data['product_items_list'][j]['product_item'].id === data['cart_items_list'][i]['cart_item'].product) {

            this.cartItems.push(this.cartItemSetter(data['cart_items_list'][i]['cart_item'], data['product_items_list'][j]['product_item']));
          }
        }


      }




      return this.cartItems;

    }))
    
  }
  // takes in an object of type any, more likely data from an http response, and stores it in the cart object of this service.
  public cartSetter(cart: any) {
    this.cart.id = cart.id
    this.cart.user = cart.user
    this.cart.isActive = cart.isActive
    this.cart.total = cart.total

  }
  // takes in an object of type any, more likely data from an http response, and stores it in a temporary cart item object.
  //it then adds the temp cart item to the list of cart items object of this service
  public cartItemSetter(cartItem: any, productItem: any): CartItem {
    let tempItem: CartItem = {
      id: 0,
      isActive: false,
      product: {
        id: 0,
        title: '',
        description: '',
        price: 0,
        quantity: 0,
        slug: '',
        image: ''
      },
      subtotal: 0,
      qty: 0,
      cart: 0
    }

    tempItem.id = cartItem.id
    tempItem.isActive = cartItem.isActive
    tempItem.cart = cartItem.cart
    tempItem.product = {
      id: productItem.id,
      title: productItem.title,
      description: productItem.description,
      price: 0,
      quantity: 0,
      slug: productItem.slug,
      image: productItem.image
    }

    // console.log(this.tempProduct)
    tempItem.qty = cartItem.qty
    tempItem.subtotal = cartItem.subtotal





    return tempItem;
  }
  
}
