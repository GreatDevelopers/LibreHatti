$(document).ready(function(){
    $('.quotedistance').change(function(event){
        var quoted_order_no = document.getElementById('quoteorder').value;
        var distance = document.getElementById('quotedistance').value;
        reverse('librehatti.suspense.views.quoted_save_distance', function(url) {
            var request_url = url + "/?quoted_order_id=" + quoted_order_no + "&distance=" + distance;
            $.ajax({
                url: request_url,
                success: function(data){
                }
            });
        });
    });
})