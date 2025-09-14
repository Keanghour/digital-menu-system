<template>

    <div class="roles-permission-container">
        <h3 class="text-center mb-4">Roles and Permissions</h3>
        <table class="table-auto w-full">
            <thead>
                <tr>
                    <th class="px-4 py-2">No</th>
                    <th class="px-4 py-2">ID</th>
                    <th class="px-4 py-2">Role Name</th>
                    <th class="px-4 py-2">Created At</th>
                    <th class="px-4 py-2">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(role, index) in roles" :key="role.id">
                    <td class="border px-4 py-2">{{ index + 1 }}</td>
                    <td class="border px-4 py-2">{{ role.id }}</td>
                    <td class="border px-4 py-2">{{ role.name }}</td>
                    <td class="border px-4 py-2">{{ formatDate(role.createdAt) }}</td>
                    <td class="border px-4 py-2">
                        <Button label="Edit Role" icon="pi pi-pencil" @click="editRole(role.id)" />
                        <Button label="Permissions" icon="pi pi-shield" @click="goToPermissions(role.id)" class="ml-2" />
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';

// Define roles
const roles = ref([
    { id: 1, name: 'Admin', createdAt: new Date('2023-12-19T18:12:00') },
    { id: 2, name: 'Editor', createdAt: new Date('2023-12-15T14:30:00') },
    { id: 3, name: 'Viewer', createdAt: new Date('2023-12-20T09:15:00') },
]);

const router = useRouter();

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

function editRole(id) {
    console.log('Edit Role ID:', id);
    // Add navigation logic if necessary
}

function goToPermissions(roleId) {
    router.push({ name: 'permission', params: { id: roleId } });
}
</script>

<style scoped>
.roles-permission-container {
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
