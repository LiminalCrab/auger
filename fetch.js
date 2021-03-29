fetch("data/links.json")
    .then(response => response.json())
    .then(json => console.log(json));