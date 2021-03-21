var socket = io();
socket.on('toweb', function(args){
	document.getElementById("height").innerHTML = args.height;
	document.getElementById("speed").innerHTML = args.speed;
	document.getElementById("battery").innerHTML = args.battery;
	document.getElementById("acceleration").innerHTML = "X:"+args.acceleration.x+", Y:"+args.acceleration.x+", Z:"+args.acceleration.x;
	document.getElementById("gyroscope").innerHTML = "X:"+args.gyroscope.x+", Y:"+args.gyroscope.x+", Z:"+args.gyroscope.x;
});