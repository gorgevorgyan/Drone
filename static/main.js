  var green='#030fd8'



  var slider = document.getElementById("myRange");
  var output = document.getElementById("demo");

  output.innerHTML = slider.value;

  var slider1 = document.getElementById("myRange1");
  var output1 = document.getElementById("demo1");

  output1.innerHTML = slider1.value;

  var slider2 = document.getElementById("myRange2");
  var output2 = document.getElementById("demo2");
  output2.innerHTML = slider2.value;

  // var sliderm1 = document.getElementById("m1");
  // var outputm1 = document.getElementById("demom1");

  // outputm1.value = sliderm1.value;


  slider.oninput = function() {
    update()
    output.innerHTML = this.value;
  }
  // sliderm1.oninput = function() {
  //   update()
  //   outputm1.value = this.value;
  // }
  // outputm1.oninput = function() {
  //   update()
  //   sliderm1.value = this.value;
  // }
  slider1.oninput = function() {
    update()
    output1.innerHTML = this.value;
  }
  slider2.oninput = function() {
    update()
    output2.innerHTML = this.value;
  }

  class JoystickController
  {
// stickID: ID of HTML element (representing joystick) that will be dragged
// maxDistance: maximum amount joystick can move in any direction
// deadzone: joystick must move at least this amount from origin to register value change
constructor( stickID, maxDistance, deadzone )
{
  this.id = stickID;
  let stick = document.getElementById(stickID);

  // location from which drag begins, used to calculate offsets
  this.dragStart = null;

  // track touch identifier in case multiple joysticks present
  this.touchId = null;
  
  this.active = false;
  this.value = { x: 0, y: 0,}; 

  let self = this;

  function handleDown(event)
  {
    self.active = true;

    // all drag movements are instantaneous
    stick.style.transition = '0s';

    // touch event fired before mouse event; prevent redundant mouse event from firing
    event.preventDefault();

    if (event.changedTouches){

      self.dragStart = { x: event.changedTouches[0].clientX, y: event.changedTouches[0].clientY };
    }
    else{
      self.dragStart = { x: event.clientX, y: event.clientY };
    }

    // if this is a touch event, keep track of which one
    if (event.changedTouches){

      self.touchId = event.changedTouches[0].identifier;
    }
    update()
  }
  
  function handleMove(event) 
  {
    if ( !self.active ) return;

      // if this is a touch event, make sure it is the right one
      // also handle multiple simultaneous touchmove events
      let touchmoveId = null;
      if (event.changedTouches)
      {
        for (let i = 0; i < event.changedTouches.length; i++)
        {
          if (self.touchId == event.changedTouches[i].identifier)
          {

            touchmoveId = i;
            event.clientX = event.changedTouches[i].clientX;
            event.clientY = event.changedTouches[i].clientY;
          }
        }

        if (touchmoveId == null) return;
      }

      const xDiff = event.clientX - self.dragStart.x;
      const yDiff = event.clientY - self.dragStart.y;
      const angle = Math.atan2(yDiff, xDiff);
      const distance = Math.min(maxDistance, Math.hypot(xDiff, yDiff));
      const xPosition = distance * Math.cos(angle);
      const yPosition = distance * Math.sin(angle);

    // move stick image to new position
    stick.style.transform = `translate3d(${xPosition}px, ${yPosition}px, 0px)`;

    // deadzone adjustment
    const distance2 = (distance < deadzone) ? 0 : maxDistance / (maxDistance - deadzone) * (distance - deadzone);
    const xPosition2 = distance2 * Math.cos(angle);
    const yPosition2 = distance2 * Math.sin(angle);
    const xPercent = parseFloat((xPosition2 / maxDistance).toFixed(4));
    const yPercent = parseFloat((yPosition2 / maxDistance).toFixed(4));

    self.value = { x: xPercent, y: yPercent };
    update()
  }

  function handleUp(event) 
  {

    if ( !self.active ) return;

      // if this is a touch event, make sure it is the right one
      if (event.changedTouches && self.touchId != event.changedTouches[0].identifier) return;

      // transition the joystick position back to center
      stick.style.transition = '.2s';
      stick.style.transform = `translate3d(0px, 0px, 0px)`;

      // reset everything
      self.value = { x: 0, y: 0 };
      self.touchId = null;
      self.active = false;
      update()
    }

    stick.addEventListener('mousedown', handleDown);
    stick.addEventListener('touchstart', handleDown);
    document.addEventListener('mousemove', handleMove, {passive: false});
    document.addEventListener('touchmove', handleMove, {passive: false});
    document.addEventListener('mouseup', handleUp);
    document.addEventListener('touchend', handleUp);

  }
}

let joystick1 = new JoystickController("stick1", 64, 8);
function update()
{ 
  // console.log('change')
  let states={
   m1:document.getElementById("demom1").value, 
   m2:document.getElementById("demom2").value,
   m3:document.getElementById("demom3").value,
   m4:document.getElementById("demom4").value,
   x: joystick1.value.x, 
   y: joystick1.value.y,
   z:slider.value,
   X_config:slider1.value,
   Y_config:slider2.value
 }; 
 socket.emit('states',states);

}

// function loop()
// {
//   requestAnimationFrame(loop);
//   update();
// }

// loop();



document.onkeydown = function (event) {
  if (event.keyCode==38) {

    document.getElementById("myRange").value++;
    output.innerHTML = slider.value;
    update()
  }
  if (event.keyCode==40) {

    document.getElementById("myRange").value--;
    output.innerHTML = slider.value;
    update()
  }
  if (event.keyCode==87) {
    joystick1.value.y=1
    update()
    document.getElementById("t3").style.fill = "red";
    document.getElementById("t4").style.fill = "red";
    document.getElementById("t1").style.fill = green;
    document.getElementById("t2").style.fill = green;
  }
  if (event.keyCode==83) {
    joystick1.value.y=-1
    update()
    document.getElementById("t1").style.fill = "red";
    document.getElementById("t2").style.fill = "red";
    document.getElementById("t3").style.fill = green;
    document.getElementById("t4").style.fill = green;


  }
  if (event.keyCode==65) {
    joystick1.value.x=1
    update()
    document.getElementById("t2").style.fill = "red";
    document.getElementById("t4").style.fill = "red";
    document.getElementById("t1").style.fill = green;
    document.getElementById("t3").style.fill = green;

  }
  if (event.keyCode==68) {
    joystick1.value.x=-1
    update()
    document.getElementById("t1").style.fill = "red";
    document.getElementById("t3").style.fill = "red";
    document.getElementById("t4").style.fill = green;
    document.getElementById("t2").style.fill = green;

  }
    if (event.keyCode==81) {
    socket.emit('fullLeft');
    document.getElementById("t2").style.fill = "red";
    document.getElementById("t3").style.fill = "red";
    document.getElementById("t1").style.fill = green;
    document.getElementById("t4").style.fill = green;

  } 
  if (event.keyCode==69) {
    socket.emit('fullRight');
    document.getElementById("t1").style.fill = "red";
    document.getElementById("t4").style.fill = "red";
    document.getElementById("t2").style.fill = green;
    document.getElementById("t3").style.fill = green;

}
}
document.onkeyup = function (event) {
  if (event.keyCode==32) {
    document.getElementById("myRange").value=0
    update() 
    socket.emit('home');
    document.getElementById("demo").innerHTML='0'
  }
  if (event.keyCode==87) {
    joystick1.value.y=0
    update()
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t3").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";
  }
  if (event.keyCode==83) {
    joystick1.value.y=0
    update()
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";
    document.getElementById("t3").style.fill = "black";

  }
  if (event.keyCode==65) {
    joystick1.value.x=0
    update()
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t3").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";

  }
  if (event.keyCode==68) {
    joystick1.value.x=0
    update()
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t3").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";

  } 
  if (event.keyCode==81) {
    socket.emit('stopRotate');
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t3").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";

  } 
  if (event.keyCode==69) {
    socket.emit('stopRotate');
    document.getElementById("t1").style.fill = "black";
    document.getElementById("t3").style.fill = "black";
    document.getElementById("t4").style.fill = "black";
    document.getElementById("t2").style.fill = "black";

  }
}
function setValue(theValue) {

  // Animate the Button to the value clicked on.
  $("#slider").slider('value', theValue);

  //Display the numeric value on the html page.
  $('#showValue').html('Height: ' + theValue);


}

const checkbox = document.getElementById('customSwitch1')

checkbox.addEventListener('change', (event) => {
  if (event.currentTarget.checked) {
    $('#iu').modal();
  } 
})
// $('input[type="checkbox"]').on('change', function(e){
//    if(e.target.checked){
//      $('#myModal').modal();
//    }
// });

function config(){
update()

 // socket.emit('config',config);
 $('#iu').modal('toggle')



}