console.log("currency-dropdown.js loaded");

const currencies = ['IRR', 'USD', 'EUR', 'GBP', 'NZD']; // Add/remove as needed

function updateBuyingOptions() {
    const selling = document.getElementById('selling-currency').value;
    const buyingSelect = document.getElementById('buying-currency');
    let options = [];
    if (selling === 'IRR' || selling === '') {
        options = currencies.filter(c => c !== 'IRR');
    } else {
        options = ['IRR'];
    }

    // Remove all options except 'All'
    Array.from(buyingSelect.options).forEach(opt => {
        if (opt.value !== "") buyingSelect.removeChild(opt);
    });

    // Add new options
    options.forEach(currency => {
        const opt = document.createElement('option');
        opt.value = currency;
        opt.text = currency;
        buyingSelect.appendChild(opt);
    });

    // Auto-select IRR if it's the only option
    if (options.length === 1) {
        buyingSelect.value = options[0];
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('selling-currency').addEventListener('change', function() {
        updateBuyingOptions();
    });
    updateBuyingOptions();
});