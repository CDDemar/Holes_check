# Holes_check
University Project, in which given a set of points the script must categorize them into holes. Each point represents a snapshot of a car on the road.

# Params:
- #### R: Radius.
- #### S: Magnitude Value for discriminating the normalized acceleration of each point.

# Classes:
- ## Point:
     - #### ID: The point id.
     - #### Trip_ID: The trip id.
     - #### Time Stamp: the time in which the point was snapshoted.
     - #### Lat: The latitude of the point.
     - #### Lng: The longitude of the point.
     - #### Alt: The altitude of the point.
     - #### Speed: The speed of the point.
     - #### Ace: The acceletarion of the point.
     - #### Processed: Indicates if the point has being processed by the script.
- ## Trip:
     - #### ID: The trip id.
     - #### points[]: Set of points created by the trip.
     - #### distance: The distance realized by the trip.
