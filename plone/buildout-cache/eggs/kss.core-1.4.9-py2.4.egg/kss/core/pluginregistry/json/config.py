     
try:
    import jsonserver
    from jsonserver.interfaces import IJSONRPCRequest
    from jsonserver.minjson.interfaces import IJSONStreamWriteable, IJSONWriter
except ImportError:
    try:
        import Products.jsonserver
        from Products.jsonserver.interfaces import IJSONRPCRequest
        from Products.jsonserver.minjson.interfaces import IJSONStreamWriteable, IJSONWriter
    except ImportError:
        HAS_JSON = False
    else:
        HAS_JSON = True
else:
    HAS_JSON = True
