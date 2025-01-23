from django.db import models

class Airport(models.Model):
    iata = models.CharField(max_length=3, unique=True)  
    city = models.CharField(max_length=100) 
    lat = models.DecimalField(max_digits=9, decimal_places=6)  
    lon = models.DecimalField(max_digits=9, decimal_places=6) 
    state = models.CharField(max_length=2) 

    def __str__(self):
        return f"{self.iata}) - {self.city}"
    
    class Meta:
        db_table = 'aiports'
    