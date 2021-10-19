# StarTrails and Keogram

Python script to take in a night's JPGs of the night sky and construct a synthetic all-night
exposure showing startrails, and a keogram. 

Startrails method: Stacked image, using numpy to find the night's maximum
value for each pixel.

Keogram method: Use numpy to extract the middle column from each JPG; construct a new image stitching all the middle columns into an array.
