/* global $ */

var rate_url = $('#game_rate_url').val();

$(document).ready(function(){
  "use strict";
  
  $(".rating-star").click(function(){
    var r = (parseInt(this.id[5]) + 1) / 2;
    var posting = $.post(rate_url, {rating: r});
    posting.done(function(data){
      var r = parseInt(data);
      $(".rating-star")
        .filter(":lt(" + r + ")")
        .children("span")
        .addClass("star-full");
      $(".rating-star")
        .filter(":gt(" + (r - 1) + ")")
        .children("span")
        .removeClass("star-full");
    });
  });
});