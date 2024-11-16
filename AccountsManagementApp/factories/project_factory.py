import factory
from faker import Faker
from AccountsManagementApp.models.Project import Project

fake = Faker()


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = factory.Sequence("Project{0}".format)
    description = fake.text()
    start_date = fake.date()
    end_date = fake.date()
    status = factory.Iterator(Project.PROJECT_STATUS, cycle=True)
