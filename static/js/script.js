const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const resultImage = document.getElementById('result-image');
const generateBtn = document.getElementById('generate-btn');
const loading = document.getElementById('loading');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            previewImage.src = reader.result;
            previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

generateBtn.addEventListener('click', () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    loading.classList.remove('hidden');
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then((response) => response.json())
        .then((data) => {
            loading.classList.add('hidden');
            if (data.error) {
                alert(data.error);
                return;
            }
            resultImage.src = `data:image/png;base64,${data.sketch}`;
            resultImage.parentElement.classList.remove('hidden');
        })
        .catch((error) => {
            loading.classList.add('hidden');
            alert('Error generating sketch.');
        });
});
