var jail = document.getElementById('jail');

document.addEventListener('mousemove', mouseUpdate, false);
document.addEventListener('mouseenter', mouseUpdate, false);

var seenMouse = false;

function mouseUpdate(e) {
  var jailCoords = jail.getBoundingClientRect();
  var pageCoords = document.body.getBoundingClientRect();

  var x = e.pageX - jailCoords.left;
  var y = e.pageY - jailCoords.top;

  document.body.style.setProperty('--mouseX', x);
  document.body.style.setProperty('--mouseY', y);

  document.body.style.setProperty('--width', pageCoords.width);
  document.body.style.setProperty('--height', pageCoords.height);
  
  if (!seenMouse) {
    document.body.classList.add('seenMouse');
    seenMouse = true;
  }
}

function mouseLeft(e) {
  document.body.classList.remove('seenMouse');
  seenMouse = false;
}

document.addEventListener('mouseleave', mouseLeft, false);
