function POST_DATA(){
    fetch("data/links.json")
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const html = data.map(links => {
            return `<a href="${data.data[0]}">${data}</a>`
        })
        console.log(html)
    });
}

POST_DATA();
