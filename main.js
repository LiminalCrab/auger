const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

let dateStore = [];

fetch('urls.json')
.then(response => response.text())
.then(data => {
  let siteList = JSON.parse(data)

  //for each, send them to the proxy, and then fetch them again to avoid CORS.
  siteList.urls.forEach((index => { 
    let uri = new URL(`http://127.0.0.1:8080/${index}`)

    //we have to fetch it from the proxy now.
    fetch(uri).then((res) => {
      res.text().then((parsedXML) => {
        let doc = DOMPARSER(parsedXML, 'text/xml');
        const items = doc.querySelectorAll("item"); //surely I don't actually need two of these? 
        const entries = doc.querySelectorAll("entry");
        const innerDate = doc.querySelectorAll("pubDate");
        let html = ``;

        //sorting the dates test
        innerDate.forEach(el => {
          var dateData = el.innerHTML;
          el.innerHTML = dateData.replace(/^([0-9]{4})([0-9]{2})([0-9]{2})/, "$1/$2/$3"); //remove the <> tags
          const unixTimeParse = new Date(`'${dateData}'`);
          dateStore.push(unixTimeParse);
          DatetoHtml = dateStore.sort(function(x, y){
            return y - x
          })
          console.log(DatetoHtml)     
      });
      })
    })
  }))
})
