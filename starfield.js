
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let w, h, stars = [], objects = [], burst = false, burstStart, burstTarget = "";

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;

  stars = Array.from({length: 300}, () => ({
    x: Math.random() * w - w/2,
    y: Math.random() * h - h/2,
    z: Math.random() * w,
    speed: 2
  }));

  objects = Array.from({length: 40}, () => ({
    x: Math.random() * w,
    y: Math.random() * h,
    z: Math.random() * w,
    type: Math.random() > 0.5 ? 'planet' : 'asteroid',
    color: Math.random() > 0.5 ? '#44ccff' : '#aaa',
    size: Math.random() * 3 + 2,
    speed: Math.random() * 2 + 1
  }));
}

function draw() {
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, w, h);

  // Stars
  ctx.fillStyle = 'white';
  stars.forEach(star => {
    star.z -= star.speed;
    if (burst) star.speed += 0.4;
    if (star.z <= 0 || star.speed > 60) {
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
      ctx.arc(x, y, 1.2, 0, 2 * Math.PI);
      ctx.fill();
    }
  });

  // Planets & asteroids
  objects.forEach(obj => {
    obj.z -= obj.speed;
    if (burst) obj.speed += 0.3;
    if (obj.z <= 0 || obj.speed > 80) {
      obj.x = Math.random() * w;
      obj.y = Math.random() * h;
      obj.z = w;
      obj.speed = Math.random() * 2 + 1;
    }
    const k = 128.0 / obj.z;
    const x = (obj.x - w/2) * k + w/2;
    const y = (obj.y - h/2) * k + h/2;
    if (x >= 0 && x < w && y >= 0 && y < h) {
      ctx.beginPath();
      ctx.fillStyle = obj.color;
      ctx.globalAlpha = obj.type === 'planet' ? 0.6 : 0.4;
      ctx.arc(x, y, obj.size, 0, 2 * Math.PI);
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  });

  // Complete burst
  if (burst && Date.now() - burstStart > 2500) {
    burst = false;
    window.location.href = burstTarget;
  }

  requestAnimationFrame(draw);
}

function startWarp() {
  document.getElementById('intro').style.display = 'none';
  document.getElementById('universe').style.display = 'flex';
}

function navigateTo(page) {
  document.getElementById('universe').style.display = 'none';
  burstTarget = page;
  burst = true;
  burstStart = Date.now();
}

window.addEventListener('resize', resize);
resize();
draw();
