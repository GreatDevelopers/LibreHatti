$(document).ready(function(){
    $('.price_per_unit').attr('readonly', 'readonly');
    $('#id_buyer_text').blur(function(){
        field_id = this.id.split("-")[1]
        item_id = $(this).val();
        buyer_id = $("#id_buyer").val();
        reverse('librehatti.programmeletter.views.programmerletter_details', function(url) {
            var request_url = url + "/?item_id=" + buyer_id;
            $.ajax({
                url: request_url,
                success: function(data){
                   if (data != 'fail'){
                    divide_data = data.split("&");
                    alert(data);
                    $("#id_contact_person").val(divide_data[0]);
                    $("#id_contact_number").val(divide_data[1]);
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').attr('readonly','readonly');
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').val(data);
                }
                else if(data == 'fail'){
                    $("#id_contact_person").val(divide_data[0]);
                    $("#id_contact_number").val(divide_data[1]);
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').removeAttr('readonly');
                    $('#id_purchaseditem_set-' + field_id +'-price_per_unit').val('0');
                }
                }
            })
        });
    })


    $('.item').click(function(){
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
