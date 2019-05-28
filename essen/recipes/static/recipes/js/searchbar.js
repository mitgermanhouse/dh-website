

function btnpress(caller) {
    var recipe_btn = document.getElementById("recipe_search");
    var ingredient_btn = document.getElementById("ingredient_search");
    recipe_btn.setAttribute("class", "btn btn-primary");
    ingredient_btn.setAttribute("class", "btn btn-primary");

    caller.setAttribute("class", "btn btn-primary active");

    var search = document.getElementById("query");
    search.setAttribute("value", caller.id);

}

$(document).ready(function() {
    $(document).on('click', '.btn', function (event) {
        btnpress(event.target);
    });
});

function setActive() {
    var active_btn = document.getElementById(document.getElementById("query").value);
    active_btn.setAttribute("class", "btn btn-primary active")
}

