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

dpi = settings["ark_dpi"]
width_px = mmToPixels(settings["ark_bredde_i_mm"])
height_px = mmToPixels(settings["ark_hoyde_i_mm"])

paper_margin_px = mmToPixels(settings["rutenett_marg_i_mm"])
inner_width_px = width_px - 2 * paper_margin_px
inner_height_px = height_px - 2 * paper_margin_px

dots_distance_px = mmToPixels(settings["prikker_avstand_i_mm"])
dots_diameter_px = mmToPixels(settings["prikker_diameter_i_mm"])

array_nr_of_dots_x = inner_width_px // dots_distance_px + 1
array_nr_of_dots_y = inner_height_px // dots_distance_px + 1

if settings["rutenett_sentrert"]:
	array_x0_px = paper_margin_px + (inner_width_px - ((array_nr_of_dots_x - 1) * dots_distance_px)) // 2
	array_y0_px = paper_margin_px + (inner_height_px - ((array_nr_of_dots_y - 1) * dots_distance_px)) // 2
else:
	array_x0_px = paper_margin_px
	array_y0_px = paper_margin_px



# Lager selve bildet:

img = np.full((height_px, width_px, 1), 255, np.uint8)




# Tegner prikkene i rutenettet:
for i in range(array_nr_of_dots_x):
	for j in range(array_nr_of_dots_y):
		cv2.circle(img, (array_x0_px + i * dots_distance_px, array_y0_px + j * dots_distance_px), 0, (0), dots_diameter_px)




# Lagrer bildet som png:

cv2.imwrite(settings["filbane_png"], img)




# Lagrer bildet som pdf:

image1 = Image.open(settings["filbane_png"])
im1 = image1.convert("RGB")
im1.save(settings["filbane_pdf"], format="PDF", resolution=dpi)
print(f"Lagret prikkefil som {settings['filbane_pdf']}")



# Forhåndsviser bildet:

if False:
	preview_scale = 800 / height_px
	cv2.namedWindow("Prikker", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Prikker", int(width_px*preview_scale), int(height_px*preview_scale))
	cv2.imshow("Prikker", img)
	cv2.waitKey(0)
