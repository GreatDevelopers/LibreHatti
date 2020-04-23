$(document).ready(function(){
    $('#save_register_button').click(function(){
        var addressValue = $(this).attr("href");
        reverse('librehatti.reports.views.save_fields', function(url) {
            var request_url = url + "/?" + addressValue;
            $.ajax({
                url: request_url,
                success: function(data){
                    if (data == 0){
                       BootstrapDialog.show({
                        title: '<b>Error</b>',
                        message: 'You should enter a Title for this register',
                        buttons: [{
                            icon: 'glyphicon glyphicon-remove',
                            cssClass: 'btn btn-danger',
                            label: ' Close',
                            action: function(dialogItself){
                                dialogItself.close();
                            }
                        }]
                    });

                   }

                   else if (data == 1){
                       BootstrapDialog.show({
                        title: '<b>Great</b>',
                        message: 'Register Saved Successfully',
                        buttons: [{
                            icon: 'glyphicon glyphicon-ok',
                            cssClass: 'btn btn-info btn-large',
                            label: ' Close',
                            action: function(dialogItself){
                                dialogItself.close();
                                location.reload();
                            }
                        }]
                    });
                   }
               }

           })
});
return false;
})
});
