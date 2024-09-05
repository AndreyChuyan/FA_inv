const createModal = document.getElementById('modalCreateArm')
// Проверяет, существует ли вообще такой элемент модального окна. Если элемент найден, то выполняются следующие действия:
if (createModal) {
  // Добавляет обработчик события 'show.bs.modal' на модальное окно updateModal. 
  // Это событие срабатывает при отображении модального окна перед его показом.
  createModal.addEventListener('show.bs.modal', event => {
    // Получает кнопку, которая вызвала модальное окно, и сохраняет её в переменную button.
    const button = event.relatedTarget
    // Извлекает информацию из атрибута  кнопки, которая вызвала модальное окно, и сохраняет это значение в переменные
    const department = button.getAttribute('data-bs-department-arm')

    // Обновляет содержимое заголовка модального окна (modalTitle)
    const modalTitle = createModal.querySelector('.modal-title')
    const modalBodyInputDepartment = createModal.querySelector('#cr-department-arm')
    console.log('modalBodyInputDepartment:', modalBodyInputDepartment);
    
    // формирует текст  и устанавливает его в соответствующий элемент модального окна modalTitle.
    modalTitle.textContent = `Добавление компьютера`
    // Устанавливает значение в поле ввода (input) модального окна (modalBodyInputName) равным значению переменной name.
    modalBodyInputDepartment.value = department

  })
}