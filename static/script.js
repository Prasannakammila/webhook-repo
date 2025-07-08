function fetchEvents() {
    fetch('/events')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('events');
            container.innerHTML = '';
            data.forEach(event => {
                const div = document.createElement('div');
                div.className = 'event';
                div.textContent = event.message;
                container.appendChild(div);
            });
        });
}

setInterval(fetchEvents, 15000); // Refresh every 15 seconds
fetchEvents(); // Load initially
