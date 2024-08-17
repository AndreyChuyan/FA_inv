// Получает элемент модального окна с идентификатором 'updateModal' и сохраняет его в переменную updateModal.
const updateModal = document.getElementById('modalUpdate')
// Проверяет, существует ли вообще такой элемент модального окна. Если элемент найден, то выполняются следующие действия:
if (updateModal) {
  // Добавляет обработчик события 'show.bs.modal' на модальное окно updateModal. 
  // Это событие срабатывает при отображении модального окна перед его показом.
  updateModal.addEventListener('show.bs.modal', event => {
    // Получает кнопку, которая вызвала модальное окно, и сохраняет её в переменную button.
    const button = event.relatedTarget
    // Извлекает информацию из атрибута  кнопки, которая вызвала модальное окно, и сохраняет это значение в переменные
    const id                = button.getAttribute('data-bs-id')
    const user              = button.getAttribute('data-bs-user')
    const title             = button.getAttribute('data-bs-title')
    const location          = button.getAttribute('data-bs-location')
    const name              = button.getAttribute('data-bs-name')
    const model             = button.getAttribute('data-bs-model')
    const release           = button.getAttribute('data-bs-release')
    const num_serial        = button.getAttribute('data-bs-num_serial')
    const num_invent        = button.getAttribute('data-bs-num_invent')
    const num_service       = button.getAttribute('data-bs-num_service')
    const price             = button.getAttribute('data-bs-price')
    const formular          = button.getAttribute('data-bs-formular')
    const state             = button.getAttribute('data-bs-state')
    const description       = button.getAttribute('data-bs-description')
    const workerdepartment  = button.getAttribute('data-bs-workerdepartment')
    const user_id           = button.getAttribute('data-bs-user_id')
      

    
    // Обновляет содержимое модального окна 
    const modalTitle = updateModal.querySelector('.modal-title')
    const modalBodyInput_01  = updateModal.querySelector('#arm-id')
    const modalBodyInput_02 = updateModal.querySelector('#arm-department')
    const modalBodyInput_11 = updateModal.querySelector('#arm-user')
    const modalBodyInput_12 = updateModal.querySelector('#arm-title')
    const modalBodyInput_13 = updateModal.querySelector('#arm-location')
    const modalBodyInput_14 = updateModal.querySelector('#arm-name')
    const modalBodyInput_15 = updateModal.querySelector('#arm-model')
    const modalBodyInput_16 = updateModal.querySelector('#arm-release')
    const modalBodyInput_17 = updateModal.querySelector('#arm-num_serial')
    const modalBodyInput_18 = updateModal.querySelector('#arm-num_invent')
    const modalBodyInput_19 = updateModal.querySelector('#arm-num_service')
    const modalBodyInput_20 = updateModal.querySelector('#arm-price')
    const modalBodyInput_21 = updateModal.querySelector('#arm-formular')
    const modalBodyInput_22 = updateModal.querySelector('#arm-state')
    const modalBodyInput_23 = updateModal.querySelector('#arm-description')


    const selectElement = document.getElementById('arm-user')

    console.log(user_id)
    // формирует текст  и устанавливает его в соответствующий элемент модального окна modalTitle.
    modalTitle.textContent = `редактирование компьютера ${title}`
    // Устанавливает значение в поле ввода (input) модального окна 
    modalBodyInput_01.value = id
    modalBodyInput_11.value = user
    modalBodyInput_12.value = title           
    modalBodyInput_13.value = location        
    modalBodyInput_14.value = name            
    modalBodyInput_15.value = model           
    modalBodyInput_16.value = release         
    modalBodyInput_17.value = num_serial      
    modalBodyInput_18.value = num_invent      
    modalBodyInput_19.value = num_service     
    modalBodyInput_20.value = price           
    modalBodyInput_21.value = formular        
    modalBodyInput_22.value = state           
    modalBodyInput_23.value = description     
    modalBodyInput_02.value = workerdepartment

    // значение id пользователя по умолчанию
    selectElement.value = user_id

  })
}