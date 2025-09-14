<!-- src/views/pages/UserManagement/Users.vue -->

<script setup>
import { ref, reactive, onBeforeMount, computed } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

const customers1 = ref([]);
const loading1 = ref(true);
const errorMessage = ref('');
const filters1 = reactive({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
});
const defaultImage = 'https://www.pngkit.com/png/full/329-3292528_fire-magic-cover-for-refreshment-center.png';

const currentCustomer = reactive({
    id: null,
    name: '',
    gender: 'Male',
    phone: '',
    email: '',
    address: '',
    profilePicture: defaultImage,
    isActive: true,
});
const customerDialogVisible = ref(false);
const viewDialogVisible = ref(false);
const deleteCustomerDialogVisible = ref(false);
const currentCustomerId = ref(null);
const isEditMode = ref(false);

onBeforeMount(async () => {
    try {
        const response = await fetch('https://fakestoreapi.com/users');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        customers1.value = data.slice(0, 20).map(user => ({
            id: user.id,
            name: `${user.name.firstname} ${user.name.lastname}`,
            gender: user.gender || 'Not specified',
            phone: user.phone || 'Not provided',
            email: user.email,
            address: `${user.address.city}, ${user.address.street}, ${user.address.number}`,
            profilePicture: user.image || defaultImage,
            isActive: Math.random() > 0.5,
        }));
    } catch (error) {
        console.error('Error fetching users:', error);
        errorMessage.value = 'Failed to load customers. Please try again later.';
    } finally {
        loading1.value = false;
    }
});

const showAddCustomerDialog = () => {
    resetCurrentCustomer();
    customerDialogVisible.value = true;
    isEditMode.value = false;
};

const saveCustomer = () => {
    try {
        if (isEditMode.value) {
            const index = customers1.value.findIndex(c => c.id === currentCustomer.id);
            if (index !== -1) {
                customers1.value[index] = { ...currentCustomer };
            } else {
                throw new Error('Customer not found for editing.');
            }
        } else {
            const newId = customers1.value.length ? Math.max(...customers1.value.map(c => c.id)) + 1 : 1;
            customers1.value.push({ ...currentCustomer, id: newId });
        }
        closeDialog();
        errorMessage.value = ''; // Reset error message on successful save
    } catch (error) {
        console.error('Error saving customer:', error);
        errorMessage.value = 'Failed to save customer. Please check the details and try again.';
    }
};

const closeDialog = () => {
    customerDialogVisible.value = false;
    resetCurrentCustomer();
};

const resetCurrentCustomer = () => {
    currentCustomer.id = null;
    currentCustomer.name = '';
    currentCustomer.gender = 'Male';
    currentCustomer.phone = '';
    currentCustomer.email = '';
    currentCustomer.address = '';
    currentCustomer.profilePicture = defaultImage;
    currentCustomer.isActive = true;
};

const editUser = (customer) => {
    Object.assign(currentCustomer, customer);
    customerDialogVisible.value = true;
    isEditMode.value = true;
};

const confirmDeleteUser = (customerId) => {
    currentCustomerId.value = customerId;
    deleteCustomerDialogVisible.value = true;
};

const deleteCustomer = (customerId) => {
    try {
        customers1.value = customers1.value.filter(c => c.id !== customerId);
        deleteCustomerDialogVisible.value = false;
        errorMessage.value = ''; // Reset error message on successful delete
    } catch (error) {
        console.error('Error deleting customer:', error);
        errorMessage.value = 'Failed to delete customer. Please try again.';
    }
};

const viewCustomer = (customer) => {
    Object.assign(currentCustomer, customer);
    viewDialogVisible.value = true;
};
</script>

<template>

    <div class="card">
        <div class="font-semibold text-xl mb-4">Customer Management</div>

        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <DataTable :value="customers1" :paginator="true" :rows="10" dataKey="id" :rowHover="true" :filters="filters1"
            filterDisplay="menu" :loading="loading1" :globalFilterFields="['name', 'gender', 'email']" showGridlines
            stripedRows tableStyle="min-width: 50rem">
            <template #header>
                <div class="flex justify-between items-center">
                    <div class="flex align-items-center">
                        <InputGroup>
                            <InputText v-model="filters1.global.value" placeholder="Keyword" />
                            <Button icon="pi pi-search" severity="success" @click="searchData" />
                        </InputGroup>
                    </div>
                    <div class="flex align-items-center gap-2">
                        <Button label="Import" icon="pi pi-upload" @click="importData" />
                        <Button label="Print" icon="pi pi-print" @click="printData" />
                    </div>
                </div>
            </template>


            <template #empty>No customers found.</template>
            <template #loading>Loading customers data. Please wait.</template>

            <Column header="No" style="min-width: 2rem">
                <template #body="{ index }">
                    {{ index + 1 }}
                </template>
            </Column>

            <Column header="Profile" style="min-width: 4rem">
                <template #body="{ data }">
                    <img :src="data.profilePicture" alt="Profile" style="width: 32px; border-radius: 50%;" />
                </template>
            </Column>

            <Column field="name" header="Name" style="min-width: 10rem" @click="viewCustomer(data)" />
            <Column field="gender" header="Gender" style="min-width: 2rem" />
            <Column field="phone" header="Phone" style="min-width: 10rem" />
            <Column field="email" header="Email" style="min-width: 10rem" />
            <Column field="address" header="Address" style="min-width: 16rem" />
            <Column header="Status" style="min-width: 8rem">
                <template #body="{ data }">
                    <span :class="data.isActive ? 'text-green-500' : 'text-red-500'">
                        <i :class="data.isActive ? 'pi pi-check-circle' : 'pi pi-times-circle'"></i>
                        {{ data.isActive ? ' Active' : ' Inactive' }}
                    </span>
                </template>
            </Column>

            <Column header="Action" style="min-width: 8rem">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editUser(slotProps.data)" />
                    <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteUser(slotProps.data.id)" />
                </template>
            </Column>
        </DataTable>

        <!-- Delete Confirmation Dialog -->
        <Dialog :visible="deleteCustomerDialogVisible" modal @hide="deleteCustomerDialogVisible = false" header="Confirm Deletion">
            <div>Are you sure you want to delete this customer?</div>
            <template #footer>
                <Button label="No" icon="pi pi-times" @click="deleteCustomerDialogVisible = false" class="p-button-text" />
                <Button label="Yes" icon="pi pi-check" @click="deleteCustomer(currentCustomerId)" />
            </template>
        </Dialog>

        <!-- Add/Edit Customer Dialog -->
        <Dialog :visible="customerDialogVisible" modal @hide="closeDialog" :header="isEditMode ? 'Edit Customer' : 'Add Customer'" class="custom-dialog">
            <div class="card-container">
                <div class="card-header">
                    <h4>{{ isEditMode ? 'Edit Customer' : 'Add Customer' }}</h4>
                </div>
                <div class="form-container">
                    <div class="field">
                        <label for="name">Name</label>
                        <InputText id="name" v-model="currentCustomer.name" />
                    </div>
                    <div class="field">
                        <label for="gender">Gender</label>
                        <Dropdown id="gender" v-model="currentCustomer.gender" :options="['Male', 'Female']" placeholder="Select Gender" />
                    </div>
                    <div class="field">
                        <label for="phone">Phone</label>
                        <InputText id="phone" v-model="currentCustomer.phone" />
                    </div>
                    <div class="field">
                        <label for="email">Email</label>
                        <InputText id="email" v-model="currentCustomer.email" />
                    </div>
                    <div class="field">
                        <label for="address">Address</label>
                        <InputText id="address" v-model="currentCustomer.address" />
                    </div>
                    <div class="field">
                        <label for="profilePicture">Profile Picture URL</label>
                        <InputText id="profilePicture" v-model="currentCustomer.profilePicture" />
                    </div>
                    <div class="field">
                        <label for="isActive">Status</label>
                        <Dropdown id="isActive" v-model="currentCustomer.isActive" :options="[{ label: 'Active', value: true }, { label: 'Inactive', value: false }]" placeholder="Select Status" />
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" @click="closeDialog" class="p-button-text" />
                <Button label="Save" icon="pi pi-check" @click="saveCustomer" />
            </template>
        </Dialog>

        <!-- View Customer Dialog -->
        <Dialog
            :visible="viewDialogVisible"
            modal
            @hide="viewDialogVisible = false"
            header="Customer Details"
            class="custom-dialog"
        >
            <div class="card-container">
                <div class="card-header">
                    <h4>Customer Information</h4>
                </div>
                <div class="card-body">
                    <div><strong>Name:</strong> {{ currentCustomer.name }}</div>
                    <div><strong>Gender:</strong> {{ currentCustomer.gender }}</div>
                    <div><strong>Phone:</strong> {{ currentCustomer.phone }}</div>
                    <div><strong>Email:</strong> {{ currentCustomer.email }}</div>
                    <div><strong>Address:</strong> {{ currentCustomer.address }}</div>
                    <div>
                        <strong>Profile Picture:</strong>
                        <img :src="currentCustomer.profilePicture" alt="Profile" class="profile-pic" />
                    </div>
                    <div>
                        <strong>Status:</strong>
                        <span :class="currentCustomer.isActive ? 'text-green-600' : 'text-red-600'">
                            <i :class="currentCustomer.isActive ? 'pi pi-check-circle' : 'pi pi-times-circle'"></i>
                            {{ currentCustomer.isActive ? ' Active' : ' Inactive' }}
                        </span>
                    </div>
                </div>
            </div>
            <template #footer>
                <Button label="Close" icon="pi pi-times" @click="viewDialogVisible = false" class="p-button-text" />
            </template>
        </Dialog>

    </div>
</template>

<style scoped lang="scss">
.form-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.field {
    display: flex;
    flex-direction: column;
}
.text-green-600 {
    color: green;
}
.text-red-600 {
    color: red;
}
.custom-dialog {
    width: 50vw;
    max-width: 600px;
}
.card-container {
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}
.card-header {
    margin-bottom: 1rem;
}
.card-body {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.profile-pic {
    width: 50px;
    border-radius: 50%;
}
.error-message {
    color: red;
    font-weight: bold;
    margin: 1rem 0;
}
</style>
