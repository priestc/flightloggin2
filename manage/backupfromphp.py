
class InvalidToken(Exception):
    pass

class InvalidURL(Exception):
    pass

class PHPBackup(object):
        
    def __init__(self, url):
        self.url = url
        
    def validate(self):
        self.uid = self._get_uid(self.url)
    
    def get_file(self):
        import urllib2
        self.validate()
        url = "http://old.flightlogg.in/backup.php?sec=%s" % self.uid
        f = urllib2.urlopen(url)
        return f
        
    def _verify_pair(self, token, uid):
        """Actually does the verifying to make sure the token is correct
        """
        from main.utils import hash_ten
        calc_token = hash_ten(uid)
        
        if not token == calc_token:
            raise InvalidToken
        
    def _get_uid(self, url):
        """
        returns the UID as long as it validates against the token
        url ex: http://flightlogg.in/logbook.php?share=1&token=6b86b273ff
        """
        
        if not "flightlogg.in" in url:
            raise InvalidURL
        
        import re
        t = m=re.search('token=[A-za-z0-9]+', url).group()
        u = m=re.search('share=[\d]+&', url).group()
        
        token = t[6:]
        uid = u[6:][:-1]
        
        #will raise error if not valid
        self._verify_pair(token, uid)
        
        return uid
