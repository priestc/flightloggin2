import math

def coord_dist(p1, p2):
    """From http://www.johndcook.com/python_longitude_latitude.html
    
    ksea-klga:
    
    gcm = 2097 nm
    airnav = 2089.7
    postgis = 2090.999
    this = 2093.347
    
    """
    
    lat1=p1.y
    long1=p1.x
    lat2=p2.y
    long2=p2.x
    
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    try:
        arc = math.acos( cos )
    except ValueError:
        return None

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 3443.92
