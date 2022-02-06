// Load select options once and store as a global variable
$(function() {
    window._recipesJson = JSON.parse(document.getElementById('recipes-json').textContent);
});

function setUpSelect(element) {

    function formatState(state) {
        if (!state.id) {
            return state.text;
        }

        var badge = '';
        if (state.category != null) {
            badge = '<span class="badge rounded-pill category-badge' + (state.category.color_is_light ? ' text-dark' : '') + '" style="background-color:' + state.category.color + ';">' + state.category.name + '</span>';
        }

        return state.text + ' ' + badge;
    }

    let filterCache = {}
    function filterSearch(query, data) {
        if (query.term === undefined) return data;

        // Get the query -> Use caching to prevent having to re-derive the name
        // and category query.
        const queryString = query.term.toLowerCase();
        let nameQuery, categoryQuery;

        if (filterCache[queryString] !== undefined) {
            nameQuery = filterCache[queryString].nameQuery;
            categoryQuery = filterCache[queryString].categoryQuery;
        } else {
            nameQuery = queryString.split(" ").filter(v => !v.startsWith("#")).join(" ");
            categoryQuery = queryString.split(" ").filter(v => v.startsWith("#")).map(v => v.slice(1)).join(" ");

            filterCache[queryString] = {
                nameQuery: nameQuery,
                categoryQuery: categoryQuery
            }
        }

        // Filter
        if (data.text === undefined || data.text.toLowerCase().indexOf(nameQuery) === -1) return null;
        if (categoryQuery.length > 0 && (data.category === undefined || data.category.name.toLowerCase().indexOf(categoryQuery) === -1)) return null;

        return data;
    }

    let select = $(element);
    select.html("<option></option>");
    select.select2({
        theme: "bootstrap-5",
        width: "style",
        placeholder: "Select Recipe",
        data: window._recipesJson.data,
        matcher: filterSearch,

        templateResult: formatState,
        templateSelection: formatState,
        escapeMarkup: (x => x) // Don't escape -> Significant performance improvement
    });

    let selection = element.getAttribute("data-selected");
    if (selection != null && selection !== "") {
        select.val(selection).trigger("change");
    }
}

function addRecipe(button) {
    let template = $("#template-recipe-select").html();
    let recipeNode = $(template);
    $(".recipe-select", recipeNode).each(function() {
        setUpSelect(this);
    });

    let recipeList = $(button).closest(".meal-container").find(".recipe-list");
    recipeList.append(recipeNode);

    // Update recipe count
    recipeList.children(".meal-recipe-count").val(recipeList.children(".recipe-container").length);
}

function deleteRecipe(button) {
    let recipeList = $(button).closest(".recipe-list")
    let recipes = recipeList.children(".recipe-container");

    if (recipes.length > 1) {
        // Delete recipe and update recipe count
        $(button).closest(".recipe-container").remove();
        recipeList.children(".meal-recipe-count").val(recipeList.children(".recipe-container").length);
    }
}

function addMeal() {
    let template = $("#template-meal").html();
    let mealNode = $(template);
    mealNode.find(".recipe-select").each(function() {
        setUpSelect(this);
    });

    // Set Day / Time
    let lastContainer = $(".meal-container").last();
    let lastContainerDay = lastContainer.find(".day-select").val();
    let lastContainerTime = lastContainer.find(".time-select").val();
    
    if (lastContainerDay != null && lastContainerDay < 6) {
        mealNode.find('.day-select').val(parseInt($(".meal-container").last().find(".day-select").val()) + 1);
        mealNode.find('.time-select').val('DIN');
    }

    $("#meal-list").append(mealNode);
}

function deleteMeal(button) {
    let meals = $("#meal-list").children(".meal-container");
    if (meals.length > 1) {
        $(button).closest(".meal-container").remove();
    }
}

// ----

function updateMealTitle(select) {
    let mealContainer = $(select).closest(".meal-container");

    let day = mealContainer.find(".day-select > option:selected:not(:disabled)").text();
    let time = mealContainer.find(".time-select > option:selected:not(:disabled)").text();

    mealContainer.find(".meal-title").text(day + " " + time);
}

// -------- //

$(function() {
    $(".day-select, .time-select").each(function() {
        let selection = $(this).attr("data-selection");
        if (selection != null && selection != "") {
            $(this).val(selection).change();
        }
    });
});

$(function() {
    $("#start_date_datepicker").datepicker({
        format: "yyyy-mm-dd",
        weekStart: 0,
        maxViewMode: 1,
        todayHighlight: true,
        daysOfWeekDisabled: "1,2,3,4,5,6",
        daysOfWeekHighlighted: "0",
        autoclose: true
    });

    $(".recipe-select").each(function() {
        setUpSelect(this);
    });
});


/*
 * Hacky fix for a bug in select2 with jQuery 3.6.0's new nested-focus "protection"
 * see: https://github.com/select2/select2/issues/5993
 * see: https://github.com/jquery/jquery/issues/4382
 *
 * TODO: Recheck with the select2 GH issue and remove once this is fixed on their side
 */

$(document).on('select2:open', () => {
    document.querySelector('.select2-search__field').focus();
});