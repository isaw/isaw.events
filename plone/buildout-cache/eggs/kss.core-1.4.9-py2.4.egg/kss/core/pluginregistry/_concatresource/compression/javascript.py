'''\
The javascript compressor uses the 3rdparty packer module
that is taken from Plone's ResourceRegistries.'''

from thirdparty.packer import JavascriptPacker
# Packer needs to be created for each packing

def stripout_comments(data):
    'Strips out ;;; lines from the data.'
    result = []
    for line in data.splitlines(True):
        if not line.lstrip().startswith(';;;'):
            result.append(line)
    return ''.join(result)

def remove_markers(data):
    'Replaces the ;;; markers by spaces but leaves the lines.'
    result = []
    for line in data.splitlines(True):
        if line.lstrip().startswith(';;;'):
            line = line.lstrip()[3:]
            result.append('   ')
        result.append(line)
    return ''.join(result)

def compress(data, compress_level):
    if compress_level == "devel":
        return remove_markers(data)
    elif compress_level == "stripped":
        return stripout_comments(data)
    elif compress_level == "safe":
        data = stripout_comments(data)
        jspacker_safe = JavascriptPacker('safe')
        return jspacker_safe.pack(data)
    elif compress_level == "full":
        data = stripout_comments(data)
        jspacker_full = JavascriptPacker('full')
        return jspacker_full.pack(data)
    elif compress_level == "safe-devel":
        date = remove_markers(data)
        jspacker_safe = JavascriptPacker('safe')
        return jspacker_safe.pack(data)
    elif compress_level == "full-devel":
        date = remove_markers(data)
        jspacker_full = JavascriptPacker('full')
        return jspacker_full.pack(data)
    else:
        # none
        return data
