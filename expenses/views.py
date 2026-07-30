from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from expenses.models import Category, Expense
from expenses.permissions import IsAdminOrReadOnly
from expenses.serializers import CategorySerializer, ExpenseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)
        if month:
            queryset = queryset.filter(date__month=month)
        if year:
            queryset = queryset.filter(date__year=year)

        summary = queryset.values("category__name").annotate(total=Sum("amount"))
        if summary.count() == 0:
            return Response({"message": "No costs were found for this period."}, status=status.HTTP_200_OK)
        result = [
            {"category": item["category__name"], "total": item["total"]} for item in summary
        ]
        return Response(result)
