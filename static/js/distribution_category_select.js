//Filtering choices for selecting items to be purchased

$(document).ready(function(){
    $('.category').attr('disabled', 'disabled');

    $('.parent_category').change(function(){
        $('.category').empty();
        $('.category').removeAttr('disabled');
        parent_category_id = $(this).val();
        reverse('catalog:select_sub_category', function(url) {
            var request_url = url + "/?cat_id=" + parent_category_id;
            $.ajax({
                url: request_url,
                datatype:'json',
                success: function(data){
                    $.each(JSON.parse(data), function(key, value){
                     $('.category').append('<option value="' + key + '">' + value +'</option>').innerHTML;
                 });
                }
            })
        });
    })
});
