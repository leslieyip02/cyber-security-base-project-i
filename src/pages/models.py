from django.db import models


class Account(models.Model):
    """
    Stores a user's information.
    """
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.password}"


class Record(models.Model):
    """
    Stores the a password record for a user.
    Each record contains an account and a password.
    """
    username = models.TextField()
    account = models.TextField()
    password = models.TextField()
