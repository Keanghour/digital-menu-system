<script setup>
import AnalyticsOrder from '@/components/Analytics/AnalyticsOrder.vue';
import { ref, onMounted, computed } from 'vue';

// Function to generate fake product data
function generateFakeProducts(count) {
    const fakeProducts = [];
    const statuses = [
        { label: "Process", color: "orange" },
        { label: "Pending", color: "blue" },
        { label: "Reject", color: "red" },
        { label: "Done", color: "green" }
    ];

    for (let i = 1; i <= count; i++) {
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        fakeProducts.push({
            no: i,
            image: `${i}.jpg`, // Assuming images are named 1.jpg, 2.jpg, etc.
            name: `Product ${i}`,
            date: new Date().toISOString().split('T')[0],
            status: status.label,
            statusColor: status.color, // Store the color
            amount: (Math.random() * 100).toFixed(2),
            transactionId: `TRANS-${Math.random().toString(36).substr(2, 9).toUpperCase()}`
        });
    }

    return fakeProducts;
}

const products = ref([]);
const searchQuery = ref('');

onMounted(() => {
    products.value = generateFakeProducts(5); // Generate 5 fake products
});

const filteredProducts = computed(() => {
    if (!searchQuery.value) return products.value;
    return products.value.filter(product =>
        product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});
</script>

<template>
    <div class="grid grid-cols-12 gap-8">
        <AnalyticsOrder />
    </div>

    <div class="card">
        <DataTable :value="filteredProducts" stripedRows tableStyle="min-width: 50rem">
            <template #header>
                <div class="flex flex-wrap gap-2 items-center justify-between">
                    <h4 class="m-0">Order Manage </h4>
                    <InputText v-model="searchQuery" placeholder="Search by name..." />
                </div>
            </template>

            <Column field="no" header="No"></Column>
            <Column field="image" header="Image">
                <template #body="slotProps">
                    <img
                        :src="`https://primefaces.org/cdn/primevue/images/product/${slotProps.data.image}`"
                        :alt="slotProps.data.image"
                        class="rounded"
                        style="width: 64px;"
                        @error="(e) => {
                            console.error('Image failed to load:', e);
                            e.target.src = 'https://via.placeholder.com/64';
                        }"
                    />
                </template>
            </Column>
            <Column field="name" header="Name"></Column>
            <Column field="date" header="Date"></Column>
            <Column field="status" header="Status">
                <template #body="slotProps">
                    <span :style="{ color: slotProps.data.statusColor }">
                        {{ slotProps.data.status }}
                    </span>
                </template>
            </Column>
            <Column field="amount" header="Amount"></Column>
            <Column field="transactionId" header="Transaction ID"></Column>
            <Column field="action" header="Action">
                <template #body="slotProps">
                    <select v-model="slotProps.data.status">
                        <option value="Process">Process</option>
                        <option value="Pending">Pending</option>
                        <option value="Reject">Reject</option>
                        <option value="Done">Done</option>
                    </select>
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<style>
.card {
    padding: 20px;
    margin: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
</style>
