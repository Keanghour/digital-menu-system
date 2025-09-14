<template>
    <div class="permission-container">
        <h3 class="text-center mb-4">Permissions for Role: {{ roleName }}</h3>

        <div class="flex justify-between items-center mb-4">
            <span class="font-bold">Role Name: {{ roleName }}</span>
            <label class="flex items-center">
                <input type="checkbox" v-model="allowAllModules" />
                <span class="ml-2">Allow All Modules</span>
            </label>
        </div>

        <table class="table-auto w-full mb-4">
            <thead>
                <tr>
                    <th class="px-4 py-2">No</th>
                    <th class="px-4 py-2">Modules</th>
                    <th class="px-4 py-2">Sub Modules</th>
                    <th class="px-4 py-2">Create</th>
                    <th class="px-4 py-2">Edit</th>
                    <th class="px-4 py-2">Delete</th>
                    <th class="px-4 py-2">View</th>
                    <th class="px-4 py-2">Allow All</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(module, index) in modules" :key="module.id">
                    <td class="border px-4 py-2">{{ index + 1 }}</td>
                    <td class="border px-4 py-2">{{ module.name }}</td>
                    <td class="border px-4 py-2">{{ module.subModule }}</td>
                    <td class="border px-4 py-2">
                        <input type="checkbox" v-model="module.create" />
                    </td>
                    <td class="border px-4 py-2">
                        <input type="checkbox" v-model="module.edit" />
                    </td>
                    <td class="border px-4 py-2">
                        <input type="checkbox" v-model="module.delete" />
                    </td>
                    <td class="border px-4 py-2">
                        <input type="checkbox" v-model="module.view" />
                    </td>
                    <td class="border px-4 py-2">
                        <input type="checkbox" v-model="module.allowAll" />
                    </td>
                </tr>
            </tbody>
        </table>

        <div class="flex justify-end mt-4">
            <Button label="Back" icon="pi pi-arrow-left" @click="goBack" class="mr-2" />
            <Button label="Save" icon="pi pi-check" @click="savePermissions" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';

const router = useRouter(); // Initialize the router
const roleName = ref('Admin'); // Example role name
const allowAllModules = ref(false); // Checkbox state

// Example modules data
const modules = ref([
    { id: 1, name: 'User Management', subModule: 'Accounts', create: false, edit: false, delete: false, view: false, allowAll: false },
    { id: 2, name: 'Product Management', subModule: 'Inventory', create: false, edit: false, delete: false, view: false, allowAll: false },
    // Add more modules as needed
]);

function goBack() {
    // Navigate to the User Management tab and set the active tab
    router.push({ name: 'rolespermission', params: { tab: 1 } }); // Assuming 1 is the index for RolesPermission
}

function savePermissions() {
    // Logic to save permissions
    console.log('Permissions saved:', { roleName: roleName.value, modules: modules.value, allowAll: allowAllModules.value });

    // Navigate to the User Management tab and set the active tab after saving
    router.push({ name: 'rolespermission', params: { tab: 1 } });
}
</script>

<style scoped>
.permission-container {
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
