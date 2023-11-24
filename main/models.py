from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=10, blank=False, unique=True)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    label = models.CharField(max_length=100, blank=False, unique=True)
    column_index = models.SmallIntegerField(default=0, db_index=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, to_field="name", blank=True, null=True)
    child_item = models.ForeignKey("self", on_delete=models.CASCADE, null=True, default=None, blank=True)
    hidden = models.BooleanField(blank=False, default=True)
    href = models.URLField(unique=True)

    def __str__(self):
        return f"{self.label} ({self.href})"
