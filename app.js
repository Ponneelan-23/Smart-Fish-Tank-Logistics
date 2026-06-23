// ======================================================
// DOM Elements
// ======================================================

const temperatureValue =
    document.getElementById("temperatureValue");

const turbidityValue =
    document.getElementById("turbidityValue");

const phValue =
    document.getElementById("phValue");

const doValue =
    document.getElementById("doValue");

const waterLevelPercent =
    document.getElementById("waterLevelPercent");

const waterFill =
    document.getElementById("waterFill");

const tankStatus =
    document.getElementById("tankStatus");

const timestamp =
    document.getElementById("timestamp");

// ======================================================
// Charts
// ======================================================

let temperatureChart;
let turbidityChart;
let waterLevelChart;

// ======================================================
// Chart Theme
// ======================================================

const chartOptions = {

    responsive: true,

    maintainAspectRatio: false,

    plugins: {

        legend: {
            display: false
        }
    },

    scales: {

        x: {

            ticks: {
                color: "#cbd5e1"
            },

            grid: {
                color: "rgba(255,255,255,0.05)"
            }
        },

        y: {

            ticks: {
                color: "#cbd5e1"
            },

            grid: {
                color: "rgba(255,255,255,0.05)"
            }
        }
    }
};

// ======================================================
// Create Charts
// ======================================================

function createCharts() {

    temperatureChart = new Chart(
        document.getElementById("temperatureChart"),
        {
            type: "line",

            data: {
                labels: [],
                datasets: [{
                    data: [],
                    borderColor: "#38bdf8",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                }]
            },

            options: chartOptions
        }
    );

    turbidityChart = new Chart(
        document.getElementById("turbidityChart"),
        {
            type: "line",

            data: {
                labels: [],
                datasets: [{
                    data: [],
                    borderColor: "#22c55e",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                }]
            },

            options: chartOptions
        }
    );

    waterLevelChart = new Chart(
        document.getElementById("waterLevelChart"),
        {
            type: "line",

            data: {
                labels: [],
                datasets: [{
                    data: [],
                    borderColor: "#fbbf24",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: false
                }]
            },

            options: chartOptions
        }
    );
}

// ======================================================
// Update Status Badge
// ======================================================

function updateStatus(status) {

    tankStatus.innerText = status;

    tankStatus.classList.remove(
        "healthy",
        "warning",
        "critical"
    );

    if (status === "Healthy") {

        tankStatus.classList.add(
            "healthy"
        );
    }

    else if (status === "Warning") {

        tankStatus.classList.add(
            "warning"
        );
    }

    else {

        tankStatus.classList.add(
            "critical"
        );
    }
}

// ======================================================
// Latest Data
// ======================================================

async function fetchLatestData() {

    try {

        const response =
            await fetch("/api/latest");

        const result =
            await response.json();

        if (!result.success) return;

        const data =
            result.data;

        temperatureValue.innerHTML =
            `${data.temperature} °C`;

        turbidityValue.innerHTML =
            `${data.turbidity} NTU`;

        phValue.innerHTML =
            data.ph ?? "--";

        doValue.innerHTML =
            data.do ?? "--";

        waterLevelPercent.innerHTML =
            `${data.water_level}%`;

        waterFill.style.height =
            `${data.water_level}%`;

        timestamp.innerHTML =
            data.timestamp;

        updateStatus(
            data.status
        );

    }

    catch (error) {

        console.error(
            "Latest Data Error:",
            error
        );
    }
}

// ======================================================
// History Data
// ======================================================

async function fetchHistoryData() {

    try {

        const response =
            await fetch("/api/history");

        const result =
            await response.json();

        if (!result.success) return;

        const history =
            result.data;

        const labels =
            history.map(item =>
                item.timestamp.split(" ")[1]
            );

        const temperatures =
            history.map(item =>
                item.temperature
            );

        const turbidity =
            history.map(item =>
                item.turbidity
            );

        const waterLevel =
            history.map(item =>
                item.water_level
            );

        // Temperature

        temperatureChart.data.labels =
            labels;

        temperatureChart.data.datasets[0].data =
            temperatures;

        temperatureChart.update();

        // Turbidity

        turbidityChart.data.labels =
            labels;

        turbidityChart.data.datasets[0].data =
            turbidity;

        turbidityChart.update();

        // Water Level

        waterLevelChart.data.labels =
            labels;

        waterLevelChart.data.datasets[0].data =
            waterLevel;

        waterLevelChart.update();

    }

    catch (error) {

        console.error(
            "History Error:",
            error
        );
    }
}

// ======================================================
// Initialize
// ======================================================

async function initializeDashboard() {

    createCharts();

    await fetchLatestData();

    await fetchHistoryData();

    setInterval(() => {

        fetchLatestData();

        fetchHistoryData();

    }, 2000);
}

// ======================================================

initializeDashboard();