
const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/calculate', {
    method: 'POST',
    body: formData
  });

  const result = await response.text();
  // const result = document.getElementById('result');
  // document.getElementById("myButton").addEventListener("click", function() {
  if (result <= 20) {
        sessionStorage.setItem('result', result);
        window.location.href = '/the_worst_result';
  }
  else if (result > 20 && result <= 40){
      sessionStorage.setItem('result', result);
      window.location.href = '/bad_result';
  }
  else if (result > 40 && result <= 60){
    sessionStorage.setItem('result', result);
    window.location.href = '/normal_result';
}
  else if (result > 60 && result <= 80){
    sessionStorage.setItem('result', result);
    window.location.href = '/good_result';
  }
  else {
   // document.getElementById('result').innerText = `The probability that this person will be given an advance payment (as a percentage): ${result}`;

   sessionStorage.setItem('result', result);
   window.location.href = '/excellent_result';
  }
  
});