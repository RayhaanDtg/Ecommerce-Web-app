from django.db import models
from products.models import Product




class StockQuerySet(models.QuerySet):
  def get_by_product(self,product):
    qs=self.filter(product=product,active=True)
    return qs




class StockManager(models.Manager):
  def get_queryset(self):
    return StockQuerySet(self.model,self._db)
  
  def get_by_product(self,product):
    qs=self.get_queryset().get_by_product(product=product)
    if qs.count() >= 1:
      instance=qs.first()
    else:
      instance=None
    return instance
       
  


  




class Stock(models.Model):
  price = models.DecimalField(max_digits=20, default=0.00, decimal_places=2)
  quantity=models.IntegerField(default=0)
  active=models.BooleanField(default=True)
  period=models.DateTimeField(auto_now=True)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  objects=StockManager()

  def __str__(self):
    return self.product.title
  
  # @property
  # def price(self):
  #   return self.price
    


