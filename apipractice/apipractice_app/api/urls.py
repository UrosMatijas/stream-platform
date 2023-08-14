from django.urls import path
from apipractice_app.api.views import video_detail, video_list, stream_platform_list, \
                                        stream_platform_detail, review_detail, single_review_detail

urlpatterns = [
    path('videos/', video_list, name='video_list'),
    path('videos/<int:video_id>/', video_detail, name='video_detail'),
    path('videos/<int:video_id>/reviews/', review_detail, name='review_detail'),
    path('videos/<int:video_id>/reviews/<int:review_id>/', single_review_detail, name='single_review_detail'),
    path('platforms/', stream_platform_list, name='stream_platform_list'),
    path('platforms/<int:platform_id>/', stream_platform_detail, name='stream_platform_detail'),
]