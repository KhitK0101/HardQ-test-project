from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ProductAccess, Lesson, Product
from .serializers import LessonSerializer, ProductStatsSerializer


class LessonListView(APIView):
    def get(self, request):
        products = ProductAccess.objects.filter(
            user=self.request.user
        ).values_list('product', flat=True)
        lessons_query = Lesson.objects.filter(products__in=products)
        serializer = LessonSerializer(
            lessons_query, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProductLessonsView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user_has_access = ProductAccess.objects.filter(
            user=request.user, product=product
        ).exists()

        if not user_has_access:
            return Response(status=status.HTTP_403_FORBIDDEN)

        lessons = Lesson.objects.filter(products=product)
        serializer = LessonSerializer(
            lessons, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProductStatsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductStatsSerializer(products, many=True)
        return Response(serializer.data)
