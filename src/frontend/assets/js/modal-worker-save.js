// Получает кнопку "Сохранить" в модальном окне и сохраняет её в переменную saveButton
const saveButton = document.querySelector('#updateModal .btn-primary');
// Добавляет обработчик события клика на кнопку "Сохранить"
saveButton.addEventListener('click', () => {
  // Получает значения полей ввода из модального окна
  const login = document.querySelector('#worker-login').value;
  const name = document.querySelector('#worker-name').value;
  const position = document.querySelector('#worker-position').value;
  const description = document.querySelector('#worker-description').value;
  const id = document.querySelector('#worker-id').value;
  const department = document.querySelector('#worker-department').value;
  const role = document.querySelector('#worker-role').value;

  // Передает значения полей в роутер с параметрами
  // Собрать данные, которые вы хотите отправить на сервер, в объект JavaScript:
  const data = {
    // role: role,
    login: login,
    name: name,
    // password: "",
    department: department,
    position: position,
    description: description
  };
  // console.log(data)

  // создать объект запроса и настроить его для отправки POST-запроса с данными в формате JSON
  fetch('/worker/update/' + id, {
  method: 'PUT',
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
})

 // Закрываем модальное окно после успешного запроса
const modal = document.querySelector('#updateModal');
const bsModal = new bootstrap.Modal(modal);
bsModal.hide();

// Обновляем текущую страницу
window.location.reload();
})

.catch(error => {
  console.error('There was a problem with fetch operation:', error);
});
