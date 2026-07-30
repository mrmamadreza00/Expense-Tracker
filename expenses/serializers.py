from rest_framework import serializers

from expenses.models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Expense
        fields = ["id", "category", "category_name", "user", "username", "amount", "date", "description"]
        read_only_fields = ["user"]

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return amount
    
