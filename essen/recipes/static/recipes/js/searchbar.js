function searchbarFilter() {
    var filter = $("#searchbar").val().toUpperCase();

    $("#recipe-list > a").each(function (_, recipe) {
        if (recipe.getAttribute("data-recipe").toUpperCase().indexOf(filter) > -1) {
            recipe.style.display = "";
        } else {
            recipe.style.display = "none";
        }
    });
}
