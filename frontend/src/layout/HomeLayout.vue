<script setup>
import { Toast } from 'primevue/toast';
import Header from '@/components/HomePage/Header.vue';
</script>

<template>
    <div class="layout-wrapper" :class="containerClass">
        <div class="layout-main-container">
            <Header />
            <div class="layout-main">
                <router-view></router-view>
            </div>
        </div>
        <div class="layout-mask animate-fadein"></div>
    </div>
    <Toast />
</template>
