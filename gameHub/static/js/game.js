/* global $ */
$(document).ready(function() {
  "use strict";

  $(window).on("message", function(evt) {
    //Note that messages from all origins are accepted

    //Get data from sent message
    var data = evt.originalEvent.data;
    //Create a new list item based on the data
    setInterval(function() {
      var url = "http://localhost:8000/games/3/highscore";
      $("#gameresult").load(url);
    }, 100000000);

    if (data.messageType)
      switch (data.messageType) {
        case "SETTING":
          $("#game_iframe").attr("width", data.options.width);
          $("#game_iframe").attr("height", data.options.height);
          break;
        case "SCORE":
          var posting = $.post( "http://localhost:8000/games/3/3/update", { score: data.score } );

          // Put the results in a div
          posting.done(function( data ) {
            console.log('done')
          });
          break;
        default:
          console.log("Do nothing");
      }
  });
});

// Assign handlers immediately after making the request,
// and remember the jqxhr object for this request
/**var jqxhr = $.post( "example.php", function() {
  alert( "success" );
})
  .done(function() {
    alert( "second success" );
  })
  .fail(function() {
    alert( "error" );
  })
  .always(function() {
    alert( "finished" );
  });
**/
