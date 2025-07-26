const fileInput = document.getElementById('fileInput');
const uploadIcon = document.getElementById('uploadIcon');

// Add an event listener to the icon
uploadIcon.addEventListener('click', () => {
  fileInput.click();
});

// Add an event listener to the file input
fileInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  
  alert('File uploaded successfully!');
});