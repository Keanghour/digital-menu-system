<template>
    <div class="add-stock-container">
        <h3 class="text-center mb-4">Add New Stock</h3>
        <form @submit.prevent="saveStock">
            <div class="flex flex-col gap-6">
                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="purchaseId" class="block font-bold mb-3">Purchase ID</label>
                        <div class="flex gap-4">
                            <InputText
                                id="purchaseId"
                                v-model.trim="stock.purchaseId"
                                required
                                :invalid="submitted && !stock.purchaseId"
                                fluid
                            />
                            <Button label="Generate" icon="pi pi-refresh" @click="generatePurchaseId" />
                        </div>
                        <small v-if="submitted && !stock.purchaseId" class="text-red-500">Purchase ID is required.</small>
                    </div>
                </div>

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="itemName" class="block font-bold mb-3">Item Name</label>
                        <InputText
                            id="itemName"
                            v-model.trim="stock.itemName"
                            required
                            :invalid="submitted && !stock.itemName"
                            fluid
                        />
                        <small v-if="submitted && !stock.itemName" class="text-red-500">Item name is required.</small>
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

                <div class="flex items-center gap-4">
                    <div class="flex-1">
                        <label for="dateComing" class="block font-bold mb-3">Date Coming</label>
                        <DatePicker v-model="stock.dateComing" showIcon fluid :showOnFocus="false"
                            placeholder="Select Date Coming" />
                        <small v-if="submitted && !stock.dateComing" class="text-red-500">Date coming is required.</small>
                    </div>

                    <div class="flex-1">
                        <label for="expiryDate" class="block font-bold mb-3">Expiry Date</label>
                        <DatePicker
                            v-model="stock.expiryDate"
                            showIcon
                            fluid
                            :showOnFocus="false"
                            placeholder="Select Expiry Date"
                        />
                        <small v-if="submitted && !stock.expiryDate" class="text-red-500">Expiry date is required.</small>
                    </div>
                </div>

                <div class="grid grid-cols-12 gap-4">
                    <div class="col-span-6">
                        <label for="purchasePrice" class="block font-bold mb-3">Purchase Price</label>
                        <div class="flex gap-2">
                            <InputGroup>
                                <InputGroupAddon>$</InputGroupAddon>
                                <InputNumber
                                    id="purchasePrice"
                                    v-model="stock.purchasePrice"
                                    mode="currency"
                                    currency="USD"
                                    locale="en-US"
                                    required
                                    :invalid="submitted && stock.purchasePrice === null"
                                />
                                <InputGroupAddon>.00</InputGroupAddon>
                            </InputGroup>
                        </div>
                        <small v-if="submitted && stock.purchasePrice === null" class="text-red-500">Purchase price is required.</small>
                    </div>

                    <div class="col-span-6">
                        <label for="sellingPrice" class="block font-bold mb-3">Selling Price</label>
                        <div class="flex gap-2">
                            <InputGroup>
                                <InputGroupAddon>$</InputGroupAddon>
                                <InputNumber
                                    id="sellingPrice"
                                    v-model="stock.sellingPrice"
                                    mode="currency"
                                    currency="USD"
                                    locale="en-US"
                                    required
                                    :invalid="submitted && stock.sellingPrice === null"
                                />
                                <InputGroupAddon>.00</InputGroupAddon>
                            </InputGroup>
                        </div>
                        <small v-if="submitted && stock.sellingPrice === null" class="text-red-500">Selling price is required.</small>
                    </div>
                </div>

                <div class="">
                    <div class="col-span-6">
                        <label for="quantity" class="block font-bold mb-3">Quantity</label>
                        <InputNumber
                            id="quantity"
                            v-model="stock.quantity"
                            integeronly
                            fluid
                            required
                        />
                        <small v-if="submitted && stock.quantity === null" class="text-red-500">Quantity is required.</small>
                    </div>
                </div>

                <div>
                    <label for="paymentMode" class="block font-bold mb-3">Payment Mode</label>
                    <Select
                        id="paymentMode"
                        v-model="stock.paymentMode"
                        :options="paymentModes"
                        optionLabel="label"
                        placeholder="Select Payment Mode"
                        fluid
                    />
                </div>
            </div>

            <div class="flex justify-end mt-4">
                <Button label="Cancel" icon="pi pi-times" text @click="cancel" />
                <Button label="Save" icon="pi pi-check" type="submit" @click="submitted = true" />
            </div>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Button from 'primevue/button';
import Select from 'primevue/selectbutton';
import DatePicker from 'primevue/datepicker';
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';

const router = useRouter(); // Get the router instance

const stock = ref({
    purchaseId: '',
    itemName: '',
    dateComing: null,
    expiryDate: null,
    purchasePrice: null,
    sellingPrice: null,
    quantity: null,
    stockIn: null,
    stockOut: null,
    paymentMode: null,
    image: null,
});

const paymentModes = ref([
    { label: 'Cash', value: 'cash' },
    { label: 'Credit Card', value: 'creditCard' },
    { label: 'PayPal', value: 'paypal' },
]);

const submitted = ref(false);

function saveStock() {
    if (validateForm()) {
        console.log('Stock saved:', stock.value);
        // Logic to save stock (e.g., API call)
    }
}

function validateForm() {
    return stock.value.purchaseId && stock.value.itemName && stock.value.dateComing &&
           stock.value.expiryDate && stock.value.purchasePrice && stock.value.sellingPrice &&
           stock.value.quantity && stock.value.paymentMode;
}

function cancel() {
    router.push({ path: 'stock' }); // Navigate back to the stock page
}

function generatePurchaseId() {
    stock.value.purchaseId = `PID-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;
}

function onImageUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            stock.value.image = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}
</script>

<style scoped>
.add-stock-container {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.text-center {
    text-align: center;
}
</style>
