from django.db import migrations
from django.conf import settings
from application.migrations import CreatorSchema
from application.models import DB_SCHEMA


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [CreatorSchema(DB_SCHEMA)]
