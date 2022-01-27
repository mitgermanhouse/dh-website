function searchbarFilter() {
    var recipes = $("#recipe-list a");
    var filter = $("#searchbar").val().toUpperCase();

    for (let i = 0; i < recipes.length; i++) {
        let recipe = recipes[i];

        if (recipe.id.toUpperCase().indexOf(filter) > -1) {
            recipe.style.display = "";
        } else {
            recipe.style.display = "none";
        }
    }
}
