from django import forms

class Select2Widget(forms.Select):
    """
    Includes values from a model instance as data attributes in <option> tags.
    """

    def __init__(self, attrs=None, choices=(), data_values=None):
        super().__init__(attrs, choices)
        self.data_values = data_values

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        data_attrs = {}
        if hasattr(value, 'instance') and self.data_values is not None:
            for attr_name in self.data_values:
                if hasattr(value.instance, attr_name):
                    data_attrs['data-' + attr_name] = str(getattr(value.instance, attr_name))

        index = str(index) if subindex is None else "%s_%s" % (index, subindex)
        if attrs is None:
            attrs = {}
        option_attrs =  self.build_attrs(self.build_attrs(self.attrs, attrs), data_attrs) if self.option_inherits_attrs else data_attrs
        if selected:
            option_attrs.update(self.checked_attribute)
        if 'id' in option_attrs:
            option_attrs['id'] = self.id_for_label(option_attrs['id'], index)
        return {
            'name': name,
            'value': value,
            'label': label,
            'selected': selected,
            'index': index,
            'attrs': option_attrs,
            'type': self.input_type,
            'template_name': self.option_template_name,
            'wrap_label': True,
        }