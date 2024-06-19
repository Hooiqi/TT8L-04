const button = document.getElementById("checkout-button");

button.addEventListener("click", () => {
    fetch("/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            event_name: document.getElementById('event_name').value,
            ticket_type: document.getElementById('ticket_type').value,
            ticket_price: document.getElementById('ticket_price').value,
        }),
    })
    .then(res => {
        if (res.ok) return res.json();
        return res.json().then(json => Promise.reject(json));
    })
    .then(session => {
        return stripe.redirectToCheckout({ sessionId: session.id });
    })
    .then(result => {
        if (result.error) {
            console.error(result.error.message);
            // Handle error (e.g., display an alert)
        }
    })
    .catch(error => {
        console.error("Error:", error);
        // Handle error (e.g., display an alert)
    });
});
