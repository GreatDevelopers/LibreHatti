//Filtering choices for selecting items to be purchased

$(document).ready(function(){
    
    $('.sub_category').attr('disabled', 'disabled');
    $('.parent_category').attr('disabled', 'disabled');
    $('.item').attr('disabled', 'disabled');
    
    $('.type').change(function(){
        parent_category_id = this.id.split("-")[1]
        $('#id_purchaseditem_set-' + parent_category_id +'-parent_category').empty();
        $('#id_purchaseditem_set-' + parent_category_id +'-parent_category').removeAttr('disabled');
        type_id = $(this).val();
        reverse('librehatti.catalog.views.select_type', function(url) {
            var request_url = url + "/?type_id=" + type_id;
            $.ajax({
                url: request_url,
                datatype:'json',
                success: function(data){
                    $.each(JSON.parse(data), function(key, value){
                     $('.parent_category').append('<option value="' + key + '">' + value +'</option>').innerHTML;
                 });
                }
            })
        });
    })

    $('.parent_category').click(function(){
        sub_category_id = this.id.split("-")[1]
        $('#id_purchaseditem_set-' + sub_category_id +'-sub_category').empty();
        $('#id_purchaseditem_set-' + sub_category_id +'-sub_category').removeAttr('disabled');
        parent_category_id = $(this).val();
        reverse('librehatti.catalog.views.select_sub_category', function(url) {
            var request_url = url + "/?cat_id=" + parent_category_id;
            $.ajax({
                url: request_url,
                datatype:'json',
                success: function(data){
                    $.each(JSON.parse(data), function(key, value){
                     $('.sub_category').append('<option value="' + key + '">' + value +'</option>').innerHTML;
                 });
                }
            })
        });
    })
    
    $('.sub_category').click(function(){
        item_id = this.id.split("-")[1]
        $('#id_purchaseditem_set-'+ item_id + '-item').empty();
        $('#id_purchaseditem_set-'+ item_id + '-item').removeAttr('disabled');
        sub_category_id = $(this).val();
        reverse('librehatti.catalog.views.select_item', function(url) {
            var request_url = url + "/?cat_id=" + sub_category_id;
            $.ajax({
                url: request_url,
                datatype:'json',
                success: function(data){  
                    $.each(JSON.parse(data), function(key, value){
                     $('.item').append('<option value="' + key + '">' + value +'</option>').html();
                 });
                }
            })
        });
    })
});

