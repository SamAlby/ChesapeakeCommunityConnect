# Generated by Django 4.2.6 on 2024-02-04 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_member_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ranking',
            field=models.SmallIntegerField(choices=[(99, 'admin'), (2, 'trusted member'), (98, 'moderator'), (1, 'member')], default=1),
        ),
    ]
