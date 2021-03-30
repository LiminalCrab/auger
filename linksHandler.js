fetch("./data/links.json")
    .then(response => response.json())
    .then(data => {
        sendData(data);
    });


function sendData(data){
    let mainContent = document.getElementById("content");
    for (var i = 0; i < data.length; i++){
        let div = document.createElement("div");
        div.innerHTML = `<p><a href="${data[i].url}">${data[i].title}</a>
        <span>${data[i].date}</span></p>`
        mainContent.appendChild(div);
    }
}

