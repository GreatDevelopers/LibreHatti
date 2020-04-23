$(document).ready(function(){
    $('.add_another').click(function(){
        BootstrapDialog.show({
            title: '<b>Add Note Line</b>',
            message: '<input id="new_note_id" name="new_note" type="text" />',
            buttons: [{
                icon: 'glyphicon glyphicon-ok',
                cssClass: 'btn btn-success',
                label: ' ADD',
                action: function(dialogItself){
                  var note_line = document.getElementById('new_note_id').value;
                  dialogItself.close();
                  reverse('librehatti.bills.views.new_note_line', function(url) {
                    var request_url = url + "/?note_line=" + note_line;
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
    $('.delete_selected').click(function(){
        BootstrapDialog.show({
            title: '<b>Are you sure?</b>',
            message: 'Are you want to accept this request?',
            buttons: [{
                icon: 'glyphicon glyphicon-ok',
                cssClass: 'btn btn-success',
                label: ' Yes',
                action: function(dialogItself){
                    var val = [];
                    $('.note_checkbox:checkbox:checked').each(function(i){
                      val[i] = $(this).val();
                  });
                    dialogItself.close();
                    reverse('librehatti.bills.views.delete_note', function(url) {
                        var request_url = url + "/?delete_note=" + val;
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
                }
            }]
        })
return false;
})
});
