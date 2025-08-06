const images = document.querySelectorAll('.carousel-img');
let current = 0;

function showNextImage() {
  images[current].classList.remove('active');
  current = (current + 1) % images.length;
  images[current].classList.add('active');
}

setInterval(showNextImage, 3000);


document.addEventListener('DOMContentLoaded', function () {
  const items = document.querySelectorAll('.accordion-item');

  items.forEach(item => {
    const header = item.querySelector('.accordion-header');
    header.addEventListener('click', () => {
      const openItem = document.querySelector('.accordion-item.active');
      if (openItem && openItem !== item) {
        openItem.classList.remove('active');
        openItem.querySelector('.accordion-body').style.display = 'none';
      }

      const body = item.querySelector('.accordion-body');
      const isOpen = item.classList.contains('active');

      if (isOpen) {
        item.classList.remove('active');
        body.style.display = 'none';
      } else {
        item.classList.add('active');
        body.style.display = 'block';
      }
    });
  });
});

const startYear = 2025;
const currentYear = new Date().getFullYear();
const yearText = currentYear > startYear ? `${startYear} - ${currentYear}` : `${startYear}`;

document.getElementById("copyright").innerText = `Copyright © ${yearText}. All rights reserved.`;



