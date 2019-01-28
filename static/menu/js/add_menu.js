
var menu_id = 0;
var recipe_id = 0;

function addItem(caller) {
    var num = caller.id.split("_")[2];
    var form = document.getElementById("day_menu_" + num);

    var div = document.createElement("div");
    div.setAttribute("class", "recipe_div")

    var new_element = document.createElement("input");
    new_element.setAttribute("list", "recipe_choices");
    new_element.name = "item_" + num;
    new_element.id = "item_" + recipe_id;

    var lbl = document.createElement("label");
    lbl.setAttribute("class", 'remove');
    lbl.setAttribute("for", "item_" + recipe_id);
    lbl.innerHTML = " &#x2717";

    div.appendChild(new_element);
    div.appendChild(lbl);

    form.insertBefore(div, caller);

    recipe_id += 1;
}

$(document).ready(function() {
    $(document).on('click', '.add_day_menu_button', function(event) {
        addItem(event.target);
    });

    $(document).on('click', '.remove', function(event) {
        target = event.target.htmlFor.split("_");
        if (target[0] == 'item') {
            num = target[target.length - 1];
            var recipe_box = document.getElementById("item_" + num);
            recipe_box.parentNode.removeChild(recipe_box);
            $('label[for="' + "item_" + num +'"]').remove();
        } else if (target[0] == 'day') {
            num = target[target.length - 1];
            var day_menu = document.getElementById("day_menu_" + num);
            day_menu.parentNode.removeChild(day_menu);
//            $('label[for="' + "day_" + target[1] +'"]').remove();
        }

    });
});


function addDayMenu() {
    var form = document.getElementById("edit_form");

//    var template = document.getElementById("day_menu_template");
//    var clone = template.cloneNode([true]);
//    clone.hidden = false;
//    clone.id = "day_menu_" + parseInt(menu_id);
//
//    add_button = clone.getElementById("add_button");
//    add_button.id = "add_button_" + parseInt(menu_id);
//
    var add_day_menu_button = document.getElementById("add_day_menu");

//    menu_id += 1;
//
//    form.insertBefore(clone, add_day_menu_button);

    var html = `
    <div class = "day_menu" id = "day_menu_` + menu_id + `">
            <div>
            <div class='day_assignment'>
                <label for="day_` + menu_id + `">Meals for: </label>
                <input list='days' id="day_` + parseInt(menu_id) + `" name="day_` + parseInt(menu_id) + `">
                <label for="day_` + parseInt(menu_id) + `" class="remove"> &#x2717 </label>
            </div>
            Recipes:
            </div>
            <div class='recipe_div'>
                <input list="recipe_choices" id="item_` + parseInt(recipe_id) + `" name="item_` + menu_id + `">
                <label for="item_` + parseInt(recipe_id) + `" class="remove"> &#x2717 </label>
            </div>
            <div class='recipe_div'>
                <input list="recipe_choices" id="item_` + parseInt(recipe_id + 1) + `" name="item_` + menu_id + `">
                <label for="item_` + parseInt(recipe_id + 1) + `" class="remove"> &#x2717 </label>
            </div>
            <div class='recipe_div'>
                <input list="recipe_choices" id="item_` + parseInt(recipe_id + 2) + `" name="item_` + menu_id + `">
                <label for="item_` + parseInt(recipe_id + 2) + `" class="remove"> &#x2717 </label>
            </div>
        <button type="button" id="add_button_` + parseInt(menu_id) + `" class="add_day_menu_button">Add Another Recipe</button>
    </div>`

    recipe_id += 3;
    menu_id += 1;

    var $new_menu = $( html);
//    form.insertBefore($new_menu, add_day_menu_button);
    $("#edit_form").append($new_menu);
}

function validateDate() {
    date_input = document.getElementById("start_date");

    var day = new Date(date_input.value).getDay();

    if (day != 0) {
        alert("The Menu start date must be a Sunday.");
    }
}






