fetch('./data/links.json')
  .then(response => response.json())
  .then(data => {
    sendData(data)
  })

function sendData (data) {
  const mainContent = document.getElementById('content')
  for (let i = 0; i < data.length; i++) {
    const div = document.createElement('li')
    div.innerHTML = `<a href="${data[i].url}">${data[i].title}</a>, <date>${data[i].date}</date>`
    mainContent.appendChild(div)
  }
}
