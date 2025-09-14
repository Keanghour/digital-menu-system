<template>
    <div>
        <div class="card">
            <h3 class="text-center mb-4">Product List</h3>
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="Add Product" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedProducts.length" />
                </template>
                <template #end>
                    <InputText v-model="filters.global.value" placeholder="Search..." />
                </template>
            </Toolbar>

            <DataTable ref="dt" v-model:selection="selectedProducts" :value="products" dataKey="id" :paginator="true"
                :rows="10" :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[10, 25, 50]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} products">
                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="code" header="Code" sortable style="min-width: 12rem"></Column>
                <Column field="name" header="Item Name" sortable style="min-width: 16rem"></Column>
                <Column header="Image" :body="imageBodyTemplate" style="width: 10rem"></Column>
                <Column field="category" header="Category" sortable style="min-width: 10rem"></Column>
                <Column field="brand" header="Brand Name" sortable style="min-width: 10rem"></Column>
                <Column field="quantity" header="Units" sortable style="min-width: 10rem"></Column>
                <Column field="price" header="Price" sortable style="min-width: 8rem">
                    <template #body="slotProps">
                        {{ formatCurrency(slotProps.data.price) }}
                    </template>
                </Column>
                <Column field="inventoryStatus" header="Status" sortable style="min-width: 10rem">
                    <template #body="slotProps">
                        <Tag :value="slotProps.data.inventoryStatus" :severity="getStatusLabel(slotProps.data.inventoryStatus)" />
                    </template>
                </Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editProduct(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteProduct(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <!-- Dialog for adding/editing products -->
        <Dialog v-model:visible="productDialog" :style="{ width: '450px' }" header="Add New Product" :modal="true">
            <div class="add-product-container">
                <form @submit.prevent="saveProduct">
                    <img v-if="product.image" :src="product.image" alt="Product Image" class="block m-auto pb-4" style="width: 100px; height: 100px; object-fit: cover;" />

                    <div class="flex flex-col gap-6">
                        <div class="flex items-center gap-4">
                            <div class="flex-1">
                                <label for="productCode" class="block font-bold mb-3">Product Code</label>
                                <div class="flex gap-4">
                                    <InputText
                                        id="productCode"
                                        v-model.trim="product.code"
                                        placeholder="Enter code manually"
                                        fluid
                                    />
                                    <Button label="Generate" icon="pi pi-refresh" @click="generateProductCode" />
                                </div>
                            </div>
                        </div>

                        <div class="flex items-center gap-4">
                            <div class="flex-1">
                                <label for="name" class="block font-bold mb-3">Name</label>
                                <InputText
                                    id="name"
                                    v-model.trim="product.name"
                                    required
                                    autofocus
                                    :invalid="submitted && !product.name"
                                    fluid
                                />
                                <small v-if="submitted && !product.name" class="text-red-500">Name is required.</small>
                            </div>

                            <div class="flex-1">
                                <label for="imageUpload" class="block font-bold mb-3">Upload Image</label>
                                <input
                                    type="file"
                                    id="imageUpload"
                                    accept="image/*"
                                    @change="onImageUpload"
                                    class="block w-full"
                                />
                            </div>
                        </div>

                        <div>
                            <label for="description" class="block font-bold mb-3">Description</label>
                            <Textarea
                                id="description"
                                v-model="product.description"
                                rows="3"
                                fluid
                            />
                        </div>

                        <div>
                            <label for="brand" class="block font-bold mb-3">Brand Name</label>
                            <InputText
                                id="brand"
                                v-model.trim="product.brand"
                                placeholder="Enter brand name"
                                fluid
                            />
                        </div>

                        <div>
                            <label for="inventoryStatus" class="block font-bold mb-3">Inventory Status</label>
                            <Select
                                id="inventoryStatus"
                                v-model="product.inventoryStatus"
                                :options="statuses"
                                optionLabel="label"
                                placeholder="Select a Status"
                                fluid
                            />
                        </div>

                        <div>
                            <span class="block font-bold mb-4">Category</span>
                            <div class="grid grid-cols-12 gap-4">
                                <div class="flex items-center gap-2 col-span-6">
                                    <RadioButton id="category1" v-model="product.category" name="category" value="Accessories" />
                                    <label for="category1">Accessories</label>
                                </div>
                                <div class="flex items-center gap-2 col-span-6">
                                    <RadioButton id="category2" v-model="product.category" name="category" value="Clothing" />
                                    <label for="category2">Clothing</label>
                                </div>
                                <div class="flex items-center gap-2 col-span-6">
                                    <RadioButton id="category3" v-model="product.category" name="category" value="Electronics" />
                                    <label for="category3">Electronics</label>
                                </div>
                                <div class="flex items-center gap-2 col-span-6">
                                    <RadioButton id="category4" v-model="product.category" name="category" value="Fitness" />
                                    <label for="category4">Fitness</label>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-12 gap-4">
                            <div class="col-span-6">
                                <label for="price" class="block font-bold mb-3">Price</label>
                                <InputNumber
                                    id="price"
                                    v-model="product.price"
                                    mode="currency"
                                    currency="USD"
                                    locale="en-US"
                                    fluid
                                />
                            </div>
                            <div class="col-span-6">
                                <label for="quantity" class="block font-bold mb-3">Quantity</label>
                                <InputNumber
                                    id="quantity"
                                    v-model="product.quantity"
                                    integeronly
                                    fluid
                                />
                            </div>
                        </div>
                    </div>

                    <div class="flex justify-end mt-4">
                        <Button label="Cancel" icon="pi pi-times" text @click="cancel" />
                        <Button label="Save" icon="pi pi-check" type="submit" @click="submitted = true" />
                    </div>
                </form>
            </div>
        </Dialog>

        <!-- Other Dialogs remain unchanged -->
    </div>
</template>

<script setup>
import { ProductService } from '@/service/ProductService';
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Select from 'primevue/selectbutton';
import Textarea from 'primevue/textarea';
import RadioButton from 'primevue/radiobutton';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Toolbar from 'primevue/toolbar';
import Tag from 'primevue/tag';

const products = ref([]);
const productDialog = ref(false);
const deleteProductDialog = ref(false);
const deleteProductsDialog = ref(false);
const product = ref({});
const selectedProducts = ref([]);
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);
const statuses = ref([
    { label: 'In Stock', value: 'instock' },
    { label: 'Out of Stock', value: 'outofstock' }
]);
const toast = useToast();
const router = useRouter(); // Initialize the router

onMounted(async () => {
    try {
        const data = await ProductService.getProducts();
        products.value = data.map(prod => ({
            ...prod,
            image: prod.image ? `https://primefaces.org/cdn/primevue/images/product/${prod.image}` : 'https://primefaces.org/cdn/primevue/images/product/product-placeholder.svg'
        }));
    } catch (error) {
        console.error("Error fetching products:", error);
    }
});

function formatCurrency(value) {
    return value ? value.toLocaleString('en-US', { style: 'currency', currency: 'USD' }) : '';
}

function imageBodyTemplate(rowData) {
    return `<img src="${rowData.image}" alt="${rowData.name}" class="rounded" style="width: 64px; height: auto;" />`;
}

function openNew() {
    router.push({ name: 'addproduct' }); // Navigate to Add Product page
}

function hideDialog() {
    productDialog.value = false;
    submitted.value = false;
}

function saveProduct() {
    submitted.value = true;

    if (product.value.name?.trim()) {
        if (product.value.id) {
            products.value[findIndexById(product.value.id)] = { ...product.value };
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Updated', life: 3000 });
        } else {
            product.value.id = createId();
            products.value.push({ ...product.value });
            toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Created', life: 3000 });
        }
        hideDialog();
    }
}

function editProduct(prod) {
    product.value = { ...prod };
    productDialog.value = true;
}

function confirmDeleteProduct(prod) {
    product.value = prod;
    deleteProductDialog.value = true;
}

function deleteProduct() {
    products.value = products.value.filter(val => val.id !== product.value.id);
    deleteProductDialog.value = false;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Product Deleted', life: 3000 });
}

function findIndexById(id) {
    return products.value.findIndex(product => product.id === id);
}

function createId() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return Array.from({ length: 5 }, () => chars.charAt(Math.floor(Math.random() * chars.length))).join('');
}

function confirmDeleteSelected() {
    deleteProductsDialog.value = true;
}

function deleteSelectedProducts() {
    products.value = products.value.filter(val => !selectedProducts.value.includes(val));
    deleteProductsDialog.value = false;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'Products Deleted', life: 3000 });
}

function getStatusLabel(status) {
    return status === 'instock' ? 'success' : 'danger'; // Adjust severity
}

function generateProductCode() {
    product.value.code = `CODE-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
}

function onImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.src = e.target.result;
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                // Resize canvas to 100x100
                canvas.width = 100;
                canvas.height = 100;
                ctx.drawImage(img, 0, 0, 100, 100);

                // Convert to data URL with 85% quality
                product.value.image = canvas.toDataURL('image/jpeg', 0.85);
            };
        };
        reader.readAsDataURL(file);
    }
}

function cancel() {
    productDialog.value = false;
}
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

.add-product-container {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dialog-content {
    display: flex;
    flex-direction: column;
}

.dialog-buttons {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}

.mb-3 {
    margin-bottom: 1rem;
}

.ml-2 {
    margin-left: 0.5rem;
}
</style>
