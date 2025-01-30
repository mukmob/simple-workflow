document.addEventListener("DOMContentLoaded", function () {
    const calendar = document.getElementById('calendar');
    const timeSlots = document.getElementById('timeSlots');
    const confirmation = document.getElementById('confirmation');
    const confirmationText = document.getElementById('confirmationText');
    const monthYearLabel = document.getElementById('monthYear');
    const prevMonthBtn = document.getElementById('prevMonth');
    const nextMonthBtn = document.getElementById('nextMonth');
    let selectedDate = new Date();
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
      // Create empty grid slots for days before the 1st of the month
      for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement('div');
        calendar.appendChild(emptyDiv);
      }
      // Generate the actual days of the month
      for (let i = 1; i <= daysInMonth; i++) {
        const dayDiv = document.createElement('div');
        dayDiv.textContent = i;
        dayDiv.setAttribute('data-date', `${year}-${month + 1}-${i}`);
        calendar.appendChild(dayDiv);
        // Add event listener to select the date
        dayDiv.addEventListener('click', function () {
          selectedDate = this.getAttribute('data-date');
          debugger
            // document.getElementsByTagName("div").classList.toggle("highlight");
          //  () =>{
          //   selectedDate.classList("active");
          // }
          // selectedDate = this.style.backgroundColor = "black";
          // selectedDate.style.backgroundColor= "black";
          timeSlots.classList.remove('hidden');
          confirmation.classList.add('hidden');
        });
      }
    }
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
    });
    // Navigate to next month
    nextMonthBtn.addEventListener('click', function () {
      currentMonth++;
      if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
      }
      generateCalendar(currentYear, currentMonth);
    });
    // Handle time slot selection
    document.querySelectorAll('.time-slot').forEach(slot => {
      slot.addEventListener('click', function () {
        selectedTime = this.getAttribute('data-time');
        // Display confirmation
        confirmationText.textContent = `You have booked an appointment on ${selectedDate} at ${selectedTime}.`;
        confirmation.classList.remove('hidden');
      });
    });
  });
  
  
  
  
  