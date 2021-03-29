function POST_DATA(){
    fetch("data/links.json")
    .then(response => { return response.json()
    }).then(data => {
        console.log(data)
        let html = data.map(links => {
            return `<a href='${links.url}>${links.title}</a>'`
        })
        console.log(html)
    }).catch(error => {
        console.log(error)
    })
}

POST_DATA();
