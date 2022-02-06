function searchbarFilter() {
    // By default, the search query only gets applied to the recipe name. If the
    // query also contains hashtags (#Category), those words only get applied to
    // the recipe category.
    const queryString = $("#searchbar").val().toLowerCase();

    let nameQuery = queryString.split(" ").filter(v => !v.startsWith("#")).join(" ");
    let categoryQuery = queryString.split(" ").filter(v => v.startsWith("#")).map(v => v.slice(1)).join(" ");

    $("#recipe-list > a").each(function (_, node) {
        const name = node.getAttribute("data-recipe").toLowerCase();
        const category = node.getAttribute("data-category").toLowerCase();

        const shouldDisplay = (name.indexOf(nameQuery) !== -1) && (category.indexOf(categoryQuery) !== -1);

        node.style.display = shouldDisplay ? "" : "none";
    });
}
