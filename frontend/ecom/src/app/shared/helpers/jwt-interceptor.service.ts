import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserService } from 'src/app/features/auth/services/user.service';


@Injectable({
  providedIn: 'root'
})
export class JwtInterceptorService {

  constructor(private userService: UserService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add auth header with jwt if user is logged in and request is to the api url
   
    const isAuth = this.userService.isAuthenticated();
    
    const hasRefresh = this.userService.validateRefresh();
  
    const isApiUrl = request.url.startsWith(`http://127.0.0.1:8000/`);
    if ( isAuth && hasRefresh) {
        request = request.clone({
            setHeaders: { Authorization: `Bearer ${this.userService.accessToken}` }
        });
       
    }else{
      if(hasRefresh===true && isAuth===false){
        this.userService.refreshTokenFunction();
        request = request.clone({
          setHeaders: { Authorization: `Bearer ${this.userService.accessToken}` }
      });
      }
    }


    return next.handle(request);
}
}
