from apipractice_app.api.serializers import VideoSerializer, StreamPlatformSerializer, ReviewSerializer
from apipractice_app.models import Video, StreamPlatform, Review
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def video_list(request):

    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'PUT', 'DELETE'])
def video_detail(request, video_id):

    if request.method == 'GET':
        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VideoSerializer(video)
        return Response(serializer.data)

    elif request.method == 'PUT':
        video = Video.objects.get(id=video_id)
        serializer = VideoSerializer(video, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        video = Video.objects.get(id=video_id)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def stream_platform_list(request):
    if request.method == 'GET':
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, context={'request': request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stream_platform_detail(request, platform_id):

    if request.method == 'GET':
        try:
            platform = StreamPlatform.objects.get(id=platform_id)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    elif request.method == 'PUT':
        platform = StreamPlatform.objects.get(id=platform_id)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        platform = StreamPlatform.objects.get(id=platform_id)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def review_detail(request, video_id):
    if request.method == 'GET':
        video = Video.objects.get(id=video_id)
        reviews = video.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        review_user = request.user
        existing_reviews = Review.objects.filter(review_user=review_user)

        if existing_reviews.exists():
            return Response({"error": "User already reviewed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(review_user=review_user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'PUT', 'DELETE'])
def single_review_detail(request, video_id, review_id):
    if request.method == 'GET':
        video = Video.objects.get(id=video_id)
        reviews = video.reviews.all()
        review = reviews.get(id=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        review = Review.objects.get(id=review_id)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        video = Video.objects.get(id=video_id)
        review_user = request.user

        try:
            review = Review.objects.get(video=video, review_user=review_user)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        if review.review_user != request.user:
            return Response({"error": "Unauthorized to update this review"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            video.update_avg_rating()
            video.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








