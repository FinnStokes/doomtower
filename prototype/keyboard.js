////////////////////////////////////////////////////////////////
/////////////////////// Keyboard Input /////////////////////////
////////////////////////////////////////////////////////////////
// This is required because you can't copy an array, it is by reference only
Object.prototype.clone = function() {
  var newObj = (this instanceof Array) ? [] : {};
  for (i in this) {
    if (i == 'clone') continue;
    if (this[i] && typeof this[i] == "object") {
      newObj[i] = this[i].clone();
    } else newObj[i] = this[i]
  } return newObj;
};

// Keys track of keys pressed
var currentKeyDown = new Array(127);

// Initialize array with false
for (var i=0; i < currentKeyDown.length; i++)
  currentKeyDown[i] = false;

function KeyPressed(e){
  currentKeyDown[e.keyCode] = true;
}
function KeyReleased(e){
  currentKeyDown[e.keyCode] = false;
}

function Keyboard(){
  this.GetKeyDown = function(){
    return currentKeyDown.clone();
  };
  
  this.init = function(){
    window.onkeydown = KeyPressed;
    window.onkeyup = KeyReleased;
  };
  this.init();
}

var Keys = {
  Up: 38,
  Down: 40,
  Left: 37,
  Right: 39,
  W: 87,
  A: 65,
  S: 83,
  D: 68,
  Space: 32,
  Num1: 49,
  Num2: 50,
  Num3: 51,
  Num4: 52,
  Num5: 53,
  Num6: 54,
  Num7: 55,
  Num8: 56,
  Num9: 57,
  Num0: 48
};