from __future__ import unicode_literals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0022_auto_20160603_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True),
        )
    ]
