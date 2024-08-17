const createModal = document.getElementById('createWorkerModal')
// Проверяет, существует ли вообще такой элемент модального окна. Если элемент найден, то выполняются следующие действия:
if (createModal) {
  // Добавляет обработчик события 'show.bs.modal' на модальное окно updateModal. 
  // Это событие срабатывает при отображении модального окна перед его показом.
  createModal.addEventListener('show.bs.modal', event => {
    // Получает кнопку, которая вызвала модальное окно, и сохраняет её в переменную button.
    const button = event.relatedTarget
    // Извлекает информацию из атрибута  кнопки, которая вызвала модальное окно, и сохраняет это значение в переменные
    const department = button.getAttribute('data-bs-workerdepartment')


    // Обновляет содержимое заголовка модального окна (modalTitle) текстом "New message to " и значением переменной name
    const modalTitle = createModal.querySelector('.modal-title')
    const modalBodyInputDepartment = createModal.querySelector('#worker-cr-department')

    // формирует текст  и устанавливает его в соответствующий элемент модального окна modalTitle.
    modalTitle.textContent = `Создание нового пользователя`
    // Устанавливает значение в поле ввода (input) модального окна (modalBodyInputName) равным значению переменной name.
    modalBodyInputDepartment.value = department

  })
}