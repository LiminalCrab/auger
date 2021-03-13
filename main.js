const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

function getSites(){
    fetch('urls.json')
    .then(res => res.text())
    .then(data => {
        console.log("resolved with:", data);
        JSON.parse(data).urls.forEach((u => {
          let url = new URL(`https://cors-anywhere.herokuapp.com/${u}`) // Temporary solution
          console.log("parsed from jason:", url); 
          fetch(url).then((res) => {
            res.text().then((htmlText) => {
              let doc = DOMPARSER(htmlText, 'text/xml')
              console.log(doc);
            })
          }) 
        })) //json 
    }) // data
  } //getsites 