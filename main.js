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
          el.innerHTML = dateData.replace(/^([0-9]{4})([0-9]{2})([0-9]{2})/, "$1/$2/$3") //remove the <> tags
          let parseThedate = Date.parse(dateData);
          dateStore.push(`${parseThedate}`);

          //okay so we're sorting here.
          dateStore.sort(function(x, y){
            return y - x
        });

      });

      const dateRemap = dateStore.map(y => new Date(y * 1000))
      console.log (dateRemap);

        items.forEach(el => {
          html += `
          <article>
            <h3>
              <span>${doc.querySelector("title").innerHTML}</span>
              <a href="${el.querySelector("link").innerHTML}" target="_blank" rel="noopener">
              ${el.querySelector("title").innerHTML}
              </a>
              <span>${el.querySelector("pubDate").innerHTML}</span>
            </h3>
          </article>
          `;
        });
        entries.forEach(el => {
          html += `
          <article>
            <h3>
              <span>${doc.querySelector("title").innerHTML}</span>
              <a href="${el.querySelector("link").innerHTML}" target="_blank" rel="noopener">
              ${el.querySelector("title").innerHTML}
              </a>
              <span>${el.querySelector("pubDate").innerHTML}</span>
            </h3>
          </article>
          `;
        });
        html += `</div>`;
        document.getElementById('content').insertAdjacentHTML("beforeend", html);
      })
    })
  }))
})
