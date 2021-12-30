import os
import sys
import math
from typing import Optional, Dict

import pint
from pint import Quantity
from pint.util import UnitsContainer
from pint.definitions import UnitDefinition
from pint.errors import UndefinedUnitError
from pint.unit import Unit

# Load unit registry with DH specific unit definitions
ureg = pint.UnitRegistry()
ureg.load_definitions(os.path.join(os.path.dirname(__file__), 'dh_units.txt'))
Q_ = ureg.Quantity

dimensionless = ureg.parse_units("dimensionless")

# Helper Functions
def load_unit_group(group_name: str) -> list[Unit]:
	group = ureg.get_group(group_name)
	units = [ureg.parse_units(unit_name) for unit_name in group.members]

	# Group units according to their dimensionality
	units_dict = {}
	for unit in units:
		if unit.dimensionality not in units_dict:
			units_dict[unit.dimensionality] = [unit]
		else:
			units_dict[unit.dimensionality].append(unit)

	# Sort units by their conversion factor
	units = [u for sl in [sorted(v) for k, v in units_dict.items()] for u in sl]

	return units

def dh_unit_parser(unit_str: str) -> Optional[Unit]:
	# Remove plural '(s)'. Pint interprets this as  * seconds
	unit_str = unit_str.lower().removesuffix('(s)')

	try:
		return ureg.parse_units(unit_str)
	except UndefinedUnitError as e:
		# TODO: Handle correctly
		print(e)
		return dimensionless
	except ValueError as e:
		# This is the case if the unit is for example "3lb bags" because a unit can't contain a scalar
		print(e)
		return dimensionless

def expand(quantity: Quantity, units: list[Unit]) -> list[Quantity]:
	if quantity.dimensionless:
		return quantity

	value = quantity
	ans = []

	# Filter out incompatible units
	units = filter(lambda u: quantity.check(u), units)
	units = reversed(sorted(units))
	units = list(units)

	for i, unit in enumerate(units):
		v_u = value.to(unit)

		if i == len(units) - 1:
			# The last unit should have increased precision
			rounded_magnitude = round(v_u.m, 2)
			if rounded_magnitude == 0: 
				continue
			component = Q_(rounded_magnitude, unit)
			ans.append(component)
		elif abs(v_u.m) >= 1:
			component = Q_(int(v_u.m), unit)
			ans.append(component)
			value -= component

	return ans

def simplify(quantity: Quantity, units: list[Unit]) -> Quantity:
	if quantity.dimensionless:
		return quantity

	if quantity.m == 0:
		return quantity

	# Filter out incompatible units
	units = filter(lambda u: quantity.check(u), units)
	units = reversed(sorted(units))
	units = list(units)

	def score(q: pint.Quantity) -> float:
		m = abs(q.m)
		s = -abs(math.log(m))  # The closer the value is to 1, the larger the score
		s += (1 / (1 - abs(q.m - round(q.m * 2)/2)))

		return s

	candidates = [quantity.to(u) for u in units]
	return list(reversed(sorted([(score(q), q) for q in candidates])))[0][1]

# # WrapperClass
# def QuantityWrapper:

# 	def __init__(self, magnitude, unit):
# 		self._magnitude = magnitude
# 		self._unit_str  = unit

# 		parsed_unit = dh_unit_parser(self._unit_str)
# 		self._quantity = Q_(self._magnitude, parsed_unit)

# 		self._valid = False
# 		self.invalidate()

# 	def _invalidate(self):
# 		self._valid = False

# 	def _compute_properties(self):
# 		if self._valid:
# 			return

# 		self._simplified_q = simplify(self._quantity, units)

# 	@property
# 	def sm_str(self):
# 		self._compute_properties()
# 		return f"{round(self._simplified_q.m, 2):g}"

# 	@property
# 	def su_str(self):
# 		if self._quantity.u == dimensionless:
# 			return self._unit_str
# 		return f"{self._simplified_q.u:~}"

# Extend Quantity type
#  This is a hack and should be fixed at some point in the future
def magnitude_str(self):
	return f"{round(self.m, 2):.3g}"

def unit_str(self):
	return f"{self.u:~}"

Quantity.magnitude_str = property(magnitude_str)
Quantity.unit_str = property(unit_str)

if __name__ == '__main__':
	pass

# TODO: Refactor	
units = load_unit_group('DH_US_cups')
all_dh_units = load_unit_group('DH_All')

print(all_dh_units)