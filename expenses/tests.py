from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from expenses.models import Expense, Category


class ExpensesTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="ali", password="1234")
        self.user2 = User.objects.create_user(username="sara", password="1234")
        self.admin = User.objects.create_user(username="admin", password="1234", is_staff=True)
        self.category_food = Category.objects.create(name="Food")
        self.category_transport = Category.objects.create(name="Transport")

    def test_user_can_create_expense(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "category": self.category_food.id,
            "amount": 100,
            "description": "descriptionOne",
            "date": "2026-07-13"
        }
        response = self.client.post("/api/expenses/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_see_others_expenses(self):
        # Arrange For Test(create tow expenses by ORM)
        Expense.objects.create(
            user=self.user1, category=self.category_food, amount=100, date="2026-07-13"
        )
        Expense.objects.create(
            user=self.user2, category=self.category_food, amount=200, date="2026-07-13"
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/expenses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_create_expense_with_negative_amount(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "category": self.category_food.id,
            "amount": -100,
            "description": "descriptionOne",
            "date": "2026-07-13"
        }
        response = self.client.post("/api/expenses/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_summary_groups_by_category(self):
        self.client.force_authenticate(user=self.user1)
        Expense.objects.create(
            user=self.user1, category=self.category_food, amount=100, date="2026-07-13"
        )
        Expense.objects.create(
            user=self.user1, category=self.category_food, amount=200, date="2026-07-15"
        )
        Expense.objects.create(
            user=self.user1, category=self.category_transport, amount=500, date="2026-07-14"
        )
        response = self.client.get("/api/expenses/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        food_summary = next(item for item in response.data if item["category"] == "Food")
        self.assertEqual(float(food_summary["total"]), 300)

    def test_non_admin_cannot_create_category(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "Other",
        }
        response = self.client.post("/api/categories/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
