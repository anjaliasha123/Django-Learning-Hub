# Generated by Django 5.1.4 on 2024-12-14 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.CharField(default='0', max_length=10),
            preserve_default=False,
        ),
    ]
