

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

// function filter() {
//
//     var bar = document.getElementById("searchbar");
//     var contents = bar.value.toLowerCase();
//     if (contents != "") {
//         for (var recipe in recipeIng) {
//             ingList = recipeIng[recipe];
//
//             var containsIng = false;
//             for (var i = 0; i < ingList.length; i++) {
//                 if (ingList[i].toLowerCase().includes(contents)) {
//                     containsIng = true;
//                     console.log("hi!");
//                     break;
//                 }
//             }
//
//             if (recipe.toLowerCase().includes(contents) || containsIng) {
//                 document.getElementById(recipe).style.display = "block";
//             } else {
//                 document.getElementById(recipe).style.display = "none";
//             }
//
//         }
//     }
// }





