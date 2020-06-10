import scipy.spatial
import numpy
import PIL.Image
import PIL.ImageDraw

# Change to desired values
width_px = 1920
height_px = 1080
sample_file = "sample.png"
result_file = "result.png"
triangle_frequency = 800
resample_filter = PIL.Image.BILINEAR

# Generate random 2D coordinates with range 0 to 1 and scale/translate them
points = numpy.random.rand(triangle_frequency, 2)
points[:,0] = points[:,0] * width_px * 4 - width_px
points[:,1] = points[:,1] * height_px * 4 - height_px

# Run the Delaunay algorithm on the points to create triangles
delaunay = scipy.spatial.Delaunay(points)
triangles = delaunay.points[delaunay.simplices]

# Create image object for resulting image
result = PIL.Image.new("RGB", (width_px * 2, height_px * 2))
draw = PIL.ImageDraw.Draw(result)

# Open sample file to sample colors from it
sample = PIL.Image.open(sample_file)
sample_pixels = sample.load()

# Calculate scale between the sample and the result
x_scale = sample.size[0] / result.size[0]
y_scale = sample.size[1] / result.size[1]

# Append all triangles to image object
for triangle in triangles:
    points = []
    for point in triangle:
        for number in point:
            points.append(number)
    center_x = sum(points[0::2]) / (len(points) / 2) * x_scale
    center_y = sum(points[1::2]) / (len(points) / 2) * y_scale
    if (center_x < 0):
        center_x = 0
    if (center_y < 0):
        center_y = 0
    if (center_x >= sample.size[0]):
        center_x = sample.size[0] - 1
    if (center_y >= sample.size[1]):
        center_y = sample.size[1] - 1
    color = sample_pixels[center_x, center_y]
    draw.polygon(points, fill=color)

# Downsize the image to the desired size and apply sample filter for anti-aliasing
result = result.resize((width_px, height_px), resample=resample_filter)

# Save file to the desired path
result.save(result_file)