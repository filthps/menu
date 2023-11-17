import itertools
from django.contrib import admin
from django import forms
from main.models import MenuItem, Menu


def get_initial():
    pass


class CustomMenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ("child_item",)

    parent_item = forms.ChoiceField(
        choices=itertools.chain([("", "----",)], map(lambda x: (x.pk, x,), MenuItem.objects.all())),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent = MenuItem.objects.filter(child_item_id=self.instance.id)
        self.initial["parent_item"] = (parent[0].pk, parent[0],) if parent.count() else ("", "----",)

    def clean(self):
        cleaned_data = super().clean()
        parent_item = cleaned_data.get("parent_item", None)
        if parent_item:
            del cleaned_data["parent_item"]
        if not parent_item:
            return super().clean()
        MenuItem.objects.filter(id=parent_item).update(child_item=self.instance.pk)
        return super().clean()


class ItemsModelAdmin(admin.ModelAdmin):
    form = CustomMenuItemForm


admin.site.register(Menu)
admin.site.register(MenuItem, ItemsModelAdmin)
