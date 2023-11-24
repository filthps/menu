import itertools
from django import forms
from django.contrib import admin
from django.db.models import F, Q
from main.models import MenuItem, Menu


class CustomMenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        exclude = ("child_item",)
    parent_item = forms.ChoiceField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent = MenuItem.objects.filter(child_item=self.instance)
        if parent.count():
            self.initial["parent_item"] = (parent[0].pk, parent[0],)
        else:
            self.initial["parent_item"] = ("", "----",)
        self.fields["parent_item"].choices = itertools.chain([("", "----",)],
                                                             map(
                                                                 lambda x: (x.pk, x,), MenuItem.objects.filter(
                                                                     Q(menu_id=self.instance.menu_id) | Q(menu__isnull=True))))

    def clean(self):
        cleaned_data = super().clean()
        parent_item_pk = cleaned_data.get("parent_item", None)
        if not parent_item_pk:
            return super().clean()
        self._check_circular_parent_child_relationship(self.instance, parent_item_pk)
        self._check_self_child_relationship(self.instance, parent_item_pk)
        MenuItem.objects.filter(id=parent_item_pk).update(child_item=self.instance.pk)
        return super().clean()

    def clean_column_index(self):
        index_by_current_level = self.cleaned_data["column_index"]
        if not index_by_current_level:  # default
            last_item = MenuItem.objects.filter(menu_id=self.instance.menu_id).order_by("column_index")
            return last_item.last().column_index if last_item.count() else 0
        if not MenuItem.objects.filter(column_index=index_by_current_level - 1).count():
            raise forms.ValidationError("Указанный индекс слишком велик")
        items_with_highest_co_index = MenuItem.objects.filter(column_index__gte=self.instance.column_index)\
            .order_by("column_index")
        val = items_with_highest_co_index.last().column_index
        if items_with_highest_co_index.count():  # Сместить в право на 1 элементы старше редактируемого
            items_with_highest_co_index.update(column_index=F("column_index") + 1)
        return val

    @staticmethod
    def _check_circular_parent_child_relationship(item, parent_item: str):
        """ Валидация на предмет замыкания: item.child_item = other_item AND other_item.child_item == item """
        if item.pk == parent_item and MenuItem.objects.filter(id=parent_item).child_item == item.pk:
            raise forms.ValidationError("Циклическое замыкание между двумя записами", code="invalid")

    @staticmethod
    def _check_self_child_relationship(item, parent_item: str):
        """ Валидация на предмет замыкания ноды самой на себя: item == item.child_item """
        if item.pk == parent_item:
            raise forms.ValidationError("Замыкание ноды саму на себя", code="invalid")


class ItemsModelAdmin(admin.ModelAdmin):
    form = CustomMenuItemForm
    list_display = ("label", "href", "child_item", "hidden",)


admin.site.register(Menu)
admin.site.register(MenuItem, ItemsModelAdmin)
