import factory
from faker import Faker
from datetime import datetime
from ..models.Project import Project

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence("Project{0}".format)

    start_date = fake.date_between(
        start_date=datetime(2023, 1, 1), end_date=datetime(2023, 12, 31)
    )
    status = factory.Iterator(["upcoming", "ongoing", "completed"], cycle=True)
    end_date = factory.LazyAttribute(
        lambda project: (
            fake.date_between(
                start_date=datetime(2024, 1, 1), end_date=datetime.now().date()
            )
            if project.status == "complete"
            else None
        )
    )

    @factory.lazy_attribute
    def description(self):
        return fake.sentence(nb_words=10)
