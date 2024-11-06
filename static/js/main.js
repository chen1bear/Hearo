// main.js
function getRecommendation() {
    const preference = document.getElementById("preference").value;

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ preference: preference })
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById("recommendations");
        recommendationsDiv.innerHTML = "";

        if (data.length === 0) {
            recommendationsDiv.innerHTML = "<p>沒有符合的推薦，請嘗試其他音樂風格！</p>";
            return;
        }

        data.forEach(band => {
            const bandInfo = `<p><strong>${band.BandName}</strong> - 風格: ${band.Genre}, 熱門歌曲: ${band.PopularSong}</p>`;
            recommendationsDiv.innerHTML += bandInfo;
        });
    })
    .catch(error => console.error('Error:', error));
}

