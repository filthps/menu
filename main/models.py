from django.db import models
from django.db.models import F


class Menu(models.Model):
    name = models.CharField(max_length=10, blank=False, unique=True, db_index=True)


class MenuItem(models.Model):
    inner_text = models.CharField(max_length=100, blank=False)
    level_index = models.SmallIntegerField(default=0, db_index=True)
    column_index = models.SmallIntegerField(default=0, db_index=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field="name")
    parent_item = models.ForeignKey("self", on_delete=models.CASCADE, null=True, default=None, blank=True)
    hidden = models.BooleanField(blank=False, default=False)
    href = models.URLField()
