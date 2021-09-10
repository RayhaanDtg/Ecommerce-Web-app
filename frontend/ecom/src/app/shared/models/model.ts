export interface Product {
    id: number;
    title: string;
    description: string;
    price:number;
    quantity:number;    
    slug:string;
    image:string;
    //inStock?: boolean;
}

export interface Cart{
    id:number;
    total:number;
    isActive:boolean;
    user:number;
}
export interface CartItem{
    id:number;
    subtotal:number;
    qty:number;
    isActive:boolean;
    product:Product;
    cart:number;

}

export interface Stock{
    id:number;
    price:number;
    quantity:number;
    active:boolean;
    product:number;
}
// export class Cart{
//     id:number;
//     total:number;
//     products:Product[];
//     constructor(id:number,total:number, products:Product[]){
//         this.id=id;
//         this.total=total;
//         this.products=products;

//     }

// }
export interface UserData {
   
    email: string ;
  first_name: string ;
  last_name: string ;
  password:string;
 
  userId:number;
	// constructor(
	// public email: string,
    // public firstname: string,
    // public lastname:string
	// ){}
}
export interface Address{
    address_line_1:string;
    address_line_2:string;
    city:string;
    state:string;
    phone_number:number;
    billing_profile:number;
    id:number;
}
export interface Payment{
    method:string;
    card_name:string;
    card_number:number;
    expMonth:number;
    expYear:number
}
// export interface User{
//     username: string;
//     firstname:string;
//     lastname:string;
// }

// export class Product{
//     id: number;
//     title: string;
//     description: string;
//     price: number;
//     slug:string;
//     existInCart?: boolean;

//     constructor( id: number,title: string,description: string,price: number, slug:string,existInCart?: boolean){
//         this.id=id;
//         this.title=title;
//         this.description=description;
//         this.price=price;
//         this.slug=slug;
//         this.existInCart=existInCart;
//     }
// }