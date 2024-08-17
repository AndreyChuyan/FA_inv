// Получает элемент модального окна с идентификатором 'updateModal' и сохраняет его в переменную updateModal.
const updateModal = document.getElementById('updateModal')
// Проверяет, существует ли вообще такой элемент модального окна. Если элемент найден, то выполняются следующие действия:
if (updateModal) {
  // Добавляет обработчик события 'show.bs.modal' на модальное окно updateModal. 
  // Это событие срабатывает при отображении модального окна перед его показом.
  updateModal.addEventListener('show.bs.modal', event => {
    // Получает кнопку, которая вызвала модальное окно, и сохраняет её в переменную button.
    const button = event.relatedTarget
    // Извлекает информацию из атрибута  кнопки, которая вызвала модальное окно, и сохраняет это значение в переменные
    const name = button.getAttribute('data-bs-1')
    const fio = button.getAttribute('data-bs-2')
    const position = button.getAttribute('data-bs-3')
    const description = button.getAttribute('data-bs-4')
    const id = button.getAttribute('data-bs-5')
    const department = button.getAttribute('data-bs-6')
    


    // Обновляет содержимое заголовка модального окна (modalTitle) 
    const modalTitle = updateModal.querySelector('.modal-title')
    const modalBodyInput_Name = updateModal.querySelector('#worker-name')
    const modalBodyInput_fio = updateModal.querySelector('#worker-fio')
    const modalBodyInput_Position = updateModal.querySelector('#worker-position')
    const modalBodyInput_Description = updateModal.querySelector('#worker-description')
    const modalBodyInput_Id = updateModal.querySelector('#worker-id')
    const modalBodyInput_Department = updateModal.querySelector('#worker-department')

    // формирует текст  и устанавливает его в соответствующий элемент модального окна modalTitle.
    modalTitle.textContent = `редактирование ${name}`
    // Устанавливает значение в поле ввода (input) модального окна (modalBodyInputName) равным значению переменной name.
    modalBodyInput_Name.value = name
    modalBodyInput_fio.value = fio
    modalBodyInput_Position.value = position
    modalBodyInput_Description.value = description
    modalBodyInput_Id.value = id
    modalBodyInput_Department.value = department

  })
}