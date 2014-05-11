//Basic Product Strructure to be used.

function product(name, id, no, element) {
    this.name = name;
    this.id = id;
    this.no = no;
    this.element = null;
    this.increment = function(no) {
        no = typeof no == "undefined" ? 1 : no;
        for (var i = 0; i < no; i++) {
            this.no++;
        }
    }
    this.decrement = function(no) {
        no = typeof no == "undefined" ? 1 : no;
        for (var i = 0; i < no; i++) {
            this.no--;
        }
    }

    this.returnhtmlname = function() {
        return name + "(" + this.no + ")";
    }

    this.returnname = function() {
        return this.name;
    }

    this.returnid = function() {
        return this.id
    }

    this.createid = function() {
        return this.id + "productcart";
    }

    this.createhtml = function() {
        //Check if html element was created earlier
        if (this.element != null) {
            return this.element;
        }
        //Create the HTML element
        var li = $("<li></li>");
        li.attr("id", this.createid());
        li.html(this.returnhtmlname());

        //Add the created element. From now on this will used.
        this.element = li;
        return this.element;
    }

    this.remove = function() {
        //Remove the html
        $("#" + this.createid()).remove();
    }
}



//Cart module: Will hold the cart upto checkout
var cart = {};

cart.items = [];

cart.container = "#cartitems";

cart.addItem = function(name, id, no) {
    item = this.isthere(id);
    //Check if the item is already in the List
    if (item >= 0) {
        //Item is already present so we don't need to add one for.
        this.items[item].increment(no);
        cart.synchtml();
    } else if (item == -1) {
        //This item doesn't exist; hence we will add this one
        var newProduct = new product(name, id, no);
        this.items.push(newProduct);

        //Now we have new product. Lets add this to the page
        cart.synchtml();

    }

}


cart.isthere = function(id) {
    var isthere = false;
    for (var item in this.items) {
        if (id == this.items[item].id) {
            isthere = true;
            return item;
            break;
        }
    }

    //return the result
    if (!isthere) {
        return -1;
    }
};

cart.removeItem = function(id, no) {
    //Get the id the selected item.
    item = this.isthere(id);
    if (item = -1) // Item is not present
    {
        return false;
    } else {
        this.items[item].decrement(no);
        this.synchtml();
    }
}

cart.syncproducthtml = function(product, id) {
    //Check if the element even exist. if not then we need to create it.
    if (product.element == null) {
    	product.createhtml();
        $(this.container).append(product.element);
    }

    var element = $("#" + id);

    //Now sync the details.
    if (!element.length) {
        alert("I couldn't find my element. Please check");
    }

    element.html(product.returnhtmlname());
}


cart.synchtml = function() {
    //For each of the element
    $.each(this.items, function(key, value) {
        //We don't have to do anything with the array here. Staight go to the value
        if (value.no <= 0) {
            //It is is negative that means we have to remvove this
            this.items[key].remove();
            this.items.slice(key, 1);
        } else {
            // There are the products. Now we to synchtml

            //Check if it even has a html
            if (value.element == null) {
                value.createhtml();
            }

            //Now add this html on the page
            $(cart.container).append(value.element);

            //Now we have html we can now directly access it and sync it.
            cart.syncproducthtml(value, value.createid());
        }
    });
}
