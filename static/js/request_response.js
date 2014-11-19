$(document).ready(function(){
    $('.accept_request').click(function(){
        var id = $(this).attr("href");
        accept_request_url = '/catalog/accept_request/?id=' + id;
        reject_request_url = '/catalog/reject_request/?id=' + id;
        BootstrapDialog.show({
            title: '<b>Request Response</b>',
            message: 'Are you want to accept this request?',
            buttons: [{
                icon: 'glyphicon glyphicon-ok',
                cssClass: 'btn btn-success',
                label: ' Yes',
                action: function(dialogItself){
                    dialogItself.close();
                    $.ajax({
                        url: accept_request_url,
                        success: function(data){
                            location.reload();
                        }
                    })
                }
            },
            {
                icon: 'glyphicon glyphicon-remove',
                cssClass: 'btn btn-danger',
                label: ' No',
                action: function(dialogItself){
                    dialogItself.close();
                    $.ajax({
                        url: reject_request_url,
                        success: function(data){
                            location.reload();
                        }
                    })
                }
            }]
        })
        return false;
    })
    });