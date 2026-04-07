const addTodoButton = document.getElementById("add-todo");
const todoInput = document.getElementById("todo-input");
const todoList = document.getElementById("todo-list");

// Load existing todos from local storage
window.onload = function () {
  const todos = JSON.parse(localStorage.getItem("todos")) || [];
  todos.forEach((todo) => {
    addTodoToDOM(todo);
  });
};

addTodoButton.addEventListener("click", function () {
  if (todoInput.value) {
    addTodoToDOM(todoInput.value);
    todoInput.value = "";
  }
});

function addTodoToDOM(todo) {
  const todoItem = document.createElement("li");
  todoItem.textContent = todo;
  // Add click event to remove todo
  todoItem.addEventListener("click", function () {
    todoItem.remove();
    updateLocalStorage();
  });
  todoList.appendChild(todoItem);
  updateLocalStorage();
}

function updateLocalStorage() {
  const todos = Array.from(todoList.children).map((li) => li.textContent);
  localStorage.setItem("todos", JSON.stringify(todos));
}
