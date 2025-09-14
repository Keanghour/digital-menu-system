<script setup>
import { ref, computed, onMounted } from 'vue';

const searchQuery = ref('');
const filterType = ref('day');
const startDate = ref('');
const endDate = ref('');

// Dummy functions for import and export
const importReports = () => {
    alert("Import functionality is not implemented yet.");
};

const exportReports = () => {
    alert("Export functionality is not implemented yet.");
};

// Function to filter reports based on the selected date range
const filterByDate = () => {
    alert(`Filtering reports from ${startDate.value} to ${endDate.value}`);
};

// Function to generate fake report data
const generateFakeReports = (count) => {
    const fakeReports = [];
    const statuses = [
        { label: "Processed", color: "orange" },
        { label: "Pending", color: "blue" },
        { label: "Rejected", color: "red" },
        { label: "Completed", color: "green" }
    ];

    for (let i = 1; i <= count; i++) {
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30)); // Random date in the last 30 days
        fakeReports.push({
            date: date.toISOString().split('T')[0],
            total: (Math.random() * 100).toFixed(2),
            count: Math.floor(Math.random() * 10) + 1 // Random count between 1 and 10
        });
    }

    return fakeReports;
};

// Placeholder for summarized reports
const summarizedReports = ref([]);

// Populate the summarizedReports with fake data on mounted
onMounted(() => {
    summarizedReports.value = generateFakeReports(10); // Generate 10 fake reports
});

// Function to view details of a report
const viewReport = (data) => {
    alert(`Viewing report for date: ${data.date}`);
};
</script>

<template>
    <div class="card">
        <div class="flex justify-between mb-4">
            <h4 class="m-0">Report Summary</h4>
            <div class="flex">
                <button @click="importReports" class="mr-2">Import</button>
                <button @click="exportReports">Export</button>
            </div>
        </div>

        <div class="flex mb-8">
            <div class="flex flex-col mr-2">
                <label for="startDate">Start Date:</label>
                <InputText type="date" v-model="startDate" />
            </div>
            <div class="flex flex-col">
                <label for="endDate">End Date:</label>
                <InputText type="date" v-model="endDate" />
            </div>
            <button @click="filterByDate" class="mt-4">Submit</button>
        </div>

        <div class="flex justify-end mb-4">
            <select v-model="filterType" class="mr-2">
                <option value="day">Daily</option>
                <option value="week">Weekly</option>
                <option value="month">Monthly</option>
                <option value="month">Yearly</option>
            </select>
        </div>

        <DataTable :value="summarizedReports" stripedRows tableStyle="min-width: 50rem">
            <Column field="date" header="Date"></Column>
            <Column field="total" header="Total Amount"></Column>
            <Column field="count" header="Count"></Column>
            <Column header="Action">
                <template #body="{ data }">
                    <div class="justify-center">
                        <i class="pi pi-eye cursor-pointer action-icon" @click="viewReport(data)" title="View Report"></i>
                        <i class="pi pi-upload cursor-pointer action-icon" @click="importReports" title="Import"></i>
                        <i class="pi pi-download cursor-pointer action-icon" @click="exportReports" title="Export"></i>
                    </div>
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<style scoped>
.card {
    padding: 20px;
    margin: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
button {
    margin-left: 10px;
    padding: 5px 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
.action-icon {
    margin-left: 10px; /* Space between icons */
}
</style>
