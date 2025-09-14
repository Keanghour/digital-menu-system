<template>
    <div class="add-user-container">
        <h3 class="text-center mb-4">Add New User</h3>
        <form @submit.prevent="submitForm">
            <div class="flex flex-col gap-6">
                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="fullName" class="block font-bold mb-3">Full Name</label>
                        <InputText
                            id="fullName"
                            v-model.trim="user.full_name"
                            required
                            :invalid="submitted && !user.full_name"
                            placeholder="Enter full name"
                            fluid
                        />
                        <small v-if="submitted && !user.full_name" class="text-red-500">Full name is required.</small>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="email" class="block font-bold mb-3">Email</label>
                        <InputText
                            id="email"
                            type="email"
                            v-model.trim="user.email"
                            required
                            :invalid="submitted && !user.email"
                            placeholder="Enter user email"
                            fluid
                        />
                        <small v-if="submitted && !user.email" class="text-red-500">Email is required.</small>
                        <small v-if="submitted && !isValidEmail(user.email)" class="text-red-500">Email must be valid.</small>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="password" class="block font-bold mb-3">Password</label>
                        <Password
                            id="password"
                            v-model="user.password"
                            toggleMask
                            required
                            :invalid="submitted && !user.password"
                            placeholder="Enter password"
                            fluid
                        />
                        <small v-if="submitted && !user.password" class="text-red-500">Password is required.</small>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="passwordConfirmation" class="block font-bold mb-3">Confirm Password</label>
                        <Password
                            id="passwordConfirmation"
                            v-model="user.password_confirmation"
                            toggleMask
                            required
                            :invalid="submitted && !user.password_confirmation"
                            placeholder="Confirm password"
                            fluid
                        />
                        <small v-if="submitted && !user.password_confirmation" class="text-red-500">Password confirmation is required.</small>
                        <small v-if="submitted && user.password !== user.password_confirmation" class="text-red-500">Passwords must match.</small>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="role" class="block font-bold mb-3">Role</label>
                        <Select
                            id="role"
                            v-model="user.role"
                            :options="roles"
                            optionLabel="label"
                            placeholder="Select a role"
                            required
                            :invalid="submitted && !user.role"
                            fluid
                        />
                        <small v-if="submitted && !user.role" class="text-red-500">Role is required.</small>
                    </div>
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <Button label="Cancel" icon="pi pi-times" text @click="cancel" />
                <Button label="Add User" icon="pi pi-check" type="submit" @click="submitted = true" />
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Select from 'primevue/selectbutton';
import Password from 'primevue/password';

const router = useRouter();

const user = ref({
    full_name: '',
    email: '',
    password: '',
    password_confirmation: '',
    role: ''
});

const roles = ref([
    { label: 'Admin', value: 'admin' },
    { label: 'Editor', value: 'editor' },
    { label: 'Viewer', value: 'viewer' },
]);

const submitted = ref(false);

function submitForm() {
    if (validateForm()) {
        console.log('User added:', user.value);
        // Logic to add user (e.g., API call)

        // After successful addition, navigate back to the users tab
        router.push({ name: 'adduser', params: { tab: 0 } }); // Adjust tab index as needed
    }
}

function validateForm() {
    return user.value.full_name &&
           user.value.email &&
           isValidEmail(user.value.email) &&
           user.value.password &&
           user.value.password_confirmation === user.value.password &&
           user.value.role;
}

function isValidEmail(email) {
    return /\S+@\S+\.\S+/.test(email);
}

function cancel() {
    // Navigate back to the users tab
    router.push({ name: 'adduser', params: { tab: 0 } }); // Adjust tab index as needed
}
</script>

<style scoped>
.add-user-container {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.text-center {
    text-align: center;
}
</style>
