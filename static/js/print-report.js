/**
 * Print Report Functionality
 * Handles report printing with proper formatting
 */

// Function to prepare the page for printing
function preparePrint() {
    // Add print-specific classes
    document.body.classList.add('printing');
    
    // Create print header if it doesn't exist
    if (!document.querySelector('.print-header')) {
        const header = document.createElement('div');
        header.className = 'print-header';
        
        const title = document.createElement('h1');
        title.textContent = document.title || 'Visitor Pass System Report';
        
        const date = document.createElement('p');
        const now = new Date();
        date.textContent = 'Generated on: ' + now.toLocaleDateString() + ' at ' + now.toLocaleTimeString();
        
        header.appendChild(title);
        header.appendChild(date);
        
        // Insert at the beginning of the main content
        const content = document.querySelector('.content') || document.body;
        content.insertBefore(header, content.firstChild);
    }
    
    // Create print footer if it doesn't exist
    if (!document.querySelector('.print-footer')) {
        const footer = document.createElement('div');
        footer.className = 'print-footer';
        footer.textContent = 'Visitor Pass System © ' + new Date().getFullYear() + ' | Printed from Admin Portal';
        
        // Append to the end of the main content
        const content = document.querySelector('.content') || document.body;
        content.appendChild(footer);
    }
}

// Function to clean up after printing
function cleanupAfterPrint() {
    // Remove print-specific classes
    document.body.classList.remove('printing');
    
    // Remove print header and footer
    const header = document.querySelector('.print-header');
    if (header) header.remove();
    
    const footer = document.querySelector('.print-footer');
    if (footer) footer.remove();
}

// Function to print the current report
function printReport() {
    // Prepare the document for printing
    preparePrint();
    
    // Use browser print functionality
    window.print();
    
    // Clean up after printing dialog is closed
    // Note: This happens immediately in some browsers, so the cleanup
    // might occur before the print dialog is closed
    setTimeout(cleanupAfterPrint, 1000);
}

// Add event listeners for print events
window.addEventListener('beforeprint', preparePrint);
window.addEventListener('afterprint', cleanupAfterPrint);

// Initialize print buttons
document.addEventListener('DOMContentLoaded', function() {
    const printButtons = document.querySelectorAll('.print-report-btn');
    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            printReport();
        });
    });
});
