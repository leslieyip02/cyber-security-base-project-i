from django.db import models


class Account(models.Model):
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.password}"
