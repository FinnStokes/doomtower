// MOUSE
var latestCoords = [{x: 0, y: 0}];

function getCoords(e) {
  if (e.offsetX)
    return { x: e.offsetX, y: e.offsetY };
  else if (e.layerX)
    return { x: e.layerX, y: e.layerY };
  else
    return { x: e.pageX - canvas.offsetLeft, y: e.pageY - canvas.offsetTop };
}

function mouseMove(e){
  if (e.touches) {
    // Touch Events
    for (var i=1; i <= e.touches.length; i++ ){
      latestCoords[i] = getCoords(e.touches[i - 1]);
    }
  } else {
    // Mouse Events
    latestCoords[0] = getCoords(e);
  }
}

var isMouseDown = false;
function mouseDown(e){ // AKA Input Start
  e.preventDefault();
  isMouseDown = true;
}
function mouseUp(e){ // AKA Input End
  isMouseDown = false;
}

function scroll(e){
  e.preventDefault();
  if ( e.wheelDelta > 0 || e.wheelDeltaY > 0 || e.detail < 0)
    game.camera.obj.y -= 32;
  else if ( e.wheelDelta < 0 || e.wheelDeltaY < 0 || e.detail > 0)
    game.camera.obj.y += 32;
}

// Input Listeners
function startListeners(){
  // touch screen support
  canvas.ontouchmove = mouseMove;
  canvas.ontouchstart = mouseDown;
  canvas.ontouchend = mouseUp;

  // mouse support
  canvas.onmousemove = mouseMove;
  canvas.onmousedown = mouseDown;
  canvas.onmouseup = mouseUp;
  
  // mouse scroll
  window.addEventListener('DOMMouseScroll', scroll, false);
  window.onmousewheel = document.onmousewheel = scroll;
}