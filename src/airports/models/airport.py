from django.db import models

class Airport(models.Model):
    iata = models.CharField(max_length=3, unique=True, blank=False, null=False)  
    city = models.CharField(max_length=100, blank=False, null=False) 
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=False, null=False) 
    state = models.CharField(max_length=2, blank=False, null=False) 
    log = models.ForeignKey('logs.DataLoadLog', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.iata} - {self.city}"
    
    class Meta:
        db_table = 'aiports'
    