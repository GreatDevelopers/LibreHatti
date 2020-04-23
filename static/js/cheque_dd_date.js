$(document).ready(function(){

    $('.control-group.form-row.field-cheque_dd_number ').hide();
    $('.control-group.form-row.field-cheque_dd_date ').hide();
    $('.control-group.form-row.field-mode_of_payment ').change(function(){
    mode_of_payment_id = $('#id_mode_of_payment').val();
    if(mode_of_payment_id != 1 && mode_of_payment_id !=0 && mode_of_payment_id !=4){
         $('.control-group.form-row.field-cheque_dd_number ').show();
         $('.control-group.form-row.field-cheque_dd_date ').show();
        }
    else{
        $('.control-group.form-row.field-cheque_dd_number ').hide();
        $('.control-group.form-row.field-cheque_dd_date ').hide();
    }
    });

});
