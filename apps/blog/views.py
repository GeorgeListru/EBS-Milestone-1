from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.blog.models import Category, Blog, Comment
from apps.blog.serializers import CategorySerializer, BlogSerializer, CommentSerializer
from apps.common.permissions import ReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BlogListView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly,)

    def get(self, request):
        blogs = Blog.objects.all()
        serialized_blogs = BlogSerializer(blogs, many=True)
        for blog in serialized_blogs.data:
            blog["comments"] = CommentSerializer(Comment.objects.filter(blog=blog["id"]), many=True).data
        return Response(serialized_blogs.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogItemView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly, IsAuthenticated)

    def get(self, request, pk):
        blog = get_object_or_404(Blog.objects.filter(pk=pk))
        serialized_blog = BlogSerializer(blog)
        comments = Comment.objects.filter(blog=blog)
        serialized_comments = CommentSerializer(comments, many=True)
        return Response({"blog": serialized_blog.data, "comments": serialized_comments.data})


class CommentCreateView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog.objects.filter(pk=request.data.get("blog")))
        if request.data.get("text"):
            comment = Comment.objects.create(text=request.data.get("text"), blog=blog)
            return Response(CommentSerializer(comment).data)
        return Response({"error": "text is required"}, status=400)
