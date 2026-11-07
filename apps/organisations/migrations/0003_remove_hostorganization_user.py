from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_hostorganisation_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostorganization',
            name='user',
        ),
    ]