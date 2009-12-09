$(document).ready(function() {

    $(function(){
      $('#epiclock').epiclock({offset: {seconds: SERVER_OFFSET}});
      $.epiclock();
   });

});
