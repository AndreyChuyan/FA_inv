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

  // Проверки на пустое значение (и пробелы)
  if (!name.trim()) { 
    alert("Пожалуйста, заполните поле - Логин:");
    return; 
  }



  // Передает значения полей в роутер с параметрами
  // Собрать данные, которые вы хотите отправить на сервер, в объект JavaScript:
  const data = {
    // role: role,
    fio: fio,
    name: name,
    // password: "",
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

  // Устанавливаем задержку перед обновлением страницы
  setTimeout(() => {
    // Обновляем текущую страницу
    window.location.reload();
  }, 500); // 1 секунда
})
