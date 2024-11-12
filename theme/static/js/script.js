document.getElementById('encryptButton').addEventListener('click', async function() {
    const keyData = await encryptKeys();  // Run your AES/RSA encryption logic here
    document.getElementById('encrypted_key').value = keyData; // Store encrypted key in hidden input
});

const imgInput = document.querySelector(".img__input");
const dispImg = document.querySelector(".img__display");

// const imgInput2 = document.querySelector(".img__input2");
// const dispImg2 = document.querySelector(".img__display2");

imgInput.addEventListener("change", (event) => {
    const imgObj = event.target.files[0];
    dispImg.src = URL.createObjectURL(imgObj);
})


// When the form is submitted, encrypted data will be sent along with the image

// async function handleKeyGenerationAndImageUpload() {
//     // Step 1: Generate the encryption keys
//     const { aesKey, rsaKey } = generateEncryptionKeys(); // Replace with your existing key generation logic

//     // Step 2: Save the keys to Cloudflare KV (via Django API)
//     const response = await fetch('/api/apiPost/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//             aesKey: aesKey,
//             rsaKey: rsaKey,
//         }),
//     });

//     if (!response.ok) {
//         alert("Failed to save keys!");
//         return;
//     }

//     // Step 3: Proceed with image upload if keys are successfully saved
//     const image = document.querySelector('#imageInput').files[0];

//     const formData = new FormData();
//     formData.append('image', image);

//     const imageUploadResponse = await fetch('/api/upload-image/', {
//         method: 'POST',
//         body: formData,
//     });

//     if (imageUploadResponse.ok) {
//         alert('Image uploaded successfully');
//     } else {
//         alert('Failed to upload image');
//     }
// }
