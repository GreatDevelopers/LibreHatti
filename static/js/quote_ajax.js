//Filtering choices for selecting items to be purchased

$(document).ready(function(){
    $('.sub_category').attr('disabled', 'disabled');
    $('.item').attr('disabled', 'disabled');
    
    $('.parent_category').change(function(){
        sub_category_id = this.id.split("-")[1]
             $('#id_quoteditem_set-' + sub_category_id +'-sub_category').empty();
        $('#id_quoteditem_set-' + sub_category_id +'-sub_category').removeAttr('disabled');
        parent_category_id = $(this).val();
        request_url = '/catalog/select_sub_category/?cat_id=' + parent_category_id ;
        $.ajax({
            url: request_url,
        datatype:'json',
            success: function(data){
                $.each(JSON.parse(data), function(key, value){
                       $('.sub_category').append('<option value="' + key + '">' + value +'</option>').innerHTML;
                });
            }
        })
    })
    
    $('.sub_category').change(function(){
        item_id = this.id.split("-")[1]
            $('#id_quoteditem_set-'+ item_id + '-item').empty();
        $('#id_quoteditem_set-'+ item_id + '-item').removeAttr('disabled');
        sub_category_id = $(this).val();
        request_url = '/catalog/select_item/?cat_id=' + sub_category_id ;
        $.ajax({
            url: request_url,
        datatype:'json',
            success: function(data){  
                $.each(JSON.parse(data), function(key, value){
                       $('.item').append('<option value="' + key + '">' + value +'</option>').html();
                });
            }
        })
    })
});        
        
