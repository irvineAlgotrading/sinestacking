# for calculating the change in diameters of aluminum and stainless shrink fits

import math

# Coefficients of thermal expansion (in per degree Celsius)
alpha_aluminum = 23e-6  # For aluminum 6061-T6
alpha_steel = 16e-6     # For 316 stainless steel

# Temperature changes (in Celsius)
delta_T_aluminum = -196 - 20  # Aluminum cooled to liquid nitrogen temperature from room temperature
delta_T_steel = 200 - 20      # 316 heated to 200 degrees Celsius from room temperature

# Original diameters (in inches)
diameter_aluminum = 1.102  # Diameter of aluminum puck
diameter_steel = 1.100    # Diameter of steel hole

# Calculating the change in diameter for both materials
delta_diameter_aluminum = diameter_aluminum * alpha_aluminum * delta_T_aluminum
delta_diameter_steel = diameter_steel * alpha_steel * delta_T_steel

# Calculating new diameters after temperature changes
new_diameter_aluminum = diameter_aluminum + delta_diameter_aluminum
new_diameter_steel = diameter_steel + delta_diameter_steel

# Printing results
print(f"Change in diameter of aluminum: {delta_diameter_aluminum} inches")
print(f"New diameter of aluminum: {new_diameter_aluminum} inches")
print(f"Change in diameter of steel: {delta_diameter_steel} inches")
print(f"New diameter of steel: {new_diameter_steel} inches")
print(f"----")
# print(f("starting fit: (diameter_steel)"))
# print(f("starting fit: (diameter_steel)"))