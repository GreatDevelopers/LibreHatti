var counter = 1;
var limit = 100;
function addInput(divName){
     if (counter == limit)  {
          alert("You have reached the limit of adding " + counter + " inputs");
     }
     else {
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "Add Another " + (counter + 1) + " <br><input type='text' name='kilometer'> <br> <br> <input type='text' name='Date'>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     }
}
