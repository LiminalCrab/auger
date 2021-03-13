const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

function getSites(){
    fetch('urls.json')
    .then(res => res.text())
    .then(data => {
        console.log("resolved with:", data);
        JSON.parse(data).urls.forEach((u => {
          let url = new URL(`http://127.0.0.1:8080/${u}`); //Temporary solution
          console.log("parsed from jason:", url); 
          fetch(url).then((res) => {
            res.text().then((parsedText) => {
              let doc = DOMPARSER(parsedText, 'text/xml');
              console.log(doc)
          })
        }) //json 
    })) //getsites 
  })
}
