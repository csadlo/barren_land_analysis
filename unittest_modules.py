from BLA_modules import Point, Parcel, ParcelsHaveOverlap, ParcelsHaveOverlapDebug, ParcelsShareBorder


def test_ParcelsHaveOverlap():

    # Assuming a 100x100 grid:

    print("\nNow Testing ParcelsHaveOverlap()")

    # Make sure that a parcel can be detected as overlapping with itself
    parcel_center       = Parcel(Point(40, 40), Point(60, 60), "unknown")
    assert ParcelsHaveOverlap(parcel_center, parcel_center) == True, "Center and Center overlap is True"

    # These overlap in a 'plus' shape:
    parcel_horizontal   = Parcel(Point(10, 40), Point(90, 60), "unknown")
    parcel_vertical     = Parcel(Point(40, 10), Point(60, 90), "unknown")
    assert ParcelsHaveOverlap(parcel_horizontal, parcel_vertical) == True, "Horizontal and Vertical overlap is True"

    # Horizontal and Center Overlap case:
    assert ParcelsHaveOverlap(parcel_horizontal, parcel_center) == True, "Horizontal and Center Overlap is True"

    # Vertical and Center Overlap case:
    assert ParcelsHaveOverlap(parcel_horizontal, parcel_center) == True, "Vertical and Center Overlap is True"

    # Parcel Big overlaps Parcel Small completely:
    parcel_big       = Parcel(Point(10, 10), Point(90, 90), "unknown")
    parcel_small     = Parcel(Point(40, 40), Point(60, 60), "unknown")
    assert ParcelsHaveOverlap(parcel_big, parcel_small) == True, "Big and Small overlap is True"

    # Parcel Big overlaps Parcel Small completely and share two border:
    parcel_big       = Parcel(Point(10, 10), Point(90, 90), "unknown")
    parcel_small     = Parcel(Point(10, 10), Point(60, 60), "unknown")
    assert ParcelsHaveOverlap(parcel_big, parcel_small) == True, "Big and Small overlap is True"

    # None overlap and they are far from each other:
    parcel_LowerLeft =  Parcel(Point(10, 10), Point(30, 30), "unknown")
    parcel_LowerRight = Parcel(Point(70, 10), Point(90, 30), "unknown")
    parcel_UpperLeft =  Parcel(Point(10, 70), Point(30, 90), "unknown")
    parcel_UpperRight = Parcel(Point(70, 70), Point(90, 90), "unknown")

    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_LowerRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_UpperLeft) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_UpperRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerRight, parcel_UpperLeft) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerRight, parcel_UpperRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_UpperLeft, parcel_UpperRight) == False, "Should return False"

    # None overlap but they all share borders with each other:
    parcel_LowerLeft =  Parcel(Point(20, 20), Point(50, 50), "unknown")
    parcel_LowerRight = Parcel(Point(50, 20), Point(80, 50), "unknown")
    parcel_UpperLeft =  Parcel(Point(20, 50), Point(50, 80), "unknown")
    parcel_UpperRight = Parcel(Point(50, 50), Point(80, 80), "unknown")

    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_LowerRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_UpperLeft) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerLeft, parcel_UpperRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerRight, parcel_UpperLeft) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_LowerRight, parcel_UpperRight) == False, "Should return False"
    assert ParcelsHaveOverlap(parcel_UpperLeft, parcel_UpperRight) == False, "Should return False"

    # These tests were created because errors were found during full-scale problem solving and traced back to these modules:
    # None of these parcels overlap with the barren parcel, so they should all return False
    test_parcel_1 = Parcel(Point(0, 60), Point(60, 100), "unknown")
    test_parcel_2 = Parcel(Point(0, 60), Point(80, 100), "unknown")
    test_parcel_3 = Parcel(Point(0, 60), Point(100, 100), "unknown")
    barren_parcel = Parcel(Point(60, 40), Point(80, 60), "barren")

    assert ParcelsHaveOverlap(test_parcel_1, barren_parcel) == False, "Should return False"
    assert ParcelsHaveOverlap(test_parcel_2, barren_parcel) == False, "Should return False"
    assert ParcelsHaveOverlap(test_parcel_3, barren_parcel) == False, "Should return False"

    print("Passed")


def test_ParcelsShareBorder():

    # Assuming a 100x100 grid:

    print("\nNow Testing ParcelsShareBorder()")

    # A and B actually share a border case:
    # A shares its entire right border with part of B's left border:
    parcel_A = Parcel(Point(0, 10), Point(20, 20), "unknown")
    parcel_B = Parcel(Point(20, 0), Point(30, 40), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == True, "Should return True"

    # A and B only share a corner point case Point(20, 20):
    # A shares its upperright corner with B's lowerleft
    parcel_A = Parcel(Point(0, 10), Point(20, 20), "unknown")
    parcel_B = Parcel(Point(20, 20), Point(30, 40), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == False, "Should return False"

    # A and B only share a corner point case Point(20, 20):
    # A shares its bottomright corner with B's upperleft
    parcel_A = Parcel(Point(0, 20), Point(20, 30), "unknown")
    parcel_B = Parcel(Point(20, 10), Point(40, 20), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == False, "Should return False"

    # B is too far above A case:
    parcel_A = Parcel(Point(0, 10), Point(20, 20), "unknown")
    parcel_B = Parcel(Point(20, 30), Point(30, 70), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == False, "Should return False"

    # A and B actually share a border case:
    # A shares its entire right border with part of B's right border 
    # (ie. they both overlap and share a border):
    parcel_A = Parcel(Point(0, 10), Point(20, 20), "unknown")
    parcel_B = Parcel(Point(10, 0), Point(20, 30), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == True, "Should return True"

    # A and B actually share a border case:
    # A and B are the same parcel therefore share all borders:
    parcel_A = Parcel(Point(0, 10), Point(20, 20), "unknown")
    parcel_B = parcel_A
    assert ParcelsShareBorder(parcel_A, parcel_B) == True, "Should return True"

    # A and B overlap but do not share a border:
    parcel_A = Parcel(Point(0, 20), Point(50, 30), "unknown")
    parcel_B = Parcel(Point(20, 0), Point(30, 50), "unknown")
    assert ParcelsShareBorder(parcel_A, parcel_B) == False, "Should return False"

    print("Passed")


if __name__ == "__main__":
    

    
    test_ParcelsHaveOverlap()

    test_ParcelsShareBorder()

    print("\nAll Module Unit Tests Passed")