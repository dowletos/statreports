# Generated by Django 4.1.7 on 2023-02-17 13:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='View_UserSet',
            fields=[
                ('rowidn', models.IntegerField(primary_key=True, serialize=False, verbose_name='ROWNUM')),
                ('categoryTitle', models.TextField(max_length=250, verbose_name='Категория')),
                ('subCategoryTitle', models.TextField(max_length=250, verbose_name='Элемент')),
                ('subCategoryLink', models.TextField(max_length=250, verbose_name='Ссылка')),
                ('profileIndexTitle', models.TextField(max_length=250, verbose_name='Профиль')),
                ('username', models.TextField(max_length=250, verbose_name='Пользователь')),
                ('is_active', models.BooleanField(verbose_name='Статус_пользователя')),
                ('flp', models.TextField(max_length=250, verbose_name='ФИО')),
                ('subCategorySort', models.IntegerField(verbose_name='Порядок_сортировки')),
            ],
            options={
                'db_table': 'navigation_menu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='bankbase',
            fields=[
                ('CODE', models.TextField(max_length=250, primary_key=True, serialize=False, verbose_name='CODE')),
                ('bankid_PK', models.IntegerField(verbose_name='bankid_PK')),
                ('ARESTFL', models.IntegerField(verbose_name='ARESTFL')),
                ('LONGNAME', models.IntegerField(verbose_name='LONGNAME')),
                ('BAN_ID', models.IntegerField(verbose_name='BAN_ID')),
                ('BAN_NAME', models.TextField(max_length=250, verbose_name='BAN_NAME')),
                ('HEAD_ID', models.IntegerField(verbose_name='HEAD_ID')),
                ('HEAD_CODE', models.TextField(max_length=250, verbose_name='HEAD_CODE')),
                ('REG_ID', models.IntegerField(verbose_name='REG_ID')),
                ('REG_CODE', models.TextField(max_length=250, verbose_name='REG_CODE')),
                ('REG_NAME', models.TextField(max_length=250, verbose_name='REG_NAME')),
            ],
            options={
                'verbose_name': 'Банк',
                'verbose_name_plural': 'Справочник банков',
                'ordering': ['HEAD_CODE'],
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('categoryID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryTitle', models.CharField(db_index=True, max_length=250, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Справочник категорий',
                'ordering': ['categoryID'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('content', models.TextField(blank=True, verbose_name='Содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('photo', models.ImageField(blank=True, upload_to='uploads/%Y/%m/%d/', verbose_name='Фотография')),
                ('is_published', models.BooleanField(default=False, verbose_name='Опубликовано')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': '1. НОВОСТИ',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='profilesIndex',
            fields=[
                ('profileIndex_PK', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('profileIndexTitle', models.CharField(db_index=True, max_length=250, verbose_name='Наименование Профиля')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Справочник профилей',
                'ordering': ['profileIndex_PK'],
            },
        ),
        migrations.CreateModel(
            name='subCategory',
            fields=[
                ('subCategoryID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('subCategoryTitle', models.CharField(db_index=True, max_length=250, verbose_name='Наименование элемента')),
                ('subCategoryLink', models.TextField(verbose_name='Наименование элемента')),
                ('subCategorySort', models.IntegerField(verbose_name='Порядковый номер в сортировке')),
            ],
            options={
                'verbose_name': 'Элемент категории',
                'verbose_name_plural': 'Справочник элементов ',
                'ordering': ['subCategorySort'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bankid_FK', models.TextField(blank=True, max_length=90)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userRights',
            fields=[
                ('rightID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('profilesIndex_FK', models.ForeignKey(db_column='profilesIndex_FK', on_delete=django.db.models.deletion.PROTECT, to='users.profilesindex', verbose_name='Прикрепленный профиль')),
                ('userID', models.ForeignKey(db_column='userID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Права',
                'verbose_name_plural': '3. ПРАВА ПОЛЬЗОВАТЕЛЕЙ',
                'ordering': ['userID'],
                'unique_together': {('userID', 'profilesIndex_FK')},
            },
        ),
        migrations.CreateModel(
            name='profiles',
            fields=[
                ('profileID', models.BigAutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryID_FK', models.ForeignKey(db_column='categoryID_FK', on_delete=django.db.models.deletion.PROTECT, to='users.category', verbose_name='Категория')),
                ('profileIndex_FK', models.ForeignKey(db_column='profileIndex_FK', on_delete=django.db.models.deletion.PROTECT, to='users.profilesindex', verbose_name='Профиль')),
                ('subCategoryID_FK', models.ForeignKey(db_column='subCategoryID_FK', on_delete=django.db.models.deletion.PROTECT, to='users.subcategory', verbose_name='Элемент категории')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': '2. ПРОФИЛИ',
                'ordering': ['profileID'],
                'unique_together': {('profileIndex_FK', 'categoryID_FK', 'subCategoryID_FK')},
            },
        ),
    ]
