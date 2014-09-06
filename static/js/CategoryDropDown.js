$(document).ready(function() {
    //Get the controls where we find the data-extratype attribute
    $("[data-extratype='categorydropdown']").change(function() {
        //Get the changed value
        selected_value = $(this).val();

        //Now get the sub categories and keep doing this
        reverse("librehatti.catalog.views.getsubcat", function(data) {
            $.get(data + "?id=" + selected_value,
                function(data) {
                	try
                	{
                		categories = $.parseJSON(data);
                		alert(categories);

                	}
                	catch(err)
                	{
                		alert("Cannot parse JSON. Error.");
                	}
                	
                });
        });
    });
});


function reverse(urlstring, callback) {
    if (typeof callback != "function") {
        return false;
    }

    $.get(reverseurl + "?string=" + urlstring, callback);
}
