function searchbarFilter() {
    // By default, the search query only gets applied to the faq question. If the
    // query also contains hashtags (#Category), those words only get applied to
    // the faq category.
    const queryString = $("#searchbar").val().toLowerCase();

    let questionQuery = queryString.split(" ").filter(v => !v.startsWith("#")).join(" ");
    let categoryQuery = queryString.split(" ").filter(v => v.startsWith("#")).map(v => v.slice(1)).join(" ");

    $("#faq-list > a").each(function (_, node) {
        const question = node.getAttribute("data-faq").toLowerCase();
        const category = node.getAttribute("data-category").toLowerCase();

        const shouldDisplay = (question.indexOf(questionQuery) !== -1) && (category.indexOf(categoryQuery) !== -1);

        node.style.display = shouldDisplay ? "" : "none";
    });
}
