from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'ordering': ['service'], 'verbose_name': 'Аккаунт', 'verbose_name_plural': 'Аккаунты'},
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.TextField(),
        ),
    ]