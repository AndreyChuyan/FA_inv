﻿const saveButton_create = document.querySelector('#createModal .btn-primary');

saveButton_create.addEventListener('click', () => {
  const cr1 = document.querySelector('#cr-title').value;
  const cr2 = document.querySelector('#cr-location').value;
  const cr3 = document.querySelector('#cr-name').value;
  const cr4 = document.querySelector('#cr-model').value;
  const cr5 = document.querySelector('#cr-release').value;
  const cr6 = document.querySelector('#cr-num_serial').value;
  const cr7 = document.querySelector('#cr-num_invent').value;
  const cr8 = document.querySelector('#cr-num_service').value;
  const cr9 = document.querySelector('#cr-price').value;
  const cr10 = document.querySelector('#cr-state').value;
  const cr11 = document.querySelector('#cr-description').value;

  const data = {
    title: cr1,
    location: cr2,
    name: cr3,
    model: cr4,
    release: cr5,
    num_serial: cr6,
    num_invent: cr7,
    num_service: cr8,
    price: cr9,
    state: cr10,
    description: cr11
  };
  console.log('data:', data);

  // fetch('/worker/', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json'
  //   },
  //   body: JSON.stringify(data)
  })
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Network response was not ok');
//     }
//     return response.json();
//   })
//   .then(data => {
//     console.log('Response from server:', data);

//     const modal = document.querySelector('#createWorkerModal');
//     const bsModal = new bootstrap.Modal(modal);
//     bsModal.hide();

//     window.location.reload();
//   })
//   .catch(error => {
//     console.error('There was a problem with fetch operation:', error);
//   });
});