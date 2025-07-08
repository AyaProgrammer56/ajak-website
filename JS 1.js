// Animation for About Section
window.addEventListener("DOMContentLoaded", () => {
  const text = document.querySelector(".about-text");
  const image = document.querySelector(".about-image");

  if (text && image) {
    text.style.opacity = 0;
    image.style.opacity = 0;

    setTimeout(() => {
      text.style.transition = "opacity 1s ease";
      image.style.transition = "opacity 1s ease";
      text.style.opacity = 1;
      image.style.opacity = 1;
    }, 500);
  }
});








// Toggle Sections with Smooth Slide Effect
function toggleSection(id) {
  const content = document.getElementById(id);

  if (!content) return;

  const isVisible = content.style.display === "block";
  if (isVisible) {
    content.style.height = content.scrollHeight + "px";
    requestAnimationFrame(() => {
      content.style.transition = "height 0.5s ease, opacity 0.5s ease";
      content.style.height = "0";
      content.style.opacity = 0;
    });
    setTimeout(() => {
      content.style.display = "none";
    }, 500);
  } else {
    content.style.display = "block";
    content.style.height = "auto";
    const height = content.scrollHeight + "px";
    content.style.height = "0";
    content.style.opacity = 0;
    requestAnimationFrame(() => {
      content.style.transition = "height 0.5s ease, opacity 0.5s ease";
      content.style.height = height;
      content.style.opacity = 1;
    });
  }
}
