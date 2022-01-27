function addIngredient(button) {
    $("#ingredient-list").append($("#template-ingredient").html());
}

function deleteIngredient(button) {
    if ($(".remove-button").length > 1) {
        $(button).closest(".ingredient-col").remove();
    }
}