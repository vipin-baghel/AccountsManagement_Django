from django.db import models
from django.db.models.constraints import CheckConstraint
from django.db.models.expressions import Q
from django.core.exceptions import ValidationError


class Project(models.Model):
    PROJECT_STATUS = [
        ("upcoming", "UPCOMING"),
        ("ongoing", "ONGOING"),
        ("completed", "COMPLETED"),
    ]
    status = models.CharField(max_length=10, choices=PROJECT_STATUS)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} : {self.status}"

    def clean(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date cannot be less than start date")

        if self.status == "completed" and not self.end_date:
            raise ValidationError(
                {"end_date": "End date is required when project status is complete"}
            )

        if self.status != "completed" and self.end_date:
            raise ValidationError(
                {
                    "end_date": "End date should be null when project status is not complete"
                }
            )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(end_date__gte=models.F("start_date")),
                name="end_date_after_start_date",
            )
        ]
