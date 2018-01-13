/* global $ */
$(document).ready(function() {
  "use strict";

  $(window).on("message", function(evt) {
    //Note that messages from all origins are accepted
    //Game id and user_id from the hidden field to post the data
    var game_update_url = $('#game_update_url').val();
    var game_highscore_url = $('#game_highscore_url').val();
    //Get data from sent message
    var data = evt.originalEvent.data;
    //updates the highscore
    setInterval(function() {
      $("#gameresult").load(game_highscore_url);
    }, 10000);

    if (data.messageType)
      switch (data.messageType) {
        case "SETTING":
          $("#game_iframe").attr("width", data.options.width);
          $("#game_iframe").attr("height", data.options.height);
          break;
        default:
          var posting = $.post( game_update_url, { data: JSON.stringify(data) });
          $.ajaxSetup({
	    beforeSend: function(xhr) {
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	  });
	  // using jQuery - source Django
	  function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
		    var cookie = jQuery.trim(cookies[i]);
		    // Does this cookie string begin with the name we want?
		    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		        break;
		    }
		}
	    }
	    return cookieValue;
	  }
	  var csrftoken = getCookie('csrftoken');
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
