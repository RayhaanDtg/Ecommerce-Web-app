
import { UserService } from 'src/app/features/auth/services/user.service'
import { CartService } from 'src/app/features/cart/cart.service';

export function appInitializer(authenticationService: UserService,cartService:CartService) {
    return () => new Promise(resolve => {
      
        authenticationService.refreshTokenFunction()
            .subscribe().add(resolve);
            
        
      
      

    }
    
    );
}