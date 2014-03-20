$(document).on("ready",function() {
//################################################################
//Set up datepicker.
$("#dateField").datepicker();

$("#dateField").on("change",function(){
 var date = $(this).val();
 window.location.href = "/blueBus/"+date;
});

$(".showHiddenElementButton").on("click", function() { 
 $(".hiddenElement").show();
 $(this).remove()
});

//################################################################
});
