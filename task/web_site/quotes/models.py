from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=30, null=False, unique=True)
    born_date = models.DateField(null=False)
    born_location = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    tags = models.JSONField(default=list, null=False)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    quote = models.TextField(null=False)

    def __str__(self):
        return self.quote
