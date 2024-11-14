from django.db import models


class Project(models.Model):
    PROJECT_STATUS = [
        ("upcoming", "UPCOMING"),
        ("ongoing", "ONGOING"),
        ("completed", "COMPLETED"),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=PROJECT_STATUS)

    def __str__(self):
        return f"{self.name} : {self.status}"
