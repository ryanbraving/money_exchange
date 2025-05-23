console.log("listings.js loaded");

function attachRowClickHandlers() {
    document.querySelectorAll('.table-row').forEach(row => {
        row.onclick = function(e) {
            if (e.target.tagName.toLowerCase() === 'a') return;
            const href = this.getAttribute('data-href');
            if (href) {
                // Append current query string to detail view
                const query = window.location.search;
                window.location.href = href + query;
            }
        };
    });
}

function updateBreadcrumbListingsLink() {
    const query = window.location.search;
    const link = document.getElementById('breadcrumb-listings-link');
    console.log('Updating breadcrumb link:', link, query);
    if (link) {
        link.href = '/listings/' + query;
    }
}

function ajaxUpdateTable(url = null) {
    const selling = document.getElementById('selling-currency').value;
    const buying = document.getElementById('buying-currency').value;

    let params = new URLSearchParams({
        selling_currency: selling,
        buying_currency: buying,
    });

    if (url) {
        let urlObj = new URL(url, window.location.origin);
        if (urlObj.searchParams.has('sort')) params.set('sort', urlObj.searchParams.get('sort'));
        if (urlObj.searchParams.has('dir')) params.set('dir', urlObj.searchParams.get('dir'));
        if (urlObj.searchParams.has('page')) params.set('page', urlObj.searchParams.get('page'));
    }

    let fetchUrl = `/listings/table-partial/?${params.toString()}`;

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('listings-table-body').innerHTML = data.html;
            window.history.pushState({}, '', fetchUrl.replace('/table-partial', ''));
            attachAjaxLinkHandlers();
            attachRowClickHandlers();
            updateBreadcrumbListingsLink();
        });
}

function attachAjaxLinkHandlers() {
    document.querySelectorAll('a.ajax-link').forEach(link => {
        link.onclick = function(e) {
            e.preventDefault();
            ajaxUpdateTable(this.href);
        };
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('selling-currency').addEventListener('change', function() {
        ajaxUpdateTable();
    });
    document.getElementById('buying-currency').addEventListener('change', function() {
        ajaxUpdateTable();
    });
    attachAjaxLinkHandlers();
    attachRowClickHandlers();
    updateBreadcrumbListingsLink();
});