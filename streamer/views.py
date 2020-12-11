# from django.http import HttpResponse
# from django.http import StreamingHttpResponse
# import time
# import os
#
#
# # Create your views here.
# def index(request):
#     # return HttpResponse("Hello, world. You're at the stream index.")
#     file = open('/home/vivek/Videos/SANAM/Aap Ki Nazron Ne Samjha - Sanam.mp4', "rb")
#     return StreamingHttpResponse(streaming_content=file, content_type='video/mp4')
#
#
# def stream_response_generator():
#     yield "<html><body>\n"
#     for x in range(1,11):
#         yield "<div>%s</div>\n" % x
#         yield " " * 1024  # Encourage browser to render incrementally
#         time.sleep(1)
#         yield "</body></html>\n"
#
#
# def read(chunksize=819200):
#     with open('/home/vivek/Videos/SANAM/Aap Ki Nazron Ne Samjha - Sanam.mp4', "rb") as video_file:
#         byte = video_file.read(chunksize)
#         while byte:
#             yield byte
#             time.sleep(1)
import os
import re
import mimetypes
from wsgiref.util import FileWrapper

from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
from django.template import loader


range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)


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


def stream_video(request, path='/home/vivek/Videos/SANAM/Aap Ki Nazron Ne Samjha - Sanam.mp4'):
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


def player(request):
    template = loader.get_template('streamer/player.html')
    context = {}
    return HttpResponse(template.render(context, request))
