$(document).ready(function(){
    $('#save_register_button').click(function(){
        var addressValue = $(this).attr("href");

        request_url = '/save_fields/?' + addressValue;
        $.ajax({
            url: request_url,
            success: function(data){
            if (data == 0){
                alert('You should enter a Title for this register');
            }

            else if (data == 1){
                alert('Register Save Successfully');
                location.reload();
            }
            }
            
        })
        return false;
    })
});