$(document).ready(function(){
            $('.summary').click(function(){
                var addressValue = $(this).attr("href");
                var a = reverse('librehatti.suspense.views.summary_page', function(url) {
                                var request_url = url + "?" + addressValue;
                                $.ajax({
                                    url: request_url,
                                    success: function(data){

                                        BootstrapDialog.show({
                    title: '<b>Suspense Summary</b>',
                    message: data,

                    buttons: [{
                        icon: 'glyphicon glyphicon-ok',
                        cssClass: 'btn btn-success',
                        label: ' Ok',
                        action: function(dialogItself){
                            dialogItself.close();
                        }
                    }]
                })
                                    }
                                })
                            });
return false;
})
});
