def hash_ten(value):
    import hashlib;
    m = hashlib.sha256()
    m.update(str(value))
    return m.hexdigest()[:10]
