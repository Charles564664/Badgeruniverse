
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let stars = [], w, h, burst = false, burstStart;

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
  stars = Array.from({length: 400}, () => ({
    x: Math.random() * w - w/2,
    y: Math.random() * h - h/2,
    z: Math.random() * w,
    speed: 2
  }));
}

function draw() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = 'white';

  stars.forEach(star => {
    star.z -= star.speed;
    if (burst) {
      star.speed += 0.5;
    }
    if (star.z <= 0 || star.speed > 50) {
      star.x = Math.random() * w - w/2;
      star.y = Math.random() * h - h/2;
      star.z = w;
      star.speed = 2;
    }

    const k = 128.0 / star.z;
    const x = star.x * k + w/2;
    const y = star.y * k + h/2;
    if (x >= 0 && x < w && y >= 0 && y < h) {
      ctx.beginPath();
      ctx.arc(x, y, 1.5, 0, 2 * Math.PI);
      ctx.fill();
    }
  });

  if (burst && Date.now() - burstStart > 2000) {
    burst = false;
    window.location.href = burstTarget;
  }

  requestAnimationFrame(draw);
}

function startWarp() {
  document.getElementById('intro').style.display = 'none';
  document.getElementById('universe').style.display = 'flex';
}

let burstTarget = "";
function navigateTo(page) {
  document.getElementById('universe').style.display = 'none';
  burstTarget = page;
  burst = true;
  burstStart = Date.now();
}

window.addEventListener('resize', resize);
resize();
draw();
