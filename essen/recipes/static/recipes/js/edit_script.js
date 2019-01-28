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
    var form = document.getElementById("edit_form");

    var div = document.createElement("div");
    var ids = ["ingredient", "quantity", "units"];
    var i;
    for (i = 0; i < 3; i++) {
        var new_element = document.createElement("input");
        new_element.name = ids[i];
        new_element.id = ids[i];

        var new_label = document.createElement("label");
        new_label.setAttribute('for', ids[i]);
        new_label.innerHTML = capitalizeFirstLetter(ids[i] + ":");

        div.appendChild(new_label);
        div.appendChild(new_element);
    }
    var submit_button = document.getElementById("submit");

    form.insertBefore(div, submit_button);
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


