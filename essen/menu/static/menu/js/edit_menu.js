// Load select options once and store as a global variable
$(function() {
    let selectOptions = $("#template-recipe-select-options").html();
    window._selectOptions = selectOptions;
});

function makeSelectpicker(element) {
    let select = $(element);

    select.html(window._selectOptions);
    select.selectpicker("val", select.data("selection").toString());
}

function addRecipe(button) {
    let template = $("#template-recipe-select").html();
    let recipeNode = $(template);
    $(".recipe-select", recipeNode).each(function() {
        makeSelectpicker(this);
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
        makeSelectpicker(this);
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
        makeSelectpicker(this);
    });
});