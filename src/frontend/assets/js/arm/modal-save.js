// Получает кнопку "Сохранить" в модальном окне и сохраняет её в переменную saveButton
const saveButton = document.querySelector('#modalUpdate .btn-primary');
// Добавляет обработчик события клика на кнопку "Сохранить"
saveButton.addEventListener('click', () => {
  // Получает значения полей ввода из модального окна
  const id                = document.querySelector('#arm-id').value;
  const id_worker         = document.querySelector('#arm-user').value;
  const title             = document.querySelector('#arm-title').value;
  const location          = document.querySelector('#arm-location').value;
  const name              = document.querySelector('#arm-name').value;
  const model             = document.querySelector('#arm-model').value;
  const release           = document.querySelector('#arm-release').value;
  const num_serial        = document.querySelector('#arm-num_serial').value;
  const num_invent        = document.querySelector('#arm-num_invent').value;
  const num_service       = document.querySelector('#arm-num_service').value;
  const price             = document.querySelector('#arm-price').value;
  const formular          = document.querySelector('#arm-formular').value;
  const state             = document.querySelector('#arm-state').value;
  const description       = document.querySelector('#arm-description').value;
  const department        = document.querySelector('#arm-department').value;
  // Передает значения полей в роутер с параметрами
  // Собрать данные, которые вы хотите отправить на сервер, в объект JavaScript:
  const data = {
    title       : title       ,
    location    : location    ,
    name        : name        ,
    model       : model       ,
    release     : release     ,
    num_serial  : num_serial  ,
    num_invent  : num_invent  ,
    num_service : num_service ,
    price       : price       ,
    formular    : formular    ,
    state       : state       ,
    description : description ,
    description2: ""          ,
    description3: ""          ,
    id_worker   : id_worker   
  };
  console.log(data)

  // создать объект запроса и настроить его для отправки POST-запроса с данными в формате JSON
  fetch('/arm/' + id, {
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
    const modal = document.querySelector('#modalUpdate');
    const bsModal = new bootstrap.Modal(modal);
    bsModal.hide();

  // Устанавливаем задержку перед обновлением страницы
  setTimeout(() => {
    // Обновляем текущую страницу
    window.location.reload();
  }, 500); // 1 секунда
})

