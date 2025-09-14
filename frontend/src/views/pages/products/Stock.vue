<template>
    <div>
        <div class="card">
            <h3 class="text-center mb-4">Stock List</h3>
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="Add Stock" icon="pi pi-plus" severity="secondary" class="mr-2" @click="navigateToAddStock" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedStocks.length" />
                </template>
                <template #end>
                    <InputText v-model="filters.global.value" placeholder="Search..." />
                </template>
            </Toolbar>

            <DataTable ref="dt" v-model:selection="selectedStocks" :value="stocks" dataKey="id" :paginator="true"
                :rows="10" :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[10, 25, 50]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} stocks">
                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="purchaseId" header="Purchase ID" sortable style="min-width: 12rem"></Column>
                <Column field="itemName" header="Item Name" sortable style="min-width: 16rem"></Column>
                <Column field="image" header="Image" :body="imageBodyTemplate" style="width: 10rem"></Column>
                <Column field="dateComing" header="Date Coming" sortable style="min-width: 10rem"></Column>
                <Column field="expiryDate" header="Expiry Date" sortable style="min-width: 10rem"></Column>
                <Column field="purchasePrice" header="Purchase Price" sortable style="min-width: 10rem">
                    <template #body="slotProps">
                        {{ formatCurrency(slotProps.data.purchasePrice) }}
                    </template>
                </Column>
                <Column field="sellingPrice" header="Selling Price" sortable style="min-width: 10rem">
                    <template #body="slotProps">
                        {{ formatCurrency(slotProps.data.sellingPrice) }}
                    </template>
                </Column>
                <Column field="quantity" header="Quantity" sortable style="min-width: 10rem"></Column>
                <Column field="stockIn" header="Stock In" sortable style="min-width: 10rem"></Column>
                <Column field="stockOut" header="Stock Out" sortable style="min-width: 10rem"></Column>
                <Column field="paymentMode" header="Payment Mode" sortable style="min-width: 10rem"></Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editStock(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteStock(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <!-- Confirm Delete Stock Dialog -->
        <Dialog v-model:visible="deleteStockDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div>
                <p>Are you sure you want to delete this stock?</p>
                <div class="dialog-buttons">
                    <Button label="Yes" icon="pi pi-check" @click="deleteStock" />
                    <Button label="No" icon="pi pi-times" @click="navigateToStock" />
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            stocks: [],
            selectedStocks: [],
            filters: {
                global: { value: null },
            },
            deleteStockDialog: false,
        };
    },
    methods: {
        navigateToAddStock() {
            this.$router.push({ path: 'addstock' });
        },
        navigateToStock() {
            this.$router.push({ path: 'stock' }); // Adjust the path as necessary
        },
        confirmDeleteSelected() {
            this.deleteStockDialog = true;
        },
        deleteStock() {
            this.stocks = this.stocks.filter(stock => !this.selectedStocks.includes(stock));
            this.selectedStocks = [];
            this.deleteStockDialog = false;
        },
        closeDeleteDialog() {
            this.deleteStockDialog = false;
        },
        editStock(stock) {
            // Implement edit functionality if needed
        },
        formatCurrency(value) {
            return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
        },
    },
};
</script>

<style scoped>
.text-center {
    text-align: center;
}

.card {
    padding: 20px;
    margin: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.dialog-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}
</style>
