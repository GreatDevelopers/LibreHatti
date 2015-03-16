$(document).ready(function(){
    $("#id_Voucher").change(function(){
    var session = $("#id_Session").val();
    var Voucher = $("#id_Voucher").val();
    reverse('librehatti.Test_Reports.views.Test_Reports_data', function(url) {
    var request_url = url +"?session=" +session+"&&voucher=" +Voucher;
             $.ajax({
                url: request_url,
                success: function(data){
                        var get_data = data.split(":");
                            $("#id_Client").val(get_data[0]+" "+get_data[1]);
                            $("#id_Address").val(get_data[2]);
                            $("#id_Refernce_no").val(get_data[3]);                    
                            $("#id_Testing_Date").val(get_data[4]);                    
                            $("#id_Subject").val(get_data[5]);                    
                            $("#id_City").val(get_data[6]);                    
                }
            })

}); 
})    
});
