document.getElementById('convertBtn').addEventListener('click', async function() {
    let fileInput = document.getElementById('imageUpload').files[0];
    if (!fileInput) {
        alert("Lütfen bir resim yükleyin!");
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    let response = await fetch("/convert", {
        method: "POST",
        body: formData
    });

    if (response.ok) {
        let jsonBlob = await response.blob();
        let downloadLink = document.getElementById("downloadLink");
        downloadLink.href = URL.createObjectURL(jsonBlob);
        downloadLink.style.display = "block";
        downloadLink.innerText = "JSON Modeli İndir";
        downloadLink.download = "minecraft_model.json";
    } else {
        alert("Dönüştürme başarısız!");
    }
});
