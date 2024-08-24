// импортировать конкретную функцию (не дефолтную)
import { validatePasswordMode, validateTelephone } from '../../assets/js/validators.js';

// Получает кнопку "Сохранить" в модальном окне и сохраняет её в переменную saveButton
const saveButton = document.querySelector('#updateModal .btn-primary');
// Добавляет обработчик события клика на кнопку "Сохранить"
saveButton.addEventListener('click', () => {
  // Получает значения полей ввода из модального окна
  const fio         = document.querySelector('#worker-fio').value;
  const name        = document.querySelector('#worker-name').value;
  const position    = document.querySelector('#worker-position').value;
  const description = document.querySelector('#worker-description').value;
  const id          = document.querySelector('#worker-id').value;
  const department  = document.querySelector('#worker-department').value;
  const role        = document.querySelector('#worker-role').value;
  const password    = document.querySelector('#worker-password').value;
  // Проверки на пустое значение (и пробелы)
  if (!name.trim()) { 
    alert("Пожалуйста, заполните поле - Логин:");
    return; 
  }

  if (!fio.trim()) { 
    alert("Пожалуйста, заполните поле - Имя");
    return; 
  }

// Вызов функции проверки пароля соответсия требованиям
const passwordError = validatePasswordMode(password);
if (passwordError) {
  alert(passwordError);
  return;
}

if (!position.trim()) { 
  alert("Пожалуйста, заполните поле - Должность");
  return; 
}

  // Вызов функции проверки телефона
  const phoneError = validateTelephone(description);
  if (phoneError) {
    alert(phoneError);
    return;
  }



  // Передает значения полей в роутер с параметрами
  // Собрать данные, которые вы хотите отправить на сервер, в объект JavaScript:
  const data = {
    // role: role,
    fio: fio,
    name: name,
    password: password,
    department: department,
    position: position,
    description: description
  };
  console.log(data)

  // создать объект запроса и настроить его для отправки POST-запроса с данными в формате JSON
  fetch('/worker/' + id, {
  method: 'PUT',
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
          throw new Error('Duplicate user');
        } else {
          throw new Error('Network response was not ok');
        }
      });
    }
    return response.json();
  })
  .then(data => {
    console.log('Response from server:', data);


      // Закрываем модальное окно после успешного запроса
      const modal = document.querySelector('#updateModal');
      const bsModal = new bootstrap.Modal(modal);
      bsModal.hide();

      // Устанавливаем задержку перед обновлением страницы
      setTimeout(() => {
        // Обновляем текущую страницу
        window.location.reload();
      }, 500); // 1 секунда
    })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
});
