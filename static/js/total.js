$(document).on("input", ".new_value", function() {

    var previous_total = document.getElementById('previous_total').value;

    var new_value = 0;
    $(".new_value").each(function(){
        new_value += +$(this).val();
        var id = (this).id;
        var previous_id = 'previous_' + id;
        var previous_value = document.getElementById(previous_id).value;
        var temp = document.getElementById(id).value;
        if (temp){
            previous_total = previous_total - previous_value
        }
    });

    var new_sum = previous_total + new_value;

    $("#new_total").val(new_sum);
});
