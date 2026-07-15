document.addEventListener("DOMContentLoaded", function () {

    // ============================
    // Monthly Booking Chart
    // ============================

    const bookingDataElement = document.getElementById("monthly-bookings-data");

    if (bookingDataElement) {

        const bookingData = JSON.parse(bookingDataElement.textContent);

        const bookingCanvas = document.getElementById("monthlyBookingChart");

        if (bookingCanvas) {

            new Chart(bookingCanvas, {

                type: "line",

                data: {

                    labels: bookingData.labels,

                    datasets: [{

                        label: "Bookings",

                        data: bookingData.values,

                        borderColor: "#2563EB",

                        backgroundColor: "rgba(37,99,235,0.15)",

                        fill: true,

                        tension: 0.4,

                        borderWidth: 3,

                        pointRadius: 4,

                        pointHoverRadius: 6

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            display: true,

                            position: "top"

                        }

                    },

                    scales: {

                        x: {

                            grid: {

                                display: false

                            }

                        },

                        y: {

                            beginAtZero: true,

                            ticks: {

                                precision: 0

                            }

                        }

                    }

                }

            });

        }

    }

    // ============================
    // Hotel Comparison Chart
    // ============================

    const hotelDataElement = document.getElementById("hotel-distribution-data");

    if (hotelDataElement) {

        const hotelData = JSON.parse(hotelDataElement.textContent);

        const hotelCanvas = document.getElementById("hotelChart");

        if (hotelCanvas) {

            new Chart(hotelCanvas, {

                type: "doughnut",

                data: {

                    labels: hotelData.labels,

                    datasets: [{

                        data: hotelData.values,

                        backgroundColor: [

                            "#2563EB",

                            "#10B981"

                        ],

                        borderColor: "#ffffff",

                        borderWidth: 2

                    }]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "65%",

                    plugins: {

                        legend: {

                            position: "bottom",

                            labels: {

                                usePointStyle: true,

                                padding: 15

                            }

                        }

                    }

                }

            });

        }

    }

});
// =======================================
// Booking Analytics - Monthly Chart
// =======================================

const bookingMonthlyData = document.getElementById("booking-monthly-data");

if (bookingMonthlyData) {

    const data = JSON.parse(bookingMonthlyData.textContent);

    const canvas = document.getElementById("bookingMonthlyChart");

    if (canvas) {

        new Chart(canvas, {

            type: "bar",

            data: {

                labels: data.labels,

                datasets: [{

                    label: "Bookings",

                    data: data.values,

                    backgroundColor: "#2563EB",

                    borderRadius: 8

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    x: {

                        grid: {

                            display: false

                        }

                    },

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    }

}
// =======================================
// Booking Analytics - Hotel Distribution
// =======================================

const bookingHotelData = document.getElementById("booking-hotel-data");

if (bookingHotelData) {

    const data = JSON.parse(bookingHotelData.textContent);

    const canvas = document.getElementById("bookingHotelChart");

    if (canvas) {

        new Chart(canvas, {

            type: "doughnut",

            data: {

                labels: data.labels,

                datasets: [{

                    data: data.values,

                    backgroundColor: [

                        "#2563EB",
                        "#10B981"

                    ],

                    borderWidth: 2,

                    borderColor: "#ffffff"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "65%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,

                            padding: 15

                        }

                    }

                }

            }

        });

    }

}
// =======================================
// Booking Analytics - Season Distribution
// =======================================

const seasonDataElement = document.getElementById("season-data");

if (seasonDataElement) {

    const data = JSON.parse(seasonDataElement.textContent);

    const canvas = document.getElementById("seasonChart");

    if (canvas) {

        new Chart(canvas, {

            type: "bar",

            data: {

                labels: data.labels,

                datasets: [{

                    label: "Bookings",

                    data: data.values,

                    backgroundColor: [
                        "#3B82F6",
                        "#10B981",
                        "#F59E0B",
                        "#EF4444"
                    ],

                    borderRadius: 8

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
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

}
// =======================================
// Booking Analytics - Lead Time
// =======================================

const leadTimeDataElement = document.getElementById("leadtime-data");

if (leadTimeDataElement) {

    const data = JSON.parse(leadTimeDataElement.textContent);

    const canvas = document.getElementById("leadTimeChart");

    if (canvas) {

        new Chart(canvas, {

            type: "pie",

            data: {

                labels: data.labels,

                datasets: [{

                    data: data.values,

                    backgroundColor: [
                        "#2563EB",
                        "#10B981",
                        "#F59E0B",
                        "#EF4444"
                    ]

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,
                            padding: 15

                        }

                    }

                }

            }

        });

    }

}
// =======================================
// Customer Type Chart
// =======================================

const customerTypeData = document.getElementById("customer-type-data");

if(customerTypeData){

    const data = JSON.parse(customerTypeData.textContent);

    new Chart(document.getElementById("customerTypeChart"),{

        type:"bar",

        data:{

            labels:data.labels,

            datasets:[{

                data:data.values,

                backgroundColor:"#2563EB",

                borderRadius:8

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{
                legend:{display:false}
            }

        }

    });

}

// =======================================
// Guest Status Chart
// =======================================

const guestStatusData=document.getElementById("guest-status-data");

if(guestStatusData){

    const data=JSON.parse(guestStatusData.textContent);

    new Chart(document.getElementById("guestStatusChart"),{

        type:"pie",

        data:{

            labels:data.labels,

            datasets:[{

                data:data.values,

                backgroundColor:[
                    "#2563EB",
                    "#10B981",
                    "#F59E0B"
                ]

            }]

        },

        options:{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{

                legend:{

                    position:"bottom",

                    labels:{

                        usePointStyle:true,

                        padding:15

                    }

                }

            }

        }

    });

}
// =======================================
// Market Segment Chart
// =======================================

const marketData = document.getElementById("market-segment-data");

if (marketData) {

    const data = JSON.parse(marketData.textContent);

    new Chart(document.getElementById("marketSegmentChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: "#10B981",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: { display: false }

            }

        }

    });

}

// =======================================
// Top Countries Chart
// =======================================

const countryData = document.getElementById("countries-data");

if (countryData) {

    const data = JSON.parse(countryData.textContent);

    new Chart(document.getElementById("countriesChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: "#F59E0B",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            indexAxis: "y",

            plugins: {

                legend: { display: false }

            }

        }

    });

}

// =======================================
// Special Requests Chart
// =======================================

const requestData = document.getElementById("special-request-data");

if (requestData) {

    const data = JSON.parse(requestData.textContent);

    new Chart(document.getElementById("specialRequestChart"), {

        type: "line",

        data: {

            labels: data.labels,

            datasets: [{

                label: "Guests",

                data: data.values,

                borderColor: "#EF4444",

                backgroundColor: "rgba(239,68,68,.15)",

                fill: true,

                tension: 0.4

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}
// =======================================
// Revenue Analytics
// =======================================

// ADR by Hotel
const adrHotelData = document.getElementById("adr-hotel-data");

if (adrHotelData) {

    const data = JSON.parse(adrHotelData.textContent);

    new Chart(document.getElementById("adrHotelChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                label: "Average ADR",

                data: data.values,

                backgroundColor: "#2563EB",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}

// ADR by Season
const adrSeasonData = document.getElementById("adr-season-data");

if (adrSeasonData) {

    const data = JSON.parse(adrSeasonData.textContent);

    new Chart(document.getElementById("adrSeasonChart"), {

        type: "line",

        data: {

            labels: data.labels,

            datasets: [{

                label: "Average ADR",

                data: data.values,

                borderColor: "#10B981",

                backgroundColor: "rgba(16,185,129,.15)",

                fill: true,

                tension: 0.4

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false

        }

    });

}

// Revenue Category
const revenueCategoryData = document.getElementById("revenue-category-data");

if (revenueCategoryData) {

    const data = JSON.parse(revenueCategoryData.textContent);

    new Chart(document.getElementById("revenueCategoryChart"), {

        type: "doughnut",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: [

                    "#2563EB",
                    "#10B981",
                    "#F59E0B"

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "65%"

        }

    });

}

// Stay Type
const stayTypeData = document.getElementById("stay-type-data");

if (stayTypeData) {

    const data = JSON.parse(stayTypeData.textContent);

    new Chart(document.getElementById("stayTypeChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: "#8B5CF6",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}
// =======================================
// Statistics Charts
// =======================================

// ADR Distribution
const adrStats = document.getElementById("adr-distribution-data");

if (adrStats) {

    const data = JSON.parse(adrStats.textContent);

    new Chart(document.getElementById("adrDistributionChart"), {

        type: "doughnut",

        data: {

            labels: data.labels,

            datasets: [{

                data: data.values,

                backgroundColor: [

                    "#2563EB",
                    "#10B981",
                    "#F59E0B"

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            cutout: "65%"

        }

    });

}

// =======================================
// Lead Time Distribution
// =======================================

const leadStats = document.getElementById("lead-distribution-data");

if (leadStats) {

    const data = JSON.parse(leadStats.textContent);

    new Chart(document.getElementById("leadDistributionChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                label: "Bookings",

                data: data.values,

                backgroundColor: "#F59E0B",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

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

// ======================================
// Stay Type Distribution
// ======================================

const stayStats = document.getElementById("stay-distribution-data");

if (stayStats) {

    const data = JSON.parse(stayStats.textContent);

    new Chart(

        document.getElementById("stayDistributionChart"),

        {

            type: "pie",

            data: {

                labels: data.labels,

                datasets: [{

                    data: data.values,

                    backgroundColor: [

                        "#10B981",
                        "#2563EB",
                        "#F59E0B"

                    ],

                    borderWidth: 2,

                    borderColor: "#ffffff"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,

                            padding: 20

                        }

                    }

                }

            }

        }

    );

}
// ======================================
// Cancellation Distribution
// ======================================

const cancelData = document.getElementById("cancellation-data");

if (cancelData) {

    const data = JSON.parse(cancelData.textContent);

    new Chart(

        document.getElementById("cancellationChart"),

        {

            type: "doughnut",

            data: {

                labels: data.labels,

                datasets: [{

                    data: data.values,

                    backgroundColor: [

                        "#10B981",

                        "#EF4444"

                    ],

                    borderWidth: 2,

                    borderColor: "#ffffff",

                    hoverOffset: 10

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                cutout: "65%",

                plugins: {

                    legend: {

                        position: "bottom",

                        labels: {

                            usePointStyle: true,

                            pointStyle: "circle",

                            padding: 20

                        }

                    }

                }

            }

        }

    );

}
// ======================================
// ADR by Customer Type
// ======================================

const adrCustomerData = document.getElementById("adr-customer-data");

if (adrCustomerData) {

    const data = JSON.parse(adrCustomerData.textContent);

    new Chart(document.getElementById("adrCustomerChart"), {

        type: "bar",

        data: {

            labels: data.labels,

            datasets: [{

                label: "Average ADR",

                data: data.values,

                backgroundColor: "#3B82F6",

                borderRadius: 8

            }]

        },

        options: {

            indexAxis: "y",

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                x: {

                    beginAtZero: true

                }

            }

        }

    });

}