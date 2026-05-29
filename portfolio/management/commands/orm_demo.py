from traceback import print_tb

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.contrib.auth import get_user_model
from portfolio.models import Project
from django.db.models import Count
User = get_user_model()


class Command(BaseCommand):
    help = "ORM demo: prints example queries and results to console"

    def handle(self, *args, **options):
        self.stdout.write("ORM demo:\n")

        qs = User.objects.filter(is_active=True)
        self.stdout.write("Active users (count=%d):" % qs.count())
        for u in qs[:10]:
            self.stdout.write(" - %s <%s>" % (u.get_username(), u.email))

        q = (Q(title__icontains='Django') | Q(technologies__icontains='Python'))
        projects = Project.objects.filter(q)
        self.stdout.write("\nProjects matching (Django OR Python):")
        self.stdout.write("SQL: %s" % str(projects.query))
        for p in projects[:10]:
            self.stdout.write(" - %s" % p)

        # Aggregations demo using existing models
        self.stdout.write("\nAggregations demo:")
        total_projects = Project.objects.aggregate(total=Count('id'))
        self.stdout.write(f"Total projects: {total_projects}\n")








