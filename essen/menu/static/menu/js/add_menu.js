
var meal_id = 0;
var recipe_id = 0;

function addItem(caller) {
    var num = caller.id.split("_")[2];
    var form = document.getElementById("body_" + num);

    var form_group = document.createElement("div");
    form_group.setAttribute("class", "form-group");
    form_group.setAttribute("id", "form_group_" + recipe_id);

    var div = document.createElement("div");
    div.setAttribute("class", "col-sm-7");

    var new_element = document.createElement("input");
    new_element.setAttribute("list", "recipe_choices");
    new_element.setAttribute("class", "form-control");
    new_element.required = true;
    new_element.name = "item_" + num;
    new_element.id = "item_" + recipe_id;

    var lbl = document.createElement("label");
    lbl.setAttribute("class", "remove");
    lbl.setAttribute("for", "form_group_" + recipe_id);
    lbl.innerHTML = " x";

    div.appendChild(new_element);
    form_group.appendChild(div);
    form_group.appendChild(lbl);

    form.insertBefore(form_group, caller);

    recipe_id += 1;
}

$(document).ready(function() {
    $(document).on('click', '.add_day_menu_button', function(event) {
        addItem(event.target);
    });

    $(document).on('click', '.remove', function(event) {
        target = event.target.htmlFor.split("_");
        if (target[0] == 'form') {
            num = target[target.length - 1];
            var recipe_box = document.getElementById("form_group_" + num);
            recipe_box.parentNode.removeChild(recipe_box);
            $('label[for="' + "item_" + num +'"]').remove();
        } else if (target[0] == 'meal') {
            num = target[target.length - 1];
            var meal = document.getElementById("meal_" + num);
            meal.parentNode.removeChild(meal);
//            $('label[for="' + "day_" + target[1] +'"]').remove();
        }

    });
});

function validateDate() {
    date_input = document.getElementById("start_date");

    var day = new Date(date_input.value).getDay();
    console.log(day);
    if (day != 6) {
        alert("The Menu start date must be a Sunday.");
        return false;
    }
    return true;
}

function validateForm() {
    return validateDate();

}

function addDayMenu() {
    var container = document.createElement("div");
    container.setAttribute("id", "meal_" + meal_id);
    container.setAttribute("class", "panel panel-default");
    $("#edit_form").append(container);

    // heading
    var choose_day = document.createElement("div");
    choose_day.setAttribute("id", "choose_day");
    choose_day.setAttribute("class", "panel-heading h5");
    $('<label>', {for: "day_" + meal_id, text: "Meals for:"}).appendTo(choose_day);
    var selector = document.getElementById("day_selector").cloneNode(true);
    selector.setAttribute('id', 'day_' + meal_id);
    selector.setAttribute('name', 'day_' + meal_id);
    selector.style.visibility = "visible";
    selector.setAttribute("class", "btn");
    $(selector).appendTo(choose_day);
    $('<label>', {for: "meal_" + meal_id, class: "remove", text: " x"}).appendTo(choose_day);
    container.appendChild(choose_day);

    // body
    var body = document.createElement("div");
    body.setAttribute("id", "body_" + meal_id);
    body.setAttribute("class", "panel-body form-group");
    var addButton = $('<button>', {class: "add_day_menu_button btn btn-primary",
        id: 'add_button_' + meal_id, text: "Add another recipe", onclick: "addItem()", type:"button"});
    addButton.appendTo(body);
    container.appendChild(body);

    for (i = 0; i<3; i++) {
        addItem(document.getElementById('add_button_' + meal_id));
    }

    recipe_id += 3;
    meal_id += 1;
}
