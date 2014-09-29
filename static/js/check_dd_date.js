$(document).ready(function(){
    $('.check_dd_number').hide();
    $('.check_dd_date').hide();
    $("label[for='id_check_dd_number']").hide();
    $("label[for='id_check_dd_date']").hide();
    $('.mode_of_payment').change(function(){
    mode_of_payment_id = $(this).val();
    if(mode_of_payment_id != 1 && mode_of_payment_id !=0){
         $('.check_dd_number').show();
         $('.check_dd_date').show();
         $("label[for='id_check_dd_number']").show();
         $("label[for='id_check_dd_date']").show();
        }
    else{
         $('.check_dd_number').hide();
         $('.check_dd_date').hide();
         $("label[for='id_check_dd_number']").hide();
         $("label[for='id_check_dd_date']").hide();
        }
    })
    
});