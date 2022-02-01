function addIngredient(button) {
    $("#ingredient-list").append($("#template-ingredient").html());
}

function deleteIngredient(button) {
    if ($(".remove-button").length > 1) {
        $(button).closest(".ingredient-col").remove();
    }
}

$(function() {
    $(".select2category").select2({
        theme: "bootstrap-5",
        width: "style",
        placeholder: "Select Category",
        allowClear: true,

        templateResult: formatState,
        templateSelection: formatState,
    });
})

function formatState (state) {
    if (!state.id) {
        return state.text;
    }

    let $element = $(state.element);
    let color = $element.data('color')
    let colorIsLight = $element.data('color_is_light') === "True";

    let badge = '<span class="badge rounded-pill category-badge' + (colorIsLight ? ' text-dark' : '') + '" style="background-color:' + color + ';">' + state.text + '</span>';
    return jQuery.parseHTML(badge);
}