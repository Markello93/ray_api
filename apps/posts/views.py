# import aiofiles
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
# from .forms import UploadFileForm
#
# async def handle_uploaded_file(f):
#     async with aiofiles.open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             await destination.write(chunk)
#
# async def async_uploader(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             await handle_uploaded_file(request.FILES["file"])
#             return HttpResponseRedirect("/")
#     else:
#         form = UploadFileForm()
#     return render(request, "upload.html", {"form": form})
from rest_framework import viewsets

from apps.posts.models import Post
from apps.posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для товаров."""

    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer

    # @action(detail=False)
    # def popular(self, request, top=6):
    #     """Возвращает топ популярных товаров."""
    #     popular_products = (
    #         Product.objects.annotate(total_quantity=Sum('order_products__quantity'))
    #         .filter(total_quantity__gt=0)
    #         .order_by('-total_quantity')[:top]
    #     )
    #     serializer = ShortProductSerializer(popular_products, many=True, context={'request': request})
    #     return Response(serializer.data)



#
# class ReviewViewSet(viewsets.ModelViewSet):
#     permission_classes = (AdminModeratorAuthorOrReadOnly,)
#     serializer_class = ReviewSerializer
#     pagination_class = LimitOffsetPagination
#
#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
#         serializer.save(author=self.request.user, title=title)
#
#     def get_queryset(self):
#         title_id = self.kwargs.get("title_id")
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (AdminModeratorAuthorOrReadOnly,)
#
#     def get_queryset(self):
#         review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
#         return review.comments.all()
#
#     def perform_create(self, serializer):
#         review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
#         serializer.save(author=self.request.user, review=review)
#
#
# async def test_view(request,cars,):
