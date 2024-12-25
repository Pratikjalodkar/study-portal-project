from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()


# to remove the plural 's' from the model name in the admin panel
    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'
        
    def __str__(self):
        return self.title
    
class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due = models.DateField()
    is_finished = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homework'
        
    def __str__(self):
        return self.title
    


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    # description = models.TextField()
    is_finished = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'
        
    def __str__(self):
        return self.title


