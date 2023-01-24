from rest_framework import serializers

from apps.blog.models import Category, Blog, Comment


# Create your serializers here.


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ("id", "title", "slug", "body", "posted", "category", "enabled", "comment")
