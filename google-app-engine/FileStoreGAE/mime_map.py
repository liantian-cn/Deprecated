#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'Liantian'
# __email__ = "liantian.me+code@gmail.com"
#
# Copyright 2015-2016 liantian
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>

mime2img_map = {
    'application/javascript': 'image/mime/js.png',
    'application/msword': 'image/mime/rtf.png',
    'application/octet-stream': 'image/mime/file.png',
    'application/pdf': 'image/mime/pdf.png',
    'application/postscript': 'image/mime/eps.png',
    'application/vnd.ms-excel': 'image/mime/xls.png',
    'application/vnd.ms-powerpoint': 'image/mime/ppt.png',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'image/mime/xlsx.png',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template': 'image/mime/dotx.png',
    'application/x-bzip2': 'image/mime/zip.png',
    'application/x-gzip': 'image/mime/zip.png',
    'application/x-javascript': 'image/mime/js.png',
    'application/x-kword': 'image/mime/doc.png',
    'application/x-msdownload': 'image/mime/exe.png',
    'application/x-python-code': 'image/mime/py.png',
    'application/x-sh': 'image/mime/file.png',
    'application/x-shockwave-flash': 'image/mime/flv.png',
    'application/x-tar': 'image/mime/zip.png',
    'application/xml': 'image/mime/xml.png',
    'application/zip': 'image/mime/zip.png',
    'audio/midi': 'image/mime/mid.png',
    'audio/mpeg': 'image/mime/mpg.png',
    'audio/vnd.dlna.adts': 'image/mime/aac.png',
    'audio/wav': 'image/mime/wav.png',
    'audio/x-aiff': 'image/mime/aiff.png',
    'audio/x-wav': 'image/mime/wav.png',
    'image/bmp': 'image/mime/bmp.png',
    'image/gif': 'image/mime/gif.png',
    'image/jpeg': 'image/mime/jpeg.png',
    'image/png': 'image/mime/png.png',
    'image/svg+xml': 'image/mime/svg.png',
    'image/tiff': 'image/mime/tiff.png',
    'image/x-ms-bmp': 'image/mime/bmp.png',
    'image/x-rgb': 'image/mime/rb.png',
    'text/css': 'image/mime/css.png',
    'text/csv': 'image/mime/csv.png',
    'text/html': 'image/mime/html.png',
    'text/plain': 'image/mime/txt.png',
    'text/richtext': 'image/mime/rtf.png',
    'text/rtf': 'image/mime/rtf.png',
    'text/x-python': 'image/mime/py.png',
    'text/xml': 'image/mime/xml.png',
    'video/avi': 'image/mime/avi.png',
    'video/mp4': 'image/mime/mp4.png',
    'video/mpeg': 'image/mime/mpg.png',
    'video/quicktime': 'image/mime/qt.png',
    'video/x-flv': 'image/mime/flv.png',
    'video/x-msvideo': 'image/mime/avi.png'
}
