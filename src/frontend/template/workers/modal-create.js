import { validatePassword } from '../../assets/js/validators.js';

// import { validatePassword } from './validators.js';

const saveButton_create = document.querySelector('#createWorkerModal .btn-primary');


saveButton_create.addEventListener('click', () => {
  const cr_fio = document.querySelector('#worker_cr_fio').value;
  const cr_name = document.querySelector('#worker-cr-name').value;
  const cr_position = document.querySelector('#worker-cr-position').value;
  const cr_description = document.querySelector('#worker-cr-description').value;
  // const id = document.querySelector('#worker-id').value;
  const cr_department = document.querySelector('#worker-cr-department').value;
  const cr_password = document.querySelector('#worker-cr-password').value;

  // Проверки на пустое значение (и пробелы)
  if (!cr_name.trim()) { 
    alert("Пожалуйста, заполните поле - Логин:");
    return; 
  }

// Вызов функции проверки пароля соответсия требованиям
const passwordError = validatePassword(cr_password);
if (passwordError) {
  alert(passwordError);
  return;
}

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

  // проверка на конфликт дублирования
  .then(response => {
    if (!response.ok) {
      return response.json().then(data => {
        if (data.message === 'UNIQUE constraint failed: worker.name') {
          alert('Пользователь с таким логином уже существует. Пожалуйста, выберите другой логин.');
          throw new Error('Duplicate object');
        } else {
          throw new Error('Network response was not ok');
        }
      });
    }
    return response.json();
  })
  .then(data => {
    console.log('Response from server:', data);
    
    const modal = document.querySelector('#createWorkerModal');
    const bsModal = bootstrap.Modal.getInstance(modal);
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