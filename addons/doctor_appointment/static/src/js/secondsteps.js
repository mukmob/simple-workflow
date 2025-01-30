document.addEventListener("DOMContentLoaded", function () {
    const calendar = document.getElementById('calendar');
    const timeSlots = document.getElementById('timeSlots');
    const confirmation = document.getElementById('confirmation');
    const confirmationText = document.getElementById('confirmationText');
    const selectedDateInput = document.getElementById('selectedDate');
    const selectedTimeInput = document.getElementById('selectedTime');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    const monthYearLabel = document.getElementById('monthYear');

    const BASE_URL = window.location.origin;
    const TIME_SLOT_URL = `${BASE_URL}/booking/get_time_slot`;
    console.log("BASE_URL:", BASE_URL);
    console.log("TIME_SLOT_URL:", TIME_SLOT_URL);

    //let selectedDate = null;
    let selectedTime = null;
    let currentMonth = new Date().getMonth();
    let currentYear = new Date().getFullYear();
    // Generate calendar for selected month and year
    function generateCalendar(year, month) {
        calendar.innerHTML = ''; // Clear the previous calendar
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDay = new Date(year, month, 1).getDay();
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        // Update the month and year label
        monthYearLabel.textContent = `${monthNames[month]} ${year}`;
        // Get the current date for comparison
        const today = new Date();
        
        
        const todayDate1 = new Date(today.getFullYear(), today.getMonth(), today.getDate());
        const todayDate = new Date(document.getElementById("sub_dates").value);
        console.log(todayDate);
        // Create empty grid slots for days before the 1st of the month
        for (let i = 0; i < firstDay; i++) {
            const emptyDiv = document.createElement('div');
            calendar.appendChild(emptyDiv);
        }
        // Generate the actual days of the month
        for (let i = 1; i <= daysInMonth; i++) {
            const dayDiv = document.createElement('div');
            dayDiv.textContent = i;
            const date = new Date(year, month, i);
            const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
            dayDiv.setAttribute('data-date', dateString);
            // Disable dates before today, but allow today
            // Changes Made here 1
            
            if (date.toDateString() === todayDate.toDateString()) {  // problem
                dayDiv.addEventListener('click', function () { selectedDate(dayDiv.getAttribute("data-date")); });
                dayDiv.setAttribute('class', "btn btn-primary");
            }
            else if (date < todayDate) {
                dayDiv.classList.add('disabled');
            }
            else {
                console.log("das");
                     dayDiv.addEventListener('click', function () { selectedDate(dayDiv.getAttribute("data-date")); });
            }
            // Till Here
            calendar.appendChild(dayDiv);
        }
    
    }

    
    // Function to set the selected date
    window.setSelectedDate = function (element) {
        /*selectedTime = null;
        selectedTimeInput.value = ''; // Clear the selected time input field
        confirmation.classList.add('hidden'); // Hide confirmation
        selectedDate = element.getAttribute('data-date');
        selectedDateInput.value = selectedDate; // Update the selected date input field
        console.log("Selected Date:", selectedDate);
        timeSlots.classList.remove('hidden');
        generateTimeSlots(selectedDate);*/
        console.log("call");
    };


    function selectedDate(day){
        console.log(day);
        
        document.getElementById("slots-container").innerHTML = "";
        doctor_id = document.getElementById("sub_doctor_id").value;
        document.getElementById("selectedDate").value = day;

        const formdata = new FormData();
        formdata.append("date", day);
        formdata.append("doctor_id", doctor_id);
        const requestOptions = {
            method: "POST",
            body: formdata,
            redirect: "follow"
          };
          const response = fetch(TIME_SLOT_URL, requestOptions)
          .then((response) => response.text())
          .then(data => { 
            
            const avail_slot = JSON.parse(data);
            n = avail_slot.length 
            console.log(typeof(avail_slot));
            console.log(avail_slot);
            slot_html = '';
            total_val = Object.keys(avail_slot).length;
            if(total_val > 0){
                
                for (const property in avail_slot) {
                    //console.log(avail_slot[property]);
                    timeslot = '<button class="btn time-slot" onclick="setSelectedTime(this)" data-time="'+avail_slot[property]+'">'+avail_slot[property]+'</button>';
                    slot_html += timeslot;
                  }
            } else{
                console.log("elseif");
                slot_html = 'NO SLOT IS AVAILABLE ON TODAY';
            }
            
              console.log(slot_html);
              document.getElementById("slots-container").innerHTML = slot_html;
            });   
    }
    
    // Function to generate time slots
    function generateTimeSlots(date) {
        timeSlots.innerHTML = ''; // Clear the previous time slots
        const times = ['09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM'];
        times.forEach(time => {
            const timeDiv = document.createElement('div');
            timeDiv.textContent = time;
            timeDiv.setAttribute('data-time', time);
            timeDiv.addEventListener('click', function () { selectedTime(timeDiv); });
            timeSlots.appendChild(timeDiv);
        });
    }
    // Function to set the selected time
    window.setSelectedTime = function (element) {
        selectedTime = element.getAttribute('data-time');
        selectedTimeInput.value = selectedTime;
        console.log("Selected Time:", selectedTime);
        confirmationText.textContent = `You have booked an appointment on ${document.getElementById("selectedDate").value} at ${selectedTime}. `;
        confirmation.classList.remove('hidden');
    };
    // Initialize the calendar
    generateCalendar(currentYear, currentMonth);
    // Navigate to previous month
    prevMonthBtn.addEventListener('click', function () {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        generateCalendar(currentYear, currentMonth);
        addDateClickListeners();
    });

    nextMonthBtn.addEventListener('click', function () {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        generateCalendar(currentYear, currentMonth);
        addDateClickListeners();
    });
    
    function addDateClickListeners() {
        document.querySelectorAll(".calendar > div").forEach(button => {
            button.addEventListener("click", () => {
                // Remove highlight from all dates
                document.querySelectorAll(".calendar > div").forEach(btn => btn.classList.remove("btn", "btn-primary"));
                // Highlight the selected date
                button.classList.add("btn", "btn-primary");
            });
        });
    }
    addDateClickListeners();
});


function validateForm() {
    const selectedDoctor = document.getElementById("sub_doctor_id").value;
    const selectedTreatment = document.getElementsByName("selected_treatment_id")[0].value;
    const selectedTime = document.getElementById("selectedTime").value;
    const selectedDate = document.getElementById("selectedDate").value;
    

   
    if (!selectedDoctor) {
        alert("Please select a doctor.");
        return false;
    }
    if (!selectedTreatment) {
        alert("Please select a treatment.");
        return false;
    }
    if (!selectedDate) {
        alert("Please select a date.");
        return false;
    }
    if (!selectedTime) {
        alert("Please select a time slot.");
        return false;
    }
    return true;
}

function setSelectedTime(button) {
    const selectedTime = button.getAttribute("data-time");
    document.getElementById("selectedTime").value = selectedTime;
}

