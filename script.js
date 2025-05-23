
function startUniverse() {
  document.getElementById('intro').style.display = 'none';
  document.getElementById('universe').style.display = 'block';
}
function navigateTo(page) {
  const warp = document.getElementById('warp');
  warp.style.display = 'block';
  setTimeout(() => {
    window.location.href = page;
  }, 1800);
}
