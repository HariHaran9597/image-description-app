const imageUpload = document.getElementById('imageUpload');
const describeButton = document.getElementById('describeButton');
const descriptionText = document.getElementById('descriptionText');
const resultDiv = document.getElementById('result');
const imagePreview = document.getElementById('imagePreview');

// Show a preview of the selected image
imageUpload.addEventListener('change', () => {
    const file = imageUpload.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Image Preview">`;
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.innerHTML = `<p>No image selected</p>`;
    }
});

// Send the image to the backend for description
describeButton.addEventListener('click', () => {
    const file = imageUpload.files[0];
    if (!file) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    fetch('/describe', { 
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.description) {
            descriptionText.textContent = data.description;
            resultDiv.style.display = 'block';
        } else {
            descriptionText.textContent = 'Error: ' + (data.error || 'Could not describe image.');
            resultDiv.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        descriptionText.textContent = 'Error: An unexpected error occurred.';
        resultDiv.style.display = 'block';
    });
});
