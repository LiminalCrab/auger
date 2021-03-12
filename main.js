const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

function getSites(){
    fetch('urls.json')
    .then(res => res.text())
    .then(data => {
        console.log(data);
        JSON.parse(data).urls.forEach((u => {
          let url = new URL(u)
          console.log(url);  
        }))
    })
}