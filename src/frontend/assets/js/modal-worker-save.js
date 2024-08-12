// Получает кнопку "Сохранить" в модальном окне и сохраняет её в переменную saveButton
const saveButton = document.querySelector('#updateModal .btn-primary');
//document.querySelector('#worker-id').value = workerId
// Добавляет обработчик события клика на кнопку "Сохранить"
saveButton.addEventListener('click', () => {
  // Получает значения полей ввода из модального окна
  const login = document.querySelector('#worker-login').value;
  const name = document.querySelector('#worker-name').value;
  const position = document.querySelector('#worker-position').value;
  const description = document.querySelector('#worker-description').value;
  const id = document.querySelector('#worker-id').value;
  const department = document.querySelector('#worker-department').value;

  // Передает значения полей в роутер с параметрами
  // Собрать данные, которые вы хотите отправить на сервер, в объект JavaScript:
  const data = {
    role: "guest",
    login: login,
    name: name,
    password: "",
    department: department,
    position: position,
    description: description
  };
  // console.log(data)

  // создать объект запроса и настроить его для отправки POST-запроса с данными в формате JSON
  fetch('/worker/update/' + id, {
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
})
.catch(error => {
  console.error('There was a problem with fetch operation:', error);
});
  // Замените /your-route на путь к вашему роутеру
  // window.location.href = `/your-route?id=${id}&login=${login}&name=${name}&position=${position}&description=${description}`;
});