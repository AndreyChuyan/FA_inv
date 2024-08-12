// Получает элемент модального окна с идентификатором 'updateModal' и сохраняет его в переменную updateModal.
const updateModal = document.getElementById('updateModal')
// Проверяет, существует ли вообще такой элемент модального окна. Если элемент найден, то выполняются следующие действия:
if (updateModal) {
  // Добавляет обработчик события 'show.bs.modal' на модальное окно updateModal. 
  // Это событие срабатывает при отображении модального окна перед его показом.
  updateModal.addEventListener('show.bs.modal', event => {
    // Получает кнопку, которая вызвала модальное окно, и сохраняет её в переменную button.
    const button = event.relatedTarget
    // Извлекает информацию из атрибута  кнопки, которая вызвала модальное окно, и сохраняет это значение в переменную name
    const name = button.getAttribute('data-bs-workername')
    const login = button.getAttribute('data-bs-workerlogin')
    const position = button.getAttribute('data-bs-workerposition')
    const description = button.getAttribute('data-bs-workerdescription')
    
    // Обновляет содержимое заголовка модального окна (modalTitle) текстом "New message to " и значением переменной name
    const modalTitle = updateModal.querySelector('.modal-title')
    const modalBodyInputName = updateModal.querySelector('#worker-name')
    const modalBodyInputLogin = updateModal.querySelector('#worker-login')
    const modalBodyInputPosition = updateModal.querySelector('#worker-position')
    const modalBodyInputDescription = updateModal.querySelector('#worker-description')

    // формирует текст  и устанавливает его в соответствующий элемент модального окна modalTitle.
    modalTitle.textContent = `редактирование ${name}`
    // Устанавливает значение в поле ввода (input) модального окна (modalBodyInputName) равным значению переменной name.
    modalBodyInputName.value = name
    modalBodyInputLogin.value = login
    modalBodyInputPosition.value = position
    modalBodyInputDescription.value = description
  })
}