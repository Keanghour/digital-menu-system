<template>
    <div class="add-stock-container">
        <Tabs value="0">
            <TabList>
                <Tab value="0" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-cart-plus" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Add Product</span>
                </Tab>
                <Tab value="1" as="div" class="flex items-center gap-2">
                    <Avatar icon="pi pi-cart-plus" shape="circle" />
                    <span class="font-bold whitespace-nowrap">Add Stock</span>
                </Tab>
            </TabList>
            <TabPanels>
                <TabPanel value="0" as="p" class="m-0">
                    <AddProduct />
                </TabPanel>
                <TabPanel value="1" as="p" class="m-0">
                    <AddStock />
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
import AddProduct from './AddProduct.vue';
import AddStock from './AddStock.vue';
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
