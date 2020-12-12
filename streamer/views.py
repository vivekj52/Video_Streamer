import os
import re
import glob
import mimetypes
from wsgiref.util import FileWrapper
import json

from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
local_path_of_videos = '/home/vivek/Videos/HINDI/'


class RangeFileWrapper(object):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.filelike.seek(offset, os.SEEK_SET)
        self.remaining = length
        self.blksize = blksize

    def close(self):
        if hasattr(self.filelike, 'close'):
            self.filelike.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.remaining is None:
            # If remaining is None, we're reading the entire file.
            data = self.filelike.read(self.blksize)
            if data:
                return data
            raise StopIteration()
        else:
            if self.remaining <= 0:
                raise StopIteration()
            data = self.filelike.read(min(self.remaining, self.blksize))
            if not data:
                raise StopIteration()
            self.remaining -= len(data)
            return data


def stream_video(request):
    path = '/home/vivek/Videos/SANAM/Aap Ki Nazron Ne Samjha - Sanam.mp4'
    # path = request.GET['path']
    # if path is None:
        # path = '/home/vivek/Videos/SANAM/Aap Ki Nazron Ne Samjha - Sanam.mp4'
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = range_re.match(range_header)
    size = os.path.getsize(path)
    content_type, encoding = mimetypes.guess_type(path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else size - 1
        if last_byte >= size:
            last_byte = size - 1
        length = last_byte - first_byte + 1
        resp = StreamingHttpResponse(RangeFileWrapper(open(path, 'rb'), offset=first_byte, length=length), status=206, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'

    return resp


@login_required()
def player(request):
    template = loader.get_template('streamer/player.html')
    context = {}
    return HttpResponse(template.render(context, request))


def list_movies(request):

    mp4 = glob.glob(os.path.join(local_path_of_videos, '**/*.mp4'))
    mkv = glob.glob(os.path.join(local_path_of_videos, '**/*.mkv'))

    movies = mp4 + mkv
    response = []

    for movie in movies:
        pair = {'name': movie[movie.rfind('/')+1:movie.rfind('.')],
                'path': movie}
        response.append(pair)

    return HttpResponse(json.dumps(response))

