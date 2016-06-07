from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0024_auto_20160606_1949'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('code', 'sequence')]),
        ),
    ]
