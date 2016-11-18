from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
# from bootcamp.videos.forms import VideoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string

from .models import Video, Tag, VideoComment

from serializers import CommentSerializer


def videos(request):
    all_videos = Video.get_published()
    return _videos(request, all_videos)


def _videos(request, videos):
    paginator = Paginator(videos, 12)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    popular_tags = Tag.get_popular_tags()
    return render(request, 'videos/videos.html', {
        'videos': videos,
        'popular_tags': popular_tags
    })


def video(request, slug):
    video = get_object_or_404(Video, slug=slug, status=Video.PUBLISHED)
    return render(request, 'videos/video.html', {'video': video})


def tag(request, tag_name):
    tags = Tag.objects.filter(tag=tag_name)
    videos = []
    for tag in tags:
        if tag.video.status == Video.PUBLISHED:
            videos.append(tag.video)
    return _videos(request, videos)


# @login_required
# def write(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST)
#         if form.is_valid():
#             video = Video()
#             video.create_user = request.user
#             video.title = form.cleaned_data.get('title')
#             video.content = form.cleaned_data.get('content')
#             status = form.cleaned_data.get('status')
#             if status in [Video.PUBLISHED, Video.DRAFT]:
#                 video.status = form.cleaned_data.get('status')
#             video.save()
#             tags = form.cleaned_data.get('tags')
#             video.create_tags(tags)
#             return redirect('/videos/')
#     else:
#         form = VideoForm()
#     return render(request, 'videos/write.html', {'form': form})
#
#
# @login_required
# def drafts(request):
#     drafts = Video.objects.filter(create_user=request.user,
#                                   status=Video.DRAFT)
#     return render(request, 'videos/drafts.html', {'drafts': drafts})
#
#
# @login_required
# def edit(request, id):
#     tags = ''
#     if id:
#         video = get_object_or_404(Video, pk=id)
#         for tag in video.get_tags():
#             tags = u'{0} {1}'.format(tags, tag.tag)
#         tags = tags.strip()
#     else:
#         video = Video(create_user=request.user)
#
#     if video.create_user.id != request.user.id:
#         return redirect('home')
#
#     if request.POST:
#         form = VideoForm(request.POST, instance=video)
#         if form.is_valid():
#             form.save()
#             return redirect('/videos/')
#     else:
#         form = VideoForm(instance=video, initial={'tags': tags})
#     return render(request, 'videos/edit.html', {'form': form})
#
#
# @login_required
# def preview(request):
#     try:
#         if request.method == 'POST':
#             content = request.POST.get('content')
#             html = 'Nothing to display :('
#             if len(content.strip()) > 0:
#                 # html = markdown.markdown(content, safe_mode='escape')
#                 html = content
#             return HttpResponse(html)
#         else:
#             return HttpResponseBadRequest()
#
#     except Exception, e:
#         return HttpResponseBadRequest()
#

# class CommentViewSet(viewsets.ModelViewSet):
#     # queryset = Comment.objects.filter(parent=None) # Don't
#     queryset = Comment.objects.all()
#
#     serializer_class = CommentSerializer
#
#     @list_route()
#     def roots(self, request):
#         queryset = Comment.objects.filter(parent=None)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class CommentDetailAPIView(RetrieveAPIView):
#     queryset = VideoComment.objects.all()
#     serializer_class = CommentSerializer

@login_required
def comment(request):
    try:
        if request.method == 'POST':
            video_id = request.POST.get('video')
            video = Video.objects.get(pk=video_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                video_comment = VideoComment(user=request.user,
                                             video=video,
                                             comment=comment)
                video_comment.save()
            html = u''
            for comment in video.get_comments():
                html = u'{0}{1}'.format(html, render_to_string('videos/partial_video_comment.html',
                                        {'comment': {comment}}))
            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception, e:
        return HttpResponseBadRequest()
