// Simply remove recently typed input in the input field 
// So on next page reload, it displays randomly picked food recipe
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}
// Disabled Submit button if the input field is empty
document.querySelector("#food_name").onkeyup = function(){
    if (document.querySelector("#food_name").value === ''){
        document.querySelector("#submit").disabled = true;
    }else{
        document.querySelector("#submit").disabled = false;
        document.querySelector("#submit").style.cursor = 'pointer';
    }
}
// Animate the preptime minutes using jquery 


$('.count').prop('Counter',0).animate({
    Counter: $('.count').text()
}, {
    duration: 1000,
    easing: 'swing',
    step: function (now) {
        $(this).text(Math.ceil(now));
    }
});

// Suggest users as they type in food name after 4 characters
// Based on fetch food names from spoonacular API
$SCRIPT_ROOT = window.location.href ;
food_items = [];

$(function() {
    $('#food_name').bind('keyup', function() {
        if ($('#food_name').val().length == 4){
            $.getJSON($SCRIPT_ROOT + '/food_list', {
                a: $('#food_name').val(),
            }, function(data) {
                food_items = data.response;
                $("#food_name").autocomplete({
                    source: food_items,
                });
            });
        }
        return false;
    });
});