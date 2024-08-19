//
// Обрабатываем открытие модального окна для создания пользователя.
const createModal = document.getElementById('modal_create');
if (createModal) {
  // Добавляем обработчик события 'show.bs.modal' на модальное окно.
  createModal.addEventListener('show.bs.modal', (event) => {
    // Получаем кнопку, вызвавшую модальное окно, и извлекаем информацию из её атрибутов.
    const { relatedTarget: button } = event;
    const department = button.getAttribute('bs-department');

    // Находим элементы внутри модального окна и обновляем их содержимое.
    const modalTitle = createModal.querySelector('.modal-title');
    const modalBodyInputDepartment = createModal.querySelector('#cr-department');
    
    modalTitle.textContent = 'Создание нового пользователя';
    modalBodyInputDepartment.value = department;
  });
}


//
// Функция сохранения данных
function saveData() {
  // Получаем значения полей формы
  const formData = {
    role: document.querySelector('#worker-cr-role').value.trim(),
    fio: document.querySelector('#worker_cr_fio').value.trim(),
    name: document.querySelector('#worker-cr-name').value.trim(),
    position: document.querySelector('#worker-cr-position').value.trim(),
    description: document.querySelector('#worker-cr-description').value.trim(),
    department: document.querySelector('#worker-cr-department').value.trim(),
    password: document.querySelector('#worker-cr-password').value.trim()
  };

  // Проверки на пустое значение
  if (!formData.department) {
    return alert("Пожалуйста, заполните поле - Подразделение");
  }
  if (!formData.name) {
    return alert("Пожалуйста, заполните поле - Логин");
  }
  if (!formData.password) {
    return alert("Пожалуйста, заполните поле - Пароль");
  }

  // добавим статичные значения в запрос
  const data = {
    ...formData,
    // role: "user"
  };

  console.log('data:', data);

  // делаем запрос в бекенд
  fetch('/worker/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
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
    
    const modal = document.querySelector('#modal_create');
    const bsModal = bootstrap.Modal.getInstance(modal);
    bsModal.hide();

    // Устанавливаем задержку перед обновлением страницы
    setTimeout(() => {
      window.location.reload();
    }, 500); // 0.5 секунды
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });
}

//
// Привязываем функцию сохранения данных к кнопке сохранения
const saveButtonCreate = document.querySelector('#modal_create .btn-primary');
if (saveButtonCreate) {
  saveButtonCreate.addEventListener('click', saveData);
}