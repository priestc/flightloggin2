

class GetPHPBackup(object):

    class InvalidToken(Exception):
        pass

    class InvalidURL(Exception):
        pass
        
    def __init__(self, user, url):
        self.user = user
        self.token, self.uid = self.extract_token_and_uid(url)
    
    def get_file(self):
        import urllib
        url = "http://old.flightlogg.in/backup.php?sec=%s" % self.uid
        f=urllib.urlopen(url)
        print f.read()
        return f
        
    def verify_pair(self, token, uid):
        import hashlib;
        m = hashlib.sha256()
        m.update(uid) # poop = the salt used on the PHP site
        calc_token = m.hexdigest()[:10]
        
        if not token == calc_token:
            raise self.InvalidToken
        
    def extract_token_and_uid(self, url):
        """
        ex: http://flightlogg.in/logbook.php?share=1&token=6b86b273ff
        """
        
        if not "flightlogg.in" in url:
            raise self.InvalidURL
        
        import re
        t = m=re.search('token=[A-za-z0-9]+', url).group()
        u = m=re.search('share=[\d]+&', url).group()
        
        token = t[6:]
        uid = u[6:][:-1]
        
        #will raise error if not valid
        self.verify_pair(token, uid)
        
        return token, uid
