#def process_input():

# In terms of storage efficiency, I immediately noticed that storing a 2d array for each point of land would not
# scale efficiently in a production environment, particularly in the case of a sparsely populated matrix. So
# I decided to use a different method of simply recording parcels of land according to coordinate values.

# Assumptions made:
# Assumed that it is valid input for two barren lands to partially or completely overlap each other


# Outline Data Structures:

    # Parcel:
        # int bottomleft_x
        # int bottomleft_y
        # int upperright_x
        # int upperright_y
        # int area
        # type BARREN or FERTILE
        

# Outline Helper Functions:

    # A function that takes two parcels of land and checks if they have any overlap between them
    # ParcelsHaveOverlap(parcel A, parcel B)
        # Return true if:
        # Any of the (4) corner coordinates are within the ranges of the other parcel
        # If there is overlap in the X range, AND the Y range

    # A function that checks if a parcel contains any barren land and returns a barren land parcel if true
    # ParcelContainsBarren(parcel, barren_lands)
        # Loop over the sorted list of barren lands
            # ParcelsHaveOverlap(parcel, some_barren_parcel)



# Outline Program:

    # Given a section of land that has barren land  (Started testing with 100,100 with a barren land of 60,40 79,59)

    # read from stdin the size of the grid
    # read from stdin the coords of barren land rectangles

    # Generate a list of barren-land parcel objects

    # (Optional Optimization) Check to confirm that no two barren-land parcels completely overlap another. 
    # If so, the overlapped parcel should be removed from the list.

    # (Optional Optimization)
    # Sort the list of barren-land parcels by lowerleft corner coordinate, biased in the X direction first

    # Brute Force - Optimize Later
    # Write a list of all the possible parcels (rectangles) of land and their associated coordinates
        # (This process must include all permutations. A hueristic may be written later for optimization)

        # Generate coordinates of possible fertile land parcels
            # Build a list of all of the relevant X coordinates of the barren-land parcels plus outer dimensions.
                # Sort and make values unique.
            # Build a list of all of the relevant Y coordinates of the barren-land parcels plus outer dimensions.
                # Sort and make values unique.

        # Select every possible lower-left parcel corner coordinate tuple
        # Loop over Y coord list (starting at 0)
            # Loop over X coord list (starting at 0)
                # Find all possible upper-right corner coordinates for this lower-left corner coordinate
                # Set inner loop upperbounds to maximums

                # Use a new starting counter set to y-counter + 1
                # Loop over remaining y-coordinates list to upperbound

                    # Use a new starting counter set to x-counter + 1
                    # Loop over remaining x-coordinates list to upperbound

                        # With a suggested upper-right corner coordinate in hand, check if the resulting 
                        # parcel would contain barren land. If the parcel would contain barren land, 
                        # exit this loop because nothing else beyond will be barren-free land.

                        # Create the suggested parcel
                        # suggested_parcel

                        # (Checking)
                        # barren_land = ParcelContainsBarren(suggested_parcel, list_of_barren_lands)
                        # If empty
                            # Add the suggested parcel to a growing list of candidates
                        # Else
                            # Exit
                            # (Optimization) Access the lower-left coordinate of the returned barren parcel.
                            # Save the X coordinate value or index and use as the new X upperbound

                    

        # One possible heuristic is to keep all of the sets of parcels from each permutation separated and compare
        # the largest parcels contained within each set. Throw away the sets whose largest parcels is too small.

    
    # Then *SORTING* of the list highest to lowest areas of land

    # Select the largest parcel => LARGEST

    # Loop once over the remaining parcels in the (sorted) list with
        # ParcelsHaveOverlap(LARGEST, candidate_parcel)
        # If the candidate overlaps with the largest, remove the candidate from the list

    # Now loop again over the (still sorted) list of remaining parcels. (None of which overlap with the LARGEST)
        # Grab the second largest parcel and repeat the previous step with it
        # Repeat with third largest parcel and so on...

    # Remaining list is barren-land-free parcels that have no overlap with each other and also sorted.

    # Cycle over the list of barren-land-free parcels and find which ones are connected to each other and 
    # associate them with each other in some sort of collection

    # Sort the collections into ascending order by land area and send to stdout


#############################################################################################
#############################################################################################
#############################################################################################

from BLA_modules import Point, Parcel, LandCollection, ParcelsHaveOverlap, ParcelContainsBarren, ParcelsShareBorder, PointIsInsideParcel
from collections import deque


# This series 

# Generate Parcels in a brute-force manner. Where N is the size of the grid and X is the number of barren land, this is O(X^5) time complexity, but O(1) in terms of N
def GenerateParcels_BruteForce(X_coord_values, Y_coord_values, list_of_barren_lands):

    debug = False

    list_of_fertile_lands = []

    # Select/cycle over every possible lower-left parcel corner coordinate tuple
    # Loop over Y coord list (starting at 0)
    for i in range(0, len(Y_coord_values)-1):

        lowerleft_Y = Y_coord_values[i]

        # Loop over X coord list (starting at 0)
        for j in range(0, len(X_coord_values)-1):

            lowerleft_X = X_coord_values[j]
            LowerLeft = Point(lowerleft_X, lowerleft_Y)

            # Find all possible upper-right corner coordinate tuples for this given lower-left corner coordinate tuple

            # Set inner loop lowerbounds to minimums
            X_loop_index_lowerbound = j + 1
            Y_loop_index_lowerbound = i + 1

            # Set inner loop upperbounds to maximums
            X_loop_index_upperbound = len(X_coord_values)
            Y_loop_index_upperbound = len(Y_coord_values)

            # Use a new starting counter set to y-counter + 1
            # Loop over remaining y-coordinates list to upperbound

            ii = Y_loop_index_lowerbound
            while Y_loop_index_lowerbound <= ii and ii < Y_loop_index_upperbound:

                # Use a new starting counter set to x-counter + 1
                # Loop over remaining x-coordinates list to upperbound

                jj = X_loop_index_lowerbound
                while X_loop_index_lowerbound <= jj and jj < X_loop_index_upperbound:

                    UpperRight = Point(X_coord_values[jj],Y_coord_values[ii])
                    if debug: print("UpperRight Corner -", UpperRight)

                    # With a suggested upper-right corner coordinate in hand, create the suggested parcel
                    parcel_to_be_checked = Parcel(LowerLeft, UpperRight, "unknown")

                    # Check if the resulting parcel would contain some amount of barren land. If the parcel would contain 
                    # barren land, try a parcel that is slightly smaller and see if it is barren-land free.
                    # If the parcel IS free of barren-land, then we can exit this loop and suggest the
                    # next lowerleft corner coordinate tuple.

                    # (Checking)
                    barren_land = ParcelContainsBarren(parcel_to_be_checked, list_of_barren_lands)

                    if barren_land is None: # Great!
                        if debug: print(parcel_to_be_checked)
                        # Add the suggested parcel to a growing list of purely fertile lands
                        parcel_to_be_checked.land_type = "fertile"
                        list_of_fertile_lands.append(parcel_to_be_checked)
                    else:
                        if debug: print(parcel_to_be_checked, " failed on ", barren_land)
                        if debug: print("jj =", jj)
                        if debug: print("X_loop_index_upperbound =", X_loop_index_upperbound)

                        # Save the X coordinate value's index and use as the new X upperbound for
                        # subsequent loops with larger Y values. (ie. a taller, but skinnier parcel_to_be_checked)
                        # We don't want to break here but rather preserve the more limiting X_loop_index_upperbound for further passes of larger values of Y
                        X_loop_index_upperbound = jj    # Short-circuit this X-direction for-loop
                    
                    jj = jj + 1

                ii = ii + 1

    return list_of_fertile_lands


# This generates parcels by generating and looping over lowerleft corner coordinate tuples and choosing the smallest possible upperright corner coordinate 
# tuple values to pair the lowerleft with. This effectively eliminates iterating over multiple upperright corner coordinate tuples and just calculate it instead
# This shifts more work to the final part (the "Stitching" part) of the Novel_BLA_Method() solution, but it might be faster overall.
def GenerateParcels_SmallestParcelsOnly(X_coord_values, Y_coord_values, list_of_barren_lands):

    debug = False

    list_of_fertile_lands = []

    # Select/cycle over every possible lower-left parcel corner coordinate tuple
    # Loop over Y coord list (starting at 0)
    for i in range(0, len(Y_coord_values)-1):

        lowerleft_Y = Y_coord_values[i]

        # Loop over X coord list (starting at 0)
        for j in range(0, len(X_coord_values)-1):

            lowerleft_X = X_coord_values[j]
            LowerLeft = Point(lowerleft_X, lowerleft_Y)

            # Now calculate the smallest possible upper-right corner coordinate tuple for this given lower-left corner coordinate tuple
            ii = i + 1
            jj = j + 1

            UpperRight = Point(X_coord_values[jj],Y_coord_values[ii])
            if debug: print("UpperRight Corner -", UpperRight)

            # With a suggested upper-right corner coordinate in hand, create the suggested parcel
            parcel_to_be_checked = Parcel(LowerLeft, UpperRight, "unknown")

            # Check if the resulting parcel would contain some amount of barren land. If the parcel would contain 
            # barren land, then skip to the next possible lowerleft corner coordinate tuple. The current one is a lost cause

            # (Checking)
            barren_land = ParcelContainsBarren(parcel_to_be_checked, list_of_barren_lands)

            if barren_land is None: # Great!
                # Add the suggested parcel to a growing list of purely fertile lands
                parcel_to_be_checked.land_type = "fertile"
                list_of_fertile_lands.append(parcel_to_be_checked)

    return list_of_fertile_lands


# Generate Parcels by guessing a wide (X-direction parcel) and reducing the width if too wide
def GenerateParcels_FirstOptimization(X_coord_values, Y_coord_values, list_of_barren_lands):

    debug = False

    list_of_fertile_lands = []

    # Select/cycle over every possible lower-left parcel corner coordinate tuple
    # Loop over Y coord list (starting at 0)
    for i in range(0, len(Y_coord_values)-1):

        lowerleft_Y = Y_coord_values[i]

        # Loop over X coord list (starting at 0)
        for j in range(0, len(X_coord_values)-1):

            lowerleft_X = X_coord_values[j]
            LowerLeft = Point(lowerleft_X, lowerleft_Y)

            # Find all possible upper-right corner coordinate tuples for this given lower-left corner coordinate tuple

            # Set inner loop lowerbounds to minimums
            X_loop_index_lowerbound = j + 1
            Y_loop_index_lowerbound = i + 1

            # Set inner loop upperbounds to maximums
            X_loop_index_upperbound = len(X_coord_values)
            Y_loop_index_upperbound = len(Y_coord_values)

            # Use a new starting counter set to y-counter + 1
            # Loop over remaining y-coordinates list to upperbound

            ii = Y_loop_index_lowerbound
            while Y_loop_index_lowerbound <= ii and ii < Y_loop_index_upperbound:

                # Use a new starting counter set to the outer \x-counter + 1
                # Loop over remaining x-coordinates list to upperbound

                jj = X_loop_index_upperbound - 1
                while X_loop_index_lowerbound <= jj and jj < X_loop_index_upperbound:

                    UpperRight = Point(X_coord_values[jj],Y_coord_values[ii])
                    if debug: print("UpperRight Corner -", UpperRight)

                    # With a suggested upper-right corner coordinate in hand, create the suggested parcel
                    parcel_to_be_checked = Parcel(LowerLeft, UpperRight, "unknown")

                    # Check if the resulting parcel would contain some amount of barren land. If the parcel would contain 
                    # barren land, try a parcel that is slightly smaller and see if it is barren-land free.
                    # If the parcel IS free of barren-land, then we can exit this loop and suggest the
                    # next lowerleft corner coordinate tuple.

                    # (Checking)
                    barren_land = ParcelContainsBarren(parcel_to_be_checked, list_of_barren_lands)

                    if barren_land is None: # Great!
                        # Add the suggested parcel to a growing list of purely fertile lands
                        parcel_to_be_checked.land_type = "fertile"
                        list_of_fertile_lands.append(parcel_to_be_checked)
                        # Cause us to exit both of the while loops
                        ii = Y_loop_index_upperbound
                        jj = X_loop_index_upperbound # redundant
                        break
                    else:
                        # If this parcel contains barren land area, try and check a smaller parcel
                        jj = jj - 1
                
                ii = ii + 1

    return list_of_fertile_lands


def Novel_BLA_Method(GRID_MAX_X, GRID_MAX_Y, list_of_barren_lands):
    
    debug = False
    perf_debug = False

    if debug: print("\nBeginning Timer Now")
    time_after_input = time.perf_counter()

    # Write a list of all the possible parcels (rectangles) of land and their associated coordinates
    # (This process must include all permutations. A hueristic may be written later for optimization)

    # Generate the corner coordinates of possible fertile land parcels
    # Build a list of all of the relevant X coordinates of the barren-land parcels plus outer dimensions.
    X_coord_values = []
    X_coord_values.append(0)
    X_coord_values.append(GRID_MAX_X)

    for barren_parcel in list_of_barren_lands:
        X_coord_values.append(barren_parcel.lowerleft.X)
        X_coord_values.append(barren_parcel.upperright.X)

    # Sort and make values unique.
    X_coord_values = sorted(set(X_coord_values))

    # Build a list of all of the relevant Y coordinates of the barren-land parcels plus outer dimensions.
    Y_coord_values = []
    Y_coord_values.append(0)
    Y_coord_values.append(GRID_MAX_Y)

    for barren_parcel in list_of_barren_lands:
        Y_coord_values.append(barren_parcel.lowerleft.Y)
        Y_coord_values.append(barren_parcel.upperright.Y)

    # Sort and make values unique.
    Y_coord_values = sorted(set(Y_coord_values))

    if debug: print(X_coord_values)
    if debug: print(Y_coord_values)

    if perf_debug: print("Beginning Parcel Generation")
    time_before_nested_loop = time.perf_counter()

    # Generate a list of fertile (non-barren-land-containing) parcels
    # This is where most of the time is spent in the overall algorithm. Time spent 

    # One possible heuristic here is to keep all of the sets of parcels from each major permutation separated and compare
    # the largest parcels contained within each set. Throw away whole sets whose largest parcel is too small.

    #list_of_fertile_lands = GenerateParcels_BruteForce(X_coord_values, Y_coord_values, list_of_barren_lands)

    list_of_fertile_lands = GenerateParcels_FirstOptimization(X_coord_values, Y_coord_values, list_of_barren_lands)

    #list_of_fertile_lands = GenerateParcels_SmallestParcelsOnly(X_coord_values, Y_coord_values, list_of_barren_lands)

    # TODO - Next
    # Create a modified version of GenerateParcels_SmallestParcelsOnly() which constructs a connected graph to contain 
    # all of the fertile parcels of land instead of a list.



    if perf_debug: print("Finishing Parcel Generation")
    time_after_nested_loop = time.perf_counter()
    if perf_debug: print("Time elasped is =", time_after_nested_loop - time_before_nested_loop)
    if perf_debug: print("Total time elapsed =", time_after_nested_loop - time_after_input)

    # Then *SORTING* of the list highest to lowest areas of land
    list_of_fertile_lands.sort(key=lambda L: L.area, reverse=True)

    # Storage list for our final answer
    list_of_final_parcels = []


    # Currently the code below is a BFS algorithm on a dataset that isn't yet contained/representated in a graph model. Currently it is a simple list.
    # If it were contained in a graph model, we could traverse a bit faster and not create/delete list_of_final_parcels or shorter_list_of_final_parcels.
    # Some basic performance testing shows that the following code is actually the one of the faster parts of the program, 
    # so until the other parts speed up, we need not be too concerned.

    if debug: print("Beginning Overlap While Loop")
    time_before_while_loop = time.perf_counter()
    if debug: print("Total time elapsed =", time_before_while_loop - time_after_input, flush=True)

    pass_count = 0
    if debug: print("Size of list_of_fertile_lands =", len(list_of_fertile_lands))

    while list_of_fertile_lands:    # while the list_of_fertile_lands is not empty...

        pass_count = pass_count + 1
        if debug: print("Pass ", pass_count, ":", flush=True)

        # Select the largest parcel => LARGEST
        largest_parcel = list_of_fertile_lands.pop(0)

        # Save this parcel for our final answer
        list_of_final_parcels.append(largest_parcel)

        parcels_removed_this_pass = 0
        new_list_of_fertile_lands = []
        # Loop once over the remaining parcels in the (sorted) list with
        for this_parcel in list_of_fertile_lands:

            if ParcelsHaveOverlap(largest_parcel, this_parcel):
                if debug: print("Found Overlap Between ", largest_parcel, "and", this_parcel)
                parcels_removed_this_pass = parcels_removed_this_pass + 1

            else:
                new_list_of_fertile_lands.append(this_parcel)
            
        if debug: print("Count of fertile parcels to be removed during this pass:", parcels_removed_this_pass, flush=True)

        list_of_fertile_lands = new_list_of_fertile_lands

        # Now loop again over the (still sorted) list of remaining parcels. (None of which overlap with the LARGEST)
        # Grab the second largest parcel and repeat the previous step with it
        # Repeat with third largest parcel and so on...

    if perf_debug: print("Finishing Overlap While Loop")
    time_after_while_loop = time.perf_counter()
    if perf_debug: print("Time elasped is =", time_after_while_loop - time_before_while_loop)
    if perf_debug: print("Total time elapsed =", time_after_while_loop - time_after_input)

    # Remaining list is barren-land-free parcels that have no overlap with each other and is also sorted in descending order

    if debug: print("List of parcels that have no overlap between each other:")
    i = 0
    for parcel in list_of_final_parcels:
        i = i + 1
        if debug: print(i, ": Area ", parcel.area, " ", parcel)

    # Cycle over the list of barren-land-free parcels and find which ones are connected to each other and 
    # associate them with each other in some sort of collection

    # Now we "stitch" the parcels together into contiguously connected but not necessarily rectangular collections of land
    # and total up the acreage of each collection containing one or more parcels. This algorithm should work relatively fast on unsorted lists
    if debug: print("Beginning Stitching While Loop", flush=True)
    time_before_while_loop = time.perf_counter()

    list_of_land_collections = []
    

    # Currently the code below is a BFS algorithm on a dataset that isn't yet contained/representated in a graph model. Currently it is a simple list.
    # If it were contained in a graph model, we could traverse a bit faster and not create/delete list_of_final_parcels or shorter_list_of_final_parcels.
    # Some basic performance testing shows that the following code is actually the fastest part of the program, so until the other parts speed up, we need not be too concerned.

    # Create a list of collections of parcels
    while list_of_final_parcels:    # while the list_of_final_parcels is not empty...

        # Start with the first parcel and use it to start a new collection of parcels
        first_parcel = list_of_final_parcels.pop(0)

        # Create a new LandCollection object
        # We intentially start id'ing the LandCollections at 1 instead of 0
        this_LC = LandCollection(len(list_of_land_collections)+1, "fertile")  
        this_LC.list_of_parcels.append(first_parcel)

        # Track the LandCollection among the other LandCollections
        list_of_land_collections.append(this_LC)

        # Setup a new queue to track all of the fertile parcels that will be iteratively discovered to be connected to
        # both directly and indirectly to the first_parcel
        # When the size of the queue reduces to zero, we know that we've exhausted all the parcels that could be connected
        queue = deque()
        queue.append(first_parcel)

        while queue:    # while the queue still has connected parcels to process

            this_parcel = queue.popleft()

            this_LC.list_of_parcels.append(this_parcel)
            this_LC.total_land_area += this_parcel.area

            connecting_parcels_found_this_pass = 0
            shorter_list_of_final_parcels = []

            # Find all the other (fertile) parcels that are neighboring this_parcel
            # Loop once over the remaining parcels in the list.
            # This will supply us with all the parcels that are directly connected to "this_parcel"
            for possible_neighbor_parcel in list_of_final_parcels:

                if ParcelsShareBorder(this_parcel, possible_neighbor_parcel):
                    if debug: print("Found A Shared Border Between ", this_parcel, "and", possible_neighbor_parcel, flush=True)
                    queue.append(possible_neighbor_parcel)
                    connecting_parcels_found_this_pass = connecting_parcels_found_this_pass + 1
                else:
                    shorter_list_of_final_parcels.append(possible_neighbor_parcel)
            
            if debug: print("Count of fertile parcels found to be connected during this pass:", connecting_parcels_found_this_pass, flush=True)

            list_of_final_parcels = shorter_list_of_final_parcels


    if perf_debug: print("Finishing Stitching While Loop", flush=True)
    time_after_while_loop = time.perf_counter()
    if perf_debug: print("Time elasped is =", time_after_while_loop - time_before_while_loop)
    if perf_debug: print("Total time elapsed =", time_after_while_loop - time_after_input)

    # Sort the collections into ascending order by land area and send to stdout
    list_of_land_collections.sort(key=lambda LC: LC.total_land_area)

    if debug: print("Final Output:")
    if list_of_land_collections:
        for this_LC in list_of_land_collections:
            print(this_LC.total_land_area, end=' ')
    else:
        print("0", end=' ')



# This is a simple "brute force" function that gets the job done but scales poorly with grid-size
def Basic_Breadth_First_Search_Method(GRID_MAX_X, GRID_MAX_Y, list_of_barren_lands):

    debug = False

    point_visited = []
    # Generate a 2d Array of GRID and set each point to "-1" if it is a barren square meter
    # Otherwise set it to 0
    for X in range(GRID_MAX_X):
        point_visited.append([])
        for Y in range(GRID_MAX_Y):
            point_visited[X].append([])

            barren_pt = False
            for parcel in list_of_barren_lands:
                if PointIsInsideParcel(X, Y, parcel):
                    barren_pt = True

            if barren_pt:
                point_visited[X][Y] = -1
            else:
                point_visited[X][Y] = 0

    queue = deque()
    list_of_land_collections = []

    if debug:
        for X in range(GRID_MAX_X):
            print(point_visited[X])

    # Cycle over the grid and find non-barren points that are connected to each other
    for Y in range(GRID_MAX_Y):
        for X in range(GRID_MAX_X):

            if point_visited[X][Y] == 0:
                if debug: print("queuing first thing X=",X,"Y=",Y, flush=True)
                queue.append([X, Y])

                # Being at this point in the code means that a new collection of parcels are being gathered
                LC = []

                while queue:

                    point = queue.popleft()
                    if debug: print("After popping, length of queue is ", len(queue))
                    if debug: print("point = ", point, flush=True)

                    this_points_X = point[0]
                    this_points_Y = point[1]

                    # If the grid point is out of bounds, just skip it and move on
                    if this_points_X < 0 or this_points_X >= GRID_MAX_X or this_points_Y < 0 or this_points_Y >= GRID_MAX_Y:
                        continue

                    if debug: print("point = ", point, "is within bounds", flush=True)
                    # If the grid point is in-bounds, isn't barren, and hasn't been visited, mark it as 
                    # having now been visited....
                    if point_visited[this_points_X][this_points_Y] == 0:
                        if debug: print("Marking X=",this_points_X,"Y=",this_points_Y,"as visited")
                        point_visited[this_points_X][this_points_Y] = 1
                        LC.append([this_points_X,this_points_Y])    # We will use this later to count the total square meters

                        # Then we get the neighbors of this newly-visited point and submit them to the queue for processing
                        queue.append([this_points_X-1,this_points_Y])    # Left Neighbor
                        queue.append([this_points_X+1,this_points_Y])    # Right Neighbor
                        queue.append([this_points_X,this_points_Y+1])    # Top Neighbor
                        queue.append([this_points_X,this_points_Y-1])    # Bottom Neighbor
                        if debug: print("length of queue is ", len(queue))

                # If LC is non-empty
                if LC:
                    list_of_land_collections.append(LC)

    list_of_land_areas = []
    for LC in list_of_land_collections:
        list_of_land_areas.append(len(LC))

    list_of_land_areas.sort()

    if list_of_land_areas:
        for LA in list_of_land_areas:
            print(LA, end=' ')
    else:
        print("0", end=' ')



from sys import stdin
from operator import methodcaller
from math import sqrt
import time
import os

def main():

    override_default_grid_size = os.getenv('OVERRIDE_DEFAULT_GRID_SIZE')

    if override_default_grid_size == "1":
        # read from stdin the coords of barren land rectangles
        grid_string = stdin.readline()
        GRID_MAX_X, GRID_MAX_Y = map(int, grid_string.split())
        GRID_MAX_X = GRID_MAX_X + 1
        GRID_MAX_Y = GRID_MAX_Y + 1
    else:   # Default values
        GRID_MAX_X = 400
        GRID_MAX_Y = 600

    list_of_barren_lands = []

    # read from stdin the coords of barren land rectangles
    # Generate a list of barren-land parcel objects
    for line in stdin:
        x1, y1, x2, y2 = map(int, line.split())
        x2 = x2 + 1
        y2 = y2 + 1
        # TODO
        # Add error checking here to confirm that the coordinate values provided are valid
        # I.e. is the lower-left and upper-right really lower-left and upper-right?
        # Are they within the bounds of the grid?

        input_barren_parcel = Parcel( Point(x1, y1), Point(x2, y2), "barren")
        list_of_barren_lands.append( input_barren_parcel )

    # (Optional Optimization) Check to confirm that no two barren-land parcels completely overlaps one over the other. 
    # If so, the overlapped parcel should be removed from the list. One less barren parcel to deal with.

    # Here we determine which algorithm to use depending on the number of barren areas 
    # and the size of the input grid. This program uses two algorithms, the first is a simple
    # breadth-first search algorithm where individual square meters and metadata are tracked in a 2d array.
    # The other uses a more novel approach that is extremely fast when number of barren lands isn't large
    # relative to the size of the grid. Some basic testing showed that even with a 1000x1000 
    # grid size and over 100 barren lands, the simple breadth-first search algorithm is easily outperformed
    # by the Novel_BLA_Method() which essentially runs in constant time relative to grid size.
    # The Novel_BLA_Method() is still unrefined and has a lot of room for improvement and optimization. 
    # As it is improved, the algorithm cross-over factor of (0.20) can be increased.
    # In a real production code we would do more to better flesh out this handoff between alogorithms.
    # I ran out of large input files to test on and didn't reveal where a basic, square meter-wise 2d array Breadth-First-
    # Search algorithm would be faster. I ultimately took an educated guess of 0.20.

    # TODO 
    # Write a script to generate larger input files to test on. An input file of 100 barren lands is too easy 
    # and Novel_BLA_Method() operates in constant time relative to the grid size. 
    # Add these new test input files into the "tests/" folder and the answers into the test_BLA.sh script.

    factor = len(list_of_barren_lands) / sqrt(GRID_MAX_X * GRID_MAX_Y)

    if (factor < 0.20):
        Novel_BLA_Method(GRID_MAX_X, GRID_MAX_Y, list_of_barren_lands)
    else:
        Basic_Breadth_First_Search_Method(GRID_MAX_X, GRID_MAX_Y, list_of_barren_lands)

main()
