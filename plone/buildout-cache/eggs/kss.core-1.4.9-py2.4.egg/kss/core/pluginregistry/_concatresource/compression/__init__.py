'''\
Preprocess resource files by applying compression on them
'''

__all__ = ('compress', )

from javascript import compress as compress_javascript

def compress(data, content_type, compress_level):
    'Returns compressed text for a given content type'
    assert content_type == 'application/x-javascript', \
        'Only application/x-javascript content types are supported.'
    return compress_javascript(data, compress_level)
