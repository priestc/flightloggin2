def hash_ten(value, length=10):
    import hashlib;
    m = hashlib.sha256()
    m.update(str(value))
    return m.hexdigest()[:length]
