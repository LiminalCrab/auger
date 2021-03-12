
function getFeed(feed){
    fetch(feed)
        .then(response => response.text())
        .then(str => new window.DOMParser().parseFromString(str, "text/xml"))
        .then(data => { 
        console.log(data)
        const items = data.querySelectorAll("item");
        let html = '';
        items.forEach(el => {
            html += `
            <article> 
                <h2>
                    <a href="${el.querySelector("link").innerHTML}" target="_blank" rel="noopener">
                    ${el.querySelector("title").innerHTML}
                    </a>
                </h2>
            </article>`
        });
        document.body.insertAdjacentHTML("beforeend", html)
    });
}