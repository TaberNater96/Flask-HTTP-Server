document.addEventListener('DOMContentLoaded', function() {
    // Immediately fetches and displays existing TODO items when the page loads.
    fetchTodos();

    // Attaches an event listener to the form used for creating new TODOs.
    // When the form is submitted, it prevents the default form submission (which would cause a page reload) and instead calls the createTodo function to handle the creation asynchronously.
    document.getElementById('create-todo-form').addEventListener('submit', function(event) {
        event.preventDefault(); // prevents the default page reload on form submission
        createTodo();
    });
});

// Fetches all TODO items from the server API and updates the list displayed on the page.
function fetchTodos() {
    const todoList = document.getElementById('todo-list'); // the HTML element where TODOs will be displayed
    const loading = document.getElementById('loading'); // will display "loading..." while the items are being fetched

    // Makes an asynchronous HTTP GET request to the '/api/todos' endpoint.
    fetch('/api/todos')
        .then(response => {
            // Checks if the server's response was successful (such HTTP status 200-299).
            if (!response.ok) {
                // If the response is not ok, an error is thrown to be caught by the .catch block.
                throw new Error('Network response was not ok');
            }
            // Parses the response body from JSON format into a JavaScript array or object.
            return response.json();
        })
        .then(todos => {
            // This block executes if the fetch and JSON parsing were successful.
            loading.style.display = 'none'; // hides the loading indicator once todo items are parsed
            todoList.innerHTML = ''; // clears any existing content from the TODO list.

            // If there are no TODOs, it displays a message indicating that.
            if (todos.length === 0) {
                todoList.innerHTML = '<p>No TODOs found. Create your first one above!</p>'
                return;
            }

            // Iterates over each TODO item received from the server.
            todos.forEach(todo => {
                // For each TODO, creates a corresponding HTML element.
                const todoItem = createTodoElement(todo);
                todoList.appendChild(todoItem);
            });
        })
        .catch(error => {
            // Executes if any error occurred during the fetch operation.
            loading.style.display = 'none';
            console.error('Error fetching TODOs:', error);
            todoList.innerHTML = '<p>Error loading TODOs. Please try again later.</p>';
        });
}

// Gathers data from the create TODO form and sends it to the server to create a new TODO item.
function createTodo() {
    // Retrieves the values entered by the user in the title and description input fields.
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;

    // Makes an asynchronous HTTP POST request to the '/api/todos' endpoint.
    fetch('/api/todos', {
        method: 'POST',
        headers: {
            // Tells the server that the request body is in JSON format.
            'Content-Type': 'application/json',
        },
        // Converts the JavaScript object containing title, description, and initial completed status into a JSON string to be sent as the request body.
        body: JSON.stringify({
            title: title,
            description: description,
            completed: false // new TODOs are initially marked as not completed.
        }),
    })
    .then(response => {
        // Checks if the server's response was successful.
        if (!response.ok) {
            // If not successful, it attempts to parse the error message from the server's JSON response and then throws an error to be caught by the .catch block.
            return response.json().then(err => { throw err; });
        }
        return response.json();
    })
    .then(newTodo => {
        // Executes if the TODO creation was successful and clears the input fields in the form.
        document.getElementById('title').value = '';
        document.getElementById('description').value = '';

        // Refreshes the entire list of TODOs to include the newly added item.
        fetchTodos();
    })
    .catch(error => {
        console.error('Error creating todo:', error); // logs the error
        alert('Failed to create TODO: ' + (error.message || 'Unknown error'));
    })
}

// Sends updated data for a specific TODO item to the server, where 'id' is the unique identifier and 'data' is an object containing the fields to be updated
function updateTodo(id, data) {
    // Makes an asynchronous HTTP PUT request to '/api/todos/{id}' endpoint.
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
        // If successful, parse the server's response (updated TODO item) from JSON.
        return response.json();
    })
    .then(updatedTodo => {
        // After a successful update, refresh the entire TODO list to reflect the changes.
        fetchTodos();
    })
    .catch(error => {
        console.error('Error updating todo:', error); // Log the error
        // Alert the user about the failure to update.
        alert('Failed to update TODO: ' + (error.message || 'Unknown error'));
    });
}

// Sends a request to the server to delete a specific TODO item.
function deleteTodo(id) {
    // Asks the user for confirmation before proceeding with the deletion.
    if (!confirm('Are you sure you want to delete this TODO?')) {
        return; // if the user cancels, do nothing.
    }
    
    // Makes an asynchronous HTTP DELETE request to '/api/todos/{id}'.
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
        // After successful deletion, refresh the TODO list.
        fetchTodos();
    })
    .catch(error => {
        console.error('Error deleting todo:', error); // Log the error.
        alert('Failed to delete TODO: ' + (error.message || 'Unknown error'));
    });
}

// Toggles the completion status of a TODO item (such as 'incomplete' to 'complete').
function toggleTodoStatus(id, currentStatus) {
    // The new status is the opposite of the current status.
    updateTodo(id, { completed: !currentStatus});
}

// Creates and returns an HTML list item (<li>) element representing a single TODO item.
function createTodoElement(todo) {
    // Create the main list item (<li>).
    const li = document.createElement('li');
    // Assign CSS classes for styling. If the TODO is completed, an additional class 'todo-completed' is added.
    li.className = `todo-item ${todo.completed ? 'todo-completed' : ''}`;
    // Store the TODO's id as a data attribute on the element, useful for later retrieval.
    li.dataset.id = todo.id;

    // Create a <div> to display the TODO's title.
    const title = document.createElement('div');
    title.className = 'todo-title';
    title.textContent = todo.title;

    // Create a <div> to display the TODO's description.
    const description = document.createElement('div');
    description.className = 'todo-description';
    description.textContent = todo.description || 'No description'; // display a default if no description.

    // Create a <div> to display creation and update timestamps.
    const timestamps = document.createElement('div');
    timestamps.className = 'timestamp';
    timestamps.textContent = `Created: ${formatDate(todo.created_at)}`; // format and display creation date.
    if (todo.updated_at) {
        // If an update timestamp exists, format and append it.
        timestamps.textContent += ` | Updated: ${formatDate(todo.updated_at)}`;
    }

    // Create a <div> to hold action buttons (toggle, edit, delete).
    const actions = document.createElement('div');
    actions.className = 'todo-actions';

    // Create the "Mark Complete" / "Mark Incomplete" button.
    const toggleBtn = document.createElement('button');
    toggleBtn.className = 'toggle-button';
    toggleBtn.textContent = todo.completed ? 'Mark Incomplete' : 'Mark Complete'; // text depends on current status.
    // When clicked, this button calls toggleTodoStatus with the TODO's id and current completion status.
    toggleBtn.onclick = function() {
        toggleTodoStatus(todo.id, todo.completed);
    };
    
    // Create the "Edit" button.
    const editBtn = document.createElement('button');
    editBtn.className = 'edit-button';
    editBtn.textContent = 'Edit';
    // When clicked, this button shows or hides the inline edit form for this TODO item.
    editBtn.onclick = function() {
        const editForm = li.querySelector('.edit-form'); // find the edit form within this <li>.
        // Toggle the display style between 'block' (visible) and 'none' (hidden).
        editForm.style.display = editForm.style.display === 'block' ? 'none' : 'block';
    };
    
    // Create the "Delete" button.
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-button';
    deleteBtn.textContent = 'Delete';
    // When clicked, this button calls the deleteTodo function with the TODO's id.
    deleteBtn.onclick = function() {
        deleteTodo(todo.id);
    };
    
    // Add the created buttons to the 'actions' <div>.
    actions.appendChild(toggleBtn);
    actions.appendChild(editBtn);
    actions.appendChild(deleteBtn);

    // Create the inline form for editing a TODO item. This form is initially hidden.
    const editForm = document.createElement('div');
    editForm.className = 'edit-form';
    // Set the inner HTML of the form, including input fields for title and description, and Save/Cancel buttons.
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

    // Append all created parts (title, description, timestamps, actions, edit form) to the main list item (<li>).
    li.appendChild(title);
    li.appendChild(description);
    li.appendChild(timestamps);
    li.appendChild(actions);
    li.appendChild(editForm);

    // Add event listener for the "Save Changes" button within the edit form.
    editForm.querySelector('.save-button').addEventListener('click', function() {
        // Get the new title and description from the edit form's input fields.
        const newTitle = document.getElementById(`edit-title-${todo.id}`).value;
        const newDescription = document.getElementById(`edit-description-${todo.id}`).value;

        // Call updateTodo to send the changes to the server.
        updateTodo(todo.id, {
            title: newTitle,
            description: newDescription
        });

        // Hide the edit form after saving.
        editForm.style.display = 'none';
    });

    // Add event listener for the "Cancel" button within the edit form.
    editForm.querySelector('.cancel-button').addEventListener('click', function() {
        // Simply hide the edit form without saving changes.
        editForm.style.display = 'none';
    });

    // Return the fully constructed list item (<li>) element.
    return li;
}

// Utility function to format a date string into a more human-readable local date format. The 'dateString' is expected to be a string that can be parsed by the Date constructor (e.g., ISO 8601 format).
function formatDate(dateString) {
    if (!dateString) return 'Unknown'; // if the date string is null or empty, return 'Unknown'.
    const date = new Date(dateString);
    // Convert the date to a string using the locale-specific date format (e.g., "MM/DD/YYYY" in the US).
    return date.toLocaleDateString();
}