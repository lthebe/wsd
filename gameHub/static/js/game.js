/* global $ */
$(document).ready(function() {
  "use strict";

  $(window).on("message", function(evt) {
    //Note that messages from all origins are accepted
    //Game id and user_id from the hidden field to post the data
    var url = $('#game_update_url').val();
    //Get data from sent message
    var data = evt.originalEvent.data;
    //to update the highscore - yet to be done.
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
        default:
          var posting = $.post( url, { data: JSON.stringify(data) });
          posting.done(function( data ) {
            //sends event to the iframe if error or to be load the new data
            if (data.messageType=='LOAD' || data.messageType=='ERROR'){
              var iframe_window = $("#game_iframe")[0].contentWindow;
              iframe_window.postMessage(data, "*");
            }
          });
          break;
      }
  });
});
