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
  
    // Проверки на пустое значение (и пробелы)
    if (!title.trim()) { 
      alert("Пожалуйста, заполните поле - Учетное имя");
      return; 
    }
  
    // Проверка на наличие ровно 4 знаков
    if (title.trim().length < 6) {
      alert("Учетное имя должно содержать не меньше 6 знаков");
      return;
    }
  
    // Проверки на пустое значение (и пробелы)
    if (!location.trim()) { 
      alert("Пожалуйста, заполните поле - Расположение");
      return; 
    }
  
      // Проверки на пустое значение (и пробелы)
      if (!name.trim()) { 
          alert("Пожалуйста, заполните поле - Название");
          return; 
          }
  
      // Проверки на пустое значение (и пробелы)
      if (!num_serial.trim()) { 
          alert("Пожалуйста, заполните поле - Заводской номер");
          return; 
        }
  
    
  
  
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
  // проверка на конфликт дублирования
  .then(response => {
    if (!response.ok) {
        return response.json().then(data => {
            if (data.message === 'UNIQUE constraint failed: arm.title') {
                alert('Компьютер с таким учетным именем уже существует. Пожалуйста, выберите другое имя.');
                throw new Error('Duplicate object');
            } else {
                throw new Error('Network response was not ok');
            }
        });
    }
    // только если запрос прошел успешно, возвращаем данные
    return response.json();
  })
  .then(data => {
      console.log('Response from server:', data);

      const modal = document.querySelector('#modalUpdate');
      const bsModal = bootstrap.Modal.getInstance(modal);
      
      // только если запрос прошел успешно без конфликтов, закрываем модальное окно
      bsModal.hide();
      
      // Устанавливаем задержку перед обновлением страницы
      setTimeout(() => {
          // Обновляем текущую страницу
          window.location.reload();
      }, 500); // 0.5 секунды
  })
  .catch(error => {
      console.error('There was a problem with fetch operation:', error);
  });
});

