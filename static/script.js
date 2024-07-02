
  function loadQualifications() {
  var universityDropdown = document.getElementById("UniOptions");
  var qualificationDropdown = document.getElementById("qualifications");
  var selectedUniversity = universityDropdown.value;
  // alert(selectedUniversity)
  var data = {
    'university': selectedUniversity
  };
  var csrftoken = getCookie('csrftoken');
  // Send an AJAX request to the server
  $.ajax({
    type: "POST",
    url: "qualification-names/",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    beforeSend: function(xhr, settings) {
      // Set the CSRF token in the request headers
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function (response) {
        // Handle the response from the server
        var selectedQualifications = "";
        selectedQualifications = response.availQualifications;
          
          // Clear existing options
          qualificationDropdown.innerHTML = "";
          
          // Parse the response text and extract qualifications
          var qualifications = selectedQualifications.split("\n");
          
          // Add new options
          for (var i = 0; i < qualifications.length; i++) {
              var option = document.createElement("option");
              option.value =i;
              option.textContent = qualifications[i];
              qualificationDropdown.appendChild(option);
          }
      },
      error: function (xhr, status, error) {
        alert(error)
      }
    });
  
}
function submitForm() {
  var selectedQualification = document.getElementById("qualifications").options[document.getElementById("qualifications").selectedIndex].text;
  var selectedNQFLevel = document.getElementById("degree").value;
  var selectedYearsOfExp = document.getElementById("experience").value;

  var data = {
    'qualification': selectedQualification,
    'nqfLevel': selectedNQFLevel,
    'selectedYearsOfExp': selectedYearsOfExp
  };
  var csrftoken = getCookie('csrftoken');

  event.preventDefault();  // Prevent form submission

  // Show the loading spinner
   var loader= document.getElementById("loadingSpinner");
   loader.classList.remove("hide");

  // Disable the submit button to prevent multiple submissions
  document.getElementById("submitButton").setAttribute("disabled", "true");

  // Send an AJAX request to the server
  $.ajax({
    type: "POST",
    url: "results/",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    beforeSend: function(xhr, settings) {
      // Set the CSRF token in the request headers
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    },
    success: function(response) {
      // Handle the response from the server
      var results = response.result;
     
      // window.location.href = "results/";
      var showResults = document.getElementById("results");
      showResults.innerText = results;
      if(response.bl==true)      
      showResults.setAttribute("style", "color:#53b153")
      else{
      showResults.setAttribute("style", "color:#9b2525")
       // Redirect to the results page  

      }
      
    }, complete: function() {
      // Hide the loading spinner
      $('#loadingSpinner').addClass('hide');

      // Enable the submit button
      $('#submitButton').prop('disabled', false);

      // Reset the form
      $('#myForm')[0].reset();
    },
    error: function(xhr, status, error) {
      console.log(error);
    }
  });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Check if the cookie name matches the expected format
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}