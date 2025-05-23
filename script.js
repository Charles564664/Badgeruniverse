
function startPortal() {
  document.getElementById('intro').style.display = 'none';
  document.getElementById('universe').style.display = 'block';
}

function flyTo(section) {
  const warp = document.getElementById('warp');
  warp.style.display = 'block';
  setTimeout(() => {
    alert('Navigating to: ' + section);
    warp.style.display = 'none';
  }, 2000);
}
