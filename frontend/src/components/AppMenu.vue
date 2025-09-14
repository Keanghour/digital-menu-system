<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';


const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }],
    },
    {
        items: [{ label: 'User Management', icon: 'pi pi-fw pi-users', to: '/userManagement' }]
    },

    {
    icon: 'pi pi-fw pi-briefcase',
    to: '/products',
    items: [
        {
            label: 'Products',
            icon: 'pi pi-fw pi-shopping-cart',
            items: [
                {
                    label: 'Products',
                    icon: 'pi pi-fw pi-box',
                    to: '/products/product'
                },
                {
                    label: 'Stocks',
                    icon: 'pi pi-fw pi-table',
                    to: '/products/stock'
                },
                {
                    label: 'Add Product & Stock',
                    icon: 'pi pi-fw pi-th-large',
                    to: '/products/controllerlist'
                }
            ]
        }
    ]
    },

    {
    icon: 'pi pi-fw pi-briefcase',
    to: '/sale',
    items: [
        {
            label: 'Sales',
            icon: 'pi pi-fw pi-megaphone',
            items: [
                {
                    label: 'Incoive List',
                    icon: 'pi pi-fw pi-tablet',
                    to: ''
                },
                {
                    label: 'Invoice ( Customer )',
                    icon: 'pi pi-fw pi-file-edit',
                    to: ''
                },
                {
                    label: 'Invoice ( Admin )',
                    icon: 'pi pi-fw pi-file-edit',
                    to: ''
                },
                {
                    label: 'Invoice Template',
                    icon: 'pi pi-fw pi-file',
                    to: ''
                }
            ]
        }
    ]
    },
    {
        items: [{ label: 'User', icon: 'pi pi-fw pi-user', to: '/user' }]
    },
    {
        items: [{ label: 'Product', icon: 'pi pi-fw pi-th-large', to: '/product' }]
    },
    {
        items: [{ label: 'Order', icon: 'pi pi-fw pi-truck', to: '/order' }]
    },
    {
        items: [{ label: 'Report', icon: 'pi pi-fw pi-book', to: '/report' }]
    },
    {
        items: [{ label: 'My Wallet', icon: 'pi pi-fw pi-wallet', to: '/wallet' }]
    },
    {
        items: [{ label: 'Notification', icon: 'pi pi-fw pi-bell', to: '/notification' }]
    },
    {
        items: [{ label: 'Setting', icon: 'pi pi-fw pi-cog', to: '/setting' }]
    },


]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
