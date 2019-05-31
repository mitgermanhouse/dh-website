var numIngredients;

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
    numIngredients++;
    var html= `<div id="div_` + numIngredients.toString() + `" class="ing_div">
                    <div class="row">
                        <div class="col-sm-2">
                            <div style="margin: 15px; text-align: right">
                                <label for='ingredient_` + numIngredients.toString() + `'>Ingredient:</label>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <input class="form-control" type="text" id="ingredient_` + numIngredients.toString() + `"
                                   name="ingredient" required>
                        </div>
                        <div class="col-sm-2">
                            <div style="margin: 15px; text-align: right">
                                <label for='quantity_` + numIngredients.toString() + `'>Quantity:</label>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <input class="form-control" type="number" id="quantity_` + numIngredients.toString() + `"
                                   name="quantity" required>
                        </div>
                        <div class="col-sm-1">
                            <div style="margin: 15px; text-align: right">
                                <label for='units_` + numIngredients.toString() + `'>Unit:</label>
                            </div>
                        </div>
                        <div class="col-sm-2">
                            <input class="form-control" type="text" id="units_` + numIngredients.toString() + `"
                                   name="units" required>
                        </div>
                        <div class="col-sm-1">
                            <label for="div_` + numIngredients.toString() + `" class="remove"> &#x2717 </label>
                        </div>
                    </div>
                </div>`;
    $(html).appendTo(document.getElementById("ingredient_list"));
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


$(document).ready(function() {
    numIngredients = $('.ing_div').length;

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

