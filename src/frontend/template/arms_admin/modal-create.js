const saveButton_create = document.querySelector('#modalCreateArm .btn-primary');

saveButton_create.addEventListener('click', () => {
  const cr1   = document.querySelector('#cr-title').value;
  const cr2   = document.querySelector('#cr-location').value;
  const cr3   = document.querySelector('#cr-name').value;
  const cr4   = document.querySelector('#cr-model').value;
  const cr5   = document.querySelector('#cr-release').value;
  const cr6   = document.querySelector('#cr-num_serial').value;
  const cr7   = document.querySelector('#cr-num_invent').value;
  const cr8   = document.querySelector('#cr-num_service').value;
  const cr9   = document.querySelector('#cr-price').value;
  const cr10  = document.querySelector('#cr-formular').value;
  const cr11  = document.querySelector('#cr-state').value;
  const cr12  = document.querySelector('#cr-description').value;
  const cr13  = document.querySelector('#cr_dep').value;
  const cr14  = document.querySelector('#cr_fio').value;

  console.log('cr_dep:', cr13);

  // Проверки на пустое значение (и пробелы)
  if (!cr1.trim()) { 
    alert("Пожалуйста, заполните поле - Учетное имя");
    return; 
  }

  // Проверка на наличие ровно 4 знаков
  if (cr1.trim().length < 6) {
    alert("Учетное имя должно содержать не меньше 6 знаков");
    return;
  }

  // Проверки на пустое значение (и пробелы)
  if (!cr2.trim()) { 
    alert("Пожалуйста, заполните поле - Расположение");
    return; 
  }

    // Проверки на пустое значение (и пробелы)
    if (!cr3.trim()) { 
        alert("Пожалуйста, заполните поле - Название");
        return; 
        }

    // Проверки на пустое значение (и пробелы)
    if (!cr6.trim()) { 
        alert("Пожалуйста, заполните поле - Заводской номер");
        return; 
      }

  const data = {
    title:          cr1,
    department_arm: cr13,
    location:       cr2,
    name:           cr3,
    model:          cr4,
    release:        cr5,
    num_serial:     cr6,
    num_invent:     cr7,
    num_service:    cr8,
    price:          cr9,
    formular:       cr10,
    state:          cr11,
    description:    cr12,
    description2:   "",
    description3:   "",
    id_worker:      cr14
  };
  console.log('data:', data);

  fetch('/arm/', {
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

      const modal = document.querySelector('#modalCreateArm');
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
