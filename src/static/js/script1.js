
const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/calculate', {
    method: 'POST',
    body: formData
  });
  const result = await response.text();
  document.getElementById('result').innerText = `The probability that this person will be given an advance payment (as a percentage): ${result}`;
});