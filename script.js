
function enterUniverse() {
  const overlay = document.getElementById('overlay');
  const universe = document.getElementById('universe');
  overlay.style.transform = "scale(5)";
  overlay.style.opacity = "0";
  setTimeout(() => {
    overlay.style.display = "none";
    universe.style.display = "flex";
  }, 2000);
}
