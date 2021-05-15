import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { UserService } from 'src/app/features/auth/services/user.service';

@Injectable({
  providedIn: 'root'
})
export class ErrorInterceptorService implements HttpInterceptor {

  constructor(private userService: UserService) { }
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
   
    return next.handle(request).pipe(catchError(err => {
        if ([401, 403].includes(err.status) && this.userService.isAuthenticated()) {
            console.log("here we are in the http interceptor and we have an error")
            this.userService.logout();
        }

        const error = (err && err.error && err.error.message) || err.statusText;
        console.log(err);
        return throwError(error);
    }))
}
}
