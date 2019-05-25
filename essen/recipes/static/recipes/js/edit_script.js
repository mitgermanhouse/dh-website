function validateForm() {
  var inputs = document.forms["edit_form"].getElementsByTagName("input");
  var i;
  for (i=0; i<inputs.length; i++) {
      if (inputs[i].value == "") {
        alert("Please fill out all fields.");
        return false;
      }
    }
}

function addIngredient() {
    var div_len = $('.ing_div').length + 1

    var form = document.getElementById("edit_form");

    var div = document.createElement("div");
    div.setAttribute('class', 'ing_div')
    div.setAttribute('id', 'div_' + div_len)
    var ids = ["Ingredient", "Quantity", "Unit"];
    var i;
    for (i = 0; i < 3; i++) {
        var new_element = document.createElement("input");
        new_element.name = ids[i];
        new_element.id = ids[i] + "_" + div_len;

        var new_label = document.createElement("label");
        new_label.setAttribute('for', ids[i] + "_" + div_len);
        new_label.innerHTML = capitalizeFirstLetter(" " + ids[i] + ":" + " ");

        div.appendChild(new_label);
        div.appendChild(new_element);
    }
    var div_label = document.createElement("label");
    div_label.setAttribute('for', 'div_'+div_len);
    div_label.innerHTML = ' &#x2717 ';
    div_label.setAttribute('class', 'remove');
    div.appendChild(div_label);

    var submit_button = document.getElementById("submit");

    form.insertBefore(div, submit_button);
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


$(document).ready(function() {
    $(document).on('click', '.remove', function(event) {
        target = event.target.htmlFor.split("_");
        if (target[0] == 'div') {
            num = target[target.length - 1];
            var ing = document.getElementById("div_" + num);
            ing.parentNode.removeChild(ing);
            $('label[for="' + "div_" + num +'"]').remove();
        } else if (target[0] == 'lateplate') {
            num = target[target.length - 1];
            var ing = document.getElementById("div_" + num);
            ing.parentNode.removeChild(ing);
        }

    });
});

