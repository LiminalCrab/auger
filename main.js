const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

function getData(){
  fetch('urls.json')
  .then(response => response.text())
  .then(data => {
    console.log("Step one:", data) // del
    let siteList = JSON.parse(data)
    console.log("sitelist data", siteList); //del

    //for each, send them to the proxy, and then fetch them again to avoid CORS.
    siteList.urls.forEach((index => { 
      let uri = new URL(`http://127.0.0.1:8080/${index}`)
      console.log(uri);

      //we have to fetch it from the proxy now.
      fetch(uri).then((res) => {
        res.text().then((parsedXML) => {
          let doc = DOMPARSER(parsedXML, 'text/xml')
          console.log(doc);
          const item = doc.querySelectorAll("item")
          const entries = doc.querySelectorAll("entry");
          console.log(entries, item); // delete

        })
      })
    }))
  })
}