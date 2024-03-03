// register and login Open popup function
function openPopup(popupId) {
    // Close other popups before opening the selected one
    var otherPopups = document.querySelectorAll('.popup');
    for (var i = 0; i < otherPopups.length; i++) {
        if (otherPopups[i].id !== popupId) {
            otherPopups[i].style.display = "none";
        }
    }

    document.getElementById(popupId).style.display = "block";
}

// Close popup function
function closePopup(popupId) {
    document.getElementById(popupId).style.display = "none";
}

// Close popup when clicking outside or on the "X" button
window.onclick = function (event) {
    var popups = document.querySelectorAll('.popup');
    for (var i = 0; i < popups.length; i++) {
        if (event.target == popups[i] || event.target.classList.contains('close-btn')) {
            popups[i].style.display = "none";
        }
    }
}
// linking header footer html pages 

    // Load header and footer
    fetchAndLoad("./includes/header.html", "header-placeholder");
    fetchAndLoad("./includes/footer.html", "footer-placeholder");

    // Load content based on the current page
    var currentPage = window.location.pathname.split("/").pop().replace(".html", "") || "main";
    function fetchAndLoad(url, placeholderId) {
        url = '/' + url; // Assuming your pages are served from the root
        console.log("Fetching:", url);
    
        // Check if the target element exists in the document
        var targetElement = document.getElementById(placeholderId);
        if (!targetElement) {
            console.error("Error loading content: Target element not found with id:", placeholderId);
            return;
        }
    
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.text();
            })
            .then(data => {
                console.log("Successfully loaded content:", data);
                targetElement.innerHTML = data;
            })
            .catch(error => console.error("Error loading content:", error));
    }
    
    
    

// local shops 
function showPopup(action) {
    if (action === 'Add Local Shop') {
        // Customize this function to load product details based on the action
        // For simplicity, just setting a placeholder title
        document.getElementById('popupTitle').textContent = action;

        // Display the overlay and popup
        document.getElementById('overlay').style.display = 'block';
        document.getElementById('popup').style.display = 'block';
    }
}

function hidePopup() {
    // Hide the overlay and popup
    document.getElementById('overlay').style.display = 'none';
    document.getElementById('popup').style.display = 'none';
}


function loginAs(role) {
    // Perform actions based on the selected role (manufacturer or distributor)
    alert('Logging in as ' + role);

    // Update the heading based on the selected role
    document.getElementById('loginHeading').innerText = role.charAt(0).toUpperCase() + role.slice(1) + ' Login';
    // Update the document title
    document.title = 'Login - ' + role.charAt(0).toUpperCase() + role.slice(1);
}

function closePopup(popupId) {
    document.getElementById(popupId).style.display = "none";
    // Reset the heading and title to "Login Form"
    document.getElementById('loginHeading').innerText = 'Login Form';
    document.title = 'Login Form';
}