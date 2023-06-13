$(function() {
    $(".select2category").select2({
        theme: "bootstrap-5",
        width: "style",
        placeholder: "Select Category",
        allowClear: true,

        templateResult: formatState,
        templateSelection: formatState,
        escapeMarkup: (x => x)  // Don't escape
    });
})

function formatState (state) {
    if (!state.id) {
        return state.text;
    }

    let $element = $(state.element);
    let color = $element.data('color')
    let colorIsLight = $element.data('color_is_light') === "True";

    return '<span class="badge rounded-pill category-badge' + (colorIsLight ? ' text-dark' : '') + '" style="background-color:' + color + ';">' + state.text + '</span>';
}
