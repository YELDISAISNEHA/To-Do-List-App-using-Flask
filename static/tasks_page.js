function deleteTask(taskId) {
    fetch(`/delete_task/${taskId}`, {method: "DELETE"})
    .then(Response => Response.json())
    .then(data => {
        if (data.status === "success") {
            document.getElementById(taskId).remove();
        } else {
            alert("Error: " + data.message);
        }
    });
}