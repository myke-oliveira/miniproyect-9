document.querySelector('input[type="submit"]').addEventListener('click', async function (event) {
  event.preventDefault();

  const file = document.querySelector('input[type="file"]').files[0];

  const formData = new FormData()
  formData.append('file', file)

  const URL = "http://localhost:5000"

  try {
    const response = await fetch(URL, {
      header: {
        "Content-Type": "multipart/form-data"
      },
      body: formData,
      method: "POST"
    })

    const data = await response.json()

    const html = data.error
      ? `<p class="fs-1"><strong>Error:</strong> ${data.error}</p>`
      : `<p class="fs-1"><strong>Result:</strong> ${data.text}</p>`

    document.querySelector('#result').innerHTML = html
  } catch (error) {
    console.error(error)

    html = '<p class="fs-1"><strong>Error:</strong> Service temporarily unavailable! Try again later. If the problem persists, call development team.</p>'
    document.querySelector('#result').innerHTML = html

  }
  
})