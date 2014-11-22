$(document).ready(function(){
        $('.distance').change(function(event){
            var quoted_order_no = document.getElementById('order').value;
            var distance = document.getElementById('distance').value;
            request_url = "/suspense/quoted_save_distance/?quoted_order_id=" + quoted_order_no + "&distance=" + distance;
            $.ajax({
                url: request_url,
                success: function(data){
                }
            });
        });
    })