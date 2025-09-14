<script setup>
import { ref, computed, onMounted } from 'vue';

const balance = ref(1000.00); // Example initial balance
const transactions = ref([]); // Placeholder for transaction history

// Function to generate fake transaction data
const generateFakeTransactions = (count) => {
    const fakeTransactions = [];

    for (let i = 1; i <= count; i++) {
        const date = new Date();
        date.setDate(date.getDate() - Math.floor(Math.random() * 30)); // Random date in the last 30 days
        const amount = (Math.random() * 100).toFixed(2);
        const type = Math.random() > 0.5 ? 'Deposit' : 'Withdrawal';
        fakeTransactions.push({
            date: date.toISOString().split('T')[0],
            amount,
            type,
        });
    }

    return fakeTransactions;
};

// Populate the transactions with fake data on mounted
onMounted(() => {
    transactions.value = generateFakeTransactions(10); // Generate 10 fake transactions
});

// Dummy functions for deposit and withdraw
const depositFunds = () => {
    alert("Deposit functionality is not implemented yet.");
};

const withdrawFunds = () => {
    alert("Withdraw functionality is not implemented yet.");
};
</script>

<template>
    <div class="card">
        <div class="flex justify-between mb-4">
            <h4 class="m-0">Wallet Overview</h4>
        </div>

        <div class="mb-4">
            <h5>Balance: ${{ balance.toFixed(2) }}</h5>
        </div>

        <div class="flex mb-4">
            <button @click="depositFunds" class="mr-2">Deposit</button>
            <button @click="withdrawFunds">Withdraw</button>
        </div>

        <h5>Transaction History</h5>
        <DataTable :value="transactions" stripedRows tableStyle="min-width: 50rem">
            <Column field="date" header="Date"></Column>
            <Column field="amount" header="Amount"></Column>
            <Column field="type" header="Transaction Type"></Column>
        </DataTable>
    </div>
</template>

<style scoped>
.card {
    padding: 20px;
    margin: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
button {
    margin-left: 10px;
    padding: 5px 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
button:hover {
    background-color: #0056b3;
}
</style>
