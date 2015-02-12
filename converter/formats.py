#!/usr/bin/env python


class BaseFormat(object):
    """
    Base format class.

    Supported formats are: ogg, avi, mkv, webm, flv, mov, mp4, mpeg, segment
    """

    format_name = None
    ffmpeg_format_name = None

    def parse_options(self, opt):
        if 'format' not in opt or opt.get('format') != self.format_name:
            raise ValueError('invalid Format format')
        return ['-f', self.ffmpeg_format_name]


class OggFormat(BaseFormat):
    """
    Ogg container format, mostly used with Vorbis and Theora.
    """
    format_name = 'ogg'
    ffmpeg_format_name = 'ogg'


class AviFormat(BaseFormat):
    """
    Avi container format, often used vith DivX video.
    """
    format_name = 'avi'
    ffmpeg_format_name = 'avi'


class MkvFormat(BaseFormat):
    """
    Matroska format, often used with H.264 video.
    """
    format_name = 'mkv'
    ffmpeg_format_name = 'matroska'


class WebmFormat(BaseFormat):
    """
    WebM is Google's variant of Matroska containing only
    VP8 for video and Vorbis for audio content.
    """
    format_name = 'webm'
    ffmpeg_format_name = 'webm'


class FlvFormat(BaseFormat):
    """
    Flash Video container format.
    """
    format_name = 'flv'
    ffmpeg_format_name = 'flv'


class MovFormat(BaseFormat):
    """
    Mov container format, used mostly with H.264 video
    content, often for mobile platforms.
    """
    format_name = 'mov'
    ffmpeg_format_name = 'mov'


class Mp4Format(BaseFormat):
    """
    Mp4 container format, the default Format for H.264
    video content.
    """
    format_name = 'mp4'
    ffmpeg_format_name = 'mp4'


class MpegFormat(BaseFormat):
    """
    MPEG(TS) container, used mainly for MPEG 1/2 video codecs.
    """
    format_name = 'mpg'
    ffmpeg_format_name = 'mpegts'


class Mp3Format(BaseFormat):
    """
    Mp3 container, used audio-only mp3 files
    """
    format_name = 'mp3'
    ffmpeg_format_name = 'mp3'

class SegmentFormat(BaseFormat):
    """
    TS segment format
    """
    format_name = 'segment'
    ffmpeg_format_name = 'segment'
    format_options = {
        'time': int,
        'list_size': int,
        'list_type': str,
        'list_file': str,
        'format': str
    }
    
    def safe_options(self, opts):
        safe = {}
        # Only copy options that are expected and of correct type
        # (and do typecasting on them)
        for k, v in opts.items():
            if k in self.format_options:
                typ = self.format_options[k]
                try:
                    safe[k] = typ(v)
                except:
                    pass

        return safe
    
    def parse_options(self, opt):
        if 'segment' not in opt:
            raise ValueError('Segment options required')
        safe        = self.safe_options(opt['segment']);
        optlist     = super(SegmentFormat, self).parse_options(opt);
        if 'segment' in opt:
            if 'time' in safe:
                optlist.extend(['-segment_time', str(safe['time'])])
            if 'list_size' in safe:
                optlist.extend(['-segment_list_size', str(safe['list_size'])])
            if 'list_type' in safe:
                optlist.extend(['-segment_list_type', safe['list_type']])
            if 'list_file' in safe:
                optlist.extend(['-segment_list', safe['list_file']])  
            if not 'format' in safe:
                raise ValueError('format of segment is required');
            else:
                optlist.extend(['-segment_format', safe['format']])
            return optlist
        return None;


format_list = [
    OggFormat, AviFormat, MkvFormat, WebmFormat, FlvFormat,
    MovFormat, Mp4Format, MpegFormat, Mp3Format, SegmentFormat
]
