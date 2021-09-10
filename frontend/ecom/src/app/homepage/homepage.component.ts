import { Component, Input, OnInit } from '@angular/core';
import {UserData} from  'src/app/shared/models/model';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';
import { Observable } from 'rxjs';
import { Breakpoints, BreakpointObserver } from '@angular/cdk/layout';
import { map } from 'rxjs/operators';


declare let $: any;
//declare var require: any
@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.css']
})
export class HomepageComponent implements OnInit {
  public  dict: { [name: string] :  string; } = {}
  

 /** Based on the screen size, switch from standard to one column per row */
 cards = this.breakpointObserver.observe(Breakpoints.Handset).pipe(
  map(({ matches }) => {
    if (matches) {
      return [
        {imageName:'img1', title: 'Welcome', cols: 2, rows: 1 },
        { imageName:'img2',title: 'Card 2', cols: 2, rows: 1 },
        { imageName:'img3',title: 'Contact us', cols: 2, rows: 1 },
        {imageName:'img4', title: 'Our location', cols: 2, rows: 1 }
      ];
    }

    return [
      {imageName:'img1', title: 'Welcome', cols: 2, rows: 1 },
      {imageName:'img2', title: 'Card 2', cols: 1, rows: 1 },
      { imageName:'img3',title: 'Contact us', cols: 1, rows: 2 },
      {imageName:'img4', title: 'Our location', cols: 1, rows: 1 }
    ];
  })
);

  constructor(private breakpointObserver: BreakpointObserver) {
    this.dict["img1"]="http://127.0.0.1:8000/media/products/forest.jpg";
    this.dict["img2"]="http://127.0.0.1:8000/media/products/forest.jpg";
    this.dict["img3"]="http://127.0.0.1:8000/media/products/forest.jpg";
    this.dict["img4"]="http://127.0.0.1:8000/media/products/forest.jpg";
    console.log("here in homepage constructor");
    console.log(this.dict);
    
   }

  ngOnInit(): void {
    
  }
 public getImage(name:string):string{
   console.log("got into get image");
   console.log(this.dict[name]);
   return 'url(' + ( this.dict[name]) + ')';
 }
  

  
  
  
}
