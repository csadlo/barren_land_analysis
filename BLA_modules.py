# Outline Data Structures:

# Point
class Point(object):

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "Point(%s,%s)"%(self.X, self.Y)

# Parcel
class Parcel:

    def __init__(self, lowerleft: Point,  upperright: Point, land_type):

        self.lowerleft = lowerleft
        self.upperright = upperright
        self.area = (upperright.X - lowerleft.X) * (upperright.Y - lowerleft.Y)
        self.land_type = land_type
        # (Optional Optimization)
        # Store land_type as an integer instead of string
        self.belongs_to_collection = -1

        # TODO
        # Add error-checking for when the lowerleft and upperright are not in fact lower and upper
        # Add check to make sure area isn't zero or negative

    def __str__(self):
        return "Parcel(%s,%s,%s)"%(self.lowerleft, self.upperright, self.land_type)

# LandCollection
class LandCollection:

    def __init__(self, id, land_type):

        self.id = id
        self.land_type = land_type
        self.list_of_parcels = []
        self.total_land_area = 0


# Helper Functions:

# A function that takes two parcels of land and checks if they have any overlap between them
def ParcelsHaveOverlap(parcel_A, parcel_B):
    
    # Return false if:
    # If A is too far left of B
    if (parcel_A.upperright.X <= parcel_B.lowerleft.X):
        return False
    # Or if A is too far right of B
    elif (parcel_A.lowerleft.X >= parcel_B.upperright.X):
        return False
    # Or if A is too far above B
    elif (parcel_A.lowerleft.Y >= parcel_B.upperright.Y):
        return False
    # Or if A is too far below B
    elif (parcel_A.upperright.Y <= parcel_B.lowerleft.Y):
        return False

    return True

# A function that takes two parcels of land and checks if they have any overlap between them
def ParcelsHaveOverlapDebug(parcel_A, parcel_B):
    
    # Return false if:
    # If A is too far left of B
    if (parcel_A.upperright.X <= parcel_B.lowerleft.X):
        print("Reason A:")
        return False
    # Or if A is too far right of B
    elif (parcel_A.lowerleft.X >= parcel_B.upperright.X):
        print("Reason B:")
        return False
    # Or if A is too far above B
    elif (parcel_A.lowerleft.Y >= parcel_B.upperright.Y):
        print("Reason C:")
        return False
    # Or if A is too far below B
    elif (parcel_A.upperright.Y <= parcel_B.lowerleft.Y):
        print("Reason D:")
        return False

    print("Reason E:")
    return True

# A function that checks if a given parcel contains any barren land areas and returns a specific barren land parcel if true, else it returns None
def ParcelContainsBarren(parcel, barren_lands):
    # Loop over the list of barren lands
    for some_barren_parcel in barren_lands:
        if ParcelsHaveOverlap(parcel, some_barren_parcel):
            return some_barren_parcel

    return None

# Checks if two number ranges contain a non-zero overlap with each other
def RangesHaveOverlap(start1, end1, start2, end2):
    return end1 > start2 and end2 > start1

# This function takes in two parcels and determines if they share a non-zero length border with each other regardless of if they share any area overlap.
def ParcelsShareBorder(parcel_A, parcel_B):

    # Return False if there is a clear gap between them:
    # If A is too far left of B
    if (parcel_A.upperright.X < parcel_B.lowerleft.X):
        return False
    # Or if A is too far right of B
    elif (parcel_A.lowerleft.X > parcel_B.upperright.X):
        return False
    # Or if A is too far above B
    elif (parcel_A.lowerleft.Y > parcel_B.upperright.Y):
        return False
    # Or if A is too far below B
    elif (parcel_A.upperright.Y < parcel_B.lowerleft.Y):
        return False

    # Check if A's bottom edge lines up with either of B's top or bottom edges
    if (parcel_A.lowerleft.Y == parcel_B.lowerleft.Y) or (parcel_A.lowerleft.Y == parcel_B.upperright.Y):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.X, parcel_A.upperright.X, parcel_B.lowerleft.X, parcel_B.upperright.X):
            return True

    # Check if A's top edge lines up with either of B's top or bottom edges
    if (parcel_A.upperright.Y == parcel_B.lowerleft.Y) or (parcel_A.upperright.Y == parcel_B.upperright.Y):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.X, parcel_A.upperright.X, parcel_B.lowerleft.X, parcel_B.upperright.X):
            return True

    # Check if A's left edge lines up with either of B's left or right edges
    if (parcel_A.lowerleft.X == parcel_B.lowerleft.X) or (parcel_A.lowerleft.X == parcel_B.upperright.X):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.Y, parcel_A.upperright.Y, parcel_B.lowerleft.Y, parcel_B.upperright.Y):
            return True

    # Check if A's right edge lines up with either of B's left or right edges
    if (parcel_A.upperright.X == parcel_B.lowerleft.X) or (parcel_A.upperright.X == parcel_B.upperright.X):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.Y, parcel_A.upperright.Y, parcel_B.lowerleft.Y, parcel_B.upperright.Y):
            return True

    return False


# This function takes in two parcels and determines if they share a non-zero length border with each other regardless of if they share any area overlap or not.
def ParcelsShareBorderDebug(parcel_A, parcel_B):

    # Return false if there is a clear gap between them:
    # If A is too far left of B
    if (parcel_A.upperright.X < parcel_B.lowerleft.X):
        print("Reason A:")
        return False
    # Or if A is too far right of B
    elif (parcel_A.lowerleft.X > parcel_B.upperright.X):
        print("Reason B:")
        return False
    # Or if A is too far above B
    elif (parcel_A.lowerleft.Y > parcel_B.upperright.Y):
        print("Reason C:")
        return False
    # Or if A is too far below B
    elif (parcel_A.upperright.Y < parcel_B.lowerleft.Y):
        print("Reason D:")
        return False

    # Check if A's bottom edge lines up with either of B's top or bottom edges
    if (parcel_A.lowerleft.Y == parcel_B.lowerleft.Y) or (parcel_A.lowerleft.Y == parcel_B.upperright.Y):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.X, parcel_A.upperright.X, parcel_B.lowerleft.X, parcel_B.upperright.X):
            print("Reason E:")
            return True

    # Check if A's top edge lines up with either of B's top or bottom edges
    if (parcel_A.upperright.Y == parcel_B.lowerleft.Y) or (parcel_A.upperright.Y == parcel_B.upperright.Y):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.X, parcel_A.upperright.X, parcel_B.lowerleft.X, parcel_B.upperright.X):
            print("Reason F:")
            return True

    # Check if A's left edge lines up with either of B's left or right edges
    if (parcel_A.lowerleft.X == parcel_B.lowerleft.X) or (parcel_A.lowerleft.X == parcel_B.upperright.X):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.Y, parcel_A.upperright.Y, parcel_B.lowerleft.Y, parcel_B.upperright.Y):
            print("Reason G:")
            return True

    # Check if A's right edge lines up with either of B's left or right edges
    if (parcel_A.upperright.X == parcel_B.lowerleft.X) or (parcel_A.upperright.X == parcel_B.upperright.X):
        # Then we need to check if the edge's ranges also have any overlap:
        if RangesHaveOverlap( parcel_A.lowerleft.Y, parcel_A.upperright.Y, parcel_B.lowerleft.Y, parcel_B.upperright.Y):
            print("Reason H:")
            return True

    print("Reason I:")
    return False

# This function is simple enough. It checks if a point would be inside of a parcel by its description
def PointIsInsideParcel(X, Y, parcel):

    return (parcel.lowerleft.X <= X and X < parcel.upperright.X) and (parcel.lowerleft.Y <= Y and Y < parcel.upperright.Y)
