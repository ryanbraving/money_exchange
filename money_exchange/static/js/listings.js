console.log("listings.js loaded");

function attachRowClickHandlers() {
    console.log('Attaching row click handlers...');
    document.querySelectorAll('.table-row').forEach(row => {
        row.onclick = function(e) {
            if (e.target.tagName.toLowerCase() === 'a') return;
            const href = this.getAttribute('data-href');
            const query = window.location.search;
            console.log('Row clicked. href:', href, 'query:', query);
            if (href) {
                window.location.href = href + query;
            }
        };
    });
}

function updateBreadcrumbListingsLink() {
    let lastQuery = localStorage.getItem('listings_last_query') || window.location.search;
    const link = document.getElementById('breadcrumb-listings-link');
    if (link) {
        link.href = '/listings/' + lastQuery;
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
    let newUrl = `/listings/?${params.toString()}`;

    // Store the last query string
    localStorage.setItem('listings_last_query', '?' + params.toString());

    fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            document.getElementById('listings-table-body').innerHTML = data.html;
            window.history.pushState({}, '', newUrl);
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
        ajaxUpdateTable();
    });
    document.getElementById('buying-currency').addEventListener('change', function() {
        ajaxUpdateTable();
    });
    attachAjaxLinkHandlers();
    attachRowClickHandlers();
    updateBreadcrumbListingsLink();

    // Prevent navigation if already on the listings page
    const listingsLink = document.getElementById('breadcrumb-listings-link');
    if (listingsLink) {
        listingsLink.addEventListener('click', function(e) {
            if (window.location.pathname === '/listings/') {
                e.preventDefault();
            }
        });
    }
});

// Handle browser navigation (back/forward)
window.addEventListener('popstate', function(event) {
    ajaxUpdateTable(window.location.href);
});