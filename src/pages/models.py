from django.db import models

# FIX 4: Use password encryption
# from django.contrib.auth.hashers import make_password


class Account(models.Model):
    """
    Stores a user's information.
    """
    username = models.TextField()
    password = models.TextField()

    def __str__(self):
        return f"{self.username}: {self.password}"

    # FIX 4: Use password encryption
    # def save(self, *args, **kwargs):
    #     self.password = make_password(self.password)
    #     super(Account, self).save(*args, **kwargs)


class Record(models.Model):
    """
    Stores the a password record for a user.
    Each record contains an account and a password.
    """
    username = models.TextField()
    account = models.TextField()
    password = models.TextField()
