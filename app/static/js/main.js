document.addEventListener("DOMContentLoaded", () => {
  const rows = document.querySelectorAll(".chapter-row, .card, .form-card");

  rows.forEach((el, index) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(18px)";

    setTimeout(() => {
      el.style.transition = "0.45s ease";
      el.style.opacity = "1";
      el.style.transform = "translateY(0)";
    }, index * 70);
  });

  const progressBar = document.getElementById("progressBar");

  if (progressBar) {
    window.addEventListener("scroll", () => {
      const height = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.scrollY / height) * 100;
      progressBar.style.width = progress + "%";
    });
  }

  const drawerBtn = document.getElementById("drawerBtn");
  const chapterDrawer = document.getElementById("chapterDrawer");
  const closeDrawer = document.getElementById("closeDrawer");

  if (drawerBtn && chapterDrawer) {
    drawerBtn.addEventListener("click", () => {
      chapterDrawer.classList.add("open");
    });
  }

  if (closeDrawer && chapterDrawer) {
    closeDrawer.addEventListener("click", () => {
      chapterDrawer.classList.remove("open");
    });
  }

    const spotifyCircle = document.getElementById("spotifyCircle");

    if (spotifyCircle) {
    spotifyCircle.addEventListener("click", () => {
        spotifyCircle.classList.add("playing");
    });
    }
});