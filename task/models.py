from django.db import models

from accounts.models import CustomUser

class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    dueDate = models.DateField()
    file = models.ImageField(upload_to='taskfiles/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.title
