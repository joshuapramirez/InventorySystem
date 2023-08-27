
function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function closeModal(event) {
    const isModalContainer = event.target.id === 'modal-container';
    const isConfirmButton = event.target.classList.contains('confirm-sale-button') || event.target.classList.contains('confirm-stock-button');

    if (isModalContainer || isConfirmButton) {
        const modalContainer = document.querySelector('.modal-container');
        modalContainer.style.display = 'none'; // Hide the modal
    }
}


function confirmSale(event, id) {
    event.stopPropagation();
    const addSaleInput = document.getElementById(`add-sale-input-modal-${id}`);
    const quantitySoldDiv = document.getElementById(`quantity-sold-${id}`);
    const salesDiv = document.getElementById(`sales-${id}`);
    const stockDiv = document.getElementById(`quantity-in-stock-${id}`);
    const confirmButton = event.target;

    const saleQuantity = parseInt(addSaleInput.value, 10);
    const currentQuantitySold = parseInt(quantitySoldDiv.textContent, 10);
    const currentSales = parseFloat(salesDiv.textContent);
    const currentStock = parseInt(stockDiv.textContent, 10);

    if (!isNaN(saleQuantity) && saleQuantity >= 0 && saleQuantity <= currentStock) {
        // Make a fetch request to update the inventory
        fetch(`/inventory/confirm_sale/${id}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                sale_quantity: saleQuantity,
            }),
        })
        .then(response => response.json())
        .then(result => {

            if (result.success) {
                // Update the values in the DOM
                quantitySoldDiv.textContent = result.quantity_sold;
                salesDiv.textContent = '$' + result.sales;
                stockDiv.textContent = result.quantity_in_stock;
            } else {
                console.error("Failed to update inventory:", result.message);
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
    }

    closeModal(event);
}

function confirmStock(event, id) {
    event.stopPropagation();
    const addStockInput = document.getElementById(`add-stock-input-modal-${id}`);
    const stockDiv = document.getElementById(`quantity-in-stock-${id}`);
    const confirmButton = event.target;

    const addStockQuantity = parseInt(addStockInput.value, 10);
    const currentStock = parseInt(stockDiv.textContent, 10);

    if (!isNaN(addStockQuantity)) {
        // Make a fetch request to update the inventory
        fetch(`/inventory/confirm_stock/${id}`, {
            method: "POST",
            headers: {
                "Content-type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                add_stock_quantity: addStockQuantity,
            }),
        })
        .then(response => response.json())
        .then(result => {

            if (result.success) {
                // Update the values in the DOM
                stockDiv.textContent = result.updated_quantity_in_stock;
            } else {
                console.error("Failed to update inventory:", result.message);
            }
        })
        .catch(error => {
            console.error("Fetch error:", error);
        });
    }

    closeModal(event);
}

document.addEventListener("DOMContentLoaded", function() {

    function addStock(event, id) {
        event.stopPropagation();
        console.log("Add stock for product ID:", id);
        showAddStockForm(id);
    }

    function addSale(event, id) {
        event.stopPropagation();
        showAddSaleForm(id);
    }

    function redirectToProduct(id) {
        console.log("Navigate to per_product page for product ID:", id);
        const url = `/inventory/per_product/${id}`;
        window.location.href = url;
    }

    function showAddSaleForm(id) {
        const existingModal = document.getElementById('modal-container');
        if (existingModal) {
            document.body.removeChild(existingModal);
        }

        const modalContainer = document.createElement('div');
        modalContainer.classList.add('modal-container');
        modalContainer.setAttribute('id', 'modal-container');

        const addSaleForm = document.getElementById(`add-sale-form-${id}`)?.cloneNode(true);
        if (addSaleForm) {
            const clonedAddSaleInput = addSaleForm.querySelector('input');
            clonedAddSaleInput.setAttribute('id', `add-sale-input-modal-${id}`);
            addSaleForm.style.display = 'block';

            modalContainer.appendChild(addSaleForm);
            document.body.appendChild(modalContainer);
            modalContainer.addEventListener('click', closeModal);

            console.log("Open sale form for product ID:", id);
        }
    }

    function showAddStockForm(id) {
        const existingModal = document.getElementById('modal-container');
        if (existingModal) {
            document.body.removeChild(existingModal);
        }

        const modalContainer = document.createElement('div');
        modalContainer.classList.add('modal-container');
        modalContainer.setAttribute('id', 'modal-container');

        const addStockForm = document.getElementById(`add-stock-form-${id}`)?.cloneNode(true);
        if (addStockForm) {
            const clonedAddStockInput = addStockForm.querySelector('input');
            clonedAddStockInput.setAttribute('id', `add-stock-input-modal-${id}`);
            addStockForm.style.display = 'block';

            modalContainer.appendChild(addStockForm);
            document.body.appendChild(modalContainer);
            modalContainer.addEventListener('click', closeModal);

            console.log("Open stock form for product ID:", id);
        }
    }

    const inventoryTableBody = document.getElementById("inventory-table-body");
    if (inventoryTableBody) {
        inventoryTableBody.addEventListener("click", function(event) {
            const target = event.target;

            // Handle button and icon clicks
            if (target.matches(".add-stock-button, .add-sale-button, .add-stock-icon, .add-sale-icon")) {
                const productId = target.getAttribute("data-product-id");
                if (target.matches(".add-stock-button, .add-stock-icon")) {
                    addStock(event, productId);
                } else if (target.matches(".add-sale-button, .add-sale-icon")) {
                    addSale(event, productId);
                }
                return;
            }

            const tr = target.closest("tr");
            if (tr) {
                const productId = tr.getAttribute("data-product-id");
                redirectToProduct(productId);
            }
        });
    }

    function closeModal(event) {
        if (event.target.classList.contains('modal-container')) {
            document.body.removeChild(event.target);
        }
    }
});
