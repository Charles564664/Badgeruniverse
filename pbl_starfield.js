
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');
let stars = [], w, h;

function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
  stars = Array.from({length: 300}, () => ({
    x: Math.random() * w - w / 2,
    y: Math.random() * h - h / 2,
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
    if (star.z <= 0) star.z = w;
    const k = 128.0 / star.z;
    const x = star.x * k + w / 2;
    const y = star.y * k + h / 2;
    if (x >= 0 && x < w && y >= 0 && y < h) {
      ctx.beginPath();
      ctx.arc(x, y, 1.4, 0, 2 * Math.PI);
      ctx.fill();
    }
  });
  requestAnimationFrame(draw);
}
function navigateTo(page) {
  window.location.href = page;
}
window.addEventListener('resize', resize);
resize();
draw();
