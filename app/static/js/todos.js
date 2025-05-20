document.addEventListener('DOMContentLoaded', function() {
    fetchTodos();

    document.getElementById('create-todo-form').addEventListener('submit', function(event) {
        event.preventDefault();
        createTodo();
    });
});

function fetchTodos() {
    const todoList = document.getElementById('todo-list');
    const loading = document.getElementById('loading');

    fetch('/api/todos')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(todos => {
            loading.style.display = 'none';
            todoList.innerHTML = '';

            if (todos.length === 0) {
                todoList.innerHTML = '<p>No TODOs found. Create your first one above!</p>'
                return;
            }

            todos.forEach(todo => {
                const todoItem = createTodoElement(todo);
                todoList.appendChild(todoItem);
            });
        })
        .catch(error => {
            loading.style.display = 'none';
            console.error('Error fetching TODOs:', error);
            todoList.innerHTML = '<p>Error loading TODOs. Please try again later.</p>';
        });
}

function createTodo() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    fetch('/api/todos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            title: title,
            description: description,
            completed: false
        }),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(newTodo => {
        document.getElementById('title').value = '';
        document.getElementById('description').value = '';

        // Refresh the todo list
        fetchTodos();
    })
    .catch(error => {
        console.error('Error creating todo:', error);
        alert('Failed to create TODO: ' + (error.message || 'Unknown error'));
    })
}

function updateTodo(id, data) {
    fetch(`/api/todos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(updatedTodo => {
        fetchTodos(); // refresh the list
    })
    .catch(error => {
        console.error('Error updating todo:', error);
        alert('Failed to update TODO: ' + (error.message || 'Unknown error'));
    });
}

function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this TODO?')) {
        return;
    }
    
    fetch(`/api/todos/${id}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        fetchTodos(); // refresh the list
    })
    .catch(error => {
        console.error('Error deleting todo:', error);
        alert('Failed to delete TODO: ' + (error.message || 'Unknown error'));
    });
}

// Toggle TODO completion status
function toggleTodoStatus(id, currentStatus) {
    updateTodo(id, { completed: !currentStatus});
}

// Create DOM element for a TODO item
function createTodoElement(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.completed ? 'todo-completed' : ''}`;
    li.dataset.id = todo.id;

    const title = document.createElement('div');
    title.className = 'todo-title';
    title.textContent = todo.title;

    const description = document.createElement('div');
    description.className = 'todo-description';
    description.textContent = todo.description || 'No description';

    const timestamps = document.createElement('div');
    timestamps.className = 'timestamp';
    timestamps.textContent = `Created: ${formatDate(todo.created_at)}`;
    if (todo.updated_at) {
        timestamps.textContent += ` | Updated: ${formatDate(todo.updated_at)}`;
    }

    const actions = document.createElement('div');
    actions.className = 'todo-actions';

    // Toggle status button
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toggle-button';
    toggleBtn.textContent = todo.completed ? 'Mark Incomplete' : 'Mark Complete';
    toggleBtn.onclick = function() {
        toggleTodoStatus(todo.id, todo.completed);
    };
    
    // Edit button
    const editBtn = document.createElement('button');
    editBtn.className = 'edit-button';
    editBtn.textContent = 'Edit';
    editBtn.onclick = function() {
        const editForm = li.querySelector('.edit-form');
        editForm.style.display = editForm.style.display === 'block' ? 'none' : 'block';
    };
    
    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-button';
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = function() {
        deleteTodo(todo.id);
    };
    
    actions.appendChild(toggleBtn);
    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    // Edit form
    const editForm = document.createElement('div');
    editForm.className = 'edit-form';
    editForm.innerHTML = `
        <div>
            <label for="edit-title-${todo.id}">Title:</label>
            <input type="text" id="edit-title-${todo.id}" value="${todo.title}" required>
        </div>
        <div>
            <label for="edit-description-${todo.id}">Description:</label>
            <textarea id="edit-description-${todo.id}">${todo.description || ''}</textarea>
        </div>
        <div class="todo-actions">
            <button type="button" class="save-button">Save Changes</button>
            <button type="button" class="cancel-button">Cancel</button>
        </div>
    `;

    // Add event listeners to edit form buttons
    li.appendChild(title);
    li.appendChild(description);
    li.appendChild(timestamps);
    li.appendChild(actions);
    li.appendChild(editForm);

    // Save button logic
    editForm.querySelector('.save-button').addEventListener('click', function() {
        const newTitle = document.getElementById(`edit-title-${todo.id}`).value;
        const newDescription = document.getElementById(`edit-description-${todo.id}`).value;

        updateTodo(todo.id, {
            title: newTitle,
            description: newDescription
        });

        editForm.style.display = 'none';
    });

    // Cancel button logic
    editForm.querySelector('.cancel-button').addEventListener('click', function() {
        editForm.style.display = 'none';
    });

    return li;
}

function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}