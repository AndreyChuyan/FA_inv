// Получает кнопку "Сохранить" в модальном окне и сохраняет её в переменную saveButton
const saveButton = document.querySelector('#updateModal .btn-primary');
//document.querySelector('#worker-id').value = workerId
// Добавляет обработчик события клика на кнопку "Сохранить"
saveButton.addEventListener('click', () => {
  // Получает значения полей ввода из модального окна
  const login = document.querySelector('#worker-login').value;
  const name = document.querySelector('#worker-name').value;
  const position = document.querySelector('#worker-position').value;
  const description = document.querySelector('#worker-description').value;
  const id = document.querySelector('#worker-id').value;

  // Передает значения полей в роутер с параметрами
  // Замените /your-route на путь к вашему роутеру
  window.location.href = `/your-route?id=${id}&login=${login}&name=${name}&position=${position}&description=${description}`;
});