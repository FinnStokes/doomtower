// Camera
function Camera(x,y){
  this.x = x;
  this.y = y;
  this.w = 1;
  this.h = 1;
  this.destroy = false;
  
  this.name = 'player';
  
  this.velocity = { x: 0, y: 0 };
  this.maxVelocity = { x: 20, y: 30 }; // this.maxVelocity.y == jump power
  this.acceleration = { x: 1, y: 1 };
  this.decceleration = { x: 1 , y: 1 };
  this.friction = { x: 1, y: 1 };
  this.gravity = 2;
  
  this.canJump = true;
  this.onGround = true;
  this.canMove = true;
  this.spring = false;

  this.state = 'isLanded';

  this.move = function(dir){
    var v = this.velocity.x * dir;
    var a = this.acceleration.x;
    var d = this.decceleration.x;
    var maxv = this.maxVelocity.x;
    
    if (dir != 0){
      if ( v < 0 ){
        v += d;
      } else if ( v < maxv ){
        v += a;
        if ( v > maxv ){
          v = maxv;
        }
      }
      this.velocity.x = v * dir;
    } else {
      this.applyGroundFriction(1,0);
    }
  };
  
  this.moveY = function(dir){
    var v = this.velocity.y * dir;
    var a = this.acceleration.y;
    var d = this.decceleration.y;
    var maxv = this.maxVelocity.y;
    
    if (dir != 0){
      if ( v < 0 ){
        v += d;
      } else if ( v < maxv ){
        v += a;
        if ( v > maxv ){
          v = maxv;
        }
      }
      this.velocity.y = v * dir;
    } else {
      this.applyGroundFriction(0,1);
    }
  };
  
  this.applyGroundFriction = function(x,y){
    if (x){
      var dir;
      var velx = this.velocity.x;
      
      if ( velx > 0 ){
        dir = 1;
      } else if ( velx < 0 ){
        dir = -1;
      } else {
        dir = 0;
      }
      this.velocity.x -= this.friction.x * dir;
    } else if (y){
      var dir;
      var vely = this.velocity.y;
      
      if ( vely > 0 ){
        dir = 1;
      } else if ( vely < 0 ){
        dir = -1;
      } else {
        dir = 0;
      }
      this.velocity.y -= this.friction.y * dir;
    }
  };
  
  this.update = function(){
    this.inputLeftRight();
    this.x += this.velocity.x;
    this.y += this.velocity.y;
  };
  
  // Input
  this.keyboardState = keyboard.GetKeyDown();
  this.prevKeyboardState = this.keyboardState;
  
  this.inputLeftRight = function(){
    // bools for easy checks
    var prevup = this.keyboardState[Keys.Up] == true;
    var prevdown = this.keyboardState[Keys.Down] == true;
    var prevleft = this.keyboardState[Keys.Left] == true;
    var prevright = this.keyboardState[Keys.Right] == true;

    // Update
    this.keyboardState = keyboard.GetKeyDown();
    
    // bools for easy checks
    var up = this.keyboardState[Keys.Up] == true;
    var down = this.keyboardState[Keys.Down] == true;
    var left = this.keyboardState[Keys.Left] == true;
    var right = this.keyboardState[Keys.Right] == true;
    
    /*
    if ( right )
      this.move(1);
      else if ( left )
        this.move(-1);
      else
        this.move(0);
    */
    if ( up )
      this.moveY(-1);
      else if ( down )
        this.moveY(1);
      else
        this.moveY(0);
  };
  
  this.draw = function(){
	  // Draw stuff to come when graphics go into game
  }; 
}