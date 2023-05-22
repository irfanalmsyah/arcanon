from .models import Report
from chat.models import Room
from forum.models import Post, Comment
from django.views import View
from django.http import JsonResponse


class ReportView(View):
    def post(self, request):
        reportee = request.user
        type = request.POST.get('type')
        id = request.POST.get('id')
        reason = request.POST.get('reason')
        room = None
        post = None
        comment = None
        if type == 'room':
            room = Room.objects.get(name=id)
        elif type == 'post':
            post = Post.objects.get(id=id)
        elif type == 'comment':
            comment = Comment.objects.get(id=id)
        report = Report(
            reportee=reportee,
            room=room,
            post=post,
            comment=comment,
            reason=reason
        )
        report.save()
        return JsonResponse({'status': 'success'})
