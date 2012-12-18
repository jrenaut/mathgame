$("#addition").click(function() {
  $("#addition-holder").addClass("active");
  $("#subtraction-holder").removeClass("active");
  $("#multiplication-holder").removeClass("active");
  $('#main-content').load('/add');  
});

$("#multiplication").click(function() {
  $("#multiplication-holder").addClass("active");
  $("#subtraction-holder").removeClass("active");
  $("#addition-holder").removeClass("active");
  $('#main-content').load('/multiply');
});

$("#subtraction").click(function() {
  $("#subtraction-holder").addClass("active");
  $("#addition-holder").removeClass("active");
  $("#multiplication-holder").removeClass("active");
  $('#main-content').load('/subtract');
});
