# Generated by Django 3.1.3 on 2022-02-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchat', '0008_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
    ]
