function searchbarFilter() {
    var recipeList = document.getElementById("recipe-list");
    var recipes = recipeList.getElementsByTagName("a");
    var filter = document.getElementById("searchbar").value.toUpperCase();

    for (let i = 0; i < recipes.length; i++) {
        let recipe = recipes[i];

        if (recipe.id.toUpperCase().indexOf(filter) > -1) {
            recipe.style.display = "";
        } else {
            recipe.style.display = "none";
        }
    }
}
