from django.db import models

class DataLoadLog(models.Model):
    model = models.CharField(max_length=100, null=False, blank=False)
    success = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=255, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(auto_now=True)
    n_records = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'data_load_logs'
        ordering = ['-started_at']