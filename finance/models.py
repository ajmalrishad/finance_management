from django.db import models

class Transaction(models.Model):
    transaction_particulars = models.TextField()
    branch_name = models.TextField()
    file_name = models.TextField()

    def __str__(self):
        return self.branch_name

