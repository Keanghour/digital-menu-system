<template>
    <FloatingConfigurator v-if="!isLoginPage" />
    <Toast position="top-right" /> <!-- Toast positioned at the top-right -->
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden relative">
        <div class="flex flex-col items-center justify-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div v-if="loading" class="flex justify-center">
                        <ProgressSpinner /> <!-- Use the spinner from PrimeVue -->
                    </div>
                    <div v-else>
                        <label for="email1" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Email</label>
                        <InputText id="email1" type="text" placeholder="Email address" class="w-full md:w-[30rem] mb-2" v-model="email" />
                        <div v-if="emailError" class="text-red-500 text-sm mb-4">{{ emailError }}</div>

                        <label for="password1" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Password</label>
                        <Password id="password1" v-model="password" placeholder="Password" :toggleMask="true" class="mb-2" fluid :feedback="false"></Password>
                        <div v-if="passwordError" class="text-red-500 text-sm mb-4">{{ passwordError }}</div>

                         <div class="flex items-center justify-between mt-2 mb-8 gap-8"> <!-- http://127.0.0.1:8000/v1/auth/admin/api/login -->
                            <div class="flex items-center">
                                <Checkbox v-model="checked" id="rememberme1" binary class="mr-2"></Checkbox>
                                <label for="rememberme1">Remember me</label>
                            </div>
                            <span class="font-medium no-underline ml-2 text-right cursor-pointer text-primary">Forgot password?</span>
                        </div>
                        <Button label="Sign In" class="w-full" @click="handleLogin"></Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<!-- <script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { login } from '@/service/AuthService'; // Import the login function
import { useToast } from 'primevue/usetoast'; // Import Toast
import ProgressSpinner from 'primevue/progressspinner'; // Import the ProgressSpinner

// const email = ref('');
// const password = ref('');
const email = ref('admin@gmail.com'); // Replace with your static email
const password = ref('password123');   // Replace with your static password
const checked = ref(false);
const router = useRouter(); // Get the router instance
const route = useRoute(); // Get the current route
const emailError = ref(''); // Email error message
const passwordError = ref(''); // Password error message
const loading = ref(false); // Loading state
const toast = useToast(); // Initialize Toast

const isLoginPage = route.name === 'login'; // Check if the current route is the login page

const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email regex
    return re.test(email);
};

const handleLogin = async () => {
    console.log('Attempting login with:', email.value, password.value);

    // Reset previous error messages
    emailError.value = '';
    passwordError.value = '';

    // Validate email and password
    if (!email.value) {
        emailError.value = 'Email is required.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: emailError.value, life: 2000 });
        return;
    } else if (!validateEmail(email.value)) {
        emailError.value = 'Invalid email format.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: emailError.value, life: 2000 });
        return;
    }

    if (!password.value) {
        passwordError.value = 'Password is required.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: passwordError.value, life: 2000 });
        return;
    }

    loading.value = true; // Set loading to true
    try {
        const data = await login(email.value, password.value);
        console.log('API Response:', data);

        if (data.success) {
    if (data.changePasswordRequired) {
        // Redirect to password change page
        router.push({ name: 'change-password' });
    } else {
        localStorage.setItem('token', data.accessToken);
        localStorage.setItem('refreshToken', data.refreshToken);
        toast.add({ severity: 'success', summary: 'Login Successful', detail: 'Welcome back!', life: 3000 });

        // Add delay before redirecting
        await new Promise(resolve => setTimeout(resolve, 3000));
        router.push({ name: 'dashboard' });
    }
}

    } catch (error) {
        console.error('Login failed:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: error.message || 'An unexpected error occurred.', life: 2000 });
    } finally {
        loading.value = false; // Set loading to false after attempt
    }
};

</script> -->


<script setup>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
// ❌ Removed: import { login } from '@/service/AuthService';
import { useToast } from 'primevue/usetoast';
import ProgressSpinner from 'primevue/progressspinner';

// Static credentials (for development)
const email = ref('admin@gmail.com');
const password = ref('password123');
const checked = ref(false);
const router = useRouter();
const route = useRoute();
const emailError = ref('');
const passwordError = ref('');
const loading = ref(false);
const toast = useToast();

const isLoginPage = route.name === 'login';

// ✅ Inline login function
const login = async (email, password) => {
    await new Promise(resolve => setTimeout(resolve, 1000)); // simulate delay

    if (email === 'admin@gmail.com' && password === 'password123') {
        return {
            success: true,
            accessToken: 'fake-access-token',
            refreshToken: 'fake-refresh-token',
            changePasswordRequired: false
        };
    } else {
        throw new Error('Invalid email or password');
    }
};

const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

const handleLogin = async () => {
    console.log('Attempting login with:', email.value, password.value);
    emailError.value = '';
    passwordError.value = '';

    if (!email.value) {
        emailError.value = 'Email is required.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: emailError.value, life: 2000 });
        return;
    } else if (!validateEmail(email.value)) {
        emailError.value = 'Invalid email format.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: emailError.value, life: 2000 });
        return;
    }

    if (!password.value) {
        passwordError.value = 'Password is required.';
        toast.add({ severity: 'warn', summary: 'Validation Error', detail: passwordError.value, life: 2000 });
        return;
    }

    loading.value = true;
    try {
        const data = await login(email.value, password.value);
        console.log('API Response:', data);

        if (data.success) {
            if (data.changePasswordRequired) {
                router.push({ name: 'change-password' });
            } else {
                localStorage.setItem('token', data.accessToken);
                localStorage.setItem('refreshToken', data.refreshToken);
                toast.add({ severity: 'success', summary: 'Login Successful', detail: 'Welcome back!', life: 3000 });

                await new Promise(resolve => setTimeout(resolve, 3000));
                router.push({ name: 'dashboard' });
            }
        }

    } catch (error) {
        console.error('Login failed:', error);
        toast.add({ severity: 'error', summary: 'Error', detail: error.message || 'An unexpected error occurred.', life: 2000 });
    } finally {
        loading.value = false;
    }
};
</script>


<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}

/* Add any additional styles here */
</style>
