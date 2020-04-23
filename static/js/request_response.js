$(document).ready(function(){
    $('.accept_request').click(function(){
        var id = $(this).attr("href");
        BootstrapDialog.show({
            title: '<b>Request Response</b>',
            message: 'Are you want to accept this request?',
            buttons: [{
                icon: 'glyphicon glyphicon-ok',
                cssClass: 'btn btn-success',
                label: ' Yes',
                action: function(dialogItself){
                    dialogItself.close();
                    reverse('librehatti.catalog.request_change.accept_request', function(url) {
                        var request_url = url + "/?id=" + id;
                        $.ajax({
                            url: request_url,
                            success: function(data){
                                location.reload();
                            }
                        })
                    });
                }
            },
            {
                icon: 'glyphicon glyphicon-remove',
                cssClass: 'btn btn-danger',
                label: ' No',
                action: function(dialogItself){
                    dialogItself.close();
                    reverse('librehatti.catalog.request_change.reject_request', function(url) {
                        var request_url = url + "/?id=" + id;
                        $.ajax({
                            url: request_url,
                            success: function(data){
                                location.reload();
                            }
                        })
                    });
                }
            }]
        })
return false;
})
});
