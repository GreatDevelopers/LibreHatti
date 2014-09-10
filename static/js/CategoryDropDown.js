$(document).ready(function()
{
    //Get the controls where we find the data-extratype attribute
    $("[data-extratype='categorydropdown']").change(getcat);
});

function getcat()
{
    //Get the changed value
    selected_value = $(this).val();
    $(this).attr('extraselected', '1');

    //Now get the sub categories and keep doing this
    reverse("librehatti.catalog.views.getsubcat", function(data)
    {
        $.get(data + "?id=" + selected_value,
            function(data)
            {
                try
                {
                    categories = $.parseJSON(data);
                }
                catch (err)
                {
                    alert("Cannot parse JSON. Error.");
                }

                //Now we have the categories
                //Create a dropdown just below the above one
                createdropdown(categories);

            });
    });
}

function reverse(urlstring, callback)
{
    if (typeof callback != "function")
    {
        return false;
    }

    $.get(reverseurl + "?string=" + urlstring, callback);
}

function deletedropdown(dropdown)
{
    $("[parent-dropdown='" + dropdown.attr("id") + "'").each(function(index, el)
    {
        deletedropdown($(el));
    });

    $('[button-parent="' + dropdown.attr("id") + '"]').remove();
    dropdown.remove();
}

function createdropdown(options)
{
    parent_dd = $("[extraselected='1']");
    var para = $("<p></p>");

    //First check if there are other dropdowns
    $("[parent-dropdown='" + parent_dd.attr("id") + "']").each(function(index, el)
    {
        //Check if there is any dropdown with this as parent
        deletedropdown($(el));
    });

    var select = $("<select id='" + parent_dd.attr("id") + "generated" + "'></select>");

    var button = $("<button class='btn btn-primary'>Select</button>")
    				.attr('button-parent', select.attr("id"));

    //Remove the previous button
    $('[button-parent="' + parent_dd.attr("id") + '"]').remove();

    //Load the options in the select
    for (key in options)
    {
        var option = $("<option value='" + key + "'>" + options[key] + "</options>");
        select.append(option);
    }

    //Add the required attributes to the new select
    select.attr('data-extratype', 'categorydropdown');

    //Add the parent id to it
    select.attr('parent-dropdown', parent_dd.attr("id"));

    //Apply the action
    select.change(getcat);

    para.append(select);
    para.append(button);

    //Add the select just below the parent dropdown
    if (options.length != 0)
    {
        if (parent_dd.parent("div").length != 0)
        {
            parent_dd.parent("div").append(para);
        }
        else
        {
            parent_dd.parent("p").parent("div").append(para)
        }
    }

    parent_dd.removeAttr('extraselected');
}

function btnaction(button)
{
	button.click(function(event) {
		
		//Aim here is to add the buttons parent dropdown options
		//to the main and top dropdown. 

		//Traverse through the dropdowns to get the parent DD
		parent_dd = $("#" + $(this).attr("button-parent"));

		//Add an attribute for the selected option
		parent_dd.find(":selected").attr("selected", "selected");

		if (parent_dd.length == 0)
		{
			alert("Cannot Find parent dropdown in button");
		}

		while (true)
		{
			if (parent_dd.attr("parent-dropdown") == undefined)
			{
				break;
			}
			else
			{
				var nextparent = $("#" + parent_dd.attr("parent-dropdown"));
				nextparent.html(parent_dd.html());
			}
		}

		//Now 
	});
}