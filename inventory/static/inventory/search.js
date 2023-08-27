function openSuggestedProductModal(productName) {
    const modal = document.getElementById('suggestedProductModal');
    const suggestedProductName = document.getElementById('suggestedProductName');

    suggestedProductName.textContent = productName;
    modal.style.display = 'block';
}

function closeSuggestedProductModal() {
    const modal = document.getElementById('suggestedProductModal');
    modal.style.display = 'none';
}

function redirectToProduct(pk) {
    const suggestedProductPk = parseInt(pk);
    window.location.href = `/inventory/per_product/${suggestedProductPk}`;  // Redirect to the product page using the primary key
}

function displayMessage(content) {
    const messagesContainer = document.getElementById('messagesContainer');

    // Clear the container before appending a new message
    messagesContainer.innerHTML = '';

    const messageDiv = document.createElement('div');
    messageDiv.textContent = content;
    messagesContainer.appendChild(messageDiv);

    messagesContainer.removeAttribute('hidden'); // Show the messages container
}


//Make an AJAX call to get the suggested product data and trigger modal if needed

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchButton = document.getElementById('searchButton');

    if (searchForm && searchButton) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const messagesContainer = document.getElementById('messagesContainer');
            if (messagesContainer) {
                messagesContainer.setAttribute('hidden', '');
            }

            const queryInput = document.querySelector('input[name="q"]');
            if (queryInput) {
                const query = queryInput.value;
                if (query) {
                    fetch('/inventory/search_product/?q=' + encodeURIComponent(query))
                        .then(response => response.json())
                        .then(data => {
                            if (data.exact_match) {
                                const redirectUrl = `/inventory/per_product/${data.redirect_pk}`;
                                window.location.href = redirectUrl;
                            } else if (data.suggested_product) {
                                openSuggestedProductModal(data.suggested_product.name);

                                const yesButton = document.getElementById('yesButton');
                                if (yesButton) {
                                    yesButton.addEventListener('click', function() {
                                        const suggestedProductPk = data.suggested_product.pk;
                                        redirectToProduct(suggestedProductPk);
                                    });
                                }
                            } else {
                                displayMessage('No product found.');
                            }
                        })
                        .catch(error => console.error('Error fetching suggested product data:', error));
                }
            }
        });

        // Add an event listener for the search button click
        searchButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent any default click behavior

            // Manually trigger the form submission
            searchForm.dispatchEvent(new Event('submit'));
        });
    }
});