import json

from django import template

from recipes.units import units

register = template.Library()


@register.simple_tag
def data_quantities_str(**kwargs):
    if "ingredient" in kwargs:
        quantity = kwargs["ingredient"]._p_quantity
    elif "quantity" in kwargs:
        quantity = kwargs["quantity"]
    else:
        raise ValueError("Invalid kwargs for data_quantities_str tag.")

    quantities = [quantity.to(u) for u in units.all_dh_units if quantity.check(u)]
    quantities = [q for q in quantities if q.m >= 0.1 and q.m <= 100]

    return json.dumps([[q.magnitude_str, q.unit_str] for q in quantities])
