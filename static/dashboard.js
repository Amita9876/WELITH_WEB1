
document.addEventListener("DOMContentLoaded", function () {

    // Sample Dashboard Data
    const totalUsers = 1200;
    const totalSales = 75000;
    const totalOrders = 320;

    // Update Dashboard Cards
    const usersElement = document.getElementById("totalUsers");
    const salesElement = document.getElementById("totalSales");
    const ordersElement = document.getElementById("totalOrders");

    if (usersElement) usersElement.textContent = totalUsers;
    if (salesElement) salesElement.textContent = "₹ " + totalSales;
    if (ordersElement) ordersElement.textContent = totalOrders;

    // Create Sales Chart
    const ctx = document.getElementById("salesChart");

    if (ctx) {
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                datasets: [{
                    label: "Monthly Sales",
                    data: [12000, 15000, 10000, 18000, 22000, 20000],
                    backgroundColor: "#4e73df"
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

});