<!-- src/views/pages/UserManagement/RolesManagement.vue -->
<template>
    <div class="add-stock-container">
        <Tabs value="0">
            <TabList>
                <Tab value="1" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-cart-plus" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Users</span>
                </Tab>
                <Tab value="0" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-shield" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Role & Permission</span>
                </Tab>
                <Tab value="2" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-list" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Account Request</span>
                </Tab>
                <Tab value="3" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-user-plus" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Add User</span>
                </Tab>
            </TabList>
            <TabPanels>
                <TabPanel value="1" as="p" class="m-0">
                    <Users />
                </TabPanel>
                <TabPanel value="0" as="div" class="m-0">
                    <RolesPermission />
                </TabPanel>
                <TabPanel value="2" as="div" class="m-0">
                    <AccountRequest />
                </TabPanel>
                <TabPanel value="3" as="div" class="m-0">
                    <AddUser /> <!-- Include the AddUser component here -->
                </TabPanel>
            </TabPanels>
        </Tabs>
    </div>
</template>

<script setup>
import Tabs from 'primevue/tabs';
import TabList from 'primevue/tablist';
import Tab from 'primevue/tab';
import TabPanels from 'primevue/tabpanels';
import TabPanel from 'primevue/tabpanel';
import Avatar from 'primevue/avatar';

import Users from './Users.vue';
import RolesPermission from './RolesPermission.vue';
import AccountRequest from './AccountRequest.vue';
import AddUser from './AddUser.vue';

</script>

<style scoped>
.add-stock-container {
    padding: 4px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.text-center {
    text-align: center;
}
</style>
