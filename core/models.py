from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Baby(models.Model):
    class Meta:
        #ordering = ('name',)
        verbose_name_plural = 'Babies'
    
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    birth_weight = models.DecimalField(decimal_places=3, max_digits=5)
    birth_length = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(75)])
    current_percentile = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    current_weight = models.DecimalField(decimal_places=3, max_digits=5, null=True, blank=True)
    age_in_months = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(60)], null=True, blank=True)
    
    def __str__(self):
        return self.name

class Record(models.Model):
    class Meta:
        ordering = ('-date',)
        pass
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(decimal_places=3, max_digits=5)
    length = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)], null=True, blank=True)
    percentile = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    