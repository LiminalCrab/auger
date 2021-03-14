const DOMPARSER = new DOMParser().parseFromString.bind(new DOMParser())

fetch('urls.json')
.then(response => response.text())
.then(data => {
  //console.log("Step one:", data) // del
  let siteList = JSON.parse(data)
  //console.log("sitelist data", siteList); //del

  //for each, send them to the proxy, and then fetch them again to avoid CORS.
  siteList.urls.forEach((index => { 
    let uri = new URL(`http://127.0.0.1:8080/${index}`)
    //console.log(uri);

    //we have to fetch it from the proxy now.
    fetch(uri).then((res) => {
      res.text().then((parsedXML) => {
        let doc = DOMPARSER(parsedXML, 'text/xml');
        //console.log(doc);
        const items = doc.querySelectorAll("item"); //surely I don't actually need two of these? 
        const entries = doc.querySelectorAll("entry");
        const innerDate = doc.querySelectorAll("pubDate");
        let html = ``;
          //html += `<p>${doc.querySelector("published").innerHTML}</p>`
        //console.log(html);
        //console.log(entries, items); // delete
        innerDate.forEach(el => {
          var dateData = el.innerHTML;
          el.innerHTML = dateData.replace(/^([0-9]{4})([0-9]{2})([0-9]{2})/, "$1/$2/$3")
          let parseThedate = Date.parse(dateData);
          console.log(parseThedate)


        });
        

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
