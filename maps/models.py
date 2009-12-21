def copy_empty_images(sender, **kwargs):
    """ Copy over some blank map files to demonstrate to the user
        what the heck "stats maps" even is
    """
    
    ## only work when the User instance is created
    if not kwargs.pop('created'):
        return
    
    import os
    import shutil
    from django.conf import settings
    
    id_ = str(kwargs.pop('instance').id)
    directory = os.path.join(settings.BASE_MAP_PATH, id_)
    try:
        os.makedirs(directory)
    except OSError:
        ## if it already exists, then don't worry about it.
        pass
        
    names = ('states-unique.png','states-count.png','states-colored.png')
        
    for name in names:
        blank = os.path.join(settings.PROJECT_PATH, "maps", "blank", name)
        filename = os.path.join(directory, name)
        shutil.copy(blank, filename)
        
   
## registere this function to be called whenever a user instance is saved
from django.contrib.auth.models import User
from django.db.models.signals import post_save
post_save.connect(copy_empty_images, sender=User)
