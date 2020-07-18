import cv2
import numpy as np
from PIL import Image
import yaml


# Henter settings:

with open("settings.yaml", "r") as file:
	settings = yaml.load(file, Loader=yaml.FullLoader)



# Nyttige funksjoner:

def mmToPixels(mm):
	return int(dpi * (mm / 25.4))



# Setter viktige variabler:

width_px = settings["ark_bredde"]
height_px = settings["ark_hoyde"]
dpi = settings["ark_dpi"]

paper_margin_px = mmToPixels(settings["rutenett_marg_i_mm"])
inner_width_px = width_px - 2 * paper_margin_px
inner_height_px = height_px - 2 * paper_margin_px

dots_distance_px = mmToPixels(settings["prikker_avstand_i_mm"])
dots_radius_px = mmToPixels(settings["prikker_radius_i_mm"])
dots_diameter_px = dots_radius_px // 2

array_nr_of_dots_x = inner_width_px // dots_distance_px + 1
array_nr_of_dots_y = inner_height_px // dots_distance_px + 1

if settings["rutenett_sentrert"]:
	print((inner_width_px - ((array_nr_of_dots_x - 1) * dots_distance_px)) // 2)
	array_x0_px = paper_margin_px + (inner_width_px - ((array_nr_of_dots_x - 1) * dots_distance_px)) // 2
	array_y0_px = paper_margin_px + (inner_height_px - ((array_nr_of_dots_y - 1) * dots_distance_px)) // 2
else:
	array_x0_px = paper_margin_px
	array_y0_px = paper_margin_px



# Lager selve bildet:

img = np.full((height_px, width_px, 1), 255, np.uint8)





# Tegner prikkene i rutenettet:
print("Jaa  ", paper_margin_px)
print("Hmmmm", inner_width_px, inner_height_px, dots_distance_px, dots_distance_px)
print("Halla", array_nr_of_dots_x, array_nr_of_dots_y)
for i in range(array_nr_of_dots_x):
	for j in range(array_nr_of_dots_y):
		cv2.circle(img, (array_x0_px + i * dots_distance_px, array_y0_px + j * dots_distance_px), 0, (0), dots_diameter_px)


# cv2.circle(img, (array_nr_of_dots_x + 7 * dots_distance_px, array_nr_of_dots_y + 11 * ), 30, (0), 10)




# Lagrer bildet som png:

cv2.imwrite("prikker.png", img)




# Lagrer bildet som pdf:

image1 = Image.open(r"prikker.png")
im1 = image1.convert("RGB")
im1.save(r"prikker.pdf", resolution=dpi)



# Forhåndsviser bildet:

if False:
	preview_scale = 800 / height_px
	cv2.namedWindow("Prikker", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Prikker", int(width_px*preview_scale), int(height_px*preview_scale))
	cv2.imshow("Prikker", img)
	cv2.waitKey(0)
