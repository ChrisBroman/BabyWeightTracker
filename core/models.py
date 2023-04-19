from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Baby(models.Model):
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Babies'
    
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    birth_weight = models.IntegerField(validators=[MinValueValidator(2500), MaxValueValidator(5000)])
    birth_length = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(75)])
    current_percentile = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    
    def __str__(self):
        return self.name

class Record(models.Model):
    class Meta:
        ordering = ('-date')
    
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.IntegerField(validators=[MinValueValidator(2500), MaxValueValidator(5000)])
    length = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    z_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    percentile = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    