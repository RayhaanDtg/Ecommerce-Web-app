import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductListComponent } from './features/products/product-list/product-list.component';
import { HomepageComponent } from 'src/app/homepage/homepage.component';
//import { NavbarComponent } from './features/navbar/navbar.component';
import{ProductDetailComponent} from './features/products/product-detail/product-detail/product-detail.component';
import{AppComponent} from 'src/app/app.component'
import {RegisterComponent} from 'src/app/features/auth/register/register.component' ;
import {LoginComponent} from 'src/app/features/auth/login/login/login.component';
import {CartComponent} from 'src/app/features/cart/cart/cart.component';
//import { SidenavComponent } from './features/sidenav/sidenav/sidenav.component'
import{AuthguardService} from 'src/app/shared/helpers/authguard.service'
import { AccountComponent } from './features/account/account/account.component'




const routes: Routes = [
  {
    path: "",
    component: HomepageComponent,
  },
  {
    path: "product-list",
    component: ProductListComponent,
    canActivate: [AuthguardService] 
  },
  {
    path: "product-detail",
    component: ProductDetailComponent,
  },
  {
    path: "register",
    component: RegisterComponent,
  },
  {
    path: "login",
    component: LoginComponent,
  },
  {
    path: "cart",
    component: CartComponent,
  },
  {
    path:"account",
    component: AccountComponent,
  },

];
const appRoutes: Routes = [
  {
    path: "",
    component: HomepageComponent,
  },
  {
    path: "product-list",
    component: ProductListComponent,
    canActivate: [AuthguardService] 
  },
  {
    path: "product-detail",
    component: ProductDetailComponent,
  },
  {
    path: "login",
    component: LoginComponent,
  },
  {
    path: "register",
    component: RegisterComponent,
  },
  {
    path:"account",
    component: AccountComponent,
  },
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
