/* global $ */

var rate_url = $('#game_rate_url').val();

$(document).ready(function(){
  "use strict";
  
  $(".rating-star").click(function(){
    var x = parseInt(this.id[5]);
    
    $(".rating-star")
      .filter(":lt(" + x + ")")
      .children("p")
      .addClass("star-full");
    $(".rating-star")
      .filter(":gt(" + (x - 1) + ")")
      .children("p")
      .removeClass("star-full");
  });
});