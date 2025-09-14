<!-- src/views/pages/UserManagement/AccountRequest.vue -->

<template>
    <div class="account-request-container">
        <h3 class="text-center mb-4">Account Requests</h3>
        <table class="table-auto w-full">
            <thead>
                <tr>
                    <th class="px-4 py-2">No</th>
                    <th class="px-4 py-2">User Name</th>
                    <th class="px-4 py-2">Requisition Date</th>
                    <th class="px-4 py-2">Delete Request Date</th>
                    <th class="px-4 py-2">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(request, index) in requests" :key="request.id">
                    <td class="border px-4 py-2">{{ index + 1 }}</td>
                    <td class="border px-4 py-2">{{ request.userName }}</td>
                    <td class="border px-4 py-2">{{ formatDate(request.requisitionDate) }}</td>
                    <td class="border px-4 py-2">{{ formatDate(request.deleteRequestDate) }}</td>
                    <td class="border px-4 py-2">
                        <Button label="Edit" icon="pi pi-pencil" @click="editRequest(request.id)" />
                        <Button label="Confirm" icon="pi pi-check" @click="confirmRequest(request.id)" class="ml-2" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Button from 'primevue/button';

const requests = ref([
    {
        id: 1,
        userName: 'John Doe',
        requisitionDate: new Date('2023-12-19T08:30:00'),
        deleteRequestDate: new Date('2023-12-20T10:00:00'),
    },
    {
        id: 2,
        userName: 'Jane Smith',
        requisitionDate: new Date('2023-12-18T14:15:00'),
        deleteRequestDate: new Date('2023-12-19T09:45:00'),
    },
    {
        id: 3,
        userName: 'Alice Johnson',
        requisitionDate: new Date('2023-12-20T12:00:00'),
        deleteRequestDate: new Date('2023-12-21T11:30:00'),
    },
]);

function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
    }).format(new Date(date));
}

function editRequest(id) {
    console.log('Edit Request ID:', id);
}

function confirmRequest(id) {
    console.log('Confirm Request ID:', id);
}
</script>

<style scoped>
.account-request-container {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.table-auto {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
th {
    background-color: #f4f4f4;
}
</style>
