$(document).ready(function(){
    $('.price_per_unit').attr('readonly', 'readonly');
    $('body').on('click','select.item',function(){
        field_id = this.id.split("-")[1]
        item_id = $(this).val();
        reverse('librehatti.catalog.views.price_per_unit', function(url) {
            var request_url = url + "/?item_id=" + item_id;
            $.ajax({
                url: request_url,
                success: function(data){
                   if (data != 'fail'){
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').attr('readonly','readonly');
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').val(data);
                }
                else if(data == 'fail'){
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').removeAttr('readonly');
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').val('0');
                }
                }
            })
        });
    })
});
