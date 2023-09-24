from django.db.models import Sum
from rest_framework import serializers
from .models import Lesson, UserLesson, Product, ProductAccess


class LessonSerializer(serializers.ModelSerializer):
    is_watched = serializers.SerializerMethodField()
    duration_watched = serializers.SerializerMethodField()
    last_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('title',
                  'video_url',
                  'duration',
                  'is_watched',
                  'duration_watched')

    def get_is_watched(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(user=user, lesson=obj).first()
        return user_lesson.is_watched if user_lesson else False

    def get_duration_watched(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(user=user, lesson=obj).first()
        return user_lesson.duration_watched if user_lesson else 0

    def get_last_viewed(self, obj):
        user = self.context['request'].user
        user_lesson = UserLesson.objects.filter(user=user, lesson=obj).first()
        return user_lesson.last_viewed if user_lesson else None


class ProductStatsSerializer(serializers.ModelSerializer):
    total_watched_lessons = serializers.SerializerMethodField()
    total_time_watched = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'total_watched_lessons',
                  'total_time_watched',
                  'total_users',
                  'purchase_percentage']

    def get_total_watched_lessons(self, obj):
        return UserLesson.objects.filter(lesson__products=obj).count()

    def get_total_time_watched(self, obj):
        total_time = UserLesson.objects.filter(
            lesson__products=obj
        ).aggregate(total_duration=Sum('duration_watched'))
        return total_time['total_duration']

    def get_total_users(self, obj):
        return ProductAccess.objects.filter(product=obj).count()

    def get_purchase_percentage(self, obj):
        total_users = Product.objects.count()
        total_product_access = ProductAccess.objects.filter(
            product=obj
        ).count()
        return (
            total_product_access / total_users
        ) * 100 if total_users > 0 else 0
