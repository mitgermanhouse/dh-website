$(function() {
  let recipeContainers = (".recipe-container");
  $("tr.quantity > td.unit, tr.quantity > td.magnitude", recipeContainers).click(function() {
    let row = $(this).parent();
    let currentIndex = row.data("index");
    let quantities = row.data("quantities") ;
    
    if (quantities.length == 0) return;
    if (currentIndex === undefined) {
      // Set the initial index
      if (quantities.length > 1) {
        let initialUnit = $(".unit", row).text();
        if (quantities[0][1] == initialUnit) {
          currentIndex = 0;
        } else {
          currentIndex = -1;
        }
      }
    }

    let newIndex = (currentIndex + 1) % quantities.length;
    row.data("index", newIndex);

    $(".magnitude", row).text(quantities[newIndex][0]);
    $(".unit", row).text(quantities[newIndex][1]);
  });
});