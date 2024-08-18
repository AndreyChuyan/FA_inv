// // Функция модернизации данных
// function modeData() {
// // Получаем значения полей формы
// const formData = {
//   role: document.querySelector('#worker-role').value.trim(),
//   fio: document.querySelector('#worker-fio').value.trim(),
//   name: document.querySelector('#worker-name').value.trim(),
//   position: document.querySelector('#worker-position').value.trim(),
//   description: document.querySelector('#worker-description').value.trim(),
//   department: document.querySelector('#worker-department').value.trim(),
//   password: document.querySelector('#worker-password').value.trim(),
// };
//   // Получаем id отдельно
//   const id = document.querySelector('#worker-id').value.trim();

//   // Проверки на пустое значение (и пробелы)
//   if (!formData.name) { 
//     return alert("Пожалуйста, заполните поле - Логин:");
//   }
//   // if (!formData.password) { 
//   //   return alert("Пожалуйста, заполните поле - Пароль:");
//   // }

//   // добавим статичные значения в запрос
//   const data = {
//     ...formData,
//     // role: "guest"
//   };
//   console.log({ id, ...formData });

//   // делаем запрос в бекенд
//   fetch('/worker/' + id, {
//   method: 'PUT',
//   headers: {
//     'Content-Type': 'application/json'
//   },
//   body: JSON.stringify(data)
//   })
//   .then(response => {
//     if (!response.ok) {
//       return response.json().then(data => {
//         if (data.message === 'UNIQUE constraint failed: worker.name') {
//           alert('Пользователь с таким логином уже существует. Пожалуйста, выберите другой логин.');
//           throw new Error('Duplicate user');
//         } else {
//           throw new Error('Network response was not ok');
//         }
//       });
//     }
//     return response.json();
//   })
//   .then(data => {
//   console.log('Response from server:', data);

//     // Закрываем модальное окно после успешного запроса
//     const modal = document.querySelector('#modal_update');
//     const bsModal = bootstrap.Modal.getInstance(modal);
//     bsModal.hide();

//     // Устанавливаем задержку перед обновлением страницы
//     setTimeout(() => {
//       window.location.reload();
//     }, 500); // 0.5 секунды
//   })
//   .catch(error => {
//     console.error('There was a problem with the fetch operation:', error);
//   });
// }

// //
// // Привязываем функцию сохранения данных к кнопке сохранения
// const saveButtonUpdate = document.querySelector('#modal_update .btn-primary');
// if (saveButtonUpdate) {
//   saveButtonUpdate.addEventListener('click', modeData);
// }

// Получаем элемент модального окна с идентификатором 'modal_update'
const updateModal = document.getElementById('modal_update');

if (updateModal) {
  // Обработчик события 'show.bs.modal' на модальное окно updateModal
  updateModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    
    // Извлекаем информацию из атрибутов кнопки
    const { bs1: name, bs2: fio, bs3: position, bs4: description, bs5: id, bs6: department, bs7: role } = button.dataset;

    // Получаем элементы модального окна
    const modalElements = {
      roleInput: updateModal.querySelector('#worker-role'),
      title: updateModal.querySelector('.modal-title'),
      fioInput: updateModal.querySelector('#worker-name'),
      nameInput: updateModal.querySelector('#worker-fio'),
      positionInput: updateModal.querySelector('#worker-position'),
      descriptionInput: updateModal.querySelector('#worker-description'),
      idInput: updateModal.querySelector('#worker-id'),
      departmentInput: updateModal.querySelector('#worker-department')
    };

    // Устанавливаем значения в элементы модального окна
    modalElements.title.textContent = `редактирование ${name}`;
    modalElements.roleInput.value = role;
    modalElements.nameInput.value = name;
    modalElements.fioInput.value = fio;
    modalElements.positionInput.value = position;
    modalElements.descriptionInput.value = description;
    modalElements.idInput.value = id;
    modalElements.departmentInput.value = department;
  });

  // Функция модернизации данных
  function modeData() {
    // Получаем значения полей формы
    const formData = {
      role: document.querySelector('#worker-role').value.trim(),
      fio: document.querySelector('#worker-fio').value.trim(),
      name: document.querySelector('#worker-name').value.trim(),
      position: document.querySelector('#worker-position').value.trim(),
      description: document.querySelector('#worker-description').value.trim(),
      department: document.querySelector('#worker-department').value.trim(),
      password: document.querySelector('#worker-password').value.trim(),
    };
    // Получаем id отдельно
    const id = document.querySelector('#worker-id').value.trim();

    // Проверки на пустое значение (и пробелы)
    if (!formData.name) {
      return alert("Пожалуйста, заполните поле - Логин:");
    }

    // добавим статичные значения в запрос
    const data = {
      ...formData,
      // role: "guest"
    };
    console.log({ id, ...formData });

    // делаем запрос в бекенд
    fetch('/worker/' + id, {
      method: 'PUT',
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

        // Закрываем модальное окно после успешного запроса
        const modal = document.querySelector('#modal_update');
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
    // Привязываем функцию сохранения данных к кнопке сохранения
    const saveButtonUpdate = document.querySelector('#modal_update .btn-primary');
    if (saveButtonUpdate) {
      saveButtonUpdate.addEventListener('click', modeData);
    }
  }