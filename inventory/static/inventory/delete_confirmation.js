// Open the delete confirmation modal
function openDeleteModal(productId) {
    var modal = document.getElementById('id01');
    modal.style.display = 'block';
}

// Close the delete confirmation modal
function closeDeleteModal() {
    var modal = document.getElementById('id01');
    modal.style.display = 'none';
}

// Delete the inventory item and redirect to the delete URL
function deleteInventory(productId) {
    var deleteUrl = `/inventory/delete/${productId}`
    console.log(deleteUrl)
    window.location.href = deleteUrl;
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById('id01');
    if (event.target == modal) {
        closeDeleteModal();
    }
}