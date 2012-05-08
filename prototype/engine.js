////////////////////////////////////////////////////////////////
///////////////////////// Game Engine //////////////////////////
////////////////////////////////////////////////////////////////
function GameEngine(ctx){
  this.context = ctx;
  this.entities = [];
  this.floors = [];
  this.guis = [];
  this.elapsedTime = 0;
  this.stop = false;
  this.pause = false;
  this.width;
  this.height;
  
  Timer.call( this );

  this.update = function(){
    if (!this.pause)
      this.elapsedTime++;
    
    for (var i=0; i<this.entities.length; i++)
      if (!this.entities[i].destroy)
        this.entities[i].update();
      
    for (var i=this.entities.length-1; i>=0; --i){
      if (this.entities[i].destroy){
        if (this.entities[i].clear)
          this.entities[i].clear(this.context);
        this.entities.splice(i, 1);
      }
    }
    
    for (var i=0; i<this.floors.length; i++)
      if (!this.floors[i].destroy)
        this.floors[i].update();
      
    for (var i=this.floors.length-1; i>=0; --i){
      if (this.floors[i].destroy){
        if (this.floors[i].clear)
          this.floors[i].clear(this.context);
        this.floors.splice(i, 1);
      }
    }
    
    for (var i=0; i<this.guis.length; i++)
      if (!this.guis[i].destroy)
        this.guis[i].update();
      
    for (var i=this.guis.length-1; i>=0; --i){
      if (this.guis[i].destroy){
        if (this.guis[i].clear)
          this.guis[i].clear(this.context);
        this.guis.splice(i, 1);
      }
    }

  };
  
  this.clear = function(){
    this.context.clearRect(0,0,1024,600);
  };
  
  this.draw = function(){
    this.cameraStart(); // Only works if the camera is added in init()
    
    // Draw Floors
    for (var i=0; i<this.floors.length; i++)
      this.floors[i].draw(this.context);
      
    // Draw Entities
    for (var i=0; i<this.entities.length; i++)
      this.entities[i].draw(this.context);

    this.cameraRestore();
    
    // Draw GUI
    for (var i=0; i<this.guis.length; i++)
      this.guis[i].draw(this.context);
  };
  
  // Camera
  this.cameraStart = function(){
    // Camera: Save and Translate
    if (this.camera){
      // Full screen clear
      this.context.clearRect(0,0,this.width,this.height);
      var c = {
        x: this.camera.x - this.camera.obj.x,
        y: this.camera.y - this.camera.obj.y
      };
      this.context.save();
      this.context.translate( c.x, c.y );
    }
  };

  this.cameraRestore = function(){
    if (this.camera){ this.context.restore(); }
  };

  
  this.addEntity = function(entity){
    this.entities.push(entity);
  };
  
  this.addFloor = function(floor){
    this.floors.push(floor);
  };
  
  this.addGUI = function(gui){
    this.guis.push(gui);
  };
  
  this.loop = function(){
    if (!this.stop){
      this.update();
      this.clear();
      this.draw();
    }
  };
  
  this.start = function(){
      var that = this;
      (function gameLoop() {
        that.loop();
        requestAnimFrame(gameLoop);
      })();
  };
}

function Timer(){
  this.gameTime = 0;
  this.maxStep = 0.05;
  this.wallLastTimestamp = 0;
  
  this.tick = function(){
    var wallCurrent = Date.now();
    var wallDelta = (wallCurrent - this.wallLastTimestamp) / 1000;
    this.wallLastTimestamp = wallCurrent;
    
    var gameDelta = Math.min(wallDelta, this.maxStep);
    this.gameTime += gameDelta;
    return gameDelta;
  };
}

// requestAnimationFrame for smart animating by http://paulirish.com/2011/requestanimationframe-for-smart-animating/
window.requestAnimFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
