
function startUniverse() {
  document.getElementById('intro').style.display = 'none';
  document.getElementById('universe').style.display = 'block';
}
function navigateTo(page) {
  document.body.innerHTML = '<div class="warp"></div>';
  setTimeout(() => { window.location.href = page; }, 1200);
}
