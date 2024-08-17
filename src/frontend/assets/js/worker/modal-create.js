const saveButton_create = document.querySelector('#createWorkerModal .btn-primary');

saveButton_create.addEventListener('click', () => {
  const cr_fio = document.querySelector('#worker_cr_fio').value;
  const cr_name = document.querySelector('#worker-cr-name').value;
  const cr_position = document.querySelector('#worker-cr-position').value;
  const cr_description = document.querySelector('#worker-cr-description').value;
  // const id = document.querySelector('#worker-id').value;
  const cr_department = document.querySelector('#worker-cr-department').value;
  const cr_password = document.querySelector('#worker-cr-password').value;

  const data = {
    fio: cr_fio,
    name: cr_name,
    password: cr_password,
    department: cr_department,
    position: cr_position,
    description: cr_description
  };
  console.log('data:', data);

  fetch('/worker/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Response from server:', data);

    const modal = document.querySelector('#createWorkerModal');
    const bsModal = new bootstrap.Modal(modal);
    bsModal.hide();

      // Устанавливаем задержку перед обновлением страницы
      setTimeout(() => {
        // Обновляем текущую страницу
        window.location.reload();
      }, 500); // 1 секунда
  
    })
    .catch(error => {
      console.error('There was a problem with fetch operation:', error);
    });
  });