const popup = document.getElementById('popup');
const close = document.getElementById('close');
const imageContainer = document.querySelector('.img-border img');


imageContainer.addEventListener('click', () => {
  popup.style.display = 'flex';
});


close.addEventListener('click', () => {
  popup.style.display = 'none';
});

popup.addEventListener('click', (event) => {
  if (event.target === popup) {
    popup.style.display = 'none';
  }
});
