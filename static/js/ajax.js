//Filtering choices for selection of materials

$(document).ready(function(){
    $('.lab').change(function(){
        mat_id = this.id.split("-")[1]
            $('#id_purchaseditem_set-' + mat_id +'-material').empty();
        lab_id = $(this).val();
        request_url = '/catalog/select_secondary_category/?cat_id=' + lab_id ;
        $.ajax({
            url: request_url,
        datatype:'json',
            success: function(data){
                $.each(JSON.parse(data), function(key, value){
                       $('.material').append('<option value="' + key + '">' + value +'</option>').innerHTML;
                });
            }
        })
    })
    
    $('.material').change(function(){
        test_id = this.id.split("-")[1]
            $('#id_purchaseditem_set-'+ test_id + '-item').empty();
        material_id = $(this).val();
        request_url = '/catalog/select_item/?cat_id=' + material_id ;
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
        
