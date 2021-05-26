# StarTrails

Python script to take in a night's JPGs of the night sky and construct a synthetic all-night
exposure showing startrails. Method: Stacked image, using numpy to find the night's maximum
value for each pixel. Tricky part: Filtering out clouds, which are so illuminated by city lights
that they dominate the result. Work in progress.
