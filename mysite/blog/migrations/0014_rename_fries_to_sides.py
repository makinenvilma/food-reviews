from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0013_remove_blogpage_body"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpage",
            old_name="fries",
            new_name="sides",
        ),
    ]
