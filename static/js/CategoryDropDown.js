$(document).ready(function() {
    //Get the controls where we find the data-extratype attribute
    $("[data-extratype='categorydropdown']").change(getcat);
    });

function getcat() {
    //Get the changed value
    selected_value = $(this).val();
    $(this).attr('extraselected', '1');

    //Now get the sub categories and keep doing this
    reverse("librehatti.catalog.views.getsubcat", function(data) {
        $.get(data + "?id=" + selected_value,
            function(data) {
                try {
                    categories = $.parseJSON(data);
                } catch (err) {
                    alert("Cannot parse JSON. Error.");
                }



                //Now we have the categories
                //Create a dropdown just below the above one
                createdropdown(categories);

            });
    });
}

function reverse(urlstring, callback) {
    if (typeof callback != "function") {
        return false;
    }

    $.get(reverseurl + "?string=" + urlstring, callback);
}


function createdropdown(options) {
    parent_dd = $("[extraselected='1']");
    var para = $("<p></p>");
    var select = $("<select id='" + parent_dd.attr("id") + "generated" + "'></select>");

    //Load the options in the select
    for (key in options) {
        var option = $("<option value='" + key + "'>" + options[key] + "</options>");
        select.append(option);
    }

    //Add the required attributes to the new select
    select.attr('data-extratype', 'categorydropdown');

    select.change(getcat);

    para.append(select);

    //Add the select just below the parent dropdown
    parent_dd.parent("div").append(para);

    //
}
