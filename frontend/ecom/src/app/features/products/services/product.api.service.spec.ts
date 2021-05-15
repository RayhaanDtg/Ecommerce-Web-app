import { TestBed } from '@angular/core/testing';

import { Product.ApiService } from './product.api.service';

describe('Product.ApiService', () => {
  let service: Product.ApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Product.ApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
