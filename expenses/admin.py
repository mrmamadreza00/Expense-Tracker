from django.contrib import admin
from django.contrib.admin import ModelAdmin

from expenses.models import Expense, Category


# Register your models here.


@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass
