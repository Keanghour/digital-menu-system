<template>
    <div :class="{ 'dark-theme': isDarkTheme }" class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" @click="onMenuToggle">
                <i class="pi pi-bars"></i>
            </button>
            <router-link to="/" class="layout-topbar-logo">
                <span>Dashboard</span>
            </router-link>
        </div>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="handleToggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
            </div>

            <button class="layout-topbar-action" @click="toggleProfileMenu">
                <i class="pi pi-user"></i>
            </button>
            <div :class="['profile-menu', { 'block': isProfileMenuVisible }]">
                <ul>
                    <li v-for="item in profileMenuItems" :key="item.label" @click="handleMenuClick(item)">
                        <i :class="item.icon"></i> {{ item.label }}
                    </li>
                </ul>
            </div>
        </div>

        <div v-if="isLoading" class="loading-overlay">
            <ProgressSpinner />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useLayout } from '@/components/composables/layout';
import { useRouter } from 'vue-router';
import ProgressSpinner from 'primevue/progressspinner'; // Adjust the import as needed
import { logout } from '@/service/AuthService'; // Import the logout function

const { onMenuToggle, toggleDarkMode: layoutToggleDarkMode, isDarkTheme } = useLayout();
const isProfileMenuVisible = ref(false);
const isLoading = ref(false); // Loading state

const router = useRouter();

// Profile menu items
const profileMenuItems = [
    { label: 'Profile', icon: 'pi pi-user' },
    { label: 'Settings', icon: 'pi pi-cog' },
    { label: 'Logout', icon: 'pi pi-sign-out' }
];

function toggleProfileMenu() {
    isProfileMenuVisible.value = !isProfileMenuVisible.value;
}

function handleToggleDarkMode() {
    layoutToggleDarkMode();
    localStorage.setItem('darkTheme', JSON.stringify(isDarkTheme.value));
}

async function handleMenuClick(item) {
    console.log(`Clicked on ${item.label}`);

    if (item.label === 'Logout') {
        isLoading.value = true;

        await logout(); // Call the logout API

        // Clear tokens from local storage
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');

        // Redirect to login
        router.push({ name: 'login' });

        isLoading.value = false; // Reset loading state
    } else {
        isProfileMenuVisible.value = false;
    }
}

function handleScroll() {
    isProfileMenuVisible.value = false;
}

onMounted(() => {
    const savedTheme = localStorage.getItem('darkTheme');
    if (savedTheme) {
        isDarkTheme.value = JSON.parse(savedTheme);
    }
    document.addEventListener('scroll', handleScroll);
});

onBeforeUnmount(() => {
    document.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.layout-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
}

.profile-menu {
    position: absolute;
    right: 1rem;
    top: 90%;
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 0.50rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    width: 200px;
    display: none;
}

.profile-menu.block {
    display: block;
}

.dark-theme .profile-menu {
    background: black !important;
    border-color: #666 !important;
}

.dark-theme .profile-menu li {
    color: rgb(255, 255, 255) !important;
}

.dark-theme .profile-menu li:hover {
    background-color: #555 !important;
}

.profile-menu ul {
    list-style: none;
    padding: 6px;
    margin: 0;
}

.profile-menu li {
    display: flex;
    align-items: center;
    padding: 0.5rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.profile-menu li:hover {
    background-color: var(--hover-bg-color);
}

.profile-menu i {
    margin-right: 1rem;
}

.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2000;
}
</style>
