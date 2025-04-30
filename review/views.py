from drf_spectacular.utils import OpenApiExample
from rest_framework import generics
from .serializers import ProductReviewSerializer
from .models import ProductReview
from drf_spectacular.views import extend_schema

class ProductReviewList(generics.ListCreateAPIView):
    """ """
    serializer_class = ProductReviewSerializer
    queryset = ProductReview.objects.all()

    @extend_schema(
        tags=["Reviews"],
        summary="List all products reviews",
        description="Returns a list of all products reviews in the system.",
        responses={200: ProductReviewSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        tags=["Reviews"],
        summary="Create a new products review",
        description="Allows an authenticated user to submit a review for a products.",
        request=ProductReviewSerializer,
        responses={201: ProductReviewSerializer},
        examples=[
            OpenApiExample(
                "Sample Review",
                value={
                    "products": 1,
                    "rating": 4,
                    "comment": "Really good quality!",
                },
                request_only=True,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """ """
    @extend_schema(
        summary="Retrieve a specific products review",
        description="Get the details of a single products review by its ID.",
        responses={200: ProductReviewSerializer},
        tags=["Reviews"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Reviews"],
        summary="Update a products review",
        description="Fully update a products review using its ID.",
        request=ProductReviewSerializer,
        responses={200: ProductReviewSerializer},
        examples=[
            OpenApiExample(
                "Full Review Update",
                value={
                    "products": 1,
                    "rating": 5,
                    "comment": "Updated review comment here."
                },
                request_only=True,
            )
        ],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=["Reviews"],
        summary="Partially update a products review",
        description="Update one or more fields of a products review (e.g., just the rating or comment).",
        request=ProductReviewSerializer,
        responses={200: ProductReviewSerializer},
        examples=[
            OpenApiExample(
                "Partial Review Update",
                value={
                    "rating": 3
                },
                request_only=True,
            )
        ],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        tags=["Reviews"],
        summary="Delete a products review",
        description="Delete a products review by its ID.",
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
